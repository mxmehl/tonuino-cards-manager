# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Dataclass holding configuration for a single card and all its operations"""

import logging
from dataclasses import dataclass, field
from pathlib import Path

from ._helpers import (
    copy_to_sdcard,
    decimal_to_hex,
    get_audio_length,
    get_files_in_directory,
    proper_dirname,
)

MODES = {
    "play-random": 1,
    "album": 2,
    "party": 3,
    "single": 4,
    "audiobook": 5,
    "admin": 6,
    "play-from-to": 7,
    "album-from-to": 8,
    "party-from-to": 9,
}


@dataclass
class Card:  # pylint: disable=too-many-instance-attributes
    """Dataclass holding a single card, its configuration and operations"""

    no: int = 0
    description: str = ""
    summary: str = ""
    source: list[str] = field(default_factory=list)
    mode: str = "play-random"
    from_song: int = 0
    to_song: int = 0
    extra1: int = 0
    extra2: int = 0
    sourcefiles: list[Path] = field(default_factory=list)

    def import_dict_to_card(self, data: dict):
        """Import the config dict for a card as DC"""
        for key in data.keys():
            value = data[key]
            # `source` can be a string or a list. Convert it to a list if it's a string
            if key == "source" and isinstance(value, str):
                logging.debug("Converting source string to list: %s", value)
                setattr(self, key, [value])
            else:
                logging.debug("Overriding default configuration for '%s' with '%s'", key, value)
                setattr(self, key, value)

    def create_carddesc(self, cardno: int) -> str:
        """Create a description for the card"""
        output = f"Card no. {cardno}"

        # If description set, take this
        if desc := self.description:
            output += f" ({desc})"
        # Otherwise, show first file and total amount of files
        elif self.sourcefiles:
            output += f" ({self.sourcefiles[0].name}... ({len(self.sourcefiles)} files)"

        return output

    def parse_card_config(self):
        """Parse configuration and detect possible mistakes"""
        # If mode single, set extra1 to 01 (first song in folder)
        if self.mode == "single":
            self.extra1 = 1

        # If mode is a from-to mode, the keys `from_song` and `to_song` must exist
        elif self.mode in ("play-from-to", "album-from-to", "party-from-to"):
            if (fromval := self.from_song) and (toval := self.to_song):
                self.extra1 = fromval
                self.extra2 = toval
            else:
                logging.error(
                    "You've set a mode with from-to song ranges, but you haven't defined this "
                    "range. Set the keys 'from_song' and 'to_song' in your card configuration. "
                    "This card will not work as expected!"
                )

    def parse_sources(self, sourcebasepath: str) -> None:
        """Parse sources, which can be one or multiple directories or single files"""
        # Check for each source whether it's a directory or file
        for source_str in self.source:
            source = Path(sourcebasepath) / Path(source_str)

            logging.debug("Parsing source %s", source)

            if source.is_dir():
                logging.debug("%s has been detected as a directory", source)
                self.sourcefiles.extend(get_files_in_directory(source, audio_only=True))
            elif source.is_file():
                logging.debug("%s has been detected as a file", source)
                self.sourcefiles.append(source)
            else:
                logging.warning(
                    "%s seems to be neither a file nor a directory. Will not process",
                    source,
                )
                continue

    def check_too_many_files(self):
        """Check whether sources contain too many files (>255)"""
        if len(self.sourcefiles) > 255:
            logging.warning(
                "This card and therefore a directory on the SD card is handling "
                "more than 255 files (%s). This will not work in typical Tonuino MP3 players!",
                len(self.sourcefiles),
            )

    def process_card(self, destination: str, sourcebasepath: str, filenametype: str) -> list[int]:
        """Process a card with its configuration, also copying files. Return processed sources"""

        # Convert card number to two-digit folder number (max. 99), and create destination path
        dirpath = Path(destination) / Path(proper_dirname(self.no))

        # create destination directory if not present, delete all files in it
        dirpath.mkdir(parents=True, exist_ok=True)
        for dirfile in get_files_in_directory(dirpath):
            logging.debug("Delete %s from destination", dirfile)
            dirfile.unlink(missing_ok=True)

        # Parse provided sources for this card, get list of all single MP3 files
        self.parse_sources(sourcebasepath)

        # Run checks
        self.check_too_many_files()

        audiolength = []
        # Iterate through all files
        for idx, mp3 in enumerate(self.sourcefiles):
            copy_to_sdcard(idx, mp3, dirpath, filenametype)
            audiolength.append(get_audio_length(mp3))
        return audiolength

    def create_card_bytecode(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        cookie: str,
        version: int,
        directory: int,
        mode: str,
        extra1: int,
        extra2: int,
    ) -> str:
        """Create the bytecode for a card"""
        # pylint: disable=consider-using-f-string
        return "{cookie}{version}{directory}{mode}{extra1}{extra2}".format(
            cookie=cookie,
            version=decimal_to_hex(version),
            directory=decimal_to_hex(directory),
            mode=decimal_to_hex(MODES[mode]),
            extra1=decimal_to_hex(extra1),
            extra2=decimal_to_hex(extra2),
        )
