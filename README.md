<div style="display: flex; align-items: center; gap: 20px;">
  <img src="assets/logo.png" alt="HoloContour Logo" width="100"/>
  <div>
    <p style="font-size: 14px; margin: 0;">A minimalist tool for holographic plankton image segmentation.</p>
  </div>
</div>




# HoloContour

This repository provides a pipeline for segmenting holographic particle images using a hybrid region-growing and contour refinement method. It integrates with the [MorphoCut](https://github.com/morphocut/morphocut) framework and exports outputs compatible with [EcoTaxa](https://ecotaxa.obs-vlfr.fr/).

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
  <img src="assets/sample.jpg" alt="Segmentation Result" width="400"/>
</p>


- **Red dashed**: Initial region estimate
- **Blue solid**: Refined segmentation contour

---
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

