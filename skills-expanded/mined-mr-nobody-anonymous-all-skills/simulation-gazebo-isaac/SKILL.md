---
name: simulation-gazebo-isaac
description: "Use when setting up robot simulation in Gazebo, Isaac Sim, Webots, PyBullet, or MuJoCo with ROS 2 — URDF/SDF physics tuning, sensor noise modeling, sim-to-real transfer, domain randomization, or headless CI simulation. Provides exact physics parameters that match reality (friction, inertia, contact params), validated sensor noise values, simulator selection criteria, and working launch/spawn/bridge code for Gazebo Harmonic + ROS 2 Jazzy/Humble."
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


# Robot Simulation: Gazebo, Isaac Sim, and the Sim-to-Real Gap

## 0. Naming disambiguation (gets everyone)

| Name | What it actually is | ROS 2 pairing |
|---|---|---|
| Gazebo Classic (gazebo11) | EOL Jan 2025. Do NOT start new projects on it | Foxy/Humble via `gazebo_ros_pkgs` |
| Gazebo (formerly "Ignition") | The current one. Versions: Fortress (LTS, Humble), Harmonic (LTS, Jazzy), Ionic | `ros_gz` packages |
| Isaac Sim | NVIDIA Omniverse-based, PhysX 5, RTX rendering, GPU-parallel RL | ROS 2 bridge extension, any distro |
| Isaac Lab | RL framework on top of Isaac Sim (replaces Isaac Gym / OmniIsaacGymEnvs) | Standalone Python, export policy to ROS 2 |

Pairings that work without pain (use these, not other combos):
- ROS 2 Humble ↔ Gazebo Fortress (`ros-humble-ros-gz`)
- ROS 2 Jazzy ↔ Gazebo Harmonic (`ros-jazzy-ros-gz`)
- ROS 2 Kilted/Rolling ↔ Gazebo Ionic

Classic-era APIs (`gazebo_ros`, `libgazebo_ros_*.so` plugins, `spawn_entity.py`) do NOT exist in modern Gazebo. The modern equivalents are `gz sim`, `gz-sim-*-system` plugins, `ros_gz_sim create`, and `ros_gz_bridge`. If an LLM-generated launch file references `gazebo_ros`, it's writing for the dead simulator.

## 1. Simulator selection (decide in 60 seconds)

| Need | Pick | Why |
|---|---|---|
| ROS 2 robot dev, nav2/moveit integration, sensors | Gazebo Harmonic | First-class ros_gz bridge, SDF sensors, DART physics |
| Photorealistic perception data, synthetic datasets | Isaac Sim | RTX ray-traced cameras, Replicator for domain randomization |
| Massively parallel RL (1000s of envs) | Isaac Lab | GPU PhysX, 10k+ envs on one RTX 4090 |
| Fast contact-rich RL / MPC research, no rendering needs | MuJoCo (≥2.3, free) | Best contact solver stability, analytic derivatives (MJX for JAX) |
| Quick Python prototyping, grasping experiments | PyBullet | pip install, zero setup, decent contacts, dated renderer |
| Education, swarm robotics, deterministic CI | Webots | Deterministic replay, built-in robot models, easy headless |
| Soft bodies, deformables | Isaac Sim (FEM) or SOFA | Gazebo/MuJoCo rigid-body only (MuJoCo has limited flex) |

Rules of thumb:
- If the deliverable is a ROS 2 stack on a real robot → Gazebo. Period.
- If the deliverable is a trained policy → MuJoCo or Isaac Lab, then deploy via ROS 2 node running the exported ONNX policy.
- Isaac Sim needs an RTX GPU (≥8 GB VRAM, RTX 3070+ realistic minimum; A4000+ for Replicator at scale). No NVIDIA GPU → Isaac is off the table.
- CPU-only CI runner → Gazebo headless (`-s`), Webots, PyBullet, or MuJoCo all fine. Isaac Sim is not.

## 2. Inertia: the #1 cause of "my robot explodes/flips/jitters"

A URDF with fake inertia (`<inertia ixx="1" iyy="1" izz="1"/>` on a 0.1 kg link) is the most common sim failure. Symptoms: robot launches into orbit on spawn, wheels sink/jitter, arm oscillates violently under PID.

Correct inertia for primitives (mass m, about COM):

