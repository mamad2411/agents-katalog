---
name: genex-threejs-open-world
description: Build a big explorable world that stays fast — seeded heightfield terrain with chunk streaming, biomes, points of interest, instanced scatter, and honest world bounds. Use when the ask says big or open world, multiple regions or locations, exploration, or any map beyond one arena — before the first terrain code, instead of one flat plane with fog.
---

# Genex Three.js Open World

"Big world" in a request is a size class, not a mood. A 300 m plane with fog
pulled in to hide the walls is an arena wearing a costume — the player finds
the invisible wall in the first two minutes, and no amount of dressing
survives that. This skill is the recipe for a world that is actually big —
kilometers-class, streamed, varied — at a cost one session can afford.

## Decide the scale first, as a number

Put the world's size in the plan (and in the content contract's `world:` line
when `$genex-threejs-game-content` is loaded — a big world exists to hold
content, so the two skills almost always load together):

- **One arena** (~100–300 m): only when the ask says so (a shooter map, a
  sports pitch, a boss rush). Never the silent fallback for "big world".
- **A district** (~500 m – 1 km): a town + surroundings; streaming optional.
- **Open world** (2–4 km bounded): the default meaning of "big/open world" —
  a dozen locations, real travel time between them, streamed terrain. Beyond
  ~4 km you're spending budget on emptiness; density beats acreage.

Bound the world honestly: an edge-mountain ring, a coastline, or a cliff
reads as "the world ends here" — an invisible wall on a flat horizon reads as
a bug. Fog is atmosphere and draw-distance management
(`$genex-threejs-atmosphere-aerial-perspective` for the real thing), never a
wall to hide how small the map is.

## The scaling law: procedural fabric, generated landmarks

The single decision that determines whether a big world is affordable:

- **The world's FABRIC is procedural** — a seeded heightfield, instanced
  vegetation, scattered rocks and props built from primitives and the
  procedural skills (`$genex-threejs-procedural-vegetation`,
  `$genex-threejs-procedural-geometry`). Procedural fabric costs the same at
  4 km as at 300 m; that is what makes the size class reachable.
- **Generated assets are LANDMARKS** — `npx genex model` set pieces placed at
  points of interest (the village well, the boss lair gate, the shrine), a
  ground texture (`npx genex texture --terrain`, UVs from `worldUV` — never a
  hand-picked repeat), a skybox. Hero assets decorate the world's landmarks;
  they never decide the world's size, because a world assembled from
  hand-placed generated meshes caps out at a diorama.

Wire generated pieces in as upgrades over procedural placeholders (the
standard swap discipline), so the world is walkable at full size from the
first hour.

## One height function to rule everything

Terrain is a seeded fBm heightfield (`$genex-threejs-procedural-fields` owns
the noise craft) with ridges for drama, an edge-mountain ring for the bound,
and **flattened pads blended in around each location** so structures sit on
level ground. The load-bearing rule: **exactly one canonical
`getHeightAt(x, z)`** that chunk meshing, physics grounding, placement
scatter, NPC spawns, and the minimap all share. The moment a second height
formula exists, trees float and feet sink — every large-world bug report
starts there.

Full copy-paste module — noise, fBm, location flattening, chunk manager,
instanced scatter — in
[references/terrain-streaming.md](references/terrain-streaming.md).

## Stream chunks, budget the frame

Build the terrain as fixed-size chunks (128 m is a good default) around the
player: load radius ~5 chunks (~600 m view with fog), unload behind, and
build queued chunks inside a **per-frame time budget** (a few ms) so streaming
never hitches the game. Seam rule: compute normals with a one-vertex apron
into the neighbor chunk, or every chunk border shows as a lighting crease.
Far distance is fog + the skybox — a low-res far ring is an upgrade, not a
requirement.

Physics grounding: keep the character/vehicle on the ground via the canonical
`getHeightAt` (cheap, always loaded) or per-chunk Rapier heightfield
colliders (`$genex-threejs-physics-rapier`) when projectiles and ragdolls
need real collision — but never build colliders for chunks the player isn't
near.

## Biomes: variety from two noise fields

Two low-frequency noise fields (temperature, moisture) + altitude + slope
give 4–7 biomes from one lookup: meadow, forest, marsh, desert, alpine, snow.
The biome function drives everything downstream from ONE place — vertex
colors or texture blend, vegetation species and density
(`$genex-threejs-procedural-vegetation`, instanced), enemy spawn tables and
ambient audio per biome (that's the content hookup). "Different locations" in
an ask is only half-answered by placed structures; the other half is the
ground itself changing as you travel.

## Points of interest: the world's content skeleton

A data table of locations — id, name, position, radius, builder function —
is the spine the content contract hangs from (quest givers live somewhere;
"locations: 8" means eight entries here):

- **Density beats acreage:** a point of interest every ~300–500 m of travel
  on the natural routes. A 4 km world with three POIs is emptier than a 1 km
  world with eight.
- Each location: terrain pad flattened (blend into the heightfield — see the
  reference), a hand-authored builder (walls, tents, standing stones — merged
  primitive geometry + generated landmark pieces), spawns, loot, and its
  compass/minimap marker.
- Light budget: point lights per location, hard cap world-wide (~6 active) —
  swap distant ones for emissive materials (`$genex-threejs-lighting-design`
  owns the walk).
- Roads or worn paths between major POIs guide travel and double as the
  navigation answer ("follow the road north beats a quest arrow").

## Performance floors (the size class depends on them)

- **Instancing for everything repeated**: trees, grass, rocks are
  `InstancedMesh` per chunk — thousands of draw calls is the classic
  big-world death; hundreds is the target.
- **Merge static location geometry** per material into a handful of meshes.
- Shadows at scale need a strategy, not defaults: a tight shadow camera
  following the player, or cascades — `$genex-threejs-shadow-systems`.
- Keep per-frame allocation out of the loop (reuse vectors), and keep chunk
  building inside its time budget.
- Phone-survivable stays the bar: pixel ratio cap, texture ≤ 2048², and the
  chunk radius is the quality knob to shrink first.

## Day/night: cheap and almost expected

A big explorable world reads twice as alive with a sun cycle: one animated
`DirectionalLight` angle + a palette lerp (sky, fog, ambient) + practical
lights that matter at night. It's ~50 lines against the lighting rig
(`$genex-threejs-lighting-design`), and it makes travel time feel like time.
Optional — but when the ask says "like the big RPGs", this is one of the
three things they mean.

## Failure modes to catch

- A flat plane with invisible walls and close fog shipped as "big world" —
  the defining failure this skill exists to prevent.
- Two height functions (mesh vs physics vs placement) drifting apart —
  floating trees, buried chests.
- Hand-placing every tree at world scale — placement must be seeded scatter
  with biome rules, or the world stays empty.
- Per-chunk geometry that never unloads or shares materials — memory climbs,
  draw calls explode.
- POIs as map dots only — a named location with nothing to do fails the
  content contract it was meant to serve (`$genex-threejs-game-content`).
- Seams: normal creases at every chunk border (missing apron), or texture
  tiling picked by eye instead of `worldUV` (`$genex-ai-texture`).
