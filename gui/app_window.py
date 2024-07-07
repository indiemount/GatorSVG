import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import xml.etree.ElementTree as ET

from .image_preview_window import ImagePreviewWindow
from .listbox import ListBox
from .property_panel import PropertyPanel
from .quick_edits_window import QuickEditWindow
from app_vars import root_element, selected_element
from utils.config import OPEN_SVG_FILE_PATH, SVG_OUTPUT_PATH
from utils.image_helper import convert_svg_to_png, save_png_to_file
from utils.svg_parser import parse_element, save_svg_to_file


class AppWindow(tk.Frame):
    """
    Main application window that contains the top taskbar and panels.
    """
    def __init__(self, root):
        """
        Initialize the AppWindow.

        Args:
            root: The root Tkinter window.
        """
        super().__init__(root)
        self.root = root
        self.root.columnconfigure(0, weight=10)
        self.root.columnconfigure(1, weight=20)
        self.root.columnconfigure(2, weight=25)

        self.create_widgets()

    def create_widgets(self):
        """
         Create the top taskbar and panels of the app.
         """
        self.create_top_taskbar()
        self.create_panels()

    def create_top_taskbar(self):
        """
        Create the top taskbar of the app.
        """
        # Create a top taskbar frame
        top_taskbar_frame = tk.Frame(self)
        top_taskbar_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Create a menu bar
        menu_bar = tk.Menu(self)
        self.master.config(menu=menu_bar)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_changes)
        file_menu.add_command(label="Save As", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export PNG", command=self.export_png)

        # Window Menu
        window_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Window", menu=window_menu)
        window_menu.add_command(label="Image Preview", command=self.toggle_image_preview)
        window_menu.add_command(label="Quick Edits", command=self.toggle_quick_edit_window)

        # Support menu
        menu_bar.add_cascade(label="Support", command=self.support_external)

        # FAQ menu
        menu_bar.add_cascade(label="FAQ", command=self.faq_external)

    def create_panels(self):
        """
        Create the panels of the app.
        """
        self.svg_listbox = ListBox(self)
        self.image_preview_window = ImagePreviewWindow(self)
        self.property_panel = PropertyPanel(self, self.image_preview_window)
        self.quick_edit_window = QuickEditWindow(self)

    def open_file(self):
        """
        Opens a file dialog and loads the selected SVG file into the app.
        """
        # Open a file dialog for opening a file
        file_path = filedialog.askopenfilename(defaultextension=".svg", initialdir="assets")
        if file_path:
            # Check if the file is an SVG file
            if not file_path.endswith(".svg"):
                # Display an error message
                tk.messagebox.showerror("Error", "Please select an SVG file.")
                return

            OPEN_SVG_FILE_PATH.set(file_path)

            # Load the SVG file
            tree = ET.parse(OPEN_SVG_FILE_PATH.get())
            root_element.set_element(tree.getroot())
            parsed_tree = root_element.get_element()

            # Display the attributes of the SVG element
            self.svg_listbox.clear_svg_listbox()
            self.display_attributes(parsed_tree)
            save_svg_to_file(SVG_OUTPUT_PATH)
            self.image_preview_window.load_image()

            print(f"File successfully Opened {file_path}")

            # Bring the focus back to the main window
            self.root.focus_force()

    def save_changes(self):
        """
        Saves the SVG file to the currently opened file path.
        """
        save_svg_to_file(OPEN_SVG_FILE_PATH.get())

    def save_as(self):
        """
        Opens a file dialog and saves the SVG file to the selected file path.
        """
        # Ask the user where they want to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".svg", initialdir="assets")
        if file_path:
            # Save the SVG file
            save_svg_to_file(file_path)

    def export_png(self):
        """
        Exports the SVG file to a PNG image at the selected file path.
        """
        # Ask the user where they want to save the PNG file
        file_path = filedialog.asksaveasfilename(defaultextension=".png", initialdir="assets")
        if file_path:
            # Convert the SVG file to a PNG image
            image = convert_svg_to_png(SVG_OUTPUT_PATH)
            if image is not None:
                save_png_to_file(image, file_path)

    def toggle_image_preview(self):
        """
        Toggles the visibility of the image preview window.
        """
        # Toggle the image preview window
        self.image_preview_window.toggle_image_preview()

    def toggle_quick_edit_window(self):
        """
        Toggles the quick edit window.
        """
        self.quick_edit_window.toggle_window()

    def faq_external(self):
        """
         Opens the FAQ external link.
         """
        webbrowser.open_new("https://github.com/indiemount/GatorSVG")

    def support_external(self):
        """
        Opens the support external link.
        """
        webbrowser.open_new("paypal.me/indiemount")

    def display_attributes(self, element, level=0):
        """
        Recursively displays attributes of an SVG element.

        Args:
            element: The SVG element to display attributes for.
            level: The depth level of the element in the hierarchy.
        """
        self.svg_listbox.insert_listbox(element, level)

        parse_element(element, self.property_panel)

        for child in element:
            self.display_attributes(child, level + 1)

        self.property_panel.clear_displayed_attributes()

    def change_selection(self):
        """
        Updates the property panel to display the attributes of the selected element.

        This function retrieves the selected element and updates the property panel to
        display its attributes. If no element is selected, the function returns without
        making any changes.

        """
        self.property_panel.clear_displayed_attributes()
        select = selected_element.get_element()

        if select is None:
            return

        self.property_panel.check_text(select)

        parse_element(select, self.property_panel)


if __name__ == "__main__":
    root = tk.Tk()
    app_window = AppWindow(root)
    root.mainloop()