```
Solid box (x,y,z dims):    ixx = m(y²+z²)/12   iyy = m(x²+z²)/12   izz = m(x²+y²)/12
Solid cylinder (r, h, z-axis): ixx = iyy = m(3r²+h²)/12   izz = m·r²/2
Solid sphere (r):          ixx = iyy = izz = 2mr²/5
Hollow sphere shell:       2mr²/3
```

URDF macro pattern (xacro) — use this in every robot description:

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
```

Sanity checks the agent must apply:
- Triangle inequality: ixx + iyy ≥ izz (and permutations). Violations → DART/PhysX silently misbehaves or errors.
- Realistic magnitude: a 1 kg, 10 cm cube has inertia ≈ 0.0017 kg·m². If you see 1.0 for a small link, it's wrong by ~1000×.
- Mass ratio between connected links < 100:1, ideally < 10:1. A 50 kg base driving a 0.001 kg sensor link makes the constraint solver stiff → jitter. Give tiny links ≥ 0.01 kg and matching inertia, or make them fixed joints (Gazebo lumps fixed-joint links into the parent — good).
- `<origin>` inside `<inertial>` is the COM offset, not the visual origin. For a wheel whose mesh origin is at the rim, this matters.
- Never give a link `<visual>` + `<collision>` but no `<inertial>` unless it's attached by a fixed joint — URDF parsers default mass to 0 → kinematic or rejected.
- Real robots: get mass from a scale, COM/inertia from CAD (Fusion 360 / SolidWorks "mass properties", set material densities first). Mesh-based inertia tools (meshlab) assume uniform density — fine for printed parts, wrong for assemblies with motors.

## 3. Friction and contact parameters that match reality

### 3.1 Friction coefficients (measured, use as starting points)

| Pair | μ (static, dry) |
|---|---|
| Rubber tire on dry concrete | 0.8–1.0 |
| Rubber on smooth tile / linoleum | 0.5–0.7 |
| Rubber on wet smooth floor | 0.3–0.45 |
| Rubber on carpet | 0.6–0.8 (plus deformation drag, not just μ) |
| Hard plastic caster on tile | 0.2–0.35 |
| PLA/ABS on wood | 0.4–0.5 |
| Steel on steel | 0.5–0.6 dry |
| Robot gripper rubber pad on cardboard | 0.5–0.7 |

SDF (modern Gazebo) per-collision:

```xml
<collision name="wheel_collision">
  <geometry><cylinder><radius>0.05</radius><length>0.03</length></cylinder></geometry>
  <surface>
    <friction>
      <ode>
        <mu>0.9</mu>          <!-- primary direction -->
        <mu2>0.9</mu2>        <!-- secondary; lower mu2 on casters/omniwheels -->
        <fdir1>0 0 1</fdir1>  <!-- only if anisotropic friction needed -->
      </ode>
    </friction>
    <contact>
      <ode>
        <kp>1e6</kp>          <!-- contact stiffness; 1e5–1e7 typical -->
        <kd>100</kd>          <!-- contact damping; 1–1000 -->
        <min_depth>0.001</min_depth>  <!-- allow 1mm penetration before force -->
        <max_vel>0.1</max_vel>        <!-- cap correction velocity; kills bounce -->
      </ode>
    </contact>
  </surface>
</collision>
```

Critical: friction is combined from BOTH surfaces in contact (typically min or product depending on engine). If your ground plane has `<mu>100</mu>` (a common copy-paste), wheel slip behavior is governed entirely by the wheel — fine — but if the ground has μ=0.1 your perfect wheel still slips. Always set the ground plane explicitly.

`kp`/`kd` tuning:
- Too-high kp (1e9+) with default step size → stiff system → vibration/explosion. 1e6 is right for wheeled robots on rigid floors.
- Wheels "sinking" into ground → kp too low or min_depth too large.
- Bouncing on spawn → set `max_vel 0.1` and `min_depth 0.001`, and spawn the robot 1–2 cm above ground, not intersecting it.

Casters: model as a frictionless sphere (`mu 0.01, mu2 0.01`) rather than simulating the swivel assembly. Simulating real caster swivel joints adds two fast unactuated joints that destabilize the solver and gain you nothing.

### 3.2 Gazebo physics step config (world SDF)

```xml
<physics name="default" type="dart">
  <max_step_size>0.001</max_step_size>          <!-- 1 ms; 4 ms ok for slow mobile robots -->
  <real_time_factor>1.0</real_time_factor>      <!-- 0 = run as fast as possible (CI/RL) -->
  <real_time_update_rate>1000</real_time_update_rate>
