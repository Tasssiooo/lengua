import os
import sys

from configparser import ConfigParser
from pathlib import Path


if sys.platform == "linux" or sys.platform == "darwin":
    config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
else:
    # Assumes it's Windows
    config_dir = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))

CONFIG_FILE_PATH = config_dir / "lengua.conf"


def set_collection(collection_path: str):
    """
    Writes a .conf file and sets the value 'path' of 'collection' section
    to the path to your 'collection.anki2' file.
    """

    config = ConfigParser()

    if not config.has_section("collection"):
        config.add_section("collection")

    config.set("collection", "path", collection_path)

    with open(CONFIG_FILE_PATH, "w") as lengua_conf:
        config.write(lengua_conf)
