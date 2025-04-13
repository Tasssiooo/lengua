import os
import sys

from configparser import ConfigParser, NoSectionError
from anki.collection import Collection
from anki.decks import DeckId
from .configurations import CONFIG_FILE_PATH


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


def create_vocabulary_note(
    word: str, part_of_speech: str, example: str, meaning: str, translations: str
):
    """
    Creates a 'Vocabulary' type note and returns it.
    """
    model = COLLECTION.models.by_name("Vocabulary")

    if model:
        note = COLLECTION.new_note(model)
        note["Word"] = word
        note["Part of Speech"] = part_of_speech
        note["Example"] = example
        note["Meaning"] = meaning
        note["Translations"] = translations

        return note

    print("Error: note 'Vocabulary' type is missing.")
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

    print(f'"{front}" note created successfully!')


def update_vocabulary(deck_id: DeckId, term: str, term_data: dict[str, list[str]]):
    for part_of_speech, definitions in term_data.items():
        for definition in definitions:
            meaning = f"<i>({definition[1]})</i> {definition[2]}"
            example = definition[3]
            translations = " - ".join(definition[4:])

            vocabulary_note = create_vocabulary_note(
                term, part_of_speech.casefold(), example, meaning, translations
            )

            COLLECTION.add_note(vocabulary_note, deck_id)
