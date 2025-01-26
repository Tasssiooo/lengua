import sys

from anki.collection import Collection

# Objectives:
# - Handle collections
# - Handle creation of decks
# - Handle creating of notes
# - Handle templates and card types


# Path -> Collection
# Get a Path to a anki2 file and returns a Collection.
def get_collection(path: str) -> Collection:
    try:
        return Collection(path)
    except Exception as e:
        print(f"Error getting collection: {e}")
        sys.exit(1)


# DeckId -> Deck
# Get a DeckId and returns a Deck whose id equals DeckId.
# If no deck is found, then it returns a new one.
def get_deck(collection: Collection, name: str, new: bool = False):
    deck_id = collection.decks.id(name, new)
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
    col = get_collection("/home/tassio/.local/share/Anki2/Tassio/collection.anki2")
    print(f"get_collection: {col}")
    deck = get_deck(col, "deck test", True)
    print(f"get_deck: {deck}")
