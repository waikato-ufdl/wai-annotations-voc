import os

from wai.annotations.core.component.util import (
    SeparateFileWriter,
    SplitSink,
    SplitState,
    ExpectsDirectory,
    RequiresNoSplitFinalisation
)

from .._format import VOCODFormat


class VOCODWriter(
    ExpectsDirectory,
    RequiresNoSplitFinalisation,
    SeparateFileWriter[VOCODFormat],
    SplitSink[VOCODFormat]
):
    """
    Writer of Pascal VOC XML files.
    """
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    def consume_element_for_split(
            self,
            element: VOCODFormat
    ):
        # Unpack the instance
        image_info, xml = element

        # Write the image
        self.write_data_file(image_info, self._split_path)

        # If the image is a negative, skip writing the annotations
        if xml is None:
            return

        # Format the XML filename
        xml_filename = f"{os.path.splitext(image_info.filename)[0]}.xml"

        # Save the XML
        xml.write(os.path.join(self._split_path, xml_filename), "utf-8", short_empty_elements=False)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "output directory to write annotations to (images are placed in same directory)"
