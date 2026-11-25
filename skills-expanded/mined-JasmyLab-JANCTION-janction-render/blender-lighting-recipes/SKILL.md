---
name: blender-lighting-recipes
description: Sets up lighting in Blender from recipes scaled to the subject's size - studio three-point, soft product light, HDRI, overcast, sunset and night - with starting values for power, size and placement. Use when a scene has no lights, renders too dark, flat or harsh, or when an agent must light a model it has just imported for product shots, a turntable or a portfolio still.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-product-shots, blender-turntable, blender-color-management
---

# Blender Lighting Recipes

Light relative to the subject, not in absolute numbers. A 10 cm cup and a 4 m car need the same setup at different
scales: measure the subject, then place lights at multiples of its size and scale power with distance squared.
All values below are starting points; preview and adjust exposure or power in steps of about 2x.

Do not add or replace lights in a user's lit scene without asking: lighting is part of the look.

## Measure the subject

```python
import bpy
from mathutils import Vector

def bounds(objs):
    pts = [o.matrix_world @ Vector(c) for o in objs if o.type in {"MESH", "CURVE", "FONT"} for c in o.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return (lo + hi) / 2, (hi - lo).length          # center, size (bounding diagonal, metres)

center, size = bounds(bpy.context.scene.objects)
```

## Studio three-point (products, characters, portfolio)

```python
import math

def area_light(name, power, sz, azimuth_deg, elevation_deg, dist, center):
    a, e = math.radians(azimuth_deg), math.radians(elevation_deg)
    loc = center + Vector((math.cos(e) * math.sin(a), -math.cos(e) * math.cos(a), math.sin(e))) * dist
    data = bpy.data.lights.new(name, "AREA")
    data.shape, data.size, data.energy = "DISK", sz, power
    obj = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (center - loc).to_track_quat("-Z", "Y").to_euler()
    return obj

d = 2.0 * size                              # distance: twice the subject size
scale = (d / 2.0) ** 2                      # power grows with distance squared
area_light("Key",  500 * scale, size,       -45, 35, d, center)
area_light("Fill", 150 * scale, size * 1.5,  60, 15, d, center)
area_light("Rim",  400 * scale, size * 0.5, 170, 45, d, center)
```

Ratios that read well: key : fill about 3 : 1 (more contrast for drama, less for catalog), rim at 60-100 % of the key
for a bright outline. Bigger light = softer shadows; size about equal to the subject for products.

## Recipes

| Recipe | Setup | Good for |
|---|---|---|
| Soft product box | Key as above with size 2x subject, fill from the front low, white world at 0.3-0.5 | Packshots, cosmetics, electronics |
| HDRI studio | World Environment Texture with a studio HDRI, strength 1; rotate with a Mapping node Z until the main highlight sits where you want it | Fast, natural reflections on metal and glass |
| Overcast | World color light grey 0.6-0.8, strength 1-2, no sun | Even, shadow-soft exteriors and models |
| Sunset | Sun lamp 3-5 W/m2 at 5-10 degrees elevation, warm (about 3000 K), angle 1-3 degrees; blue-ish world at 0.2-0.5 | Mood, long shadows |
| Night | Moon as a weak blue sun (0.05-0.2), practical lights (lamps, windows) as the main sources, exposure +1 to +2 | Interiors and streets at night |

```python
# HDRI world (pass an .hdr or .exr path you have)
w = bpy.context.scene.world or bpy.data.worlds.new("World")
bpy.context.scene.world = w
try:
    w.use_nodes = True                      # older versions; newer ones always use nodes
except AttributeError:
    pass
nt = w.node_tree
env = nt.nodes.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load("/path/to/studio.hdr")
nt.links.new(env.outputs["Color"], nt.nodes["Background"].inputs["Color"])
nt.nodes["Background"].inputs["Strength"].default_value = 1.0
```

Light color in Kelvin: a Blackbody node on the light's nodes in Cycles, or an RGB close to it (about 3000 K is
(1.0, 0.7, 0.4), 6500 K is white).

## Diagnose by symptom

| Symptom | Fix |
|---|---|
| One side black | Add fill or raise world strength; check normals face outward |
| Harsh, small shadows | Make the key larger or move it closer (softer), not brighter |
| Flat, no shape | Lower the fill; move the key further to the side (45-70 degrees) |
| Subject merges into background | Add or strengthen the rim; separate background brightness |
| Blown highlights | Lower power by half or exposure by 1 stop; check AgX is on (blender-color-management) |
| Fireflies near lights | Larger lights, no tiny bright emitters; see blender-render-settings |

On JANCTION Render, `environment="studio"` (or `sunset`, `overcast`, `night`) lights a scene without lights of its own,
and a preview with `environment="compare"` shows all four in one image so the user can pick.
