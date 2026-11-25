---
name: ros2-fundamentals
description: >-
  Use when designing, writing, or debugging ROS2 systems — choosing between topics/services/actions, configuring QoS profiles, fixing "no messages received" failures, DDS discovery on WiFi, executor deadlocks, node composition, parameters, and Python launch files. Provides production-grade ROS2 architecture knowledge for code that works on real robots the first time.
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
# ROS2 Fundamentals

This skill covers the ROS2 knowledge that separates working demos from production robots:
communication primitive selection, QoS (the #1 silent failure in all of ROS2), DDS discovery
on real networks, executor/callback-group deadlocks, composition, parameters, and launch.

Target: ROS2 Humble/Iron/Jazzy. `rclpy` and `rclcpp` patterns shown where they differ.

---

## 1. Communication Primitive Selection (Topics vs Services vs Actions)

The selection rule, stated once, correctly:

| Primitive | Use when | Never use for |
|-----------|----------|---------------|
| **Topic** | Continuous data streams; many-to-many; sender doesn't care who listens (sensor data, odometry, cmd_vel, state broadcast) | Request/response logic; anything needing confirmation |
| **Service** | Quick request/response that completes in **< ~1 second** and cannot be preempted (get map, set mode, trigger calibration snapshot) | Anything long-running; anything you might want to cancel; anything needing progress feedback |
| **Action** | Long-running, preemptible goals with feedback (navigate to pose, move arm to joint state, dock, grasp) | High-rate streaming; simple flags |

**Hard rules:**

1. **Never call a service for something that takes more than ~1s.** Service calls block the
   client (or occupy an executor thread). A blocked service call inside a callback is the #1
   deadlock pattern (see §5). If it's long-running, it's an Action. No exceptions.
2. **Never use a topic where you need to know the command was received.** Topics are
   fire-and-forget at the application level even with RELIABLE QoS — reliability guarantees
   delivery to *matched* subscriptions, not that anyone is subscribed or acted on it.
3. **`cmd_vel`-style control is a topic** at fixed rate with a deadman/timeout on the
   receiver: if no message for N ms (typically 200–500 ms), stop the robot. Always implement
   the timeout. A crashed teleop node must not leave the robot driving at last commanded velocity.
4. **Actions are built on 5 underlying topics/services** (goal, cancel, result, feedback,
   status). They are not "heavy" — use them freely for any motion command.

```python
# Action server skeleton (rclpy) — the parts people get wrong
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node

class DockServer(Node):
    def __init__(self):
        super().__init__('dock_server')
        self._as = ActionServer(
            self, Dock, 'dock',
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,          # accept/reject BEFORE execution
            cancel_callback=self.cancel_cb,      # MUST implement or goals can't be canceled
            callback_group=ReentrantCallbackGroup())  # see §5 — execute runs long

    def goal_cb(self, goal_request):
        # Reject here if robot is in a bad state. Do NOT accept-then-abort.
        return GoalResponse.ACCEPT

    def cancel_cb(self, goal_handle):
        return CancelResponse.ACCEPT             # default rejects cancels — always override

    def execute_cb(self, goal_handle):
        rate = self.create_rate(10)
        while not docked:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_robot()                 # cancel MUST leave hardware safe
                return Dock.Result()
            goal_handle.publish_feedback(fb)
            rate.sleep()                          # needs MultiThreadedExecutor (§5)
        goal_handle.succeed()
        return Dock.Result()
```

---

## 2. QoS Profiles — the #1 Silent Failure in ROS2

**The failure mode:** publisher and subscriber both running, topic shows in `ros2 topic list`,
zero messages arrive, **no error anywhere**. Cause: incompatible QoS. This single issue
accounts for more lost engineering hours than any other ROS2 problem.

### Compatibility rules (Request vs Offered — RxO)

A subscription's *requested* QoS must be satisfiable by the publisher's *offered* QoS:

| Policy | Compatible when |
|--------|-----------------|
| Reliability | Pub RELIABLE matches sub RELIABLE or BEST_EFFORT. Pub BEST_EFFORT only matches sub BEST_EFFORT. **Sub RELIABLE + pub BEST_EFFORT = NO MESSAGES.** |
| Durability | Pub TRANSIENT_LOCAL matches sub TRANSIENT_LOCAL or VOLATILE. Pub VOLATILE only matches sub VOLATILE. **Sub TRANSIENT_LOCAL + pub VOLATILE = NO MESSAGES.** |
| Deadline | Pub deadline ≤ sub deadline |
| Liveliness lease | Pub lease ≤ sub lease |

History and depth are **not** compatibility-checked — they're local buffer policy only.

### The standard profiles and when to use each

| Profile | Reliability | Durability | Depth | Use for |
|---------|-------------|------------|-------|---------|
| `qos_profile_sensor_data` | BEST_EFFORT | VOLATILE | 5 | LiDAR, cameras, IMU — anything where the *latest* sample matters and a dropped frame is fine |
| Default (`QoSProfile(depth=10)`) | RELIABLE | VOLATILE | 10 | Commands, state, most things |
| Latched / `TRANSIENT_LOCAL` | RELIABLE | TRANSIENT_LOCAL | 1 | Maps, robot_description, anything published once that late-joining subs need |
| `qos_profile_services_default` | RELIABLE | VOLATILE | 10 | Services (handled internally) |

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from rclpy.qos import qos_profile_sensor_data

# Sensor subscription — matches BEST_EFFORT driver publishers
self.create_subscription(LaserScan, 'scan', self.scan_cb, qos_profile_sensor_data)

# Latched map publisher — late joiners get the last message
map_qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1)
self.map_pub = self.create_publisher(OccupancyGrid, 'map', map_qos)
```

```cpp
// rclcpp equivalents
sub_ = create_subscription<sensor_msgs::msg::LaserScan>(
    "scan", rclcpp::SensorDataQoS(), cb);
