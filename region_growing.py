from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from particleSizer import generate_mask
from skimage.exposure import match_histograms
from skimage.draw import polygon
import os

def normalize(mask, range=255):
    normalized = (range * (mask - np.min(mask)) / np.ptp(mask)).astype(int).astype('uint8')
    return normalized


def find_min_point_inside(image, mask):
    min_point = np.unravel_index(np.argmin(image[mask]), image.shape)
    return min_point


def region_growing(image, seed, max_iterations=20000):
    mask = np.zeros_like(image, dtype=np.bool)
    region_mean = image[seed]
    tolerance = 25  # Adjust this threshold based on your image characteristics
    iterations = 0

    stack = [seed]

    while stack and iterations < max_iterations:
        current = stack.pop()

        if not mask[current]:
            mask[current] = True

            # Get neighboring pixels
            neighbors = [
                (current[0] + 1, current[1]),
                (current[0] - 1, current[1]),
                (current[0], current[1] + 1),
                (current[0], current[1] - 1),
            ]

            for neighbor in neighbors:
                # Check if the neighbor is within the image boundaries
                if (
                        0 <= neighbor[0] < image.shape[0]
                        and 0 <= neighbor[1] < image.shape[1]
                        and not mask[neighbor]
                        and np.abs(image[neighbor] - region_mean) < tolerance
                ):
                    stack.append(neighbor)

        iterations += 1

    return mask


def contour_to_mask(img, contour):
    r = contour[:, 0]
    c = contour[:, 1]
    mask = np.zeros_like(img, dtype=np.uint8)
    rr, cc = polygon(r, c, shape=mask.shape)
    mask[rr, cc] = 1
    return mask


