from presidio_analyzer import PatternRecognizer, RecognizerRegistry
from presidio_analyzer.nlp_engine import NlpEngine
from analyser.recognizers.dob_recognizer import DobRecognizer
from analyser.recognizers.dni_recognizer import DniRecognizer
from analyser.recognizers.phone_recognizer import PhoneRecognizer
from analyser.recognizers.address_recognizer import AddressRecognizer
from analyser.recognizers.postal_code_city_recognizer import PostalCodeCityRecognizer
from presidio_analyzer.predefined_recognizers import SpacyRecognizer


class RecognizerRegistryWrapper:
    def __init__(self,
            recognizers: list[str] = None,
            languages: list[str] = ["es", "en"],
            engine: NlpEngine = None) -> None:
        self._registry = RecognizerRegistry(supported_languages = languages)
        self._registry.add_nlp_recognizer(nlp_engine=engine)

        # Load recognisers by name
        self._recognizers = []
        if recognizers:
            for name in recognizers:
                recognizer = self.__retrieve_recognizer_by_name(name)
                if recognizer:
                    self._registry.add_recognizer(recognizer)
                    self._recognizers.append(name)

    def get_registry(self):
        return self._registry
    
    def __custom_recognizers(self) -> dict[str, PatternRecognizer]:
        return {
            "DOB": DobRecognizer(),
            "DNI": DniRecognizer(),
            "PHONE": PhoneRecognizer(),
            "ADDRESS": AddressRecognizer(),
            "POSTAL_CODE_CITY": PostalCodeCityRecognizer(),
            "PERSON": SpacyRecognizer(supported_entities=["PERSON"], supported_language="es"),
            "LOCATION": SpacyRecognizer(supported_entities=["LOCATION"], supported_language="es"),
            "ORG": SpacyRecognizer(supported_entities=["ORG"], supported_language="es"),
            "EMAIL": SpacyRecognizer(supported_entities=["EMAIL"], supported_language="es"),
        }
    
    def __retrieve_recognizer_by_name(self, name: str) -> PatternRecognizer:
        return self.__custom_recognizers().get(name, None)

    def check_recognizer(self, name: str) -> bool:
        return name in self._recognizers