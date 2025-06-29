# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Helper functions for copy operations and conversions"""

import logging
import re
import shutil
import sys
from pathlib import Path

from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError


def _sanitize_filename(filename: str) -> str:
    """Sanitize a filename"""
    return re.sub("[^A-Za-zÄÖÜäöü0-9-_]+", "", filename.replace(" ", "_"))


def copy_to_sdcard(index: int, mp3file: Path, destination_dir: Path, filenametype: str) -> None:
    """Copy a single file to the SD card in a suitable"""
    logging.debug("Processing %s", mp3file)
    if filenametype == "mp3tags":
        # If no ID3 tags are present, use file name, otherwise $artist-$title
        try:
            meta = EasyID3(mp3file)
            filename = _sanitize_filename(f"{meta['artist'][0]}-{meta['title'][0]}")
        except (ID3NoHeaderError, KeyError):
            logging.debug(
                "File %s does not contain any ID3 tags. Using its file name", mp3file.name
            )
            filename = _sanitize_filename(mp3file.stem)

        # copy file to destination using a compatible name based on tags
        destname = "{track}-{filename}.mp3".format(  # pylint: disable=consider-using-f-string
            # Track number, filled with leading zeros
            track=str(index + 1).zfill(3),
            # Artist and title / or filename
            filename=filename,
        )
    elif filenametype == "tracknumber":
        destname = "{track}.mp3".format(  # pylint: disable=consider-using-f-string
            # Track number, filled with leading zeros
            track=str(index + 1).zfill(3)
        )
    else:
        logging.critical(
            "You did specify a wrong filenametype '%s'."
            "Supported are: 'mp3tags' and 'tracknumber'. ",
            filenametype,
        )
        sys.exit(1)

    logging.debug("Copying %s to %s", mp3file, destination_dir / Path(destname))
    shutil.copy2(mp3file, destination_dir / Path(destname))


def proper_dirname(dirno: int | str) -> str:
    """Convert a directory number to a proper two-digit directory name"""
    return str(dirno).zfill(2)


def decimal_to_hex(number: int | str) -> str:
    """Convert a decimal number to a hex number"""
    return f"{int(number):02x}"


def get_files_in_directory(directory: Path, audio_only: bool = False) -> list[Path]:
    """Get all files in a directory, sorted. Optionally only display music files"""
    audioexts = (".mp3", ".opus", ".ogg")
    allfiles = [f for f in directory.iterdir() if f.is_file()]

    # Only return files with audio file extension
    if audio_only:
        return sorted([f for f in allfiles if f.suffix in audioexts])

    return sorted(allfiles)


def get_directories_in_directory(directory: Path) -> list[Path]:
    """Get all directories in a directory, sorted"""
    return sorted([f for f in directory.iterdir() if f.is_dir()])
