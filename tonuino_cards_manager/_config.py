# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""
Dataclass holding general configuration
"""

import logging
import sys
from dataclasses import dataclass, field

import yaml

from ._card import Card
from ._helpers import validate_config_schema

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "sourcebasedir": {"type": "string"},
        "cardcookie": {"type": "string", "minLength": 8, "maxLength": 8},
        "version": {"type": "integer", "minimum": 1},
        "maxcardsperqrcode": {"type": "integer", "minimum": 1},
        "filenametype": {
            "type": "string",
            "enum": ["mp3tags", "tracknumber"],
        },
        "create_tableofcontents": {"type": "boolean"},
        "cards": {"type": "object", "minproperties": 1},
    },
    "required": ["cards"],
    "additionalProperties": False,
}

CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "source": {
            "oneOf": [
                {"type": "string", "minLength": 1},
                {"type": "array", "items": {"type": "string", "minLength": 1}},
            ],
        },
        "mode": {
            "type": "string",
            "enum": [
                "play-random",
                "album",
                "party",
                "single",
                "audiobook",
                "admin",
                "play-from-to",
                "album-from-to",
                "party-from-to",
            ],
            "default": "play-random",
        },
        "from_song": {"type": "integer", "minimum": 1},
        "to_song": {"type": "integer", "minimum": 1},
        "dest_folder": {"type": "integer", "minimum": 1, "maximum": 99},
    },
    "required": ["source"],
    "additionalProperties": False,
}


@dataclass
class Config:
    """Dataclass holding the configuration for all cards"""

    sourcebasedir: str = ""
    cardcookie: str = "1337B347"
    version: int = 2
    maxcardsperqrcode: int = 4
    filenametype: str = "mp3tags"
    create_tableofcontents: bool = True
    cards: dict[int, Card] = field(default_factory=dict)

    def _import_and_check_cards(self, cards: dict[str | int, dict]):
        """
        Import the cards data from dict to DC, and check for a number of potential issues. The
        checks limit themselves to the card key (numeric) and their role in the whole cards dict.
        The schema check for the cards themselves is done in the Card class.
        """
        # Check if card keys are numeric
        for key in cards:
            if isinstance(key, str) and key.isnumeric():
                pass
            elif isinstance(key, int):
                pass
            else:
                logging.critical("Card identifiers must be numeric. Found '%s' instead", key)
                sys.exit(1)

        # Import card data, add to dict with int identifier and card config DC
        for cardno, carddata in cards.items():
            validate_config_schema(carddata, CARD_SCHEMA)
            carddc = Card()
            # Here, the cards are validated against the CARD_SCHEMA in _card.py
            carddc.import_dict_to_card(carddata)
            self.cards[int(cardno)] = carddc

        # Check if card keys are numbered consecutively
        cardset = set(self.cards)
        cardset = {n for n in cardset if n < 100}
        cardamount = len(cardset)
        cardtargetlayout = set(range(1, cardamount + 1))
        if cardset != cardtargetlayout:
            logging.critical(
                "The %s cards don't seem to be numbered consecutively, "
                "or you used the same card identifier multiple times",
                cardamount,
            )
            sys.exit(1)

        # Check if more than 99 cards
        if len(self.cards) > 99:
            logging.warning(
                "You have defined more than 99 cards (%s). "
                "This will not work in typical Tonuino MP3 players!",
                len(self.cards),
            )

    def import_and_check_config(self, data: dict):
        """
        Import and check all YAML data, overriding the defaults if present. Works in two steps:
            1. Import the general configuration data, which is not card-specific.
            2. Import the cards data, which is card-specific.
        """
        validate_config_schema(data, CONFIG_SCHEMA)

        for key in data.keys():
            # Do not override the cards key, will be imported separately
            if key == "cards":
                continue
            value = data[key]
            logging.debug("Overriding default configuration for '%s' with '%s'", key, value)
            setattr(self, key, value)

        self._import_and_check_cards(data.get("cards", {}))


def _read_config_file(file: str) -> dict:
    """Read config file and detect if cards are defined"""
    with open(file, "r", encoding="UTF-8") as yamlfile:
        data = yaml.safe_load(yamlfile)

    return data


def _load_config_dict(data: dict) -> Config:
    """Load the read YAML file as a Config object"""
    config = Config()
    config.import_and_check_config(data)

    logging.debug("Configuration loaded as dataclass: %s", config)
    return config


def get_config(file: str) -> Config:
    """Read config and return Config object"""
    data = _read_config_file(file)
    return _load_config_dict(data)
