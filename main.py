import argparse
import yaml
from pathlib import Path
from holo_contour.pipeline.pipeline_runner import process_to_ecotaxa


def load_yaml_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EcoTaxa processing pipeline.")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    parser.add_argument("--input", type=str, required=True, help="Path to input image folder")
    parser.add_argument("--name", type=str, default=None, help="Output name (default: last folder name)")

    args = parser.parse_args()

    config = load_yaml_config(args.config)
    input_folder = args.input
    output_name = args.name or Path(input_folder).resolve().name

    contour_params = config.get("contour", {})
    metadata = config.get("input_metadata", {})

    process_to_ecotaxa(
        input_folder=input_folder,
        output_name=output_name,
        contour_params=contour_params,
        lat=metadata.get("lat"),
        lon=metadata.get("lon"),
        date=metadata.get("date"),
        ext=metadata.get("ext", ".png")
    )
