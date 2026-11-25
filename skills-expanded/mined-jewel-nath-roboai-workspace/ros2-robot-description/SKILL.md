---
name: ros2-robot-description
description: Write and check a ROS 2 robot description - URDF and xacro links, joints and limits, inertials from CAD mass
  properties, meshes and package:// paths, the <ros2_control> block, robot_state_publisher, TF frames per REP 103/105,
  Gazebo Harmonic and MuJoCo loading notes, and checks with xacro, check_urdf, RViz, view_frames and gz sdf.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-18
---

# ROS 2 robot description

Lets an agent build a URDF/xacro description that RViz, `robot_state_publisher`, ros2_control and
simulators all accept, and prove it before anything moves. Written for ROS 2 Jazzy (urdfdom 4,
Gazebo Harmonic) from the docs and sources; the recipes were not run. Lyrical and Humble
differences are at the end.

## When to use

- Starting a `my_robot_description` package, or turning CAD or a sketch into URDF/xacro.
- Adding a link, joint, sensor mount, mesh or camera optical frame.
- Filling in masses and inertias, or fixing a robot that floats, shakes or explodes in simulation.
- Adding the `<ros2_control>` block that a hardware interface or Gazebo will read.
- RViz shows missing links, white models or "No transform"; the TF tree is broken or wrong.

Elsewhere: controllers and hardware plugins in [ros2-control](../ros2-control/SKILL.md); nodes,
launch and QoS in [ros2-core](../ros2-core/SKILL.md); running simulations in `sim-gazebo` and
`sim-mujoco` (later skills).

## Quick start

```bash
cd ~/ros2_ws/src
ros2 pkg create my_robot_description --build-type ament_cmake --license Apache-2.0
cd my_robot_description && mkdir -p urdf meshes/visual meshes/collision launch rviz
# write the files from references/description-package.md, then:
xacro urdf/my_robot.urdf.xacro > /tmp/my_robot.urdf && check_urdf /tmp/my_robot.urdf
cd ~/ros2_ws && colcon build --packages-select my_robot_description && source install/setup.bash
ros2 launch urdf_launch display.launch.py urdf_package:=my_robot_description \
  urdf_package_path:=urdf/my_robot.urdf.xacro
```

`check_urdf` and `urdf_to_graphviz` come with urdfdom; if they are not on the PATH, install
`liburdfdom-tools`. The last command starts `robot_state_publisher`, `joint_state_publisher_gui`
and RViz; move every joint with the sliders.

## Workflow

1. **Fix the frames first.** Choose the root (`base_footprint` on the ground, or `base_link`),
   then one frame per rigid part and per sensor. Follow REP 103: x forward, y left, z up, SI units;
   cameras get an extra `<name>_optical_frame` (z forward, x right, y down) through a fixed joint
   with `rpy="${-pi/2} 0 ${-pi/2}"`. The robot's pose in the world comes from TF (`odom`, `map`,
   per REP 105), never from a `floating` or `planar` joint. Details in
   [references/frames.md](references/frames.md).
   *Check:* a sketch or table of every frame, its parent and its offset, measured on the robot or
   taken from CAD.

2. **Lay out the package.** A top-level `urdf/my_robot.urdf.xacro` holding only `xacro:arg`s and
   includes; one file per subsystem; inertia macros; the `<ros2_control>` block and the `<gazebo>`
   tags in their own files. Install `urdf`, `meshes`, `launch`, `rviz` to `share/`. Full example:
   [references/description-package.md](references/description-package.md) and
   [references/sensors-control-display.md](references/sensors-control-display.md).
   *Check:* `xacro urdf/my_robot.urdf.xacro` prints XML with no warnings.

3. **Write links and joints.** Each moving link has `<visual>`, `<collision>` and `<inertial>`.
   Joint types: `revolute` and `prismatic` need `<limit effort= velocity= lower= upper=>`
   (urdfdom rejects them without one); `continuous` for wheels; `fixed` for mounts. Put a joint's
   `<origin>` on the rotation axis; `<axis>` is given in the joint frame, which is also the child
   link's frame. Give both drive wheels the same `<axis xyz="0 1 0">`, so that positive velocity on
   either one drives the robot forward.
   Use xacro's built-in `pi` and `radians()`, properties for every dimension, and macros for
   anything repeated.
   *Check:* `check_urdf` lists the tree you sketched; `urdf_to_graphviz /tmp/my_robot.urdf my_robot`
   writes a PDF of it.

