from skimage.measure import label, regionprops

def reg_props(mask, name_props):
    """
    Extract specified morphological properties from a binary mask.

    Parameters:
    - mask: 2D binary numpy array
    - name_props: list of property names to extract

    Returns:
    - list of dicts, each containing the selected properties for one region
    """
    labeled_mask = label(mask)
    all_props = regionprops(labeled_mask)

    results = []
    for region in all_props:
        props = {name: getattr(region, name, None) for name in name_props}
        results.append(props)
    return results
