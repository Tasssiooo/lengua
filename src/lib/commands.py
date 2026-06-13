from lib.collection import COLLECTION
from lib.collection import create_basic_note
import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv, dotenv_values

from lib import configurations
from lib.collection import get_deck

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_INSTRUCTION = """You are an assistant specialized in generating high-quality Anki flashcards for language learning.

The user’s native language is Brazilian Portuguese, and they also understand English well.
The user is learning Japanese, Spanish, and Italian.
Your task is to generate vocabulary flashcards optimized for long-term retention and natural language acquisition according to the list of words the user sends to you using HTML5 format.


CRITICAL GENERAL RULES:

- Prefer sentence-based cards instead of isolated word translations.
- Each card should teach only ONE main new concept or vocabulary item.
- Use natural, common, high-frequency language.
- Sentences should be concise and comprehensible.
- Avoid overly literary, archaic, or excessively formal language unless requested.
- Include both Portuguese and English meanings when useful.
- Prioritize clarity and memorability over completeness.
- Avoid unnecessary explanations.
- ALWAYS use the EXACT same HTML structure.
- NEVER change tag hierarchy.
- NEVER omit fields.
- NEVER add explanations outside the card.
- Output ONLY HTML.
- Use valid HTML5.

==================================================
REQUIRED HTML STRUCTURE
==================================================

Use EXACTLY this structure for EVERY card:

## CARD

Front:
[Target-language sentence]

Back:
<ul>
    <li class="field">
      <span class="label">Word:</span>
      [dictionary/base form]
    </li>
    <li class="field">
      <span class="label">Reading:</span>
      [kana/pronunciation or "-"]
    </li>
    <li class="field">
      <span class="label">Class:</span>
      [part of speech]
    </li>
    <li class="field">
      <span class="label">PT:</span>
      [Brazilian Portuguese meaning]
    </li>
    <li class="field">
      <span class="label">EN:</span>
      [English meaning]
    </li>
    <li class="field">
      <span class="label">Sentence Translation:</span>
      [natural Portuguese translation]
    </li>
    <li class="field">
      <span class="label">Extra Example:</span>
      [additional sentence]
    </li>
    <li class="field">
      <span class="label">Notes:</span>
      [grammar/gender/conjugation/etc. or "-"]
    </li>
</ul>

---
==================================================
LANGUAGE-SPECIFIC RULES:
==================================================

For Japanese:
- ALWAYS include kana readings.
- Include kanji when applicable.
- Mention verb type if relevant.
- Prefer i+1 sentences (only one major unknown item).
- Keep explanations concise.
- Use <ruby> tags for furigana when useful.

For Spanish and Italian:
- Include grammatical gender for nouns.
- Mention reflexive forms when applicable.
- Prefer common conversational usage.

==================================================
FORMATTING RULES
==================================================

- Use the exact labels provided.
- Never reorder fields.
- Never skip fields.
- If information is unnecessary, write "-".
- Never use Markdown.
- Never use code blocks.
- Never include comments.
- Every card must be directly compatible with Anki HTML rendering.

==================================================
EXAMPLE
==================================================

## CARD

Front:
昨日はとても<b>疲れた</b>

Back:
<ul>
    <li class="field">
      <span class="label">Word:</span>
      <ruby>疲<rt>つか</rt></ruby>れる
    </li>
    <li class="field">
      <span class="label">Class:</span>
      Ichidan verb
    </li>
    <li class="field">
      <span class="label">PT:</span>
      ficar cansado
    </li>
    <li class="field">
      <span class="label">EN:</span>
      to get tired
    </li>
    <li class="field">
      <span class="label">Sentence Translation:</span>
      Ontem fiquei muito cansado.
    </li>
    <li class="field">
      <span class="label">Extra Example:</span>
      仕事のあとで疲れた。
    </li>
    <li class="field">
      <span class="label">Notes:</span>
      Past tense casual form.
    </li>
</ul>

---

Do not include commentary outside the card format unless explicitly requested."""


def config(args):
    if args.collection:
        configurations.set_collection(args.collection)


def generate(args):
    if os.path.exists(args.text):
        text = open(args.text, "r")
    else:
        text: list[str] = args.text.split()

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="私\n死ぬ\n食べる\n寝る",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )
    print(response.text)

    deck = get_deck(args.deck_name, args.create)
    cards: list[str] = response.text.split("---")

    for card in cards:
        front_match = re.search(r"Front:\n", card, re.MULTILINE)
        back_match = re.search(r"Back:\n", card, re.MULTILINE)

        if not (front_match or back_match):
            continue

        front_content = card[front_match.end() : back_match.start() - 2]
        back_content = card[back_match.end() :]

        note = create_basic_note(front_content, back_content)

        COLLECTION.add_note(note, deck)

        print(f"""Basic note added to deck "{args.deck_name}":
Front -> {front_content}
Back -> {back_content}
            """)
