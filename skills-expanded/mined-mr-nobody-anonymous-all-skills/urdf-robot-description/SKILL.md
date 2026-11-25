---
name: urdf-robot-description
description: "Use when writing or debugging URDF/Xacro robot descriptions for ROS 2 — link/joint trees, inertia tensors, collision geometry, xacro macros, ros2_control tags, Gazebo/Ignition spawning. Provides exact inertia formulas, working xacro patterns, mimic joint rules, mesh simplification strategy, and fixes for the classic 'robot explodes in simulation' and 'no transform from base_link' failures."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# URDF / Xacro Robot Description — Expert Knowledge

## 0. Mental Model (read this first)

A URDF is a **tree, not a graph**. One root link, every other link has exactly
one parent joint. No kinematic loops (use SDF or `<gazebo>` extensions for
closed chains; URDF cannot express them — four-bar linkages must be faked with
a mimic joint or split chain).

Three parallel geometry channels per link, all optional but with hard
consequences:

| Channel | Consumer | Missing ⇒ |
|---|---|---|
| `<visual>` | RViz, Gazebo rendering | invisible link (fine) |
| `<collision>` | physics contacts, MoveIt self-collision | falls through floor / arm clips itself |
| `<inertial>` | dynamics engine | **link ignored or NaN explosion** (see §6) |

`robot_state_publisher` consumes URDF + `/joint_states` and publishes TF.
Gazebo consumes URDF (converted to SDF internally). MoveIt consumes URDF +
SRDF. They all parse the *same* file — design for the strictest consumer
(the physics engine).

## 1. Minimal Correct Skeleton

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="myrobot">

  <!-- root link: NO inertia needed ONLY if it is the fixed-to-world root
       in Gazebo via a fixed joint to world; otherwise give it inertia -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0.05" rpy="0 0 0"/>
      <geometry><box size="0.4 0.3 0.1"/></geometry>
      <material name="grey"><color rgba="0.5 0.5 0.5 1"/></material>
    </visual>
    <collision>
      <origin xyz="0 0 0.05" rpy="0 0 0"/>
      <geometry><box size="0.4 0.3 0.1"/></geometry>
    </collision>
    <inertial>
      <origin xyz="0 0 0.05" rpy="0 0 0"/>
      <mass value="5.0"/>
      <inertia ixx="0.0417" ixy="0" ixz="0" iyy="0.0708" iyz="0" izz="0.1042"/>
    </inertial>
  </link>

  <joint name="lidar_joint" type="fixed">
    <parent link="base_link"/>
    <child link="lidar_link"/>
    <origin xyz="0.1 0 0.12" rpy="0 0 0"/>
  </joint>

  <link name="lidar_link">
    <visual><geometry><cylinder radius="0.035" length="0.04"/></geometry></visual>
    <collision><geometry><cylinder radius="0.035" length="0.04"/></geometry></collision>
    <inertial>
      <mass value="0.15"/>
      <inertia ixx="6.6e-5" ixy="0" ixz="0" iyy="6.6e-5" iyz="0" izz="9.2e-5"/>
    </inertial>
  </link>
</robot>
```

Rules baked into the above:
- `base_link` is the conventional root name (REP-105). If you have a floating
  base, add `base_footprint` (massless-ish, on the ground plane) as root with
  a fixed joint up to `base_link`.
- `<origin>` inside `<joint>` is the transform **parent→child frame**.
- `<origin>` inside `<visual>/<collision>/<inertial>` is relative to the
  **link's own frame** (which sits at the joint).
- Material colors only render in RViz from URDF; Gazebo Classic needs
  `<gazebo reference="link"><material>Gazebo/Grey</material></gazebo>`;
  modern Gazebo (gz-sim) reads the URDF `<material><color>` fine.

## 2. Joint Types — exact semantics

| Type | DOF | `<axis>` | `<limit>` required | Notes |
|---|---|---|---|---|
| `fixed` | 0 | ignored | no | merged by Gazebo into parent (lumping) unless `<gazebo><preserveFixedJoint>` / `gz` flag |
| `revolute` | 1 rot | yes | **yes** (lower, upper, effort, velocity) | parser ERROR without limits |
| `continuous` | 1 rot | yes | only effort+velocity | wheels; no lower/upper |
| `prismatic` | 1 lin | yes | **yes**, limits in meters | |
| `floating` | 6 | — | no | almost no tool supports it; don't use; Gazebo gives you a free-floating root automatically |
| `planar` | 3 | yes (normal) | no | poorly supported; avoid |

Joint limit numbers that matter:

```xml
<limit lower="-2.617" upper="2.617" effort="28.0" velocity="3.14"/>
<!-- effort: Nm (revolute) or N (prismatic). velocity: rad/s or m/s. -->
<dynamics damping="0.1" friction="0.05"/>
<!-- damping Nm·s/rad. Zero damping on a heavy arm in Gazebo = oscillation.
     Start with damping 0.1–1.0 per arm joint, 0.01 for small servos. -->
