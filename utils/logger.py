from typing import Any

def log(title: str, text: Any) -> None:
    print("#" * 50 + " " + title + " " + "#" * 50)
    print(f"{text}\n")