map_pub_ = create_publisher<nav_msgs::msg::OccupancyGrid>(
    "map", rclcpp::QoS(1).transient_local());
```

### The classic traps

1. **Subscribing to a sensor driver with default QoS.** Most LiDAR/camera drivers publish
   BEST_EFFORT. Your default-QoS subscription requests RELIABLE → silent no-match. Fix:
   `qos_profile_sensor_data` on the subscription, or better, **adaptive matching**:

```python
# Match whatever the publisher offers (Humble+)
infos = self.get_publishers_info_by_topic('scan')
if infos:
    qos = infos[0].qos_profile
    self.create_subscription(LaserScan, 'scan', self.cb, qos)
```

2. **`/map` or `/robot_description` arrives once then never again for late joiners.**
   Publisher must be TRANSIENT_LOCAL *and* subscriber must request TRANSIENT_LOCAL.
   (`robot_state_publisher` publishes `/robot_description` transient-local since Galactic.)

3. **rosbag replay produces no output.** `ros2 bag play` re-offers recorded QoS; if your
   node's subscription QoS mismatches, silence. Use `--qos-profile-overrides-path`.

### Debugging QoS — do this FIRST when "no messages"

```bash
ros2 topic info /scan --verbose      # shows EVERY endpoint's full QoS — compare pub vs sub
ros2 topic echo /scan --qos-reliability best_effort   # echo with explicit QoS
```

In code, register incompatibility callbacks so mismatches are loud, not silent:

```python
from rclpy.qos_event import SubscriptionEventCallbacks
def incompat_cb(event):
    self.get_logger().error(f'QoS incompatible! total={event.total_count}')
self.create_subscription(LaserScan, 'scan', self.cb, qos,
    event_callbacks=SubscriptionEventCallbacks(incompatible_qos=incompat_cb))
