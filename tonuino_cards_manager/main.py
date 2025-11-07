# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Tools to administrate and rename files to store them on a SD card for Tonuino"""

import argparse
import logging
from datetime import timedelta

from . import __version__
from ._clean import clean_unconfigured_dirs
from ._config import get_config
from ._helpers import table_of_contents
from ._qrcode import generate_qr_codes

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-c", "--config", required=True, help="The config file")
parser.add_argument(
    "-d",
    "--destination",
    required=True,
    help="The destination directory in which the data is written to",
)
parser.add_argument(
    "-f",
    "--force",
    action="store_true",
    help="Delete all song folders on the destination which are not configured by you",
)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
parser.add_argument("--version", action="version", version="%(prog)s " + __version__)


def configure_logger(args) -> logging.Logger:
    """Set logging options"""
    log = logging.getLogger()
    logging.basicConfig(
        encoding="utf-8",
        format="%(levelname)s: %(message)s",
        level=(logging.DEBUG if args.verbose else logging.INFO),
    )

    return log


def main() -> None:
    """Main function"""
    args = parser.parse_args()

    # Set logger
    configure_logger(args=args)

    # Read YAML file
    config = get_config(args.config)

    qrdata = []
    toc_list: list[list[str | int]] = [["No.", "Description", "Files", "Duration"]]

    # Iterate through the cards and their configs
    for cardno, card in config.cards.items():
        # Add card number to card DC
        card.no = cardno

        # Card description and user info
        logging.info("Processing %s", card.create_carddesc())

        # Parse configuration and detect possible mistakes
        card.parse_card_config()

        # Create dir for card, parse sources, and copy accordingly
        card_audio_length = card.process_card(
            args.destination, config.sourcebasedir, config.filenametype
        )

        # Create card bytecode for this directory
        card_bytecode = card.create_card_bytecode(
            cookie=config.cardcookie,
            version=config.version,
            directory=card.no,
            mode=card.mode,
            extra1=card.extra1,
            extra2=card.extra2,
        )

        card_description = card.create_carddesc()
        # Add card to QR code generation
        qrdata.append(f"{card_bytecode};{card_description}")

        # Extract content of card
        card_description_qr = card_description.split("(")
        card_description_qr = card_description_qr[1].split(")")
        card_total_audio_length_str = str(timedelta(seconds=sum(card_audio_length)))
        # Add card to table of contents
        toc_list.append(
            [cardno, card_description_qr[0], len(card_audio_length), card_total_audio_length_str]
        )

    # Delete directories that have not been configured
    if args.force:
        clean_unconfigured_dirs(args.destination, config.cards)

    # Create QR code
    generate_qr_codes(qrdata, config.maxcardsperqrcode)

    # Create table of contents
    if config.create_tableofcontents:
        table_of_contents(toc_list, args.config)


if __name__ == "__main__":
    main()
