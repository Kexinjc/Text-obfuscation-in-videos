from typing import List, Optional, Tuple

from presidio_analyzer import Pattern, PatternRecognizer


class DniRecognizer(PatternRecognizer):
    """
    Recognize DNI number using regex.

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
            "NIF",
            r"\b[0-9]?[0-9]{7}[-]?[A-Z]\b",
            0.6,
        ),
        Pattern(
            "DNI",
            r"\b[0-9]{8}[-]?[A-Z]?\b",
            0.6,
        ),
    ]

    CONTEXT = ["documento nacional de identidad", "DNI", "NIF", "identificación", "D.N.I"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "es",
        supported_entity: str = "DNI",
        replacement_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        self.replacement_pairs = (
            replacement_pairs if replacement_pairs else [("-", ""), (" ", "")]
        )
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )