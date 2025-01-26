from typing import TextIO


COMPATIBILITY = [
    {
        "name": "english",
        "url": "https://dictionary.reverso.net/english-definition/",
        "compatible_with": [
            "arabic",
            "german",
            "spanish",
            "french",
            "hebrew",
            "italian",
            "japanese",
            "dutch",
            "polish",
            "portuguese",
            "brazilian",
            "romanian",
            "russian",
            "turkish",
            "chinese",
            "swedish",
        ],
    },
    {
        "name": "portugues",
        "url": "https://dicionario.reverso.net/",
        "compatible_with": ["espanhol", "japones", "italiano", "frances"],
    },
]


def reverso2anki(
    text: TextIO | list[str], deck_name: str, source: str, target: str, create: bool
):

    for term in text:
        print(term)
