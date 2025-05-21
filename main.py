import os
from morphocut.core import Pipeline, Call
from morphocut.file import Find, Glob
from morphocut.image import ImageProperties, ImageReader, FindRegions
from morphocut.stream import Progress
from morphocut.str import Format
from morphocut.contrib.ecotaxa import EcotaxaWriter
from morphocut.contrib.zooprocess import CalculateZooProcessFeatures
from contour.morpho_custom import HoloContourNode


def process_to_ecotaxa(
    input_folder,
    output_name,
    contour_params,
    lat=None,
    lon=None,
    date=None,
    ext=".png"
):
    """
    Process images in a folder using MorphoCut and export to EcoTaxa format.

    Args:
        input_folder (str): Path to folder containing raw images.
        output_name (str): Name for the EcoTaxa output zip file.
        contour_params (dict): Parameters to pass to HoloContourNode.
        lat, lon, date (optional): Metadata for EcoTaxa.
        ext (str): File extension filter (default: ".png").
    """
    # output_dir = os.path.join(os.path.dirname(input_folder), "output")
    output_dir = os.path.join(os.path.join(input_folder), "output")
    os.makedirs(output_dir, exist_ok=True)

    print(f"Selected folder: {input_folder}")
    print(f"Files will be extracted to: {output_dir}")

    with Pipeline() as pipeline:
        fn = Find(input_folder, [ext])
        path = Glob(fn)
        basename = Call(lambda x: os.path.splitext(os.path.basename(x))[0], path)

        metadata = {
            "id": Format("{object_id}", object_id=basename),
            "lat": lat,
            "lon": lon,
            "date": date,
        }

        img = ImageReader(path)
        img_gray = img[:, :, 0]
        # img_gray = img

        mask, plot = HoloContourNode(img_gray, contour_params=contour_params)

        region_props = ImageProperties(mask, img_gray)

        # to handle multiple objects
        # region_props = FindRegions(mask, img_gray, min_area=30)

        object_meta = CalculateZooProcessFeatures(region_props, metadata)

        output_zip = os.path.join(output_dir, f"EcoTaxa_{output_name}.zip")
        EcotaxaWriter(
            output_zip,
            [(Format("{object_id}.jpg", object_id=basename), img_gray)],
            object_meta=object_meta,
        )

        output_zip_mask = os.path.join(output_dir, f"EcoTaxa_{output_name}_mask.zip")
        EcotaxaWriter(
            output_zip_mask,
            [(Format("{object_id}.jpg", object_id=basename), mask)],
            object_meta=object_meta,
        )

        if holo_params["save_plot"]:
            output_zip_plot = os.path.join(output_dir, f"EcoTaxa_{output_name}_plot.zip")
            EcotaxaWriter(
                output_zip_plot,
                [(Format("{object_id}.jpg", object_id=basename), plot)],
                object_meta=object_meta,
            )

        Progress(fn)

    pipeline.run()


if __name__ == '__main__':
    holo_params = {
        "avg_thresh": 63,
        "min_contour_area": 30,
        "seed_thresh": 45,
        "save_plot": False,
        "median": False,
        "hist_match": False,
        "ref_path": None,
    }

    process_to_ecotaxa(
        input_folder=r'D:\mojmas\files\Projects\Holo_contour\data\data2',
        output_name='sample',
        contour_params=holo_params
    )
