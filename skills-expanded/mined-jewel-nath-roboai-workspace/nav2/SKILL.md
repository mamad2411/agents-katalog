---
name: nav2
description: ROS2 Nav2 navigation stack including behavior trees, costmaps, planners (NavFn, Smac, ThetaStar), controllers (DWB, RPP, MPPI), and recovery behaviors. Use when configuring mobile robot navigation.
category: navigation
tags: [ros2, nav2, navigation, planning, behavior-trees, costmap]
version: "1.0.0"
---

# Nav2

Nav2 is the ROS2 navigation stack for mobile robots. It provides a complete navigation solution with pluggable planners, controllers, and recovery behaviors orchestrated through behavior trees.

## When to Use

- Configuring autonomous navigation for mobile robots
- Setting up global and local costmaps
- Implementing path planning and obstacle avoidance
- Creating behavior trees for navigation logic
- Tuning planner and controller parameters
- Implementing waypoint following
- Configuring recovery behaviors for stuck situations
- Debugging navigation failures and path planning issues

## Quick Start

```bash
# Install Nav2
sudo apt install ros-$ROS_DISTRO-navigation2 ros-$ROS_DISTRO-nav2-bringup

# Launch TurtleBot3 simulation with Nav2
ros2 launch nav2_bringup tb3_simulation_launch.py

# Or launch with your own robot
ros2 launch nav2_bringup navigation_launch.py \
  use_sim_time:=true \
  params_file:=/path/to/nav2_params.yaml \
  map:=/path/to/map.yaml
```

**Basic Navigation Commands:**
```bash
# Set initial pose
ros2 topic pub /initialpose geometry_msgs/msg/PoseWithCovarianceStamped \
  '{header: {frame_id: "map"}, pose: {pose: {position: {x: 0.0, y: 0.0}, orientation: {w: 1.0}}}}'

# Send navigation goal
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  '{pose: {header: {frame_id: "map"}, pose: {position: {x: 1.0, y: 2.0}, orientation: {w: 1.0}}}}'
```

## Core Concepts

### 1. Nav2 Architecture

Nav2 consists of multiple lifecycle-managed servers that communicate via ROS2 topics and actions:

```
NavigateToPose Action
         ↓
Behavior Tree (BT Navigator)
         ↓
Planner Server ←→ Global Costmap
         ↓
Controller Server ←→ Local Costmap
         ↓
Recovery Server (backup, spin, wait)
         ↓
Robot (via cmd_vel)
```

**Key Servers:**

| Server | Purpose | Default Plugin |
|--------|---------|----------------|
| `bt_navigator` | Behavior tree execution | BehaviorTreeEngine |
| `planner_server` | Global path planning | NavFnPlanner |
| `controller_server` | Local trajectory following | DWBLocalPlanner |
| `recovery_server` | Recovery behaviors | ClearCostmap, Spin, Backup |
| `waypoint_follower` | Multi-waypoint navigation | WaitAtWaypoint |
| `velocity_smoother` | Smooth velocity commands | VelocitySmoother |

### 2. Behavior Trees (BTs)

Behavior trees define navigation logic as a tree of tasks that execute based on conditions.

**Basic Navigation BT:**
```xml
<!-- behavior_trees/navigate_to_pose.xml -->
<root BTCPP_format="4">
  <BehaviorTree ID="NavigateToPose">
    <Sequence name="root">
      <!-- Compute path to goal -->
      <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
      
      <!-- Follow the path -->
      <FollowPath path="{path}" controller_id="FollowPath"/>
      
      <!-- Check if goal reached -->
      <GoalReached goal="{goal}"/>
    </Sequence>
  </BehaviorTree>
</root>
```

