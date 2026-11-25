---
name: sim-gazebo
description: Run a ROS 2 Jazzy robot in Gazebo Harmonic (gz-sim8) - SDF worlds and their system plugins, ros_gz_sim
  gz_sim.launch.py and headless CI runs, spawning from /robot_description with create, ros_gz_bridge YAML, /clock and
  use_sim_time, ros_gz_image, lidar/camera/IMU sensors and gz_frame_id, gz_ros2_control, Fuel models, Classic migration.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-19
---

# Gazebo simulation

Lets an agent start a Gazebo world from ROS 2, spawn the robot, connect its sensors and controllers to
ROS, and run the same simulation headless in CI. Written for Jazzy with Gazebo Harmonic, checked
against gazebosim.org, gz-sim 8.15, ros_gz 1.0.25 and gz_ros2_control 1.2.20 (`jazzy` branches); the
recipes were not run. Humble/Fortress and Lyrical/Jetty differences are at the end.

## When to use

- Writing an SDF world, or a launch file that starts Gazebo and spawns a robot from `/robot_description`.
- Bridging topics between Gazebo and ROS 2: `/clock`, sensors, commands, odometry, joint states.
- Adding a lidar, camera, depth camera, IMU, GPS (NavSat) or contact sensor to a simulated robot.
- Driving the simulated robot through ros2_control with `gz_ros2_control`.
- Running Gazebo without a display: CI, Docker, a remote machine.
- Porting a package from Gazebo Classic (`gazebo_ros`, `spawn_entity.py`, `libgazebo_ros_*.so`).
- Debugging: robot missing or invisible, sensor topics silent, TF errors under sim time, controllers
  that never load.

Elsewhere: the URDF and how Gazebo converts it to SDF (fixed-joint lumping, massless links, meshes) in
[ros2-robot-description](../ros2-robot-description/SKILL.md) and its
[simulators.md](../ros2-robot-description/references/simulators.md); controllers, their YAML and the
`<ros2_control>` tag in [ros2-control](../ros2-control/SKILL.md); containers and GPUs in
[ops-docker-ci](../ops-docker-ci/SKILL.md); the reality gap in [sim-to-real](../sim-to-real/SKILL.md).

## Quick start

```bash
sudo apt install ros-jazzy-ros-gz ros-jazzy-gz-ros2-control   # Gazebo Harmonic comes as gz_*_vendor packages
source /opt/ros/jazzy/setup.bash
gz sim --versions                                            # 8.x is Harmonic
ros2 launch ros_gz_sim gz_sim.launch.py gz_args:="-r -v 3 empty.sdf"
```

For a robot, copy the world from [references/world.md](references/world.md) and the launch file and
bridge YAML from [references/launch.md](references/launch.md) into `my_robot_gazebo`, then:

```bash
ros2 launch my_robot_gazebo sim.launch.py                                   # with the GUI
ros2 launch my_robot_gazebo sim.launch.py gz_flags:="-r -s --headless-rendering -v 3"   # CI
ros2 topic hz /clock && ros2 control list_controllers
```

## Workflow

1. **Lay out the packages.** `my_robot_description` holds the URDF and meshes;
   `my_robot_gazebo` holds `worlds/`, `config/bridge.yaml` and `launch/`; the controller YAML stays
   where the ros2-control skill puts it (`my_robot_bringup/config/controllers.yaml`). Depend on
   `ros_gz_sim`, `ros_gz_bridge`, `ros_gz_image` and `gz_ros2_control` in `package.xml`, not on the
   whole `ros_gz` metapackage.
   *Check:* `rosdep install --from-paths src -i -y` resolves everything; `colcon build` passes.

2. **Write the world.** An SDF `<world>` with `<physics>` (`max_step_size`, `real_time_factor`), a
   light, a ground and the **system plugins**: a world that lists any `<plugin>` loses the default
   Physics, UserCommands and SceneBroadcaster, so list them too. Add one world system per sensor
   family: Sensors (`<render_engine>ogre2</render_engine>`) for cameras and `gpu_lidar`, Imu,
   NavSat (plus `<spherical_coordinates>`), Contact, ForceTorque. DART is the default physics engine;
   Classic `<ode>` solver blocks and `<real_time_update_rate>` are not read. Template and physics
   notes: [references/world.md](references/world.md).
   *Check:* `gz sdf -k worlds/my_world.sdf` says valid, and
   `gz sim -s -r -v 4 --iterations 2000 worlds/my_world.sdf` exits without errors.

