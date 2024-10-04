from typing import List, Optional, Tuple

from presidio_analyzer import Pattern, PatternRecognizer


class PhoneRecognizer(PatternRecognizer):
    """
    Recognize spanish phone number using regex.

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
            "phone number",
            r"\b\d{9}$\b",
            0.6,
        ),
        Pattern(
            "international phone number",
            r"\b\+34\d{9}$\b",
            0.6,
        ),
    ]

    CONTEXT = ["teléfono", "teléfono móvil", "teléfono fijo", "teléfono de contacto", "numero de teléfono", "numero"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "es",
        supported_entity: str = "PHONE",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        self.replacement_pairs = (
            replacement_pairs if replacement_pairs else [(" ", "")]
        )
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )