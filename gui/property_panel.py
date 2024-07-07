import tkinter as tk

from app_vars import namespace_mappings, root_element, selected_element
from utils.config import SVG_OUTPUT_PATH
from utils.svg_parser import find_attribute_value, save_svg_to_file, update_svg_attribute


class PropertyPanel(tk.Frame):
    """
    Represents the Property Panel in the GUI.
    """
    def __init__(self, master, image_preview_panel):
        """
        Initialize the PropertyPanel.

        Args:
            master: The parent tkinter widget.
            image_preview_panel: The image preview panel to interact with.
        """
        super().__init__(master)

        self.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.image_preview_panel = image_preview_panel

        # Create widgets and layout for the property panel
        self.master.label = tk.Label(self, text="Property Panel")
        self.master.label.pack()

        self.property_entries = {}
        self.displayed_attributes = {}

    def clear_displayed_attributes(self):
        """
        Clear all the displayed attributes in the PropertyPanel.
        """

        for attr, widgets in self.displayed_attributes.items():
            for widget in widgets:
                widget.destroy()

        # Clear the dictionary
        self.displayed_attributes.clear()

        for widget in self.winfo_children():
            widget.destroy()

    def check_text(self, select):
        """
        Check if the selected_element contains a <text> element and display its attributes.

        Args:
            select: The selected XML element.
        """
        if "{http://www.w3.org/2000/svg}tspan" in select.tag:
            self.display_attribute(select.tag, select.text, 3)

    def display_attribute(self, attr, value, type_id):
        """
        Display an attribute along with its value and buttons for getting and setting values.

        Args:
            attr: The name of the attribute.
            value: The current value of the attribute.
            type_id: The type of attribute (1 - Normal, 2 - Style, 3 - Element).
        """
        # Create a frame to contain the attribute label and entry
        attribute_frame = tk.Frame(self)
        attribute_frame.pack(side=tk.TOP, fill=tk.X, padx=5)
        attr_label = tk.Label(attribute_frame)

        # Display namespace rather than the whole link
        if attr.startswith("{"):
            namespace_uri, attribute_name = attr.split("}")[0][1:], attr.split("}")[1]

            found_namespace = False  # Flag variable

            for uri, known_prefix in namespace_mappings.items():
                if uri in namespace_uri:
                    namespace_uri = known_prefix
                    display_key = "{" + namespace_uri + "}" + attribute_name
                    if type_id == 1:
                        attr_label = tk.Label(attribute_frame, text=f"{display_key}:")
                    elif type_id == 3:
                        attr_label = tk.Label(attribute_frame, text=f"(element){display_key}:")
                    else:
                        attr_label = tk.Label(attribute_frame, text=f"(style){display_key}:")

                    found_namespace = True
                    break  # Exit the loop when the namespace is found

            if not found_namespace:
                attr_label = tk.Label(attribute_frame, text=f"{attribute_name}:")
        else:
            if type_id == 2:
                attr_label = tk.Label(attribute_frame, text=f"(style){attr}:")
            else:
                attr_label = tk.Label(attribute_frame, text=f"{attr}:")

        attr_label.grid(row=0, column=0, sticky="w")

        entry = tk.Entry(attribute_frame)
        entry.insert(0, value)
        entry.grid(row=0, column=1, sticky="w")
        attribute_frame.grid_rowconfigure(0, weight=1)
        attribute_frame.grid_columnconfigure(0, minsize=200)
        attribute_frame.grid_columnconfigure(1, minsize=150)

        get_button = tk.Button(attribute_frame, text="Get", width=10, relief="groove", bg="white", command=lambda: self.get_value(entry, attr, type_id))
        set_button = tk.Button(attribute_frame, text="Set", width=10, relief="groove", bg="white", command=lambda: self.set_value(entry.get(), attr, type_id))

        get_button.grid(row=0, column=2, padx=5, pady=5)
        set_button.grid(row=0, column=3, padx=5, pady=5)

        if type_id == 1:
            self.property_entries[attr] = entry

        self.displayed_attributes[attr] = (attribute_frame, attr_label, entry)

    def get_value(self, entry, attribute_name, type_id):
        """
        Get the value of an attribute and update the entry field with it.

        Args:
            entry: The tkinter Entry widget to display the value.
            attribute_name: The name of the attribute.
            type_id: The type of attribute (1 - Normal, 2 - Style, 3 - Element).
        """

        element_id = selected_element.get_element().get('id')
        # Get the value of the attribute
        value = find_attribute_value(root_element.get_element(), element_id, attribute_name, type_id)

        # If the value is found, paste it to the entry
        if value is not None:
            entry.delete(0, tk.END)
            entry.insert(0, value)
        else:
            print(f"Value for {element_id}.{attribute_name}: Not Found!")

    def set_value(self, new_value, attr, type_id):
        """
        Set the value of an attribute based on the input in the entry field.

        Args:
            new_value: The tkinter Entry widget containing the new value.
            attr: The name of the attribute.
            type_id: The type of attribute (1 - Normal, 2 - Style, 3 - Element).
        """
        select = selected_element.get_element()
        is_value_changed = update_svg_attribute(select, attr, type_id, new_value)

        if is_value_changed == 1:
            save_svg_to_file(SVG_OUTPUT_PATH)
            self.image_preview_panel.load_image()


if __name__ == "__main__":
    root = tk.Tk()
    property_panel = PropertyPanel(root)
    property_panel.pack(fill=tk.BOTH, expand=True)
    root.mainloop()