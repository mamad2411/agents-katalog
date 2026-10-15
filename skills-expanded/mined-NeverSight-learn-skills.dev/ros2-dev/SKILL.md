---
name: ros2-dev
description: >
  Expert guidance for ROS 2 (Jazzy) development in Python (rclpy) and C++ (rclcpp).
  Use whenever the user works with ROS 2 nodes, topics, services, actions, QoS,
  parameters, lifecycle nodes, executors, callback groups, launch files, colcon/ament
  builds, package.xml/setup.py, tf2, URDF/Xacro, DDS (Fast-DDS, Cyclone DDS), or ros2
  CLI tools (run, launch, topic, node, service, param, bag, doctor). Also trigger on
  implicit cues: "my node can't see the topic", "messages aren't arriving", "callback
  not firing", "QoS mismatch", "transform lookup failed", "colcon build fails", "launch
  file not working", "which message type for", "how do I make two nodes talk", "robot
  not moving", "how to test a ROS node". ALSO use for ROS 2 + Gazebo simulation
  debugging -- whenever the user mentions Gazebo, gz sim, ros_gz_bridge, use_sim_time,
  /clock, sim-to-real, or reports "the laser scan drifts when the robot turns", "the
  map gets corrupted", "odom doesn't match", "the robot tips over in Gazebo", "the scan
  is stuck", or any case where a ROS 2 graph and a physics simulator disagree -- even
  if they don't say "ROS 2" explicitly.
---

# ROS 2 Development Companion

> **Quick navigation**
> - Node structures, callbacks, executors, lifecycle nodes --> `references/node-patterns.md`
> - Topics, services, actions, QoS profiles, custom messages --> `references/communication.md`
> - Workspace layout, colcon, ament, package creation --> `references/workspace-build.md`
> - Launch files, arguments, composition, namespaces --> `references/launch-files.md`
> - Coordinate frames, tf2, URDF, Xacro --> `references/tf2-urdf.md`
> - CLI tools, rqt, RViz, DDS, logging, ros2 bag --> `references/debugging.md`
> - Unit tests, integration tests, launch_testing, CI/CD --> `references/testing.md`
> - Simulation debugging (Gazebo): odom-vs-physics, sim_time, drift --> `references/simulation-debugging.md`
> - Ready-to-use diagnostic scripts (sim ground-truth comparison) --> `scripts/`

---

## Core Philosophy: The ROS 2 Mindset

The fundamental paradigm shift in robotics is this: **traditional software is
request/response; robots are continuous data streams.**

In a typical application, a client sends a request, a server processes it, and returns
a response. The server is idle between requests. In robotics, sensors produce data
continuously (30 Hz camera, 10 Hz LiDAR, 100 Hz IMU), processing nodes transform
that data continuously, and actuator nodes consume commands continuously. There is
no "idle."

**Think of ROS 2 as a distributed event bus, not a request/response system.**

| ROS 2 Concept | Description |
|---|---|
| Service (`/srv`) | Request/reply for occasional queries -- NOT the main data path |
| Topic (`/topic`) | The primary communication pattern -- continuous, decoupled pub/sub |
| Topic with QoS | Topics function as message queues with configurable reliability and durability |
| Action (`/action`) | Goal + progress feedback + result -- used for "do this and tell me how it's going" |
| Node | An independent process with its own callbacks and state |
| Launch file | Orchestrates which nodes start, with what parameters and connections; declares the system topology |
| Callback | Functions triggered by incoming messages, timers, or service requests |
| Parameter server | Runtime configuration injected at launch |

### The Three Laws of ROS 2 Development

1. **Never block a callback.** Callbacks run on executor threads. A blocked callback
   means missed messages. If you need to do slow work, use a separate thread or
   break the work into stages.

2. **Never assume message delivery.** Topics are lossy by default (best-effort QoS).
   Even with reliable QoS, network partitions happen. Design nodes to handle missing
   data gracefully.

3. **Never use global state across callbacks.** Each callback may run on a different
   thread (MultiThreadedExecutor). Use node-scoped state with proper synchronization.

