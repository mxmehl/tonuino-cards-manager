# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""Global constants"""

from importlib.metadata import version

__version__ = version("tonuino-cards-manager")

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