</physics>
```

- Manipulators with stiff position control: step ≤ 1 ms. Quadrupeds/contact-rich: 0.5 ms.
- `ros2_control` update rate must be ≤ 1/step. Controller at 1000 Hz with 4 ms physics step = controller sees stale states 4× per cycle → oscillation.
- Determinism: Gazebo is deterministic for the same binary, same step size, same machine, single-threaded physics — but NOT across machines or threads. Don't write CI asserts on exact poses; assert tolerances (e.g., position within 5 cm).

## 4. Modern Gazebo + ROS 2: the working skeleton

### 4.1 Spawn + bridge launch (ROS 2 Jazzy + Harmonic)

```python
# launch/sim.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg = get_package_share_directory('my_robot_description')
    world = os.path.join(pkg, 'worlds', 'office.sdf')

    return LaunchDescription([
        # Gazebo finds meshes via this, NOT GAZEBO_MODEL_PATH (Classic-era var)
        SetEnvironmentVariable('GZ_SIM_RESOURCE_PATH',
                               os.path.dirname(pkg)),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch', 'gz_sim.launch.py')),
            # -r = run immediately; -s = server only (headless); -v 4 verbose
            launch_arguments={'gz_args': f'-r {world}'}.items()),
        Node(package='ros_gz_sim', executable='create',
             arguments=['-topic', 'robot_description',
                        '-name', 'my_robot', '-z', '0.02'],
             output='screen'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': open(
                 os.path.join(pkg, 'urdf', 'robot.urdf')).read(),
                 'use_sim_time': True}]),
        Node(package='ros_gz_bridge', executable='parameter_bridge',
             parameters=[{'config_file': os.path.join(pkg, 'config', 'bridge.yaml'),
                          'use_sim_time': True}]),
    ])
```

```yaml
# config/bridge.yaml — direction: GZ_TO_ROS, ROS_TO_GZ, or BIDIRECTIONAL
- ros_topic_name: /clock
  gz_topic_name: /clock
  ros_type_name: rosgraph_msgs/msg/Clock
  gz_type_name: gz.msgs.Clock
  direction: GZ_TO_ROS            # MANDATORY for use_sim_time to work
- ros_topic_name: /cmd_vel
  gz_topic_name: /model/my_robot/cmd_vel
  ros_type_name: geometry_msgs/msg/Twist
  gz_type_name: gz.msgs.Twist
  direction: ROS_TO_GZ
- ros_topic_name: /scan
  gz_topic_name: /scan
  ros_type_name: sensor_msgs/msg/LaserScan
  gz_type_name: gz.msgs.LaserScan
  direction: GZ_TO_ROS
- ros_topic_name: /imu
  gz_topic_name: /imu
  ros_type_name: sensor_msgs/msg/Imu
  gz_type_name: gz.msgs.IMU
  direction: GZ_TO_ROS
- ros_topic_name: /camera/image_raw
  gz_topic_name: /camera
  ros_type_name: sensor_msgs/msg/Image
  gz_type_name: gz.msgs.Image
  direction: GZ_TO_ROS
```

Camera images: prefer `ros_gz_image image_bridge` over parameter_bridge for throughput (uses image_transport, supports compression).

### 4.2 The use_sim_time trap

EVERY node in a simulated stack must run with `use_sim_time: true`, AND the /clock bridge must exist. Symptoms of getting this wrong: TF "lookup would require extrapolation into the future/past", nav2 costmap never updates, message_filters never fire. Checklist:
1. `/clock` bridged (see yaml above).
2. `use_sim_time: true` on robot_state_publisher, all controllers, nav2, rviz (`ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true`).
3. `ros2 topic echo /clock --once` shows ticking sim time.

### 4.3 ros2_control in Gazebo (gz_ros2_control)

```xml
<!-- in URDF -->
<ros2_control name="GazeboSystem" type="system">
  <hardware><plugin>gz_ros2_control/GazeboSimSystem</plugin></hardware>
  <joint name="left_wheel_joint">
    <command_interface name="velocity"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