---

## Decision Table: Python vs C++ for This Node

ROS 2 supports both Python (rclpy) and C++ (rclcpp). For teams starting out,
**default to Python** unless you have a specific reason for C++.

| Criterion | Choose Python (rclpy) | Choose C++ (rclcpp) |
|---|---|---|
| Learning curve | Lower -- familiar syntax | Higher -- memory management, build system |
| Iteration speed | Fast -- no compile step | Slower -- colcon build on every change |
| Performance need | Sufficient for < 30 Hz processing | Required for > 100 Hz or real-time control |
| Image/point cloud processing | OK for prototyping, NumPy helps | Required for production throughput |
| Hardware drivers | OK for serial/I2C prototyping | Preferred for production drivers |
| Interop with ML | Natural -- Python ML ecosystem | Requires bindings or separate process |
| Debugging | pdb, print, easy introspection | gdb, more complex but more powerful |

**Recommendation:** Write everything in Python first. Port individual nodes to C++ only
when profiling shows Python is the bottleneck. ROS 2 is designed for mixed-language
systems -- Python and C++ nodes communicate identically over topics/services/actions.

---

## Decision Table: Which QoS Profile?

QoS (Quality of Service) controls message delivery guarantees. A **mismatch between
publisher and subscriber QoS causes silent failure** -- no error, just no messages.

| Data Type | Reliability | Durability | History Depth | Example Profile |
|---|---|---|---|---|
| Sensor stream (camera, LiDAR, IMU) | Best Effort | Volatile | 1-5 | `SensorDataQoS()` |
| Robot commands (cmd_vel) | Reliable | Volatile | 1 | Custom reliable |
| Map data (occupancy grid) | Reliable | Transient Local | 1 | `QoSProfile(depth=1, durability=TRANSIENT_LOCAL)` |
| Diagnostics / status | Reliable | Volatile | 10 | `qos_profile_system_default` |
| Parameter events | Reliable | Transient Local | Keep All | Built-in |
| tf2 transforms | Reliable | Volatile | 100 | Built-in tf2 QoS |
| tf2 static transforms | Reliable | Transient Local | Keep All | Built-in static tf2 QoS |

**The #1 QoS Gotcha:** If a publisher uses Best Effort and a subscriber uses Reliable,
the subscriber will never receive messages. No error. No warning. Just silence. Always
check QoS compatibility first when debugging "topic not showing up."

```python
# Quick QoS profiles for common cases
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

SENSOR_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=5
)

RELIABLE_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)

LATCHED_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1
)
```

---

## Decision Table: Which Executor Model?

Executors determine how callbacks are scheduled. Think of them as the event loop.

| Executor | Threading | Use When |
|---|---|---|
| `SingleThreadedExecutor` | One thread | Simple nodes, no parallelism needed -- single-threaded event loop |
| `MultiThreadedExecutor` | Thread pool | Multiple independent callbacks that can run in parallel |
| `StaticSingleThreadedExecutor` | One thread, static schedule | Performance-critical, known callback set |

```python
# Default: single-threaded (safe, simple)
rclpy.spin(node)

# Multi-threaded: when you need parallel callback execution
from rclpy.executors import MultiThreadedExecutor
executor = MultiThreadedExecutor(num_threads=4)
executor.add_node(node)
executor.spin()
```

**With MultiThreadedExecutor, you MUST use callback groups** to control which callbacks
can run in parallel. See `references/node-patterns.md` for details.

---

## Node Architecture Selection

| Node Type | Complexity | Use When |
|---|---|---|
| **Simple node** (subclass `Node`) | Lowest | Quick prototyping, single-purpose nodes |
| **Lifecycle node** (subclass `LifecycleNode`) | Medium | Nodes that need orderly startup/shutdown, hardware drivers |
| **Component node** (loaded into a container) | Medium | Zero-copy intra-process communication, reducing process count |

