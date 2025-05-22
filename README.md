# 🧠 HoloContour Segmentation Pipeline

This project provides a pipeline for segmenting holographic particle images using a hybrid region-growing and contour refinement method. It integrates with the [MorphoCut](https://github.com/morphocut/morphocut) framework and exports outputs compatible with [EcoTaxa](https://ecotaxa.obs-vlfr.fr/).

---

## 🚀 Features

- Contour-based object detection with:
  - Intensity filtering
  - Histogram matching (optional)
  - Region growing from intensity minima
- Optional plot saving of initial vs. refined masks
- Compatible with `EcoTaxaWriter`
- YAML-based configuration
- Safe fallback for empty masks

---

## 🖼 Example

The figure below shows an example of the pipeline's segmentation output:
  
<p align="left">
  <img src="examples/sample.jpg" alt="Segmentation Result" width="400"/>
</p>


- **Red dashed**: Initial region estimate
- **Blue solid**: Refined segmentation contour

---

## ⚙️ Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt

python main.py --config configs/sample_config.yaml --input path/to/your/data



---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



