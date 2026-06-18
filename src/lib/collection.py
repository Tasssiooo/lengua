import sys

from configparser import NoSectionError, NoOptionError
from anki.collection import Collection
from .configurations import get_config

_COLLECTION = None


def get_collection() -> Collection:
    global _COLLECTION

    try:
        if _COLLECTION is None:
            config = get_config()
            _COLLECTION = Collection(config.get("collection", "path"))

        return _COLLECTION
    except NoSectionError as e:
        sys.exit(f"Configuration file invalid: section '{e.section}' is missing.")
    except NoOptionError as e:
        sys.exit(
            f"Configuration file invalid: value '{e.option}' of '{e.section}' section not found."
        )


def get_deck(name: str, new: bool = False) -> int:
    """
    Searches for a deck by name and returns it.
    If new is True, creates a new deck if not found.
    """
    collection = get_collection()

    deck_id = collection.decks.id(name, new)

    if deck_id:
        return deck_id

    sys.exit(f'Deck "{name}" not found.')


def create_basic_note(front: str, back: str):
    """
    Creates a 'Basic' type note and returns it.
    """
    collection = get_collection()
    model = collection.models.by_name("Basic")

    if model:
        note = collection.new_note(model)
        note["Front"] = front
        note["Back"] = back

        return note

    sys.exit("Error: note 'Basic' type is missing.")


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
    collection = get_collection()
    model = collection.models.by_name("Japanese")

    if not model:
        model = collection.models.new("Japanese")
        template = collection.models.new_template("jp_tmpl")

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
            collection.models.new_field("Word"),
            collection.models.new_field("Word reading"),
            collection.models.new_field("Word meaning"),
            collection.models.new_field("Word furigana"),
            collection.models.new_field("Word audio"),
            collection.models.new_field("Sentence"),
            collection.models.new_field("Sentence meaning"),
            collection.models.new_field("Sentence furigana"),
            collection.models.new_field("Sentence audio"),
            collection.models.new_field("Notes"),
            collection.models.new_field("Pitch accent"),
            collection.models.new_field("Pitch accent notes"),
            collection.models.new_field("Frequency"),
            collection.models.new_field("Image"),
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

        collection.models.add(model)

    note = collection.new_note(model)
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

    return note