**Start with simple nodes.** Move to lifecycle nodes when you need deterministic
startup ordering (e.g., "configure the camera before the detector starts"). Move to
component nodes when profiling shows IPC overhead matters.

See `references/node-patterns.md` for implementation patterns for each type.

---

## Anti-Patterns Table

These are the most common mistakes made by developers new to ROS 2.

| Anti-Pattern | Why It's Wrong | What To Do Instead |
|---|---|---|
| **Treating topics like HTTP endpoints** | Topics are continuous streams, not request/response. Don't publish a message and wait for a reply on another topic. | Use a Service for request/response. Use topics for streaming data. |
| **Using global state across callbacks** | With MultiThreadedExecutor, callbacks run on different threads. Global state causes race conditions. | Store state on the node instance. Use locks if shared across callback groups. |
| **Blocking in callbacks** | A blocked callback stalls the executor. Other subscriptions stop receiving. The node appears dead. | Use async patterns, break work into stages, or offload to a worker thread. |
| **Polling instead of subscribing** | Creating a timer that calls a service every 100ms to check for new data. | Subscribe to the topic -- ROS 2 will call your callback when data arrives. |
| **One giant node** | Putting all logic in a single node. Hard to test, reuse, or distribute. | One node per responsibility. Connect via topics/services. |
| **Ignoring QoS** | Using default QoS everywhere, then wondering why sensor data is unreliable or map data is missing. | Match QoS to data type. See the QoS table above. |
| **String-typing topic names** | Hardcoding `/camera/image_raw` everywhere. Typos cause silent failures. | Use remapping in launch files. Declare topic names as parameters. |
| **Not using `try`/`except` in callbacks** | An unhandled exception in a callback kills the node silently. | Wrap callback bodies in try/except, log the error, and continue. |
| **Sleeping in callbacks** | Using `time.sleep()` to wait for something. | Use ROS 2 timers, or restructure as a state machine. |
| **Creating publishers/subscribers in callbacks** | Dynamically creating comms objects at runtime. | Create all publishers/subscribers in `__init__` or lifecycle `on_configure`. |

---

