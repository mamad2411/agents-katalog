---
name: print-bambu-3mf
description: 'Bambu Studio .3mf project file format: ZIP-archive layout, key XML/JSON files inside, important setting keys in project_settings.config, programmatic read/write recipes (Python zipfile + ElementTree), .3mf vs .gcode.3mf distinction, diffing and templating. USE FOR: extracting slicer settings from a saved .3mf, generating .3mf templates from STLs, diffing two .3mf project files, automating sidecar creation from a known-good slice, scripting Bambu Studio output, reading thumbnails or G-code out of a sliced project.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["3mf","bambu-studio","slicer","file-format","python","templating"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/3dprint", "emoji": "🖨️" } }
---

# Bambu Studio `.3mf` File Format — Reference

> **Companion skills:**
> - `print-bambu-studio` — slicer settings & profiles (the values that *go into* a .3mf)
> - `print-bambu-p2s` — printer hardware (where the .3mf eventually runs)
> - `cad-build123d-general` *(separate plugin)* §8a — production-mode
>   `*.print.md` sidecars, if you also model with build123d

## Purpose

`.3mf` is Bambu Studio's project format — model, plate layout, slicer
profile, per-object overrides, and (when sliced) the resulting G-code,
all bundled into a single file. This skill covers the **file format**:
what's inside a `.3mf`, what each piece means, and how to read/write
one programmatically.

For *what settings you should put in a .3mf*, see `print-bambu-studio`.
This skill is the parser/serializer reference, not the slicer reference.

## What's a `.3mf`?

A `.3mf` is a standard 3MF Consortium ZIP archive — Bambu Studio
extends it with vendor-specific config files. Two common variants:

| File | Contains | Use case |
|---|---|---|
| `something.3mf` | Model + plate + profile, **no G-code** | Project save; opens in Bambu Studio for re-slicing |
| `something.gcode.3mf` | All of the above **plus** sliced G-code + per-plate metadata | Sent to printer via Bambu Network / SD card |

Both are valid ZIP files. `unzip -l file.3mf` works. So does
Python's `zipfile` module.

## Internal layout

A typical Bambu `.3mf` (project save):

```
file.3mf  (ZIP)
├── [Content_Types].xml          # MIME type registry (3MF spec)
├── _rels/
│   └── .rels                    # ZIP package relationships (3MF spec)
├── 3D/
│   ├── 3dmodel.model            # Top-level model XML — references object_*.model files
│   └── Objects/
│       ├── object_1.model       # Per-object mesh XML (vertices + triangles)
│       ├── object_2.model
│       └── ...
└── Metadata/
    ├── project_settings.config  # XML — global slicer settings (THE big one)
    ├── model_settings.config    # XML — per-object setting overrides
    ├── slice_info.config        # XML — slice summary (filament weight, time, temps used)
    ├── plate_1.json             # JSON — plate layout, filament assignments
    ├── plate_1.png              # Thumbnail (PNG)
    ├── plate_1_small.png        # Small thumbnail
    ├── pick_1.png               # Object-pick thumbnail (for "pick" UI)
    ├── top_1.png                # Top-down preview
    ├── plate_1.gcode            # Sliced G-code (only in *.gcode.3mf)
    ├── plate_1.gcode.md5        # G-code checksum (only in *.gcode.3mf)
    ├── cut_information.xml      # Cut/clip tool history (if cutter was used)
    └── custom_gcode_per_layer.xml  # Per-layer custom G-code (color changes etc.)
```

For multi-plate projects, every per-plate file repeats with `_2`, `_3`,
etc. (`plate_2.json`, `plate_2.gcode`, `plate_2.png`, …).

### File responsibilities

