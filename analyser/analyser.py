from dataclasses import dataclass
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

from analyser.recogniser import RecognizerRegistryWrapper
import utils.logger as logger

DEFAULT_ANALYSER_CONFIG = {
    "nlp_engine_name": "spacy",
    "models": [
        {"lang_code": "es", "model_name": "es_core_news_md"},
        {"lang_code": "en", "model_name": "en_core_web_lg"},
    ],
}

DEFAULT_RECOGNIZERS = ["DOB", "DNI", "PHONE", "ADDRESS", "POSTAL_CODE_CITY", "PERSON", "LOCATION", "ORG", "EMAIL"]

@dataclass
class SensitiveText:
    text_type: str
    words: list[str]

class OCRAnalyser:
    def __init__(self, 
            analyser_config: dict = DEFAULT_ANALYSER_CONFIG,
            recognizers: list[str] = DEFAULT_RECOGNIZERS,
            excluded_recognizers: list[str] = [],
            filtered_words: list[str] = [],
            unfiltered_words: list[str] = []):
        # Initialise engine
        engine = NlpEngineProvider(nlp_configuration=analyser_config).create_engine()

        # Get supported languages
        supported_languages = [model["lang_code"] for model in analyser_config["models"]]

        # Get recognizers
        if recognizers:
            self.recognizers = recognizers
        else:
            self.recognizers = DEFAULT_RECOGNIZERS
        
        if excluded_recognizers:
            self.recognizers = [rec for rec in self.recognizers if rec not in excluded_recognizers]

        # Initialise recogniser registry
        self.registry_wrapper = RecognizerRegistryWrapper(
            languages = supported_languages, 
            recognizers = self.recognizers,
            engine = engine)
        registry = self.registry_wrapper.get_registry()

        # Get filter/unfiltered words
        self.filtered_words = []
        if filtered_words:
            self.filtered_words = filtered_words

        self.unfiltered_words = []
        if unfiltered_words:
            self.unfiltered_words = unfiltered_words            

        # Initialise analyser
        self.analyser = AnalyzerEngine(nlp_engine=engine, registry=registry, supported_languages=supported_languages)

    def analyse_text(self, text: str, language: str) -> list[SensitiveText]:
        results = self.analyser.analyze(text=text, language=language)

        sensitive_texts = []
        for result in results:
            # Check if entity type is a registered recognizer
            if self.registry_wrapper.check_recognizer(result.entity_type):
                text_type = result.entity_type
                words = text[result.start:result.end].split()

                # Filter out words
                words = [word for word in words if word not in self.unfiltered_words]

                # Check if words are not empty
                if len(words) > 0:
                    sensitive_texts.append(SensitiveText(text_type=text_type, words=words))

        # Check for other sensitive words
        if len(self.filtered_words) > 0:   
            sensitive_texts.append(SensitiveText(text_type="OTHER", words=self.filtered_words))
        
        return sensitive_texts

    def analyse_text_to_string(self, text: str, language: str, debug: bool = False) -> list[str]:
        sensitive_texts = self.analyse_text(text, language)
        if debug:
            logger.log("Recognizers", self.recognizers)
            logger.log("Sensitive texts", sensitive_texts)
        sensitive_words = list(set(word for sublist in sensitive_texts for word in sublist.words))
        return sensitive_words