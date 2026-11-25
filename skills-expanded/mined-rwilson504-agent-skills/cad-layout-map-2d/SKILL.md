---
name: cad-layout-map-2d
description: 'Render a labeled 2D top-down (or side/front) layout map of a parametric build123d model from its FeatureRegistry, drawing every cavity, hole, cutout, and boss to scale on an outer-box outline with a north/south/east/west compass and color-coded annotations. USE FOR: "show me a layout diagram", "annotated top view", "where are the holes", "draw the layout", "schematic of the box", "diagram the compartments", verifying spatial intent before printing, communicating layout to the user.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","svg","layout","diagram","documentation"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD Layout Map (2D)

> **Prerequisite:** Load `cad-build123d-general` (for `ORIENTATION` and the
> design/test/production scaffold) and `cad-feature-inventory` (for the
> `FeatureRegistry` that this skill reads from). This skill is the visual
> sibling of the text-based feature inventory.

## Purpose

The text feature inventory tells you *what* features exist; the six-view
renders show the *finished mesh*. Neither answers "are these things
positioned where I think they are?" before you commit to a print.

This skill produces a **single, to-scale 2D PNG** showing the outer box
outline plus every registered feature, color-coded by type, with X/Y
coordinates and a compass overlay. It's drawn with `matplotlib`, so it
runs anywhere build123d already runs and renders in seconds.

Use it whenever:

- The user asks where things are spatially.
- You want to confirm a layout change visually without rebuilding the STL.
- You're explaining the model to someone who can't read the script.
- The text inventory is correct but two features look like they might
  collide and you want to *see* the clearance.

## Source of truth

This skill **consumes** the `FeatureRegistry` (`cad-feature-inventory`)
and the `ORIENTATION` map (`cad-build123d-general`). It does not invent
new coordinates — every shape it draws traces back to a registered
feature or to a script constant the layout map imports.

If a feature is on the model but not registered, it won't appear on
the map. That's the point: the map is a contract that says "these are
the features you told the script about."

## How it works

1. Create a sibling script next to your model: `layout_map.py`.
2. Import the model's parameters and helpers (`from your_model import ...`).
3. Read features from the registry. The registry is the single source
   of truth for what the map draws — both *positions* and *dimensions*
   come from each feature's record (`r["position"]`, `r["dimensions"]`).
   Named constants (`OUTER_W`, `OUTER_D`) are imported only for the
   outer-box outline, never for individual feature geometry.
4. Pick a projection plane: top (XY, looking down −Z), front (XZ,
   looking along −Y), or side (YZ, looking along −X).
5. Draw the outer-box outline, then one matplotlib patch per feature.
6. Annotate compass directions from `ORIENTATION` so the labels match
   what the user (and the feature inventory) calls each side.
7. Save to `exports/layout_<view>.png`.

The map is intentionally **not regenerated automatically by the model
script** — keep it as a separate runnable so it doesn't slow down every
rebuild. Run it after meaningful layout changes.

## Reference implementation

Drop this in a new file `layout_map.py` next to your model script.
Replace `your_model` with your actual module name and adjust the
parameter imports.