```

**Rule for code generation: every subscription to a sensor topic gets
`qos_profile_sensor_data`; every "publish once, read forever" topic gets
RELIABLE + TRANSIENT_LOCAL depth 1 on BOTH sides. Never leave QoS implicit on these.**

### Other QoS policies that matter in production

- **Deadline**: declare expected publish period; get a callback when missed. Use on safety
  topics (cmd_vel, e-stop heartbeat) instead of hand-rolled watchdog timers.
- **Lifespan**: messages older than N expire from the queue. Use on commands so a robot
  doesn't execute a stale cmd_vel after network recovery.
- **KEEP_LAST depth**: for high-rate sensors, depth 1–5. Large depths on image topics
  silently eat hundreds of MB of RAM.

---

## 3. DDS Discovery on Real Networks (WiFi)

ROS2 discovery uses DDS Simple Discovery: **UDP multicast** announcements
(239.255.0.1, port 7400 + offsets). This works on a desk Ethernet switch and fails
constantly on real robot networks.

### Why WiFi breaks discovery

- Many APs (especially enterprise — Cisco/Aruba/Ubiquiti with "multicast filtering" or
  client isolation) drop or rate-limit multicast.
- Multicast over WiFi is sent at the lowest basic rate with no ACK — lossy by design.
- Symptoms: nodes see each other intermittently, `ros2 node list` differs per machine,
  discovery takes 30+ seconds, topics match then unmatch.

### Diagnosis ladder (run in order)

```bash
# 1. Same ROS_DOMAIN_ID on every machine? (default 0; valid 0-101)
echo $ROS_DOMAIN_ID
# 2. Same RMW on every machine? Cross-vendor (FastDDS↔CycloneDDS) interop is officially
#    supported but is the first thing to eliminate. Standardize:
echo $RMW_IMPLEMENTATION        # rmw_fastrtps_cpp | rmw_cyclonedds_cpp
# 3. Is multicast actually passing? (CycloneDDS ships a tester)
#    machine A: ros2 multicast receive     machine B: ros2 multicast send
# 4. Firewall: UDP 7400-7500 must be open (Ubuntu: ufw status). Windows Defender
#    Firewall blocks DDS by default — allow the app or the port range.
# 5. ROS_LOCALHOST_ONLY=1 set anywhere? It silently confines a machine to loopback.
# 6. Multiple NICs (eth + wlan + docker0)? DDS may announce the wrong interface.
```

### Fix 1 — Pin the network interface (multiple-NIC machines, Docker hosts)

CycloneDDS via `CYCLONEDDS_URI`:

```xml
<!-- cyclonedds.xml -->
<CycloneDDS>
  <Domain>
    <General>
      <Interfaces><NetworkInterface name="wlan0" priority="default"/></Interfaces>
      <AllowMulticast>spdp</AllowMulticast>  <!-- multicast for discovery only,
                                                  unicast for data: best WiFi setting -->
    </General>
  </Domain>
</CycloneDDS>
```
```bash
export CYCLONEDDS_URI=file:///etc/cyclonedds.xml
```

`AllowMulticast: spdp` is the single highest-value CycloneDDS setting for WiFi robots:
discovery still uses multicast (low rate, tolerable) but all user data goes unicast.

### Fix 2 — Static peers (when multicast is fully blocked)

CycloneDDS:
```xml
<Discovery>
  <ParticipantIndex>auto</ParticipantIndex>
  <Peers>
    <Peer address="192.168.1.10"/>
    <Peer address="192.168.1.20"/>
  </Peers>
</Discovery>
```
FastDDS: equivalent `initialPeersList` in an XML profile via `FASTRTPS_DEFAULT_PROFILES_FILE`.

### Fix 3 — FastDDS Discovery Server (recommended for fleets / bad WiFi)

Replaces peer-to-peer multicast discovery with a client-server model (like the old
roscore, but only for discovery — data still flows peer-to-peer):

```bash
# On one stable machine (robot's main computer or a server):
fastdds discovery -i 0 -l 192.168.1.10 -p 11811

# On EVERY node-running machine (including the server machine):
export ROS_DISCOVERY_SERVER=192.168.1.10:11811
```

**Critical gotcha:** with a discovery server, `ros2 topic list` / `ros2 node list` on a
machine won't see anything unless that shell also has `ROS_DISCOVERY_SERVER` set AND the
daemon is restarted as a *super client*:

```bash
ros2 daemon stop
export ROS2_EASY_MODE=...   # or use a super-client XML profile
# Simplest: super-client profile
export FASTRTPS_DEFAULT_PROFILES_FILE=/path/super_client.xml
ros2 daemon stop && ros2 daemon start
```

### Domain ID hygiene

- Each robot on a shared network gets its own `ROS_DOMAIN_ID` (1–101). Two robots on
  domain 0 on the same lab WiFi WILL cross-subscribe — a real robot has driven off
  because it received another robot's cmd_vel.
- Domain IDs above 101 overflow the UDP port calculation on some platforms — stay ≤ 101.
- ~120 participants max per domain per machine before port exhaustion; one participant
  per *process* (not per node) since Foxy.

---

## 4. Executors — How Callbacks Actually Run

- **SingleThreadedExecutor** (default for `rclpy.spin(node)`): one callback at a time,
  ever. Simple, deterministic, and the source of every "my node froze" bug.
- **MultiThreadedExecutor**: thread pool; concurrency governed by callback groups (§5).
- **EventsExecutor** (rclcpp; rclpy in Jazzy+): push-based, much lower overhead and jitter
  than the default wait-set executor. Use for high-rate control nodes in C++.

```python
from rclpy.executors import MultiThreadedExecutor
executor = MultiThreadedExecutor(num_threads=4)
executor.add_node(node)
try:
    executor.spin()
