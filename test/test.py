import unittest
import xml.etree.ElementTree as ET

from utils.svg_parser import find_attribute_value
from api import module


class TestFind(unittest.TestCase):
    def test_parse(self):
        tree = ET.parse("test_svg_file.svg")
        return tree.getroot()

    def test_find_attribute(self):
        parsed_tree_mock = self.test_parse()

        # 1 - Normal, 2 - Style, 3 - Element
        find_attribute_value(parsed_tree_mock, "poster", "{http://www.w3.org/1999/xlink}href", 1)
        find_attribute_value(parsed_tree_mock, "poster", "{xlink}href", 1)
        find_attribute_value(parsed_tree_mock, "desc", "fill", 2)
        find_attribute_value(parsed_tree_mock, "tspan273", "element", 3)

    def test_quick_edits(self):
        svg_path = r"Z:\GatorSVG\assets\Sample.svg"
        quick_edit_attrs = [
            {
                'ID': 'desc',
                'attribute': 'fill',
                'type': 'Style',
                'value': '#462254'
            },
            {
                'ID': 'path271',
                'attribute': 'rx',
                'type': 'Normal',
                'value': '15'
            },
            {
                'ID': 'tspan273',
                'attribute': 'tspan',
                'type': 'Element',
                'value': '8.1'
            },
        ]
        save_option = "save_as"
        save_as_name = r"Z:\GatorSVG\test\test_svg_file.svg"

        # Call the set_element function
        module.set_element(svg_path, quick_edit_attrs, save_option, save_as_name)


if __name__ == "__main__":
    unittest.main()
