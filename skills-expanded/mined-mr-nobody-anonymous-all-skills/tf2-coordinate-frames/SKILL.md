---
name: tf2-coordinate-frames
description: "Use when writing or debugging ROS 2 code that publishes, listens to, or transforms between coordinate frames (TF2): map/odom/base_link trees, static vs dynamic transforms, lookup timeouts, extrapolation errors, multi-robot namespacing. Provides REP-103/REP-105 conventions, exact frame contracts, working rclpy/rclcpp patterns, and a debugging checklist that resolves 95% of TF errors."
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


# TF2 Coordinate Frames (ROS 2)

Expert reference for the ROS 2 transform system. Everything here assumes ROS 2 Humble or newer (Jazzy-compatible). All code is tested patterns — copy them as-is.

## 1. The Frame Tree Contract (REP-105)

The canonical mobile-robot tree. **TF is a TREE — every frame has exactly one parent. Two parents for one frame breaks everything silently.**

```
earth (optional, multi-map)
 └── map                    ← world-fixed, discrete jumps allowed, NO drift
      └── odom              ← world-fixed, continuous, drifts over time
           └── base_link    ← rigidly attached to robot body
                ├── base_footprint (optional, base_link projected to ground)
                ├── laser_frame / lidar_link
                ├── camera_link
                │    └── camera_optical_frame   ← z-forward! (see §3)
                ├── imu_link
                └── wheel_left_link, wheel_right_link, ...
```

### Who publishes what (NEVER violate this)

| Transform | Publisher | Type | Rate |
|---|---|---|---|
| `map → odom` | Localization (AMCL, slam_toolbox, robot_localization global EKF) | dynamic | 10–50 Hz typical (AMCL: on update + transform_tolerance) |
| `odom → base_link` | Odometry source (diff_drive controller, robot_localization local EKF, VIO) | dynamic | 20–100 Hz, MUST be high-rate and smooth |
| `base_link → sensors` | `robot_state_publisher` (from URDF) or static_transform_publisher | static | latched, published once |
| wheel/arm joints | `robot_state_publisher` + `joint_states` | dynamic | at joint_states rate |

**Exactly ONE node publishes each transform.** Running AMCL + slam_toolbox simultaneously = two `map→odom` publishers = TF jumping/flickering. Running an EKF and a diff-drive plugin both publishing `odom→base_link` is the #1 Gazebo/Nav2 mistake — set `enable_odom_tf:=false` on the controller or `publish_tf: false` in one of them.

### Why does `odom` exist at all?

- `odom → base_link` is **continuous and smooth** — no jumps, ever. Derived from wheel encoders/IMU/VIO integration. It drifts unboundedly, but a controller sampling it gets locally consistent velocity/position. Use `odom` frame for **control, obstacle avoidance, short-horizon motion**.
- `map → base_link` is **accurate but discontinuous** — localization corrections cause jumps (AMCL resample, loop closure). A velocity controller fed map-frame poses will spike when a 30 cm correction lands in one cycle.
- The trick: localization does NOT publish `map → base_link` directly. It computes where the robot is in `map`, looks up `odom → base_link`, and publishes `map → odom = (map→base_link) * (odom→base_link)⁻¹`. The correction is absorbed into `map → odom`, which jumps, while `odom → base_link` stays smooth.
- Rule of thumb: **plan in `map`, control in `odom`, sense in sensor frames, command in `base_link`.**

## 2. REP-103 Conventions (units, axes, rotation)

- Units: **meters, radians, seconds**. Always. No degrees, no millimeters in TF.
- Body frames (`base_link`, sensors): **x forward, y left, z up** (right-handed, FLU).
- World frames (`map`, `odom`): **x east, y north, z up (ENU)**. NOT NED. If you ingest aerospace/marine data (NED), convert: `x_enu = y_ned, y_enu = x_ned, z_enu = -z_ned`, yaw_enu = π/2 − yaw_ned.
- Rotation: quaternions in TF messages `(x, y, z, w)` order. Identity = `(0,0,0,1)` — **a zeroed quaternion `(0,0,0,0)` is invalid and causes silent garbage or "Quaternion malformed" warnings.** If you fill a message manually, set `w = 1.0`.
- Positive yaw = counterclockwise viewed from above (z-up, right-hand rule).
- Frame IDs: **no leading slash** in ROS 2. `"map"`, never `"/map"` — tf2 rejects leading slashes with `tf2.InvalidArgumentException`.