```python
"""Top-down labeled layout map of <project>.

Reads parameters and FeatureRegistry from <your_model>.py and draws a
to-scale top view PNG annotating every registered feature.
"""

from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from your_model import (
    ORIENTATION,
    OUTER_W, OUTER_D,           # outer-box footprint in the chosen plane
    FEATURES,                   # the FeatureRegistry instance
)

OUT = Path(__file__).parent / "exports" / "layout_top.png"
OUT.parent.mkdir(parents=True, exist_ok=True)

# --- color map by feature type ---
COLOR_BY_TYPE = {
    "open storage cavity":      "#3b6db5",
    "rectangular compartment":  "#3bb56d",
    "round blind hole":         "#cc7a00",
    "rectangular wall cutout":  "#b53b6d",
    "U-shaped wall cutout":     "#3b6db5",
    "rod support boss":         "#888888",
}
DEFAULT_COLOR = "#444444"

def _color(record):
    return COLOR_BY_TYPE.get(record["type"], DEFAULT_COLOR)

# --- plot ---
fig, ax = plt.subplots(figsize=(11, 10))
drawn_count = 0

# Outer box outline
ax.add_patch(patches.Rectangle(
    (-OUTER_W / 2, -OUTER_D / 2), OUTER_W, OUTER_D,
    linewidth=2, edgecolor="black", facecolor="#f4f1ea"))

# Top-face features (cavities, holes, bosses)
for r in FEATURES._records:                       # see "Registry access" below
    if r["face"] != ORIENTATION["top"]:
        continue
    pos = r["position"]; dim = r["dimensions"]
    cx, cy = pos.get("x", 0), pos.get("y", 0)
    color = _color(r)
    if "diameter" in dim:                          # round hole or boss
        ax.add_patch(patches.Circle((cx, cy), dim["diameter"] / 2,
            linewidth=1.2, edgecolor=color, facecolor=color, alpha=0.35))
        ax.annotate(r["name"], (cx, cy), ha="center", va="center", fontsize=7)
        drawn_count += 1
    elif "W" in dim and "D" in dim:                # rectangular cavity / boss
        w, d = dim["W"], dim["D"]
        ax.add_patch(patches.Rectangle(
            (cx - w / 2, cy - d / 2), w, d,
            linewidth=1.5, edgecolor=color, facecolor=color, alpha=0.25))
        ax.annotate(r["name"], (cx, cy), ha="center", va="center",
                    fontsize=8, fontweight="bold")
        drawn_count += 1

# Front/back wall cutouts: drawn as colored bars on the appropriate edge
for r in FEATURES._records:
    if r["face"] not in (ORIENTATION["front"], ORIENTATION["back"]):
        continue
    pos = r["position"]; dim = r["dimensions"]
    edge_y = OUTER_D / 2 if r["face"] == ORIENTATION["front"] else -OUTER_D / 2
    cx = pos.get("x", 0); w = dim.get("W", 10)
    ax.plot([cx - w / 2, cx + w / 2], [edge_y, edge_y],
            color=_color(r), linewidth=6, solid_capstyle="butt")
    ax.annotate(r["name"], (cx, edge_y + (3 if edge_y > 0 else -3)),
                ha="center", va="bottom" if edge_y > 0 else "top",
                fontsize=8, color=_color(r))
    drawn_count += 1

# Left/right wall cutouts: drawn as colored bars on the side edges
for r in FEATURES._records:
    if r["face"] not in (ORIENTATION["left"], ORIENTATION["right"]):
        continue
    pos = r["position"]; dim = r["dimensions"]
    edge_x = OUTER_W / 2 if r["face"] == ORIENTATION["right"] else -OUTER_W / 2
    cy = pos.get("y", 0); h = dim.get("D", dim.get("W", 10))
    ax.plot([edge_x, edge_x], [cy - h / 2, cy + h / 2],
            color=_color(r), linewidth=6, solid_capstyle="butt")
    ax.annotate(r["name"], (edge_x + (3 if edge_x > 0 else -3), cy),
                ha="left" if edge_x > 0 else "right", va="center",
                fontsize=8, color=_color(r))
    drawn_count += 1

if drawn_count == 0:
    print("WARNING: No features found for this view. Check that features "
          "are registered with the correct face (via FEATURES.register(...)) "
          "and that ORIENTATION maps the expected axis names.")

# Compass labels — pulled from ORIENTATION so they always match the inventory
ax.annotate(f"FRONT ({ORIENTATION['front']})", (0, OUTER_D / 2 + 12),
            ha="center", fontsize=11, fontweight="bold")
ax.annotate(f"BACK ({ORIENTATION['back']})", (0, -OUTER_D / 2 - 8),
            ha="center", fontsize=11, fontweight="bold")
ax.annotate(f"LEFT\n({ORIENTATION['left']})",
            (-OUTER_W / 2 - 10, 0), ha="center", va="center",
            fontsize=11, fontweight="bold")
ax.annotate(f"RIGHT\n({ORIENTATION['right']})",
            (OUTER_W / 2 + 10, 0), ha="center", va="center",
            fontsize=11, fontweight="bold")

ax.set_xlim(-OUTER_W / 2 - 25, OUTER_W / 2 + 25)
ax.set_ylim(-OUTER_D / 2 - 20, OUTER_D / 2 + 25)
ax.set_aspect("equal")
# 10 mm grid — mandatory. 3D-print models live at 50–250 mm scale, so
# matplotlib's auto ticks (25/50 mm) are too coarse to read clearances
# off the layout. Always lock both axes to MultipleLocator(10).
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.tick_params(axis="both", labelsize=8)
ax.grid(True, linestyle=":", alpha=0.4)
ax.set_xlabel("X (mm)"); ax.set_ylabel("Y (mm)")
ax.set_title("<Project> — Top View Layout (looking down −Z)")

plt.tight_layout()
plt.savefig(OUT, dpi=150)
print(f"Wrote {OUT}")
```