3. **Make every file findable.** `model://` and `package://` URIs in worlds, includes and meshes are
   looked up on `GZ_SIM_RESOURCE_PATH`; includes fall back to Fuel. Put the parent of each
   package's `share` directory on it: `AppendEnvironmentVariable` in the launch file, a colcon
   `.dsv` hook, or `<gazebo_ros gazebo_model_path="${prefix}/../"/>` in `package.xml` (read by
   `gz_sim.launch.py` and `gz_server.launch.py`, not by plain `gz sim`). Fuel models download on
   first use into `~/.gz/fuel`; offline CI needs them fetched beforehand (`gz fuel download -u <url>`)
   or copied into a package. Details in [references/world.md](references/world.md).
   *Check:* `-v 4` output has no `Unable to find uri[...]` or `Failed to load mesh`; the launch
   argument `debug_env:=true` of `gz_sim.launch.py` prints the paths it set.

4. **Launch Gazebo from ROS.** Include `ros_gz_sim`'s `gz_sim.launch.py` with `gz_args` (the
   `gz sim` command line) and `on_exit_shutdown:=true`. `-r` starts the clock; without it the world
   is paused and everything waiting on sim time waits forever. `-s` runs only the server, `-g` only
   the GUI (it attaches to a running server), `--headless-rendering` renders sensors through EGL with
   no display. Alternative: `gz_server.launch.py world_sdf_file:=...` runs the server as a ROS node
   (`gzserver`), unpaused, and offers the `simulation_interfaces` services (`/gzserver/reset_simulation`,
   `/gzserver/step_simulation`, ...). Full launch file: [references/launch.md](references/launch.md).
   *Check:* `gz topic -l` lists `/clock`, `/stats` and `/world/my_world/...`;
   `gz topic -e -t /stats -n 1` shows `real_time_factor` near the world's target.

5. **Spawn the robot.** Run `robot_state_publisher` (with `use_sim_time: true`) on the expanded xacro,
   then `ros2 run ros_gz_sim create -topic robot_description -name my_robot -z 0.05`. `create` reads
   the transient-local topic and sends the XML to `/world/<world>/create`, where sdformat converts
   the URDF; without `-world` it asks Gazebo for the world name. `-file` takes a path or a Fuel URL, `-string` raw XML;
   `-x -y -z -R -P -Y` set the pose; `-allow_renaming true` spawns duplicates. Spawn slightly above the
   ground so collisions do not start interpenetrated.
   *Check:* `create` logs `Entity creation successful.`; `gz model --list` shows `my_robot`.

6. **Bridge topics.** One `parameter_bridge` with a YAML `config_file`: `/clock` first and
   `GZ_TO_ROS` only, then each sensor topic, and commands `ROS_TO_GZ`. Every ROS node that touches
   simulated data gets `use_sim_time: true`, RViz included. Images can go through
   `ros_gz_image image_bridge` instead (image_transport, compressed topics); `camera_info` still goes
   through the YAML. Type pairs and the YAML: [references/launch.md](references/launch.md).
   *Check:* `ros2 topic hz /clock` and each sensor topic tick; `ros2 topic echo --once /scan` has a
   sensible `header.stamp` (sim seconds, not wall time).

7. **Add sensors.** Put `<sensor>` elements in `<gazebo reference="<link>">` blocks of the URDF (or in
   the SDF model): set `<topic>` to a short name, `<update_rate>`, noise from the datasheet, and
   `<gz_frame_id>` to the URDF link. Without it the header carries a Gazebo scoped name such as
   `my_robot::base_link::lidar`, which TF does not know. Cameras stamp images and `camera_info` with
   `<camera><optical_frame_id>` when it is set. Blocks per sensor, topics and message types:
   [references/sensors.md](references/sensors.md).
   *Check:* `gz topic -e -t /scan -n 1` shows data; on the ROS side `header.frame_id` names a frame
   in `ros2 run tf2_tools view_frames`, and RViz shows the scan or image in the right place.

