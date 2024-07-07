import subprocess

from io import BytesIO
from PIL import Image
from utils.config import INKSCAPE_PATH
from utils.svg_parser import resource_path


def convert_svg_to_png(load_file_path):
    """
    Convert an SVG file to a PNG image.

    Args:
        load_file_path (str): The file path of the SVG file to be converted.

    Returns:
        Image: A Pillow image object representing the converted PNG.
            Returns None if the conversion process encounters an error.
    """
    try:
        # Run Inkscape command to convert SVG to PNG and capture the output
        result = subprocess.run(
            [INKSCAPE_PATH.get(), '--export-type=png', '--export-filename=-',
             resource_path(load_file_path)], capture_output=True, check=True)

        # Create a Pillow image from the PNG data
        image = Image.open(BytesIO(result.stdout))

        return image
    except subprocess.CalledProcessError as e:
        print(f"Error running Inkscape: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def save_png_to_file(image, save_file_path):
    """
    Save a Pillow image to a PNG file.

    Args:
        image (Image): The Pillow image object to be saved.
        save_file_path (str): The file path where the PNG image will be saved.

    Raises:
        Exception: If the saving process encounters an error.
    """
    try:
        if image:
            # Save the image to the specified output file path
            image.save(save_file_path)

            print(f"Image saved to {save_file_path}")
        else:
            print("Image conversion failed. Cannot save.")
    except Exception as e:
        print(f"Error: {e}")
