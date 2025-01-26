import os
import sys

from configparser import ConfigParser


if sys.platform == "linux" or sys.platform == "darwin":
    config_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
else:
    config_dir = os.environ["APPDATA"]  # Assumes it's Windows...

CONFIG_FILE_PATH = os.path.join(config_dir, "lengua.conf")


def set_collection(collection_path: str):
    """
    Writes a .conf file and sets the value 'path' of 'collection' section
    to the path to your 'collection.anki2' file.
    """
    config = ConfigParser()
    config.add_section("collection")
    config.set("collection", "path", collection_path)

    with open(CONFIG_FILE_PATH, "w") as lengua_conf:
        config.write(lengua_conf)
