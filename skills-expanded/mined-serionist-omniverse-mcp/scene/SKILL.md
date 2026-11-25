---
name: scene
description: >-
  Use when working on what is in an Omniverse or Isaac Sim stage: finding out what a scene holds, looking at it,
  placing, moving, creating or hiding prims, lighting and cameras, checking that a change worked, or capturing a
  scene from many viewpoints and variant states in one sweep. Covers looking before acting, reading the captures,
  spatial reasoning with bounds, the verification loop, and a sweep's shots and manifest.
allowed-tools: >-
  mcp__plugin_omniverse-mcp_omniverse__get_sim_state mcp__plugin_omniverse-mcp_omniverse__get_scene_tree
  mcp__plugin_omniverse-mcp_omniverse__get_prim_properties mcp__plugin_omniverse-mcp_omniverse__get_prim_bounds
  mcp__plugin_omniverse-mcp_omniverse__capture_viewport mcp__plugin_omniverse-mcp_omniverse__get_logs
  mcp__plugin_omniverse-mcp_omniverse__get_job
---

# Work on a scene

The stage is a USD hierarchy of prims with paths such as `/World/Robot/base`. Edits apply at once; things move only
while physics plays. Never edit blind: look, change, look again.

## Steps

1. **Orient.** `get_sim_state` first: the up axis (Y or Z) decides which coordinate is height, `meters_per_unit` the
   scale of every number, and whether physics is playing. To work on a scene from a file, `open_scene` it, after
   `save_scene` when the open stage should be kept: it goes without a prompt. Its answer gives the same axis and units.
2. **Find what is there.**
   - `get_scene_tree` lists the hierarchy, each prim's path, type and position; with `include_properties`, or
     `filter_types` or `property_filter` to keep some types or properties, Kit writes the prims' values to a file
     instead, to grep.
   - `get_prim_properties` for one prim's attributes, its applied schemas (`api_schemas`) and its relationships'
     targets, such as the material it is bound to; `get_prim_bounds` for its world box.
