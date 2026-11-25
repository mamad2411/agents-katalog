# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Generate scenes (core pipeline, no Genesis needed)
python generate_table_bussing_scenes.py --num_trials 32 --output_dir outputs/my_scenes --seed 42

# Render a single trial (requires genesis-world)
python render_scene.py --scene_dir outputs/my_scenes --trial 0

# Render all trials
./run.sh 32 outputs/my_scenes 42

# Regenerate table config and robot obstacle mesh (requires genesis-world)
python export_scene_config.py --export_mesh
```

## Dependencies

```bash
# Core (generation only)
pip install numpy trimesh igl open3d scipy matplotlib

# Rendering and export
pip install genesis-world imageio
```

## Architecture

This is a table bussing scene generation pipeline for robot manipulation. It places objects on a digital twin table using grid-based collision detection.

### Module Dependency Graph

```
generate_table_bussing_scenes.py  ← main pipeline (standalone, no Genesis)
  └── table_bussing_config.py     ← object configs, mesh paths, constraint zones

render_scene.py                   ← multi-view Genesis renderer
  ├── export_scene_config.py      ← robot/table constants (ROBOT_URDF, TABLE_GLB, positions)
  └── table_bussing_config.py

export_scene_config.py            ← generates root.json + assets/marvin_obstacle.obj via Genesis
```

### 3-Phase Placement Pipeline (`generate_table_bussing_scenes.py`)

1. **Place containers** (bins + dish tray) in hardcoded `constraint_zone` regions
2. **Compute dynamic boundary** from placed containers: `max_x = min(bin edges)`, `max_y = min(tray edge)`
3. **Place remaining objects** within dynamic boundary, then place bread on top of teal_plate

### Grid System

- 3D occupancy voxel grid over table surface (0.01m resolution)
- Mesh→grid via `igl.signed_distance()` (SDF threshold 0.0025)
- Stable placement found via `scipy.signal.correlate` + convex hull stability check
- Robot obstacle mesh pre-occupies grid cells to prevent object-robot overlap

### Coordinate Conventions

- All coordinates in DT (Digital Twin) world space
- Rotation: Euler `[90, 0, z_rot]` degrees — 90° roll converts GLB y-up to z-up world
- Quaternions: `[w, x, y, z]` (Genesis convention)
- Grid index to world: `x = xmin + (i + 0.5) * resolution`

### Output Formats

- `all_scenes.npz` — `{obj_name}_positions` (N,3) and `{obj_name}_quaternions` (N,4) arrays
- `scene_info.json` — object names, configs, root info
- `schema/state-{idx:03d}.json` — SceneDescription-compatible JSON per trial
- `scaled_meshes/` — cached pre-scaled OBJ meshes (delete to regenerate after scale changes)

## Key Gotchas

- `Digital_twin_asset/` and `marvin_description/` contain Git LFS files — run `git lfs pull` if meshes are broken symlinks
- Generation uses pre-scaled OBJ meshes; rendering uses original GLB files (for colors)
- Schema JSON UUIDs are random and don't encode asset paths — gs-core can't resolve meshes from UUID alone (known TODO)
- Bread placement depends on `teal_plate` being placed first; falls back to table center if plate missing
- Environment variables `ROBOT_URDF` and `TABLE_GLB` override default paths in `export_scene_config.py`
- After changing object scales in `table_bussing_config.py`, delete `scaled_meshes/` to force regeneration
