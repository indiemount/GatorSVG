import platform
import subprocess
import tkinter as tk

from PIL import Image, ImageTk
from gui.app_window import AppWindow
from utils.config import INKSCAPE_PATH
from utils.svg_parser import resource_path


def is_inkscape_installed():
    """
    Check if Inkscape is installed on the system.

    Returns:
        bool: True if Inkscape is installed, False otherwise.
    """
    try:
        subprocess.run(["inkscape", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False


def get_inkscape_path():
    """
    Get the path to the Inkscape executable based on the operating system.

    This function sets the INKSCAPE_PATH variable to the path of the Inkscape executable.

    Note: Some features of the program may not work if Inkscape is not installed.

    Raises:
        subprocess.CalledProcessError: If the subprocess to find Inkscape fails.
    """
    operating_system = platform.system()

    try:
        if is_inkscape_installed():
            if operating_system == "Windows":
                INKSCAPE_PATH.set(resource_path(subprocess.check_output(["where", "inkscape.exe"]).decode("utf-8").strip()))
                print(f"Inkscape is installed at {INKSCAPE_PATH.get()}")
            elif operating_system == "Darwin" or operating_system == "Linux":
                INKSCAPE_PATH.set(resource_path(subprocess.check_output(["which", "inkscape.exe"]).decode("utf-8").strip()))
                print(f"Inkscape is installed at {INKSCAPE_PATH.get()}")
        else:
            print("Some Features of the Program will not work. Please install Inkscape to make it work.")
    except Exception as e:
        print(e)
        exit(1)


def initialize_app():
    """
    Initialize the PropertyPanel.

    This function sets up the main Tkinter window, initializes the AppWindow, sets the application icon,
    and starts the Tkinter event loop.
    """
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("GatorSVG")
    root.geometry('1250x500')

    # Initialize the main window
    app_window = AppWindow(root)

    # Create a PhotoImage object for the image file "logo.png".
    logo = ImageTk.PhotoImage(Image.open(resource_path("assets/LogoGatorSVG.png")))

    # Set the icon for the app window using the PhotoImage object.
    root.iconphoto(True, logo)

    app_window.pack(fill=tk.BOTH, expand=True)

    # Open the file when the application starts
    app_window.open_file()

    # Start the Tkinter event loop
    root.mainloop()


def main():
    """
    Entry point for the application.

    This function initializes the Inkscape path and sets up the application.
    """
    get_inkscape_path()  # Ensures the correct Inkscape path is obtained.
    initialize_app()     # Initializes the application.


if __name__ == "__main__":
    main()
