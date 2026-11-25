---
name: blender-product-shots
description: Makes e-commerce and catalog product renders in Blender - camera framing from the model's size, 3/4 and turnaround angles, a shadow catcher with a transparent background, a seamless backdrop, studio light and accurate color - from a .blend or an imported glTF, FBX, USD or OBJ model. Use when a user wants product photos, packshots, listing images or marketing stills of a 3D model.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-lighting-recipes, blender-color-management, blender-turntable
---

# Blender Product Shots

A product shot sells the object: it fills the frame, its color is true, its edges are clean, and every angle is lit the
same. Frame from the model's real size, light it (blender-lighting-recipes), check color (blender-color-management).

## Standard set

| Shot | Camera | Notes |
|---|---|---|
| Hero 3/4 | 30-45 degrees to the side, 15-25 degrees above | The default listing image |
| Front, side, back | 0 / 90 / 180 / 270 degrees, 5-15 degrees above | Same distance and light for all |
| Top | 80-90 degrees above | Flat-lay products, packaging |
| Detail | Longer lens, close on a feature | Label, texture, connector |

Lens: 50-85 mm for most products, 85-135 mm for small items (less perspective distortion). Fill about 70-80 % of the
frame. Square 1440x1440 or 2000x2000 for marketplaces; 16:9 for banners.

## Frame the camera from the bounds

```python
import bpy, math
from mathutils import Vector

def frame_camera(objs, azimuth_deg=-35, elevation_deg=20, lens=70, fill=0.75):
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    center = sum(pts, Vector()) / len(pts)
    radius = max((p - center).length for p in pts)
    cam_data = bpy.data.cameras.new("CAM_Product")
    cam_data.lens = lens
    cam = bpy.data.objects.new("CAM_Product", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    r = bpy.context.scene.render
    aspect = (r.resolution_x * r.pixel_aspect_x) / (r.resolution_y * r.pixel_aspect_y)
    fov = 2 * math.atan(math.tan(cam_data.angle / 2) * min(aspect, 1 / aspect))   # the narrower side must fit
    dist = radius / math.sin(fov / 2)                   # far enough to see everything from any side
    a, e = math.radians(azimuth_deg), math.radians(elevation_deg)
    cam.location = center + Vector((math.cos(e) * math.sin(a), -math.cos(e) * math.cos(a), math.sin(e))) * dist
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    bpy.context.view_layer.update()
    # tight fit from this angle, then step back so the product fills about `fill` of the frame
    co, _ = cam.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), [v for p in pts for v in p])
    cam.location = center + (co - center) / fill
    cam_data.clip_end = max(cam_data.clip_end, dist * 4)
    return cam

product = [o for o in bpy.context.scene.objects if o.type == "MESH" and not o.name.startswith("Backdrop")]
frame_camera(product)
```

For the turnaround, rotate the azimuth (0, 90, 180, 270) and render each; keep lens, distance and lights identical.

## Transparent background with a real shadow (Cycles)

```python
s = bpy.context.scene
s.render.film_transparent = True
lowest = min((o.matrix_world @ Vector(c)).z for o in product for c in o.bound_box)
bpy.ops.mesh.primitive_plane_add(size=50, location=(0, 0, lowest))
floor = bpy.context.active_object
floor.name = "Backdrop_ShadowCatcher"
floor.is_shadow_catcher = True
s.render.image_settings.file_format = "PNG"
s.render.image_settings.color_mode = "RGBA"
```

The PNG keeps the contact shadow on transparent pixels, so the product can sit on any page color.

## Seamless backdrop (when the background must show)

A floor plane with its back edge extruded up and a large bevel (a "sweep") avoids a visible horizon. Use a neutral
material (base color 0.8 for white, 0.18 for mid grey, roughness 0.6-0.8). Keep the backdrop at least 3x the product size
so its edges stay out of frame.

## Color and edges

- Brand colors: compare against the swatch under AgX and under Standard or Khronos PBR Neutral; show the user, do not
  pick silently (blender-color-management).
- Clean silhouettes: pixel filter width 1.0-1.5 (`cycles.filter_width` in Cycles, `render.filter_size` in EEVEE) and
  enough samples that edges on transparency are not noisy.
- Labels and fine text: render the detail shot at the final resolution and zoom in; denoisers can smear small type.
- Glass and liquids: Cycles, transmission bounces 8 or more, and a backdrop or HDRI for the glass to refract.

## With JANCTION Render

`render_preview(scene_url=..., preset="product")` frames the model and renders 4 studio shots at 0/90/180/270 degrees
on a plain backdrop; the final gives 4 PNGs. `transparent=True` keeps the background transparent. With no model, find a
free one first: `asset_search("<item>")`. From a terminal: `uvx janction-render shots model.glb --transparent`.
