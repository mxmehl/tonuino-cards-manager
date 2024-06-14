# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Helper functions for file operations"""

import logging
from pathlib import Path
from shutil import rmtree

from ._card import Card
from ._helpers import get_directories_in_directory, proper_dirname


def clean_unconfigured_dirs(destination: str, cards: dict[int, Card]):
    """Delete directories that are not configured as cards"""
    dest = Path(destination)
    # Calculate which directories are handled by the configuration
    handled_dirs = [proper_dirname(card) for card in cards]
    # For each existing directory on the SD card, check whether it is concerned
    # by the configuration
    for dirpath in get_directories_in_directory(dest):
        if dirpath.name in ("mp3", "advert"):
            continue
        if dirpath.name not in handled_dirs:
            logging.info(
                "The directory %s exists on the SD card although it is not configured here. "
                "Deleting it because you requested it with --force",
                dirpath.name,
            )
            rmtree(dirpath)
