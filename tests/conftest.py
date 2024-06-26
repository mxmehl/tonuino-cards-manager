# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Pytest fixtures"""

from pathlib import Path

import pytest

from tonuino_cards_manager._config import get_config


@pytest.fixture
def temp_dir(tmp_path):
    """
    Fixture for creating a temporary directory for testing.
    """
    return tmp_path


@pytest.fixture
def test_audio_dir():
    """
    Fixture to provide the path to the audio test data directory.
    """
    return Path(__file__).parent / "data" / "audio"


@pytest.fixture
def test_config_dir():
    """
    Fixture to provide the path to the config test data directory.
    """
    return Path(__file__).parent / "data" / "config"


@pytest.fixture
def config(test_config_dir):  # pylint: disable=redefined-outer-name
    """
    Fixture providing the the config.
    """
    return get_config(str(test_config_dir / "ok_4cards.yaml"))


@pytest.fixture
def cards_ok(test_config_dir):  # pylint: disable=redefined-outer-name
    """
    Fixture providing well configured cards from the config.
    """
    cardcfg = get_config(str(test_config_dir / "ok_4cards.yaml")).cards
    # Extending the number (cardno) value
    for i in range(1, 4):
        cardcfg[i].no = i
    return cardcfg


@pytest.fixture
def cards_faulty(test_config_dir):  # pylint: disable=redefined-outer-name
    """
    Fixture providing badly configured cards from the config.
    """
    return get_config(str(test_config_dir / "error_faulty_cards.yaml")).cards