| File | Format | What's in it | When to touch it |
|---|---|---|---|
| `3D/3dmodel.model` | XML (3MF spec) | `<resources>` (object IDs) and `<build>` (instance transforms) — the assembly tree | Replacing a mesh, changing transforms |
| `3D/Objects/object_*.model` | XML (3MF spec) | `<vertices>` + `<triangles>` for one object | Replacing a single object's geometry |
| `Metadata/project_settings.config` | XML | Hundreds of slicer settings (layer height, walls, infill, supports, temps, …) | **Most edits live here** |
| `Metadata/model_settings.config` | XML | Per-object overrides (this object uses filament 2, that one needs more supports) | Multi-material, per-object support tweaks |
| `Metadata/slice_info.config` | XML | What the slicer produced: filament length, weight, time per object | Read-only reference; regenerated on re-slice |
| `Metadata/plate_*.json` | JSON | Filament order on the AMS, plate type, bed temp override | Multi-color sequencing |
| `Metadata/plate_*.gcode` | Plain text G-code | The actual machine instructions | **Don't hand-edit** — re-slice instead |

## `project_settings.config` — the important keys

This is the file that controls almost everything. It's an XML doc with
hundreds of `<setting key="...">value</setting>` entries. Here are the
ones worth knowing for programmatic edits / sidecar generation:

### Geometry & quality
| Key | Type | Notes |
|---|---|---|
| `layer_height` | float (mm) | 0.20 default; 0.16 / 0.12 for finer detail |
| `initial_layer_print_height` | float (mm) | Usually 0.20 even on finer prints (better adhesion) |
| `wall_loops` | int | Wall count. 3 default; 4–5 for mechanical strength |
| `top_shell_layers` | int | Solid top layers. 5 default |
| `bottom_shell_layers` | int | Solid bottom layers. 3 default |
| `sparse_infill_density` | percent str ("15%") | Infill density |
| `sparse_infill_pattern` | enum | `gyroid` / `grid` / `honeycomb` / `lightning` / `concentric` |

### Speed
| Key | Type | Notes |
|---|---|---|
| `outer_wall_speed` | mm/s | Most-impactful quality setting |
| `inner_wall_speed` | mm/s | |
| `sparse_infill_speed` | mm/s | |
| `initial_layer_speed` | mm/s | First layer; lower for adhesion |
| `travel_speed` | mm/s | |

### Supports
| Key | Type | Notes |
|---|---|---|
| `enable_support` | "0" / "1" | Master switch |
| `support_type` | enum | `normal(auto)` / `tree(auto)` / `tree(manual)` / etc. |
| `support_threshold_angle` | deg | Default 30 |
| `support_top_z_distance` | float (mm) | 0.2 default; raise for easier removal |
| `support_filament` | int | 0 = same as object, 1+ = AMS slot for support material |
| `support_interface_top_layers` | int | More = smoother top of supported surface |

### Material / temperature (per-filament arrays — see below)
| Key | Type | Notes |
|---|---|---|
| `nozzle_temperature` | int array, "210,210,210,210" | Per AMS slot |
| `hot_plate_temp` | int | Bed temp |
| `filament_type` | str array | `PLA`, `PETG`, `ABS`, etc. per slot |
| `filament_settings_id` | str array | Profile name per slot |

### Brim / adhesion
| Key | Type | Notes |
|---|---|---|
| `brim_type` | enum | `auto_brim` / `outer_only` / `outer_and_inner` / `no_brim` |
| `brim_width` | float (mm) | |
| `brim_object_gap` | float (mm) | Default 0.0; raise to 0.1 if brim won't peel |

### "Per-something" arrays

Many settings are **comma-separated arrays indexed by AMS filament slot or
extruder**, not single values. Examples:

```xml
<setting key="nozzle_temperature">220,220,220,220</setting>
<setting key="filament_type">PLA;PETG;ABS;PLA</setting>
```

Be careful when mutating these — modifying the wrong index changes the
wrong filament.

## Reading a `.3mf` programmatically

Python stdlib only — no third-party deps needed for the basics.

```python
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

THREE_MF = Path("project.3mf")

# 1. Inspect contents
with zipfile.ZipFile(THREE_MF) as z:
    for name in z.namelist():
        info = z.getinfo(name)
        print(f"  {info.file_size:>10}  {name}")

# 2. Read project settings
with zipfile.ZipFile(THREE_MF) as z:
    with z.open("Metadata/project_settings.config") as f:
        tree = ET.parse(f)
root = tree.getroot()

# 3. Pull a single setting value
def get_setting(root, key):
    el = root.find(f".//setting[@key='{key}']")
    return el.text if el is not None else None

print("Layer height:", get_setting(root, "layer_height"))
print("Wall loops:",   get_setting(root, "wall_loops"))
print("Infill:",       get_setting(root, "sparse_infill_density"),
                       get_setting(root, "sparse_infill_pattern"))

# 4. Pull a thumbnail
with zipfile.ZipFile(THREE_MF) as z:
    if "Metadata/plate_1.png" in z.namelist():
        Path("preview.png").write_bytes(z.read("Metadata/plate_1.png"))
```

