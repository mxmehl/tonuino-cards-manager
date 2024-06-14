"""Convert cover images to many potentially working formats"""

import argparse
from os import path
from pathlib import Path

from wand.color import Color  # type: ignore
from wand.image import Image  # type: ignore

BORDERS = {"top": 5, "right": 0, "bottom": 5, "left": 0}
DIMENSIONS_DICT = {
    "width": 838 - BORDERS["right"] - BORDERS["left"],
    "height": 508 - BORDERS["top"] - BORDERS["bottom"],
}
DIMENSIONS_STR = f"{DIMENSIONS_DICT['width']}x{DIMENSIONS_DICT['height']}"
ROTATION = int(-90)

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "-f",
    "--file",
    required=True,
    help="The source cover image file",
)


def filename_extend(filename, *additions):
    """Add a certain string to a filename, e.g. file.jpg to file-addition.jpg"""
    filebasename = Path(filename).stem + "-"
    filedirname = path.dirname(filename)
    fileext = Path(filename).suffix

    additions = [x for x in additions if x]

    return filedirname + "/" + filebasename + "-".join(additions) + fileext


def save_file(image: Image, filename, *additions) -> None:
    """Save a file under another file name, using an identifier"""
    # Load the image
    # adding top and bottom border sizes
    new_height = image.height + BORDERS["top"] + BORDERS["bottom"]

    # Set the background color to black
    with Image(width=image.width, height=new_height, background=Color("white")) as img:
        # Composite the original image onto the new image
        img.composite(image, left=0, top=BORDERS["top"])

        # Save the result
        img.save(filename=filename_extend(filename, *additions))


def all_operations(img: Image, filename: str, rotation=False):
    """Wrapper for all image operations"""
    rot = "rot" if rotation else ""
    # Merely set dimensions without cropping
    with img.clone() as i:
        i.resize(**DIMENSIONS_DICT)
        save_file(i, filename, "resized", rot)

    # Liquid rescaling
    with img.clone() as i:
        i.liquid_rescale(**DIMENSIONS_DICT)
        save_file(i, filename, "liquid", rot)

    # Blurred background extension
    with img.clone() as i:
        with i.clone() as blurred:
            blurred.blur(0, 9)
            blurred.resize(**DIMENSIONS_DICT)

            i.transform(resize=DIMENSIONS_STR)
            blurred.composite(i, gravity="center", operator="over")
            save_file(blurred, filename, "blurred", rot)

    # White background extension
    with img.clone() as i:
        # Resize the image while preserving the aspect ratio
        i.transform(resize=DIMENSIONS_STR)

        # Create a new image with the desired dimensions and a black background
        with Image(**DIMENSIONS_DICT, background=Color("white")) as bg:
            # Center the resized image onto the new background image
            bg.composite(i, gravity="center")
            save_file(bg, filename, "bg-white", rot)

    # Most dominant color background extension
    with img.clone() as i:

        color = get_dominant_color(filename)

        # Resize the image while preserving the aspect ratio
        i.transform(resize=DIMENSIONS_STR)

        # Create a new image with the desired dimensions and a black background
        with Image(**DIMENSIONS_DICT, background=Color(color)) as bg:
            # Center the resized image onto the new background image
            bg.composite(i, gravity="center")
            save_file(bg, filename, "bg-dominant", rot)


def rgb_to_hex(r, g, b):
    """Convert RGB color to HEX value"""
    return f"#{r:02x}{g:02x}{b:02x}".upper()


def get_dominant_color(image_path):
    """Get the most frequently used color of an image"""
    with Image(filename=image_path) as img:
        # Resize the image to speed up the process
        img.sample(100, 100)  # Resize to 100x100 pixels

        # Get the color histogram
        histogram = img.histogram

        # Find the most frequent color
        most_frequent_color: Color = max(histogram, key=histogram.get)

        return most_frequent_color.string


def main():
    """Main function"""
    args = parser.parse_args()

    filename = args.file

    with Image(filename=filename) as img:
        # Operations on normal image
        all_operations(img, filename)

        # Operations on -90 rotated image
        img.rotate(ROTATION)

        all_operations(img, filename, rotation=True)
