from xml.etree.ElementTree import Element

from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.domain.image.object_detection.util import set_object_label

from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject

from .._format import VOCODFormat


class FromVOCOD(
    RequiresNoFinalisation,
    ProcessorComponent[VOCODFormat, ImageObjectDetectionInstance]
):
    """
    Converter from VGG annotations to internal format.
    """
    def process_element(
            self,
            element: VOCODFormat,
            then: ThenFunction[ImageObjectDetectionInstance],
            done: DoneFunction
    ):
        # Unpack the external format
        image_info, xml = element

        # Extract located objects from the XML
        located_objects = None
        if xml is not None:
            located_objects = LocatedObjects(map(self.to_located_object, xml.findall("object")))

        then(
            ImageObjectDetectionInstance(
                image_info,
                located_objects
            )
        )

    @staticmethod
    def to_located_object(object_element: Element) -> LocatedObject:
        """
        Converts the XML <object> sub-section to a located object.

        :param object_element:
                    The <object> XML.
        :return:
                    The located object.
        """
        # Get the object label
        label: str = object_element.findtext("name")

        # Get the bounding box XML element
        bndbox_element = object_element.find("bndbox")

        # Get the boundary co-ordinates
        x_min = int(bndbox_element.findtext("xmin"))
        x_max = int(bndbox_element.findtext("xmax"))
        y_min = int(bndbox_element.findtext("ymin"))
        y_max = int(bndbox_element.findtext("ymax"))

        # Create the located object
        located_object = LocatedObject(x_min, y_min, x_max - x_min + 1, y_max - y_min + 1)
        set_object_label(located_object, label)

        return located_object
