import tkinter as tk

from app_vars import selected_element


class ListBox(tk.Listbox):
    """
    Custom Listbox widget to display XML elements with double-click functionality.
    """
    def __init__(self, master):
        """
        Initialize the custom Listbox.

        Args:
            master: Parent Widget (app_window).
        """
        super().__init__(master)

        # Grid settings
        self.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        master.grid_rowconfigure(1, weight=1)
        master.columnconfigure(0, minsize=350)

        self.parent = master
        self.previously_selected_item_index = 0
        self.elements = {}

        self.bind("<Double-Button-1>", self.on_listbox_select)

    def insert_listbox(self, element, level=0):
        """
        Insert an item into the Listbox.

        Args:
            element (ElementTree.Element): The XML element to insert.
            level (int): The nesting level of the element in the XML hierarchy.
        """
        indent = "  " * level
        ele_id = element.get("id")
        # Get the tag name of the element
        if ele_id is not None:  # Add a check to ensure element.tag is not None
            tag = element.tag.split("}")[-1] + "(" + ele_id + ")" + str(level)
        else:
            tag = element.tag.split("}")[-1] + "(" + ")" + str(level)
        self.elements[tag] = element
        self.insert(tk.END, f"{indent}{tag}")

    def clear_svg_listbox(self):
        """
        Clear all items from the Listbox.
        """
        self.delete(0, tk.END)

    def on_listbox_select(self, event):
        """
        Handle a double click event on an item in the Listbox.

        Args:
            event: The event object containing information about the event.
        """
        selected_item_index = self.curselection()
        self.selection_clear(0, tk.END)

        # Update the appearance of the selected item
        self.itemconfig(self.previously_selected_item_index, {'bg': 'white', 'fg': 'black'})
        self.previously_selected_item_index = selected_item_index
        self.itemconfig(selected_item_index, {'bg': 'blue', 'fg': 'white'})

        selected_item = self.get(selected_item_index).strip()
        selected_element.set_element(self.elements.get(selected_item))

        self.parent.change_selection()


if __name__ == "__main__":
    root = tk.Tk()
    # Create the ListBox instance
    listbox = ListBox(root)
    # Start the tkinter main loop
    root.mainloop()
