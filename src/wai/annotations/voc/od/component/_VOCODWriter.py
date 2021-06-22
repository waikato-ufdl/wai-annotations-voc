from typing import Dict

from wai.annotations.core.component.util import JSONFileWriter, SplitSink, SplitState, ExpectsFile

from .._format import VOCODFormat


class VOCODWriter(
    ExpectsFile,
    JSONFileWriter[VOCODFormat],
    SplitSink[VOCODFormat]
):
    """
    Writer of VGG-format JSON files.
    """
    _split_image = SplitState(lambda self: {})
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    def consume_element_for_split(
            self,
            element: VOCODFormat
    ):
        # Unpack the instance
        image_info, image = element

        # Write the image
        self.write_data_file(image_info, self._split_path)

        # If the image is a negative, skip writing it
        if len(image.regions) == 0:
            return

        self._split_image[f"{image.filename}-1"] = image

    def finish_split(self):
        pass

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "output file to write annotations to (images are placed in same directory)"
