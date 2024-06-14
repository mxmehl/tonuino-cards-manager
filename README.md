<!--
SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>

SPDX-License-Identifier: GPL-3.0-only
-->

# Tonuino Cards Manager

Welcome to the **Tonuino Cards Manager**, a convenient utility designed to streamline the process of managing and organizing music for [Tonuino music boxes](https://www.voss.earth/tonuino/). This tool simplifies managing your Tonuino's SD card content and RFID cards settings.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)

## Overview

The **Tonuino Cards Manager** provides an easy way to prepare and manage music collections for your Tonuino music box. Whether you want to assign single songs or entire albums to specific RFID cards, this tool handles the setup seamlessly through a YAML configuration file.

## Features

- **Easy Configuration**: Use a simple YAML file to define which music plays for each RFID card.
- **Multiple Sources**: Assign songs or albums from various sources to one RFID card.
- **All modi**: The tool supports all playing modi, e.g. single and party mode.
- **Automated Management**: The tool automates the copying and organizing of music files into the appropriate structure for Tonuino.
- **QR Code Generation**: QR codes will be generated for each card which allows you to quickly configure your cards, e.g. with [TonUINO NFC Tools](https://marc136.github.io/tonuino-nfc-tools/)
- **User-Friendly**: Intuitive and designed with simplicity in mind for managing kids' music collections.

## Installation

To install the **Tonuino Cards Manager**, you need to have Python (at least version 3.10) installed. You can install the application using `pip`:

```
pip3 install tonuino-cards-manager
```

## Usage

Once installed, you can use the tool by following these steps:

1. Prepare your YAML configuration file (e.g. `mybox.yaml`), specifying the music for each RFID card.
2. Run the tool with the following command:
   ```bash
   tonuino-cards-manager --config mybox.yaml --destination /path/to/tonuino-sd-card/
   ```
3. The tool will process the YAML file and organize your music according to the specified configuration (see below).

<!-- Add demo here -->

## Configuration

The core of the **Tonuino Cards Manager** is the configuration file where you define your music setup. Here's a basic example of what the configuration might look like:

```yaml
# sourcebasedir: ""
# cardcookie: "1337B347"
# version: 2

cards:
  # A whole directory in album mode
  1:
    source:
      - Rolf Zuckowski/1994 Im Kindergarten
    mode: album
  # A whole directory in party mode. A single source can also be written this way
  2:
    source: Fredrik Vahle/1990 Der Spatz
    mode: party
  # A whole directory, play one of the 10 first episodes randomly
  3:
    source: Audio Books/Benjamin Blümchen/
    mode: play-from-to
    from_song: 1
    to_song: 10
  # Multiple single songs and a whole directory in party mode
  4:
    description: Favourite songs of the last few weeks
    source:
      - Singles/Die alte Moorhexe.mp3
      - Singles/Große Uhren machen tick tack.mp3
      - Singles/Best of Last Vacation/
    mode: party
```

### Configuration Details

- **sourcebasedir**: If all your music is in one directory, you can add the path here and make the `source` entries for the cards relative to this directory. Default: `""`
- **cardcookie**: The card cookie of your Tonuino box. [Background here](https://discourse.voss.earth/t/bedeutung-der-konstante-cardcookie/10241). Default: `1337B347`
- **version**: Card format version, `2` for Tonuino 2.1.x and TNG. Default: `2`
- **cards**: A list of RFID cards.
  - **id**: The number of the card. These numbers must be unique and be actual numbers, not texts.
    - **description**: A free-text field to describe the card, useful for collections of single songs. Only relevant for your information when handling the QR code. Default: `""`
    - **source**: A string or list of paths to songs or albums assigned to the card. Mandatory.
    - **mode**: The play mode for this card. Can be any of the following modes. Default: `play-random`
      - `play-random`: play a random file from the folder, front-back buttons locked
      - `album`: play the complete folder
      - `party`: play files in the folder in random order
      - `single`: play a specific file in the folder
      - `audiobook`: play a folder and save the progress
      - `admin`: create an admin card
      - `play-from-to`: play a random file between the start and end file (you need to set `from_song` and `to_song`)
      - `album-from-to`: play all files between the start and end file in consecutive order (you need to set `from_song` and `to_song`)
      - `party-from-to`: play all files between the start and end file at random (you need to set `from_song` and `to_song`)
    - **from_song**: If you set one of the `*-from-to` modes, write the number of the song you want to start from (from the list of sources you provided). Default: `0`
    - **to_song**: Equivalent to `from_song`. Default: `0`

## Limitations

The tool currently has a few limitation. Please feel free to contribute to the project or share your ideas how to fix them.

- A maximum of 99 cards will be supported as every configured card will create a separate folder. A typical Tonuino's MP3 player component can only support folders between 01-99.
- Version 1 of the RFID cards format is not tested as I don't have such a box.

## Contributing

Contributions are welcome! To contribute to the **Tonuino Cards Manager**, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-or-fix-name
   ```
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository:
   ```bash
   git push origin feature-or-fix-name
   ```
5. Open a Pull Request on the main repository.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0-only). See the [LICENSE](LICENSE) file for details.

---

Happy listening with your Tonuino music box! If you have any questions or need further assistance, please open an issue on GitHub.
