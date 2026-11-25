---
name: 3d-blender-python-procedural-modeling
description: "Automate 3D geometry generation, UV unwrapping, PBR material assignment, and glTF asset export using the Blender Python (bpy) API."
category: 3d
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - 3d
  - blender
  - python
  - bpy
  - procedural
  - gltf
---

# Blender Python (bpy) Procedural Modeling and Asset Pipeline

## Overview & Core Principles
Automate 3D geometry generation, UV unwrapping, PBR material assignment, and glTF asset export using the Blender Python (bpy) API.

### Procedural Pipeline Invariants
1. **Context Management in Headless Mode**:
   - Run via CLI: `blender -b --python script.py`.
   - Ensure active object context is explicitly assigned (`bpy.context.view_layer.objects.active = obj`) before operator invocation.
2. **Mesh Topology Generation**:
```python
import bpy
import bmesh

def create_parametric_gear(teeth=16, radius=2.0):
    mesh = bpy.data.meshes.new("ParametricGear")
    obj = bpy.data.objects.new("ParametricGear", mesh)
    bpy.context.collection.objects.link(obj)
    
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, radius=radius, segments=teeth*2)
    bm.to_mesh(mesh)
    bm.free()
    return obj
```
3. **Export Standards**:
   - glTF 2.0 binary (`.glb`) format with Draco mesh compression.
   - PBR roughness/metallic packed into green/blue channels of metallicRoughness map.
