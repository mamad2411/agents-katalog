---
name: cad-build123d-six-view-checks
description: 'Generate front/back/left/right/top/bottom verification images for build123d models after each rebuild. USE FOR: six-side screenshots, orthographic checks, verify walls/faces, compare +Y vs -Y, regression snapshots, visual QA before print.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","verification","orthographic","rendering","qa"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# Build123d Six-View Checks

> **Prerequisite:** Load `cad-build123d-general` first for orientation-map and export-mode conventions.

## Purpose
Create a repeatable visual QA step that exports six labeled views (front, back, left, right, top, bottom) after geometry rebuilds. This helps catch wrong-face edits, mirrored features, hidden split seams, and accidental wall penetrations before printing.

## Source of Truth
This skill is the source of truth for six-view verification workflow in CAD projects in this repo.

- Orientation labels use the model's global axes: `front=+Y`, `back=-Y`, `left=-X`, `right=+X`, `top=+Z`, `bottom=-Z`.
- File naming convention: `<part-name>_<view>.png`.
- Output folder convention: `<project>/exports/views/`.

## Preferred Tools

### 1) OCP CAD Viewer (interactive, best first choice)
Use when the user wants quick manual confirmation in VS Code.

- VS Code extension: OCP CAD Viewer
- Python package: `ocp-vscode`
- Strength: fastest way to inspect the exact face orientation with selection and measurements.

Workflow:
1. Rebuild the model script.
2. Open in OCP CAD Viewer.
3. Capture six snapshots using fixed camera directions.
4. Save to `exports/views/` with the naming convention above.

### 2) Headless snapshot pipeline (automated CI-style checks)
Use when the user wants reproducible images generated on every run.

Recommended Python stack:
- `trimesh`
- `pyvista`
- `pillow`

Install:
```powershell
pip install trimesh pyvista pillow
```

## Integration Pattern
Add a verification switch in CAD scripts so six views can be enabled without affecting production exports.

```python
VERIFY_VIEWS = True
VIEWS_DIR = EXPORT_DIR / "views"
PART_BASENAME = "my_part"
```

Run order at end of script:
1. Build part
2. Export STL/STEP
3. If `VERIFY_VIEWS` is true, generate six-view PNGs
4. Print generated file paths

## Reference Camera Map

| View | Look Direction | Up Direction |
|------|----------------|--------------|
| front | +Y -> origin | +Z |
| back | -Y -> origin | +Z |
| right | +X -> origin | +Z |
| left | -X -> origin | +Z |
| top | +Z -> origin | +Y |
| bottom | -Z -> origin | +Y |

Use orthographic projection for QA images. Perspective can hide alignment issues.

## Quality Checklist
For each generated view, verify:

1. Outer silhouette matches expected dimensions.
2. No unintended wall penetrations.
3. No mirrored features across +Y/-Y or +X/-X.
4. Split seams are understood (boolean partition lines vs true recesses).
5. Labeling is consistent with orientation map.

## Quick Triage: "Is this a real dent or a split seam?"

1. Compare opposite faces (`front` vs `back`, `left` vs `right`).
2. If the line appears only where booleans intersect but no face-depth shift exists, it is likely a coplanar split seam.
3. Confirm with geometry queries (face normal and center position) before changing dimensions.
4. If needed, run a cleanup pass (for example, `part.clean()` where safe).

## Minimal Verification Helper (drop-in)
Use this helper pattern when a project asks for repeatable image checks.

```python
from pathlib import Path

def report_expected_views(base_name: str, out_dir: Path) -> None:
    names = ["front", "back", "left", "right", "top", "bottom"]
    out_dir.mkdir(parents=True, exist_ok=True)
    for n in names:
        print(out_dir / f"{base_name}_{n}.png")
```

This helper does not render images by itself; pair it with your selected viewer/render backend.

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Back wall looks indented in one viewer only | Shading/split seam artifact | Verify with opposite face + geometry query, then apply cleanup pass if needed |
| Front and back labels appear swapped | Camera direction map inverted | Re-check `front=+Y`, `back=-Y` mapping |
| Six files missing after build | Verification switch disabled | Set `VERIFY_VIEWS=True` |
| Images generated but not comparable | Perspective camera or random zoom | Lock orthographic projection and fixed camera map |
| User says "wall is missing" but math says it's there | Wall is geometrically present but thin (≤5 mm) — invisible as a sliver in iso views | Confirm with the head-on close-up of that face (`_<face>-close.png` shows a solid silhouette = wall exists). If user still wants more visible material, bump thickness to ≥8–10 mm. Don't rely only on top-down or head-on views — iso views are the user's primary visual check. |

## See Also

- Related skill: `cad-build123d-general` (orientation map, export workflow)
- Related skill: `cad-build123d-tools` (viewer and tooling catalog)
- **Sister skill: `cad-render-images`** (publication renders \u2014 hero,
  exploded, cutaway, turntable). This skill = QA snapshots; that skill =
  documentation/marketing renders.
- OCP CAD Viewer: https://github.com/bernhard-42/vscode-ocp-cad-viewer
