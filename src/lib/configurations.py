import os
import sys

from configparser import ConfigParser
from pathlib import Path

CONFIG = None


def resolve_config_file_path():
    if sys.platform == "linux":
        config_dir = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    elif sys.platform == "darwin":
        config_dir = Path.home() / "Library" / "Application Support"
    else:
        config_dir = Path(
            os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming"
        )

    config_file_path = config_dir / "lengua" / "lengua.conf"
    config_file_path.parent.mkdir(parents=True, exist_ok=True)

    return config_file_path


def get_collection():
    global CONFIG

    if CONFIG is None:
        CONFIG = ConfigParser()
        CONFIG.read(resolve_config_file_path(), encoding="utf-8")

    return CONFIG


def set_collection(collection_path: str):
    """
    Writes a .conf file and sets the value 'path' of 'collection' section
    to the path to your 'collection.anki2' file.
    """

    config = get_collection()
    config_file_path = resolve_config_file_path()

    if not config.has_section("collection"):
        config.add_section("collection")

    config.set("collection", "path", collection_path)

    with open(config_file_path, "w", encoding="utf-8") as lengua_conf:
        config.write(lengua_conf)