def holo_contour(img_org, avg_thresh=81, min_contour_area=30, seed_thresh=45, plot=False):
    
    img = img_org
    # # histogram matching to reference
    # ref_path = r'D:\mojmas\files\Projects\Holo_contour\data\data2\001-1524.pgm(1,312)-Z35.00.png'
    ref_path = r'D:\mojmas\files\Projects\Holo_contour\data\data2\001-4923.pgm(406,428)-Z43.50.png'
    ref = cv2.imread(ref_path, 0)
    matched = match_histograms(img_org, ref)
    matched = np.clip(matched, img_org.min(), img_org.max())
    matched = matched.astype(img_org.dtype)
    # img = matched  # for dataset 1 only

    img_blur = cv2.medianBlur(img, 5)
    img = img_blur

    # gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # # Get the initial seed point from the user
    # fig, ax = plt.subplots(figsize=(8, 8))
    # ax.imshow(gray_image, cmap='gray')
    # ax.set_title('Click to provide a seed point for region growing')

    # seed_point = plt.ginput(1, show_clicks=True)[0]
    # seed_point = (int(seed_point[1]), int(seed_point[0]))

    init_mask = generate_mask(img)

    # seed_point = find_min_point_inside(gray_image, gray_image > 0)
    seed_point = find_min_point_inside(img_org, init_mask > 0)
    seed_point = (seed_point[0], seed_point[1])

    segmentation_mask = region_growing(img, seed_point)

    contours = measure.find_contours(segmentation_mask, 0.5)

    # Filter out small contours based on area
    filtered_contours = [contour for contour in contours if contour.shape[0] > min_contour_area]

    # # Display the original image and the segmented image with the filtered contour
    # fig, ax = plt.subplots(figsize=(8, 8))
    # ax.imshow(gray_image, cmap='gray')
    #
    # for contour in filtered_contours:
    #     ax.plot(contour[:, 1], contour[:, 0], '-r', linewidth=2)
    #
    # ax.set_title('Region Growing Contour Segmentation (Filtered)')
    # plt.show()

    while True:
        outside_points = np.where((img < seed_thresh) & ~segmentation_mask)

        if len(outside_points[0]) == 0:
            break  # No more points below the threshold outside detected contours

        seed_point = (outside_points[0][0], outside_points[1][0])

        new_segmentation_mask = region_growing(img, seed_point)

        segmentation_mask |= new_segmentation_mask

        new_contours = measure.find_contours(new_segmentation_mask, 0.5)

        new_filtered_contours = [contour for contour in new_contours if contour.shape[0] > min_contour_area]

        # fig, ax = plt.subplots(figsize=(8, 8))
        # ax.imshow(gray_image, cmap='gray')
        #
        # for contour in filtered_contours + new_filtered_contours:
        #     ax.plot(contour[:, 1], contour[:, 0], '-r', linewidth=2)
        #
        # ax.set_title('Region Growing Contour Segmentation (Filtered + Iterative)')
        # plt.show()
        filtered_contours += new_filtered_contours

    if plot:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(img_org, cmap='gray')

    # Remove contours based on average mean intensity threshold
    filtered_merged_contours = []

    for filtered_contour in filtered_contours:
        req_mask = contour_to_mask(img, filtered_contour)

        if median:
            region_pixels = img_org[req_mask > 0]
            region_median = np.median(region_pixels)
            region_mean = region_median
        else:
            # region_mean = np.mean(img_org*req_mask)
            contour_coords = np.array(
                list(zip(filtered_contour[:, 0].astype(int), filtered_contour[:, 1].astype(int))))
            region_mean = np.mean(img[contour_coords[:, 0], contour_coords[:, 1]])

        if region_mean <= avg_thresh:
            filtered_merged_contours.append(filtered_contour)

    union_area = np.zeros_like(segmentation_mask, dtype=np.bool)
    for contour in filtered_merged_contours:
        union_area |= measure.grid_points_in_poly(segmentation_mask.shape, contour)

    # remove areas outside of mask
    contours = measure.find_contours(init_mask, 0.5)
    contour = max(contours, key=len)
    r = contour[:, 0]
    c = contour[:, 1]
    mask = np.zeros_like(init_mask, dtype=np.uint8)
    rr, cc = polygon(r, c, shape=mask.shape)
    mask[rr, cc] = 1
    union_area = union_area * mask
    # union_area = mask
    if plot:
        ax.plot(contour[:, 1], contour[:, 0], '--r', label='Initial')
        # plt.show()

    merged_contours = measure.find_contours(union_area, 0.5)
    # contours = measure.find_contours(segmentation_mask, 0.5)
    merged_contours = [contour for contour in merged_contours if contour.shape[0] > min_contour_area]

    final_mask = np.zeros_like(init_mask, dtype=np.uint8)
    for merged_contour in merged_contours:
        if plot:
            ax.plot(merged_contour[:, 1], merged_contour[:, 0], '-b', linewidth=2, label='Refined')
        final_mask += contour_to_mask(img, merged_contour)

    if plot:
        ax.set_title('Final Segmentation Result')
        ax.legend()
        plt.tight_layout()
        # plt.savefig(output_path)
        plt.show()
 
    return final_mask




# root = r'D:\mojmas\files\Projects\Holo_contour\data\data1'
root = r'D:\mojmas\files\Projects\Holo_contour\data\data2'
# root = r'D:\mojmas\files\Projects\Holo_contour\data\data3'
median = False

if median:
    avg_thresh = 100    # average median intensity threshold data1
    # avg_thresh = 67    # average median intensity threshold data2
else:
    # avg_thresh = 85    # average mean intensity threshold data1
    avg_thresh = 81    # average mean intensity threshold data2


min_contour_area = 30           # small contours minimum area
seed_thresh = 45      # for second contour it searches values below this thresh


for file in Path(root).glob('*.png'):
    input_path = str(file)
    output_path = str(file.parent / 'seg' / (file.stem + ".out.png"))
    img_org = cv2.imread(input_path, 0)
    
    mask = holo_contour(img_org, avg_thresh, min_contour_area, seed_thresh)

    mask = (mask * 255)
    cv2.imwrite(output_path, mask)
    print(f"  Saved refined mask: {output_path}")

