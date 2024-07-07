from utils.svg_parser import set_attribute_value
import xml.etree.ElementTree as ET


def save_svg_to_file(svg_path, root_element):
    """
    Save the modified SVG data to a file.

    Args:
        svg_path (str): The path to save the SVG file.
        root_element (Element): The root element of the modified SVG data.
    """
    # Create an ElementTree object with the root element
    tree = ET.ElementTree(root_element)

    # Write the ElementTree to the SVG file
    tree.write(svg_path)


def set_element(svg_path, quick_edit_attrs, save_option, save_as_name=None):
    """
    Modify the specified attribute of an SVG element.

    Args:
        svg_path (str): The path to the SVG file.
        quick_edit_attr (dict): A dictionary containing the ID, attribute name, type, and value.
        save_option (str): Option for saving: 'save' or 'save_as'.
        save_as_name (str, optional): The name to use when saving as a new file. Required if save_option is 'save_as'.
    """
    # Parse the SVG file
    tree = ET.parse(svg_path)
    root = tree.getroot()

    for attr in quick_edit_attrs:
        element_id = attr['ID']
        attribute_name = attr['attribute']
        type_id = {'Normal': 1, 'Style': 2, 'Element': 3}[attr['type']]
        new_value = attr['value']

        # Find the element with the specified ID and set its attribute value
        if set_attribute_value(root, element_id, attribute_name, type_id, new_value):
            # Save or Save As functionality based on save_option
            if save_option == 'save':
                save_svg_to_file(svg_path, root)
            elif save_option == 'save_as' and save_as_name:
                save_svg_to_file(save_as_name, root)
        else:
            print("Error Changing Value", element_id)
