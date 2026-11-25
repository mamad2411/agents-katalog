---
name: godot-procedural
description: Procedural generation in Godot 4.7 - seeded RandomNumberGenerator, FastNoiseLite terrain and biomes, TileMapLayer generation (cellular automata caves, BSP and random-walk dungeons, terrains), wave function collapse, Poisson-disc scattering, weighted loot tables, SurfaceTool/ArrayMesh heightmaps plus HeightMapShape3D, threaded chunk streaming. Use for random levels, terrain or runtime meshes.
license: MIT
compatibility: Godot 4.7+ (GDScript and C#).
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Procedural Generation (4.7)

## Rules that save you later
1. **Seed everything.** Use one `RandomNumberGenerator` per generator with an explicit `seed` (`rng.seed = hash("my seed")` for text seeds). Pass it down; never call global `randf()` inside generation. Show the seed in a debug overlay and save it with the game.
2. **Data first, nodes last.** Generate into arrays (`PackedInt32Array`, `Dictionary[Vector2i, int]`, `PackedFloat32Array`), validate, then write to TileMapLayer, GridMap or meshes in one pass.
3. **Validate and retry.** Flood-fill or path-check (`AStarGrid2D`) that the start reaches the exit, enforce min/max room counts, then retry with `seed + 1` on failure. Cap the retries.
4. **Threads build data; the main thread touches nodes.** Use `WorkerThreadPool.add_task()` for noise and mesh arrays, then `call_deferred` to add nodes or set meshes. See `godot-performance`.
5. Rebake navigation after the level exists (`godot-navigation-ai`).

## Randomness API
- `RandomNumberGenerator`: `seed`, `state` (save it to resume a sequence exactly), `randi_range`, `randf_range`, `randfn(mean, deviation)` (gaussian), `rand_weighted(PackedFloat32Array)` → index (weighted tables).
- Shuffle reproducibly: Fisher–Yates with your rng. `Array.shuffle()` and `pick_random()` use the **global** generator.
- Per-cell randomness without stored state: hash the coordinates, e.g. `hash(Vector3i(x, y, world_seed))`, which is stable across runs and machines.

## Noise (FastNoiseLite)
| Property | Meaning |
|---|---|
| `noise_type` | `TYPE_SIMPLEX_SMOOTH` (default, terrain), `TYPE_PERLIN`, `TYPE_CELLULAR` (Voronoi: biomes, cracks), `TYPE_VALUE` |
| `seed`, `frequency` | lower frequency = larger features (0.005–0.02 for world maps in tile units) |
| `fractal_type`, `fractal_octaves`, `fractal_lacunarity`, `fractal_gain` | detail layers (FBM, 3–6 octaves) |
| `domain_warp_enabled` + `domain_warp_*` | organic, swirly coastlines |
- `get_noise_2d(x, y)`/`get_noise_3d` return roughly −1..1. Remap with `remap()` or `(n + 1) * 0.5`. Batch with `get_image(w, h)` when you need a whole texture.
- Biomes: combine two noises (height + moisture, or temperature) and threshold them into a lookup table. Use a different `seed` for each noise.
- Shaders and editor previews: `NoiseTexture2D` (`noise`, `seamless`, `as_normal_map`, `color_ramp`). It generates on a thread, so `await texture.changed` before reading its image.

## 2D tile generation
| Technique | Good for |
|---|---|
| Noise thresholds | overworlds, islands, biomes |
| Cellular automata (4–5 smoothing passes, wall if ≥5 of 8 neighbors are walls) | caves |
| Random walk / drunkard's walk | organic tunnels, guaranteed connectivity |
| BSP split + rooms + L-shaped corridors | classic roguelike dungeons |
| Room templates (prefab scenes/patterns stitched on a grid) | Spelunky-style designed variety |
| Wave function collapse | tile-adjacency puzzles, towns. Use the "Wave Function Collapse (WFC)" addon by AlexeyBond (TileMapLayer and GridMap) |
- Writing: `set_cell(coords, source_id, atlas_coords)`. For autotiling, collect cells per terrain and call `set_cells_terrain_connect(cells, terrain_set, terrain)` **once per terrain**. It's slow for big maps, so generate per chunk or use direct atlas coords.
- `TileMapLayer.set_pattern()` stamps prefab rooms saved as `TileMapPattern`s.
- Big maps: chunk them (e.g. 32×32) and generate around the camera. Clear far chunks with `erase_cell`.

## 3D generation
- **Heightmap terrain**: a grid of vertices from noise → `SurfaceTool` (`set_uv`, `add_vertex`, `index()`, `generate_normals()`, `generate_tangents()` for normal maps) → `commit()`. Collision: `HeightMapShape3D` (`map_width`, `map_depth`, `map_data`), which is much cheaper than a trimesh. Scale the CollisionShape3D to match the grid spacing.
- **Fast path**: fill `PackedVector3Array`/`PackedInt32Array` yourself and call `ArrayMesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, arrays)`. It's several times faster than SurfaceTool for large meshes.
- Edit existing meshes with `MeshDataTool`. Debug lines and gizmos: `ImmediateMesh`.
- **Scatter** (trees, rocks, grass): Poisson-disc points → `MultiMeshInstance3D` (one draw call). Set `instance_count` after `transform_format` and `mesh`. Raycast down or sample the heightmap for Y.
- **Modular dungeons in 3D**: generate on a 2D grid, then place GridMap items or instantiate room scenes at `Vector3(x, 0, y) * cell_size` (`godot-3d-gameplay`).
- Large terrain with sculpting and LOD: the Terrain3D addon (`godot-addons`).

## Loot, names, encounters
- Weighted tables as a `Resource` (`entries: Array[LootEntry]` with `weight`) so designers edit them in the inspector. Roll with `rng.rand_weighted(weights)`.
- Pity timers and "bags" (shuffle a list of outcomes and draw until it's empty) feel fairer than pure randomness.
- Markov chains or syllable tables for names. Keep the generated strings out of translation files.

Seeded noise maps, caves, BSP dungeon, Poisson disc, loot table, heightmap terrain and threaded chunks (compiled by the tests): [references/patterns.md](references/patterns.md)
