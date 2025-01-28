import sys
import io

from typing import TextIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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


def extract(url: str, term: str, source: str, target: str):
    def english_version():
        """
        Content extractor for the english version of the site
        """
        # Ex.: https://dictionary.reverso.net/english-definition/longing#translation=brazilian
        soup = get_soup(f"{url}{term}#translation={target}")

        div_definition_list__pos = soup.select_one(
            "app-definition-nav-tabs ~ div.definition-list__pos"
        )

        if not div_definition_list__pos:
            print("Error: bad formatted page source")
            sys.exit(1)
        else:
            app_definition_pos_block = div_definition_list__pos.select(
                "app-definition-pos-block"
            )

        for element in app_definition_pos_block:
            # Part of speech: verb, noun, adjective, etc.
            h2 = element.select("div.definition-pos-block > h2")

            # The definitons, examples and translations
            div_definition_example = element.select(
                "div.definition-pos-block__examples > app-definition-example > div.definition-example"
            )

            part_of_speech = h2[0].get_text(strip=True)
            dets = [tag.get_text("\n", True) for tag in div_definition_example]

            yield (part_of_speech, dets)

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
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "app-translate-link"))
        )

        return BeautifulSoup(driver.page_source, "lxml")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def reverso2anki(
    text: TextIO | list[str], deck_name: str, source: str, target: str, create: bool
):
    source = source.lower()
    target = target.lower()

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
        # match source:
        #     case "english":
        #         # Ex.: https://dictionary.reverso.net/english-definition/longing#translation=brazilian
        #         extract_eng_ver(f"{url}{term}#translation={target}")
        #     case _:
        #         # todo

        for content in extract(url, term, source, target):
            print(content)

        if isinstance(text, io.TextIOWrapper):
            text.close()
