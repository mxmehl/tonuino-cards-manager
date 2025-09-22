# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Tests for _helper.py"""

import logging
import os

from pytest import raises

from tonuino_cards_manager._helpers import (
    _sanitize_filename,
    copy_to_sdcard,
    decimal_to_hex,
    get_audio_length,
    get_directories_in_directory,
    get_files_in_directory,
    proper_dirname,
    table_of_contents,
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


def test_copy_to_sdcard_with_tags(temp_dir, test_audio_dir, config):
    """
    Test copying an MP3 file with ID3 tags to the destination directory.
    """
    mp3file_1 = test_audio_dir / "01. Tester - Test Sound 01.mp3"
    mp3file_2 = test_audio_dir / "02. Tester - Test Sound 02.mp3"

    copy_to_sdcard(0, mp3file_1, temp_dir, config.filenametype)
    copy_to_sdcard(1, mp3file_2, temp_dir, config.filenametype)

    # Verify that the files were copied to the expected destination
    assert os.path.exists(temp_dir / "001-Tester-Test_Sound_01.mp3")
    assert os.path.exists(temp_dir / "002-Tester-Test_Sound_02.mp3")


def test_copy_to_sdcard_without_tags(temp_dir, test_audio_dir, config):
    """
    Test copying an MP3 file without ID3 tags to the destination directory.
    """
    mp3file = test_audio_dir / "03. Tester - Test Sound 03 - without ID3.mp3"

    copy_to_sdcard(2, mp3file, temp_dir, config.filenametype)

    # Verify that the file was copied to the expected destination
    assert os.path.exists(temp_dir / "003-03_Tester_-_Test_Sound_03_-_without_ID3.mp3")


def test_copy_to_sdcard_track_number_only(temp_dir, test_audio_dir):
    """
    Test copying an MP3 file with configuration "tracknumber"
    """
    mp3file = test_audio_dir / "03. Tester - Test Sound 03 - without ID3.mp3"

    copy_to_sdcard(3, mp3file, temp_dir, "tracknumber")

    # Verify that the file was copied to the expected destination
    assert os.path.exists(temp_dir / "004.mp3")


def test_copy_to_sdcard_wrong_filenametype(temp_dir, test_audio_dir, caplog):
    """
    Test copying an MP3 file with wrong configuration of filenametype
    """
    mp3file = test_audio_dir / "03. Tester - Test Sound 03 - without ID3.mp3"
    with caplog.at_level(logging.CRITICAL):
        with raises(SystemExit):
            copy_to_sdcard(3, mp3file, temp_dir, "thisiswrong")

    # Verify error
    assert "You did specify a wrong filenametype" in caplog.text


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


def test_get_audio_length(test_audio_dir):
    """
    Test the get_audio_length function on mp3 file and non audio file
    """
    mp3file = test_audio_dir / "01. Tester - Test Sound 01.mp3"
    assert get_audio_length(mp3file) == 3


def test_get_files_in_directory_all(test_audio_dir):
    """
    Test the get_files_in_directory function on files and directories
    """
    expected_files = [
        test_audio_dir / "00. not a music file.txt",
        test_audio_dir / "01. Tester - Test Sound 01.mp3",
        test_audio_dir / "02. Tester - Test Sound 02.mp3",
        test_audio_dir / "03. Tester - Test Sound 03 - without ID3.mp3",
    ]

    # Expected list should be sorted
    assert get_files_in_directory(test_audio_dir) == sorted(expected_files)


def test_get_files_in_directory_audio(test_audio_dir):
    """
    Test the get_files_in_directory function on files and directories, filter non-audio files
    """
    expected_files = [
        test_audio_dir / "01. Tester - Test Sound 01.mp3",
        test_audio_dir / "02. Tester - Test Sound 02.mp3",
        test_audio_dir / "03. Tester - Test Sound 03 - without ID3.mp3",
    ]

    # Expected list should be sorted
    assert get_files_in_directory(test_audio_dir, audio_only=True) == sorted(expected_files)


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


def test_table_of_contents(test_config_dir):
    """
    Test the if the table_of_contents function creates a pdf file.
    """
    # If the pdf file already exists delete it
    if os.path.exists(test_config_dir / "TOC_ok_1card.pdf"):
        os.remove(test_config_dir / "TOC_ok_1card.pdf")
    # test the function
    toc_list = [["No.", "Description", "Files", "Duration"], [1, "describtion1", 1, "0:00:01"]]
    table_of_contents(toc_list, test_config_dir / "ok_1card.yaml")
    assert os.path.exists(test_config_dir / "TOC_ok_1card.pdf")
