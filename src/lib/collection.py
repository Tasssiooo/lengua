import os
import sys

from configparser import ConfigParser, NoSectionError, NoOptionError
from anki.collection import Collection
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


def create_japanese_note(
    word: str,
    word_reading: str,
    word_meaning: str,
    word_furigana: str,
    word_audio: str,
    sentence: str,
    sentence_meaning: str,
    sentence_furigana: str,
    sentence_audio: str,
    notes: str,
    pitch_accent: str,
    pitch_accent_notes: str,
    frequency: str,
    image: str,
):
    model = COLLECTION.models.by_name("Japanese")

    if not model:
        model = COLLECTION.models.new("Japanese")
        template = COLLECTION.models.new_template("jp_tmpl")

        template["qfmt"] = (
            '<div lang="ja">{{Word}}<div style="font-size: 20px;">{{Sentence}}</div></div>'
        )
        template["afmt"] = """<div lang="ja">
{{furigana:Word furigana}}

<!-- This part enables pitch accent.

{{#Pitch accent}}
	<br><div style='font-size: 24px'>{{Pitch accent}}</div>
{{/Pitch accent}} 

-->

<div style='font-size: 25px; padding-bottom:20px'>{{Word meaning}}</div>
<div style='font-size: 25px;'>{{furigana:Sentence furigana}}</div>
<div style='font-size: 25px; padding-bottom:10px'>{{Sentence meaning}}</div>

{{Word audio}}
{{Sentence audio}}
<br>
{{Image}}

{{#Notes}}
	<br>
	<div style="font-size: 20px; padding-top:12px">Note: {{Notes}}</div>
{{/Notes}}

<!-- This part enables pitch accent notes.

{{#Pitch accent notes}}
<div style="font-size: 20px; width: fit-content; max-width:40vw; margin: auto">
	<details><summary>Pitch Accent Notes</summary>
		<br>{{Pitch accent notes}}
	</details>
</div>
{{/Pitch accent notes}}

-->

</div>"""

        model["flds"] = [
            COLLECTION.models.new_field("Word"),
            COLLECTION.models.new_field("Word reading"),
            COLLECTION.models.new_field("Word meaning"),
            COLLECTION.models.new_field("Word furigana"),
            COLLECTION.models.new_field("Word audio"),
            COLLECTION.models.new_field("Sentence"),
            COLLECTION.models.new_field("Sentence meaning"),
            COLLECTION.models.new_field("Sentence furigana"),
            COLLECTION.models.new_field("Sentence audio"),
            COLLECTION.models.new_field("Notes"),
            COLLECTION.models.new_field("Pitch accent"),
            COLLECTION.models.new_field("Pitch accent notes"),
            COLLECTION.models.new_field("Frequency"),
            COLLECTION.models.new_field("Image"),
        ]
        model["tmpls"] = [template]
        model["css"] = """.card {
 font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", "Noto Sans JP", "Noto Sans CJK JP", Osaka, "メイリオ", Meiryo, "ＭＳ Ｐゴシック", "MS PGothic", "MS UI Gothic", sans-serif;
 font-size: 44px;
 text-align: center;
}

img {
max-width: 300px;
max-height: 250px;
}

.mobile img {
max-width: 50vw;
}

/* This part defines the bold color. */
b{color: #5586cd}"""

        COLLECTION.models.add(model)

    note = COLLECTION.new_note(model)
    note["Word"] = word
    note["Word reading"] = word_reading
    note["Word meaning"] = word_meaning
    note["Word furigana"] = word_furigana
    note["Word audio"] = word_audio
    note["Sentence"] = sentence
    note["Sentence meaning"] = sentence_meaning
    note["Sentence furigana"] = sentence_furigana
    note["Sentence audio"] = sentence_audio
    note["Notes"] = notes
    note["Pitch accent"] = pitch_accent
    note["Pitch accent notes"] = pitch_accent_notes
    note["Frequency"] = frequency
    note["Image"] = image

    return model
