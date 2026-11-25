---
name: ros2-control
description: >-
  Set up ros2_control on ROS 2 Jazzy: a SystemInterface hardware plugin, the <ros2_control> URDF tag,
  controller YAML (joint_state_broadcaster, joint_trajectory_controller, diff_drive_controller), spawners,
  tests on mock_components/GenericSystem or gz_ros2_control, and debugging with the ros2 control CLI.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-18
---

# ros2_control

Connects a robot's motors and encoders to standard ROS 2 controllers, proves the setup on mock
hardware and in Gazebo, then runs it on the real board. Checked against ros2_control 4.50 and
ros2_controllers 4.43, the Jazzy releases on 2026-11-18; the recipes were not run.

## When to use

- Writing or fixing a hardware interface plugin for a motor-controller board, servos or a CAN bus.
- Adding a `<ros2_control>` tag to a URDF, writing controller YAML, spawning controllers.
- An arm driven by `joint_trajectory_controller` (what MoveIt 2 talks to), a differential-drive
  base driven by `diff_drive_controller` (what Nav2 talks to), `/joint_states` from the broadcaster.
- Debugging: a controller will not load or activate, no `/joint_states`, the robot does not move.

Not here: PID tuning, real-time kernels and motor firmware (later `control-` and `fw-` skills);
building the URDF itself ([ros2-robot-description](../ros2-robot-description/SKILL.md)).

## Quick start

On mock hardware first; no robot needed.

```bash
sudo apt install ros-jazzy-ros2-control ros-jazzy-ros2-controllers ros-jazzy-xacro
```

1. Add the `<ros2_control>` tag with `mock_components/GenericSystem` to the URDF.
2. Write `config/controllers.yaml`, one section per controller with its `type`.
3. Launch `robot_state_publisher`, `ros2_control_node` and one `spawner` with `--param-file`.

All three files, ready to adapt: [references/urdf-yaml-launch.md](references/urdf-yaml-launch.md).

```bash
ros2 launch my_robot_bringup robot.launch.py hardware:=mock
ros2 control list_hardware_components     # my_robot_system ... active
ros2 control list_controllers             # every controller active
ros2 topic echo --once /joint_states
```

## Workflow

### 1. Declare the interfaces in the URDF

- The tag `<ros2_control name="my_robot_system" type="system">` holds a `<hardware><plugin>` and,
  per joint, the `command_interface` and `state_interface` names (`position`, `velocity`,
  `effort`). `<param>` entries under `<hardware>` reach the plugin as `info_.hardware_parameters`.
- Make the plugin a xacro argument (`mock`, `gz`, `real`) so one description serves all three.
- Wheels: command `velocity`, state `position` and `velocity`. Position-controlled arm joints:
  command `position`, state `position` and `velocity`.
- Every joint in the tag must exist in the URDF; non-joint I/O goes in `<gpio>`.

Check: `xacro my_robot.urdf.xacro hardware:=mock > /tmp/r.urdf && check_urdf /tmp/r.urdf`
(`check_urdf` comes with `liburdfdom-tools`).

### 2. Write the controller YAML

- One top-level section per controller, each with `type:` in its own `ros__parameters`.
- `joint_state_broadcaster` needs nothing else; it publishes every state interface.
- `joint_trajectory_controller`: `joints`, `command_interfaces`, `state_interfaces`,
  `constraints`.
- `diff_drive_controller`: wheel names, measured `wheel_separation` and `wheel_radius`, frames,
  `cmd_vel_timeout`, limits as `linear.x.max_velocity` and similar (unset means no limit).

Check: the file parses (`python3 -c "import yaml; yaml.safe_load(open('controllers.yaml'))"`),
and every joint name in it appears in the `<ros2_control>` tag.

### 3. Launch and spawn

- `robot_state_publisher` publishes `/robot_description`; the controller manager subscribes to
  it. Do not pass the URDF to `ros2_control_node`.
