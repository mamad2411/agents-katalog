---
name: ros2-core
description: Write and debug everyday ROS 2 code - ament_cmake and ament_python packages, rclpy and rclcpp nodes,
  topics, services, actions, parameters and parameter files, launch files (Python, XML, YAML), QoS mismatches, lifecycle
  nodes, executors and callback groups, custom msg/srv/action interfaces, logging, and inspecting a running system.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-18
---

# ROS 2 core

Lets an agent create ROS 2 packages and nodes, wire them up with launch and parameter files, and find
out why data does not flow. Written for ROS 2 Jazzy (Ubuntu 24.04, Python 3.12) from the Jazzy docs
and sources; the recipes were not run. Lyrical and Humble differences are at the end.

## When to use

- Creating a package, a node (Python or C++), or a msg/srv/action interface.
- Adding a publisher, subscription, service, action, timer or parameter to a node.
- Writing or fixing a launch file or a parameter YAML file.
- A topic is silent, a service call hangs, a node will not start, or a parameter is ignored.
- Turning a driver into a lifecycle node, or choosing an executor and callback groups.

Elsewhere: build flags and overlays on the [colcon](../../wiki/tools/colcon.md) page; picking an RMW
in the [middleware guide](../../wiki/guides/choose-a-ros2-middleware.md); URDF and TF in
[ros2-robot-description](../ros2-robot-description/SKILL.md); controllers and hardware interfaces in
[ros2-control](../ros2-control/SKILL.md).

## Quick start

```bash
source /opt/ros/jazzy/setup.bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
ros2 pkg create my_robot_nodes --build-type ament_python --license Apache-2.0 \
  --dependencies rclpy std_msgs sensor_msgs
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install --packages-select my_robot_nodes
source install/setup.bash          # in every new shell, after every build that adds files
ros2 pkg executables my_robot_nodes
```

Add the node from [references/python-nodes.md](references/python-nodes.md) as
`my_robot_nodes/range_filter.py`, register it in `setup.py`, rebuild, then
`ros2 run my_robot_nodes range_filter`. For C++ use `--build-type ament_cmake --dependencies rclcpp
std_msgs sensor_msgs` and [references/cpp-nodes.md](references/cpp-nodes.md).

## Workflow

1. **Lay out the packages.** One package per role: nodes, interfaces, bringup (launch and config),
   description. Python-only nodes use `ament_python`; C++ and interfaces use `ament_cmake`. Build
   files and an interface package are in [references/packages.md](references/packages.md).
   *Check:* `colcon build --packages-up-to <pkg>` passes and `ros2 pkg executables <pkg>` lists
   every node.

2. **Write the node.** One class per node. Create publishers, subscriptions, timers, clients and
   servers once, in the constructor. Declare every parameter (with a default and a descriptor)
   before reading it. Use timers, not `while` loops with `sleep`. Keep callbacks short; move slow
   work to its own callback group (step 7). Log through the node's logger, throttled in hot paths.
   *Check:* `ros2 node info /<node>` shows the expected publishers, subscriptions and services.

3. **Pick QoS per topic.** Start from a named profile and change only what you must.

   | Data | rclpy / rclcpp | Policy |
   |---|---|---|
   | Sensor streams (scans, images, IMU) | `qos_profile_sensor_data` / `rclcpp::SensorDataQoS()` | best effort, keep last 5 |
   | Commands, state, events | depth `10` / `rclcpp::QoS(10)` | reliable, volatile, keep last |
   | Latched data (maps, robot_description, config) | `QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL)` / `rclcpp::QoS(1).transient_local()` | reliable, transient local |

   A pair connects only if every policy is compatible: a best-effort publisher cannot feed a
   reliable subscription, and a volatile publisher cannot feed a transient-local subscription.
   Deadline, liveliness and lease duration must be compatible too. Subscribe to sensor topics with
   the sensor profile; it accepts both reliable and best-effort publishers.
   *Check:* `ros2 topic info -v /<topic>` lists both ends with their QoS, and no node logs
   "incompatible QoS".

