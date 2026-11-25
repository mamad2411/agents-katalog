---
name: blender-color-management
description: Handles Blender color management for renders - view transform (AgX, Filmic, Standard, Khronos PBR Neutral), looks, exposure, output formats and color spaces of textures - so renders are not washed out, clipped or off-color. Use when a render looks grey, flat, too contrasty or the wrong color, when product colors must match a brand, or when exporting EXR, PNG or video.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-render-settings, blender-product-shots, blender-reference-match
---

# Blender Color Management

Most "washed out" and "too dark" complaints are color management, not lighting. Read the settings first, change one
thing, preview again. Changing the view transform of a user's existing scene changes its look: ask first.

## Read the current state

```python
import bpy
s = bpy.context.scene
vs = s.view_settings
print(s.display_settings.display_device, vs.view_transform, vs.look, vs.exposure, vs.gamma,
      s.sequencer_colorspace_settings.name)
```

## Which view transform

| View transform | Use for | Watch out |
|---|---|---|
| AgX (default since Blender 4.0) | Photoreal and most lit scenes; bright lights roll off without hue skew | Looks flatter than Standard; saturated brand colors desaturate in highlights |
| Filmic (older default) | Scenes made in Blender 2.8-3.6 that were tuned under it | Keep it for those scenes; do not "upgrade" to AgX without asking |
| Standard | UI graphics, flat shading, logos, when a hex color must come out as that hex | Highlights clip hard; lit scenes look harsh |
| Khronos PBR Neutral (4.2 and later) | Product renders where base colors should stay close to the swatch | Less highlight range than AgX |

Looks add contrast on top of a view transform. In Python the AgX looks carry the view name in some versions
("AgX - Punchy") and not in others, so set them defensively:

```python
def set_look(name):
    vs = bpy.context.scene.view_settings
    for candidate in (f"{vs.view_transform} - {name}", name):
        try:
            vs.look = candidate
            return candidate
        except TypeError:
            pass
    return None
```

## Exposure before lights

`view_settings.exposure` is in stops (+1 = twice as bright). If a well-lit scene is uniformly too dark or too bright,
change exposure by 0.25-1 stop instead of re-lighting. If only parts are wrong (one side black, highlights clipped),
it is lighting: see blender-lighting-recipes.

## Textures in the right color space

Color maps (base color, albedo): sRGB. Data maps (normal, roughness, metallic, height, masks): Non-Color. A normal map
left on sRGB gives wrong shading; a roughness map on sRGB makes surfaces too glossy or too matte.

```python
for img in bpy.data.images:
    n = img.name.lower()
    if any(k in n for k in ("normal", "nrm", "rough", "metal", "height", "disp", "ao", "mask")):
        print("check", img.name, img.colorspace_settings.name)   # should be Non-Color
```

Print first and fix after checking: names are a hint, not proof.

## Output formats

| Need | Format | Notes |
|---|---|---|
| Web, previews, e-commerce | PNG 8-bit (RGBA for transparency) | The view transform is baked in |
| Compositing, grading later | OpenEXR (half float, multilayer for passes) | Scene-linear data; the view transform is not baked in |
| Video delivery | Frames first, then encode H.264 `yuv420p` | Encode from PNG frames so a crash does not lose the whole video |

## Diagnose by symptom

| Symptom | Likely cause | First check |
|---|---|---|
| Grey and flat | AgX or Filmic on a scene tuned for Standard, or no contrast look | `view_transform`, `look` |
| Logo color off by a shade | AgX desaturating near white | Try Standard or Khronos PBR Neutral on a copy and show both |
| Everything too dark | Exposure, or lights in the wrong units after an import | `exposure`; light power vs scene scale |
| Pastel textures, wrong normals | Data maps tagged sRGB | Texture color spaces above |
| Video darker than the frames | Player or encoder range | Encode with `yuv420p` and compare frame 1 of both |

On JANCTION Render the scene's own color management is kept. To show the user AgX against Standard, render two cheap
previews of the same frame (the second from a copy whose script sets `view_transform`) and put them side by side before
changing anything.
