"""Tests for _card.py"""

import logging
import os

from pytest import raises

from tonuino_cards_manager._card import Card


def test_default_card_initialization():
    """
    Test the default initialization of the Config class.
    """
    card = Card()
    assert card.no == 0
    assert isinstance(card.source, list)
    assert not card.source
    assert isinstance(card.sourcefiles, list)
    assert not card.sourcefiles
    assert card.mode == "play-random"


def test_imported_card(cards):
    """Test import_card method"""
    # Card 1 is a single
    assert isinstance(cards[1], Card)
    assert isinstance(cards[1].source, list)
    assert cards[1].source == ["01. Tester - Test Sound 01.mp3"]
    assert cards[1].description == ""
    assert cards[1].mode == "single"

    # Card 2 has multiple sources, but default mode
    assert isinstance(cards[2].source, list)
    assert cards[2].source == [
        "01. Tester - Test Sound 01.mp3",
        "02. Tester - Test Sound 02.mp3",
    ]
    assert cards[2].mode == "play-random"

    # Card 3 has a directory as source
    assert cards[3].source == ["."]
    assert cards[3].to_song == 3


def test_create_carddesc(cards, test_audio_dir):
    """Test create_carddesc method"""
    # Card description before sourcefiles have been gathered
    assert cards[1].create_carddesc(1) == "Card no. 1"

    # Test with parsed sources
    cards[1].parse_sources(test_audio_dir)
    assert cards[1].create_carddesc(1) == "Card no. 1 (01. Tester - Test Sound 01.mp3... (1 files)"

    # Test with preset description
    cards[4].parse_sources(test_audio_dir)
    assert cards[4].create_carddesc(4) == "Card no. 4 (Favourite songs of the last few weeks)"


def test_parse_card_config_unknown_mode(cards, caplog):
    """Test the parse_card_config method with an unknown mode"""
    cards[1].mode = "nonexitent-mode"
    with caplog.at_level(logging.CRITICAL):
        with raises(SystemExit):
            cards[1].parse_card_config()

    assert "The mode 'nonexitent-mode' is unknown, this will not work." in caplog.text


def test_parse_card_config_single(cards):
    """Test the parse_card_config method with a single"""
    cards[1].parse_card_config()

    assert cards[1].extra1 == 1


def test_parse_card_config_from_to(cards):
    """Test the parse_card_config method with a from-to mode"""
    cards[3].parse_card_config()

    assert cards[3].extra1 == 2
    assert cards[3].extra2 == 3


def test_parse_card_config_from_to_missing(cards, caplog):
    """Test the parse_card_config method with a from-to mode but for which the
    ranges haven't been defined"""
    cards[3].from_song = 0
    with caplog.at_level(logging.ERROR):
        cards[3].parse_card_config()

    assert (
        "You've set a mode with from-to song ranges, but you haven't defined this range"
        in caplog.text
    )


def test_parse_sources(test_audio_dir, cards):
    """Test the parse_sources method"""
    cards[4].parse_sources(test_audio_dir)

    # Test of source file actually exists
    assert os.path.exists(cards[4].sourcefiles[1])
    # Test amount
    assert len(cards[4].sourcefiles) == 2
    # Test whether it found the correct files
    assert "tests/data/audio/02. Tester - Test Sound 02.mp3" in str(cards[4].sourcefiles[0])
    assert "tests/data/audio/subdir_audio/A different file.mp3" in str(cards[4].sourcefiles[1])

    # Test the "." source
    cards[3].parse_sources(test_audio_dir)
    assert len(cards[3].sourcefiles) == 3
    assert "tests/data/audio/03. Tester - Test Sound 03 - without ID3.mp3" in str(
        cards[3].sourcefiles[2]
    )


def test_parse_sources_none_source(test_audio_dir, cards, caplog):
    """Test the parse_sources method, with None source"""
    cards[1].source = None
    with caplog.at_level(logging.ERROR):
        cards[1].parse_sources(test_audio_dir)

    assert "The source definition for this card seems to be empty" in caplog.text


def test_parse_sources_no_source(test_audio_dir, cards, caplog):
    """Test the parse_sources method, with empty list entry"""
    cards[2].source[1] = ""
    with caplog.at_level(logging.WARNING):
        cards[2].parse_sources(test_audio_dir)

    assert "2nd source of this card appears to be empty. Will not process" in caplog.text


def test_parse_sources_faulty_source(test_audio_dir, cards, caplog):
    """Test the parse_sources method, with one faulty source"""
    cards[1].source[0] = "/this/path/does/not/exist1337"
    with caplog.at_level(logging.WARNING):
        cards[1].parse_sources(test_audio_dir)

    assert "/this/path/does/not/exist1337 seems to be neither a file nor a directory" in caplog.text


def test_process_card(temp_dir, test_audio_dir, cards):
    """Test the process_card method"""
    cards[3].process_card(temp_dir, test_audio_dir)

    assert os.path.exists(temp_dir / "03" / "002-Tester-Test_Sound_02.mp3")
    assert os.path.exists(temp_dir / "03" / "003-03_Tester_-_Test_Sound_03_-_without_ID3.mp3")


def test_process_card_existing_file(temp_dir, test_audio_dir, cards):
    """Test the process_card method, with a file already existing at destination"""
    # Create file at the destination directory, and a sibling directory
    (temp_dir / "01").mkdir()
    (temp_dir / "03").mkdir()
    (temp_dir / "03" / "bla.mp3").touch()
    assert os.path.exists(temp_dir / "03" / "bla.mp3")

    # See if the file is still present afterwards. It shouldn't, but the sibling dir
    cards[3].process_card(temp_dir, test_audio_dir)
    assert not os.path.exists(temp_dir / "03" / "bla.mp3")
    assert os.path.exists(temp_dir / "01")


def test_create_card_bytecode(config, cards):
    """Test create_card_bytecode method"""
    co = config
    ca = cards[3]
    ca.parse_card_config()

    bytecode = ca.create_card_bytecode(
        cookie=co.cardcookie,
        version=co.version,
        directory=ca.no,
        mode=ca.mode,
        extra1=ca.extra1,
        extra2=ca.extra2,
    )

    assert bytecode == "1337B3470203070203"
