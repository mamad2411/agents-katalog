---
name: cad-feature-inventory
description: 'Generate a per-face inventory of a parametric build123d model: for each axis face (top/bottom/left/right/front/back) lists the features (holes, cutouts, debossed text, protrusions) sitting on that face with their positions and dimensions. USE FOR: "what is on the top face", "list features by side", "show me a feature map", "describe the model", debugging "which wall has the notch", documenting a part for review, AI ↔ user direction conversations.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","introspection","documentation","features","cad"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD Feature Inventory

> **Prerequisite:** Load `cad-build123d-general` first. This skill assumes
> you already have an `EXPORT_MODE` flag and an `ORIENTATION` map (skill
> section 8a). The inventory uses the same map so axis labels and friendly
> direction names stay consistent.

## Purpose

Make a parametric model **self-describing**. As you add features
(holes, notches, debossed text, bosses, slots, channels), you tag each
one with the face it lives on plus its key dimensions and position. At
export time, the script prints a per-face summary like:

```
Feature Inventory (model dimensions: 165.50 × 111.47 × 38.40 mm)

  +X  Front  (notch end)        165.50 × ... face area
    ◽ Finger pull notch
        type:        rectangular cutout
        position:    Y=0.00, Z=26.40 (centered on wall, flush with rim)
        dimensions:  W=38.19  D=24.00  through the wall (2.75)

  -Z  Bottom  (build plate)
    ◽ Debossed text "BUY"
        type:        recessed text
        position:    centered, Z=floor surface (Z=2.75)
        dimensions:  cap height 18.00, depth 1.20
    ◽ Debossed text "MORE"
        ...
```

This solves three recurring frustrations:

1. **AI ↔ user direction conversations.** When the user says "move the
   notch on the front wall", both you and the user can confirm against
   the printed inventory which features are actually on the +X face.
2. **Model review.** Before you print, scan the inventory once instead
   of re-reading the script.
3. **Refactoring.** When you change a parameter, the new dimensions
   show up in the inventory so you spot off-by-one errors immediately.

## How it works

A small `FeatureRegistry` collects feature records as you build.
Each `register(...)` call records:

- `name` — short label ("Finger pull notch", "BUY text")
- `face` — one of `+X -X +Y -Y +Z -Z` (or a friendly name from the
  `ORIENTATION` map; both work)
- `type` — free-form ("rectangular cutout", "round hole", "boss",
  "recessed text", "slot")
- `position` — dict with as many of `x y z` as are meaningful (mm)
- `dimensions` — dict of named dimensions (mm); the keys become the
  printed labels. Use whatever naming makes sense for the feature
  (e.g. `{"W": 38.19, "D": 24.0}`, `{"diameter": 4.0, "depth": 8.0}`,
  `{"cap_height": 18.0, "depth": 1.2}`)
- `note` *(optional)* — one short clarifying sentence

The model's bounding box is also captured automatically and printed
at the top of the inventory.

## Reference implementation

Drop this in your script next to the helpers from
`cad-build123d-general` section 8a. It has zero dependencies beyond
the `ORIENTATION` map already required by that skill.

