from pathlib import Path

import pytest


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
