import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_MODEL = os.getenv("GEMINI_API_MODEL")
SYSTEM_INSTRUCTION = """You are an assistant specialized in generating high-quality Anki flashcards for language learning.

The user's native language is portuguese, and he also speaks english, spanish and italian.
Your task is to generate Anki-ready vocabulary flashcards from the list of words the user provides.
Focus on portuguese for the translations, but if you find a more meaningful word in any of the other languages, feel free use them."""


class CardStruct(BaseModel):
    word: str = Field(description="The dictionary form of the word.")
    word_meaning: str = Field(description="The translated word.")
    # ¡JAPANESE ONLY!
    word_reading: Optional[str] = Field(
        description="If it's japanese vocabulary: the word reading in hiragana."
    )
    sentence: str = Field(description="An example sentence of how the word is used.")
    # ¡JAPANESE ONLY!
    sentence_furigana: Optional[str] = Field(
        description="If it's japanese vocabulary: the same example sentence with furigana."
    )
    sentence_meaning: str = Field(description="The translated example sentence.")
    notes: Optional[str] = Field(
        description="Some pertinent information about the word if there is any."
    )


class Cards(BaseModel):
    cards: List[CardStruct]


def get_terms_data(input: str) -> list[dict[str, str]]:
    client = genai.Client(api_key=GEMINI_API_KEY)

    interaction = client.interactions.create(
        model=GEMINI_API_MODEL,
        input=input,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": Cards.model_json_schema(),
        },
    )

    cards = Cards.model_validate_json(interaction.output_text).model_dump()

    return cards["cards"]

    # sys.exit(f"Error: for some reason the AI have returned 'None'.")
