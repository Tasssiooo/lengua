import argparse

from utils.commands import config, update


def main():
    parser = argparse.ArgumentParser(
        prog="lengua",
        description="Creates and updates Anki decks and notes from terms and expression.",
    )
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Config subparser
    config_parser = subparsers.add_parser("config", help="manage configuration")
    config_parser.add_argument(
        "-col",
        "--collection",
        metavar="<path>",
        help="Path to 'collection.anki2'",
    )

    # Update subparser
    update_parser = subparsers.add_parser("update", help="manage decks")
    update_parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="create a new deck based on <deck_name> if it doesn't exist",
    )
    update_parser.add_argument(
        "deck_name", metavar="<deck_name>", help="the name of the deck"
    )
    update_parser.add_argument(
        "text",
        metavar="<text>",
        help="some type of text, could be a plain text file or a string.",
    )
    update_parser.add_argument("source", metavar="<source>", help="the text language")
    update_parser.add_argument(
        "target", metavar="<target>", help="the translation language"
    )
    update_parser.add_argument(
        "dictionary",
        choices=["cambridge", "reverso", "wiktionary"],
        metavar="<dictionary>",
        help="Cambridge, Reverso or Wiktionary",
    )

    args = parser.parse_args()

    match args.command:
        case "config":
            config(args)
        case "update":
            update(args)


if __name__ == "__main__":
    main()