## Common Beginner Error Diagnosis

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ros2 topic list` shows my topic but `ros2 topic echo` shows nothing | QoS mismatch between publisher and the echo tool | Add `--qos-reliability best_effort` to echo command, or fix publisher QoS |
| Node starts but callback never fires | Forgot to call `rclpy.spin()` or executor is not spinning | Ensure `rclpy.spin(node)` is called after node creation |
| `ros2 topic echo` works but my subscriber gets nothing | QoS mismatch between publisher and your subscriber | Match QoS profiles -- check reliability and durability settings |
| "Could not find requested resource" at build time | Missing dependency in `package.xml` | Add `<depend>package_name</depend>` to package.xml |
| "No executable found" with `ros2 run` | Missing entry point in `setup.py` or `setup.cfg` | Add console_scripts entry point; run `colcon build` again |
| Transform lookup fails with "Could not find a connection" | Missing tf2 broadcaster or frame name typo | Check `ros2 run tf2_tools view_frames`; verify frame names |
| Node can't find another node's topics | Different `ROS_DOMAIN_ID` or DDS discovery issue | Ensure same `ROS_DOMAIN_ID`; check `ROS_LOCALHOST_ONLY`; check firewall |
| micro-ROS topics missing from `ros2 topic list` (Docker) | Three independent causes — see debugging.md micro-ROS section | (1) Firmware domain 0 ≠ stack domain: use `rcl_init_options_set_domain_id()` in firmware. (2) Cyclone DDS on `lo`, Fast DDS on `eth0`: change cyclonedds.xml to `eth0`. (3) Agent entrypoint overrides `FASTRTPS_DEFAULT_PROFILES_FILE` silently. |
| micro-ROS topics appear then vanish | XRCE session churn from random `client_key` | Derive `client_key` from MAC address via `rmw_uros_options_set_client_key()` — stable key = instant `re-established` instead of full discovery cycle |
| `colcon build` succeeds but changes don't take effect | Forgot to source the workspace overlay | Run `source install/setup.bash` after every build |
| Launch file fails with "Package not found" | Package not built or workspace not sourced | Build with `colcon build`, then source `install/setup.bash` |
| Message type shows as "unknown" | Custom message package not built or not sourced | Build the message package first; source workspace; rebuild dependent packages |
| Subscriber receives messages out of order | History depth too small or network jitter | Increase QoS history depth; add timestamp-based reordering in callback |
| Node uses 100% CPU | Spin rate too high or busy-wait loop in callback | Use appropriate timer period; avoid busy-wait; check for infinite loops |
| "Publisher already destroyed" error | Node was destroyed while publisher was still in use | Ensure proper shutdown order; use lifecycle nodes for deterministic cleanup |
| Parameters not loading from launch file | Parameter name mismatch or wrong node name in launch | Verify parameter names match `declare_parameter()` calls; check node name |
| (Sim) Laser scan / map / robot all "drift" when the robot turns | Drive-plugin odometry decoupled from the simulator's physics | Compare `/odom` against the simulator's ground-truth pose — see `references/simulation-debugging.md`; run `scripts/sim_motion_check.py` |
| (Sim) Everything timestamped billions of seconds stale | A ROS-side node missing `use_sim_time` (often `robot_state_publisher` or the viewer bridge) | Check `ros2 param get /<node> use_sim_time` for **every** node — see simulation-debugging.md §5 |
| (Sim) Scan appears stuck / lags during motion in Foxglove or RViz | Viewer's TF buffer QoS history depth too shallow for fast `/tf` | Raise the viewer bridge's max QoS history depth — see simulation-debugging.md §9 |
| (Sim) Robot tips over or pitches shortly after spawn | Unstable footprint (e.g. two wheels on one transverse axis) | Add fore/aft passive caster support — see simulation-debugging.md §7 |
| (Sim) Sensor frame and physics disagree by a fixed offset | URDF and a parallel SDF model have drifted apart | Unify on one URDF with `<gazebo>` extension blocks — see simulation-debugging.md §6 |
| (Sim) GPU sensor topic (`/scan` etc.) exists but `ros2 topic hz` shows nothing; data appears only while `gz topic -e` runs | Lazy `ros_gz_bridge` never subscribes, so the `gpu_lidar` never ticks | Set `lazy: false` on the bridge entry — see simulation-debugging.md §8b |
| (Sim) Whole sim runs in slow motion; all sensors/odom at a fraction of configured rate | A heavy mesh used as `<collision>` geometry tanks real-time factor | Check RTF; give `<collision>` a primitive, keep the mesh for `<visual>` — see simulation-debugging.md §8c |

---

## Coding Conventions Summary

See individual reference files for full details. Key rules for this team:

### Python (rclpy) -- Primary Language

- **Node names**: `snake_case` -- e.g., `lidar_processor`, `camera_driver`
- **Topic names**: `snake_case` with namespace -- e.g., `/robot/cmd_vel`, `/sensors/imu/data`
- **Package names**: `snake_case` -- e.g., `my_robot_perception`
- **File names**: `snake_case.py` -- e.g., `lidar_processor_node.py`
- **Class names**: `PascalCase` -- e.g., `LidarProcessorNode`
- **Callbacks**: `_callback` suffix -- e.g., `image_callback`, `timer_callback`
- **Parameters**: Declare all in `__init__` with defaults and descriptions
- **Logging**: Use `self.get_logger().info()`, never `print()`

### C++ (rclcpp) -- For Performance-Critical Nodes

- Follow the same naming for nodes, topics, packages
- **Files**: `snake_case.cpp` / `snake_case.hpp`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case`
- **Member variables**: `trailing_underscore_`

### General ROS 2 Conventions

- Follow **REP 103** for units (SI) and coordinate frames (x-forward, y-left, z-up)
- Follow **REP 105** for standard frame names (map, odom, base_link)
- Follow standard ROS 2 naming conventions for topics (lowercase, namespaced)
- Use existing message types from `std_msgs`, `sensor_msgs`, `geometry_msgs`, `nav_msgs`
  before creating custom messages
