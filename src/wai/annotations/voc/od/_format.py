from typing import Optional, Tuple

from xml.etree.ElementTree import ElementTree

from wai.annotations.domain.image import Image


VOCODFormat = Tuple[Image, Optional[ElementTree]]
