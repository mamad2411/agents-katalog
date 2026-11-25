# ROS2-skill

Natural-language control of ROS 2 robots. Runs on-board (no rosbridge); auto-discovers topics/nodes/services/actions/message types/safety limits from the live ROS graph; supports emergency-stop rules.

## Triggers
- "ros2 skill"
- "robot control"
- "natural language robot"
- "ros2 command"
- "robotics osint"
- "ros robot control"

## Description
ROS2-skill enables natural language control of ROS 2 robots without requiring rosbridge. It operates on-board the robot, automatically discovering the ROS graph structure including topics, nodes, services, actions, message types, and safety limits. The skill includes emergency-stop functionality for safe operation.

## Features
- On-board natural language processing (no rosbridge required)
- Auto-discovery of ROS 2 graph:
  - Topics
  - Nodes
  - Services
  - Actions
  - Message types
  - Safety limits
- Real-time robot state awareness
- Emergency-stop rule support
- Safe robot operation
- Direct hardware access
- ROS 2 native integration

## Usage
Use when you want to control ROS 2 robots using natural language commands, particularly for field operations, research, or applications where setting up rosbridge is impractical.

## Example
```
/ros2-skill move robot forward 2 meters
/ros2-skill rotate camera to inspect equipment
/ros2-skill emergency stop all motors
/ros2-skill show current robot status and available commands
```
