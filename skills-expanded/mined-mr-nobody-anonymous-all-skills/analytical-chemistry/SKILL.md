---
name: analytical-chemistry
description: "Qualitative and quantitative analysis, calibration methods, error analysis, titrimetry, gravimetry, and instrumental methods"
category: chemistry
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/chemistry/analytical-chemistry/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Analytical Chemistry

## Scope
Analytical chemistry provides qualitative and quantitative identification of chemical constituents, developing rigorous measurement methods, calibration curves, and statistical uncertainty evaluations.

## Measurement Foundations & Validation

### 1. Statistical Treatment of Analytical Data
- **Sample Mean & Standard Deviation**:
  $$\bar{x} = \frac{1}{N}\sum_{i=1}^N x_i, \quad s = \sqrt{\frac{\sum_{i=1}^N (x_i - \bar{x})^2}{N - 1}}$$
- **Confidence Interval**: $\mu = \bar{x} \pm \frac{t \cdot s}{\sqrt{N}}$ (Student's $t$).
- **Calibration Curves & Linear Regression**:
  - Signal $y = m x + b$.
  - Sensitivity = Slope $m$.
  - Limit of Detection (LOD): $\text{LOD} = \frac{3.3 s_{\text{blank}}}{m}$.
  - Limit of Quantitation (LOQ): $\text{LOQ} = \frac{10 s_{\text{blank}}}{m}$.

### 2. Method Validation Protocols (ICH Q2(R1))
- **Specificity**: Ability to assess analyte unequivocally in the presence of expected components (matrix).
- **Linearity**: Evaluated across range $\ge 5$ concentrations, coefficient of determination $R^2 \ge 0.995$.
- **Precision**: Repeatability (intra-day) and intermediate precision (inter-day), expressed as $\%\text{RSD} < 2\%$.
- **Accuracy / Recovery**: Recovery range typically $98.0\% - 102.0\%$.

## Tools & Standards
- **Standards**: ISO/IEC 17025 (Testing and calibration laboratories), ICH Q2(R1), USP <621> Chromatography.
- **Software**: ChemStation, Chromeleon, Empower, OriginLab, R / Python (`scipy.stats`).
- **Canonical References**: Skoog, West, Holler & Crouch — *Fundamentals of Analytical Chemistry*; Harris — *Quantitative Chemical Analysis*.