4. **Parameters.** Load values from a YAML file in the launch file ([references/launch.md](references/launch.md)).
   Reject bad values with a descriptor range or `add_on_set_parameters_callback` (which must not
   change state), and apply accepted changes in `add_post_set_parameters_callback`.
   *Check:* `ros2 param get /<node> <name>` shows the file's value, and `ros2 param set` with an
   out-of-range value is refused.

5. **Services and actions.** A service is a short request and reply; an action is a long task with
   feedback and cancel. Inside callbacks, call services and actions asynchronously and handle the
   result in a done-callback. Python action servers reject every cancel unless you pass a
   `cancel_callback`.
   *Check:* `ros2 service call /<srv> <type> "{...}"` and
   `ros2 action send_goal --feedback /<action> <type> "{...}"` return what you expect.

6. **Launch it.** One bringup package holds the launch and parameter files. Set `use_sim_time` once
   for all nodes with `SetParameter`. Remap topics in the launch file, not in code.
   *Check:* `ros2 launch <pkg> <file> --show-args` lists the arguments; after launch,
   `ros2 node list` shows each node once.

7. **Executors and callback groups.** The default single-threaded executor runs one callback at a
   time. For parallel work use a `MultiThreadedExecutor` and put the slow or blocking callbacks in
   their own callback group; without groups the node still runs one callback at a time. Code is in
   the references.
   *Check:* `ros2 topic hz /<fast_topic>` stays steady while the slow work runs.

8. **Lifecycle nodes, where start-up order matters** (drivers, anything that opens hardware).
   Allocate in `on_configure`, start in `on_activate`, stop in `on_deactivate`, release in
   `on_cleanup`. An override must call the base class `on_activate`/`on_deactivate`, or its
   lifecycle publishers never switch on and drop every message.
   *Check:* `ros2 lifecycle set /<node> configure`, then `activate`;
   `ros2 lifecycle get /<node>` reports `active` and data flows.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Subscriber gets nothing; log says "offering incompatible QoS" or "requesting incompatible QoS" | Reliability or durability mismatch | Compare `ros2 topic info -v`; relax the subscriber (best effort, volatile) |
| Late subscriber misses the map or robot description | Publisher or subscriber is volatile | Both ends transient local, depth 1 |
| Topic exists but the subscriber never fires | Name or namespace differs (`scan` vs `/scan`), or a remap went to the wrong node | `ros2 node info` on both nodes; relative names resolve under the node's namespace |
| Node hangs in a callback | Synchronous service or action call on a single-threaded executor | Async call plus done-callback, or separate callback group plus `MultiThreadedExecutor` |
| `MultiThreadedExecutor` but callbacks still run one at a time | All callbacks in the default (mutually exclusive) group | Give slow callbacks their own group |
| `ParameterNotDeclaredException`, or a YAML value ignored | Parameter read before declaring, or YAML key does not match the node's full name | Declare first; check the name with `ros2 node list` |
| `InvalidParameterTypeException` at start-up | YAML gives `1` for a double, or a string for a number | Match the declared type (`1.0`) |
| Lifecycle node `active` but nothing published | Overridden `on_activate` skipped the base class call (rclpy then drops silently, rclcpp logs once) | Call `super().on_activate(state)` / `LifecycleNode::on_activate(state)` |
| Action goals cannot be cancelled (Python) | Default `cancel_callback` rejects all | Pass one that returns `CancelResponse.ACCEPT` |
| TF extrapolation errors in simulation | Some nodes on wall time, some on `/clock` | `SetParameter(name='use_sim_time', value=True)` before all nodes |
| `rclpy.shutdown()` raises after Ctrl-C | Context already shut down by the signal handler | Use `rclpy.try_shutdown()` in `finally` |
| Executable or launch file "not found" after adding it | Not installed, or the shell has not re-sourced the overlay | Add to `setup.py` `entry_points`/`data_files` or `install()`; rebuild; `source install/setup.bash` |
| Python edits ignored | Built without `--symlink-install` | Rebuild with it (new files still need a rebuild) |
| Two nodes with one name; parameters or services act oddly | Same `name=` launched twice in one namespace | Unique names or namespaces |
| Nodes on two machines cannot see each other | Different `ROS_DOMAIN_ID` or RMW, discovery limited, or firewall | Match `ROS_DOMAIN_ID` and `RMW_IMPLEMENTATION`; check `ROS_AUTOMATIC_DISCOVERY_RANGE`; run `ros2 doctor --report` |

