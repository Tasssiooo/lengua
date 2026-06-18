import os
import sys
from lib.ai import get_terms_data
from lib.languages import create_japanese_flashcards
from lib.collection import get_collection, get_deck
from lib.configurations import set_collection


def config(args):
    if args.collection:
        set_collection(args.collection)


def generate(args):
    input: str = args.text

    if os.path.exists(args.text):
        with open(args.text, "r", encoding="utf-8") as text_file:
            input = text_file.read()

    terms_data = get_terms_data(input)
    collection = get_collection()
    deck = get_deck(args.deck_name, args.create)

    match args.srclang:
        case "jp":
            create_japanese_flashcards(terms_data, deck)
            sys.exit(0)