### Sliced G-code header has machine metadata

For `.gcode.3mf` files, the G-code itself starts with a comment block
that's often the easiest way to grab "what was this print":

```python
with zipfile.ZipFile(THREE_MF) as z:
    if "Metadata/plate_1.gcode" in z.namelist():
        gcode_head = z.read("Metadata/plate_1.gcode").decode("utf-8", errors="ignore")[:4000]
        print(gcode_head)
```

The first ~50 lines include filament weight, estimated time, layer count,
nozzle/bed temps, and Bambu Studio version.

## Writing / templating a `.3mf`

The cleanest pattern: **start from a known-good `.3mf`** (one you've
sliced and verified) and swap in the new mesh. This avoids hand-rolling
the XML namespaces and content-types boilerplate, which is fiddly.

```python
import shutil
import zipfile
from pathlib import Path

TEMPLATE   = Path("template.3mf")        # known-good baseline
NEW_STL    = Path("hf_bin.stl")
OUT        = Path("hf_bin.3mf")

# 1. Copy template
shutil.copy(TEMPLATE, OUT)

# 2. Replace the mesh inside the ZIP
#    Note: ZipFile can append but not delete in place; rewrite via tmp.
import tempfile
import os

with tempfile.TemporaryDirectory() as td:
    extracted = Path(td)
    with zipfile.ZipFile(OUT) as z:
        z.extractall(extracted)

    # Convert STL → 3MF mesh XML and overwrite
    # (in practice: use trimesh to load STL then write it back as 3mf
    # vertices+triangles in the existing object_1.model file)
    object_xml = extracted / "3D" / "Objects" / "object_1.model"
    write_mesh_xml(object_xml, NEW_STL)   # left as exercise; see trimesh recipe

    # 3. Re-zip preserving the 3MF folder structure
    OUT.unlink()
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for path in extracted.rglob("*"):
            if path.is_file():
                z.write(path, path.relative_to(extracted))
```

### Easier: just open Bambu Studio, swap mesh, save

For one-off use, the GUI workflow (open template, right-click object →
Replace with → pick new STL) is faster than scripting. Script when you
need to generate dozens of variants (e.g. one `.3mf` per Harbor Freight
bin preset).

### `trimesh` is a useful dependency for mesh I/O

```python
import trimesh
m = trimesh.load("hf_bin.stl")
# Vertices: m.vertices  (Nx3 float)
# Faces:    m.faces     (Mx3 int)
m.export("hf_bin.3mf", file_type="3mf")  # writes a minimal valid .3mf
```

The `trimesh`-exported `.3mf` is a **bare** 3MF (just the mesh, no
slicer settings). Bambu Studio will open it but treat it as a fresh
import — you'll lose any tuned profile. Use for round-tripping geometry,
not for preserving slicer state.

## Diffing two `.3mf` files

Useful when "I changed something between v1 and v2 — what was it?":

```python
import difflib
import zipfile
from pathlib import Path

A, B = Path("v1.3mf"), Path("v2.3mf")

def read_text(z, name):
    try:
        return z.read(name).decode("utf-8", errors="ignore").splitlines()
    except KeyError:
        return []

with zipfile.ZipFile(A) as za, zipfile.ZipFile(B) as zb:
    # Diff project settings (the most common change source)
    a_lines = read_text(za, "Metadata/project_settings.config")
    b_lines = read_text(zb, "Metadata/project_settings.config")
    print("\n".join(difflib.unified_diff(a_lines, b_lines,
                                         fromfile="v1 settings",
                                         tofile="v2 settings",
                                         lineterm="")))
```

For mesh diffs, compare vertex counts / bounding boxes via `trimesh`
rather than line-diffing the XML — vertex order may differ even when
the mesh is identical.

## Test-print profiles (prototype mode)

