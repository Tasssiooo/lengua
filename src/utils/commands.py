import os

from utils import configurations
from dictionaries import reverso2anki


def config(args):
    if args.collection:
        configurations.set_collection(args.collection)


def update(args):
    if os.path.exists(args.text):
        text = open(args.text, "r")
    else:
        text = [args.text]

    match args.dictionary:
        # case "cambridge":
        #     # todo
        #     ...
        case "reverso":
            reverso2anki(text, args.deck_name, args.source, args.target, args.create)
        # case "wiktionary":
        #     # todo
