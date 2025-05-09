from skimage.filters import sobel
from skimage.feature import canny
from skimage.morphology import binary_closing, disk
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import remove_small_objects
from skimage.color import rgb2gray
from skimage.util import img_as_float
from scipy.ndimage import binary_fill_holes


def region_refining(binary_image, area_thresh=25):
    # Step 1: remove small objects
    cleaned = remove_small_objects(binary_image.astype(bool), min_size=area_thresh)

    # Step 2: fill holes and clean borders
    filled = binary_fill_holes(cleaned)
    return filled.astype(np.uint8)


def canny_edge(image):
    if image.ndim == 3:
        image = rgb2gray(image)
    edges = canny(image)
    closed = binary_closing(edges, disk(3))
    filled = binary_fill_holes(closed)
    return region_refining(filled)


def sobel_edge(image):
    if image.ndim == 3:
        image = rgb2gray(image)
    edges = sobel(image)
    binary = edges > 0.05
    closed = binary_closing(binary, disk(3))
    filled = binary_fill_holes(closed)
    return region_refining(filled)


def region_methods():
    return {
        'structuredForest': None,  # handled separately via OpenCV
        'cannyEdge': canny_edge,
        'sobelEdge': sobel_edge,
        # Additional methods can be added here
    }