When iterating on a design, you don't need finish-quality prints — you
need fast, cheap test fits. The prototype workflow below comes from
[How-To Geek's "3 slicer tricks"](https://www.howtogeek.com/slicer-tricks-i-use-to-speed-up-3d-printing-prototypes/)
article. Author's measured savings on a real part:

| Mode | Time | Filament |
|---|---|---|
| Production (5 walls, 3D honeycomb infill) | 90 min | 69 g |
| Prototype (1 wall, lightning infill, 1 top, 1 bottom) | 49 min | 17 g |
| **Savings** | **~45%** | **~75%** |

### The three techniques

1. **Drop walls + top/bottom layers to 1.** Sacrifices structural
   integrity, fine for fit/dimension testing.
2. **Switch infill to `lightning`** (Bambu Studio name). Just enough
   structure to support top layers without the time/material cost of
   honeycomb or gyroid.
3. **Cut the model down to just the test region.** If you only need to
   validate one row of teeth or one mating surface, slice off
   everything else. Often turns a 60 min print into 5 min.

Techniques 1 + 2 mutate `project_settings.config`; technique 3 happens
in CAD or in Bambu Studio's cut tool — out of scope for the `.3mf`
mutator.

### Settings to mutate for "prototype mode"

| `project_settings.config` key | Production default | Prototype value | Why |
|---|---|---|---|
| `wall_loops` | 3 | **1** | One perimeter is enough to test fit |
| `top_shell_layers` | 5 | **1** | Visible top imperfection is acceptable |
| `bottom_shell_layers` | 3 | **1** | First layer is the bottom; bonus ones add cost |
| `sparse_infill_pattern` | `gyroid` / `grid` / `honeycomb` | **`lightning`** | Minimum structure to hold top layer |
| `sparse_infill_density` | `15%` | **`5%`–`10%`** | Lightning still works at low density |
| `enable_support` | `1` (when needed) | **`0`** | Skip supports on prototypes; redesign if it can't print without |

Settings to **not** drop in prototype mode (these protect first-layer
adhesion or surface flatness, both of which matter even for test fits):

- `initial_layer_print_height` — keep at 0.20 mm
- `initial_layer_speed` — don't speed this up; first layer must stick
- `brim_type` / `brim_width` — keep your usual brim if the part needs it
- `nozzle_temperature` / `hot_plate_temp` — keep at material defaults

### A "draft" profile is more aggressive (fit only, not function)

Sometimes you're checking *just* a contour or a hole position — you
won't even handle the part beyond removing it from the bed. For that:

| Key | Draft value | Notes |
|---|---|---|
| `layer_height` | `0.28` mm (vs default `0.20`) | Coarsest height the printer reliably runs |
| `wall_loops` | `1` | Same as prototype |
| `top_shell_layers` | `0` | **Vase mode candidate** — no top at all |
| `bottom_shell_layers` | `1` | |
| `sparse_infill_density` | `0%` | Skip infill entirely |
| `enable_support` | `0` | |
| `print_sequence` | `by object` | Prints faster on multi-part plates |

Draft mode is "this is going in the bin after I look at it" speed.
Don't use for parts you'll fit-check against another part — the layer
height is too coarse to trust ±0.1 mm.

### Mutation pattern (preserve the file structure)

Use the read pattern from above to load `project_settings.config`,
mutate values, write back. **Do not regenerate `[Content_Types].xml`,
`_rels/.rels`, or any of the per-plate `.gcode` / `.gcode.md5` files**
— if you keep the G-code, its checksum will mismatch the new settings.
Either:

- **Drop the G-code on save** so Bambu Studio re-slices on open
  (recommended for project saves), or
- **Re-slice via Bambu Studio CLI** if you need a printer-ready
  `.gcode.3mf` (`bambu-studio.exe --slice 0 --export-3mf out.3mf in.3mf`)

```python
import shutil, tempfile, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

PROTOTYPE_OVERRIDES = {
    "wall_loops":              "1",
    "top_shell_layers":        "1",
    "bottom_shell_layers":     "1",
    "sparse_infill_pattern":   "lightning",
    "sparse_infill_density":   "10%",
    "enable_support":          "0",
}

def apply_overrides(in_3mf: Path, out_3mf: Path, overrides: dict) -> None:
    """Apply project_settings.config overrides; drop sliced G-code so
    Bambu Studio re-slices on open."""
    with tempfile.TemporaryDirectory() as td:
        ext = Path(td)
        with zipfile.ZipFile(in_3mf) as z:
            z.extractall(ext)

        # Mutate project settings
        cfg = ext / "Metadata" / "project_settings.config"
        tree = ET.parse(cfg)
        root = tree.getroot()
        for key, val in overrides.items():
            el = root.find(f".//setting[@key='{key}']")
            if el is None:
                # Setting absent — append it (Bambu Studio tolerates extras)
                el = ET.SubElement(root, "setting", attrib={"key": key})
            el.text = val
        tree.write(cfg, encoding="utf-8", xml_declaration=True)

        # Drop sliced G-code + checksums (force re-slice on open)
        for stale in (ext / "Metadata").glob("plate_*.gcode*"):
            stale.unlink()

        # Re-zip
        with zipfile.ZipFile(out_3mf, "w", zipfile.ZIP_DEFLATED) as z:
            for path in ext.rglob("*"):
                if path.is_file():
                    z.write(path, path.relative_to(ext))
```

### Companion tooling

This skill folder ships two reference scripts under `scripts/`:

- `make_template.py` — generates a baseline `.3mf` from a 20 mm
  calibration cube STL using `trimesh` (a "minimal valid 3mf" you can
  hand to the mutator).
- `apply_test_profile.py` — CLI wrapper around the mutation pattern
  above. Picks `prototype` / `draft` / custom JSON profile, writes
  `<input>-<profile>.3mf`.

See `scripts/README.md` in this skill folder for usage.

## Common gotchas

| Symptom | Cause | Fix |
|---|---|---|
| `BadZipFile: File is not a zip file` | File is corrupted or you got a partial download | Re-export from Bambu Studio; verify with `unzip -l` |
| Settings I changed don't appear when I re-open | Edited `project_settings.config` but didn't re-zip with the right `[Content_Types].xml` | Always preserve `[Content_Types].xml` and `_rels/.rels` byte-for-byte |
| Bambu Studio opens the file but shows "imported as bare mesh, no profile" | Used `trimesh.export(..., file_type="3mf")` which produces a minimal 3MF without Metadata/ folder | Start from a Bambu-saved template, swap mesh in place |
| G-code present but printer rejects file | `plate_*.gcode.md5` checksum doesn't match the (modified) G-code | Re-slice in Bambu Studio; don't hand-edit G-code |
| Multi-material project loads with all filaments collapsed to slot 1 | Edited `nozzle_temperature` from `"220,220,220,220"` to `"220"` | Always preserve the comma-separated array shape |
| Thumbnail is wrong after replacing mesh | `plate_1.png` is baked at slice time, not regenerated on file open | Either re-slice, or replace `plate_1.png` with a freshly-rendered preview |
| ZIP is huge for a small model | Bambu Studio embeds full-size + small thumbnails + per-object pick PNGs | Strip `Metadata/*.png` if you only need geometry + settings (saves MB) |

## When .3mf vs STL?

| Scenario | Use |
|---|---|
| Sharing a printable model online | **STL** (universal) or **3MF** (better — embeds units + manifold info) |
| Saving your own work in progress | **.3mf project save** (preserves slicer profile) |
| Sending to printer | **`.gcode.3mf`** (sliced) |
| CAD source for an existing project | Keep the **`.py` / `.scad`**; treat `.stl` and `.3mf` as build artifacts |
| Generating dozens of variants | Script writes **STL** per variant; one **template .3mf** per print profile, mesh-swapped at print time |

## See Also

- 3MF Consortium spec: <https://github.com/3MFConsortium/spec_core>
- Bambu Studio source (its 3MF read/write code is the canonical reference for vendor extensions): <https://github.com/bambulab/BambuStudio>
- `trimesh` 3MF I/O: <https://trimesh.org/trimesh.exchange.threemf.html>
- Sister skills: `print-bambu-studio` (slicer settings the .3mf records), `print-bambu-p2s` (printer hardware that consumes the .gcode.3mf)
