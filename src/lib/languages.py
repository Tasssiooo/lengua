from lib.collection import get_collection, create_japanese_note


def create_japanese_flashcards(terms_data: list[str], deck: int) -> None:
    for term_data in terms_data:
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