- Prefix custom message packages with your project name -- e.g., `my_robot_msgs`

---

## Package Organization Example

Recommended package structure for an inspection robot:

```
my_robot_ws/
  src/
    my_robot_bringup/       # Launch files, configs, system startup
    my_robot_description/   # URDF/Xacro, meshes, robot model
    my_robot_msgs/          # Custom message/service/action definitions
    my_robot_perception/    # Camera, LiDAR processing nodes
    my_robot_navigation/    # Path planning, obstacle avoidance
    my_robot_control/       # Motor control, velocity commands
    my_robot_detection/     # Object/defect detection, analysis
    my_robot_teleop/        # Manual control interface
    my_robot_simulation/    # Gazebo worlds, sim-specific launch
```

Each package should have a single, clear responsibility. Packages communicate only
through ROS 2 interfaces (topics, services, actions) -- never by importing each
other's Python modules directly.

---

## Message Type Selection Guide

Choosing the right message type is a common stumbling block. Use existing messages
from standard packages before creating custom ones.

| You Want To Send | Message Type | Package |
|---|---|---|
| Robot velocity command | `Twist` | geometry_msgs |
| Robot position | `Pose` / `PoseStamped` | geometry_msgs |
| Robot position + velocity | `Odometry` | nav_msgs |
| 2D LiDAR scan | `LaserScan` | sensor_msgs |
| 3D point cloud | `PointCloud2` | sensor_msgs |
| Camera image | `Image` | sensor_msgs |
| Camera calibration | `CameraInfo` | sensor_msgs |
| IMU data | `Imu` | sensor_msgs |
| GPS fix | `NavSatFix` | sensor_msgs |
| Joint positions | `JointState` | sensor_msgs |
| 2D map | `OccupancyGrid` | nav_msgs |
| Planned path | `Path` | nav_msgs |
| Battery status | `BatteryState` | sensor_msgs |
| Simple string / number | `String` / `Float64` / `Int32` | std_msgs |
| Boolean flag | `Bool` | std_msgs |
| Coordinate transform | `TransformStamped` | geometry_msgs |
| Wrench (force + torque) | `WrenchStamped` | geometry_msgs |
| Diagnostic info | `DiagnosticArray` | diagnostic_msgs |

**When to create a custom message:**
- None of the standard types fit your data
- You need domain-specific fields (e.g., `PipeDefect` with defect_type, confidence)
- You need to bundle multiple pieces of related data

**When NOT to create a custom message:**
- A standard type almost works -- use it and ignore unused fields
- You just need a label on data -- use the Header.frame_id field
- You just need a simple value -- use std_msgs

---

## ROS 2 Jazzy Environment Setup

### Prerequisites (Ubuntu 24.04)

```bash
# Set locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 apt repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | \
  sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 Jazzy
sudo apt update
sudo apt install ros-jazzy-desktop  # Full desktop (recommended)
# or: sudo apt install ros-jazzy-ros-base  # Minimal (headless robots)

# Install development tools
sudo apt install python3-colcon-common-extensions python3-rosdep python3-vcstool

# Initialize rosdep
sudo rosdep init
rosdep update

# Source ROS 2 in every terminal
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Verify Installation

```bash
# Check ROS 2 is working
echo $ROS_DISTRO
ros2 doctor

