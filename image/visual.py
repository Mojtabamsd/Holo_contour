import matplotlib.pyplot as plt


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

