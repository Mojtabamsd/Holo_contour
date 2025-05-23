You can run the segmentation pipeline with:

```python
from holocontour.pipeline.pipeline_runner import pipeline_run
import yaml

with open("path/to/sample_config.yaml") as f:
    config = yaml.safe_load(f)

pipeline_run(
    input_folder="path/to/images",
    output_name="output",
    contour_params=config["contour"],
    lat=config["input_metadata"].get("lat"),
    lon=config["input_metadata"].get("lon"),
    date=config["input_metadata"].get("date"),
    ext=config["input_metadata"].get("ext", ".png")
)