# Objectives:
# - Handle collections
# - Handle creation of decks
# - Handle creating of notes
# - Handle templates and card types


# Path -> Collection
# Get a Path to a anki2 file and returns a Collection.
def get_collection(path): ...


# DeckId -> Deck
# Get a DeckId and returns a Deck whose id equals DeckId.
# If no deck is found, then it returns a new one.
def get_deck(id): ...


# Str Str -> Note
# Get two Str arguments to generate a Basic type note; first argument is
# Front and the second one is Back.
def create_basic_note(front: str, back: str): ...


# todo
def create_typein_note(front: str, back: str): ...


# todo
def create_cloze_note(text: str, back_extra: str): ...
