import os
import sys

from configparser import ConfigParser, NoSectionError
from anki.collection import Collection
from anki.decks import DeckId
from .config import CONFIG_FILE_PATH


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
    """
    Searches for a deck by name and returns it.
    If new is True, creates a new deck if not found.
    """
    deck_id = COLLECTION.decks.id(name, new)

    if deck_id:
        return deck_id

    print(f'Deck "{name}" not found.')
    sys.exit(1)


def create_basic_note(front: str, back: str):
    """
    Creates a 'Basic' type note and returns it.
    """
    model = COLLECTION.models.by_name("Basic")

    if model:
        note = COLLECTION.new_note(model)
        note["Front"] = front
        note["Back"] = back

        return note

    print("Error: note 'Basic' type is missing.")
    sys.exit(1)


# todo?
# def create_typein_note(front: str, back: str): ...
# todo?
# def create_cloze_note(text: str, back_extra: str): ...


# For my personal use, I will only use Basic types.
# Handling other card types perhaps in the future (or fork it =T).
def update_deck(deck_id: DeckId, fields: list[str]):
    """
    Updates a deck adding a new note to it.
    """
    front, back = fields
    basic_note = create_basic_note(front, back)
    COLLECTION.add_note(basic_note, deck_id)
