# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Tests for _config.py"""

import logging

from pytest import raises

from tonuino_cards_manager._config import (
    Config,
    _load_config_dict,
    _read_config_file,
    get_config,
)


def test_default_config_initialization():
    """
    Test the default initialization of the Config class.
    """
    config = Config()
    assert config.sourcebasedir == ""
    assert config.cardcookie == "1337B347"
    assert config.version == 2
    assert not config.cards


def test_read_config_file(test_config_dir, caplog):
    """Test _read_config_file function"""

    # Good file, just defaults
    data = _read_config_file(str(test_config_dir / "ok_4cards.yaml"))
    assert "version" not in data
    assert "cards" in data

    # Good file, no defaults
    data = _read_config_file(str(test_config_dir / "ok_1card.yaml"))
    assert "cards" in data
    assert "version" in data
    assert data["version"] == 1

    # Erroneous config missing the cards
    with caplog.at_level(logging.CRITICAL):
        with raises(ValueError):
            get_config(str(test_config_dir / "error_nocards.yaml"))

    assert "Config validation failed: 'cards' is a required property" in caplog.text


def test_load_config(test_config_dir):
    """Test the _load_config_dict function"""
    data = _read_config_file(str(test_config_dir / "ok_4cards.yaml"))

    config = _load_config_dict(data)

    assert isinstance(config, Config)
    assert config.cardcookie == "1337B347"


def test_get_config(test_config_dir):
    """
    Test the get_config function with some config files.
    """

    # Normal config with defaults
    config_ok1 = get_config(str(test_config_dir / "ok_4cards.yaml"))

    assert config_ok1.sourcebasedir == ""
    assert config_ok1.cardcookie == "1337B347"
    assert config_ok1.version == 2
    assert isinstance(config_ok1.cards, dict)
    assert len(config_ok1.cards) == 4
    # Test some parts of the first card
    assert 1 in config_ok1.cards

    # Config overriding defaults
    config_ok2 = get_config(str(test_config_dir / "ok_1card.yaml"))

    assert config_ok2.sourcebasedir == "/foo/bar"
    assert config_ok2.cardcookie == "DEADBEEF"
    assert config_ok2.version == 1
    assert len(config_ok2.cards) == 1


def test_import_config_none_value(test_config_dir, caplog):
    """
    Test the_import_config method with none value.
    """

    with caplog.at_level(logging.CRITICAL):
        with raises(ValueError):
            get_config(str(test_config_dir / "error_none_value.yaml"))

    assert "Config validation failed: None is not of type 'string'" in caplog.text


def test_import_cards_not_numeric(test_config_dir, caplog):
    """
    Test the _import_cards method with non-numeric card keys.
    """

    with caplog.at_level(logging.CRITICAL):
        with raises(SystemExit):
            get_config(str(test_config_dir / "error_not_numeric.yaml"))

    assert "Card identifiers must be numeric. Found 'two' instead" in caplog.text


def test_import_cards_non_consecutive(test_config_dir, caplog):
    """
    Test the _import_cards method with non-consecutive card keys.
    """

    with caplog.at_level(logging.CRITICAL):
        with raises(SystemExit):
            get_config(str(test_config_dir / "error_non_consecutive.yaml"))

    assert "The 2 cards don't seem to be numbered consecutively" in caplog.text


def test_import_cards_too_many(test_config_dir, caplog):
    """
    Test a config with more than 99 cards
    """

    with caplog.at_level(logging.WARNING):
        get_config(str(test_config_dir / "error_too_many_cards.yaml"))

    assert "You have defined more than 99 cards (103)." in caplog.text
