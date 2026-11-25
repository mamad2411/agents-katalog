---
name: cad-render-images
description: 'Generate publication-quality PNG/GIF/MP4 renders from build123d models for documentation sites, README hero shots, and embedded HTML images. USE FOR: hero/isometric renders, web-optimized PNGs, exploded views, cross-section/cutaway renders, animated turntables, color preservation from build123d Color() tags, transparent or dark-theme backgrounds, HTML <img>/<picture> embedding patterns, documentation render pipeline, headless render with trimesh + pyvista, render PCB assembly, render enclosure with components.'
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["build123d","rendering","png","documentation","visualization"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/plugins/cad", "emoji": "📐" } }
---

# CAD Render Images Skill

> **Prerequisite:** Load `cad-build123d-general` first (export workflow, orientation
> map, `Color()` tagging conventions).
>
> **Sister skill:** `cad-build123d-six-view-checks` — that skill owns
> regression QA snapshots (six fixed orthographic angles). **This** skill
> owns documentation/marketing renders (hero shots, exploded views,
> turntables, cutaways) intended for embedding on doc sites and READMEs.
> Use both: six-view for "did I break the geometry," this skill for
> "make it look good in the docs."

## Purpose

Turn `BuildPart` / `Compound` outputs into images that go into HTML
documentation pages, project READMEs, and shareable previews. Outputs:

- **PNG** — primary format. Web-optimized, transparent or themed
  background, dimensions tuned for docs page layouts.
- **GIF / MP4** — animated turntables for showing 3D context inline
  in HTML (`<img>` tag for GIF, `<video>` for MP4).
- **Optional alpha-channel masks** — for compositing into themed
  documentation pages.

This is project-agnostic: the same workflow renders a CAD container, a
PCB CAD assembly, an enclosure with components placed inside, or a
multi-part organizer.

---

## 1. When to Use Which Render Type

| Render type | Use when | Output |
|-------------|----------|--------|
| **Hero / isometric** | Top of a project README or doc page; "what is this thing" shot | PNG, ~1200×900, transparent or themed bg |
| **Top-down** | PCB layout pages (matches the SVG board view orientation) | PNG, square or page-width |
| **Six orthographic** | Regression QA after geometry edits | See `cad-build123d-six-view-checks` |
| **Exploded view** | Show assembly order, where components plug in, lid-on-base relationship | PNG, isometric camera |
| **Cross-section / cutaway** | Reveal internal structure (component clearance, standoffs, lid groove fit, internal channels) | PNG, isometric camera |
| **Turntable GIF/MP4** | Embed 3D context inline in a docs page without WebGL | Animated, ~3-5 s loop, ~600-800 px wide |

**Rule of thumb:** if the user reads the doc page, what's the *one* image
that conveys the design? That's a hero render. Everything else is
supplementary and goes lower on the page.

---

## 2. Tooling Stack

Same primary stack as `cad-build123d-six-view-checks` for consistency:

```powershell
pip install trimesh pyvista pillow imageio "imageio[ffmpeg]"
```

| Library | Role |
|---------|------|
| `trimesh` | Read STEP/STL/3MF; manipulate meshes; cross-sections |
| `pyvista` | Off-screen rendering, lighting, camera control, color tags |
| `pillow` | PNG post-processing, alpha compositing, resize/crop |
| `imageio` | GIF and MP4 encoding for turntables |

Off-screen rendering needs a working OpenGL context. On Windows this is
fine out of the box. On headless Linux CI, install `xvfb` and run:
`xvfb-run -a python render_images.py`.

---

## 3. Standard Render Pipeline

Every render follows the same pattern. Build a single `render_part(...)`
helper at the top of your render script and reuse it.

```python
from pathlib import Path
import pyvista as pv
import trimesh
from PIL import Image

# --- Theme constants (match docs site) ---
BG_DARK   = (13, 17, 23)      # #0d1117 — matches docs dark theme
BG_LIGHT  = (255, 255, 255)
BG_NONE   = None              # transparent (alpha=0)

# --- Standard sizes ---
HERO_SIZE     = (1600, 1200)
PAGE_WIDE     = (1200, 600)
SQUARE        = (1024, 1024)
TURNTABLE     = (800, 600)


def load_3mf(path: Path) -> dict:
    """Load a 3MF and return {name: (mesh, color)} for each part.
    3MF preserves build123d Color() tags as per-shape colors."""
    scene = trimesh.load(path, process=False)
    parts = {}
    if isinstance(scene, trimesh.Scene):
        for name, geom in scene.geometry.items():
            color = None
            if hasattr(geom.visual, "face_colors") and len(geom.visual.face_colors):
                # All faces share one color (typical for build123d export)
                rgba = geom.visual.face_colors[0]
                color = (rgba[0] / 255, rgba[1] / 255, rgba[2] / 255)
            parts[name] = (geom, color)
    else:
        parts["part"] = (scene, None)
    return parts


def render_part(parts: dict, out_path: Path, *,
                size=HERO_SIZE, bg=BG_DARK,
                camera="iso", zoom=1.0, opacity_overrides=None):
    """Render a parts dict to PNG. `parts` is {name: (mesh, color)}."""
    transparent = bg is None
    plotter = pv.Plotter(off_screen=True, window_size=size,
                          polygon_smoothing=True, line_smoothing=True)
    plotter.set_background([c / 255 for c in bg] if bg else (0, 0, 0))

    for name, (mesh, color) in parts.items():
        opacity = (opacity_overrides or {}).get(name, 1.0)
        pv_mesh = pv.wrap(mesh)
        plotter.add_mesh(pv_mesh,
                         color=color or (0.7, 0.7, 0.75),
                         smooth_shading=True,
                         opacity=opacity,
                         specular=0.3,
                         specular_power=15)

    set_camera(plotter, camera, zoom=zoom)
    plotter.enable_anti_aliasing("ssaa")   # 4× super-sample, sharpest
    plotter.screenshot(str(out_path), transparent_background=transparent)
    plotter.close()


def set_camera(plotter, mode: str, zoom: float = 1.0):
    if mode == "iso":
        plotter.view_isometric()
    elif mode == "top":
        plotter.view_xy()
    elif mode == "front":
        plotter.view_xz()    # +Y → camera looks into -Y
    elif mode == "right":
        plotter.view_yz()
    else:
        raise ValueError(f"unknown camera mode: {mode}")
    plotter.camera.zoom(zoom)
```

---

## 4. Color Preservation from build123d

`Color()` tags applied in build123d **survive into 3MF exports** as
per-shape RGBA. They do **NOT survive STL** (STL has no color).

### Pattern: tag, export 3MF, render

```python
# In your build123d script
from build123d import Color, Mesher

pcb.part.color  = Color(0.07, 0.30, 0.45)        # FR-4 blue
copper.color    = Color(0.85, 0.55, 0.13)        # copper brown
led_red.color   = Color(0.95, 0.20, 0.20, 0.85)  # alpha = 85% (translucent dome)

exporter = Mesher()
exporter.add_shape(pcb.part)
exporter.add_shape(copper)
exporter.add_shape(led_red)
exporter.write("assembly.3mf")     # <-- colors preserved here
```

```python
# In the render script
parts = load_3mf(Path("assembly.3mf"))
render_part(parts, Path("hero.png"), bg=BG_DARK)
```

### Gotchas

| Symptom | Cause | Fix |
|---------|-------|-----|
| Renders are uniform gray | Loaded an STL, not a 3MF | Re-export as 3MF; STL has no color |
| Translucent parts look opaque | Forgot to set alpha in `Color(r,g,b,a)` | Add the alpha component; default is 1.0 |
| Part is invisible | Alpha set to 0; or color tagged on intermediate `BuildPart` not the returned `Compound` | Tag the value you actually export |
| All parts share the first part's color | 3MF reader merged them; pass `process=False` to `trimesh.load` | Already done in `load_3mf()` above |

---

## 5. Hero / Isometric Renders

The default starting point. Standard angle: `view_isometric()` which is
equivalent to `(1, 1, 1)` direction looking at origin, +Z up.

```python
parts = load_3mf(Path("exports/desk_organizer.3mf"))
render_part(parts, Path("exports/desk_organizer_hero.png"),
            size=HERO_SIZE, bg=BG_DARK, camera="iso", zoom=1.1)
```

### Angle variations worth keeping in your back pocket

| Variant | Camera setup |
|---------|-------------|
| Front-three-quarter | `plotter.camera_position = [(2, -2, 1.5), (0,0,0), (0,0,1)]` |
| Top-down 30° | `plotter.camera_position = [(0, -1, 2), (0,0,0), (0,1,0)]` |
| Low hero (dramatic) | `plotter.camera_position = [(2, 0.5, 0.3), (0,0,0), (0,0,1)]` |

Always pass `(camera_position, focal_point, up)` as a 3-tuple of 3-tuples.

---

## 6. Web-Optimized Output

Two output styles depending on where the image lands:

### Themed (matches docs dark mode)
```python
render_part(parts, Path("exports/page_iso.png"),
            size=PAGE_WIDE, bg=BG_DARK)
```

The PNG carries the dark background bake-in. Renders crisply on dark and
light themes (the dark plate just looks intentional on light themes).

### Transparent (composites onto any background)
```python
render_part(parts, Path("exports/page_iso.png"),
            size=PAGE_WIDE, bg=BG_NONE)
```

Use transparent when:
- The host page may switch themes (light/dark toggle)
- The image goes into a Markdown README on GitHub (GitHub auto-themes)
- You want to overlay onto a styled card

### Anti-aliasing tier
- `enable_anti_aliasing("ssaa")` — best quality (4× super-sample). Slower.
  Use for hero shots and anything embedded large.
- `enable_anti_aliasing("msaa")` — faster, slightly softer. Use for
  turntable frames where speed matters.
- `enable_anti_aliasing("fxaa")` — fastest, softest. Avoid for static
  images.

### Crop & resize via Pillow
```python
img = Image.open("exports/page_iso.png")
img = img.crop(img.getbbox())     # tight-crop to non-transparent pixels
img.thumbnail((1200, 1200), Image.LANCZOS)
img.save("exports/page_iso.png", optimize=True)
```

`optimize=True` shaves ~10-30% from PNG size. For READMEs, also run
through `oxipng` or `pngquant` if size matters.

---

## 7. Exploded Views

Translate each part along an axis (usually `+Z` for lid-up explosions)
proportional to its bounding-box index, then render normally.

```python
def explode(parts: dict, *, axis="z", spacing=15.0) -> dict:
    """Offset each part along an axis. Order of dict = stack order
    (bottom → top). Returns a new {name: (mesh, color)} dict."""
    exploded = {}
    for i, (name, (mesh, color)) in enumerate(parts.items()):
        offset = [0, 0, 0]
        offset["xyz".index(axis)] = i * spacing
        exploded[name] = (mesh.copy().apply_translation(offset), color)
    return exploded


# Usage
parts = load_3mf(Path("exports/enclosure.3mf"))
exploded_parts = explode(parts, axis="z", spacing=20.0)
render_part(exploded_parts, Path("exports/enclosure_exploded.png"),
            size=HERO_SIZE, bg=BG_DARK, camera="iso", zoom=0.9)
```

### Picking the right axis & spacing
- **Lid-on-base enclosure:** `axis="z", spacing=20-30 mm`
- **Stacked PCB + components:** `axis="z", spacing=8-15 mm`
- **Side-by-side parts (e.g. controller + launchpad):** `axis="x"` or
  `axis="y"`, spacing = ~half of the longest part dimension
- Spacing too tight → reads as a misalignment bug. Too wide → loses
  the spatial relationship.

### Add ghost/lead lines (optional)
After rendering, overlay dashed lines in Pillow connecting matching
features (e.g. screw → screw hole) to make the assembly explicit.

---

## 8. Cross-Section / Cutaway Renders

Slice the model with a plane, keep one side, render. Two approaches:

### A) Trimesh slice (clean cut, fast)
```python
def cutaway(mesh: trimesh.Trimesh, *, plane_origin=(0,0,0),
            plane_normal=(0,1,0), keep="positive") -> trimesh.Trimesh:
    """Cut a mesh with a plane and keep one half. `keep` = 'positive' or
    'negative' (relative to the plane normal direction)."""
    sliced = mesh.slice_plane(plane_origin=plane_origin,
                               plane_normal=plane_normal,
                               cap=True)   # cap=True closes the cut face
    if keep == "negative":
        sliced = mesh.slice_plane(plane_origin=plane_origin,
                                   plane_normal=[-n for n in plane_normal],
                                   cap=True)
    return sliced


# Cut the front half off an enclosure to show internal standoffs
parts = load_3mf(Path("exports/enclosure.3mf"))
cut_parts = {name: (cutaway(m, plane_normal=(0, 1, 0)), c)
              for name, (m, c) in parts.items()}
render_part(cut_parts, Path("exports/enclosure_cutaway.png"),
            size=HERO_SIZE, bg=BG_DARK, camera="iso")
```

### B) Pyvista clip (interactive plane preview)
```python
plotter.add_mesh_clip_plane(pv_mesh, normal="y", origin=(0, 0, 0),
                              invert=True)
```
Use this when you want the user to scrub the cut plane interactively
before exporting.

### Highlighting the cut face
The capped cut face inherits the part's color. To make it visually
distinct (so users see "this is a section view"), color it bright cyan
or red:

```python
cut_face_color = (0, 1, 1)   # cyan = "section cut" convention
```

Detect cut faces by their flatness (`mesh.face_normals` aligned with the
slice normal) and recolor before passing to pyvista.

---

## 9. Animated Turntables (GIF / MP4)

Rotate the camera around the model in N steps, capture each frame, encode.

```python
import imageio

def render_turntable(parts: dict, out_path: Path, *,
                     size=TURNTABLE, bg=BG_DARK,
                     frames=60, elevation=25, fmt="gif"):
    """Render N frames around the Z axis. fmt = 'gif' or 'mp4'."""
    plotter = pv.Plotter(off_screen=True, window_size=size)
    plotter.set_background([c/255 for c in bg])
    for name, (mesh, color) in parts.items():
        plotter.add_mesh(pv.wrap(mesh),
                         color=color or (0.7, 0.7, 0.75),
                         smooth_shading=True)
    plotter.enable_anti_aliasing("msaa")

    images = []
    for i in range(frames):
        azimuth = 360 * i / frames
        plotter.camera_position = "iso"
        plotter.camera.azimuth = azimuth
        plotter.camera.elevation = elevation
        plotter.render()
        images.append(plotter.screenshot(return_img=True))
    plotter.close()

    if fmt == "gif":
        imageio.mimsave(out_path, images, fps=20, loop=0)
    elif fmt == "mp4":
        imageio.mimsave(out_path, images, fps=30, codec="libx264",
                          quality=8)
```

### Format choice
| Format | Use when | Size guidance |
|--------|----------|---------------|
| **GIF** | README hero loop; works in plain `<img>` tag | Keep < 2 MB; reduce `frames` to 30-40 if needed |
| **MP4 (H.264)** | Docs site that supports `<video>` tag | 4-8× smaller than equivalent GIF; use this when possible |
| **WebM (VP9)** | Even smaller than MP4, but Safari support is patchy | Only if the docs site is GitHub Pages + Chrome-first |

### GIF size discipline
GIFs balloon fast. Lever them in this order:
1. Reduce `frames` (60 → 30)
2. Reduce `size` (800×600 → 600×450)
3. Reduce frame count further if loop still loops well at 24 frames
4. Quantize palette: `imageio.mimsave(..., palettesize=128)`

---

## 10. HTML Embedding Patterns

Drop-in HTML for the docs site. If you also run the `electronics-pcb-boards`
/ `electronics-pcb-components` skills *(separate plugin)*, the SVG layouts
they produce pair well with these renders.

### Single hero image
```html
<figure class="hero">
  <img src="exports/desk_organizer_hero.png" alt="Desk organizer assembled view"
       width="1200" loading="lazy">
  <figcaption>Assembled view, isometric</figcaption>
</figure>
```

### Light/dark theme switching with `<picture>`
```html
<picture>
  <source srcset="exports/hero_dark.png" media="(prefers-color-scheme: dark)">
  <img src="exports/hero_light.png" alt="Project hero" width="1200" loading="lazy">
</picture>
```

Render two themed versions in the same script:
```python
render_part(parts, Path("exports/hero_dark.png"),  bg=BG_DARK)
render_part(parts, Path("exports/hero_light.png"), bg=BG_LIGHT)
```

### Turntable embedding
```html
<!-- GIF (always works) -->
<img src="exports/turntable.gif" alt="Rotating view" width="800">

<!-- MP4 (smaller, but needs <video>) -->
<video src="exports/turntable.mp4" autoplay loop muted playsinline
        width="800"></video>
```

### Multi-view gallery (matches PCB docs page convention)
```html
<div class="cad-gallery">
  <figure><img src="exports/pcb_top.png"     alt="Top-down PCB view"></figure>
  <figure><img src="exports/pcb_iso.png"     alt="Isometric assembly"></figure>
  <figure><img src="exports/pcb_exploded.png" alt="Exploded view"></figure>
  <figure><img src="exports/pcb_cutaway.png"  alt="Section view"></figure>
</div>
```

Pair each `<figure>` with a CSS grid container in your project's
`styles.css` for a clean 2×2 or 4× row layout.

---

## 11. Recommended Project Structure

```
<project>/
  exports/
    <part>.3mf                     # build123d output (color-tagged)
    <part>.step                    # interchange format
    images/
      <part>_hero.png              # default isometric, dark theme
      <part>_hero_light.png        # light-theme variant (optional)
      <part>_top.png               # top-down (PCBs especially)
      <part>_exploded.png          # exploded view
      <part>_cutaway.png           # cross-section
      <part>_turntable.mp4         # animated (or .gif)
      qa/                          # six-view-checks output (separate folder)
        <part>_front.png
        ...
  render_images.py                 # this skill's pipeline lives here
  <part>.py                        # build123d source
```

Keep `qa/` (regression checks) separate from `images/` (publication
renders). Different audiences, different cadence.

### Render script as build step
Add an `EXPORT_MODE` guard so renders only run when explicitly requested:

```python
RENDER_IMAGES = True   # toggle off for fast iteration

if EXPORT_MODE in ("design", "production") and RENDER_IMAGES:
    from render_images import render_all
    render_all(Path("exports/<part>.3mf"), Path("exports/images/"))
```

Renders are slow (1-5 s per still, 10-60 s per turntable). Keep them
behind a flag so they don't fire on every geometry tweak.

---

## 12. Quick Reference: Common Failure Modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Renders show uniform gray, not part colors | Loaded STL instead of 3MF | Switch source to 3MF |
| `pyvista` errors about display / X server on Linux | No OpenGL context | Wrap with `xvfb-run -a python ...` |
| Hero render is dim and flat | Default lighting; no specular | Pass `specular=0.3, specular_power=15` to `add_mesh` |
| Edges look pixelated / aliased | Anti-aliasing not enabled | `plotter.enable_anti_aliasing("ssaa")` |
| Turntable GIF is 25 MB | Too many frames or too high resolution | Reduce frames to 30, drop size to 600×450, set `palettesize=128` |
| Cross-section shows hollow interior, not solid | `slice_plane(cap=False)` leaves an open face | Pass `cap=True` |
| Exploded view looks misaligned, not exploded | Spacing too small | Increase to ~part-thickness × 4 |
| Transparent PNG has white halo on dark background | Alpha was rasterized against white | Re-export with `transparent_background=True` AND no opaque background mesh |
| Camera angle changes between runs | `view_isometric()` has consistent default; manual `camera_position` doesn't | Always set both `camera_position` + `focal_point` + `up` explicitly |
| Color shift between docs page and rendered PNG | Page CSS applies a filter (brightness, hue-rotate) | Inspect with browser dev tools; remove filter or pre-bake it into the render |

---

## See Also

- `cad-build123d-general` — `Color()` tagging, export-mode workflow
- `cad-build123d-six-view-checks` — sister skill: regression QA snapshots
- `cad-build123d-tools` — viewer/tool catalog (ocp-vscode, YACV, blendquery)
- `electronics-pcb-board-cad` *(separate plugin)* — PCB models that consume this skill for docs renders
- `electronics-pcb-components-cad` *(separate plugin)* — placed components, color-tagged
- pyvista docs: <https://docs.pyvista.org/>
- trimesh docs: <https://trimesh.org/>
- 3MF spec (color preservation): <https://3mf.io/specification/>