finally:
    node.destroy_node()
    rclpy.shutdown()
```

**Performance note (rclpy):** Python's GIL means MultiThreadedExecutor gives concurrency
(overlapping waits) but not parallelism (overlapping CPU work). CPU-heavy callbacks in
Python block everything regardless — push heavy compute to C++ nodes or worker processes.

---

## 5. Callback Groups and the Deadlock Patterns

Callback groups define what may run concurrently under a MultiThreadedExecutor:

- **MutuallyExclusiveCallbackGroup (MECG)** — default. Callbacks in the same group never
  overlap each other.
- **ReentrantCallbackGroup (RCG)** — anything in the group may run concurrently,
  including multiple invocations of the *same* callback.

### Deadlock Pattern #1 — sync service call inside a callback (THE classic)

```python
# DEADLOCK with SingleThreadedExecutor, or same MECG on multi-threaded:
def timer_cb(self):
    future = self.client.call_async(req)
    rclpy.spin_until_future_complete(self, future)   # NEVER do this inside a callback
    # or: result = future.result() after a blocking wait
```

Why: the response arrives as another callback. The executor thread is stuck inside
`timer_cb`, so the response callback can never run. Hang forever, no error.

**Fixes, in order of preference:**

```python
# Fix A (best): stay async — chain a done-callback. Works on ANY executor.
def timer_cb(self):
    future = self.client.call_async(req)
    future.add_done_callback(self.handle_response)

def handle_response(self, future):
    result = future.result()

# Fix B: MultiThreadedExecutor + put client and timer in DIFFERENT groups
self.cb_group_timer = MutuallyExclusiveCallbackGroup()
self.cb_group_client = MutuallyExclusiveCallbackGroup()
self.client = self.create_client(SetMode, 'set_mode', callback_group=self.cb_group_client)
self.timer = self.create_timer(1.0, self.timer_cb, callback_group=self.cb_group_timer)
# now spin_until_future_complete inside timer_cb can complete — but Fix A is still cleaner.
```

The same rule applies in rclcpp: a sync `client->async_send_request(req).get()` inside a
callback deadlocks a single-threaded executor. Use a separate callback group +
MultiThreadedExecutor, or chain with the future's callback overload.

### Deadlock Pattern #2 — `create_rate().sleep()` in a callback

`rate.sleep()` in rclpy is serviced by a ROS timer — which needs the executor to spin.
Sleeping inside a callback on a SingleThreadedExecutor blocks the executor → the rate
timer never fires → sleep never returns. Action server execute callbacks that loop with
a rate (§1 example) **require** MultiThreadedExecutor + the server in a Reentrant or
separate group. Alternatively use `time.sleep()` (wall time, no executor dependency)
if you don't need sim-time correctness.

### Deadlock Pattern #3 — thread-pool exhaustion

MultiThreadedExecutor with N threads, N long-running callbacks in Reentrant groups
(e.g., N goals on an action server, each blocking) → no threads left for the callbacks
they're waiting on. Bound concurrent goals, or size `num_threads` ≥ max concurrent
long-running callbacks + 2.

### Group assignment recipe (use as default for generated code)

- Fast, independent callbacks (sensor subs, state pubs): default group is fine.
- Action server `execute_callback`: ReentrantCallbackGroup.
- Any callback that waits on a service/action result: that client goes in its OWN group,
  or (better) rewrite with `add_done_callback`.
- Anything touching shared mutable state: same MECG (it's a free mutex) OR explicit locks
  with Reentrant.

---

## 6. Composition vs Standalone Nodes

A standalone node = one process. A *component* = node compiled as a shared library,
loaded into a `component_container` process. In-container, pub/sub between components
uses **intra-process communication**: zero-copy (unique_ptr messages) instead of
serialize → DDS loopback → deserialize.

**When composition matters:** camera driver → rectify → detect pipelines moving images
at 30 fps. Inter-process, each hop serializes multi-MB messages; composed with
`use_intra_process_comms`, hops are pointer moves. This is the difference between 80%
CPU and 8% on an embedded board. Nav2 and image_pipeline ship as components for this reason.

**When NOT to compose:** Python nodes (rclpy has no composition — components are
rclcpp-only); nodes you want to crash-isolate (one segfaulting component kills the
whole container); during early development (separate processes are easier to debug/restart).

```cpp
// Component boilerplate (rclcpp)
#include <rclcpp_components/register_node_macro.hpp>
namespace my_pkg {
class Rectify : public rclcpp::Node {
public:
  explicit Rectify(const rclcpp::NodeOptions & options)
  : Node("rectify", options) { /* MUST take NodeOptions; no main() */ }
};
}
RCLCPP_COMPONENTS_REGISTER_NODE(my_pkg::Rectify)
```

```python
# Launch: composed container with intra-process comms
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

