from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class PostalCodeCityRecognizer(PatternRecognizer):
    """
    Recognize spanish postal code and city using regex.

    :param patterns: List of patterns to be used by this recognizer
    :param context: List of context words to increase confidence in detection
    :param supported_language: Language this recognizer supports
    :param supported_entity: The entity this recognizer can detect
    :param replacement_pairs: List of tuples with potential replacement values
    for different strings to be used during pattern matching.
    This can allow a greater variety in input, for example by removing dashes or spaces.
    """

    PATTERNS = [
        Pattern(
            "postal code + town + (City)",
            r"\b(?:0[1-9]|1[0-9]|2[0-9]|3[0-4]|[4-5][0-9]|6[0-3]|7[0-8]|[8-9][0-5])\d{3}\b\s+\w+(?:\s+\w+)*(?:\s+\(\w+(?:\s+\w+)*\))?",
            0.6,
        ),
    ]

    CONTEXT = ["código postal", "ciudad", "localidad", "municipio", "provincia", "CP", "c.p."]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "es",
        supported_entity: str = "POSTAL_CODE_CITY",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )