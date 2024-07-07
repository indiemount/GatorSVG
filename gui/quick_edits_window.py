import tkinter as tk

from tkinter import filedialog, ttk
from app_vars import root_element
from utils.config import SVG_OUTPUT_PATH
from utils.svg_parser import find_attribute_value, save_svg_to_file, set_attribute_value


class QuickEditWindow:
    """
    Represents the Quick Edit window for modifying SVG attributes.
    """
    def __init__(self, root):
        """
        Initialize the QuickEditWindow.

        Args:
            root: The root Tkinter window.
        """

        self.input_frame = None
        self.load_button = None
        self.save_button = None
        self.add_button = None
        self.root = root
        self.rows = []  # List to store the rows of inputs

        self.quick_edit_window = None
        self.create_window()

    def create_window(self):
        """
        Create and configure the Quick Edit window and its components.
        """

        self.quick_edit_window = tk.Toplevel(self.root)
        self.quick_edit_window.title("Quick Edit")

        taskbar = tk.Menu(self.quick_edit_window)
        self.quick_edit_window.config(menu=taskbar)
        taskbar.add_command(label="Add", command=self.add_row)
        taskbar.add_command(label="Save", command=self.save_data)
        taskbar.add_command(label="Load", command=self.load_data)
        taskbar.config(borderwidth=1, relief="solid")

        self.quick_edit_window.protocol("WM_DELETE_WINDOW", self.toggle_window)

    def add_row(self):
        """
        Add a new row of input fields to the Quick Edit window.
        """
        # Create a new row with inputs for element_id, attribute_name, type, and value
        row_frame = ttk.Frame(self.quick_edit_window)
        row_frame.pack(side=tk.TOP, padx=5, pady=5)

        element_id_label = ttk.Label(row_frame, text="ID:")
        element_id_label.pack(side=tk.LEFT, padx=5, pady=5)

        element_id_entry = ttk.Entry(row_frame)
        element_id_entry.pack(side=tk.LEFT, padx=5, pady=5)

        attribute_name_label = ttk.Label(row_frame, text="Attribute:")
        attribute_name_label.pack(side=tk.LEFT, padx=5, pady=5)

        attribute_name_entry = ttk.Entry(row_frame)
        attribute_name_entry.pack(side=tk.LEFT, padx=5, pady=5)

        type_label = ttk.Label(row_frame, text="Type:")
        type_label.pack(side=tk.LEFT, padx=5, pady=5)

        type_dropdown = ttk.Combobox(row_frame, values=("Normal", "Style", "Element"))
        type_dropdown.pack(side=tk.LEFT, padx=5, pady=5)

        value_label = ttk.Label(row_frame, text="Value:")
        value_label.pack(side=tk.LEFT, padx=5, pady=5)

        value_entry = ttk.Entry(row_frame)
        value_entry.pack(side=tk.LEFT, padx=5, pady=5)

        get_button = ttk.Button(row_frame, text="Get", command=lambda: self.get_value(row_frame))
        set_button = ttk.Button(row_frame, text="Set", command=lambda: self.set_value(row_frame))

        get_button.pack(side=tk.LEFT, padx=5, pady=5)
        set_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = ttk.Button(row_frame, text="Delete", command=lambda: self.delete_row(row_frame))
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Append the new row to the rows list
        self.rows.append((element_id_entry, attribute_name_entry, type_dropdown, value_entry, row_frame))

    def get_value(self, row_frame):
        """
        Get the attribute value for a selected element and display it in the corresponding input field.

        Args:
            row_frame: The frame containing the input fields.
        """

        # Find the index of the row_frame in the rows list
        index = None
        for i, row in enumerate(self.rows):
            if row_frame == row[0].master:
                index = i
                break

        if index is not None:
            element_id = self.rows[index][0].get()
            attribute_name = self.rows[index][1].get()
            type_id = ["Normal", "Style", "Element"].index(self.rows[index][2].get()) + 1
            value = find_attribute_value(root_element.get_element(), element_id, attribute_name, type_id)

            if value is not None:
                self.rows[index][3].delete(0, tk.END)
                self.rows[index][3].insert(0, value)
            else:
                print(f"Value for {element_id}.{attribute_name}: Not Found!")

    def set_value(self, row_frame):
        """
        Set the attribute value for a selected element based on the input field values.

        Args:
            row_frame: The frame containing the input fields.
        """

        # Find the index of the row_frame in the rows list
        index = None
        for i, row in enumerate(self.rows):
            if row_frame == row[0].master:
                index = i
                break

        if index is not None:
            element_id = self.rows[index][0].get()
            attribute_name = self.rows[index][1].get()
            type_id = ["Normal", "Style", "Element"].index(self.rows[index][2].get()) + 1
            value = self.rows[index][3].get()

            if set_attribute_value(root_element.get_element(), element_id, attribute_name, type_id, value) == 1:
                self.root.change_selection()
                save_svg_to_file(SVG_OUTPUT_PATH)
                self.root.image_preview_window.load_image()

    def delete_row(self, row_frame):
        """
        Delete a row of input fields from the Quick Edit window.

        Args:
            row_frame: The frame containing the input fields to be deleted.
        """

        # Find the index of the row_frame in the rows list
        index_to_delete = None
        for i, row in enumerate(self.rows):
            if row_frame == row[-1]:  # Check if the last element of the tuple is the row_frame
                index_to_delete = i
                break

        if index_to_delete is not None:
            # Remove the last row from the rows list
            deleted_row = self.rows.pop(index_to_delete)

            # Destroy widgets in the deleted row (excluding the row_frame)
            for widget in deleted_row[:-1]:
                widget.destroy()

            # Remove the row_frame from the packing
            row_frame.pack_forget()

            # Destroy the row_frame
            row_frame.destroy()

        else:
            print("Row not found in self.rows")

    def save_data(self):
        """
        Save the data from the input fields to a text file using a file dialog.
        """

        # Open a file dialog for saving the data
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialdir="assets",
                                                 initialfile="quick_edits.txt")
        if file_path:
            with open(file_path, "w") as file:
                for row in self.rows:
                    element_id = row[0].get()
                    attribute_name = row[1].get()

                    # Check if there is a value in the type_dropdown
                    type_value = row[2].get()
                    type_id = type_value if type_value in ["Normal", "Style", "Element"] else ''

                    value = row[3].get()
                    file.write(f"{element_id},{attribute_name},{type_id},{value}\n")

    def load_data(self):
        """
        Load data from a text file and populate the input fields using a file dialog.
        """

        # Open a file dialog for loading data
        file_path = filedialog.askopenfilename(defaultextension=".txt", initialdir="assets")
        if file_path:
            try:
                # Clear all existing rows
                for row in self.rows:
                    for widget in row:
                        widget.destroy()
                self.rows.clear()

                with open(file_path, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        values = line.strip().split(",")
                        if len(values) == 4:
                            element_id_value, attribute_name_value, type_value, value = values
                            self.add_row()
                            self.rows[-1][0].insert(0, element_id_value)
                            self.rows[-1][1].insert(0, attribute_name_value)
                            self.rows[-1][2].set(type_value)
                            self.rows[-1][3].insert(0, value)
            except Exception as e:
                print(f"Error loading data: {e}")

    def toggle_window(self):
        """
        Toggle the visibility of the Quick Edit window between hidden and shown states.
        """

        if self.quick_edit_window and self.quick_edit_window.winfo_exists():
            # If the Quick Edit window exists, toggle its visibility
            if self.quick_edit_window.winfo_viewable():
                self.quick_edit_window.withdraw()  # Hide the window
            else:
                self.quick_edit_window.deiconify()  # Show the window
        else:
            # If the Quick Edit window does not exist or is closed, create it
            self.quick_edit_window = QuickEditWindow(self.root)

        self.quick_edit_window.lift()


if __name__ == "__main__":
    root = tk.Tk()

    # Create the QuickEditWindow instance
    quick_edit_window = QuickEditWindow(root)

    root.mainloop()