<safety_controller k_position="100" k_velocity="10"
                   soft_lower_limit="-2.5" soft_upper_limit="2.5"/>
<!-- optional; gazebo ignores it, ros2_control joint_limits can use soft limits -->
```

`effort="0"` or `velocity="0"` silently disables actuation in some
controllers — never leave them 0 on actuated joints.

**Axis convention:** `<axis xyz="0 0 1"/>` default. Positive rotation =
right-hand rule about axis in the **child** frame. Wheels on a diff-drive
robot: axis `0 1 0` if the wheel link's Y points along the axle (typical when
you rotate the wheel cylinder with `rpy="1.5708 0 0"`).

## 3. Inertia Tensors — formulas you must use

All about the **center of mass**, in the frame given by `<inertial><origin>`.
URDF wants the 6 unique terms of the symmetric 3×3 matrix. Off-diagonals are
0 for symmetric primitives aligned with the frame.

| Shape | ixx | iyy | izz |
|---|---|---|---|
| Box (x,y,z dims) | m(y²+z²)/12 | m(x²+z²)/12 | m(x²+y²)/12 |
| Solid cylinder, axis=Z (r, h) | m(3r²+h²)/12 | m(3r²+h²)/12 | m·r²/2 |
| Solid sphere (r) | 2mr²/5 | same | same |
| Hollow sphere | 2mr²/3 | same | same |
| Thin rod along Z (L) | mL²/12 | mL²/12 | ~0 (use ≥1e-6) |

Worked example — box 0.4×0.3×0.1 m, 5 kg (matches §1):
- ixx = 5(0.09+0.01)/12 = 0.0417
- iyy = 5(0.16+0.01)/12 = 0.0708
- izz = 5(0.16+0.09)/12 = 0.1042

Xacro macro — use this everywhere instead of hand-computing:

```xml
<xacro:macro name="box_inertial" params="mass x y z *origin">
  <inertial>
    <xacro:insert_block name="origin"/>
    <mass value="${mass}"/>
    <inertia ixx="${mass*(y*y+z*z)/12.0}" ixy="0" ixz="0"
             iyy="${mass*(x*x+z*z)/12.0}" iyz="0"
             izz="${mass*(x*x+y*y)/12.0}"/>
  </inertial>
</xacro:macro>

<xacro:macro name="cylinder_inertial" params="mass r h *origin">
  <inertial>
    <xacro:insert_block name="origin"/>
    <mass value="${mass}"/>
    <inertia ixx="${mass*(3*r*r+h*h)/12.0}" ixy="0" ixz="0"
             iyy="${mass*(3*r*r+h*h)/12.0}" iyz="0"
             izz="${mass*r*r/2.0}"/>
  </inertial>
</xacro:macro>

<xacro:macro name="sphere_inertial" params="mass r *origin">
  <inertial>
    <xacro:insert_block name="origin"/>
    <mass value="${mass}"/>
    <inertia ixx="${2.0*mass*r*r/5.0}" ixy="0" ixz="0"
             iyy="${2.0*mass*r*r/5.0}" iyz="0" izz="${2.0*mass*r*r/5.0}"/>
  </inertial>