# Run a demo
ros2 run demo_nodes_cpp talker &
ros2 run demo_nodes_py listener
# You should see "I heard: [Hello World: N]"
```

### Recommended DDS Configuration

For a small team on a local network, Cyclone DDS is simpler and more reliable
than the default Fast-DDS:

```bash
sudo apt install ros-jazzy-rmw-cyclonedds-cpp
echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
source ~/.bashrc
```

---

## Naming Convention Quick Reference

Consistent naming prevents the most common class of bugs (silent connection
failures due to typos).

| Thing | Convention | Example |
|---|---|---|
| Package name | `snake_case` | `my_robot_perception` |
| Node name | `snake_case` | `defect_detector` |
| Topic name | `snake_case`, with `/` hierarchy | `/sensors/camera/image_raw` |
| Service name | `snake_case` | `/inspection/analyze_section` |
| Action name | `snake_case` | `/navigation/follow_path` |
| Parameter name | `snake_case` | `confidence_threshold` |
| Frame ID | `snake_case` | `camera_link`, `base_link` |
| Message type | `PascalCase` | `DetectedObject.msg` |
| Python file | `snake_case.py` | `defect_detector_node.py` |
| Python class | `PascalCase` | `DefectDetectorNode` |
| Callback method | `_callback` suffix | `scan_callback`, `timer_callback` |
| Launch file | `snake_case.launch.py` | `robot.launch.py` |
| Config file | `snake_case.yaml` | `camera_params.yaml` |

---

## Common ROS 2 CLI Commands Reference

| Task | Command |
|---|---|
| List all nodes | `ros2 node list` |
| Node details | `ros2 node info /node_name` |
| List topics | `ros2 topic list -t` |
| Echo topic data | `ros2 topic echo /topic_name` |
| Check topic rate | `ros2 topic hz /topic_name` |
| Publish test message | `ros2 topic pub /topic_name msg/Type "{field: value}"` |
| List services | `ros2 service list` |
| Call a service | `ros2 service call /srv_name type "{field: value}"` |
| List parameters | `ros2 param list /node_name` |
| Get parameter | `ros2 param get /node_name param_name` |
| Set parameter | `ros2 param set /node_name param_name value` |
| View frames | `ros2 run tf2_tools view_frames` |
| Echo transform | `ros2 run tf2_ros tf2_echo frame1 frame2` |
| Record bag | `ros2 bag record -a` |
| Play bag | `ros2 bag play bag_name` |
| Build workspace | `colcon build --symlink-install` |
| Build one package | `colcon build --packages-select pkg_name` |
| Run tests | `colcon test && colcon test-result --verbose` |
| System check | `ros2 doctor --report` |

---

## Emergency Cheat Sheet

When things go wrong, run these commands in order:

```bash
# 1. Is ROS 2 working at all?
ros2 doctor --report

# 2. What nodes are running?
ros2 node list

# 3. What topics exist?
ros2 topic list -t    # -t shows message types

# 4. Is data flowing on a topic?
ros2 topic hz /my_topic        # message rate
ros2 topic echo /my_topic      # actual data (add --qos-reliability best_effort if needed)

# 5. Can nodes see each other?
ros2 node info /my_node        # shows subscribers, publishers, services

# 6. Is tf2 working?
ros2 run tf2_tools view_frames  # generates frames.pdf

# 7. What's the QoS on a topic?
ros2 topic info /my_topic -v   # -v shows QoS details

# 8. Nuclear option: restart DDS discovery
export ROS_LOCALHOST_ONLY=1    # restrict to localhost
# or kill and restart the daemon:
ros2 daemon stop && ros2 daemon start
```

---

## Reference File Index

| File | Read When |
|---|---|
| `references/node-patterns.md` | Creating nodes, choosing node type, handling callbacks, managing parameters, lifecycle nodes |
| `references/communication.md` | Publishing/subscribing, services, actions, QoS configuration, custom messages |
| `references/workspace-build.md` | Setting up workspace, creating packages, build issues, dependencies |
| `references/launch-files.md` | Launching multi-node systems, arguments, remapping, composition |
| `references/tf2-urdf.md` | Coordinate frames, transforms, robot description, sensor mounting |
| `references/debugging.md` | Diagnosing issues, CLI tools, visualization, logging, recording data |
| `references/simulation-debugging.md` | Gazebo sim debugging — odom-vs-physics divergence, `use_sim_time` propagation, URDF `<gazebo>` extensions vs parallel SDF, physical-stability faults, sensor self-occlusion, viewer display-frame issues, the sim diagnostic ladder |
| `references/testing.md` | Unit testing nodes, integration testing, launch tests, CI/CD |
