from pathlib import Path

import pytest


@pytest.fixture
def temp_dir(tmp_path):
    """
    Fixture for creating a temporary directory for testing.
    """
    return tmp_path


@pytest.fixture
def test_data_dir():
    """
    Fixture to provide the path to the test data directory.
    """
    return Path(__file__).parent / "data"
