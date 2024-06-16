"""Tests for _helper.py"""

import os

from tonuino_cards_manager._helpers import (
    _sanitize_filename,
    copy_to_sdcard,
    decimal_to_hex,
    get_directories_in_directory,
    get_files_in_directory,
    proper_dirname,
)


def test_sanitize_filename():
    """
    Test the _sanitize_filename function.
    """

    # Test cases for various filename scenarios
    test_cases = [
        # Input filename, Expected sanitized filename
        ("example file", "example_file"),  # Spaces replaced
        ("invalid!@#chars", "invalidchars"),  # Special chars removed
        ("valid-chars_123", "valid-chars_123"),  # No change
        ("german_umlauts_ÄÖÜäöü", "german_umlauts_ÄÖÜäöü"),  # German umlauts preserved
        ("    ", "____"),  # Spaces only
        ("", ""),  # Empty string
        ("%%%%", ""),  # Only special characters
        (
            "file_with   spaces",
            "file_with___spaces",
        ),  # Multiple spaces replaced with underscores
    ]

    for filename, expected in test_cases:
        assert _sanitize_filename(filename) == expected


def test_copy_to_sdcard_with_tags(temp_dir, test_data_dir):
    """
    Test copying an MP3 file with ID3 tags to the destination directory.
    """
    mp3file_1 = test_data_dir / "01. Tester - Test Sound 01.mp3"
    mp3file_2 = test_data_dir / "02. Tester - Test Sound 02.mp3"

    copy_to_sdcard(0, mp3file_1, temp_dir)
    copy_to_sdcard(1, mp3file_2, temp_dir)

    # Verify that the files were copied to the expected destination
    assert os.path.exists(temp_dir / "001-Tester-Test_Sound_01.mp3")
    assert os.path.exists(temp_dir / "002-Tester-Test_Sound_02.mp3")


def test_copy_to_sdcard_without_tags(temp_dir, test_data_dir):
    """
    Test copying an MP3 file without ID3 tags to the destination directory.
    """
    mp3file = test_data_dir / "03. Tester - Test Sound 03 - without ID3.mp3"

    copy_to_sdcard(2, mp3file, temp_dir)

    # Verify that the file was copied to the expected destination
    assert os.path.exists(temp_dir / "003-03_Tester_-_Test_Sound_03_-_without_ID3.mp3")


def test_proper_dirname():
    """
    Test the proper_dirname function.
    """
    test_cases = [
        (0, "00"),  # Single digit, expect leading zero
        (1, "01"),  # Single digit, expect leading zero
        (9, "09"),  # Single digit, expect leading zero
        (10, "10"),  # Two digits, no padding
        (99, "99"),  # Two digits, no padding
        (100, "100"),  # More than two digits, no truncation
        ("5", "05"),  # Single digit string, expect leading zero
        ("42", "42"),  # Two digits string, no padding
        ("0001", "0001"),  # String with leading zeros preserved
    ]

    for dirno, expected in test_cases:
        assert proper_dirname(dirno) == expected


def test_decimal_to_hex():
    """
    Test the decimal_to_hex function.
    """
    test_cases = [
        (0, "00"),  # Minimum value
        (1, "01"),  # Single digit
        (15, "0f"),  # Single digit hex (f)
        (16, "10"),  # Transition from one to two hex digits
        (255, "ff"),  # Maximum two-digit hex value
        (256, "100"),  # Three-digit hex
        ("12", "0c"),  # String input for decimal 12 (0x0c)
        ("127", "7f"),  # String input for decimal 127 (0x7f)
        ("0010", "0a"),  # Leading zeros in string input
    ]

    for number, expected in test_cases:
        assert decimal_to_hex(number) == expected


def test_get_files_in_directory(temp_dir):
    """
    Test the get_files_in_directory function.
    """
    # Define file and create some directories
    (temp_dir / "file1.txt").touch()
    (temp_dir / "file2.txt").touch()
    (temp_dir / "fileA.txt").touch()
    (temp_dir / "fileB.txt").touch()
    (temp_dir / "dir1").mkdir()
    (temp_dir / "dir2").mkdir()

    expected_files = [
        temp_dir / "file1.txt",
        temp_dir / "file2.txt",
        temp_dir / "fileA.txt",
        temp_dir / "fileB.txt",
    ]

    # Expected list should be sorted
    assert get_files_in_directory(temp_dir) == sorted(expected_files)


def test_get_files_in_empty_directory(temp_dir):
    """
    Test the get_files_in_directory function with an empty directory.
    """
    assert get_files_in_directory(temp_dir) == []


def test_get_directories_in_directory(temp_dir):
    """
    Test the get_directories_in_directory function.
    """
    # Create some test directories and files
    (temp_dir / "dir1").mkdir()
    (temp_dir / "dir2").mkdir()
    (temp_dir / "dirA").mkdir()
    (temp_dir / "dirB").mkdir()
    (temp_dir / "file1.txt").touch()
    (temp_dir / "file2.txt").touch()

    expected_directories = [
        temp_dir / "dir1",
        temp_dir / "dir2",
        temp_dir / "dirA",
        temp_dir / "dirB",
    ]

    # Expected list should be sorted
    assert get_directories_in_directory(temp_dir) == sorted(expected_directories)


def test_get_directories_in_empty_directory(temp_dir):
    """
    Test the get_directories_in_directory function with an empty directory.
    """
    assert get_directories_in_directory(temp_dir) == []
