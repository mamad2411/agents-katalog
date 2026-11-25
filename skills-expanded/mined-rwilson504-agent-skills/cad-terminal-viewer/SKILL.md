---
name: cad-terminal-viewer
description: 'Display STL/STEP model previews and CAD-generated PNGs directly in the terminal using rich-pixels (Python, cross-platform) or timg (Linux/macOS), bridging the render-to-PNG pipeline with in-terminal viewing. USE FOR: view STL in terminal, preview model in console, timg, rich-pixels, terminal image viewer, display PNG in terminal, quick visual check, headless preview, CLI model preview.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["terminal","preview","stl","rich-pixels","timg"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# Terminal Model & Image Viewer

> **Prerequisite:** Load `cad-build123d-general` first for export conventions.
> Works alongside `cad-build123d-six-view-checks` and `cad-render-images`.

## Purpose

Display CAD model previews (rendered PNGs from STL/STEP files) and any
project images directly in the terminal without leaving the CLI. Two
display backends are supported:

1. **rich-pixels** (Python, cross-platform — **preferred on Windows**)
2. **timg** (native binary — Linux/macOS only, no Windows builds)

Both use trimesh + pyglet as the STL-to-PNG bridge.

This skill is useful when:

- Working in a terminal-only session (SSH, CI, headless, Copilot CLI)
- You want a quick visual sanity check after a rebuild without opening a
  GUI viewer
- Displaying six-view check images or render outputs inline

## Source of Truth

This skill is the source of truth for **in-terminal image display** in
this repo. Other skills (`cad-build123d-six-view-checks`,
`cad-render-images`) generate the PNGs; this skill displays them.

---

## Display Backends

### Option 1: rich-pixels (Python — recommended, cross-platform)

Uses `rich` + `rich-pixels` + `Pillow` to render images as colored
Unicode half-block characters. Works in any 24-bit color terminal.

| Field | Value |
|-------|-------|
| **PyPI** | `rich`, `rich-pixels`, `Pillow` |
| **License** | MIT |
| **Platform** | Windows, macOS, Linux — anywhere Python runs |
| **Resolution** | Unicode half-blocks (2 pixels per character cell) |

#### Install

```powershell
pip install rich rich-pixels Pillow
```

#### Usage

```python
from rich.console import Console
from rich_pixels import Pixels
from PIL import Image

console = Console()
img = Image.open("model_preview.png")
pixels = Pixels.from_image(img, resize=(90, 45))
console.print(pixels)
```

### Option 2: timg (native binary — Linux/macOS)

