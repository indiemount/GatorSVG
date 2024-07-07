import os
import sys
import xml.etree.ElementTree as ET

from app_vars import root_element, namespace_mappings
from utils.config import OPEN_SVG_FILE_PATH


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    Args:
        relative_path: The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2

    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def convert_image_path(image_path):
    """
    Converts the respective Image_Path to the actual image path.

    Args:
        image_path: The path to the image file.

    Returns:
        str: The absolute path to the image file.
    """
    if "file" in image_path:
        return image_path
    if not os.path.isabs(image_path):
        absolute_svg_path = os.path.abspath(OPEN_SVG_FILE_PATH.get())
        image_path = os.path.abspath(os.path.join(os.path.dirname(absolute_svg_path), image_path))
        image_path = "file:///" + image_path
        print(image_path)
    return image_path


def save_svg_to_file(save_path):
    """
    Save the changes made to the SVG file.

    Args:
        save_path: The path to save the SVG file.

    Returns:
        bool: True if the changes are saved successfully, False otherwise.
    """
    try:
        svg_string = ET.tostring(root_element.get_element(), encoding="unicode", short_empty_elements=False)
        svg_string = svg_string.replace("><", ">\n<")

        if not os.path.exists(save_path):
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(svg_string)
        else:
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(svg_string)

        print("Changes saved successfully! \nSaved to", save_path)
        return True

    except Exception as e:
        print(f"Error saving SVG image: {e}")
        return False


def is_image(element, attr, value):
    """
    Check if the attribute value represents an image.

    Args:
        element: The XML element.
        attr: The name of the attribute.
        value: The value of the attribute.

    Returns:
        None
    """
    if "href" in attr and "#" not in value:
        set_attribute_value(root_element.get_element(), element.get('id'), attr, 1, convert_image_path(value.strip()))


def parse_style(style):
    """
    Parse the style attribute and return a dictionary of style properties.

    Args:
        style: The value of the style attribute.

    Returns:
        dict: A dictionary of style properties.
    """
    style_dict = {}
    if style:
        style_properties = style.split(";")
        for prop in style_properties:
            if ":" in prop:
                key, value = prop.split(":")
                style_dict[key.strip()] = value.strip()
    return style_dict


def style_dict_to_string(style_dict):
    """
    Convert a dictionary of style properties to a style attribute string.

    Args:
        style_dict: A dictionary of style properties.

    Returns:
        str: The style attribute string.
    """
    style_string = ""
    for key, value in style_dict.items():
        if style_string:
            style_string += ";"
        style_string += f"{key}:{value}"

    return style_string


def parse_element(element, property_panel):
    """
    Parse an XML element and display its attributes on the property panel.

    Args:
        element: The XML element to parse.
        property_panel: The PropertyPanel instance to display attributes.

    Returns:
        None
    """
    for attr, value in element.items():
        if attr == "style":
            style_dict = parse_style(value)
            for style_attr, style_value in style_dict.items():
                property_panel.display_attribute(style_attr, style_value, 2)
        else:
            property_panel.display_attribute(attr, value, 1)
            is_image(element, attr, value)


def get_key_by_value(target_value):
    """
    Get the key corresponding to a given value in the namespace_mappings dictionary.

    Args:
        target_value: The value to find.

    Returns:
        str: The key corresponding to the given value.
    """
    for key, value in namespace_mappings.items():
        if value == target_value:
            return key
    return None


def find_attribute_value(root, element_id, attribute_name, type_id):
    """
    Find the value of a specified attribute in the SVG element.

    Args:
        root: The root SVG element.
        element_id: The ID of the SVG element.
        attribute_name: The name of the attribute.
        type_id: The type of attribute (1 - Normal, 2 - Style, 3 - Element).

    Returns:
        str: The value of the specified attribute.
    """
    element = root.find(f".//*[@id='{element_id}']")

    if element is None:
        print(f"Element with id '{element_id}' not found.")
        return None

    if attribute_name.startswith("{"):
        namespace_name = attribute_name.split("}")[0][1:]
        namespace_uri = get_key_by_value(namespace_name)
        if namespace_uri is not None:
            attribute_name = "{" + namespace_uri + "}" + attribute_name.split("}")[1]

    if type_id == 2:
        style_value = element.get("style")
        style_dict = parse_style(style_value)
        attribute_value = style_dict.get(attribute_name)

        if style_value is not None:
            if attribute_name in style_dict:
                print(f"Attribute value for Style {element_id}.{attribute_name}: {attribute_value}")
                return attribute_value
            else:
                print(f"Style Attribute {attribute_name} not found for element {element_id}")

    if type_id == 3:
        if element.text is not None:
            print(f"Attribute value for element {element_id}: {element.text}")
            return element.text
        else:
            print(f"Text content not found for element {element_id}")

    if type_id == 1:
        if attribute_name in element.attrib:
            print(f"Attribute value for {element_id}.{attribute_name}: {element.attrib[attribute_name]}")
            return element.attrib[attribute_name]
        else:
            print(f"Attribute {attribute_name} not found for element {element_id}")

    return None


def set_attribute_value(root, element_id, attribute_name, type_id, new_value):
    """
    Set the value of an attribute in the SVG element.

    Args:
        root: The root SVG element.
        element_id: The ID of the SVG element to modify.
        attribute_name: The name of the attribute.
        type_id: The type of attribute (1 - Normal, 2 - Style, 3 - Element).
        new_value: The new value to set for the attribute.

    Returns:
        int: 1 if the value is changed, 0 otherwise.
    """
    if attribute_name.startswith("{"):
        namespace_name = attribute_name.split("}")[0][1:]
        namespace_uri = get_key_by_value(namespace_name)
        if namespace_uri is not None:
            attribute_name = "{" + namespace_uri + "}" + attribute_name.split("}")[1]

    select = root.find(f".//*[@id='{element_id}']")
    is_value_changed = update_svg_attribute(select, attribute_name, type_id, new_value)
    return is_value_changed


def update_svg_attribute(select, attribute_name, type_id, new_value):
    """
    Set the value of an attribute in the SVG element.

    Args:
        select: The SVG element to modify.
        attribute_name: The name of the attribute.
        type_id: The type of attribute (1 - Normal, 2 - Style, 3 - Element).
        new_value: The new value to set for the attribute.

    Returns:
        int: 1 if the value is changed, 0 otherwise.
    """
    if select is None:
        print(f"Error Changing Property")
        return 0

    style_attr = None
    style_dict = None
    style_value = select.get("style")
    if style_value is not None:
        style_dict = parse_style(style_value)
        style_attr = style_dict.get(attribute_name)

    # For Normal attr
    if new_value != select.get(
            attribute_name) and attribute_name in select.attrib and style_attr is None and type_id == 1:
        select.set(attribute_name, new_value)
        print(f"Attribute {attribute_name} changed to: {new_value}")
        return 1
    # For elements
    elif new_value != select.text and attribute_name not in select.attrib and style_attr is None and type_id == 3:
        select.text = new_value
        print(f"Element {select.tag} changed to: {new_value}")
        return 1
    # For style
    elif style_attr is not None and type_id == 2:
        if new_value != style_attr:
            style_dict[attribute_name] = new_value
            select.set("style", style_dict_to_string(style_dict))
            print(f"Style {attribute_name} changed to: {new_value}")
            return 1

    print(f"Error Changing Property")
    return 0
