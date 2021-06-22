import os
from xml.etree.ElementTree import ElementTree as XMLTree

from defusedxml import ElementTree

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.image import Image

from .._format import VOCODFormat


class VOCODReader(AnnotationFileProcessor[VOCODFormat]):
    """
    Reader of Pascal VOC object-detection files.
    """
    def read_annotation_file(
            self,
            filename: str,
            then: ThenFunction[VOCODFormat]
    ):
        # Parse the contents
        voc_file: XMLTree = ElementTree.parse(filename)

        # Get the filename of the image from the XML
        image_filename = os.path.join(
            os.path.dirname(filename),
            voc_file.findtext("folder"),
            voc_file.findtext("filename")
        )

        image = Image.from_file(image_filename)

        then((image, voc_file))

    def read_negative_file(
            self,
            filename: str,
            then: ThenFunction[VOCODFormat]
    ):
        image_info = Image.from_file(filename)

        then((image_info, None))
