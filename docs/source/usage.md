### Usage

You can run the segmentation pipeline with:

```python
from holocontour.pipeline.pipeline_runner import pipeline_run
import yaml

with open("path/to/sample_config.yaml") as f:
    config = yaml.safe_load(f)
    

# or define the configuration inline

contour_params = {
    "avg_thresh": 81,
    "max_attempts": 5,
    "increase_avg": 5,
    "min_contour_area": 30,
    "seed_thresh": 45,
    "save_plot": True,
    "median": False,
    "hist_match": True,
    "ref_path": 'src\holocontour\data\001-4923.pgm(406,428)-Z43.50.png'
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