**BT with Recovery:**
```xml
<root BTCPP_format="4">
  <BehaviorTree ID="NavigateWithRecovery">
    <RecoveryNode number_of_retries="6" name="NavigateRecovery">
      <Sequence name="NavigateSequence">
        <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
        <FollowPath path="{path}" controller_id="FollowPath"/>
      </Sequence>
      <ReactiveFallback name="RecoveryFallback">
        <GoalReached goal="{goal}"/>
        <SequenceStar name="RecoveryActions">
          <ClearEntireCostmap name="ClearGlobalCostmap" service_name="global_costmap/clear_entirely"/>
          <ClearEntireCostmap name="ClearLocalCostmap" service_name="local_costmap/clear_entirely"/>
          <Spin spin_dist="1.57"/>
          <Wait wait_duration="5.0"/>
        </SequenceStar>
      </ReactiveFallback>
    </RecoveryNode>
  </BehaviorTree>
</root>
```

**Common BT Nodes:**

| Node | Type | Description |
|------|------|-------------|
| `Sequence` | Control | Execute children in order, fail on first failure |
| `ReactiveFallback` | Control | Try alternatives until one succeeds |
| `RecoveryNode` | Decorator | Retry main action with recovery on failure |
| `ComputePathToPose` | Action | Call planner server to compute path |
| `FollowPath` | Action | Call controller server to follow path |
| `Spin` | Action | Rotate robot in place |
| `Backup` | Action | Drive backward |
| `Wait` | Action | Pause execution |
| `ClearEntireCostmap` | Action | Clear costmap obstacles |

### 3. Costmaps

Costmaps represent the environment as a grid where each cell has a cost value.

**Global Costmap** - Static map + obstacles, used for global planning:
```yaml
# Global costmap parameters
global_costmap:
  ros__parameters:
    update_frequency: 1.0
    publish_frequency: 1.0
    global_frame: map
    robot_base_frame: base_link
    rolling_window: false
    track_unknown_space: true
    
    plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
    
    static_layer:
      plugin: "nav2_costmap_2d::StaticLayer"
      map_subscribe_transient_local: true
    
    obstacle_layer:
      plugin: "nav2_costmap_2d::ObstacleLayer"
      observation_sources: scan
      scan:
        topic: /scan
        data_type: LaserScan
        clearing: true
        marking: true
    
    inflation_layer:
      plugin: "nav2_costmap_2d::InflationLayer"
      inflation_radius: 0.55
      cost_scaling_factor: 3.0
```

**Local Costmap** - Dynamic obstacles, used for collision avoidance:
```yaml
# Local costmap parameters
local_costmap:
  ros__parameters:
    update_frequency: 5.0
    publish_frequency: 2.0
    global_frame: odom
    robot_base_frame: base_link
    rolling_window: true
    width: 3
    height: 3
    resolution: 0.05
    
    plugins: ["voxel_layer", "inflation_layer"]
    
    voxel_layer:
      plugin: "nav2_costmap_2d::VoxelLayer"
      origin_z: 0.0
      z_resolution: 0.05
      z_voxels: 16
      max_obstacle_height: 2.0
      observation_sources: scan pointcloud
      scan:
        topic: /scan
        data_type: LaserScan
        clearing: true
        marking: true
        obstacle_range: 2.5
        raytrace_range: 3.0
      pointcloud:
        topic: /camera/depth/color/points
        data_type: PointCloud2
        min_obstacle_height: 0.2
        max_obstacle_height: 1.0
    
    inflation_layer:
      plugin: "nav2_costmap_2d::InflationLayer"
      inflation_radius: 0.45
      cost_scaling_factor: 3.0
```

**Costmap Layers:**

| Layer | Purpose | Use Case |
|-------|---------|----------|
| `static_layer` | Loads map from file | Known environment |
| `obstacle_layer` | 2D obstacle detection | LiDAR, sonar |
| `voxel_layer` | 3D obstacle detection | RGB-D, stereo |
| `inflation_layer` | Cost decay around obstacles | Safety margin |
| `range_layer` | Range sensor (IR, US) | Low-cost sensors |

### 4. Planners

Planners compute global paths from start to goal.

**NavFn (Dijkstra/A*):**
```yaml
planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      use_astar: true        # false = Dijkstra
      allow_unknown: true    # Plan through unknown space
      tolerance: 0.5         # Goal tolerance (m)
```