```python
# ---------------------------------------------------------------------------
# Feature inventory (cad-feature-inventory skill)
# ---------------------------------------------------------------------------

class FeatureRegistry:
    """Collects per-face feature records and prints a human-readable
    inventory at export time."""

    # Friendly name -> axis label, derived from ORIENTATION at print time.
    AXIS_ORDER = ("+X", "-X", "+Y", "-Y", "+Z", "-Z")

    def __init__(self):
        self._records = []  # list of dicts

    def register(self, name, face, *, type, position=None,
                 dimensions=None, note=None):
        # Allow friendly names ("front") or axis labels ("+X").
        face = ORIENTATION.get(face.lower(), face) if isinstance(face, str) else face
        if face not in self.AXIS_ORDER:
            raise ValueError(
                f"Unknown face {face!r}. Expected one of "
                f"{self.AXIS_ORDER} or a key in ORIENTATION."
            )
        self._records.append({
            "name": name,
            "face": face,
            "type": type,
            "position": position or {},
            "dimensions": dimensions or {},
            "note": note,
        })

    def print(self, part, *, header="Feature Inventory"):
        # Reverse the ORIENTATION map for friendly display names.
        face_to_friendly = {v: k.capitalize() for k, v in ORIENTATION.items()}
        # Warn if ORIENTATION is missing any of the six axes — otherwise
        # face_to_friendly lookups return "" and the inventory prints
        # confusing unlabeled rows.
        missing = [a for a in self.AXIS_ORDER if a not in face_to_friendly]
        if missing:
            print(f"  WARNING: ORIENTATION map is missing axes {missing}. "
                  f"Friendly direction names for those faces will be blank.")
        bb = part.bounding_box()
        size_x = bb.max.X - bb.min.X
        size_y = bb.max.Y - bb.min.Y
        size_z = bb.max.Z - bb.min.Z
        print(f"\n{header}")
        # Pair each axis with its friendly name from ORIENTATION (Length/
        # Width/Height-ish, but driven by the project-specific map).
        x_label = (face_to_friendly.get("+X", ""),
                   face_to_friendly.get("-X", ""))
        y_label = (face_to_friendly.get("+Y", ""),
                   face_to_friendly.get("-Y", ""))
        z_label = (face_to_friendly.get("+Z", ""),
                   face_to_friendly.get("-Z", ""))
        print(f"  Principal object size (axis ref cube excluded):")
        print(f"    X  {size_x:7.2f} mm  ({x_label[1]} ↔ {x_label[0]})")
        print(f"    Y  {size_y:7.2f} mm  ({y_label[1]} ↔ {y_label[0]})")
        print(f"    Z  {size_z:7.2f} mm  ({z_label[1]} ↔ {z_label[0]})")
        try:
            print(f"    volume: {part.volume / 1000:.2f} cm³")
        except Exception:
            pass

        for face in self.AXIS_ORDER:
            on_face = [r for r in self._records if r["face"] == face]
            if not on_face:
                continue
            friendly = face_to_friendly.get(face, "")
            label = f"  {face}  {friendly}".rstrip()
            print(f"\n{label}")
            for r in on_face:
                print(f"    \u25fd {r['name']}")
                print(f"        type:        {r['type']}")
                if r["position"]:
                    pos = "  ".join(f"{k}={v:.2f}"
                                    for k, v in r["position"].items())
                    print(f"        position:    {pos}")
                if r["dimensions"]:
                    dims = "  ".join(f"{k}={v:.2f}"
                                     for k, v in r["dimensions"].items())
                    print(f"        dimensions:  {dims}")
                if r["note"]:
                    print(f"        note:        {r['note']}")


FEATURES = FeatureRegistry()
```

## Usage pattern

Register each feature *immediately after* you build it, while the
constants are right there in your code. Don't try to retrofit a giant
registry block at the end of the script — the constants will be far
away and you'll get drift.

```python
# Notch on the +X short wall
notch_z_center = OUTER_H - NOTCH_D / 2
with Locations((OUTER_L / 2, 0, notch_z_center)):
    Box(WALL * 3, NOTCH_W, NOTCH_D, mode=Mode.SUBTRACT)
FEATURES.register(
    "Finger pull notch",
    face="front",
    type="rectangular cutout",
    position={"y": 0.0, "z": notch_z_center},
    dimensions={"W": NOTCH_W, "D": NOTCH_D, "through": WALL},
    note="centered on wall, flush with rim",
)
```

Then at the end of the script, after the `Print Orientation Summary`:

```python
FEATURES.print(tray.part)
```

## Where to register what

| Feature kind         | Face to use            | Typical dimensions |
|----------------------|------------------------|--------------------|
| Through hole         | The face it enters from | `diameter`, `through` |
| Counterbore / pocket | The face containing the opening | `diameter`, `depth` |
| Rectangular cutout / notch | The face the cut breaks through | `W`, `H` *or* `W`, `D`, `through` |
| Debossed / engraved text | The face the text is recessed into | `cap_height`, `depth`, plus one entry per `Text` line |
| Embossed text / boss / standoff | The face it grows out of | `diameter` or `W`/`H`, `height` |
| Slot / channel       | The face the slot opens onto | `W`, `L`, `depth` |
| Snap-fit hook        | The face the hook catches against | `engagement`, `width`, `depth` |
| Edge fillet / chamfer | **Skip** by default — these live on edges, not faces. Only register if the radius/size is design-critical (e.g. a fingertip-rounded rim); then pick the *primary* face the edge belongs to and note the adjacent face in `note`. | `radius` or `size`, `length` |

For features that span multiple faces (a vent that goes through both
side walls), register one entry per face.

## What this skill DOESN'T do

- It does **not** auto-detect features from final geometry. OCCT face
  selection on a finished part with fillets and booleans is too noisy
  to be reliable. Manual registration is the durable solution.
- It does not validate that registered dimensions match the actual
  geometry. If you change `NOTCH_W` and forget to update the `register`
  call, the inventory will print stale numbers — but reading them
  next to the parameter block will surface the drift quickly.
- It does not produce graphical output (axis cubes etc.). For that,
  see `cad-build123d-general` section 8a.

## See Also

- `cad-build123d-general` section 8a — `EXPORT_MODE`, `ORIENTATION`
  map, axis reference cube, print orientation summary. This skill
  sits next to that one and uses the same map.
- `electronics-enclosure-3dprint` *(separate plugin)* — uses an even more elaborate
  on-part labelling pattern in `test` mode (axis labels debossed on
  each wall). For pure documentation, the inventory printed by this
  skill is usually enough.
