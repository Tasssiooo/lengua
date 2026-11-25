import os
import requests
from ollama import chat
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_MODEL = os.getenv("GEMINI_API_MODEL")

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

SYSTEM_INSTRUCTION = """
You are an assistant specialized in generating
high-quality Anki flashcards for language learning.

The user's native language is Brazilian Portuguese.
He also speaks English, Spanish and Italian.

Your task is to generate Anki-ready vocabulary
flashcards from the list of words provided.

## TRANSLATIONS:

Focus primarily on Portuguese translations.
English, Spanish and Italian equivalents can be
included when they provide additional meaning.

## QUALITY:

Prioritize accuracy, natural translations and
useful linguistic information. Ignore duplicates.

## OUTPUT CONSISTENCY RULES

Follow these rules for every card:

1. WORD
   - Always use the dictionary form.
   - Never include articles unless they are an intrinsic part of the word.

2. PART OF SPEECH
   - Always use English grammatical labels.
   - Use singular labels: noun, verb, adjective, adverb, etc.
   - Never alternate between equivalent labels.

3. WORD MEANING
   - Write in Portuguese.
   - Use concise translations.
   - Separate multiple meanings using semicolons.
   - Do not include explanations, labels, or parenthetical comments.

4. EXAMPLE SENTENCE
   - Provide exactly one sentence.
   - Use natural, everyday language.
   - Prefer relatively simple sentences.
   - The target word must appear in its appropriate grammatical form.
   - Do not use quotation marks.

5. SENTENCE MEANING
   - Translate the entire example sentence into Portuguese.
   - Preserve its meaning and grammatical context.
   - Do not provide alternative translations.

6. NOTES
   - Keep notes to one or two short sentences.
   - Include only information that helps distinguish the word's meaning,
     grammatical behavior, or usage.
   - Do not repeat information already present in word_meaning.
   - Return null when no relevant information exists.

IMPORTANT:
Consistency is more important than stylistic variety.
Use the same formatting conventions across all cards.
Do not introduce new formatting styles or additional information.

## MULTIPLE PARTS OF SPEECH

A single word may belong to multiple grammatical categories (parts of speech).

You must identify all relevant grammatical categories of each input word.

Follow these rules:

1. Generate a separate card for each distinct grammatical category.
2. Each card must represent a genuine use of the word in that category.
3. Provide a different example sentence demonstrating that specific grammatical function.
4. The translation must correspond to the word's meaning in that particular context.
5. Do not create duplicate cards for synonymous grammatical labels.
6. Do not invent grammatical categories or force a word into a category it does not belong to.
7. If a word has only one relevant grammatical category, generate only one card.

IMPORTANT:
Do not assume that a word has only one grammatical category.
Analyze its possible grammatical functions before generating the cards."""

FREEDICTIONARY_API = "https://freedictionaryapi.com/api/v1/entries/{}/{}"

PREFERRED_TAGS = {
    "en": {"General-American"},
    # Add other dialect preferences when needed.
}

# GOOGLE_TTS = "https://translate.google.com/translate_tts?ie=UTF-8&q={}&tl={}&total=1&idx=0&textlen=999&tk=350535.255567&client=webapp&prev=input"

import logfire

logfire.configure()
logfire.instrument_pydantic(record="all")


class CardStruct(BaseModel):
    # model_config = ConfigDict(extra="ignore")

    word: str = Field(
        description="The dictionary form (lemma) of the word. Never use an inflected form unless it is itself the dictionary form."
    )

    pos: str = Field(
        description="The grammatical category. Always use a consistent English label, such as noun, verb, adjective, adverb, preposition, conjunction, or interjection."
    )

    word_meaning: str = Field(
        description="A concise Portuguese translation. Prefer the most common meaning in ordinary usage. Do not include explanations or example sentences."
    )

    sentence: str = Field(
        description="One natural, grammatically correct example sentence in the target language. Use everyday vocabulary and demonstrate the target word's meaning."
    )

    sentence_meaning: str = Field(
        description="A natural Portuguese translation of the example sentence. Preserve the original meaning without adding explanations."
    )

    notes: Optional[str] = Field(
        default=None,
        description="Optional brief grammatical or usage information. Include only relevant information that helps understand the word. Return null if no useful information exists.",
    )


class Cards(BaseModel):
    # model_config = ConfigDict(extra="forbid")

    cards: List[CardStruct]


def get_terms_data(
    input: str, lang: Literal["en", "es", "it", "ja"]
) -> list[dict[str, str]]:

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {"role": "user", "content": input},
        ],
        think=False,
        options={"num_ctx": 16384, "num_predict": 8192, "temperature": 0.2},
        format=Cards.model_json_schema(),
    )

    cards = Cards.model_validate_json(response.message.content).model_dump()

    print(cards["cards"])

    for card in cards["cards"]:
        get_ipa(card, lang)

    return cards["cards"]


def get_ipa(card: dict[str, str], lang: str) -> None:
    url = FREEDICTIONARY_API.format(lang, card["word"])

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        result = response.json()
    except (requests.RequestException, ValueError):
        return None

    print(result)
    print(card)

    pronunciations = result["entries"][0].get("pronunciations", [])

    # Collect valid IPA transcriptions for the requested POS
    candidates = []

    for pronunciation in pronunciations:

        ipa = pronunciation.get("text")

        if not ipa:
            continue

        candidates.append({"ipa": ipa, "tags": pronunciation.get("tags", [])})

    if not candidates:
        return None

    # First pass: preferred dialect
    preferred_tags = PREFERRED_TAGS.get(lang, set())

    for candidate in candidates:
        if preferred_tags.intersection(candidate["tags"]):
            card["ipa"] = candidate["ipa"]
            return None

    # Second pass: first available valid IPA
    card["ipa"] = candidates[0]["ipa"]
    return None


def get_image(cards): ...