- `ros2_control_node` takes `update_rate` (default 100 Hz).
- One `spawner` lists the broadcaster first, then the controllers, then `--param-file <yaml>`. It
  waits for the controller manager, loads, configures and activates in that order.

Check: `ros2 control list_controllers` shows each one `active`, and
`ros2 control list_hardware_interfaces` shows the command interfaces `[claimed]`.

### 4. Prove the pipeline on mock hardware

- `mock_components/GenericSystem` copies commands to states. Set `calculate_dynamics` to `true`
  so velocity commands integrate into positions and odometry moves.
- Drive it: `TwistStamped` on `/diff_drive_controller/cmd_vel`, or a `JointTrajectory` on
  `/arm_controller/joint_trajectory` (commands in the reference).

Check: `/joint_states` changes, `/diff_drive_controller/odom` moves, and
`ros2 run tf2_ros tf2_echo odom base_link` follows.

### 5. Write the hardware interface

Full header and source: [references/hardware-interface.md](references/hardware-interface.md);
plugin XML, CMake and a load check: [references/hardware-package.md](references/hardware-package.md).

- Derive from `hardware_interface::SystemInterface` (`SensorInterface` for read-only devices,
  `ActuatorInterface` for one actuator).
- `on_init(const HardwareComponentInterfaceParams & params)`: call the base `on_init(params)`
  first, read and validate `info_.hardware_parameters` and the interface lists. No I/O here.
- `on_configure`: open the link, set states and commands to 0.0. `on_cleanup`: close it.
- `on_activate`: set commands to a safe start (0.0 for velocity, the current state for
  position), then enable the drives. `on_deactivate`: stop and disable them.
- `read()`: one exchange with the board, then `set_state("<joint>/position", value)`.
  `write()`: `get_command("<joint>/velocity")`, skip NaN, send.
- Do not override `export_state_interfaces()` or `export_command_interfaces()`: deprecated on
  Jazzy, removed on Lyrical. The framework creates the interfaces from the URDF tag.
- Convert to SI units (rad, rad/s, m, N·m) inside the plugin.
- Return `return_type::ERROR` when the bus fails: the component goes to `on_error` and the
  controllers that use it are deactivated.
- Export: `PLUGINLIB_EXPORT_CLASS(my_robot_hardware::MyRobotSystem,
  hardware_interface::SystemInterface)`, a plugin XML whose class `name` matches the URDF
  `<plugin>`, and `pluginlib_export_plugin_description_file(hardware_interface
  my_robot_hardware.xml)` in CMake.

Check: `colcon build`, then `ros2 control list_hardware_components -v` lists the component
`active` with its interfaces, and the log has no "class ... does not exist".

### 6. Move to the real robot

- Launch with `hardware:=real`. Wheels off the ground or the arm at low speed for the first run.
- Give the serial device a fixed name with a udev rule; add the user to the `dialout` group.
- To stop the motors without killing the launch:
  `ros2 control set_hardware_component_state my_robot_system inactive`.

Check: with the component `inactive` (motors free, states still read), one wheel revolution by
hand moves its `/joint_states` position by 6.28 rad with the sign the URDF axis predicts; then,
active, a forward command moves the base forward.

### 7. Simulate in Gazebo Harmonic

- `sudo apt install ros-jazzy-gz-ros2-control ros-jazzy-ros-gz`.
- `<plugin>gz_ros2_control/GazeboSimSystem</plugin>` in `<hardware>`, plus the Gazebo plugin
  `gz_ros2_control::GazeboSimROS2ControlPlugin` (file `gz_ros2_control-system`) with
  `<parameters>` pointing at the controller YAML.
- No `ros2_control_node`: the controller manager runs inside Gazebo. Bridge `/clock`, use sim
  time, spawn the robot with `ros_gz_sim create`, then run the same spawner.