**Smac Planner (2D/3D/Hybrid):**
```yaml
planner_server:
  ros__parameters:
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_smac_planner/SmacPlanner2D"
      tolerance: 0.5
      downsample_costmap: false
      downsampling_factor: 1
      allow_unknown: false
      max_iterations: 1000000
      max_on_approach_iterations: 1000
      max_planning_time: 5.0
      motion_model_for_search: "DUBIN"  # DUBIN, REEDS_SHEPP, STATE
      angle_quantization_bins: 72
      analytic_expansion_max_length: 3.0
      analytic_expansion_ratio: 3.5
      minimum_turning_radius: 0.4
      reverse_penalty: 2.0
      change_penalty: 0.05
      non_straight_penalty: 1.1
      cost_penalty: 2.0
      retrospective_penalty: 0.015
      lookup_table_size: 20.0
```

**Planner Comparison:**

| Planner | Algorithm | Best For | Constraint Aware |
|---------|-----------|----------|------------------|
| NavFn | A*/Dijkstra | Simple navigation | No |
| Smac 2D | A* (lattice) | Ackermann steering | Yes |
| Smac Hybrid | A* (SE2) | Car-like robots | Yes |
| Theta* | Any-angle | Open spaces | No |

### 5. Controllers

Controllers compute velocity commands to follow the planned path.

**DWB (Dynamic Window Approach):**
```yaml
controller_server:
  ros__parameters:
    controller_plugins: ["FollowPath"]
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      debug_trajectory_details: true
      min_vel_x: 0.0
      max_vel_x: 0.5
      min_vel_y: 0.0
      max_vel_y: 0.0
      max_vel_theta: 1.0
      min_speed_xy: 0.0
      max_speed_xy: 0.5
      min_speed_theta: 0.0
      acc_lim_x: 2.5
      acc_lim_y: 0.0
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_y: 0.0
      decel_lim_theta: -3.2
      
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
      
      BaseObstacle.scale: 0.02
      PathAlign.scale: 32.0
      PathAlign.forward_point_distance: 0.1
      GoalAlign.scale: 24.0
      GoalAlign.forward_point_distance: 0.1
      PathDist.scale: 32.0
      GoalDist.scale: 24.0
      RotateToGoal.scale: 32.0
      RotateToGoal.slowing_factor: 5.0
      RotateToGoal.lookahead_time: -1.0
```

**Regulated Pure Pursuit:**
```yaml
controller_server:
  ros__parameters:
    FollowPath:
      plugin: "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController"
      desired_linear_vel: 0.5
      lookahead_dist: 0.6
      min_lookahead_dist: 0.3
      max_lookahead_dist: 0.9
      lookahead_time: 1.5
      rotate_to_heading_angular_vel: 1.8
      transform_tolerance: 0.1
      use_velocity_scaled_lookahead_dist: false
      min_approach_linear_velocity: 0.05
      approach_velocity_scaling_dist: 1.0
      use_collision_detection: true
      max_allowed_time_to_collision_up_to_carrot: 1.0
      use_regulated_linear_velocity_scaling: true
      use_cost_regulated_linear_velocity_scaling: true
      regulated_linear_scaling_min_radius: 0.9
      regulated_linear_scaling_min_speed: 0.25
      use_rotate_to_heading: true
      rotate_to_heading_min_angle: 0.785
      max_angular_accel: 3.2
      max_lateral_accel: 1.0
      max_robot_pose_search_dist: 10.0
      use_interpolation: true
      cost_scaling_dist: 0.3
      cost_scaling_gain: 1.0
      inflation_cost_scaling_factor: 3.0
```

**Controller Comparison:**

| Controller | Type | Best For | Features |
|------------|------|----------|----------|
| DWB | Sampling-based | General use | Multiple critics |
| RPP | Geometric | Ackermann | Speed regulation |
| MPPI | Optimization | Dynamic env | GPU acceleration |

