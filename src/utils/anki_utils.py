import os
import sys

from configparser import ConfigParser, NoSectionError
from anki.collection import Collection
from config import CONFIG_FILE_PATH


# Checks if the file "lengua.conf" exists. If so, creates a Collection,
# otherwise, prints an error message;
if os.path.exists(CONFIG_FILE_PATH):
    try:
        config = ConfigParser()
        config.read(CONFIG_FILE_PATH)

        collection_path = config.get("collection", "path")

        COLLECTION = Collection(collection_path)
    except NoSectionError as e:
        print(f"Config file invalid: section '{e.section}' is missing.")
        sys.exit(1)
else:
    print(
        "Error: Collection is None! You must set the path to your collection.anki2 file!"
    )
    sys.exit(1)


def get_deck(name: str, new: bool = False):
    deck_id = COLLECTION.decks.id(name, new)
    if new:
        return deck_id
    else:
        if deck_id:
            return deck_id
        else:
            print(f'Deck "{name}" not found.')
            sys.exit(1)


# Str Str -> Note
# Get two Str arguments to generate a Basic type note; first argument is
# Front and the second one is Back.
def create_basic_note(front: str, back: str): ...


# todo
def create_typein_note(front: str, back: str): ...


# todo
def create_cloze_note(text: str, back_extra: str): ...


if __name__ == "__main__":
    ...
# save_collection("/home/tassio/.local/share/Anki2/Tassio/collection.anki2")
# col = get_collection("/home/tassio/.local/share/Anki2/Tassio/collection.anki2")
# print(f"get_collection: {col}")
# deck = get_deck(col, "deck test", True)
# print(f"get_deck: {deck}")