</xacro:macro>
```

Usage (note `*origin` block param syntax):

```xml
<link name="wheel_left">
  ...
  <xacro:cylinder_inertial mass="0.3" r="0.05" h="0.02">
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </xacro:cylinder_inertial>
</link>
```

**Sanity bounds:** for a link of mass m and max dimension d, every diagonal
term must satisfy roughly `m·d²/12 ≤ I ≤ m·d²`. Triangle inequality must hold:
ixx + iyy ≥ izz (and permutations). Violating it makes ODE/DART produce NaN
or silently clamp. Never use `<inertia ixx="1" iyy="1" izz="1"/>` on a 100 g
link — a 1 kg·m² inertia on a tiny servo horn makes the arm sluggish and the
solver stiff.

**Minimum values:** Gazebo Classic warned below mass 0.001 / inertia 1e-6.
Use `mass ≥ 0.01`, diagonal `≥ 1e-5` for small parts. For decorative tiny
links, prefer merging them into the parent's visual rather than giving fake
inertia.

## 4. Missing-Inertia Physics Explosion (the #1 sim failure)

Symptoms: robot spawns then launches into the sky, vibrates violently,
links fly apart, or Gazebo prints nothing but the robot is invisible/sunk.

Root causes, in observed frequency order:

1. **A non-fixed-jointed link has no `<inertial>` block.** Gazebo Classic
   drops such links entirely (and any joint touching them) with only a
   warning; gz-sim may keep them with garbage defaults. Result: TF tree in
   RViz fine, robot in sim broken. Fix: every link on a moving joint gets
   real inertia.
2. **Inertia wildly too small for the mass** (e.g. 10 kg link with 1e-7
   inertia). Solver becomes stiff → explosion at first contact. Use the §3
   formulas.
3. **Inertia frame wrong**: `<inertial><origin>` left at 0 while the COM is
   actually 0.5 m away along the link. Robot tips over or jitters. Place the
   inertial origin at the geometric center of the visual.
4. **Two collision geometries overlapping at spawn** (e.g. wheel collision
   intersecting base collision because origins copy-pasted). Initial
   penetration → huge corrective impulse → launch. Shrink collisions by
   1–2 mm or fix origins.
5. **Mass ratio > ~1000:1 across a joint** (5 kg base, 1 g sensor on a
   revolute joint). Iterative solvers (ODE quickstep) can't converge. Merge
   the light link via fixed joint (lumping fixes it) or raise its mass.
6. **`<mu>` / contact params set to 0 or 1e9** in `<gazebo>` tags from a
   copied template.

Debug procedure: `check_urdf robot.urdf` → confirm tree; then
`gz sdf -p robot.urdf` (or `ign sdf -p`) and read the converted SDF —
links missing from the SDF output were dropped for missing inertia.

## 5. Visual vs Collision Geometry

- **Visual**: full-detail mesh OK. DAE keeps materials/colors; STL is
  geometry-only (RViz renders STL in whatever color the Material says,
  default red if missing).
- **Collision**: NEVER reuse a 100k-triangle visual mesh. Contact generation
  on concave trimeshes is O(n²)-ish, unstable (trimesh–trimesh contact in ODE
  is notoriously bad), and MoveIt collision checking slows 10–100×.

Collision strategy ladder (best → acceptable):
1. **Primitives** (box/cylinder/sphere) hand-fit to the link. A robot arm
   link is a cylinder + box. Diff-drive base is one box. This is correct for
   90% of robots.
2. **Convex hull** of the mesh (Meshlab: Filters→Convex Hull, or
   `trimesh.convex.convex_hull` in Python; export STL).
3. **Convex decomposition** (V-HACD) only when concavity matters (a gripper
   palm, a bowl).
4. Decimated trimesh (<1000 tris) — last resort, expect contact jitter.

```xml
<visual>
  <geometry><mesh filename="package://myrobot_description/meshes/visual/link2.dae"/></geometry>
</visual>
<collision>
  <geometry><mesh filename="package://myrobot_description/meshes/collision/link2_hull.stl"/></geometry>
</collision>
```

Mesh gotchas:
- `package://pkg/path` requires the package to be **installed and sourced**;
  in launch files prefer xacro-time resolution: `$(find pkg)` works in
  `.launch.py` via `FindPackageShare`, but inside URDF stick to
  `package://`. gz-sim ≥ Fortress resolves `package://` only if
  the path is in `GZ_SIM_RESOURCE_PATH` (or via `ros_gz` bridge setup) —
  set `GZ_SIM_RESOURCE_PATH=$AMENT_PREFIX_PATH/share` style paths in launch.
- Units: URDF is meters. SolidWorks/Blender STL exports are often in mm →
  robot 1000× too big. Fix with `<mesh ... scale="0.001 0.001 0.001"/>`.
- Mesh origin: exported meshes carry their CAD origin. If the mesh appears
  offset, fix it in the `<visual><origin>`, or better, re-export with origin
  at the joint location.

## 6. Xacro — patterns that work

Build command (always check your URDF generates):

