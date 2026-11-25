---
name: highway-engineering
description: "Horizontal and vertical alignment, sight distance (SSD, PSD), super-elevation, and earthwork mass diagrams"
category: civil-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/civil-engineering/highway-engineering/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Highway Engineering

## Scope
Highway engineering details the geometric layout, earthwork cut-and-fill balance, drainage, and cross-sectional design of roadway corridors.

## Geometric Formulations
- **Stopping Sight Distance (SSD)**:
  $$\text{SSD} = 1.47 V t_r + \frac{V^2}{30(a/g \pm G)}$$
  where $V$ is speed (mph), $t_r$ perception-reaction time ($2.5\text{ s}$), $G$ roadway grade.
- **Horizontal Curve Radius**: $R_{\min} = \frac{V^2}{15(0.01 e_{\max} + f_{\max})}$.
- **Vertical Curve (Crest/Sag)**: Parabolic elevation $y = y_0 + g_1 x + \frac{g_2 - g_1}{2L} x^2$, with design parameter $K = L / |A|$.

## Tools & Standards
- **Software**: Autodesk Civil 3D, Bentley OpenRoads Designer.
- **Standards**: AASHTO Geometric Design Guidelines.