Check: `ros2 control list_controllers` shows them active and the robot moves in Gazebo on the same
commands as step 4. The Gazebo side as a whole comes in a later simulation skill.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Spawner waits forever for the controller manager | `ros2_control_node` died: bad URDF, unknown plugin, joint not in URDF | Read the `ros2_control_node` log first; fix the first error |
| "class ... does not exist" for the plugin | XML `name` and URDF `<plugin>` differ, CMake export missing, workspace not sourced | Match the three names, rebuild, `source install/setup.bash` |
| Controller loads but has no parameters, or its type is unknown | YAML given only to `ros2_control_node`; Jazzy controllers do not read it | Spawner `--param-file`, `type:` in the controller's own section |
| Base ignores `/cmd_vel` | `diff_drive_controller` listens on `~/cmd_vel` and needs `TwistStamped` | Publish stamped, remap with `--controller-ros-args`, teleop with `-p stamped:=true` |
| Arm or base jumps when activated | Command left at an old value or NaN | Set commands in `on_activate`; skip non-finite commands in `write()` |
| Control loop overruns, jerky motion | Blocking or retried I/O in `read()`/`write()` | One bounded exchange per cycle; slow devices `is_async="true"`; deeper real-time work belongs to later control and firmware skills |
| Odometry drifts or turns the wrong way | Wrong `wheel_separation`/`wheel_radius`, a reversed wheel | Measure; fix direction at its source (URDF joint axis or motor sign in the plugin) |
| `gains` in the trajectory controller do nothing | Gains apply only to velocity- or effort-only command interfaces | Remove them for `position` commands |
| Limits from the URDF not applied | `enforce_command_limits` is `false` on Jazzy | Set it `true` on the controller manager, or clamp in the plugin |
| Gazebo robot does not move, TF stale | Missing `/clock` bridge or `use_sim_time` | Bridge the clock; sim time on every node |

## Checks

- `ros2 control list_hardware_components -v`: each component `active`, interfaces as declared.
- `ros2 control list_controllers`: all `active`; `ros2 control list_hardware_interfaces`: each
  command interface `[claimed]` by exactly one controller.
- `ros2 topic hz /joint_states` close to the broadcaster's rate; no overrun warnings in the
  controller manager log.
- The same launch file works with `hardware:=mock` and `hardware:=real`.
- Real robot: wheel and joint directions and scale verified by hand before closed-loop driving.

## Distro differences

- **Humble** (ros2_control 2.x): `on_init(const HardwareInfo &)`; you must override
  `export_state_interfaces()` and `export_command_interfaces()` with pointers to your own doubles;
  no `set_state`/`get_command`; `ros2_control_node` gets `robot_description` as a parameter;
  `diff_drive_controller` takes plain `Twist` with `use_stamped_vel: false`.
- **Jazzy before 4.34**: only `on_init(const HardwareInfo &)`. Check with
  `dpkg -s ros-jazzy-hardware-interface | grep Version` and upgrade.
- **Kilted** (5.x): the code here works; the old signatures are deprecated.
- **Lyrical** (6.x): the export methods, the `HardwareInfo` `on_init` and the pointer-based
  `Handle` constructor are removed; `set_state(name, 0)` with an `int` throws; controller manager
  ros args are no longer forwarded to controllers; `enforce_command_limits` defaults to `true`;
  `gz_ros2_control` pairs with Gazebo Jetty.

## Related

- Wiki: [ros2_control](../../wiki/software/ros2-control.md), [URDF](../../wiki/software/urdf.md),
  [tf2](../../wiki/software/tf2.md), [ROS 2](../../wiki/tools/ros2.md),
  [PlotJuggler](../../wiki/tools/plotjuggler.md) for plotting joint states.
- Skills: [ros2-core](../ros2-core/SKILL.md),
  [ros2-robot-description](../ros2-robot-description/SKILL.md),
  [ros2-web-bridge](../ros2-web-bridge/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md).
  Later: Gazebo simulation, Nav2, MoveIt 2, micro-ROS, control and firmware skills.
- Upstream: control.ros.org (Jazzy docs, migration guides), ros2_control_demos `jazzy` branch.
