import os
from lib.ai import get_terms_data
from lib.languages import create_japanese_flashcard, create_general_flashcard
from lib.collection import get_deck
from lib.configurations import set_collection


def config(args):
    if args.collection:
        set_collection(args.collection)


def generate(args):
    input: str = args.text

    if os.path.exists(args.text):
        with open(args.text, "r", encoding="utf-8") as text_file:
            input = text_file.read()

    terms_data = get_terms_data(input, args.klangs, args.llangs)
    deck = get_deck(args.deck_name, args.create)

    for term_data in terms_data:
        if "furigana" in term_data:
            create_japanese_flashcard(term_data, deck)
        else:
            create_general_flashcard(term_data, deck)
