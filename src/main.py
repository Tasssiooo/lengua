import argparse

from utils import config


def main():
    parser = argparse.ArgumentParser(
        prog="Lengua",
        description="Creates and updates Anki decks and notes from terms.",
        usage="lengua [-h] [-c <collection>] <input> <source> <target> {cam|wik|rev}",
    )
    parser.add_argument(
        "-c",
        "--collection",
        metavar="<collection>",
        help="path to 'collection.anki2'",
    )
    parser.add_argument(
        "input",
        metavar="<input>",
        nargs="?",
        help="path to terms file (ex.: path/to/file.txt)",
    )
    parser.add_argument(
        "source",
        metavar="<source>",
        nargs="?",
        help="terms language (pt, es, en, etc.)",
    )
    parser.add_argument(
        "target",
        metavar="<target>",
        nargs="?",
        help="language for translation (pt, es, en, etc.)",
    )
    parser.add_argument(
        "dictionary",
        choices=["cam", "wik", "rev"],
        metavar="{cam|wik|rev}",
        nargs="?",
        help="choose the dictionary: Cambridge, Wiktionary or Reverso",
    )

    args = parser.parse_args()

    if args.collection:
        config.set_collection(args.collection)

    if args.input:
        with open(args.input) as terms:
            match args.dictionary:
                case "cam":
                    ...
                case "rev":
                    ...
                case "wik":
                    ...
                case _:
                    print(f'Unknown source: "{args.source}"')


if __name__ == "__main__":
    main()
