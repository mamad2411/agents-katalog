---
name: 3d-print-model-generator
description: Generate 3D printable STL models from parametric descriptions. Use for creating 3D models, STL files, mechanical parts, gears, brackets, enclosures, or any geometry for 3D printing. Supports primitives, functional objects, custom scripts, and PNG previews.
---

# 3D Print Model Generator

Generate STL files for 3D printing using parametric Python scripts. No CAD software required.

## Dependencies

```bash
sudo pip3 install numpy-stl trimesh
```

## Quick Start

### Generate a shape

```bash
python3 /home/ubuntu/skills/3d-print-model-generator/scripts/generate_model.py \
  --shape box --params '{"x":50,"y":30,"z":10}' --output model.stl
```

### Preview as PNG

```bash
python3 /home/ubuntu/skills/3d-print-model-generator/scripts/preview_model.py model.stl preview.png
```

### List all shapes

```bash
python3 /home/ubuntu/skills/3d-print-model-generator/scripts/generate_model.py --list
```

## Workflow

1. Clarify the user's model requirements (dimensions, shape, purpose)
2. Install dependencies if needed: `sudo pip3 install numpy-stl trimesh`
3. For simple shapes: use `--shape` with `--params` JSON
4. For complex models: write a custom script using the template, then run with `--script`
5. Generate PNG preview with `preview_model.py`
6. Deliver STL file and preview image to user

## Available Shapes

Primitives: `box`, `cube`, `cylinder`, `sphere`, `cone`, `torus`
Functional: `gear`, `pipe`/`tube`, `hex_nut`/`nut`, `thread`/`screw`, `bracket`, `washer`, `grid`

For full parameter details: read `references/shapes_reference.md`

## Custom Scripts

For complex multi-part models, copy and edit the template:

```bash
cp /home/ubuntu/skills/3d-print-model-generator/templates/custom_model_template.py model_script.py
```

Custom scripts must define `generate()` returning a numpy-stl Mesh. All shape functions and utilities (`_combine_meshes`, `_translate_mesh`, `_scale_mesh`, `_rotate_mesh_z`) are pre-injected.

Run with:
```bash
python3 /home/ubuntu/skills/3d-print-model-generator/scripts/generate_model.py \
  --script model_script.py --output model.stl
```

## Transforms (CLI)

Apply after generation: `--translate x,y,z`, `--scale factor`, `--rotate-z degrees`

## 3D Printing Guidelines

- All dimensions in millimeters (mm)
- Min wall thickness: 1.2mm (FDM), 0.8mm (SLA)
- Overhangs: keep below 45° or add supports
- Tolerances: 0.2mm FDM press-fit, 0.1mm SLA
- Orient strongest axis along Z (layer lines)