<gazebo>
  <plugin filename="gz_ros2_control-system"
          name="gz_ros2_control::GazeboSimROS2ControlPlugin">
    <parameters>$(find my_robot_bringup)/config/controllers.yaml</parameters>
  </plugin>
</gazebo>
```

Gotchas:
- Package renamed: `ign_ros2_control` (Fortress-era) → `gz_ros2_control` (Harmonic). Plugin class names changed accordingly.
- Spawner nodes (`ros2 run controller_manager spawner joint_state_broadcaster`) race with Gazebo startup. Chain them with `RegisterEventHandler(OnProcessExit(...))` after the spawn-entity node, or they fail with "controller_manager not available".
- Joint `<dynamics damping="0.1" friction="0.05"/>` in URDF: without some damping on actuated joints, velocity-controlled wheels ring. 0.05–0.5 N·m·s/rad is typical for small robots.
- Effort limits in URDF are ENFORCED by gz_ros2_control. A `<limit effort="1"/>` on a wheel that needs 2 N·m → robot crawls and nobody knows why. Compute: τ = m·a·r + rolling resistance; a 5 kg robot at 1 m/s², r=0.05 m → ≥0.13 N·m/wheel, set limit 3–5× that.

## 5. Sensor noise modeling (values that match real hardware)

A noiseless sim sensor trains/validates nothing. Real defaults to copy:

### 5.1 IMU (modeled on BMI088 / MPU-9250 class MEMS)

```xml
<sensor name="imu" type="imu">
  <update_rate>200</update_rate>
  <imu>
    <angular_velocity>
      <x><noise type="gaussian">
        <mean>0</mean>
        <stddev>0.009</stddev>            <!-- rad/s; gyro white noise ~0.5 deg/s -->
        <bias_mean>0.00075</bias_mean>     <!-- rad/s bias -->
        <bias_stddev>0.005</bias_stddev>
        <dynamic_bias_stddev>0.00002</dynamic_bias_stddev>  <!-- bias random walk -->
        <dynamic_bias_correlation_time>400</dynamic_bias_correlation_time>
      </noise></x>
      <!-- repeat for y, z -->
    </angular_velocity>
    <linear_acceleration>
      <x><noise type="gaussian">
        <mean>0</mean>
        <stddev>0.021</stddev>            <!-- m/s²; accel white noise -->
        <bias_mean>0.05</bias_mean>
        <bias_stddev>0.0075</bias_stddev>
      </noise></x>
      <!-- repeat for y, z -->
    </linear_acceleration>
  </imu>
</sensor>
```

Spec-sheet conversion: gyro noise density N (deg/s/√Hz) at sample rate f → stddev = N·√f. BMI088: 0.014 deg/s/√Hz at 200 Hz → 0.198 deg/s ≈ 0.0035 rad/s. The values above are deliberately slightly pessimistic — tune your EKF against worse-than-real noise and the real robot will be a pleasant surprise.

### 5.2 2D lidar (RPLIDAR A1/A2, LDS-01 class)

```xml
<sensor name="lidar" type="gpu_lidar">
  <update_rate>10</update_rate>
  <lidar>
    <scan><horizontal>
      <samples>360</samples><resolution>1</resolution>
      <min_angle>-3.14159</min_angle><max_angle>3.14159</max_angle>
    </horizontal></scan>
    <range><min>0.15</min><max>12.0</max><resolution>0.01</resolution></range>
    <noise type="gaussian"><mean>0</mean><stddev>0.01</stddev></noise>  <!-- 1 cm; real RPLIDAR ~1% of range -->
  </lidar>
