import json
import logging


def read_settings(settings_file: str) -> dict:
    """Function that reads settings from .json file.

    Args:
        settings_file: path to settings file.

    Returns:
        dict: dictionary with settings.
    """
    try:
        with open(settings_file) as json_file:
            settings = json.load(json_file)
        logging.info(
            f"Settings was successfully read from file{settings_file}!")
    except OSError as err:
        logging.warning(
            f"Settings was not read from file{settings_file}\n{err}")
    return settings