## Common Patterns

### Pattern 1: Complete Nav2 Configuration

```yaml
# config/nav2_params.yaml
amcl:
  ros__parameters:
    use_sim_time: false
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_footprint"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

bt_navigator:
  ros__parameters:
    use_sim_time: false
    global_frame: map
    robot_base_frame: base_link
    odom_topic: /odom
    default_bt_xml_filename: "navigate_w_replanning_and_recovery.xml"
    bt_loop_duration: 10
    default_server_timeout: 20
    navigators: ["navigate_to_pose", "navigate_through_poses"]
    navigate_to_pose:
      plugin: "nav2_bt_navigator/NavigateToPoseNavigator"
    navigate_through_poses:
      plugin: "nav2_bt_navigator/NavigateThroughPosesNavigator"

controller_server:
  ros__parameters:
    use_sim_time: false
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    failure_tolerance: 0.3
    progress_checker_plugin: "progress_checker"
    goal_checker_plugins: ["general_goal_checker"]
    controller_plugins: ["FollowPath"]
    
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0
    
    general_goal_checker:
      stateful: true
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
    
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      debug_trajectory_details: true
      min_vel_x: 0.0
      max_vel_x: 0.26
      min_vel_y: 0.0
      max_vel_y: 0.0
      max_vel_theta: 1.0
      min_speed_xy: 0.0
      max_speed_xy: 0.26
      min_speed_theta: 0.0
      acc_lim_x: 2.5
      acc_lim_y: 0.0
      acc_lim_theta: 3.2
      decel_lim_x: -2.5
      decel_lim_y: 0.0
      decel_lim_theta: -3.2
      vx_samples: 20
      vy_samples: 5
      vtheta_samples: 20
      sim_time: 1.7
      linear_granularity: 0.05
      angular_granularity: 0.025
      transform_tolerance: 0.2
      xy_goal_tolerance: 0.25
      trans_stopped_velocity: 0.25
      short_circuit_trajectory_evaluation: true
      stateful: true
      critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
      BaseObstacle.scale: 0.02
      PathAlign.scale: 32.0
      PathAlign.forward_point_distance: 0.1
      GoalAlign.scale: 24.0
      GoalAlign.forward_point_distance: 0.1
      PathDist.scale: 32.0
      GoalDist.scale: 24.0
      RotateToGoal.scale: 32.0
      RotateToGoal.slowing_factor: 5.0
      RotateToGoal.lookahead_time: -1.0

local_costmap:
  ros__parameters:
    update_frequency: 5.0
    publish_frequency: 2.0
    global_frame: odom
    robot_base_frame: base_link
    rolling_window: true
    width: 3
    height: 3
    resolution: 0.05
    robot_radius: 0.22
    plugins: ["voxel_layer", "inflation_layer"]
    inflation_layer:
      plugin: "nav2_costmap_2d::InflationLayer"
      cost_scaling_factor: 3.0
      inflation_radius: 0.55
    voxel_layer:
      plugin: "nav2_costmap_2d::VoxelLayer"
      enabled: true
      origin_z: 0.0
      z_resolution: 0.05
      z_voxels: 16
      max_obstacle_height: 2.0
      mark_threshold: 0
      observation_sources: scan
      scan:
        topic: /scan
        data_type: LaserScan
        min_obstacle_height: 0.0
        max_obstacle_height: 2.0
        obstacle_range: 2.5
        raytrace_range: 3.0
        clearing: true
        marking: true
    always_send_full_costmap: true

global_costmap:
  ros__parameters:
    update_frequency: 1.0
    publish_frequency: 1.0
    global_frame: map
    robot_base_frame: base_link
    rolling_window: false
    track_unknown_space: true
    plugins: ["static_layer", "obstacle_layer", "inflation_layer"]
    static_layer:
      plugin: "nav2_costmap_2d::StaticLayer"
      map_subscribe_transient_local: true
      enabled: true
    obstacle_layer:
      plugin: "nav2_costmap_2d::ObstacleLayer"
      enabled: true
      observation_sources: scan
      scan:
        topic: /scan
        data_type: LaserScan
        min_obstacle_height: 0.0
        max_obstacle_height: 2.0
        obstacle_range: 2.5
        raytrace_range: 3.0
        clearing: true
        marking: true
    inflation_layer:
      plugin: "nav2_costmap_2d::InflationLayer"
      cost_scaling_factor: 3.0
      inflation_radius: 0.55
    always_send_full_costmap: true

planner_server:
  ros__parameters:
    expected_planner_frequency: 20.0
    use_sim_time: false
    planner_plugins: ["GridBased"]
    GridBased:
      plugin: "nav2_navfn_planner/NavfnPlanner"
      tolerance: 0.5
      use_astar: false
      allow_unknown: true

recovery_server:
  ros__parameters:
    costmap_topic: local_costmap/costmap_raw
    footprint_topic: local_costmap/published_footprint
    cycle_frequency: 10.0
    recovery_plugins: ["spin", "backup", "wait"]
    spin:
      plugin: "nav2_recoveries/Spin"
      sim_granularity: 0.017
      frequency: 20.0
    backup:
      plugin: "nav2_recoveries/BackUp"
      sim_granularity: 0.017
      frequency: 20.0
      min_linear_vel: -0.18
      max_linear_vel: -0.18
      linear_acc_lim: 1.0
    wait:
      plugin: "nav2_recoveries/Wait"
      duration: 5.0
```