</sensor>
```

What Gazebo does NOT model and reality does: returns off glass/mirrors (lidar sees through windows in sim, gets specular garbage in reality), black absorptive surfaces dropping returns, sunlight saturation outdoors, motor speed variation. Nav2 tuned in sim must be re-validated near glass walls.

### 5.3 Depth camera (RealSense D435 class)

```xml
<noise type="gaussian"><mean>0</mean><stddev>0.007</stddev></noise>
```

Real D435 depth error ≈ 2% of distance at 2 m (≈ 4 cm), growing quadratically; sim gaussian noise badly undermodels this. For perception work, add post-processing: quadratic distance-dependent noise, edge shadowing, and holes — or use Isaac Sim Replicator which models stereo-matching artifacts properly.

### 5.4 Wheel odometry drift

DiffDrive plugin odometry in sim is near-perfect — real odometry drifts 1–5% of distance traveled and worse in yaw. If you're testing SLAM/EKF, inject slip: lower wheel μ to 0.7, or add gaussian noise to the bridged odom in a relay node. A localization stack validated only against perfect sim odom WILL fail on the real robot.

## 6. Sim-to-real gap: the canonical mismatch list

What kills transfer, in observed frequency order:

1. **Actuator dynamics.** Sim joints achieve commanded velocity instantly; real motors have electrical+mechanical time constants (20–200 ms), backlash (0.5–2° in cheap gearboxes), stiction, current limits, and battery sag (a 12 V nominal pack swings 10–12.6 V → ~20% torque variation). Fix: add first-order lag to commands in sim (`v_applied += (v_cmd - v_applied) * dt/τ`, τ≈0.05–0.15 s), randomize torque ±20%.
2. **Latency.** Real pipeline: sensor → driver → DDS → controller → driver → motor = 20–80 ms total. Sim: ~0. RL policies trained at zero latency oscillate on hardware. Fix: buffer observations 1–3 control steps in training; randomize delay 0–40 ms.
3. **Mass/COM error.** Battery placement alone shifts COM by centimeters. Randomize mass ±15%, COM ±2 cm.
4. **Contact/friction.** Randomize μ 0.4–1.1 for ground contact tasks.
5. **Sensor mounting error.** Real lidar is never exactly where the URDF says; 1° of mounting pitch = 17 cm height error at 10 m. Calibrate extrinsics on the real robot; don't trust CAD.
6. **Control frequency jitter.** Sim controllers tick perfectly; Linux non-RT jitters ±1–5 ms. Matters above ~200 Hz control.
7. **Perception gap.** Sim textures/lighting ≠ reality. Either domain-randomize visuals heavily (Isaac Replicator) or use geometry-only inputs (lidar, depth) which transfer far better than RGB.

Transfer protocol that works:
1. Validate kinematics: drive 2 m straight + 360° spin on real robot, compare odom vs tape measure. Fix wheel radius/separation in URDF from MEASURED error (effective wheel separation on carpet is ~5–10% larger than geometric due to scrub).
2. System-ID the actuators: command step inputs, log response, fit τ and max accel, put those in sim.
3. Re-run the sim test suite with identified params + noise. Only then deploy.

## 7. Domain randomization (Isaac Lab / RL workflows)

Randomize per-episode (not per-step, except noise):

| Parameter | Range | Notes |
|---|---|---|
| Ground friction μ | 0.4–1.0 | per-episode |
| Link mass | ×(0.85–1.15) | all links |
| COM offset | ±2 cm | base link especially |
| Motor strength | ×(0.8–1.2) | models battery sag |
| Joint damping/friction | ×(0.5–2.0) | log-uniform |
| Observation noise | gaussian, sensor-spec σ | per-step |
| Action delay | 0–3 control steps | per-episode |
| External push | 0.5–1 m/s impulse every 5–10 s | locomotion robustness |
| Terrain | height-field roughness 0–5 cm | locomotion |

Isaac Lab event config pattern:

```python
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.envs.mdp import events as mdp

physics_material = EventTerm(
    func=mdp.randomize_rigid_body_material, mode="startup",
    params={"asset_cfg": SceneEntityCfg("robot", body_names=".*"),
            "static_friction_range": (0.4, 1.0),
            "dynamic_friction_range": (0.3, 0.9),
            "restitution_range": (0.0, 0.1), "num_buckets": 64})

add_base_mass = EventTerm(
    func=mdp.randomize_rigid_body_mass, mode="startup",
    params={"asset_cfg": SceneEntityCfg("robot", body_names="base"),
            "mass_distribution_params": (0.85, 1.15), "operation": "scale"})

push_robot = EventTerm(
    func=mdp.push_by_setting_velocity, mode="interval",
    interval_range_s=(5.0, 10.0),
    params={"velocity_range": {"x": (-0.8, 0.8), "y": (-0.8, 0.8)}})
