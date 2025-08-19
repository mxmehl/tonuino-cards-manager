# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Helper functions for copy operations and conversions"""

import logging
import re
import shutil
import sys
from pathlib import Path

from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError
from mutagen.easyid3 import EasyID3
from mutagen.id3._util import ID3NoHeaderError
from mutagen.mp3 import MP3
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle


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


def get_audio_length(mp3file: Path) -> int:
    """Get the audiolength of an audiofile"""
    file = MP3(mp3file)
    return round(file.info.length)


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


def validate_config_schema(cfg: dict, schema: dict) -> None:
    """Validate the config against a JSON schema"""
    try:
        validate(instance=cfg, schema=schema, format_checker=FormatChecker())
    except ValidationError as e:
        logging.critical("Config validation failed: %s", e.message)
        raise ValueError(e) from None
    logging.debug("Config validated successfully against schema.")


def table_of_contents(mylist, path) -> None:
    """Write a table of contents of the SD-Card to pdf"""
    # create document
    path = Path(path)
    path_toc = Path(path.parent, "Inhaltsverzeichnis_" + path.stem + ".pdf")
    doc = SimpleDocTemplate(str(path_toc), pagesize=A4)
    # container for the 'flowable' objects
    elements = []
    styles = getSampleStyleSheet()

    # add flowables to container
    elements.append(Paragraph("Inhaltsverzeichnis Tonuino", styles["Heading1"]))
    t = Table(mylist, rowHeights=1.7 * cm, repeatRows=1, spaceBefore=1 * cm)
    t.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                ("SIZE", (0, 0), (-1, -1), 16),
            ]
        )
    )
    elements.append(t)
    # write the document to disk
    doc.build(elements)
