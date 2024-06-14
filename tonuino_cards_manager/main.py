# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Tools to administrate and rename files to store them on a SD card for Tonuino"""

import argparse
import logging

from ._config import parse_config
from ._qrcode import generate_qr_codes

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-c", "--config", required=True, help="The config file")
parser.add_argument(
    "-d",
    "--destination",
    required=True,
    help="The destination directory in which the data is written to",
)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")


def configure_logger(args) -> logging.Logger:
    """Set logging options"""
    log = logging.getLogger()
    logging.basicConfig(
        encoding="utf-8",
        format="%(levelname)s: %(message)s",
        level=(logging.DEBUG if args.verbose else logging.INFO),
    )

    return log


def main():
    """Main function"""
    args = parser.parse_args()

    # Set logger
    configure_logger(args=args)

    # Read YAML file
    config = parse_config(args.config)

    qrdata = []

    # Iterate through the cards and their configs
    for cardno, card in config.cards.items():
        # Add card number to card DC
        card.no = cardno

        # Card description and user info
        logging.info("Processing %s", card.create_carddesc(card.no))

        # Parse configuration and detect possible mistakes
        card.parse_card_config()

        # Create dir for card, parse sources, and copy accordingly
        card.process_card(args.destination, config.sourcebasedir)

        # Create card bytecode for this directory
        card_bytecode = card.create_card_bytecode(
            cookie=config.cardcookie,
            version=config.version,
            directory=card.no,
            mode=card.mode,
            extra1=card.extra1,
            extra2=card.extra2,
        )

        qrdata.append(f"{card_bytecode};{card.create_carddesc(cardno)}")

    # Create QR code
    generate_qr_codes(qrdata)


if __name__ == "__main__":
    main()
