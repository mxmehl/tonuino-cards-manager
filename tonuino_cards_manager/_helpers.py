# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Helper functions for copy operations and conversions"""

import logging
import re
import shutil
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError


def _sanitize_filename(filename: str) -> str:
    """Sanitize a filename"""
    return re.sub("[^A-Za-zÄÖÜäöü0-9-_]+", "", filename.replace(" ", "_"))


def copy_to_sdcard(index: int, mp3file: Path, destination_dir: Path) -> None:
    """Copy a single file to the SD card in a suitable"""
    logging.debug("Processing %s", mp3file)
    # If no ID3 tags are present, use file name, otherwise $artist-$title
    try:
        meta = EasyID3(mp3file)
        filename = _sanitize_filename(f"{meta['artist'][0]}-{meta['title'][0]}")
    except (ID3NoHeaderError, KeyError):
        logging.debug("File %s does not contain any ID3 tags. Using its file name", mp3file.name)
        filename = _sanitize_filename(mp3file.stem)

    # copy file to destination using a compatible name based on tags
    destname = "{track}-{filename}.mp3".format(  # pylint: disable=consider-using-f-string
        # Track number, filled with leading zeros
        track=str(index + 1).zfill(3),
        # Artist and title / or filename
        filename=filename,
    )
    logging.debug("Copying %s to %s", mp3file, destination_dir / Path(destname))
    shutil.copy2(mp3file, destination_dir / Path(destname))


def proper_dirname(dirno: int | str) -> str:
    """Convert a directory number to a proper two-digit directory name"""
    return str(dirno).zfill(2)


def decimal_to_hex(number: int | str) -> str:
    """Convert a decimal number to a hex number"""
    return f"{int(number):02x}"


def get_files_in_directory(directory: Path) -> list[Path]:
    """Get all files in a directory, sorted"""
    return sorted([f for f in directory.iterdir() if f.is_file()])


def get_directories_in_directory(directory: Path) -> list[Path]:
    """Get all directories in a directory, sorted"""
    return sorted([f for f in directory.iterdir() if f.is_dir()])
