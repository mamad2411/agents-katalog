---
name: robotics-ros2-engineer
description: Architect autonomous systems, mobile robotics, and sensor pipelines using ROS 2 (Humble/Iron/Jazzy), Nav2, and TF2. Enforces real-time safety invariants, lifecycle nodes, and kinematics verification.
---

# Robotics & ROS 2 Engineer Skill

## Purpose
Directs robotics software architecture, sensor integration (LiDAR, IMU, cameras), SLAM, and autonomous navigation.

## When to Use
- Developing ROS 2 packages in C++ (`rclcpp`) or Python (`rclpy`).
- Configuring TF2 coordinate frame trees and URDF kinematics models.
- Implementing Nav2 behavior trees and real-time obstacle avoidance.

## Engineering Workflow
1. **Node Architecture**: Use managed lifecycle nodes for deterministic startup, activation, and recovery.
2. **Transforms & Clocks**: Use the TF2 buffer with exact message header timestamps; avoid hardcoded frame names.
3. **Verification**:
   - `colcon build --packages-select <pkg> --cmake-args -DCMAKE_BUILD_TYPE=Release`
   - `colcon test --packages-select <pkg>`

