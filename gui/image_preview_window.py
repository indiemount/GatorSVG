import tkinter as tk

from PIL import ImageTk
from utils.config import SVG_OUTPUT_PATH
from utils.image_helper import convert_svg_to_png


class ImagePreviewWindow:
    """
    Class representing a window for previewing the image.
    """
    def __init__(self, parent):
        """
        Initialize the ImagePreviewWindow.

        Args:
            parent: The parent window.
        """
        self.root = parent

        # Initialize zoom level
        self.zoom_level = 1.0

        # Create a Toplevel window for the image preview
        self.image_preview_window = tk.Toplevel(parent)
        self.image_preview_window.title("Image Preview")

        # Create an empty ImageTk.PhotoImage
        self.photo = None

        # Create a Label widget to display the image
        self.image_label = tk.Label(self.image_preview_window)
        self.image_label.pack()

        # Bind mouse scroll events to the zoom function
        self.image_preview_window.bind("<MouseWheel>", self.zoom)
        self.image_preview_window.protocol("WM_DELETE_WINDOW", self.toggle_image_preview)

    def toggle_image_preview(self):
        """
        Toggle the visibility of the image preview window.
        """
        if self.image_preview_window and self.image_preview_window.winfo_exists():
            # If the Quick Edit window exists, toggle its visibility
            if self.image_preview_window.winfo_viewable():
                self.image_preview_window.withdraw()  # Hide the window
            else:
                self.image_preview_window.deiconify()  # Show the window
        else:
            # If the Quick Edit window does not exist or is closed, create it
            self.image_preview_window = ImagePreviewWindow(self.root)
            self.image_preview_window.load_image()

        self.image_preview_window.lift()

    def load_image(self):
        """
        Load and display the image in the preview window.
        """
        # Convert SVG to PNG
        image = convert_svg_to_png(SVG_OUTPUT_PATH)

        # Resize based on the zoom level
        width, height = image.size
        new_width = int(width * self.zoom_level)
        new_height = int(height * self.zoom_level)
        image = image.resize((new_width, new_height))

        # Convert the resized image to PhotoImage
        self.photo = ImageTk.PhotoImage(image=image)

        # Update the image in the Label widget
        self.image_label.config(image=self.photo)
        self.image_label.update_idletasks()  # Update the display

    def zoom(self, event):
        """
        Handle zooming in and out using mouse scroll.

        Args:
            event: The mouse scroll event.
        """
        # Adjust the zoom level based on the mouse scroll direction
        if event.delta > 0:  # Scroll up (zoom in)
            self.zoom_level *= 1.2
        else:  # Scroll down (zoom out)
            self.zoom_level /= 1.2

        # Reload and display the image with the updated zoom level
        self.load_image()


if __name__ == "__main__":
    root = tk.Tk()

    # Create the ImagePreviewWindow instance
    image_preview = ImagePreviewWindow(root)

    root.mainloop()
