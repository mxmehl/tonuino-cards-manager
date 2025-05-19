# SPDX-FileCopyrightText: 2025 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Tests for _qrcode.py"""

from pytest import raises

from tonuino_cards_manager._qrcode import generate_qr_codes


def test_generate_qr_codes_direct(capsys):
    """
    Test QR code generation with a list of data and a maximum number of cards per QR code.
    """
    # Test data
    test_data = ["card1:data1", "card2:data2", "card3:data3"]
    maxcardsperqrcode = 2

    # Call function
    generate_qr_codes(test_data, maxcardsperqrcode)

    # Capture stdout
    captured = capsys.readouterr()
    output = captured.out

    # Verify output contains expected elements
    assert "QR code for cards batch 1" in output
    assert "QR code for cards batch 2" in output
    assert "(cards 1 - 2)" in output
    assert "(cards 3 - 3)" in output

    # Verify correct number of QR codes generated (2 batches for 3 items with max 2 per code)
    assert output.count("QR code for cards batch") == 2


def test_generate_qr_codes_from_default_config(config, populated_qrcode_data, capsys):
    """
    Test QR code generation with the default test config file with the default number of cards per
    QR code
    """

    # Create QR code
    generate_qr_codes(populated_qrcode_data, config.maxcardsperqrcode)

    # Capture stdout
    captured = capsys.readouterr()
    output = captured.out

    # Verify output contains expected elements
    assert "QR code for cards batch 1" in output
    assert "(cards 1 - 4)" in output

    # Verify correct number of QR codes generated (1 batch for 4 items with max 4 per code)
    assert output.count("QR code for cards batch") == 1


def test_generate_qr_codes_from_config_with_small_qrcodes(config, populated_qrcode_data, capsys):
    """
    Test QR code generation with a config with a lower amount of cards per QR code
    """

    # Set a smaller maxcardsperqrcode to test the split
    config.maxcardsperqrcode = 3

    # Create QR code
    generate_qr_codes(populated_qrcode_data, config.maxcardsperqrcode)

    # Capture stdout
    captured = capsys.readouterr()
    output = captured.out

    # Verify output contains expected elements
    assert "QR code for cards batch 1" in output
    assert "QR code for cards batch 2" in output
    assert "(cards 1 - 3)" in output
    assert "(cards 4 - 4)" in output

    # Verify correct number of QR codes generated (2 batches for 4 items with max 3 per code)
    assert output.count("QR code for cards batch") == 2


def test_generate_qr_codes_from_config_with_too_many(config, populated_qrcode_data):
    """
    Test QR code generation with a config with a too high amount of cards per QR code (more than
    2953 bytes)
    """

    # Create a large list of QR code data to exceed the 2953 bytes limit
    qrcode_data_huge = populated_qrcode_data * 20
    bytecount = sum(len(card.encode("utf-8")) for card in qrcode_data_huge)
    assert bytecount > 2953

    # Set a huge maxcardsperqrcode
    config.maxcardsperqrcode = 100

    # Create QR code and expect ValueError due to exceeding QR code size limit
    with raises(ValueError):
        generate_qr_codes(qrcode_data_huge, config.maxcardsperqrcode)