8. **Control the robot with ros2_control.** The URDF's `<ros2_control>` uses
   `gz_ros2_control/GazeboSimSystem`, and a `<gazebo>` block loads the system plugin
   `gz_ros2_control-system` (`gz_ros2_control::GazeboSimROS2ControlPlugin`) with `<parameters>`
   pointing at the controller YAML. That plugin runs the controller manager inside Gazebo with
   `use_sim_time` forced on and waits until `/robot_description` arrives, so start no
   `ros2_control_node`. Run the spawners after `create` exits. The tag, YAML and spawner details
   belong to [ros2-control](../ros2-control/SKILL.md)
   ([urdf-yaml-launch.md](../ros2-control/references/urdf-yaml-launch.md)); the Gazebo-side options
   are in [references/launch.md](references/launch.md).
   *Check:* `ros2 control list_controllers` shows all `active`; a command moves the robot in Gazebo
   and `/joint_states` follows.

9. **Run it headless and repeatable.** `gz_args:="-r -s --headless-rendering -v 3 <world>"`; give each
   parallel job its own `GZ_PARTITION` (and `ROS_DOMAIN_ID`) so simulations do not see each other;
   set `real_time_factor` to 0 to run as fast as the CPU allows when every node uses sim time. A GUI
   can join a remote headless server with `gz sim -g` in the same partition.
   *Check:* the CI job sees `/clock` advance and the test topics within its timeout, and two jobs on
   one runner do not cross-talk.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| `create` repeats "Requesting list of world names" | Gazebo not running, another `GZ_PARTITION`, or multicast blocked | Same environment in every shell; `gz topic -l` must answer; enable multicast |
| `create` repeats "Waiting messages on topic [robot_description]" | `robot_state_publisher` not running, or in another namespace | Start it first; `ros2 topic info /robot_description` |
| Sim time stuck at 0, TF and controllers wait | World started paused (no `-r`), or `/clock` not bridged | Add `-r` (or press play); bridge `/clock` `GZ_TO_ROS` |
| TF "extrapolation into the future/past", RViz drops messages | One node on wall time | `use_sim_time: true` everywhere, including RViz and `robot_state_publisher` |
| Gazebo publishes only `/world/<name>/clock` | Something else published `/clock` at startup: a bidirectional (`@`) clock bridge or a second simulation in the partition | Bridge the clock `[` only; one simulation per `GZ_PARTITION` |
| Models fall through the ground or stand frozen after adding one plugin | World plugins replace the default systems | List Physics, UserCommands and SceneBroadcaster |
| Sensor topic never appears | Its world system is missing (Sensors, Imu, NavSat, Contact...) | Add the system to the world, not to the `<sensor>` |
| Camera or lidar fails: "Unable to create the rendering window", black images | No display or OpenGL below 3.3 | `--headless-rendering`; GPU in the container (ops-docker-ci); `--render-engine ogre` on old GPUs |
| RViz "No transform" for scan or image | `frame_id` is a Gazebo scoped name | `<gz_frame_id>` per sensor; `<optical_frame_id>` for cameras; bridge `frame_id` as last resort |
| Contact sensor silent on a URDF robot | The conversion renamed the collision (`<link>_collision`) | Use the name from `gz sdf -p` output |
| "Failed to load system plugin" for `libgazebo_ros_*.so` | Gazebo Classic plugin | Replace it: [references/classic-migration.md](references/classic-migration.md) |
| "Waiting RM to load and initialize hardware..." repeats | No `/robot_description`, or the `<ros2_control>` tag fails to load | Start `robot_state_publisher`; read the first error above it |
| "Desired controller update period ... is faster than the gazebo simulation period" | `update_rate` above `1/max_step_size` | Lower `update_rate` or the step |
| Position-commanded joints lag or oscillate | gz_ros2_control turns position commands into velocity with `position_proportional_gain` (default 0.1) | Tune it, keep it at most 1; or command effort |
| Wheels slip, odometry drifts with velocity commands | Joint velocity is set instantly, the body cannot follow | Acceleration limits in the controller, realistic friction and mass |
| Real-time factor far below 1 | Mesh collisions, too many lidar rays, software rendering | Primitive collisions; fewer samples; a GPU; watch `/stats` |
| A second launch fails or sees old topics | Leftover `gz sim` processes from a killed launch | `pkill -f "gz sim"` before relaunching; `on_exit_shutdown:=true` |

