---
name: mesh-utils
description: Use when the user asks to inspect, convert, clean, or validate mesh/3D scene files (OBJ, STL, GLB, FBX, USD) via trimesh, PyMeshLab, or pxr. Routes to extensions/mesh-utils/meshops.py. Lightweight stdlib CLI; deps are pip-installed only when needed.
---

# Mesh Utilities

`extensions/mesh-utils/meshops.py` is a small JSON-on-stdout CLI that
dispatches to whichever of **trimesh**, **PyMeshLab**, or **OpenUSD
(`pxr`)** is installed. Use it for quick inspection/conversion/cleanup
of assets produced by `ai3d-gen`, external files, or Blender exports.

## Commands

```bash
python extensions/mesh-utils/meshops.py doctor          # which deps are present
python extensions/mesh-utils/meshops.py info file.glb   # verts, faces, bounds, watertight
python extensions/mesh-utils/meshops.py convert in.obj out.glb
python extensions/mesh-utils/meshops.py clean in.ply out_clean.ply
```

All output JSON; missing dependency -> `{"ok": false, "hint": "pip
install ..."}` so the user can install explicitly.

## Backend selection

| Format / task | Engine chosen |
|---|---|
| `.usd/.usda/.usdc/.usdz` | `pxr` (Usd.Stage introspection) |
| OBJ/STL/GLB/PLY/FBX (info/convert/clean) | `trimesh` if present, else `pymeshlab` |

`pxr` doesn't do mesh repair; for USD -> repair, convert via
`trimesh`/`pymeshlab` first.

## When to use what

- **trimesh**: pure-Python, covers 90% of ops (load/export, basic
  cleaning, bounds, watertight check). `pip install trimesh`.
- **pymeshlab**: richer repair filters (remeshing, decimation,
  self-intersection). `pip install pymeshlab`. Chosen automatically if
  it's the only backend.
- **pxr (usd-core)**: read-only here; used to inspect USD scenes
  (prims, meshes, up-axis). `pip install usd-core`.
- **open3d**: probed by `doctor` but not yet wired; point-cloud ops can
  be added later.

## Boundaries

- Never auto-install. Emit the hint, let the user run it.
- `clean` supports trimesh/pymeshlab only; USD stages -> convert first.
- For heavy geometry work (boolean, sculpt, unwrap) use
  `operate-blender` instead; mesh-utils is the fast path.