container = ComposableNodeContainer(
    name='camera_container', namespace='', package='rclcpp_components',
    executable='component_container_mt',   # _mt = multi-threaded executor
    composable_node_descriptions=[
        ComposableNode(package='my_pkg', plugin='my_pkg::Rectify', name='rectify',
                       extra_arguments=[{'use_intra_process_comms': True}]),
    ])
```

Intra-process gotchas: only KEEP_LAST QoS, no TRANSIENT_LOCAL; publish `unique_ptr`
to get true zero-copy; services/actions are NOT intra-process (still go through RMW).

---

## 7. Parameter System

Parameters are per-node, typed, declared-before-use (undeclared parameter access throws).

```python
class Controller(Node):
    def __init__(self):
        super().__init__('controller')
        # Declare with defaults and (optionally) descriptors/ranges
        self.declare_parameter('max_vel', 0.5)
        self.declare_parameter('wheel_base', 0.32)
        self.max_vel = self.get_parameter('max_vel').value

        # Runtime reconfigure: validate BEFORE accepting. This callback runs
        # pre-change; returning successful=False rejects the set.
        self.add_on_set_parameters_callback(self.param_cb)

    def param_cb(self, params):
        from rcl_interfaces.msg import SetParametersResult
        for p in params:
            if p.name == 'max_vel':
                if not (0.0 < p.value <= 2.0):
                    return SetParametersResult(successful=False,
                                               reason='max_vel must be in (0, 2.0]')
                self.max_vel = p.value
        return SetParametersResult(successful=True)
```

**Rules that matter:**

- `add_on_set_parameters_callback` fires for *every* set including initial launch-file
  values — your validator must accept the defaults.
- The callback validates; it should also be where you cache the value. Don't call
  `get_parameter()` in a hot loop (it takes a lock).
- YAML param files: node-name keyed, with the mandatory `ros__parameters` key:

```yaml
/controller:                # or controller: ; leading / matters with namespaces
  ros__parameters:
    max_vel: 0.5
    wheel_base: 0.32
```

- A wrong node name or missing `ros__parameters` key in YAML fails **silently** — the
  node just uses defaults. When params "don't apply", check
  `ros2 param get /controller max_vel` against the file first.
- Type is fixed at declaration: declaring `0` (int) then setting `0.5` from YAML throws.
  Write float defaults as `0.0`, not `0`.
- Global-ish config: there is no parameter server. Share via YAML files loaded into
  multiple nodes, or a dedicated node that others query with `ros2 param`/client API.

---

## 8. Launch Files (Python)

```python
# bringup.launch.py — the canonical production pattern
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    params_file = PathJoinSubstitution(
        [FindPackageShare('my_bringup'), 'config', 'controller.yaml'])

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('with_rviz', default_value='false'),

        Node(
            package='my_pkg', executable='controller', name='controller',
            output='screen',
            emulate_tty=True,                      # without this, Python logs buffer
            parameters=[params_file, {'use_sim_time': use_sim_time}],
            remappings=[('cmd_vel', 'cmd_vel_nav')],
            respawn=True, respawn_delay=2.0,       # production: auto-restart drivers
        ),

        Node(package='rviz2', executable='rviz2',
             condition=IfCondition(LaunchConfiguration('with_rviz'))),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution(
                [FindPackageShare('nav2_bringup'), 'launch', 'navigation_launch.py'])),
            launch_arguments={'use_sim_time': use_sim_time,
                              'params_file': params_file}.items()),
    ])