## Checks

Before reporting the simulation working:

- `gz sdf -k` passes for every world and model file; `gz sdf -p` on the expanded URDF has no errors.
- The launch starts with no `Unable to find uri`, `Failed to load mesh` or `Failed to load system
  plugin` lines at `-v 4`.
- `/clock` advances (`ros2 topic hz /clock`), and the real-time factor on `/stats` is near target.
- Every bridged topic publishes at the expected rate with sim-time stamps and a `frame_id` that exists
  in TF (`view_frames`, `tf2_echo base_link <sensor_frame>`).
- `ros2 control list_controllers` shows every controller `active`; a test command moves the robot in
  the expected direction.
- The headless command used in CI runs to completion on a machine without a display.

## Distro differences

- **Humble with Fortress** (`ros-humble-ros-gz`): the CLI is `ign gazebo` / `ign topic`
  (`gz_sim.launch.py` picks it), plugins are `ignition-gazebo-<name>-system` with
  `ignition::gazebo::systems::<Name>`, the resource variable is `IGN_GAZEBO_RESOURCE_PATH`, and
  sensors read `ignition_frame_id` (`gz_frame_id` only from ign-sensors 6.8). The bridge takes
  `ignition.msgs.*` or `gz.msgs.*`. There is no `gz_server.launch.py`, no `GzServer`/`RosGzBridge`
  launch actions and no `simulation_interfaces`. `ros_ign_*` packages are shims for `ros_gz_*`.
  gz_ros2_control keeps the same plugin names. Harmonic on Humble needs `ros-humble-ros-gzharmonic`
  from packages.osrfoundation.org.
- **Kilted** pairs with Ionic (gz-sim9); not covered here.
- **Lyrical with Jetty** (gz-sim10, Ubuntu 26.04, `ros-lyrical-ros-gz`): worlds, plugin file names,
  `gz_sim.launch.py`, `create` and the bridge YAML are unchanged. gz_ros2_control 3.x drops the
  `ign_ros2_control/IgnitionSystem` and `ign_ros2_control-system` aliases that Jazzy still loads. The
  GUI moved to Qt 6, so custom GUI plugins must be ported, and custom systems see velocity commands
  cleared after every step (since gz-sim 9). Lyrical's ros2_control API changes are in
  [ros2-control](../ros2-control/SKILL.md).
- Gazebo Classic reached end of life in January 2025 and pairs with none of these; port it with
  [references/classic-migration.md](references/classic-migration.md).

## Related

- References: [world.md](references/world.md), [launch.md](references/launch.md),
  [sensors.md](references/sensors.md), [classic-migration.md](references/classic-migration.md).
- Wiki: [Gazebo](../../wiki/tools/gazebo.md), [ROS 2](../../wiki/tools/ros2.md),
  [ros2_control](../../wiki/software/ros2-control.md), [URDF](../../wiki/software/urdf.md),
  [tf2](../../wiki/software/tf2.md), [PlotJuggler](../../wiki/tools/plotjuggler.md),
  [Choose a simulator](../../wiki/guides/choose-a-simulator.md).
- Skills: [ros2-robot-description](../ros2-robot-description/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md), [sim-to-real](../sim-to-real/SKILL.md); later
  `sim-mujoco`, `nav-nav2`, `manip-moveit2`, perception skills.
- Upstream: gazebosim.org/docs/harmonic (ROS 2 integration, sensors, SDF worlds, Classic migration),
  gz-sim API tutorials (finding resources, server configuration, physics, headless rendering), the
  `ros_gz` and `gz_ros2_control` READMEs and demos on their `jazzy` branches, and
  `ros_gz_project_template` for a full package layout with custom systems.
