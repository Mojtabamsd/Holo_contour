You can run the segmentation pipeline with:

```python
from holocontour.pipeline.pipeline_runner import pipeline_run
import yaml

with open("path/to/sample_config.yaml") as f:
    config = yaml.safe_load(f)
    

# or define the configuration inline

contour_params = {
    "avg_thresh": 63,
    "min_contour_area": 30,
    "seed_thresh": 45,
    "save_plot": True,
    "median": False,
    "hist_match": False,
    "ref_path": None
}

metadata = {
    "lat": None,
    "lon": None,
    "date": None,
    "ext": ".png"
}



pipeline_run(
    input_folder="path/to/images",
    output_name="output",
    contour_params=config["contour"],
    lat=config["input_metadata"].get("lat"),
    lon=config["input_metadata"].get("lon"),
    date=config["input_metadata"].get("date"),
    ext=config["input_metadata"].get("ext", ".png")
)