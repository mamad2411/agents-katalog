---
name: originpro
description: "Automate OriginPro data analysis with Python or LabTalk, configure nonlinear fitting, and inspect peak-analysis workflows."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["originpro", "originlab", "originpro-python", "nlfit-curve-fitting", "peak-analyzer", "labtalk", "scientific-graphing", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# OriginLab OriginPro Scientific Graphing & Analysis AI Skill Guide (Claude)

## Overview & Engine Architecture
OriginLab OriginPro is a scientific data analysis and publication-grade technical graphing platform. The platform features an object-oriented hierarchical **Worksheet / Matrix / Graph architecture**, an advanced **Nonlinear Curve Fitting (NLFit) Levenberg-Marquardt engine**, a **Peak Analyzer (multi-peak Gaussian/Lorentzian/Voigt deconvolution)**, repeatable **Analysis Templates (`.ogwu`)**, and the **`originpro` Python API**. OriginPro supports scripting via **LabTalk (`.ogs`)**, **Origin C**, and external **COM Automation (`Origin.Application`)**. Claude operates as a Principal Scientific Informatics Architect and Data Visualization Engineer, specializing in **`originpro` Python automation**, **NLFit parameter optimization**, **batch spectral peak deconvolution**, and **publication-quality vector graph generation**.

### OriginPro Dataflow Architecture & Python API Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 OriginPro System Architecture               │
│                                                             │
│  Data Organization & Workbook Hierarchy                     │
│  ├── Workbooks (`.ogwu`) & Matrices (Columns: X, Y, yErr, Z)│
│  ├── Graph Windows (`.oggu`) & Custom Graph Templates       │
│  └── Analysis Templates (Recalculate: Auto / Manual Mode)   │
│                                                             │
│  Analytical Engines & Algorithms                            │
│  ├── NLFit (Levenberg-Marquardt Nonlinear Optimization)     │
│  ├── Peak Analyzer (Baseline Correction, Peak Deconvolution)│
│  └── 2D/3D Surface & Contour Interpolation (Thin Plate Splin│
│                                                             │
│  Scripting & Extensibility Layer                            │
│  ├── Embedded `originpro` Python 3.11 Environment           │
│  ├── LabTalk Scripting Engine (`.ogs` Macro Execution)      │
│  └── COM Automation Server (`Origin.Application`)           │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **`originpro` Python Automated Workflows**: Author Python scripts using the official `originpro` library to launch Origin in headless mode, import raw CSV/Excel data into worksheets, execute analytical curve fits, and export vector graphs.
2. **NLFit Nonlinear Curve Fitting Triage**: Resolve fitting divergence and singular Hessian matrices by establishing bounded parameter constraints, custom initialization functions, and Levenberg-Marquardt damping factors.
3. **Automated Peak Analysis & Spectral Deconvolution**: Construct automated spectral analysis routines subtracting polynomial baselines, finding peaks, and deconvolving overlapping Gaussian/Lorentzian peaks.
4. **Analysis Template Automation**: Build reusable `.ogwu` workbook templates with linked calculation trees that update all graphs automatically upon new raw data injection.

---

## Production Python Automation: Headless Gaussian Peak Fitting & Vector Export (`originpro`)

Save this script as `fit_and_export_spectrum.py` (requires `pip install originpro pandas numpy` and OriginPro installed):

```python
"""
OriginPro Python Automation: Gaussian Peak Fitting & Graph Exporter
Loads spectral data, fits a Gaussian peak model via NLFit, generates graph, and exports PDF.
"""

import sys
import numpy as np
import originpro as op

def process_spectral_data():
    print("--- [INITIALIZING ORIGINPRO AUTOMATION PIPELINE] ---")
    
    # 1. Connect to Origin (Headless Mode)
    op.set_show(False)
    print("✅ Connected to OriginPro Backend Server!")

    # 2. Create Workbook and Worksheet
    wbook = op.new_book("w", "Spectroscopy_Analysis")
    wks = wbook[0]
    wks.from_list(0, np.linspace(400, 800, 100).tolist(), lname="Wavelength", units="nm", axis="X")

    # Generate Synthetic Spectral Peak Data
    x = np.linspace(400, 800, 100)
    y_clean = 100.0 * np.exp(-((x - 550.0) / 30.0)**2) + 10.0
    y_noise = y_clean + np.random.normal(0, 2.0, len(x))
    wks.from_list(1, y_noise.tolist(), lname="Intensity", units="a.u.", axis="Y")

    print(f"Populated Worksheet with {len(x)} spectral data points.")

    # 3. Create Scatter Graph
    graph = op.new_graph(template="scatter")
    gl = graph[0]
    plot = gl.add_plot(wks, coly=1, colx=0, type="scatter")
    gl.rescale()

    # 4. Perform Nonlinear Curve Fitting (Gaussian Model)
    print("Executing NLFit Gaussian Optimization...")
    fit = op.NLFit("Gauss")
    fit.set_data(wks, 1, 0)
    fit.fit()

    # Query Fitted Parameters (y0, xc, w, A)
    params = fit.params()
    print("\n--- [NLFIT OPTIMIZATION RESULTS] ---")
    print(f"• Baseline (y0):   {params[0]:.4f}")
    print(f"• Peak Center (xc):{params[1]:.4f} nm")
    print(f"• Peak Width (w):  {params[2]:.4f} nm")
    print(f"• Peak Area (A):   {params[3]:.4f}")
    print(f"• Adjusted R^2:    {fit.adjr2:.5f}")

    # 5. Export Publication-Quality Vector PDF
    output_pdf = "C:/SimulationModels/Fitted_Spectrum.pdf"
    graph.save_fig(output_pdf, width=1200)
    print(f"\n✅ Publication vector graph saved to: {output_pdf}")

    # Close Origin
    op.exit()
    print("OriginPro session closed.")

if __name__ == "__main__":
    process_spectral_data()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **NLFit Divergence: `Singular Hessian Matrix`** | Initial parameter guesses are orders of magnitude off, or fitting function is over-parameterized. | 1. In NLFit dialog, click **Parameter Initialization Code** to define realistic starting guesses.<br>2. Set hard parameter bounds (e.g. `w > 0`, `A > 0`).<br>3. Fix known baseline constants (`y0 = 0`). |
| **Batch Template Plot Columns Misaligned** | New dataset has a different column sequence than the Analysis Template. | In Worksheet, right-click column headers $\rightarrow$ **Set As** $\rightarrow$ ensure column designations (`X`, `Y`, `yErr`) match template specifications. |
| **`originpro.set_show(False)` Throws COM Exception** | OriginPro automation server not registered in Windows registry. | Launch OriginPro once as Administrator or run `Origin.exe /regserver` in an elevated command prompt. |
| **Exported EPS / PDF Fonts Render Distorted** | Non-TrueType font used in axis labels or font subset embedding disabled. | In Graph Export dialog, select **TrueType Fonts Only** (e.g. Arial or Helvetica) and enable **Embed Fonts**. |

---

## Command Line Syntax & LabTalk Batch Invocations

```bash
# 1. Execute LabTalk Script (.ogs) from Command Line
"C:\Program Files\OriginLab\OriginPro 2025\Origin64.exe" -r "C:\Scripts\BatchProcess.ogs"

# 2. Register OriginPro COM Automation Server
"C:\Program Files\OriginLab\OriginPro 2025\Origin64.exe" /regserver
```

### Essential File Locations
- **User Files Directory**: `%USERPROFILE%\Documents\OriginLab\User Files\`
- **Graph Templates**: `...\User Files\Templates\`
- **Application Configuration**: `C:\Program Files\OriginLab\OriginPro 2025\Origin.ini`

---

## Agent Operational Directive
> **MANDATORY**: When configuring automated NLFit curve fitting routines in OriginPro, always establish positive lower bounds on peak width ($w > 0$) and amplitude ($A > 0$) parameters to prevent the Levenberg-Marquardt optimizer from diverging into negative singularity space.
