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
from utils.configurations import CONFIG_FILE_PATH

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

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        opts = webdriver.FirefoxOptions()
        opts.add_argument("--headless")

        _driver = webdriver.Firefox(opts)
    return _driver


def get_soup(url: str):
    """
    Gets the html text of 'url' and returns the BeautifulSoup instance of it.
    """
    try:
        driver = get_driver()
        driver.get("about:blank")
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "app-translate-link"))
        )
        return BeautifulSoup(driver.page_source, "lxml")
    except Exception as e:
        print(e)


def extract(url: str, term: str, source: str, target: str):
    def english_version() -> list[dict[str, str]] | None:
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
            return None
        else:
            app_definition_pos_block = div_definition_list__pos.select(
                "app-definition-pos-block"
            )

        result = []

        for element in app_definition_pos_block:
            # Part of speech: verb, noun, adjective, etc.
            h2 = element.select("div.definition-pos-block > h2")

            # The definitons, examples and translations
            div_definition_example = element.select(
                "div.definition-pos-block__examples > app-definition-example > div.definition-example"
            )

            part_of_speech = h2[0].get_text(strip=True)

            for tag in div_definition_example:
                text = tag.get_text("\n", True)

                text = re.sub(r"!\n|US\n|UK\n", "", text)

                if not re.match(r"\d.\n.+\n(.+\n){0,2}([^\d]+\n?)*", text):
                    text = "n.\n" + text

                def_splited = text.split("\n")

                result.append(
                    {
                        "word": term,
                        "part of speech": part_of_speech.casefold(),
                        "meaning": f"<i>({def_splited[1]})</i> {def_splited[2]}",
                        "example": def_splited[3],
                        "translations": " ー ".join(def_splited[4:]) or "",
                    }
                )

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


def reverso2anki(
    text: TextIO | list[str], deck_name: str, source: str, target: str, create: bool
):
    if os.path.exists(CONFIG_FILE_PATH):
        from utils import collection

        source = source.lower()
        target = target.lower()

        deck = collection.get_deck(deck_name, create)

        lang = find_lang(source)

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

            fields_list = extract(url, term, source, target)

            if not fields_list:
                # Todo: better handling of crossplatform
                if isinstance(text, io.TextIOWrapper):
                    error_file_path = pathlib.Path(text.name).with_suffix(".errors")
                else:
                    error_file_path = pathlib.Path(
                        pathlib.Path.home() / "documents" / "lengua-reverso.errors"
                    )

                with open(error_file_path, "a") as errors:
                    errors.write(term + "\n")
                continue

            collection.update_deck(deck, fields_list)

        if isinstance(text, io.TextIOWrapper):
            text.close()

        get_driver().quit()
