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


def create_basic_note(front: str, back: str):
    model = COLLECTION.models.by_name("Basic")

    if model:
        note = COLLECTION.new_note(model)
        note["Front"] = front
        note["Back"] = back

        return note
    else:
        print("Error: note 'Basic' type is missing.")
        sys.exit(1)


# todo?
# def create_typein_note(front: str, back: str): ...


# todo?
# def create_cloze_note(text: str, back_extra: str): ...