```bash
xacro robot.urdf.xacro > /tmp/robot.urdf && check_urdf /tmp/robot.urdf
# args:
xacro robot.urdf.xacro use_sim:=true prefix:=left_ > /tmp/robot.urdf
```

Properties, math, conditionals:

```xml
<xacro:property name="wheel_radius" value="0.05"/>
<xacro:property name="wheel_sep" value="0.30"/>
<xacro:property name="PI" value="3.14159265359"/>
<xacro:arg name="use_sim" default="false"/>
<xacro:arg name="prefix" default=""/>

<!-- math: full python expressions inside ${} -->
<origin xyz="0 ${wheel_sep/2} ${wheel_radius}" rpy="${-PI/2} 0 0"/>

<!-- arg → property bridge (args are strings; do this once) -->
<xacro:property name="use_sim" value="$(arg use_sim)"/>

<xacro:if value="${use_sim}">
  <xacro:include filename="$(find myrobot_description)/urdf/gazebo.xacro"/>
</xacro:if>
<xacro:unless value="${use_sim}">
  <xacro:include filename="$(find myrobot_description)/urdf/real_hw.xacro"/>
</xacro:unless>
```

Macro with reflection (left/right symmetry — the canonical wheel macro):

```xml
<xacro:macro name="wheel" params="side reflect">
  <joint name="wheel_${side}_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_${side}_link"/>
    <origin xyz="0 ${reflect*wheel_sep/2} 0" rpy="${-PI/2} 0 0"/>
    <axis xyz="0 0 1"/>   <!-- cylinder rotated, so Z is now the axle -->
    <dynamics damping="0.01" friction="0.001"/>
  </joint>
  <link name="wheel_${side}_link">
    <visual><geometry><cylinder radius="${wheel_radius}" length="0.02"/></geometry></visual>
    <collision><geometry><cylinder radius="${wheel_radius}" length="0.02"/></geometry></collision>
    <xacro:cylinder_inertial mass="0.3" r="${wheel_radius}" h="0.02">
      <origin xyz="0 0 0" rpy="0 0 0"/>
    </xacro:cylinder_inertial>
  </link>
</xacro:macro>

<xacro:wheel side="left"  reflect="1"/>
<xacro:wheel side="right" reflect="-1"/>
```

Xacro mistakes everyone makes:
- `$(arg x)` works only for declared `<xacro:arg>`; `${x}` only for
  `<xacro:property>`. Mixing them → literal `$(arg x)` string in output.
- `xacro:if value="${'true' == use_sim}"` — args are STRINGS. `value="$(arg
  use_sim)"` works because xacro truthy-parses 'true'/'false'/'1'/'0', but
  `${use_sim and other}` on a string arg evaluates the string truthiness
  ('false' is truthy in Python!). Bridge to a property and compare:
  `${use_sim == 'true'}` if unsure.
- Including a file twice redefines macros silently (last wins) — keep one
  `common_properties.xacro` included once at the top.
- `*origin` block params must be passed as child XML elements, in declared
  order when multiple blocks (`**` for multi-element blocks).
- Namespacing for dual-arm: pass `prefix` into EVERY macro and prepend on
  every link/joint name: `name="${prefix}shoulder_link"`.

## 7. ros2_control Tags

