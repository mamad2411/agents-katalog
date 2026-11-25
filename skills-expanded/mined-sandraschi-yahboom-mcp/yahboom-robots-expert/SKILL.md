---
name: yahboom-robots-expert
description: Use this skill when you need domain expertise on Yahboom Raspbot v2 hardware, ROS 2 setup, mecanum kinematics, or integration architecture.
---

# Yahboom Robots Expert Skill

Use this skill when you need **domain expertise** on Yahboom Raspbot v2 hardware, ROS 2 setup, mecanum kinematics, or integration architecture—beyond routine operator procedures (see **yahboom-operator** for day-to-day tool use).

## 🛠️ Hardware Specifications

- **Platform**: Yahboom Raspbot v2. Main compute: **Raspberry Pi 5** (ARM64). OS: Ubuntu 24.04 + **ROS 2 Humble**.
- **Drive**: Four **mecanum wheels** (32.5 mm radius). Layout: front_left, front_right, back_left, back_right; axles parallel to robot X (forward). Enables holonomic motion: forward/back, strafe left/right, rotate in place.
- **Sensors**: 2D LIDAR (laser_link), camera (camera_link); IMU and wheel encoders for odometry.
- **Power**: Onboard battery; monitor via `read_battery` / telemetry. Low battery (< 20%) limits recommended motion duration.

## 📐 Frames and URDF

- **base_footprint**: Ground plane (z = 0).
- **base_link**: Body frame; z offset = +wheel_radius (0.0325 m) above ground. Wheel joints at z = -wheel_radius relative to base_link.
- **Wheel positions** (joint xyz): x = ±0.08, y = ±0.0745 (half track), z = -0.0325.
- **LIDAR**: Offset (0, 0, 0.0825) from base_link.
- **Camera**: Offset (0.105, 0, 0.05).

## 🤖 ROS 2 Architecture

- **ROS 2**: Humble on Ubuntu 24.04. Topics/services follow ROS 2 naming (e.g. cmd_vel, odom, scan, image).
- **MCP ↔ Robot**: yahboom-mcp server talks to a **REST bridge** (or direct ROS 2 node) on the robot network. Robot IP and bridge port configurable (env or settings).
- **Dual mode**: Server can run `--mode stdio` (MCP only) or `--mode dual --port 10892` (REST API + MCP). Dashboard (Vite) uses REST on 10892; frontend dev server on 10893.

## ⚙️ Kinematics and Motion

- **Mecanum rollers**: rollers at 45°; combined wheel velocities yield body linear and angular velocity.
- **Odometry**: from encoders + IMU; heading from IMU.
- **Trajectory recording**: start_recording → run motions → stop_recording(basename).

## 🌐 Integration and Fleet

- **Federated fleet**: Yahboom-MCP is one node; others include Dreame-MCP (mapping/sweeping), Virtual-Robotics-MCP (simulation), central hub (orchestration).
- **3D viz**: Dashboard loads real STL meshes from URDF (base_link, wheels, LIDAR, camera).

## ⚖️ Skill Application Matrix

| Use **yahboom-robots-expert** when | Use **yahboom-operator** when |
|------------------------------------|------------------------------|
| Explaining hardware, frames, or kinematics | Running tools and following workflows |
| Debugging connection, URDF, or frame issues | Choosing which tool/prompt to call |
| Designing integrations or fleet behaviour | Doing health_check → motion → recording |
| Answering “how does the robot work?” | Answering “how do I make it patrol?” |

## 🔗 Quick References

- **Tools**: yahboom, yahboom_help, yahboom_agentic_workflow.
- **Prompts**: yahboom_quick_start(robot_ip), yahboom_patrol(duration_seconds), yahboom_diagnostics().
- **Scripts**: `scripts/check_health.py` (REST health/telemetry), `scripts/run_patrol_square.ps1` (run server + dashboard hint).
- **Docs**: `docs/CONNECTIVITY.md`, `docs/architecture.md`, `docs/fleet_overview.md`.
