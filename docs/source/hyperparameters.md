### Hyperparameters

#### `img_org`
- **Type**: `numpy.ndarray`
- **Description**:  
  The original grayscale image of the hologram to process.  
  This is the input array where segmentation will be performed.

#### `avg_thresh`
- **Type**: `int`
- **Default**: `81`
- **Description**:  
  Average (or median) intensity threshold.  
  Contours with mean (or median) pixel intensity above this threshold will be discarded.  
  Use this to filter out bright noise or artifacts.

#### `max_attempts`
- **Type**: `int`
- **Default**: `5`
- **Description**:  
  The maximum number of times to retry segmentation when no valid mask is found.  
  Each retry increases `avg_thresh` to make the filter progressively less strict.

#### `increase_avg`
- **Type**: `int`
- **Default**: `5`
- **Description**:  
  The amount to increment `avg_thresh` after each failed attempt.

#### `min_contour_area`
- **Type**: `int`
- **Default**: `30`
- **Description**:  
  Minimum contour length (number of points) to keep.  
  Contours smaller than this are discarded.  
  This helps eliminate tiny irrelevant regions.

#### `seed_thresh`
- **Type**: `int`
- **Default**: `45`
- **Description**:  
  Pixel intensity threshold for detecting additional seeds in the region-growing process.  
  Any pixel below this value outside the already segmented region becomes a seed for expanding the mask.

#### `save_plot`
- **Type**: `bool`
- **Default**: `False`
- **Description**:  
  If `True`, the function will return a visualization image (as a NumPy array) showing contours overlaid on the original image.

#### `median`
- **Type**: `bool`
- **Default**: `False`
- **Description**:  
  If `True`, the median pixel intensity is used instead of the mean for thresholding contours (`avg_thresh`).  
  This can be more robust to outliers.

#### `hist_match`
- **Type**: `bool`
- **Default**: `False`
- **Description**:  
  If `True`, histogram matching is applied to the input image to align its intensity distribution to a reference image (`ref_path`).

#### `ref_path`
- **Type**: `str` or `None`
- **Default**: `None`
- **Description**:  
  Path to a reference image used for histogram matching (only relevant if `hist_match=True`).

---

### Returned Values

- **`final_mask`**:  
  A binary mask (`boolean array`) indicating detected regions.

- **`plot`**:  
  Visualization of the segmentation (or `None` if `save_plot=False`).