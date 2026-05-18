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

    # Generate subparser
    generate_parser = subparsers.add_parser(
        "generate", help="Sets configuration for deck generation"
    )
    generate_parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="creates a new deck",
    )
    generate_parser.add_argument(
        "deck_name", metavar="<deck_name>", help="the deck name"
    )
    generate_parser.add_argument(
        "text",
        metavar="<text>",
        help="some type of text, it could be a plain text file or a string.",
    )
    generate_parser.add_argument(
        "srclang", metavar="<srclang>", help="the text language"
    )
    generate_parser.add_argument(
        "tarlang", metavar="<tarlang>", help="the translation language"
    )

    args = parser.parse_args()

    match args.command:
        case "config":
            config(args)
        case "generate":
            update(args)


if __name__ == "__main__":
    main()
