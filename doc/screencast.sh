#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

# Script to create the asciinema recording:
# asciinema rec ~/tcm.cast -c ./doc/screencast.sh

# You can choose different typed, e.g. pe or pei
TYPE=pei
# What to do with comments? : for doing nothing, $TYPE for doing the same as with code
COMM=":"

. ~/Git/github/demo-magic/demo-magic.sh

clear

$TYPE 'cat tonuino-cards.yaml'
$TYPE ''
$TYPE 'tonuino-cards-manager -c tonuino-cards.yaml -d dest/'
wait
$TYPE ''