```

Sequencing rule: get the policy working with ZERO randomization first. Randomization added before the task works masks bugs and stalls learning. Then widen ranges until real-world performance plateaus. Too-wide randomization → conservative, sluggish policies.

Isaac Sim specifics:
- Units: meters, kg, seconds — but USD stages from artists are often in cm. Check `metersPerUnit` on stage load.
- PhysX solver: `solver_position_iteration_count` 4–8 for locomotion, up to 16 for manipulation; TGS solver (default in Isaac Lab) handles stiff contacts better than PGS.
- GPU pipeline requires all tensors stay on-device; a stray `.cpu()` in the obs path tanks throughput from 50k to 2k steps/s.
- Deploy: export policy to ONNX/TorchScript, run in a plain ROS 2 Python/C++ node at fixed rate. Do not run Isaac Sim on the robot.

## 8. Headless simulation in CI

Gazebo headless = server only, no GUI process:

```bash
gz sim -s -r --headless-rendering -v 3 world.sdf
```

- `-s`: server only. `--headless-rendering`: EGL-based offscreen rendering so camera/GPU-lidar sensors still work WITHOUT a display. Without this flag, sensors needing the render engine silently publish nothing in CI.
- CPU-only runner + rendering sensors: works via software EGL (mesa/llvmpipe) but slowly — budget 0.1–0.3 RTF with one camera. Prefer `gpu_lidar`→ swap to CPU `lidar` type in a CI world variant, or drop camera tests to a GPU runner.
- Set `<real_time_factor>0</real_time_factor>` in the CI world to run as fast as possible.

Working GitHub Actions job:

```yaml
jobs:
  sim_test:
    runs-on: ubuntu-24.04
    container: ros:jazzy
    steps:
      - uses: actions/checkout@v4
      - run: |
          apt-get update && apt-get install -y ros-jazzy-ros-gz xvfb
      - run: |
          . /opt/ros/jazzy/setup.sh
          colcon build --symlink-install
      - run: |
          . install/setup.sh
          # xvfb-run as belt-and-braces for anything that still wants X
          xvfb-run -a colcon test --packages-select my_robot_sim_tests \
            --event-handlers console_direct+
        timeout-minutes: 20
```

launch_testing pattern for a sim smoke test:

```python
import launch_testing, pytest, rclpy, unittest
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from nav_msgs.msg import Odometry

@pytest.mark.launch_test
def generate_test_description():
    sim = IncludeLaunchDescription(...)  # your sim.launch.py with gz_args:='-s -r --headless-rendering'
    return LaunchDescription([sim, TimerAction(period=10.0,
        actions=[launch_testing.actions.ReadyToTest()])])

class TestRobotMoves(unittest.TestCase):
    def test_odom_advances(self):
        rclpy.init()
        node = rclpy.create_node('checker')
        msgs = []
        node.create_subscription(Odometry, '/odom', msgs.append, 10)
        pub = node.create_publisher(Twist, '/cmd_vel', 10)
        end = node.get_clock().now() + rclpy.duration.Duration(seconds=15)
        while node.get_clock().now() < end:
            t = Twist(); t.linear.x = 0.2; pub.publish(t)
            rclpy.spin_once(node, timeout_sec=0.1)
        self.assertGreater(len(msgs), 10, "no odom received")
        self.assertGreater(msgs[-1].pose.pose.position.x, 0.5,
                           "robot did not move forward")  # tolerance, never exact
        rclpy.shutdown()