3. **Look.** `capture_viewport` writes three files to `mcp_output/captures/`: the image, the bounding boxes (each
   visible prim's screen box, world centre and size) and the instance segmentation (a colour per prim, with a legend).
   Read the boxes file for where things are; open the image when you need to see. `include_image=True` returns the
   image inline as well, which costs about what opening the file does (some 400 tokens at the default 640x480) and
   saves a step.
   - A prim from every side: `inspect_prim`, which frames it, with `isolate=True` to hide everything else.
   - Another view: `set_camera`, from a `position` or around a prim with `prim_path`, then capture.
   - Inside or behind something: `set_visibility(path, false)`, capture, then show it again.
   - Overlapping prims that look alike: the segmentation tells them apart.
   - What is in front of what, and how far: `include_depth=True` adds each prim's nearest distance to the legend
     (`/World/Box = [R, G, B] distance = 2.413`, stage units), a grey depth image (nearer brighter, nothing hit black)
     and the raw distances as a `.npy`. Grep the legend rather than raycasting prim by prim.
4. **Place with numbers, not by eye.** `get_prim_bounds` of the thing and of what it goes on, compute the position
   on the up axis (an object rests on a surface when its bottom equals the surface's top), `set_prim_transform`, then
   capture to check.
5. **Change,** with `create_prim`, `set_prim_transform`, `clone_prim`, `set_material`, `set_visibility` or
   `set_prim_attribute`, which sets one attribute no other tool does, such as a light's intensity; for a check that
   must leave the user's files as they are, `layer="session"` writes it in Kit's session layer, which no save keeps
   and no tool takes back until the stage is opened again.
   `clone_prim` refuses a target path that holds a prim, and `create_prim` one that holds a prim of another type:
   choose a free path, or delete the prim there first when the user wants it gone.
6. **Check every change** with another capture or `get_prim_bounds`. A tool that fails: `get_logs(min_level="warn")`
   shows what Kit reported.

## A check from many viewpoints

To look at a scene from many places and through its switches, such as each stop of an inspection robot with each
of its variant states, use `capture_sweep`: one call, where `capture_viewport` costs a turn a picture.

1. **List the shots.** Each a `position` with `yaw` and `pitch` (yaw about the up axis, 0 along +X; pitch -90 looks
   straight down), or with a `target`, or a `camera_path`; the camera's `focal_length` and apertures; the
   `selections` it shows, `{prim: {set: variant}}`; a `time` when it matters. A long list goes in a JSON file, given
   as `shots_file`, so it needn't pass through the conversation.
2. **Run it.** `capture_sweep(shots=..., name="site_a")` answers a job id at once; `get_job(id, wait=100)` until it
   ends, then one line names the folder and the shots that came out black or failed. Open the PNGs you need:
   `manifest.json` says which shot each is, with its pose, lens and selections.
3. **Again, after a change** or on a second scene built from the same spec:
   `capture_sweep(shots_file="mcp_output/sweeps/site_a/manifest.json", name="site_a_2")` takes the same shots,
   so the pictures compare one for one. Give the first sweep's `width` and `height` too: a manifest is taken again
   at its own size, and another is refused.

Every layer, the session layer's selections and the timeline are as they were afterwards, after `cancel_job` too.

## Light and black captures

Kit 105.1 and later have no default light, so a scene without lights renders black, Kit's grid alone showing, and
the capture warns.
`viewport_light("get")` shows the lighting mode and whether the stage has lights of its own; a light rig's are the
viewport's, not the stage's, and go in mode `stage` or another app. `viewport_light(action="set", mode="Default")` is
the quickest fix, `mode="camera"` a light that follows the camera. When neither suits, add a light to the stage with
`create_prim` (`DistantLight`, `DomeLight`). A `DistantLight` comes at an intensity of 50,000, UsdLux's sunlight, which
overexposes a capture: `set_prim_attribute(path, "inputs:intensity", 3000)` brings it to a few thousand. Nothing
relights the scene on its own.

## Traps

| Trap | What to do |
|---|---|
| The up axis guessed | `get_sim_state` before placing anything |
| Code of your own in `execute_script` that reads the viewport right after a camera move sees the old view | wait 20 of the viewport's frames first; `capture_viewport` and `inspect_prim` need nothing: each waits 20 frames of its own render after it sets the camera, so a move or a drawing made before the call shows |
| A call fails with "Kit at ... stopped answering" | Kit may be running a long script, or be hung for good in NVIDIA's renderer (#114); calls fail in 5 s while it stays silent. If it stays silent for minutes, ask the user to restart the Kit app, and on Isaac Sim 6.2 to start it with `--/rtx/hydra/supportMultiTickRate=false`, NVIDIA's workaround for the hang: repeated captures of one view then differ a little more. Only Kit's command line takes it: never set it with `execute_script`, which doesn't reconfigure the renderer and misleads Replicator's `step()` |
| Captures and recordings slow Kit down for 30 s after | the bridge keeps their render that long, so the next capture, or a recording at its size, sets up no new view, where Kit can hang: Kit renders about 15 % fewer updates at 640x480 meanwhile, about 60 % fewer at 4096x4096, so capture and record at the size you need, the same for both |
| Segmentation missing | the answer says why, as `Segmentation: ERROR` or an angle's `seg: ERROR`: without `omni.syntheticdata` (Isaac Sim has it), `manage_extensions` enables it; with no data yet, capture again; if it stays empty, `get_logs(channel="syntheticdata")` shows what omni.syntheticdata reported, and `get_logs(search="segmentation")` how long the bridge waited |
| Replicator's walking agents differ between two sweeps | they move on each update whatever the timeline's time: stop the timeline (`sim_control("stop")`) before a sweep whose pictures of them must repeat |
| Materials look grey at first | MDL compiles on first use: capture again before deciding a material is broken |
| `UsdGeom.Cube` and the like have no faces | implicit shapes, not meshes: `get_mesh_stats` counts only `UsdGeom.Mesh` |
| A new stage has no file | pass `file_path` to every `save_scene` of it: that writes a copy, and the stage itself still has no file |
| `save_scene` refuses a `file_path` the open stage has loaded | a sublayer or a referenced file would be replaced by the root layer: name another path, or `save_scene()` with none to save the stage to its own file |
| A file opened with `open_scene` sets no units | its `note` says so: USD reads it as centimetres, 0.01 metres per unit, and every number is scaled by it |
| A `.usdz`, or a stage `open_scene`'s answer calls read-only (an `https://` URL's) | `save_scene` can't write it back: give a `file_path` ending `.usd` or `.usda`, or use `flatten_usd` |
| A scene with thousands of instances | loading can take minutes, and tools answer slowly meanwhile: ask the user whether it has finished |