[timg](https://github.com/hzeller/timg) is a native terminal image viewer
supporting Sixel, Kitty, iTerm2 graphics protocols, or Unicode fallback.

> **⚠ Windows:** timg has **no prebuilt Windows binary** as of v1.6.x.
> Use `rich-pixels` on Windows instead.

| Field | Value |
|-------|-------|
| **Repo** | <https://github.com/hzeller/timg> |
| **License** | GPL v2 |
| **Protocols** | Sixel, Kitty, iTerm2, Unicode half/quarter blocks |
| **Formats** | PNG, JPEG, GIF, BMP, TIFF, WebP (2D images only) |

#### Install

```bash
# macOS (Homebrew)
brew install timg

# Ubuntu/Debian
sudo apt install timg

# Arch Linux
sudo pacman -S timg
```

#### Key flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-g WxH` | Output geometry in character cells | `timg -g 80x40 model.png` |
| `-p <mode>` | Pixelation: `h`=half, `q`=quarter, `k`=kitty, `i`=iterm2, `s`=sixel | `timg -pk model.png` |
| `--grid=N` | Show multiple images in N columns | `timg --grid=3 *.png` |
| `--title` | Print filename above each image | `timg --title *.png` |
| `-W` | Scale to fit terminal width | `timg -W model.png` |

---

## STL-to-PNG Rendering Pipeline

Both display backends need a PNG. STL/STEP files must be rendered first.

### Dependencies

```powershell
pip install trimesh "pyglet<2" numpy
```

> `pyglet<2` is required — trimesh's `save_image()` uses pyglet's
> OpenGL context for offscreen rendering.

### Rendering with a good isometric camera

trimesh's default camera often produces a flat, poorly-lit view.
**Rotate the mesh to an isometric angle before creating the scene** —
this is more reliable than fighting camera transforms.

```python
import trimesh
import trimesh.transformations as tf
import numpy as np
from pathlib import Path

def stl_to_png(
    stl_path: str,
    png_path: str,
    resolution: tuple = (1024, 768),
    color: tuple = (100, 149, 237, 255),  # cornflower blue
) -> Path:
    """Render an STL to a nice isometric PNG."""
    mesh = trimesh.load(stl_path)

    # Color the mesh (STL files have no color data)
    mesh.visual.face_colors = color

    # Center at origin, then rotate for a 3/4 iso view
    mesh.apply_translation(-mesh.centroid)
    rot = tf.euler_matrix(np.radians(-30), 0, np.radians(30), "sxyz")
    mesh.apply_transform(rot)

    # Let trimesh auto-frame the rotated mesh
    scene = mesh.scene()
    png_data = scene.save_image(resolution=resolution)

    out = Path(png_path)
    out.write_bytes(png_data)
    return out
```

### Why rotate the mesh instead of the camera?

trimesh's `scene.camera_transform` and `camera.look_at()` are fragile —
small missteps push the model out of frame entirely (blank white image).
Rotating the mesh at the origin and letting `scene()` auto-frame is
robust and produces consistent results.

---

## Complete Preview Helper (drop-in)

This helper tries `rich-pixels` first, then `timg`, then falls back to
printing the file path.

```python
import shutil
import subprocess
from pathlib import Path


def terminal_preview(
    image_path: str | Path,
    width: int = 90,
    height: int = 45,
) -> None:
    """Display an image in the terminal. Best-effort — never raises."""
    image_path = Path(image_path)
    if not image_path.exists():
        print(f"[preview] File not found: {image_path}")
        return

    # Try rich-pixels first (cross-platform, no binary needed)
    try:
        from rich.console import Console
        from rich_pixels import Pixels
        from PIL import Image

        console = Console()
        img = Image.open(image_path)
        pixels = Pixels.from_image(img, resize=(width, height))
        console.print(pixels)
        return
    except ImportError:
        pass

    # Try timg (Linux/macOS)
    if shutil.which("timg"):
        subprocess.run(
            ["timg", "-W", "-g", f"{width}x", str(image_path)],
            check=False,
        )
        return

    # Fallback
    print(f"[preview] No terminal viewer found.")
    print(f"[preview]   pip install rich rich-pixels Pillow")
    print(f"[preview] Image saved to: {image_path}")
```

---

## Integration Patterns

### After six-view checks

```python
# Display all six views after generation
from pathlib import Path

views_dir = Path("exports/views")
for png in sorted(views_dir.glob("*.png")):
    print(f"\n--- {png.stem} ---")
    terminal_preview(png, width=60, height=30)
```

Or with timg (Linux/macOS) as a one-liner:

```bash
timg --grid=3 --title exports/views/*.png
```

### After render-images

```python
terminal_preview("exports/renders/hero.png")
```

### In a build123d script (auto-preview after export)

```python
# At the end of your model script, after exporting STL:
stl_to_png("exports/my_part.stl", "exports/my_part_preview.png")
terminal_preview("exports/my_part_preview.png")
```

---

## Agent Integration Pattern

When an agent rebuilds a model and generates PNGs (six-view, render,
or ad-hoc), it should attempt to display them in the terminal:

1. Render the STL to a PNG using `stl_to_png()` (rotate mesh for iso view).
2. Display with `terminal_preview()` — auto-detects available backend.
3. If no viewer is available, print the file path.

This is **best-effort** — never fail a build because a viewer is missing.

---

## Quick Reference

| Task | Python | timg (Linux/macOS) |
|------|--------|--------------------|
| Preview a single PNG | `terminal_preview("model.png")` | `timg -W model.png` |
| Preview at specific size | `terminal_preview("model.png", 100, 50)` | `timg -g 100x50 model.png` |
| Six-view grid | loop + `terminal_preview()` | `timg --grid=3 --title exports/views/*.png` |
| Compare two renders | side-by-side print | `timg --grid=2 before.png after.png` |
| Render STL then preview | `stl_to_png()` + `terminal_preview()` | N/A |

## Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `No module named 'pyglet'` | Missing render dependency | `pip install "pyglet<2"` |
| `No module named 'rich_pixels'` | Missing display dependency | `pip install rich rich-pixels Pillow` |
| Blank white PNG from trimesh | Camera transform pushed model out of frame | Rotate the mesh at origin instead of moving the camera (see rendering section) |
| Dark/flat-looking render | Default camera points at a uniform face | Apply iso rotation: `euler_matrix(-30°, 0, 30°)` before `scene()` |
| timg not available on Windows | No prebuilt Windows binary | Use `rich-pixels` (Python) instead |
| Image looks garbled/blocky | Terminal doesn't support 24-bit color | Upgrade to Windows Terminal, WezTerm, iTerm2, or Kitty |
| Black image from trimesh | No OpenGL context available (headless) | Install `pyglet<2`; on headless Linux use `xvfb-run` or `pyvista` with `start_xvfb()` |

## See Also

- rich-pixels: <https://github.com/darrenburns/rich-pixels>
- timg: <https://github.com/hzeller/timg>
- Related skill: `cad-build123d-six-view-checks` (generates the PNGs)
- Related skill: `cad-render-images` (publication renders)
- Related skill: `cad-build123d-tools` (broader tooling catalog)