```

CI rules:
- Always wrap sim tests in a hard timeout (sim hangs are the #1 CI flake).
- Wait for readiness by polling `/clock` or a sensor topic, never `sleep(5)` — container cold-start varies 2–30 s.
- Assert tolerances, not exact values (sim is not cross-machine deterministic).
- Webots alternative: `webots --batch --no-rendering --stdout --stderr world.wbt` — fully deterministic, lighter than Gazebo for CI, good choice if you control the whole stack.
- PyBullet/MuJoCo in CI: just `p.connect(p.DIRECT)` / `mujoco.MjModel`, no display machinery at all — ideal for pure-physics unit tests (e.g., "does my IK solution actually reach the pose under dynamics").

## 9. Debugging checklist (symptom → cause)

| Symptom | Check, in order |
|---|---|
| Robot explodes/launches on spawn | 1) fake inertia values (§2) 2) collision geometries inter-penetrating at spawn (spawn with `-z 0.02`) 3) self-colliding links — add `<self_collide>false</self_collide>` or fix collision geometry 4) kp too high |
| Robot jitters standing still | mass ratio >100:1 between links; step size too large; kp too high/kd too low; caster modeled with real swivel joints |
| Wheels spin, robot doesn't move | ground plane μ near 0; wheel collision is the visual mesh (use cylinder primitive for wheel collisions, never mesh); effort limit too low |
| Robot drifts while "stopped" | μ too low on ground; nonzero `<dynamics friction>` missing on wheel joints; controller deadband |
| Drives in circles under straight cmd_vel | wheel_separation/radius mismatch URDF vs diff-drive plugin params; one joint axis flipped (+1 vs −1 z-axis) |
| No /scan, /imu, /camera data in ROS | 1) bridge yaml topic/type mismatch (run `gz topic -l` and compare) 2) sensor needs render engine but running `-s` without `--headless-rendering` 3) `<sensor>` attached to a link lumped away by fixed-joint reduction — add `<gazebo reference=...>` correctly or use `<dont_collapse>` |
| TF extrapolation errors | use_sim_time missing somewhere; /clock not bridged (§4.2) |
| Controllers fail to spawn | controller_manager race — chain spawners after robot spawn; gz_ros2_control plugin missing from URDF; controllers.yaml path wrong inside `<parameters>` |
| Sim runs at RTF 0.2 | mesh collision geometry (replace with primitives — a 100k-triangle collision mesh is 100× the cost); too many contact points; camera at 30 Hz on software rendering; step size smaller than needed |
| Behavior differs sim vs real | start at §6 list, top to bottom: actuator lag, latency, mass, friction, sensor extrinsics |
| Works in Gazebo GUI, fails headless CI | rendering sensors without `--headless-rendering`; test asserts exact values; readiness sleep too short |

## 10. Collision geometry rules

- Visual = pretty mesh. Collision = primitives (box/cylinder/sphere) or a convex decomposition. Never reuse the visual mesh for collision.
- Wheels: collision MUST be a `<cylinder>` (or sphere for omni robots). Mesh-collision wheels produce polygonal "bumpy" rolling.
- Concave meshes: Gazebo's ODE/DART treat trimeshes as static-only reliably; for dynamic concave objects do convex decomposition (`v-hacd`) into ≤32 hulls or model with primitives.
- Keep collision shapes 2–5 mm SMALLER than visuals for tight assemblies (grippers), or fingers permanently "collide" with each other.
- MoveIt + sim: the SRDF disables adjacent-link collisions; Gazebo doesn't read SRDF — set `<self_collide>` per-link deliberately (default false in modern Gazebo is usually what you want for arms).

## 11. Minimal diff-drive robot SDF reference (known-good params)

```xml
<plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">
  <left_joint>left_wheel_joint</left_joint>
  <right_joint>right_wheel_joint</right_joint>
  <wheel_separation>0.30</wheel_separation>   <!-- MEASURE on real robot, contact-patch center to center -->
  <wheel_radius>0.05</wheel_radius>           <!-- loaded radius (tire compresses ~2-5%) -->
  <odom_publish_frequency>50</odom_publish_frequency>
  <max_linear_acceleration>1.0</max_linear_acceleration>   <!-- match real motor capability -->
  <max_angular_acceleration>2.0</max_angular_acceleration>
  <topic>/model/my_robot/cmd_vel</topic>
  <odom_topic>/model/my_robot/odometry</odom_topic>
  <tf_topic>/model/my_robot/tf</tf_topic>
  <frame_id>odom</frame_id>
  <child_frame_id>base_link</child_frame_id>
</plugin>
```

Set max accelerations to what the real robot achieves, not infinity — otherwise nav2 tuned in sim commands accelerations the hardware can't deliver and path-following degrades on the real robot.

## 12. Quick commands

```bash
gz topic -l                         # list Gazebo topics (compare with bridge yaml)
gz topic -e -t /scan                # echo a Gazebo topic
gz model --list                     # spawned models
gz sim -g                           # attach GUI to an already-running headless server
gz sdf -p robot.urdf                # convert/validate URDF → SDF (see what Gazebo actually loads,
                                    #   including fixed-joint lumping — debug missing sensor links here)
check_urdf robot.urdf               # URDF tree validity
ros2 run tf2_tools view_frames      # TF tree sanity
ros2 topic hz /scan                 # verify sensor rate survives the bridge
```