## 3. Camera Optical Frames — the eternal trap

Image-processing conventions differ from body conventions. REP-103 defines a **suffix `_optical_frame`** with: **z forward (out of lens), x right, y down**.

- `camera_link`: x forward, y left, z up (body convention, where the camera is mounted).
- `camera_optical_frame`: child of `camera_link` with fixed rotation **RPY = (-π/2, 0, -π/2)**, i.e. quaternion `(-0.5, 0.5, -0.5, 0.5)`.
- OpenCV/`image_geometry` outputs (pixel → ray, PnP poses, depth points) are in the **optical** frame. Publishing a detected object's pose with `frame_id: camera_link` instead of `camera_optical_frame` puts your object 90° rotated twice — it appears above/beside the robot. This is the single most common perception TF bug.

Static publisher for it:

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 0 --y 0 --z 0 --roll -1.5707963 --pitch 0 --yaw -1.5707963 \
  --frame-id camera_link --child-frame-id camera_optical_frame
```

## 4. Static vs Dynamic Transforms

| | Static | Dynamic |
|---|---|---|
| Topic | `/tf_static` | `/tf` |
| QoS | `transient_local` (latched) — late joiners get it | `volatile`, depth ~100 |
| Timestamp semantics | **ignored** — valid for all time | interpolated between stamps, buffered 10 s default |
| Use for | sensor mounts, fixed frames, `camera_link→optical` | `map→odom`, `odom→base_link`, joints |
| Cost | one message ever | bandwidth × rate × frame count |

Rules:
- Never publish a fixed sensor mount on `/tf` at 100 Hz "to be safe" — it wastes bandwidth and the buffer.
- Never publish a moving transform as static — it will be "valid" forever at its first value.
- `StaticTransformBroadcaster` in rclpy/rclcpp handles the QoS for you. If you hand-roll a `/tf_static` publisher, you MUST use `QoSProfile(durability=TRANSIENT_LOCAL, depth=1, reliability=RELIABLE)` or late-starting nodes (RViz!) never see it.
- Multiple static transforms from one node: pass a **list** to `sendTransform([t1, t2, ...])` in ONE call. Calling it repeatedly with one transform each overwrites the latched message on some DDS implementations (depth=1) — frames vanish.

CLI static publisher (Humble+ flag syntax):

```bash
ros2 run tf2_ros static_transform_publisher \
  --x 0.12 --y 0.0 --z 0.25 --roll 0 --pitch 0 --yaw 3.14159 \
  --frame-id base_link --child-frame-id laser_frame
```

Launch-file form:

```python
from launch_ros.actions import Node
Node(
    package='tf2_ros', executable='static_transform_publisher',
    arguments=['--x', '0.12', '--y', '0', '--z', '0.25',
               '--roll', '0', '--pitch', '0', '--yaw', '3.14159',
               '--frame-id', 'base_link', '--child-frame-id', 'laser_frame'],
)
```

Prefer URDF + `robot_state_publisher` over a pile of static_transform_publishers once you have >3 fixed frames — one source of truth, and joint frames come free.

## 5. Broadcasting Dynamic Transforms (rclpy)

```python
import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

def quaternion_from_yaw(yaw: float):
    return (0.0, 0.0, math.sin(yaw / 2.0), math.cos(yaw / 2.0))

