# SPDX-FileCopyrightText: 2024 Max Mehl <https://mehl.mx>
#
# SPDX-License-Identifier: GPL-3.0-only

"""QR Code generation and handling"""

import logging

from qrcode.main import QRCode


def generate_qr_codes(qrdata: list[str]):
    """Generate QR codes"""
    logging.debug("QRCode data: \n%s", "\n".join(qrdata))
    print("")
    # Make each QR code contain max. 4 elements
    maxelem = 4
    for idx, qrlist in enumerate([qrdata[x : x + maxelem] for x in range(0, len(qrdata), maxelem)]):
        qrc = QRCode()
        qrc.add_data("\n".join(qrlist))
        print(
            f"QR code for cards batch {idx + 1} "
            f"(cards {(idx * maxelem) + 1} - {(idx + 1) * maxelem}):"
        )
        qrc.print_ascii()
