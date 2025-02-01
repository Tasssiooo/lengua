import os
import re
import sys
import io
import pathlib

from typing import TextIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config import CONFIG_FILE_PATH

SUPPORTED_LANGUAGES = [
    {
        "name": "english",
        "url": "https://dictionary.reverso.net/english-definition/",
        "compatible_with": [
            "arabic",
            "german",
            "spanish",
            "french",
            "hebrew",
            "italian",
            "japanese",
            "dutch",
            "polish",
            "portuguese",
            "brazilian",
            "romanian",
            "russian",
            "turkish",
            "chinese",
            "swedish",
        ],
    },
    {
        "name": "portugues",
        "url": "https://dicionario.reverso.net/",
        "compatible_with": ["espanhol", "japones", "italiano", "frances"],
    },
]


def gen_back(content: dict[str, list[str]]):
    back = []

    # pos: part of speech
    # dets: definitons, examples and translations
    for pos, dets in content.items():
        back.append(
            f"""
            <div style="display: flex; box-sizing: border-box; width: 100%;">
                <div style="display: flex; flex-direction: column; width: 100%;">
                    <h2 style="background-color: #bddef9; align-self: flex-start; display: inline-flex; height: 24px;padding: 0 8px; justify-content: center;align-items: center;border-radius: 4px;color: #2e3c43;text-transform: lowercase;font-size: 16px;font-weight: 400;line-height: 24px;">
                        {pos}
                    </h2>
                    <div style="display: flex; flex-direction: column; align-items: start; width: 100%;">
                        {"".join([
                            f"""
                            <div style="position: relative; padding: 12px 0; border-bottom: 1px dashed; width: 100%;">
                                <div style="display: flex; align-items: start; line-height: 20px; flex: 1; position: relative; flex-wrap: wrap; width: 100%;">
                                    <div style="font-size: 14px; line-height: 24px; height: 24px; margin-right: 4px;">{det[0]}</div>
                                    <div style="">
                                        <div style="font-size: 16px; line-height: 24px;">
                                            <span class="parentheses" style="font-weight: 500; white-space: nowrap; position: relative; display: inline-block;">
                                                <i>({det[1]})</i>
                                            </span>
                                            <span class="sentence" style="font-weight: 500;">
                                                {det[2]}
                                            </span>
                                        </div>
                                        <div style="font-size: 14px; line-height: 20px;">
                                            <div style="min-height: 24px; display: flex; align-items: center;">
                                                <span>
                                                    {det[3]}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="translations" style="margin-left: auto; display: flex; justify-content: flex-end; flex-basis: 40%; overflow: hidden; flex-wrap: wrap; max-height: 28px;">
                                        {
                                            "".join([
                                                f"""
                                                <div style="max-width: calc(100% - 6px); margin-right: 4px; white-space: nowrap;">
                                                    <span style="max-width: 100%; overflow: hidden;">
                                                        <span style="display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 4px; border-radius: 6px; color: #2e3c43; font-size: 14px; line-height: 20px; background-color: #e8f3fc;">
                                                            {translation}
                                                        </span>
                                                    </span>
                                                </div>
                                                """
                                                for translation in det[4:] if det[4:]
                                            ])
                                        }
                                    </div>
                                </div>
                            </div>
                            """ 
                            for det in dets
                        ])}
                    </div>
                </div>
            </div>
            """
        )
    return "\n\n".join(back)


def extract(url: str, term: str, source: str, target: str):
    def english_version() -> dict[str, list[str]] | None:
        """
        Content extractor for the english version of the site
        """
        # Ex.: https://dictionary.reverso.net/english-definition/longing#translation=brazilian
        soup = get_soup(f"{url}{term}#translation={target}")

        if not soup:
            print(
                f'Error: something happened while extracting the definition of "{term}"'
            )
            return None

        div_definition_list__pos = soup.select_one(
            "app-definition-nav-tabs ~ div.definition-list__pos"
        )

        if not div_definition_list__pos:
            print(f'Error: "{term}" not available in Reverso.')
            sys.exit(1)
        else:
            app_definition_pos_block = div_definition_list__pos.select(
                "app-definition-pos-block"
            )

        result = {}

        for element in app_definition_pos_block:
            # Part of speech: verb, noun, adjective, etc.
            h2 = element.select("div.definition-pos-block > h2")

            # The definitons, examples and translations
            div_definition_example = element.select(
                "div.definition-pos-block__examples > app-definition-example > div.definition-example"
            )

            part_of_speech = h2[0].get_text(strip=True)
            dets = []

            for tag in div_definition_example:
                text = tag.get_text("\n", True)

                text = re.sub(r"!\n|US\n|UK\n", "", text)

                if not re.match(r"\d.\n.+\n(.+\n){0,2}([^\d]+\n?)*", text):
                    text = "n.\n" + text

                dets.append(text.split("\n"))

            result[part_of_speech] = dets

        return result

    if source == "english":
        return english_version()

    return english_version()


def find_lang(source: str):
    """
    Returns the first item which 'name' key value equals 'source'.
    Otherwise returns None.
    """
    for lang in SUPPORTED_LANGUAGES:
        if lang["name"] == source:
            return lang
    return None


def get_soup(url: str):
    """
    Gets the html text of 'url' and returns the BeautifulSoup instance of it.
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-translate-link"))
        )

        return BeautifulSoup(driver.page_source, "lxml")
    except Exception as e:
        print(e)


def reverso2anki(
    text: TextIO | list[str], deck_name: str, source: str, target: str, create: bool
):
    if os.path.exists(CONFIG_FILE_PATH):
        from utils import collection

        source = source.lower()
        target = target.lower()

        deck = collection.get_deck(deck_name, create)

        lang = find_lang(source)

        # Checks two things:
        # 1. If 'source' is available in this dictionary;
        # 2. If 'source' can be translated to 'target';
        if not lang:
            print(f"Error: {source} not available in Reverso")
            sys.exit(1)
        elif not target in lang["compatible_with"]:
            print(f"Error: {source} is not compatible with {target}.")
            sys.exit(1)
        else:
            url = lang["url"]

        for term in text:
            term = term.strip().lower()

            content = extract(url, term, source, target)

            if not content:
                if isinstance(text, io.TextIOWrapper):
                    error_file_path = pathlib.Path(text.name).with_suffix(".errors")
                else:
                    error_file_path = "~/Documents/reverso.errors"

                with open(error_file_path, "a") as errors:
                    errors.write(term + "\n")
                continue

            back = gen_back(content)

            collection.update_deck(deck, [term, back])

        if isinstance(text, io.TextIOWrapper):
            text.close()
