from morphocut import Node, Output, ReturnOutputs
from region_growing import holo_contour


@ReturnOutputs
class HoloContourNode(Node):
    mask = Output("mask")
    outputs = (mask,)

    def __init__(self, img, contour_params):
        super().__init__()
        self.img = img
        self.contour_params = contour_params

    def transform(self, img):
        processed_data = holo_contour(img, **self.contour_params)
        return processed_data









