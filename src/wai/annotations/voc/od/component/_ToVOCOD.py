import os
from typing import Any
from xml.etree.ElementTree import Element, ElementTree

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image import Image
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.domain.image.object_detection.util import get_object_label

from wai.common.adams.imaging.locateobjects import LocatedObject

from .._format import VOCODFormat


class ToVOCOD(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, VOCODFormat]
):
    """
    Converter from internal format to Pascal VOC annotations.
    """
    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[VOCODFormat],
            done: DoneFunction
    ):
        image_info, located_objects = element

        if located_objects is None or len(located_objects) == 0:
            return then((image_info, None))

        root = Element("annotation")

        ToVOCOD.append_simple_element(root, "folder", os.path.dirname(image_info.filename))
        ToVOCOD.append_simple_element(root, "filename", os.path.basename(image_info.filename))

        root.append(self.size_element(image_info))

        for located_object in located_objects:
            root.append(self.object_element(located_object))

        then((image_info, ElementTree(root)))

    @staticmethod
    def size_element(image_info: Image) -> Element:
        """
        Creates a size element describing the dimensions of the image.

        :param image_info:
                    The source image.
        :return:
                    The <size> XML element.
        """
        root = Element("size")

        ToVOCOD.append_simple_element(root, "width", image_info.width)
        ToVOCOD.append_simple_element(root, "height", image_info.height)
        ToVOCOD.append_simple_element(root, "depth", 3)

        return root

    @staticmethod
    def object_element(located_object: LocatedObject) -> Element:
        """
        Creates an object element describing a single detected object.

        :param located_object:
                    The detected object to describe.
        :return:
                    The <object> XML element.
        """
        root = Element("object")

        ToVOCOD.append_simple_element(root, "name", get_object_label(located_object))
        ToVOCOD.append_simple_element(root, "pose", "Unspecified")
        ToVOCOD.append_simple_element(root, "truncated", 0)
        ToVOCOD.append_simple_element(root, "difficult", 0)

        bndbox_element = Element("bndbox")
        ToVOCOD.append_simple_element(bndbox_element, "xmin", located_object.x)
        ToVOCOD.append_simple_element(bndbox_element, "ymin", located_object.y)
        ToVOCOD.append_simple_element(bndbox_element, "xmax", located_object.x + located_object.width - 1)
        ToVOCOD.append_simple_element(bndbox_element, "ymax", located_object.y + located_object.height - 1)
        root.append(bndbox_element)

        return root

    @staticmethod
    def append_simple_element(to: Element, tag: str, text: Any):
        """
        Short-hand to append a simple element to a parent element.

        :param to:
                    The element to append the new element to.
        :param tag:
                    The tag-type of the new element.
        :param text:
                    The text content of the new element.
        """
        element = Element(tag)
        element.text = str(text)
        to.append(element)