```

**Launch knowledge that prevents real bugs:**

- **Substitutions are lazy.** `LaunchConfiguration('x')` is not a string at
  `generate_launch_description()` time. You cannot `if use_sim_time == 'true':` in
  Python — use `IfCondition`/`UnlessCondition`, or `OpaqueFunction` when you genuinely
  need the resolved value to compute things.
- **`use_sim_time` must reach EVERY node** when running under Gazebo/Isaac, or TF
  timestamps mix wall-clock and sim-clock and `lookup_transform` fails with
  extrapolation errors. Pass it explicitly in every `parameters=[...]`.
- **Startup ordering:** ROS2 launch has no depends-on. Use
  `RegisterEventHandler(OnProcessStart/OnProcessExit(...))` for hard ordering
  (e.g., spawn controller only after `gazebo` spawner exits), or lifecycle nodes +
  `nav2_lifecycle_manager`-style managers. `TimerAction(period=5.0, actions=[...])`
  is acceptable for prototypes only — it WILL flake on slow boots.
- **`emulate_tty=True` + `output='screen'`** on Python nodes, or you'll think logging
  is broken (it's just block-buffered).
- Remap in launch, not in code. Hardcoded topic names in node source are a smell; nodes
  should use simple relative names ('scan', 'cmd_vel') and launch wires the graph.
- Install launch/config dirs in `setup.py` (ament_python) or `CMakeLists.txt`
  (`install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})`) — the #1
  "launch file not found" cause is a missing install rule + stale overlay.

---

## 9. Debugging Methodology — "No Messages" Checklist

Run in this exact order; stop at the first failure:

```bash
# 0. Daemon serves stale graph info constantly. When CLI output looks wrong:
ros2 daemon stop && ros2 daemon start

# 1. Do both endpoints exist?
ros2 topic info /scan --verbose          # count pubs and subs; READ THE QoS BLOCKS

# 2. QoS compatible? (§2 rules). 90% of cases end here.

# 3. Is data flowing at the wire level?
ros2 topic hz /scan                      # publisher side OK?
ros2 topic echo /scan --once             # CLI sub may itself QoS-mismatch; add
ros2 topic echo /scan --qos-reliability best_effort --qos-durability volatile

# 4. Same domain / same RMW / discovery working? (§3 ladder)

# 5. Type match? A pub of sensor_msgs/LaserScan and sub of a different .msg checksum
#    silently won't match:
ros2 topic type /scan

# 6. Is the subscriber's executor actually spinning? A node whose spin thread is
#    blocked (deadlock §5) has matched subscriptions and receives nothing visibly.
#    py-spy dump --pid <PID>   (Python)  /  gdb -p <PID>, thread apply all bt  (C++)
```

Tools to reach for: `rqt_graph` (mismatched-QoS edges shown dashed in recent versions),
`ros2 doctor --report`, `ros2 wtf`, and for DDS-level inspection Wireshark with the RTPS
dissector (filter `rtps`).

---

## 10. Defaults for Generated Code (summary contract)

When generating ROS2 code, apply these unless the user specifies otherwise:

1. Sensor subscriptions → `qos_profile_sensor_data`. Latched data → RELIABLE +
   TRANSIENT_LOCAL depth 1 both sides. Never default-QoS a sensor or map topic.
2. Long-running operations → Actions with cancel implemented and hardware-safe cancel
   semantics. Services only for <1 s, non-preemptible calls.
3. Never block inside a callback waiting on a ROS future on the same executor.
   Prefer `add_done_callback` chaining; otherwise MultiThreadedExecutor + separate
   callback groups, stated explicitly in the code.
4. Every velocity-command consumer implements a command timeout that stops the robot.
5. Parameters: declared with typed defaults (floats as `0.0`), validated in
   `add_on_set_parameters_callback`, loaded from YAML with correct node name +
   `ros__parameters` key.
6. Launch: Python launch files, `use_sim_time` threaded to all nodes, `emulate_tty=True`,
   install rules included, event handlers (not sleeps) for ordering.
7. High-rate C++ image/pointcloud pipelines → composable nodes with
   `use_intra_process_comms: true` in a `component_container_mt`.
8. Multi-machine/WiFi deployments → pin RMW vendor on all machines, document
   `ROS_DOMAIN_ID`, and ship a CycloneDDS XML with `AllowMulticast: spdp` or a FastDDS
   discovery-server config.