`ROS_LOCALHOST_ONLY` is deprecated since Iron; use `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` (or
`SUBNET`, `OFF`) and `ROS_STATIC_PEERS`.

## Checks

Before reporting the work done:

- `colcon build --packages-up-to <pkg>` and `colcon test --packages-select <pkg>` pass;
  `colcon test-result --verbose` shows no failures.
- `ros2 node list`: each expected node once, in the expected namespace.
- `ros2 topic list -t` and `ros2 topic info -v /<topic>`: types and QoS as designed, publisher and
  subscription counts non-zero.
- `ros2 topic hz /<topic>` and `ros2 topic echo --once /<topic>`: data arrives at the rate and with the
  frame ids you expect.
- `ros2 param dump /<node>`: values match the YAML file.
- `ros2 service list -t`, `ros2 action list -t`: interfaces present with the right types.
- No `incompatible QoS`, `not declared` or exception lines in the launch output.
- For detail, run a node with `--ros-args --log-level <node_name>:=debug`.

## Distro differences

- **Lyrical Luth** (LTS from May 2026): Ubuntu 26.04, Python 3.12 to 3.14, C++20 minimum, Gazebo
  Jetty.
- `ament_target_dependencies()` is deprecated from Kilted on (a warning at every build in Lyrical).
  The `target_link_libraries(... rclcpp::rclcpp ${std_msgs_TARGETS})` form shown here works in Jazzy
  and Lyrical.
- rclcpp subscription callbacks taking `MsgT::SharedPtr` are deprecated in Lyrical; take
  `const MsgT &` or `MsgT::ConstSharedPtr`.
- Lyrical removes `rclcpp::executors::StaticSingleThreadedExecutor` (use `SingleThreadedExecutor`)
  and `rosidl_target_interfaces()` (use `rosidl_get_typesupport_target()`), and deprecates the free
  functions `rclcpp::spin_some` and `rclcpp::spin_all`.
- **Humble**: no `add_pre_set_parameters_callback`/`add_post_set_parameters_callback` (Iron added
  them) and no `ROS_AUTOMATIC_DISCOVERY_RANGE` (use `ROS_LOCALHOST_ONLY`); `LifecycleNode` in
  launch has no `autostart`.

## Related

- References: [python-nodes.md](references/python-nodes.md), [cpp-nodes.md](references/cpp-nodes.md),
  [packages.md](references/packages.md), [launch.md](references/launch.md).
- Wiki: [ROS 2](../../wiki/tools/ros2.md) (CLI), [colcon](../../wiki/tools/colcon.md),
  [tf2](../../wiki/software/tf2.md), [Fast DDS](../../wiki/software/fast-dds.md),
  [Cyclone DDS](../../wiki/software/cyclone-dds.md), [rmw_zenoh](../../wiki/software/rmw-zenoh.md),
  [choose a middleware](../../wiki/guides/choose-a-ros2-middleware.md),
  [PlotJuggler](../../wiki/tools/plotjuggler.md), [Foxglove](../../wiki/tools/foxglove.md).
- Skills: [ros2-robot-description](../ros2-robot-description/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [ros2-web-bridge](../ros2-web-bridge/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md); later: `ops-bringup`, `nav-nav2`, `fw-rtos-micro-ros`.
- Upstream: docs.ros.org/en/jazzy (Concepts: QoS, executors, parameters; Tutorials: client
  libraries, launch, custom interfaces).
