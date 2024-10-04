from typing import List, Optional

from presidio_analyzer import Pattern, PatternRecognizer


class AddressRecognizer(PatternRecognizer):
    """
    Recognize spanish address using regex.

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
            "address",
            r"\b(?:Av|Avenida|Calle|C|C/|Av/|Avda|Paseo|Pso|Plaza|Plz|Pl)\.?\/?\s*\w+\s*\d+\,?\s*Esc\:\d+\s*\d+\b",
            0.6,
        ),
    ]

    CONTEXT = ["dirección", "calle", "avenida", "paseo", "plaza", "c/", "dom", "domicilio"]

    def __init__(
        self,
        patterns: Optional[List[Pattern]] = None,
        context: Optional[List[str]] = None,
        supported_language: str = "es",
        supported_entity: str = "ADDRESS",
    ):
        patterns = patterns if patterns else self.PATTERNS
        context = context if context else self.CONTEXT
        super().__init__(
            supported_entity=supported_entity,
            patterns=patterns,
            context=context,
            supported_language=supported_language,
        )