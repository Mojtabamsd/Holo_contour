from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from skimage.draw import polygon2mask
from skimage.exposure import match_histograms
from image.structure_forest import generate_mask
from image.contour import contour_mask_union, filter_contours_by_intensity
from image.visual import plot_segmentation_result
from image.region_growing import region_grow
from image.processing import normalize, apply_histogram_matching, find_darkest_point


def holo_contour(img_org,
                 avg_thresh=81,
                 min_contour_area=30,
                 seed_thresh=45,
                 save_plot=False,
                 median=False,
                 hist_match=False,
                 ref_path=None):

    img = img_org.copy()

    if hist_match and ref_path:
        img = apply_histogram_matching(img_org, ref_path)

    img = cv2.medianBlur(img, 5)
    init_mask = generate_mask(img)

    seed = find_darkest_point(img_org, init_mask > 0)
    seg_mask = region_grow(img, seed)

    contours = measure.find_contours(seg_mask, 0.5)
    filtered_contours = [c for c in contours if len(c) > min_contour_area]

    while True:
        outside = np.where((img < seed_thresh) & ~seg_mask)
        if len(outside[0]) == 0:
            break
        seed = (outside[0][0], outside[1][0])
        new_mask = region_grow(img, seed)
        seg_mask |= new_mask
        new_contours = measure.find_contours(new_mask, 0.5)
        filtered_contours += [c for c in new_contours if len(c) > min_contour_area]

    valid_contours = filter_contours_by_intensity(
        filtered_contours, img_org, avg_thresh, median
    )

    union = contour_mask_union(valid_contours, img_org.shape)
    outer = max(measure.find_contours(init_mask, 0.5), key=len)
    init_mask_poly = polygon2mask(img_org.shape[:2], outer)
    union &= init_mask_poly

    final_mask = np.zeros_like(init_mask, dtype=np.uint8)
    final_contour = []
    for contour in measure.find_contours(union, 0.5):
        if len(contour) > min_contour_area:
            mask = polygon2mask(img_org.shape[:2], contour).astype(np.uint8)
            final_mask += mask
            final_contour.append(contour)

    if save_plot:
        plot = plot_segmentation_result(img_org, outer, final_contour)
    else:
        plot = None

    return final_mask > 0, plot



if __name__ == '__main__':
    root = Path(r'D:\mojmas\files\Projects\Holo_contour\data\data2')
    output_dir = root / 'seg'
    output_dir.mkdir(exist_ok=True)

    use_median = False
    hist_match = False
    ref_path = r'D:\mojmas\files\Projects\Holo_contour\data\data2\001-4923.pgm(406,428)-Z43.50.png'

    avg_thresh = 100 if use_median else 63
    min_area = 30
    seed_thresh = 45

    for file in root.glob('*.png'):
        img = cv2.imread(str(file), 0)
        mask, plot = holo_contour(
            img,
            avg_thresh=avg_thresh,
            min_contour_area=min_area,
            seed_thresh=seed_thresh,
            save_plot=True,
            median=use_median,
            hist_match=hist_match,
            ref_path=ref_path
        )

        output_path = output_dir / (file.stem + ".out.png")
        cv2.imwrite(str(output_path), (mask * 255).astype(np.uint8))
        print(f"Saved: {output_path}")

        output_path_plot = output_dir / (file.stem + ".plot.png")
        cv2.imwrite(str(output_path_plot), plot)
        print(f"Saved: {output_path_plot}")
