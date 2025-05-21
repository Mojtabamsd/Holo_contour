import os
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from skimage.draw import polygon, polygon2mask
from skimage.exposure import match_histograms
from particleSizer import generate_mask


def normalize(mask, range_val=255):
    """Normalize an image to a given range."""
    return (range_val * (mask - np.min(mask)) / np.ptp(mask)).astype(np.uint8)


def find_darkest_point(image, mask):
    """Find the darkest pixel within a mask."""
    return np.unravel_index(np.argmin(image[mask]), image.shape)


def region_grow(image, seed, max_iter=20000, tolerance=25):
    """Simple region growing algorithm from a seed."""
    mask = np.zeros_like(image, dtype=bool)
    region_mean = image[seed]
    stack = [seed]
    iter_count = 0

    while stack and iter_count < max_iter:
        x, y = stack.pop()
        if not mask[x, y]:
            mask[x, y] = True
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < image.shape[0] and
                    0 <= ny < image.shape[1] and
                    not mask[nx, ny] and
                    abs(image[nx, ny] - region_mean) < tolerance
                ):
                    stack.append((nx, ny))
        iter_count += 1

    return mask


def apply_histogram_matching(img, ref_path):
    """Match histogram of image to reference."""
    ref = cv2.imread(ref_path, 0)
    matched = match_histograms(img, ref)
    matched = np.clip(matched, img.min(), img.max())
    return matched.astype(img.dtype)


def contour_mask_union(contours, shape):
    """Create a union mask from multiple contours."""
    union_mask = np.zeros(shape, dtype=bool)
    for contour in contours:
        union_mask |= measure.grid_points_in_poly(shape, contour)
    return union_mask


def filter_contours_by_intensity(contours, image, threshold, use_median=False):
    """Filter contours by intensity threshold."""
    filtered = []
    for contour in contours:
        req_mask = polygon2mask(image.shape[:2], contour).astype(bool)
        region_values = image[req_mask]
        stat = np.median(region_values) if use_median else np.mean(region_values)

        # contour_coords = np.array(list(zip(contour[:, 0].astype(int), contour[:, 1].astype(int))))
        # stat = np.mean(image[contour_coords[:, 0], contour_coords[:, 1]])

        if stat <= threshold:
            filtered.append(contour)
    return filtered


def plot_segmentation_result(img_org, initial_contour, refined_contours, title="Final Segmentation Result"):
    """Plot the initial and refined contours on the original image."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(img_org, cmap='gray')

    if initial_contour is not None:
        ax.plot(initial_contour[:, 1], initial_contour[:, 0], '--r', label='Initial')

    for contour in refined_contours:
        ax.plot(contour[:, 1], contour[:, 0], '-b', linewidth=2, label='Refined')

    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    plt.show()


def holo_contour(img_org,
                 avg_thresh=81,
                 min_contour_area=30,
                 seed_thresh=45,
                 plot=False,
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

    if plot:
        plot_segmentation_result(img_org, outer, final_contour)

    return final_mask > 0



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
        mask = holo_contour(
            img,
            avg_thresh=avg_thresh,
            min_contour_area=min_area,
            seed_thresh=seed_thresh,
            plot=True,
            median=use_median,
            hist_match=hist_match,
            ref_path=ref_path
        )

        output_path = output_dir / (file.stem + ".out.png")
        cv2.imwrite(str(output_path), (mask * 255).astype(np.uint8))
        print(f"Saved: {output_path}")
