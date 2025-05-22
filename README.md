# 🧠 HoloContour Segmentation Pipeline

This project provides a pipeline for segmenting holographic particle images using a hybrid region-growing and contour refinement method. It integrates with the [MorphoCut](https://github.com/morphocut/morphocut) framework and exports outputs compatible with [EcoTaxa](https://ecotaxa.obs-vlfr.fr/).

---

## 🚀 Features

- Contour-based object detection with:
  - Median filtering
  - Histogram matching (optional)
  - Region growing from intensity minima
- Optional plot saving of initial vs. refined masks
- Compatible with `EcoTaxaWriter`
- YAML-based configuration
- Safe fallback for empty masks

---

## 🖼 Example

The figure below shows an example of the pipeline's segmentation output:
  
![Segmentation Result](examples/sample.jpg)

- **Red dashed**: Initial region estimate
- **Blue solid**: Refined segmentation contour

---

## 📂 Directory Structure

