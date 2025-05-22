from morphocut import Node, Output, ReturnOutputs
from contour.holo_contour import holo_contour

@ReturnOutputs
class HoloContourNode(Node):
    mask = Output("mask")
    plot = Output("plot")
    outputs = (mask, plot)

    def __init__(self, img, contour_params):
        super().__init__()
        self.img = img
        self.contour_params = contour_params

    def transform(self, img):
        return holo_contour(img, **self.contour_params)