Inside the URDF (this is what `ros2_control` reads via
`robot_state_publisher`'s `robot_description` topic/param):

```xml
<ros2_control name="MyRobotSystem" type="system">
  <hardware>
    <xacro:if value="${use_sim}">
      <plugin>gz_ros2_control/GazeboSimSystem</plugin>
    </xacro:if>
    <xacro:unless value="${use_sim}">
      <plugin>myrobot_hardware/MyRobotHardware</plugin>
      <param name="serial_port">/dev/ttyUSB0</param>
      <param name="baud_rate">115200</param>
    </xacro:unless>
  </hardware>

  <joint name="shoulder_joint">
    <command_interface name="position">
      <param name="min">-2.617</param>
      <param name="max">2.617</param>
    </command_interface>
    <state_interface name="position">
      <param name="initial_value">0.0</param>
    </state_interface>
    <state_interface name="velocity"/>
  </joint>

  <joint name="wheel_left_joint">
    <command_interface name="velocity">
      <param name="min">-10</param>
      <param name="max">10</param>
    </command_interface>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>

<!-- gz-sim (Fortress/Harmonic) plugin hookup -->
<gazebo>
  <plugin filename="gz_ros2_control-system"
          name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>$(find myrobot_bringup)/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

Hard-won rules:
- Plugin name history: Gazebo Classic = `gazebo_ros2_control/GazeboSystem`;
  gz-sim Humble-era = `ign_ros2_control/IgnitionSystem`; Iron+ =
  `gz_ros2_control/GazeboSimSystem`. Wrong one → controller_manager loads,
  zero interfaces exported, controllers fail with "interface not found".
- Every joint a controller claims MUST list the matching
  `command_interface` here, and `joint_state_broadcaster` needs the
  `state_interface`s. The error `'shoulder_joint/position' not available`
  means it's missing in this block, not in the YAML.
- `initial_value` on the position state interface sets the sim spawn pose of
  the joint — use it to start an arm in a non-singular config.
- Mock testing without hardware: `<plugin>mock_components/GenericSystem
  </plugin>` + `<param name="calculate_dynamics">true</param>`.
- For diff drive in gz-sim you can skip ros2_control entirely and use the
  `gz::sim::systems::DiffDrive` plugin, but then no `/joint_states` from
  controller — bridge them or use ros2_control for consistency.

## 8. Mimic Joints

```xml
<joint name="gripper_right_joint" type="prismatic">
  <parent link="gripper_base"/>
  <child link="finger_right"/>
  <axis xyz="0 1 0"/>
  <limit lower="0" upper="0.04" effort="50" velocity="0.1"/>
  <mimic joint="gripper_left_joint" multiplier="-1.0" offset="0.0"/>
</joint>
```

Semantics: `value = multiplier * other_joint + offset`. Use cases: parallel
grippers (multiplier -1 or 1), four-bar fakes, differential pulleys.

Pitfalls:
- `robot_state_publisher` honors mimic ONLY if the mimicked joint appears in
  `/joint_states` — publish the master joint only; do not publish the mimic
  joint or you get TF fighting.
- Gazebo Classic ignored `<mimic>` entirely → needed the
  `roboticsgroup_gazebo_plugins` MimicJointPlugin. gz-sim Harmonic+ supports
  it natively when spawned through `ros_gz_sim` (converted to SDF joint
  with `<mimic>`); older Fortress does not — verify with `gz sdf -p`.
- ros2_control: since Iron, mimic joints are auto-detected from URDF; don't
  give a mimic joint a `command_interface` in `<ros2_control>` — state only.
- MoveIt handles mimics fine (excluded from planning DOF) as long as the SRDF
  doesn't list them in a group's actuated joints.

## 9. Sensors and Gazebo Extensions

```xml
<gazebo reference="lidar_link">
  <sensor name="lidar" type="gpu_lidar">
    <update_rate>10</update_rate>
    <topic>scan</topic>
    <gz_frame_id>lidar_link</gz_frame_id>   <!-- without this, frame_id is wrong in Harmonic -->
    <lidar>
      <scan><horizontal><samples>360</samples>
        <min_angle>-3.14159</min_angle><max_angle>3.14159</max_angle>
      </horizontal></scan>
      <range><min>0.12</min><max>8.0</max><resolution>0.01</resolution></range>
    </lidar>
    <always_on>true</always_on>
    <visualize>false</visualize>
  </sensor>
</gazebo>
```

- `<gazebo reference="X">` attaches to link/joint X; `<gazebo>` without
  reference is model-wide (plugins).
- Friction for wheels (gz-sim): `<gazebo reference="wheel_left_link">
  <mu1>1.0</mu1><mu2>1.0</mu2><kp>1e6</kp><kd>100</kd></gazebo>`.
  Caster ball: `mu1=mu2=0.0`. kp default 1e12 is too stiff for rubber
  tires — 1e5–1e7 reduces wheel bounce.
- Fixed-joint lumping breaks `<gazebo reference="sensor_link">` because the
  link no longer exists in SDF. Workarounds: give the sensor link nonzero
  inertia AND add `<gazebo reference="sensor_joint">
  <preserveFixedJoint>true</preserveFixedJoint></gazebo>` (Classic), or in
  gz-sim attach the sensor to the lumped parent and set `<pose>` /
  `gz_frame_id` accordingly — or just check `gz sdf -p` output to see where
  your link went.

## 10. Launch Wiring (ROS 2, Python)

```python
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    xacro_file = PathJoinSubstitution(
        [FindPackageShare("myrobot_description"), "urdf", "robot.urdf.xacro"])
    robot_description = ParameterValue(
        Command([FindExecutable(name="xacro"), " ", xacro_file,
                 " use_sim:=true"]),
        value_type=str)   # value_type=str is MANDATORY or YAML-parse errors on URDF content

    return LaunchDescription([
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[{"robot_description": robot_description,
                          "use_sim_time": True}]),
        # gz-sim spawn from the topic robot_state_publisher publishes:
        Node(package="ros_gz_sim", executable="create",
             arguments=["-topic", "robot_description", "-name", "myrobot",
                        "-z", "0.1"]),   # spawn slightly above ground — avoids initial penetration
    ])