### Pattern 2: Launch File

```python
# launch/navigation.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Arguments
    use_sim_time = LaunchConfiguration('use_sim_time')
    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )
    
    declare_map = DeclareLaunchArgument(
        'map',
        default_value=PathJoinSubstitution([
            FindPackageShare('my_robot_pkg'),
            'maps',
            'office.yaml'
        ]),
        description='Path to map file'
    )
    
    declare_params = DeclareLaunchArgument(
        'params_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('my_robot_pkg'),
            'config',
            'nav2_params.yaml'
        ]),
        description='Path to Nav2 parameters'
    )
    
    # Include Nav2 bringup
    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('nav2_bringup'),
                'launch',
                'navigation_launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'map': map_yaml_file,
            'params_file': params_file,
            'autostart': 'true'
        }.items()
    )
    
    return LaunchDescription([
        declare_use_sim_time,
        declare_map,
        declare_params,
        nav2_bringup
    ])
```

### Pattern 3: Waypoint Following

```python
# waypoint_follower.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateThroughPoses
from geometry_msgs.msg import PoseStamped

class WaypointFollower(Node):
    def __init__(self):
        super().__init__('waypoint_follower')
        self.client = ActionClient(
            self, NavigateThroughPoses, 'navigate_through_poses')
        
    def send_waypoints(self, waypoints):
        """Send a list of waypoints to follow."""
        goal_msg = NavigateThroughPoses.Goal()
        
        for wp in waypoints:
            pose = PoseStamped()
            pose.header.frame_id = 'map'
            pose.header.stamp = self.get_clock().now().to_msg()
            pose.pose.position.x = wp[0]
            pose.pose.position.y = wp[1]
            pose.pose.orientation.w = 1.0
            goal_msg.poses.append(pose)
        
        self.client.wait_for_server()
        self.send_goal_future = self.client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self.send_goal_future.add_done_callback(self.goal_response_callback)
    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        
        self.get_logger().info('Goal accepted')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)
    
    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result}')
    
    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Current waypoint: {feedback.current_waypoint}')

def main(args=None):
    rclpy.init(args=args)
    node = WaypointFollower()
    
    # Define waypoints [(x, y), ...]
    waypoints = [
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
        (0.0, 0.0)
    ]
    
    node.send_waypoints(waypoints)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Anti-Patterns

### ❌ Tight goal tolerances
Setting xy_goal_tolerance < 0.1m or yaw_goal_tolerance < 0.1 rad causes oscillation and timeout failures.

**What happens:** Robot overshoots and oscillates around goal, eventually times out.

### ✅ Use realistic tolerances
```yaml
general_goal_checker:
  xy_goal_tolerance: 0.25  # 25cm is reasonable for mobile robots
  yaw_goal_tolerance: 0.25  # ~15 degrees
