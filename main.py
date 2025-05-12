from particleSizer import particle_sizer


particle_sizer(
    code_dir='.',  # not strictly used in Python version
    data_dir=r'D:\mojmas\files\Projects\Holo_contour\data\data1',
    im_format='.png',
    save_dir=r'D:\mojmas\files\Projects\Holo_contour',
    method_key='structuredForest',  # or 'structuredForest', 'cannyEdge', 'sobelEdge'
    model_path=r'D:\mojmas\files\Projects\Holo_contour\model.yml',
    # name_props=['Area', 'BoundingBox', 'ConvexArea', 'MajorAxisLength', 'MinorAxisLength'],
    name_props=['Area', 'BoundingBox'],
    use_convex_hull=True
)