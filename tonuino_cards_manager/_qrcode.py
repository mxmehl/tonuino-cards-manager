# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""QR Code generation and handling"""

import logging

from qrcode.main import QRCode


def generate_qr_codes(qrdata: list[str], maxcardsperqrcode: int):
    """Generate QR codes"""
    logging.debug("QRCode data: \n%s", "\n".join(qrdata))
    print("")
    # Make each QR code contain max. configured elements
    for idx, qrlist in enumerate(
        [qrdata[x : x + maxcardsperqrcode] for x in range(0, len(qrdata), maxcardsperqrcode)]
    ):
        qrc = QRCode()
        qrc.add_data("\n".join(qrlist))
        print(
            f"QR code for cards batch {idx + 1} (cards {(idx * maxcardsperqrcode) + 1} - "
            f"{min((idx + 1) * maxcardsperqrcode,len(qrdata))}):"
        )
        qrc.print_ascii()
