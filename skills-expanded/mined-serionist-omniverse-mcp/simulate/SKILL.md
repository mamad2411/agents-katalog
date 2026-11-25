---
name: simulate
description: >-
  Use when running physics in Omniverse or Isaac Sim: playing, pausing, stepping or stopping the simulation, mass,
  friction, colliders and forces, something falling through a floor, raycasts, spawning and driving robots (Franka,
  UR10, G1, Spot and the rest), recording a run to review frame by frame afterwards, or measuring how fast a scene
  runs: its frame rate or FPS, a speed or frame-rate target such as 15 FPS, the physics step, GPU memory, or what a
  cut to the scene gained.
allowed-tools: >-
  mcp__plugin_omniverse-mcp_omniverse__get_sim_state mcp__plugin_omniverse-mcp_omniverse__get_robot_info
  mcp__plugin_omniverse-mcp_omniverse__raycast mcp__plugin_omniverse-mcp_omniverse__get_recording_frame
  mcp__plugin_omniverse-mcp_omniverse__get_prim_bounds mcp__plugin_omniverse-mcp_omniverse__capture_viewport
  mcp__plugin_omniverse-mcp_omniverse__get_logs mcp__plugin_omniverse-mcp_omniverse__get_prim_properties
  mcp__plugin_omniverse-mcp_omniverse__get_performance mcp__plugin_omniverse-mcp_omniverse__get_scene_tree
---

# Simulate, drive robots, record, measure

Edits to the stage are instant; motion happens only while the timeline plays. `stop` resets the stage to how it was
before play, so pause to look at a moment in the middle.

## Steps

1. **Orient.** `get_sim_state`: the up axis decides which way gravity pulls, and whether the timeline plays. Its
   `timeline` line says how long a run can be: a timeline that doesn't loop pauses at its end, physics with it, and
   one that loops goes back to its start while physics goes on; Kit's own new stage runs under 2 s.
2. **Physics on what moves.** `create_prim(..., enable_physics=True)` gives a prim a rigid body and collision;
   `set_physics_properties` sets mass, density, friction and restitution. Without a collider an object falls through
   the ground: `get_prim_properties`' `api_schemas` line says whether a prim has one (`PhysicsCollisionAPI`) and a
   rigid body (`PhysicsRigidBodyAPI`). `set_physics_properties(floor, collision=True)` makes a static collider of a
   floor, with no rigid body, so it stays put. Give each shape under an Xform its own; the Xform itself is refused.
3. **Robots.** `create_robot` spawns one of franka, ur10, carter, jetbot, g1, go1, go2, h1, spot or anymal from
   Isaac Sim's asset library (Isaac Sim only), or a robot's own USD file, a path or a URL, in any Kit app.
   `get_robot_info` lists its joints, and reads where they are while the simulation plays or is paused;
   `set_joint_targets` drives them.
4. **Run.** `sim_control("play")`, `"pause"`, `"step"` or `"stop"`. To debug a body or a robot, step, look, adjust:
   `sim_control("step", steps=30, observe=["/World/Box", "/World/G1"])` advances physics exactly 30 steps and reads
   each prim back from PhysX, a body's position, rotation and velocities, a robot's joints; `steps=0` reads without
   stepping. The timeline's time doesn't move with a step, so recordings and Action Graphs need `play`. Up to 1000
   steps a call; more is `play`, or a job (the script skill). A robot that sags, oscillates or misses its target:
   read each joint's `tracking_error`, `kp` and `kd` (`get_robot_info`, or the step's `observe`), raise `kp` for sag
   or `kd` for oscillation with `set_joint_drives` in the same units, step, read again. `tracking_error none` is a
   joint no position drive acts on, such as a wheel: not a gain to tune. `apply_force` pushes a rigid body through
   PhysX while the simulation plays or is paused, at its centre of mass unless a `position` is given: an impulse
   acts at once, a force for one physics step, so a sustained push is an impulse of force times seconds. A push on
   a robot's link moves the robot through its joints: a floating robot touching nothing by the impulse over its whole
   mass, while a fixed robot's link turns about its joints and friction on the ground takes some of the push. A body
   a fixed joint holds to the world, such as a fixed robot's base, is refused. With `/physics/suppressReadback` on,
   as Isaac Sim's GPU device sets it for PhysX's Direct GPU API, the push goes through PhysX's tensor API and its
   answer says `method: tensor`; there a second push on a body before the next physics step replaces the first, so
   push once per body per step, combining pushes into one, while pushes on different bodies each land. `raycast`
   needs the simulation to have played.
5. **Record what happens.** `start_recording` with `track_prims`, play, then `stop_recording`: each frame's image and
   the tracked prims' state land in `mcp_output/recordings/<session>/`. `get_recording_frame` reads one frame back.
   Frames come from `camera_path` (the viewport's camera when empty) at `width` x `height`, 640x480 unless given,
   without moving the viewport; they stop, with a note, if the stage changes or the camera is deleted.
6. **Check** with `get_prim_bounds`, `get_robot_info`'s joint states or a capture, rather than assuming the run did
   what was asked. Where many bodies came to rest, while the simulation plays or after a pause: one
   `get_scene_tree(root, property_filter=["physics:"])`, whose blocks give each body's world `pos` (the centre of its
   box) and `rot` as physics has them, with its physics values, in one file to grep; no script reads PhysX body by
   body. A tool that fails: `get_logs(min_level="warn")`.
7. **Measure the speed.** `get_performance` gives the frame rate a target reads (`app = ... FPS`), the GPU's render
   time, the physics step and the simulated-to-real ratio, GPU memory and what the stage holds. Measure as the target
   will run: play the simulation with the robots' sensors on, call nothing else meanwhile, measure before capturing
   (a capture's kept render is released for the measurement), and with other GPU work on the machine idle. After
   each cut to the scene, measure again and compare the two answers' `conditions` first. A `not settled` note means
   the run hadn't settled: measure again, with more `warmup`. The numbers are this machine's: a target set for
   another machine is checked there.

## Traps

| Trap | What to do |
|---|---|
| `get_robot_info` says `Joint states: not read` | the line gives the reason. Stopped: play or pause, not stop, since joint states come from physics, which a stop drops. No articulation at or under the path, or a Kit app without Isaac Sim: playing doesn't help; give the robot's root, or read the joints in Isaac Sim |
| `raycast` finds nothing | play first: it uses PhysX |
| A stopped run loses the state you wanted | `pause`, not `stop`, to look at it |
| Gravity along the wrong axis | the up axis from `get_sim_state`: a Y-up stage falls along -Y |
| `get_performance` reads fast on a stopped stage | play first: with eco mode on, RTX may stop rendering a still stage, and physics doesn't step, as its note says |