```

### ❌ Ignoring costmap inflation
Setting inflation_radius too small causes robot to graze obstacles.

**What happens:** Robot collides with obstacles, gets stuck, or damages itself.

### ✅ Proper inflation for robot footprint
```yaml
inflation_layer:
  inflation_radius: 0.55  # At least robot_radius + safety_margin
  cost_scaling_factor: 3.0
```

### ❌ High controller frequency without compute
Running controller at 50Hz on underpowered hardware causes missed deadlines.

**What happens:** Jerky motion, late velocity commands, unstable control.

### ✅ Match frequency to hardware capability
```yaml
controller_server:
  controller_frequency: 20.0  # 20Hz is sufficient for most robots
```

### ❌ Single-layer costmap for 3D sensors
Using only obstacle_layer with RGB-D cameras loses height information.

**What happens:** Robot collides with overhanging obstacles or drives off ledges.

### ✅ Use voxel_layer for 3D data
```yaml
plugins: ["voxel_layer", "inflation_layer"]
voxel_layer:
  z_resolution: 0.05
  z_voxels: 16
  max_obstacle_height: 2.0
```

## Configuration Reference

### Costmap Cost Values

| Value | Meaning | Color (RViz) |
|-------|---------|--------------|
| 0 | Free space | Blue |
| 1-252 | Cost gradient | Yellow → Red |
| 253 | Inscribed radius | Orange |
| 254 | Lethal obstacle | Red |
| 255 | Unknown space | Gray |

### Planner Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| `tolerance` | Goal tolerance (m) | 0.5 |
| `allow_unknown` | Plan through unknown | true |
| `use_astar` | Use A* vs Dijkstra | true |
| `max_planning_time` | Timeout (s) | 5.0 |

### Controller Parameters

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `max_vel_x` | Max forward speed (m/s) | 0.5 - 2.0 |
| `max_vel_theta` | Max rotation (rad/s) | 1.0 - 3.0 |
| `acc_lim_x` | Forward acceleration (m/s²) | 1.0 - 5.0 |
| `sim_time` | Trajectory lookahead (s) | 1.0 - 2.0 |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| "No valid path found" | Goal in obstacle | Increase tolerance or clear costmap |
| Robot spins in place | Goal tolerance too tight | Increase yaw_goal_tolerance |
| Robot hits obstacles | Inflation too small | Increase inflation_radius |
| Jerky motion | Controller frequency mismatch | Lower controller_frequency or upgrade hardware |
| Path too close to walls | Cost scaling too low | Decrease cost_scaling_factor |
| Robot doesn't move | BT failure | Check behavior tree XML syntax |
| AMCL diverges | Laser min range too small | Set laser_min_range > 0.1 |
| Local planner fails | Max velocity too high | Reduce max_vel_x |
| Costmap not updating | Wrong topic name | Verify scan/pointcloud topic remapping |
| Recovery doesn't trigger | Recovery node misconfigured | Check RecoveryNode parameters |

## Workflow Integration

- **Before this:** Use `robot-modeling` for URDF, `sensor-fusion-slam` for localization
- **After this:** Use `path-planning` for custom algorithms, `safety-systems` for production
- **Parallel with:** Use `camera-vision` or `lidar-pointcloud` for obstacle detection
- **Before deployment:** Test thoroughly in `gazebo` simulation

## Further Reading

- [Nav2 Documentation](https://navigation.ros.org/)
- [BehaviorTree.CPP](https://www.behaviortree.dev/)
- Related skills: `path-planning`, `robot-modeling`, `sensor-fusion-slam`, `safety-systems`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering Nav2 Humble
- Includes behavior trees, costmaps, planners, controllers, recovery