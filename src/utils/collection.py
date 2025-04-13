import os
import sys

from configparser import ConfigParser, NoSectionError, NoOptionError
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
        print(f"Configuration file invalid: section '{e.section}' is missing.")
        sys.exit(1)
    except NoOptionError as e:
        print(
            f"Configuration file invalid: value '{e.option}' of '{e.section}' section not found."
        )
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


def get_vocabulary_model():
    model = COLLECTION.models.by_name("Vocabulary")

    if not model:
        model = COLLECTION.models.new("Vocabulary")
        template = COLLECTION.models.new_template("Vocabulary")

        template["qfmt"] = (
            "{{Word}}\n<span id=pos>({{Part of Speech}})</span>\n</br>\n<span id=example>{{Example}}</span>"
        )
        template["afmt"] = (
            "{{FrontSide}}\n<hr id=answer>\n{{Meaning}}\n</br>\n<span id=translations>{{Translations}}</span>"
        )

        model["flds"] = [
            COLLECTION.models.new_field("Word"),
            COLLECTION.models.new_field("Part of Speech"),
            COLLECTION.models.new_field("Example"),
            COLLECTION.models.new_field("Meaning"),
            COLLECTION.models.new_field("Translations"),
        ]
        model["tmpls"] = [template]
        model[
            "css"
        ] = """
        .card {
            font-family: Cantarell;
            font-size: 20px;
            text-align: center;
            color: black;
            background-color: white;
        }

        #pos {
            font-size: 16px;
        }
        #example, #translations {
            line-height: 4rem;
        }
        """

        COLLECTION.models.add(model)

    return model


def create_vocabulary_note(
    word: str, part_of_speech: str, example: str, meaning: str, translations: str
):
    """
    Creates a 'Vocabulary' type note and returns it.
    """
    model = get_vocabulary_model()

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


def update_deck(deck_id: DeckId, fields_list: list[dict[str, str]]):

    for fields in fields_list:
        vocabulary_note = create_vocabulary_note(
            fields["word"],
            fields["part of speech"],
            fields["example"],
            fields["meaning"],
            fields["translations"],
        )

        COLLECTION.add_note(vocabulary_note, deck_id)

        print(
            f"""
[status]
    word -> {fields["word"]}
    part_of_speech -> {fields["part of speech"]}
    example -> {fields["example"]}
    meaning -> {fields["meaning"]}
    translations -> {fields["translations"]}"""
        )
