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


@dataclass
class Config:
    """Dataclass holding the configuration for all cards"""

    sourcebasedir: str = ""
    cardcookie: str = "1337B347"
    version: int = 2
    maxcardsperqrcode: int = 4
    cards: dict[int, Card] = field(default_factory=dict)

    def _import_cards(self, cards: dict[str | int, dict]):
        """Import the cards data from dict to DC, and check for a number of
        potential issues"""
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
            carddc = Card()
            carddc.import_dict_to_card(carddata)
            self.cards[int(cardno)] = carddc

        # Check if card keys are numbered consecutively
        cardamount = len(self.cards)
        cardset = set(self.cards)
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

    def import_config(self, data: dict):
        """Import the YAML data, overriding the defaults if present"""
        for key in ("sourcebasedir", "cardcookie", "version", "maxcardsperqrcode"):
            if key in data:
                value = data[key]
                # Catch None values
                if value is None:
                    logging.critical(
                        "The value for '%s' is empty (%s). If you want to use the default, "
                        'remove the config item. If you want it to be an empty string, use ""',
                        key,
                        value,
                    )
                    sys.exit(1)

                logging.debug("Overriding default configuration for '%s' with '%s'", key, value)
                setattr(self, key, value)

        self._import_cards(data.get("cards", {}))


def _read_config_file(file: str) -> dict:
    """Read config file and detect if cards are defined"""
    with open(file, "r", encoding="UTF-8") as yamlfile:
        data = yaml.safe_load(yamlfile)

    # Check if required keys are present
    if "cards" not in data:
        logging.critical("Mandatory configuration(s) missing in file %s: %s", file, "cards")
        sys.exit(1)

    return data


def _load_config_dict(data: dict) -> Config:
    """Load the read YAML file as a Config object"""
    config = Config()
    config.import_config(data)

    logging.debug("Configuration loaded as dataclass: %s", config)
    return config


def get_config(file: str) -> Config:
    """Read config and return Config object"""
    data = _read_config_file(file)
    return _load_config_dict(data)
