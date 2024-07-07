"""
Module-level constants and classes related to XML namespaces and elements.

Namespace mappings are used to shorten the display of XML namespaces in attribute labels.
The RootElement and SelectedElement classes are singleton classes used to store the root element
and the currently selected element, respectively.
"""

namespace_mappings = {
    "http://www.w3.org/XML/1998/namespace": "xml",
    "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd": "sodipodi",
    "http://www.inkscape.org/namespaces/inkscape": "inkscape",
    "http://www.w3.org/1999/xlink": "xlink",
    "http://www.w3.org/2000/svg": "svg"
}


class RootElement:
    """
    Singleton class representing the root element of the SVG document.
    """
    def __init__(self):
        self.element = None

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of RootElement.

        Returns:
            RootElement: The singleton instance of RootElement.
        """
        if not hasattr(RootElement, '_instance'):
            RootElement._instance = RootElement()
        return RootElement._instance

    def get_element(self):
        """
        Get the root element.

        Returns:
            Element: The root element.
        """
        return self.element

    def set_element(self, element):
        """
        Set the root element.

        Args:
            element (Element): The root element to be set.
        """
        self.element = element


root_element = RootElement.get_instance()


class SelectedElement:
    """
    Singleton class representing the currently selected element in the SVG document.
    """
    def __init__(self):
        self.element = None

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of SelectedElement.

        Returns:
            SelectedElement: The singleton instance of SelectedElement.
        """
        if not hasattr(SelectedElement, '_instance'):
            SelectedElement._instance = SelectedElement()
        return SelectedElement._instance

    def get_element(self):
        """
        Get the currently selected element.

        Returns:
            Element: The currently selected element.
        """
        return self.element

    def set_element(self, element):
        """
        Set the currently selected element.

        Args:
            element (Element): The element to be set as the currently selected element.
        """
        self.element = element


selected_element = SelectedElement.get_instance()