4. **Meshes.** Reference them as `package://my_robot_description/meshes/...`. Export in metres, or
   add `scale="0.001 0.001 0.001"` for millimetre files. Use detailed meshes (`.dae`, `.stl`,
   `.obj`) for `<visual>` only; for `<collision>` use primitives or a simplified convex mesh.
   *Check:* after `colcon build` and `source install/setup.bash`, RViz shows every mesh in the
   right place and size, with no "Could not load resource" errors.

5. **Inertials.** Mass in kg at the centre of mass, tensor in kg·m² about it. Take them from CAD
   mass properties of each link's full set of parts (motors and screws included), from a scale and
   a primitive formula, or from a mesh; never from placeholders. Keep the root link without
   `<inertial>` (KDL ignores a root link's inertia and warns). Formulas, a FreeCAD script, unit
   conversions and validity tests: [references/inertials.md](references/inertials.md).
   *Check:* every tensor passes the positive-definite and triangle-inequality test, and
   `gz sdf --inertial-stats` gives the robot's weighed total mass.

6. **The `<ros2_control>` block.** Declare one `<ros2_control>` element per hardware component:
   the hardware `<plugin>` with its `<param>`s, then each `<joint>` with its command and state
   interfaces. Switch the plugin with a xacro arg (`gz_ros2_control/GazeboSimSystem` in Gazebo,
   `mock_components/GenericSystem` without hardware, your driver on the robot). Every joint named
   there must exist in the URDF. The controllers, their YAML and the hardware plugin's code belong
   to [ros2-control](../ros2-control/SKILL.md).
   *Check:* `xacro ... sim:=true` and `sim:=false` both expand, and the joint names match the URDF.

7. **Publish it.** `robot_state_publisher` takes the expanded URDF as its `robot_description`
   parameter, republishes it on the `/robot_description` topic (transient local, which
   ros2_control's controller manager reads in Jazzy), sends fixed joints on `/tf_static`, and turns
   `/joint_states` into `/tf`. In launch, wrap the xacro command:
   `ParameterValue(Command(['xacro ', path, ' sim:=', sim]), value_type=str)`. Joint states come
   from `joint_state_publisher_gui` for checks, from ros2_control's `joint_state_broadcaster` on
   the real robot or in Gazebo.
   *Check:* `ros2 topic echo --once /robot_description` returns the URDF; `tf2_echo` between the
   root and every leaf frame succeeds.

8. **Simulator notes.** Gazebo Harmonic converts URDF to SDF on spawn: links on fixed joints are
   lumped into their parent, massless links on moving joints are dropped, `<gazebo reference=>`
   tags add friction and sensors, and `package://` meshes need `GZ_SIM_RESOURCE_PATH`. MuJoCo loads
   URDF with a `<mujoco><compiler>` block and is best converted to MJCF once. Recipes:
   [references/simulators.md](references/simulators.md).
   *Check:* `gz sdf -p` on the expanded URDF prints no `urdf2sdf` errors; MuJoCo's
   `MjSpec.from_file(...).compile()` succeeds.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| RViz: "No transform from [wheel_link] to [base_link]" | No `/joint_states` for a movable joint | Run `joint_state_publisher(_gui)` or the `joint_state_broadcaster` |
| Launch fails parsing `robot_description` | xacro output parsed as YAML | `ParameterValue(..., value_type=str)` |
| Meshes missing in RViz | Package not built/installed or not sourced, wrong `package://` path, or mm-sized mesh at 1000x | `install(DIRECTORY meshes ...)`, re-source, check `scale` |
| Meshes missing in Gazebo only | Package's parent folder not in `GZ_SIM_RESOURCE_PATH` | `<gazebo_ros gazebo_model_path="${prefix}/../"/>` export, or set the variable |
| Robot floats, jitters or explodes on spawn | Wrong units in inertia, tensor not physically valid, COM outside the part, interpenetrating collisions at spawn | [inertials.md](references/inertials.md) checks; spawn slightly above the ground |
| Link and its joint vanish in Gazebo | Link has no `<inertial>` or mass 0 on a non-fixed joint | Give it real mass |
| Camera point cloud or detections rotated 90° in RViz | Image stamped in `camera_link` instead of the optical frame | Add `<camera>_optical_frame` and stamp images in it (`gz_frame_id` in Gazebo) |
| Wheel spins the wrong way, or diff drive turns in place | Wheel axes flipped per side | Same `<axis>` on both wheels |
| Warning "redefining global symbol: pi" | A `pi` property overrides xacro's built-in | Delete the property |
| "Converting unknown joint type ... into a fixed joint" | `floating` or `planar` joint | Remove it; pose comes from `odom` TF |
| "The root link ... has an inertia specified" | Inertial on the root link | Add a massless root (`base_footprint`) or move the mass to a child link |
| `version="1.2"` URDF rejected | Jazzy's urdfdom accepts only version 1.0 | Drop `version`, `quat_xyzw`, `<capsule>` and the new limits on Jazzy |
| A frame disappears in MuJoCo | `fusestatic` merges links on fixed joints | Reference the body from a site/sensor, or set `fusestatic="false"` |

## Checks

Before reporting the description done:

- `xacro urdf/my_robot.urdf.xacro [args] > /tmp/my_robot.urdf` with no warnings, for every arg
  combination you ship (`sim:=true`, `sim:=false`).
- `check_urdf /tmp/my_robot.urdf` passes and shows the intended tree.
- RViz with `joint_state_publisher_gui`: every link visible, every joint moves about the right axis,
  in the right direction, within its limits. Turn on the TF display and check that frame axes match
  REP 103 (red x forward, green y left, blue z up; optical frames z forward).
- `ros2 run tf2_tools view_frames`: one tree, root where you meant it, no orphan frames.
- `ros2 run tf2_ros tf2_echo base_link <sensor_frame>` matches the measured mount offsets.
- Every `<inertial>` passes the checks in [inertials.md](references/inertials.md); total mass
  matches the scale.
- For simulation: `gz sdf -p` clean, and the model spawns and stands still in Gazebo or MuJoCo.

## Distro differences

- **Lyrical Luth**: URDF 1.2 (opt in with `<robot version="1.2">`) adds `quat_xyzw` origins,
  `<capsule>` geometry and acceleration, deceleration and jerk limits. Jazzy's urdfdom rejects any
  version other than 1.0, and RViz does not draw capsules yet.
- `robot_state_publisher` reading the URDF from a file given as a command-line argument is
  deprecated in Jazzy and removed in Lyrical; pass the `robot_description` parameter. Lyrical adds
  `use_robot_description_topic` to subscribe to `/robot_description` instead of publishing it.
- Gazebo pairing: Jazzy with Harmonic, Kilted with Ionic, Lyrical with Jetty. Humble pairs with
  Fortress, and Gazebo Classic (EOL January 2025) plugins do not exist in any of these.
- In Humble the controller manager took `robot_description` as a parameter; from Jazzy it reads
  the `/robot_description` topic.

## Related

- References: [description-package.md](references/description-package.md),
  [sensors-control-display.md](references/sensors-control-display.md),
  [inertials.md](references/inertials.md), [frames.md](references/frames.md),
  [simulators.md](references/simulators.md).
- Wiki: [URDF](../../wiki/software/urdf.md), [tf2](../../wiki/software/tf2.md),
  [ros2_control](../../wiki/software/ros2-control.md), [ROS 2](../../wiki/tools/ros2.md),
  [Foxglove](../../wiki/tools/foxglove.md).
- Skills: [ros2-control](../ros2-control/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [ros2-web-bridge](../ros2-web-bridge/SKILL.md); later: `sim-gazebo`, `sim-mujoco`,
  `manip-moveit2`, `cad-freecad`.
- Upstream: REP 103 and REP 105 (ros.org/reps); the Jazzy URDF tutorials on docs.ros.org, which
  also list CAD exporters (FreeCAD, Fusion 360, Onshape, SolidWorks, Blender); MuJoCo's
  "URDF extensions" in its modeling guide.
