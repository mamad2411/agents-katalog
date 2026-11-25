---
name: blender-clay-wireframe
description: Renders portfolio clay and wireframe passes in Blender without touching the scene's materials - a clay override through the view layer, a wireframe overlay (Cycles shader or Wireframe modifier for clean quads), and a triangle count for the caption. Use when a user wants a clay render, a wireframe render, a modeling breakdown, a topology showcase or a quick form check of a model.
license: MIT
metadata:
  author: JasmyLab Inc. (https://render.janction.jp)
  version: "0.1.0"
  related-skills: blender-lighting-recipes, blender-turntable, blender-product-shots
---

# Blender Clay and Wireframe Renders

Clay shows form, wireframe shows topology. Both are overrides on a copy of the scene: the user's materials stay
untouched, and turning the override off restores the original look.

## Clay (any engine)

`ViewLayer.material_override` replaces every material at render time without editing them.

```python
import bpy

def clay_material(color=(0.62, 0.62, 0.62), roughness=0.55):
    m = bpy.data.materials.get("JR_Clay") or bpy.data.materials.new("JR_Clay")
    try:
        m.use_nodes = True                      # older versions; newer ones always use nodes
    except AttributeError:
        pass
    bsdf = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    return m

bpy.context.view_layer.material_override = clay_material()
```

Clay colors that read well: light grey 0.6-0.7 (neutral), warm 0.75/0.65/0.55 (sculpt look), dark grey 0.2 against a
light background. Light it with a soft key and a rim (blender-lighting-recipes); clay needs contrast from light, not
from color.

The override hits everything with a material, including emissive light panels, glass and the backdrop. Exclude them by
moving them to a second view layer or by hiding them, and say in the caption what was hidden. The world (HDRI) is not
overridden.

## Wireframe over clay (Cycles)

The Wireframe shader node draws edges at render time. It shows the triangulated mesh, so quads appear split.

```python
def clay_wire_material(wire_px=1.0, wire_color=(0.05, 0.05, 0.05)):
    m = clay_material()
    nt = m.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    wire = nt.nodes.new("ShaderNodeWireframe")
    wire.use_pixel_size = True
    wire.inputs["Size"].default_value = wire_px
    line = nt.nodes.new("ShaderNodeBsdfDiffuse")
    line.inputs["Color"].default_value = (*wire_color, 1.0)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(wire.outputs["Fac"], mix.inputs["Fac"])
    nt.links.new(bsdf.outputs["BSDF"], mix.inputs[1])
    nt.links.new(line.outputs["BSDF"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    return m

bpy.context.scene.render.engine = "CYCLES"     # the Wireframe node is Cycles-only; ask before switching a user's scene
bpy.context.view_layer.material_override = clay_wire_material()
```

## Clean quad wireframe (any engine)

For a topology showcase where quads must stay quads, add a Wireframe modifier to a duplicate of each mesh and give
the duplicate a dark material. This adds real geometry, so it also works in EEVEE.

```python
dark = bpy.data.materials.new("JR_Wire")
try:
    dark.use_nodes = True
except AttributeError:
    pass
next(n for n in dark.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"].default_value = (0.03, 0.03, 0.03, 1.0)
for o in [o for o in bpy.context.scene.objects if o.type == "MESH"]:
    dup = o.copy()
    dup.data = o.data.copy()
    dup.name = o.name + "_wire"
    bpy.context.scene.collection.objects.link(dup)
    mod = dup.modifiers.new("Wire", "WIREFRAME")
    mod.thickness = 0.002 * max(o.dimensions)      # about 0.2 % of the object's size
    mod.use_replace = True
    mod.use_even_offset = True
    dup.data.materials.clear()
    dup.data.materials.append(dark)
```

With `material_override` set, the override also covers the wire copies; for this method, give the originals the clay
material on a copy of the scene instead of using the override, or render the wire copies on their own view layer.

## Triangle count for the caption

```python
dg = bpy.context.evaluated_depsgraph_get()
tris = 0
for o in bpy.context.scene.objects:
    if o.type == "MESH" and not o.name.endswith("_wire") and o.visible_get():
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        o.evaluated_get(dg).to_mesh_clear()
print(f"{tris:,} triangles")
```

Count after modifiers (subdivision changes the number a lot) and say which you report.

## Typical breakdown sheet

Beauty, clay, clay with wireframe, from the same camera and lights. Render all three at the same resolution and lay them
out side by side, or as a turntable each (blender-turntable). On JANCTION Render, send the clay or wireframe setup as part
of a bpy `scene_script` (or a copy of the .blend saved with the override) and preview it with `render_preview` like any
other scene.