### Registry access

`FEATURES._records` is the simplest way to iterate, but if you'd
rather not touch a private attribute, add this small accessor to
`FeatureRegistry` once (it's backwards-compatible):

```python
def all(self):
    return list(self._records)
```

Then use `FEATURES.all()` in the layout map.

## Choosing the projection

| View | Axes drawn | When to use |
|------|-----------|-------------|
| **Top (XY)** | X horizontal, Y vertical, looking down −Z | Default. Best for trays, organizers, enclosures with everything reachable from above. |
| **Front (XZ)** | X horizontal, Z vertical, looking along −Y | Walls with cutouts, switch/jack panels, lid features that are seen from the front. |
| **Side (YZ)** | Y horizontal, Z vertical, looking along −X | Profile of stacked compartments, hinge axes, anything where Z layout matters more than X. |

You can have multiple layout scripts (`layout_top.py`, `layout_front.py`)
or one script that takes a `--view` flag. Start with one top view; add
others only when you actually need them.

## Grid spacing

**Lock both axes to a 10 mm major-tick grid** (`MultipleLocator(10)`).
Do NOT rely on matplotlib's auto-tick choice — it picks 25 or 50 mm at
typical 3D-print model sizes (50–250 mm), which is too coarse to read
clearances and wall thicknesses (typically 1.6–3 mm). 10 mm matches
how makers reason about printer-bed-sized parts and gives a usable
ruler against every gridline.

For very small parts (<30 mm overall) or very large parts (>500 mm),
adjust to 5 mm or 25 mm respectively, but the **default is 10 mm**.

## Color & shape conventions

- **Cavities** — translucent fill, solid outline, name in bold center.
- **Round holes / bosses** — translucent circle, short label inside.
- **Wall cutouts** — drawn as a thick colored bar on the edge of the
  outer box where the cut breaks through. Annotate above/below the bar.
- **Inside-bay features** (rod tabs, internal ribs) — small filled
  rectangles in a neutral grey so they don't fight with the cavity
  fills behind them.
- Pick **one color per feature type** (matching the keys in
  `COLOR_BY_TYPE`) and reuse it consistently between the inventory
  color hints (if any) and the map.

## Quick reference

| Symptom on the map | Likely cause | Fix |
|--------------------|--------------|-----|
| Feature missing from map | Not registered with `FEATURES.register(...)` | Add the registration immediately after building the feature. |
| Feature drawn at wrong place | `position` dict in the registry is stale | Recompute position with the same constants the model uses; don't hand-type. |
| Wall cutout drawn on the wrong edge | `face` in registration doesn't match `ORIENTATION` | Confirm which axis is `front`/`back`; the layout script reads from `ORIENTATION` directly. |
| Outer box outline doesn't match real outer dims | Imported wrong constant (e.g. `INNER_W` instead of `OUTER_W`) | Always import the *outer* footprint constants for the box outline. |
| Two features look like they collide | They actually do, OR the map is right and the model is wrong | Check the inventory positions; if they overlap there too, it's a real collision. |

## What this skill DOES NOT do

- It does not measure or query the geometry — it only visualizes what
  the registry says. If the registry is wrong, the map is wrong.
- It does not replace the `cad-build123d-six-view-checks` workflow.
  Six-views inspect the *mesh*; this map inspects the *intent*.
- It does not auto-detect feature types. The color map is a hand-tuned
  lookup keyed on the `type` strings you used in `FEATURES.register(...)`.
  Keep the type strings consistent across the project.

## See Also

- `cad-feature-inventory` — text-based per-face inventory (data source).
- `cad-build123d-six-view-checks` — rendered orthographic photos of the
  built mesh (visual sanity check on the *output*, not the *intent*).
- Working example: [`cad/soldering-station-organizer/layout_map.py`](../../cad/soldering-station-organizer/layout_map.py)
  produces [`exports/layout_top.png`](../../cad/soldering-station-organizer/exports/layout_top.png).
