from lib.collection import get_collection, create_japanese_note, create_general_note


def create_japanese_flashcard(term_data: str, deck) -> None:
    fields = dict([field.split(":", 1) for field in term_data.split("\n")])

    note = create_japanese_note(
        word=fields["word"],
        word_reading=fields["word_reading"],
        word_audio="",  # TODO
        word_meaning=fields["word_meaning"],
        word_furigana=fields["word_furigana"],
        sentence=fields["sentence"],
        sentence_meaning=fields["sentence_meaning"],
        sentence_audio="",  # TODO
        sentence_furigana=fields["sentence_furigana"],
        notes=fields["notes"],
        pitch_accent=fields["pitch_accent"],
        pitch_accent_notes=fields["pitch_accent_notes"],
        image="",  # TODO
        frequency=fields["frequency"],
    )

    collection = get_collection()
    collection.add_note(note, deck)

    note_name = fields["word"]
    deck_name = collection.decks.name(deck)

    print(f'Japanese note "{note_name}" added to deck "{deck_name}".')


def create_general_flashcard(term_data: dict[str, str], deck, lang: str):
    note = create_general_note(
        word=term_data["word"],
        word_meaning=term_data["word_meaning"],
        ipa=term_data.get("ipa", ""),
        sentence=term_data["sentence"],
        sentence_meaning=term_data["sentence_meaning"],
        notes=term_data["notes"] or "",
        lang=lang,
    )

    collection = get_collection()
    collection.add_note(note, deck)

    note_name = lang
    deck_name = collection.decks.name(deck)
    lang_name = lang

    print(f'{lang_name} language note "{note_name}" added to deck "{deck_name}"')
