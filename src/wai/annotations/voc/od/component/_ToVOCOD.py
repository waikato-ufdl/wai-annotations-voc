from wai.annotations.core.component import ProcessorComponent
from wai.annotations.core.stream import ThenFunction, DoneFunction
from wai.annotations.core.stream.util import RequiresNoFinalisation
from wai.annotations.domain.image.object_detection import ImageObjectDetectionInstance
from wai.annotations.domain.image.object_detection.util import get_object_label, get_object_prefix

from .._format import VOCODFormat


class ToVOCOD(
    RequiresNoFinalisation,
    ProcessorComponent[ImageObjectDetectionInstance, VOCODFormat]
):
    """
    Converter from internal format to VGG annotations.
    """
    def process_element(
            self,
            element: ImageObjectDetectionInstance,
            then: ThenFunction[VOCODFormat],
            done: DoneFunction
    ):
        image_info, located_objects = element

        # Create a region for each located object
        if located_objects is not None:
            regions = [Region(region_attributes=RegionAttributes(name=f"{get_object_prefix(located_object)}-{index}",
                                                                 type=get_object_label(located_object),
                                                                 image_quality=ImageQuality()),
                              shape_attributes=get_shape_attributes(located_object))
                       for index, located_object in enumerate(located_objects, 1)]
        else:
            regions = []

        # Create an image info for the image
        image = Image(filename=image_info.filename,
                      size=-1,
                      file_attributes=FileAttributes(caption="", public_domain="no", image_url=""),
                      regions=regions)

        then((image_info, image))
