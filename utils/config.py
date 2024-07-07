# Configuration variables

# File paths
SVG_OUTPUT_PATH = "assets/Test.svg"
ASSETS_DIR = "assets"


class InkscapePath:
    """
    Singleton class representing the path to the Inkscape executable.
    """
    def __init__(self):
        self.path = None

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of InkscapePath.

        Returns:
            InkscapePath: The singleton instance of InkscapePath.
        """
        if not hasattr(InkscapePath, '_instance'):
            InkscapePath._instance = InkscapePath()
        return InkscapePath._instance

    def get(self):
        """
        Get the Inkscape executable path.

        Returns:
            str: The Inkscape executable path.
        """
        return self.path

    def set(self, new_path):
        """
        Set the Inkscape executable path.

        Args:
            new_path (str): The new path to set.
        """
        self.path = new_path


INKSCAPE_PATH = InkscapePath.get_instance()


class SVGFilePath:
    """
    Singleton class representing the path to the open SVG file.
    """
    def __init__(self):
        self.path = None

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of SVGFilePath.

        Returns:
            SVGFilePath: The singleton instance of SVGFilePath.
        """
        if not hasattr(SVGFilePath, '_instance'):
            SVGFilePath._instance = SVGFilePath()
        return SVGFilePath._instance

    def get(self):
        """
        Get the open SVG file path.

        Returns:
            str: The open SVG file path.
        """
        return self.path

    def set(self, new_path):
        """
        Set the open SVG file path.

        Args:
            new_path (str): The new path to set.
        """
        self.path = new_path


OPEN_SVG_FILE_PATH = SVGFilePath.get_instance()