```

- `ParameterValue(..., value_type=str)` — omitting it is the cause of the
  cryptic `InvalidParameterValueException ... could not be parsed as yaml`.
- Spawn z-offset 0.05–0.1 m prevents §4 cause #4 at world contact.
- `joint_state_publisher_gui` only for viewing without controllers; never run
  it alongside ros2_control's `joint_state_broadcaster` (duplicate
  `/joint_states` → TF flicker).

## 11. Debugging Checklist

Run in order; stop at first failure.

1. `xacro robot.urdf.xacro > /tmp/r.urdf` — xacro errors are line-accurate;
   "No such file" usually means package not built/sourced (`colcon build
   && source install/setup.bash`).
2. `check_urdf /tmp/r.urdf` — verifies single tree. "link X not found" =
   typo in a joint's parent/child. Two roots = an orphan link.
3. `urdf_to_graphviz /tmp/r.urdf && dot -Tpdf r.gv -o r.pdf` — eyeball tree.
4. `gz sdf -p /tmp/r.urdf > /tmp/r.sdf` — diff link list vs URDF; missing
   links ⇒ inertia missing or lumped; read warnings, they're real.
5. RViz with `joint_state_publisher_gui`: set Fixed Frame to `base_link`.
   - "No transform from [X] to [base_link]": a joint to X is not in
     `/joint_states` (non-fixed joints need a state) or RSP not running.
   - Link visually offset/rotated: visual `<origin>` vs joint `<origin>`
     confusion — move the offset into the joint if the frame itself should
     move, into the visual if only cosmetics.
   - Mesh white/missing in RViz2: bad `package://` path (check
     `AMENT_PREFIX_PATH`), or DAE with up-axis Z/Y mismatch (re-export with
     Z-up).
6. Spawn in empty Gazebo world, gravity ON, no controllers: robot should
   simply rest. Jitter/launch ⇒ §4.
7. Start controllers one at a time:
   `ros2 control list_hardware_interfaces` first — every expected
   `joint/position` etc. must show `[available]`. Missing ⇒ §7.
8. `ros2 run tf2_tools view_frames` — final TF sanity; every link present,
   no duplicate-publisher warnings in `tf_monitor`.

Frequent silent killers:
- Joint and link sharing the same name — legal but confuses humans and some
  tools; suffix joints with `_joint`.
- `rpy` is fixed-axis XYZ (roll about X, then pitch about original Y, then
  yaw about original Z) — extrinsic; people import intrinsic Euler from CAD
  and get flipped links. When a 90° rotation "goes the wrong way", negate it
  before reaching for quaternion math.
- Capital letters / spaces in link names break some downstream tools
  (MoveIt SRDF generation) — snake_case only.
- Editing the .urdf instead of the .urdf.xacro and losing changes on next
  build. Only ever commit the xacro.
- `revolute` joint with `lower == upper == 0` — joint exists but can't move;
  controllers accept commands and nothing happens.

## 12. File/Package Layout (convention that tools expect)

```
myrobot_description/
├── package.xml          # exec_depend: xacro, robot_state_publisher
├── CMakeLists.txt       # install(DIRECTORY urdf meshes launch rviz DESTINATION share/${PROJECT_NAME})
├── urdf/
│   ├── robot.urdf.xacro       # top-level: includes everything, declares args
│   ├── common_properties.xacro
│   ├── base.xacro
│   ├── arm.xacro
│   ├── ros2_control.xacro
│   └── gazebo.xacro
├── meshes/
│   ├── visual/    *.dae
│   └── collision/ *.stl   (hulls, <1k tris)
├── launch/display.launch.py
└── rviz/view.rviz
```

Forgetting the `install(DIRECTORY ...)` line means meshes resolve in dev but
404 after `colcon build` on another machine — the single most common "works
on my laptop" URDF bug.
