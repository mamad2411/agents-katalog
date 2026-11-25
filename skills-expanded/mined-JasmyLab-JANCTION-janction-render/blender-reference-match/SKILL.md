---
name: blender-reference-match
description: Matches a Blender render to a reference photo, concept art or an approved earlier render - aspect and camera first, then composition, light direction, exposure and white balance, then materials - with a side-by-side and numeric comparison loop. Use when a user attaches an image and says "make it look like this", when a client approved a frame and later renders must match it, or when a re-render drifted from the approved look.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-lighting-recipes, blender-color-management, blender-product-shots
---

# Blender Reference Match

Match in the order the eye notices: shape and camera, then light, then color, then surface. Fixing materials while the
camera is wrong wastes every render after it.

## 1. Read the reference before touching Blender

Write down, in one short list: aspect ratio and orientation; camera height (eye level, high, low) and where the horizon
sits; lens feel (wide with strong perspective, or long and flat); where the key light comes from (shadow direction and
softness); overall brightness and contrast; color temperature (warm, neutral, cool); background; what the subject is
made of. Say which of these you are guessing.

## 2. Camera and composition

- Set the render aspect to the reference's (`resolution_x / resolution_y`).
- Lens: strong converging lines mean 18-35 mm; little perspective means 85 mm and up. Start at 50 mm and adjust.
- Put the horizon at the same height in frame: raise or lower the camera, do not tilt it, unless the reference is tilted.
- Overlay the reference as a camera background image (viewport) or compare side by side after each preview.

```python
import bpy
cam = bpy.context.scene.camera
cam.data.show_background_images = True
bg = cam.data.background_images.new()
bg.image = bpy.data.images.load("/path/to/reference.jpg")
bg.alpha = 0.5
bg.display_depth = "FRONT"
```

The overlay shows in the viewport (and in viewport screenshots from a Blender MCP), not in final renders.

## 3. Light, then exposure, then white balance

Match the key light's direction from the shadows, then its softness from the shadow edges (blender-lighting-recipes).
Only then compare brightness and color numerically:

```python
# python compare.py reference.jpg render.png   (needs Pillow)
import sys
from PIL import Image, ImageStat
ref, ren = (Image.open(p).convert("RGB") for p in sys.argv[1:3])
ren = ren.resize(ref.size)
for name, img in (("reference", ref), ("render", ren)):
    r, g, b = ImageStat.Stat(img).mean
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    print(f"{name:9s} luma {luma:6.1f}  r/g {r / max(g, 1):.3f}  b/g {b / max(g, 1):.3f}")
w, h = ref.size
for label, box in (("top", (0, 0, w, h // 3)), ("middle", (0, h // 3, w, 2 * h // 3)), ("bottom", (0, 2 * h // 3, w, h))):
    a = ImageStat.Stat(ref.crop(box).convert("L")).mean[0]
    b2 = ImageStat.Stat(ren.crop(box).convert("L")).mean[0]
    print(f"{label:6s} reference {a:6.1f}  render {b2:6.1f}")
```

- Overall luma off by a constant ratio: change exposure (`view_settings.exposure`, 1 stop doubles brightness).
- One region off: that is light placement or a missing source, not exposure.
- r/g and b/g off: adjust light color or world color, not the materials. Warm reference: r/g above 1.05; cool: b/g above 1.05.
- Contrast off: a look (AgX contrast looks) or the fill-to-key ratio (blender-color-management).

## 4. Materials last

Compare the subject's highlights (sharp or broad: roughness), reflections (metallic or dielectric), and how much the base
color shows in shadow. Change roughness in steps of 0.1 and preview between steps.

## Loop and stop

Change one thing, preview, compare, note the result. Stop when the side by side reads the same at a glance and the numbers
are within about 5 % luma and 0.03 in the ratios, or when the user says it matches. Report what still differs: a
reference photo often has lens effects, grain or grading that a render will only match in compositing.

## Matching an approved render

When the reference is an approved frame of the same scene, keep the file versions (engine, Blender version, color
management, samples) the same and compare the new render with the approved one at the same frame and size. Any
difference you did not intend is a regression; find which change caused it before rendering more.

On JANCTION Render, preview the same frame with `render_preview` after each change and compare it with the reference as
above; `render_preview(variations=[...])` renders 2-8 variants of lighting (`environment`, `environment_strength`),
camera or object colors in one sheet, which is a quick way to try several candidates at once.