class OdomBroadcaster(Node):
    def __init__(self):
        super().__init__('odom_broadcaster')
        self.br = TransformBroadcaster(self)   # create ONCE, in __init__
        self.timer = self.create_timer(0.02, self.tick)  # 50 Hz
        self.x = self.y = self.yaw = 0.0

    def tick(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()  # NOW, not old data
        t.header.frame_id = 'odom'          # parent
        t.child_frame_id = 'base_link'      # child
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        qx, qy, qz, qw = quaternion_from_yaw(self.yaw)
        t.transform.rotation.x = qx
        t.transform.rotation.y = qy
        t.transform.rotation.z = qz
        t.transform.rotation.w = qw          # NEVER leave w = 0
        self.br.sendTransform(t)
```

Direction convention: `header.frame_id` is the **parent**, `child_frame_id` the child. The transform stored is "pose of child expressed in parent" — i.e., it maps **points from child coordinates into parent coordinates**. Getting this backwards inverts your robot's motion in RViz (drives left, display goes right): if that happens, you almost certainly swapped parent/child or need the inverse.

rclcpp equivalent uses `tf2_ros::TransformBroadcaster` constructed from `*this`, same fields. Use `tf2::toMsg(tf2::Quaternion q)` after `q.setRPY(r, p, y)` instead of hand-rolled math.

## 6. Listening: Buffer + Listener + Timeout

```python
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from rclpy.time import Time
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException
import tf2_geometry_msgs  # REQUIRED import to register PointStamped/PoseStamped transforms

class FrameUser(Node):
    def __init__(self):
        super().__init__('frame_user')
        self.tf_buffer = Buffer()                              # default cache: 10 s
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.timer = self.create_timer(0.1, self.tick)

    def tick(self):
        try:
            # Time() == time 0 == "latest available" — the right default
            t = self.tf_buffer.lookup_transform(
                'map',            # target frame (you want data expressed IN this)
                'base_link',      # source frame (data currently lives here)
                Time(),
                timeout=Duration(seconds=0.5))
        except (LookupException, ConnectivityException, ExtrapolationException) as ex:
            self.get_logger().warn(f'TF not ready: {ex}', throttle_duration_sec=2.0)
            return
        x = t.transform.translation.x
```

Critical details:

- **Buffer and Listener must live as long as the node** — member variables, never locals. A garbage-collected listener stops filling the buffer; lookups then fail with "frame does not exist" even though `/tf` is flowing.
- **The buffer starts empty.** First lookup right after construction always fails without a timeout. Either pass `timeout=` (spins internally, Humble+ rclpy supports it in `lookup_transform`) or guard with `can_transform(..., timeout=...)`.
- **Never call `lookup_transform` with a timeout inside a subscription callback in a single-threaded executor** — the internal wait can't process incoming `/tf` messages (they're queued behind the callback you're blocking), so it deadlocks until timeout. Options:
  1. Use `Time()` (latest) + zero timeout, tolerate occasional misses.
  2. MultiThreadedExecutor + ReentrantCallbackGroup so `/tf` callbacks run concurrently.
  3. Best for sensor data: `tf2_ros.MessageFilter` — queues messages until their transform is available, then fires your callback:

```python
from tf2_ros import MessageFilter   # tf2_ros_py
from message_filters import Subscriber
sub = Subscriber(self, PointStamped, '/detected_point')
self.flt = MessageFilter(sub, self.tf_buffer, 'map', 10, self)
self.flt.registerCallback(self.on_point)   # only called when transform exists
```

- Transforming stamped data:

```python
import tf2_geometry_msgs  # side-effect import; forgetting it → "Type not loaded" / TypeException
out = self.tf_buffer.transform(point_stamped_msg, 'map', timeout=Duration(seconds=0.2))
```

  For PointCloud2 use `tf2_sensor_msgs.do_transform_cloud(cloud, transform)`.

### rclcpp pattern

```cpp
tf_buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
// ...
try {
  auto t = tf_buffer_->lookupTransform("map", "base_link",
              tf2::TimePointZero,                // latest
              tf2::durationFromSec(0.5));        // timeout (spins via dedicated thread)
} catch (const tf2::TransformException & ex) {
  RCLCPP_WARN_THROTTLE(get_logger(), *get_clock(), 2000, "TF: %s", ex.what());
  return;
}
```

For composable nodes / heavy use, give the buffer its own timer interface so timeouts don't depend on your executor:

```cpp
auto timer_interface = std::make_shared<tf2_ros::CreateTimerROS>(
    this->get_node_base_interface(), this->get_node_timers_interface());
tf_buffer_->setCreateTimerInterface(timer_interface);
```

Without this, `lookupTransform` with a timeout in a single-threaded composed container can block the whole container.

## 7. Extrapolation Errors — root causes and fixes

`ExtrapolationException` text tells you which side you're on. Read it carefully:

### "Lookup would require extrapolation **into the future**. Requested time X but the latest data is at time Y" (X > Y)

You asked for a stamp newer than the newest transform in the buffer.
1. **You used `now()` instead of `Time()`.** `lookup_transform('map','base_link', self.get_clock().now())` almost always fails because the `map→odom` publisher hasn't published *at exactly now* yet. Fix: use `Time()` (latest) unless you genuinely need time-correlated data — then add a timeout covering one publisher period.
2. **Clock skew across machines.** Sensor PC's clock is 200 ms ahead of the TF publisher's machine. Fix: chrony/NTP sync; verify with `ros2 topic echo /tf --field transforms[0].header.stamp` vs local clock.
3. **`use_sim_time` mismatch.** One node on sim time (small stamps from `/clock`), another on wall time (epoch stamps ~1.7e9). The buffer sees a 50-year gap. Fix: `use_sim_time:=true` on EVERY node when using Gazebo/bag playback — including RViz and your own nodes. This is the #1 cause in simulation.
4. **Low publish rate vs tight tolerance.** AMCL default `transform_tolerance: 1.0` post-dates its `map→odom` stamp to cover the gap between updates; if you shrank it or your odom runs at 5 Hz, consumers starve. Fix: odom ≥ 20 Hz; keep AMCL tolerance ≥ 0.5.

### "...extrapolation **into the past**. Requested time X but the earliest data is at time Y" (X < Y)

The stamp you asked for has fallen out of the buffer, or arrived before the buffer started.
1. Processing pipeline latency > 10 s buffer → enlarge: `Buffer(cache_time=Duration(seconds=30))`.
2. Node restarted (buffer wiped) while old-stamped sensor messages still in flight.
3. Bag playback looped without `--clock` + sim time, so stamps jumped backwards. Also: when a TF publisher's time jumps backwards (bag loop), listeners throw `TF_OLD_DATA` warnings forever — restart listeners or use `rclcpp::Time` jump handling; simplest fix is restarting the consumers on each loop.

### "Lookup would require extrapolation at time X, but only time Y is in the buffer"

Exactly one transform in the buffer (tf2 needs **two** stamps to interpolate, except static). Publisher just started, or publishes once. Wait, or fix the publisher rate.

## 8. Time-Correlated Transforms (the advanced lookup)

Transform sensor data captured at time T₁ into a frame as it was at time T₂ (e.g., deskewing, or "where was that detection relative to where I am now"):

```python
t = self.tf_buffer.lookup_transform_full(
    target_frame='base_link',  target_time=Time(),          # robot pose now
    source_frame='laser_frame', source_time=scan_stamp,      # data capture time
    fixed_frame='odom',                                       # frame assumed static between the two times
    timeout=Duration(seconds=0.2))
```

`fixed_frame` must be world-fixed and smooth — use `odom`, not `map` (map jumps would corrupt the interpolation). This is what laser scan assemblers and pointcloud deskewing use internally.

## 9. Multi-Robot Namespacing

TF frame IDs are **global strings** — namespacing topics does NOT namespace frames. Two robots both publishing `odom→base_link` on a shared `/tf` poison each other (base_link gets two parents → tree breaks, RViz shows teleporting robots).

Standard solution — `frame_prefix`:

```
map                                ← shared, one localization owner per robot still applies
 ├── robot1/odom ── robot1/base_link ── robot1/laser_frame
 └── robot2/odom ── robot2/base_link ── robot2/laser_frame
```

- `robot_state_publisher` parameter: `frame_prefix: 'robot1/'` (note trailing slash; prefix is prepended to every URDF frame).
- Your own broadcasters: build frame IDs from a declared parameter, never hardcode:

```python
self.declare_parameter('tf_prefix', '')
prefix = self.get_parameter('tf_prefix').value
self.base_frame = f'{prefix}base_link' if not prefix else f'{prefix}/base_link'.replace('//','/')
```

  Simplest robust form: `prefix + 'base_link'` with prefix `'robot1/'` or `''`.
- Nav2 multi-robot: set `robot_base_frame: robot1/base_link`, `odom_frame: robot1/odom` in each namespaced param file; `global_frame: map` stays shared.
- Gazebo plugins: set `<frame_name>`/`<odometry_frame>`/`<robot_base_frame>` per robot — plugins default to unprefixed `odom`/`base_link` and will collide.
- `/tf` and `/tf_static` topics themselves usually stay **global** (one shared tree). Remapping `/tf` into namespaces isolates trees completely — only do that if robots truly share nothing (then each has its own `map`).
- No leading slash, ever: `robot1/base_link` ✓, `/robot1/base_link` ✗ (tf2 throws).

## 10. Debugging Checklist (run in this order)

1. **See the tree:**
   ```bash
   ros2 run tf2_tools view_frames        # writes frames.pdf + frames.gv after listening 5 s
   ```
   Check: one connected tree? `map→odom→base_link` chain present? Any frame with two parents (shows as broken tree / missing edges)? Look at "Most recent transform" and "Buffer length" per edge — an edge with rate 10000 Hz is a fight between two publishers.
2. **Probe one transform:**
   ```bash
   ros2 run tf2_ros tf2_echo map base_link
   ```
   No output → chain broken somewhere; walk it edge by edge (`tf2_echo map odom`, `tf2_echo odom base_link`).
3. **Who publishes?**
   ```bash
   ros2 topic info /tf --verbose         # lists publisher nodes
   ros2 topic echo /tf | grep -A1 frame_id   # watch which edges stream
   ```
   Two nodes publishing the same parent→child = your bug.
4. **Timing:**
   ```bash
   ros2 run tf2_ros tf2_monitor map base_link   # avg delay, max delay per publisher
   ```
   Delay > 100 ms or negative delay → clock sync / sim-time mismatch (see §7).
5. **Static frames missing in RViz only** → RViz started before static publisher AND publisher isn't transient_local; or RViz `use_sim_time` mismatch (RViz shows "No transform from X to Y" with everything seemingly running).
6. **"frame does not exist"** → listener buffer dead (listener was a local variable, §6), frame name typo (case-sensitive), or leading slash.
7. **Robot model scattered/white in RViz** → `robot_state_publisher` running but no `/joint_states` (start `joint_state_publisher` or your controller); fixed frame in RViz set to a frame not connected to the model.
8. **Jumpy motion in RViz but smooth control** → you're visualizing in `map` and localization is correcting; normal. Jumpy control → you're controlling in `map`; switch to `odom`.

## 11. Quick-Reference: Mistakes Everyone Makes

| Symptom | Cause | Fix |
|---|---|---|
| Extrapolation into future, ~0.05 s | lookup at `now()` | use `Time()` / `tf2::TimePointZero` |
| Extrapolation, gap ≈ years | `use_sim_time` mismatch | set on ALL nodes incl. RViz |
| Lookup hangs/timeouts in callback | blocking wait in single-threaded executor | MessageFilter or MultiThreadedExecutor |
| "frame does not exist" despite /tf flowing | Buffer/Listener garbage collected | store as `self.` members |
| Robot flickers between two poses | two publishers of same edge | disable one (`enable_odom_tf:=false`, `publish_tf: false`) |
| Detected objects rotated 90°/above robot | optical vs body frame | publish in `*_optical_frame`, add the (-π/2,0,-π/2) static TF |
| Quaternion warnings / garbage rotation | rotation left as all zeros | set `w=1.0` for identity |
| RViz never sees static frames | hand-rolled `/tf_static` with volatile QoS | TRANSIENT_LOCAL or use StaticTransformBroadcaster |
| Some static frames vanish | multiple sendTransform calls, depth-1 latch | send all statics as one list |
| Robot drives right, display moves left | parent/child swapped in broadcast | header.frame_id = parent, child_frame_id = child |
| Multi-robot teleporting | shared unprefixed frames | `frame_prefix` per robot |
| `InvalidArgumentException` on lookup | leading `/` in frame id | strip slashes |
| TF_OLD_DATA spam after bag loops | time jumped backwards | restart consumers / `--clock` + sim time |
| Nav2 "Timed out waiting for transform map→base_link" | localization not running or tolerance too tight | start AMCL/slam_toolbox; transform_tolerance ≥ 0.5; odom ≥ 20 Hz |

## 12. Performance Notes

- `lookup_transform` is cheap (~µs, in-process buffer walk + interpolation). Calling it per-point on a pointcloud is NOT — look up once per cloud, then apply with `do_transform_cloud` (vectorized) or Eigen.
- Default buffer = 10 s. At 100 Hz × 30 frames that's ~30k transforms cached; fine. Raising cache_time to minutes on high-rate trees costs real memory.
- `/tf` bandwidth: each TransformStamped ≈ 100 bytes + DDS overhead. 50 joints at 100 Hz is real traffic on WiFi — drop `joint_states` rate or split high-rate frames off the shared tree if remote-viewing over weak links.
- For pure offline/algorithmic use you can feed a `Buffer` manually with `set_transform(t, 'authority')` — no listener, no ROS graph needed. Useful in unit tests:

```python
buf = Buffer()
buf.set_transform(make_tf('odom', 'base_link', x=1.0, stamp=t0), 'test')
buf.set_transform(make_tf('odom', 'base_link', x=2.0, stamp=t1), 'test')
mid = buf.lookup_transform('odom', 'base_link', t_mid)  # interpolated x=1.5
```

Test interpolation behavior this way before trusting time-correlated lookups in production code.
