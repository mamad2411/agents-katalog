---
name: game-dev-modeling
description: >-
  Make 3D models for a game with any coding agent, and get them into the engine within its limits.
  Works in the person's open Blender through the official Blender Lab MCP add-on (look at the
  viewport after every stage, the person can edit between steps, the .blend is the source), with the
  craft routed to el4cteo/blender-skills (UVs, materials, rigs, the asset-qa gate, Roblox export
  presets); headless Blender only as the fallback. Exports FBX for Roblox or GLB for the web and
  checks the file against the engine's limits with `mesh_check.py` before import. Meshy AI generation is an opt-in route, off unless the user says
  they have the Meshy CLI. Use WHENEVER the work is "3D model", "make a prop / asset / character
  model", "Blender", "bpy", "low poly", "polycount", "triangle budget", "environment", "level", "modular kit",
  "set dressing", "art style", "shading", "bake", "geometry nodes", "export FBX / GLB / glTF",
  "import a mesh into Roblox", "MeshPart", "too many triangles", "texture size", "Meshy",
  "open Blender", "live Blender", "Blender MCP", "work in Blender", "blender-skills",
  "text to 3D", "image to 3D", "โมเดล 3D", "ปั้นโมเดล".
---

# Modeling for games

Adapted from four MIT projects: [blender-skills](https://github.com/el4cteo/blender-skills/tree/9e7e04a)
(the Blender craft layer, section 3), [meshy-3d-agent](https://github.com/meshy-dev/meshy-3d-agent)
(AI generation through the Meshy CLI), [Blender Agent Studio](https://github.com/ifBars/blender-agent-studio)
(scripted Blender work with checked renders), and [blender-claude-plugin](https://github.com/ra100/blender-claude-plugin)
(bpy references and the Blender Lab MCP setup). Install either Blender plugin for its deeper
per-topic references; this file is the route and the game-engine handoff.

## 0. Decide the route (ask once)

| Route | When | Cost | Default |
|---|---|---|---|
| **Blender, scripted** | props, buildings, modular kits, stylised or low-poly assets | free, local | **yes** |
| **Meshy** (AI generation) | an organic shape or a character from a picture or a line of text | paid credits, cloud | **off** |
| **Existing file** | the user has a model already | free | when a file is given |

**Meshy is off by default.** Before the first model, ask once: "Do you have the Meshy CLI set up
(a Meshy account and `meshy` installed)? If not, I'll build it in Blender." Then:

- **No, or no answer:** do not use Meshy, and do not install `meshy-cli` or suggest signing up.
  Do not ask again in this project. Go back to Meshy only when the user brings it up.
- **Yes:** run `meshy --version` and `meshy auth status --format json --no-update-check`. Only a
  verified session counts. Then follow [Meshy rules](#meshy-only-when-opted-in) below. Meshy's own
  skill installs its CLI without asking; that step does not apply here.

## 1. Know what the model is for

Before building, write down: the engine (Roblox, web, other), what it is (prop, building,
character to rig), its size in the game (Roblox studs, metres), the triangle budget, and the
style. For Roblox the hard limits are in [section 5](#5-engine-limits). A character to rig needs a
T- or A-pose and clean topology; a prop does not.

## 2. References first

Before building, collect 6 to 12 references and write them down in `references.md` beside the
build script: link, author, licence, polygon count, and **what each one gives** (a proportion, a
budget, a way to do fur or colour).

- **Sketchfab** is measurable: `https://api.sketchfab.com/v3/search?type=models&q=<terms>&max_face_count=<n>`
  and `.../v3/models/<uid>` return face counts, licences and thumbnails without a login.
- **Pinterest and image boards** are mood only: rights unknown, nothing copied, no image committed.
- **Not a copy:** no existing game's or brand's character, even when it shows up in the search.
- Put your renders next to the closest references before calling the model done.

## 3. Blender (default route): work in the open Blender

The model is made **in Blender**, not only in a script run blind: the agent drives the person's open
Blender, looks at the viewport after every stage, and the person can grab the mouse and change
anything between steps. Background Blender is the fallback when no window is open (CI, a server, an
agent without MCP).

**Check Blender first:** `blender --version` (macOS: `/Applications/Blender.app/Contents/MacOS/Blender`).
Not installed: say so (blender.org/download, free) and stop the Blender steps.

**The craft comes from [blender-skills](https://github.com/el4cteo/blender-skills/tree/9e7e04a)**
(el4cteo, MIT, pinned at `9e7e04a`, verified on Blender 5.3): 28 skills, each with tested scripts that
run the same way live (import, then `run()`) or headless. Install it for any agent with its installer
(`install/install.sh --agent claude|codex|gemini|cursor|all`; Claude Code: `/plugin marketplace add
EL4CTEO/blender-skills`). This file keeps only what a game needs on top: the route, the budget, the
engine's limits and the handoff.

| Stage | blender-skills skill | What to run |
|---|---|---|
| First call, the 5.x API rules | `blender-core` | `env_report.run()`; its rules (data API over operators, nodes by type, no default names) |
| Hard surfaces, bevels, booleans | `blender-hardsurface-modeling` | `apply_stack.py` |
| UVs | `blender-retopology-uv` | `uv_pack.run(method="smart", res=1024)` |
| Materials, textures, bakes | `blender-pbr-materials`, `blender-texturing`, `blender-texture-baking` | then this skill's [shading](references/shading.md) and [texturing](references/texturing.md) for game palettes |
| Kits, terrain, scatter | `blender-environment-kits`, `blender-geometry-nodes` | then [environment](references/environment.md) |
| Rigs, animation | `blender-character-rigging`, `blender-animation` | `rig_check.py --profile roblox`; then [rigging](references/rigging.md) |
| Budget | `blender-game-optimization` | `mesh_stats.run(budget="roblox")` |
| **The gate** before export | `blender-asset-qa` | `qa_check.run(objects=[...], profile="roblox")` must pass |
| Export | `blender-export-pipelines` | `export_asset.run(preset="roblox")` (FBX) or `"roblox_gltf"`; its `references/roblox.md` |
| A whole asset | `blender-workflow-recipes` | recipe 4 (Roblox) |

### The live session

**Blender Lab MCP** (official; Blender 5.1+, v1.0.3, 2026-09-11) is a Blender add-on that listens on
`localhost:9876` while Blender is open with a window, plus a `blender-mcp` server for any stdio MCP
client. It runs agent-written Python in the person's Blender **with no sandbox**: say so and ask
before wiring it up. Setup, checked on Blender 5.3.0 (projects.blender.org/lab/blender_mcp/releases):

- Add-on: `blender --command extension install-file -r user_default -e mcp-1.0.3.zip`, enable it,
  and turn on Preferences → System → Allow Online Access (or start Blender with `--online-mode`).
- Server: unzip `blender-1.0.3.mcpb` and register `uv run --directory <unzipped> blender-mcp` with the
  agent (Claude Code: `claude mcp add`; Codex, Cursor, Gemini: their MCP config). `BLENDER_PATH`
  names Blender for its background tools.
- Its 26 tools (v1.0.3, listed from the server): live ones run in the open Blender:
  `execute_blender_code` (assign a dict to `result` to get data back), `get_objects_summary`,
  `get_object_detail_summary`, `render_viewport_to_path` (the look after each stage),
  `get_screenshot_of_area_as_image` / `_of_window_as_image`, `jump_to_view3d_object_by_name`;
  `search_api_docs` and `get_python_api_docs` read Blender's API docs. The `*_for_cli` twins work on
  a temporary copy of a `.blend` in background Blender. Tools added mid-session appear after the
  agent reconnects its MCP servers (Claude Code: `/mcp` or a new session).
- No MCP client yet: the add-on speaks null-byte-delimited JSON on port 9876,
  `{"type": "execute", "code": "...", "strict_json": false}` → `{"status", "result", "stdout"}`,
  so any shell can drive it (the worked example did).

How to work in it:

0. **References before step 1.** Section 2's `references.md` comes first in a live session too: the
   game's own look, then 6-12 measured references. The dungeon key skipped it and had to collect
   them afterwards.
1. **A scene or file of its own.** The session is the person's work: never reset it, never delete what
   you didn't make (blender-core's rule). Start a new scene or file for the asset.
2. **Small steps, each one sent and saved.** One stage per call (blockout, join, finish, clean, UV,
   export), each saved as `steps/NN_<stage>.py` as it is sent. The steps are the record; they replay
   headless.
3. **Look after every stage.** `render_viewport_to_path`, or `render.opengl` with the 3D View's context
   (no UI or popups on top: a splash screen covers a window screenshot), in material and wireframe
   shading.
   A number never replaces a look.
4. **Read the scene before each step.** The person may have moved, renamed or edited something
   between calls: query the objects, never assume the last step's state.
5. **Keep it non-destructive** while the person may still tune it: modifiers stay live in the stack;
   the export applies them.
6. **The `.blend` is the source.** Save it beside the exports (`save_as_mainfile(copy=True)` in a live
   session). The next person opens the file, not a rebuild script.

### Headless (no window)

`python <blender-skills>/blender-core/scripts/run_in_blender.py --blend in.blend <script.py> -- …`
runs any blender-skills script in background Blender and prints only its JSON; plain
`blender -b --python build_<asset>.py` works for a script of your own. The older examples
(`lowpoly-cat`, `wizard-cat`, `crystal-ground`, `wizard-glade`) were built this way and still rebuild
from their scripts.

Rules, whichever way:

- **The `.blend` is the source**, with `steps/` (live) or `build_<asset>.py` (headless) beside it as
  the record of how it was made.
- **Work in stages:** blockout at true scale → primary forms → secondary detail → materials →
  cleanup → export. Check proportions at the blockout, not at the end.
- **Look at it** after every stage (live: the viewport; headless: blender-skills' `review_shots.py`
  contact sheets) and before calling it done. A look shows the shape, not the topology: the
  asset-qa gate and section 5's checks cover that.
- **Colour and textures:** read [`references/texturing.md`](references/texturing.md) first. Low-poly
  work uses one material over a small palette texture (power of two), not a material per colour.
- **Materials that must leave Blender:** read [`references/shading.md`](references/shading.md) first. No engine reads a procedural node tree: build the look with nodes, bake it to a power-of-two image, export one Principled material over that image.
- **Scatter, repeats, variants from a seed:** read [`references/geometry-nodes.md`](references/geometry-nodes.md) first. Realize Instances, apply the modifier, cap the count, and count triangles after realizing. `examples/crystal-ground/build_crystal_ground.py` is the worked case for both.
- **Bones and animation:** read [`references/rigging.md`](references/rigging.md) first. A segmented low-poly model is joined into one mesh and weighted part by part; `examples/wizard-cat/rig_wizard_cat.py` is the worked case.
- **Scenes and levels:** read [`references/environment.md`](references/environment.md) first. A scene is a kit: each unique piece is built once, exported once (`kit/<Piece>.fbx`) and placed from a layout table, so Roblox uploads it once and instances the copies. `examples/wizard-glade/build_wizard_glade.py` is the worked case.
- **The house look:** read [`references/art-theme.md`](references/art-theme.md) before modelling anything that stands next to the wizard cat: the palette cells, the value and saturation rules, the size ladder in studs, and the triangle budget per asset class.
- **Modifiers stay live, the export applies them** (`use_mesh_modifiers`). Booleans leave n-gons,
  duplicate verts and back-to-back faces: the asset-qa gate finds them; triangulate only the n-gons.

## 4. Export

Live: blender-skills' `export_asset.run(preset="roblox", objects=[...], out=...)` (FBX) and
`preset="roblox_gltf"` (GLB, for `mesh_check.py`). For the GLB pass
`set=["use_active_scene=True"]`: the glTF exporter walks every scene, and another scene's selected
object leaks into the file (the worked example's GLB carried the startup Cube until this was set).

Headless, with this skill's own script:

```bash
blender -b art/rock/rock.blend --python scripts/blender_export.py -- --target roblox --out build/rock.fbx --dry-run
blender -b art/rock/rock.blend --python scripts/blender_export.py -- --target roblox --out build/rock.fbx
```

`--target roblox` applies scale and rotation, then writes FBX with Roblox's documented settings
(Path Mode Copy, Embed Textures, FBX Unit Scale, no leaf bones, no baked animation unless
`--animation`). `--target web` writes a GLB. `--dry-run` prints triangles, n-gons and whether
transforms were applied, and writes nothing. Checked on Blender 5.3.0: the cat example's FBX
re-imports with every scale 1 and the same triangle count.

## 5. Engine limits

Check the file before importing it:

```bash
python scripts/mesh_check.py build/rock.glb --target roblox      # exit 1 = over a limit
python scripts/mesh_check.py build/level.glb --target web --max-total 150000
```

It reads GLB, glTF and OBJ. For an FBX, export a GLB beside it and check that.

**Roblox** (create.roblox.com/docs/art/modeling, read 2026-11-16):

| Rule | Value |
|---|---|
| Triangles | at most **20,000 per mesh**; split a bigger model into parts |
| Geometry | watertight, no exposed backfaces, quads where possible (no n-gons), no zero-thickness faces |
| Import formats | `.fbx` (meshes, hierarchy, PBR textures, rigs, animation), `.gltf`, `.obj` (single simple mesh) |
| Textures | `.png`, `.jpg`, `.tga`, `.bmp`; about 256 px for a 5-stud object, 512 for 10, 1024 for 20. The page also states 4096 px support but 1024 for PBR maps: stay at 1024 unless checked |
| Normal maps | OpenGL, tangent space |
| Rigs | bones with scale 1 and rotation 0, root at the origin, at most 4 bone influences per vertex, no influence on the root |
| Avatar items | their own specs (character bodies, accessories): read those pages instead |

**Web (three.js and friends):** GLB. No fixed limit; agree a budget for the whole scene with the
user and pass it as `--max-total`.

Then import (Roblox: Studio → 3D Importer), and look at it in the engine. With Studio's MCP server
connected, `screen_capture` after `insert_asset` or the import shows it in place.

## 6. Bench

The four worked cases, with their prompts, every version and what caught each fault, are in
[`examples/README.md`](examples/README.md): start there for a new asset of the same kind.

A case in `benchmarks/*.toon` holds the prompt as typed, the budget and a rubric;
`scripts/bench_model.py` scores a built model against it (exit code = failed checks):

```bash
blender -b --factory-startup --python examples/lowpoly-cat/build_cat.py -- --out examples/lowpoly-cat
python scripts/bench_model.py benchmarks/lowpoly-furry-cat.toon examples/lowpoly-cat/cat.glb
```

Checks: triangle budget, the engine's limits, every mesh closed (edges welded by position, each
shared by two triangles), named parts, modelled fur, the build script beside the model, and four
renders. Whether it *looks* like the prompt is the `manual` `look` row: score it with
[`references/visual-review.md`](references/visual-review.md), a fresh reviewer on a fixed 0–10
scale with evidence per view, never the builder's own eye.

Worked case, "Create an cat furry charactor which lowest polygon" (`examples/lowpoly-cat/`):
**128 triangles** in 19 closed parts, one material, 9/9. How it got there:

| Build | Triangles | What changed |
|---|---|---|
| v1 | 168 | first pass from the prompt alone |
| v1.1 | 148 | renders showed a belly hidden inside the body (20 triangles for nothing) and a floating chest tuft |
| v3 | 128 | after the reference board (`references.md`): character proportions, muzzle and belly as face colours instead of shapes, bigger eyes |
| v4 | 128 | after `references/texturing.md`: one material over a 16 px palette texture instead of four materials |
| wizard | 200 | the follow-up "output is need wizard cat": `examples/wizard-cat/` dresses the same cat (hat, cape, crystal), 9/9 on its own case |

A second case, `benchmarks/crystal-ground.toon` (`examples/crystal-ground/`): a tile for the cat to
stand on, crystals and rocks scattered by Geometry Nodes from a seed, procedural materials baked
to a 256 px colour map and a 128 px emission map. **498 triangles** in 3 closed parts, one
material, 8/8.

| Build | Triangles | What changed |
|---|---|---|
| first render | 458 | the 128 px emission map showed crystal glow on the ground's rim: the bake margin was wider than the gap between UV islands |
| final | 498 | margin tied to the gap; small pieces given 2.5 times the texel density; the ring widened so the count reaches its cap more often |

The script never caught any of these: the renders and the references did.

Scene case (`examples/wizard-glade/`, `benchmarks/wizard-glade.toon`): a 24 × 24 stud glade, **942
triangles** placed from 354 unique in 10 kit pieces (35 copies), one material, 8/8.

## 7. Asset records

Every model gets a line in `assets/provenance.yaml`: where it came from (script path, Meshy task
id, or the source and its license), the date, and the asset id once uploaded. Never use a model
whose license is unknown; Poly Haven (CC0) is safe for textures and HDRIs.

## Meshy (only when opted in)

Only after the user said yes in section 0 and `auth status` reports verified. Rules from
meshy-3d-agent's skill that matter here:

- **Every create costs credits.** Run `meshy balance` first, give the user the plan and the
  estimate the CLI reports, and get a yes before the first paid create. A rerun, a variant or an
  extra stage is a new yes.
- **Ask what the model is for** (game asset, character to rig, render): it picks the route. A
  game asset or a triangle budget means **smart topology** (`--model-type smart-topology
  --target-polycount N`), not a standard model reduced afterwards. For Roblox, N stays under
  20,000 per mesh.
- Submit once with `create --async`, keep the task id, `wait` on it; a timeout is not a reason to
  create again. Use `--format json --no-update-check` on every command.
- **An LOD is a remesh of the existing task**, never a new generation.
- Download the GLB, run `mesh_check.py` on it, then fix or export in Blender (sections 3–5). A
  preview image is not proof of topology.
- Login is the CLI's device flow, approved by the user in a browser. Credentials never go in chat
  or in files the agent writes.
