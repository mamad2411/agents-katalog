---
name: moveit2
description: MoveIt2 motion planning, kinematics, collision checking, trajectory execution, and manipulation pipelines for robotic arms.
category: manipulation
tags: [moveit, moveit2, manipulation, motion-planning, kinematics, ompl, collision, trajectory]
version: "1.0.0"
---

# MoveIt2

MoveIt2 is the standard motion planning framework for ROS2. This skill covers configuration, kinematics solvers, collision checking, and manipulation pipelines.

## When to Use

- Configuring MoveIt for a new robot arm
- Setting up motion planning pipelines (OMPL, STOMP, CHOMP, Pilz)
- Implementing inverse kinematics (KDL, IKFast, TracIK, BioIK)
- Configuring collision checking (FCL, Bullet)
- Setting up planning scenes and collision objects
- Implementing pick-and-place pipelines
- Configuring trajectory execution and monitoring
- Debugging planning failures and IK issues
- Setting up grasp planning and manipulation

## Quick Start

```bash
# Install MoveIt2 (ROS2 Humble)
sudo apt update
sudo apt install ros-humble-moveit ros-humble-moveit-resources

# Source ROS2
source /opt/ros/humble/setup.bash

# Launch demo with Panda arm
ros2 launch moveit_resources_panda_moveit_config demo.launch.py

# Launch RViz with MotionPlanning plugin
ros2 launch moveit2_tutorials demo.launch.py
```

## Core Concepts

### 1. MoveIt Configuration Package

The MoveIt configuration package contains all robot-specific settings.

**Directory structure:**
```
my_robot_moveit_config/
├── config/
│   ├── my_robot.srdf           # Semantic robot description
│   ├── kinematics.yaml         # IK solver configuration
│   ├── joint_limits.yaml       # Velocity/acceleration limits
│   ├── sensors_3d.yaml         # Point cloud sensors
│   ├── ompl_planning.yaml      # OMPL planner settings
│   ├── chomp_planning.yaml     # CHOMP planner settings
│   ├── stomp_planning.yaml     # STOMP planner settings
│   ├── pilz_cartesian_limits.yaml  # Cartesian limits
│   └── ros_controllers.yaml    # Controller configuration
├── launch/
│   ├── demo.launch.py
│   ├── move_group.launch.py
│   └── moveit_rviz.launch.py
└── .setup_assistant            # Setup Assistant config
```

**Creating configuration with Setup Assistant:**
```bash
# Run MoveIt Setup Assistant
ros2 run moveit_setup_assistant moveit_setup_assistant

# Steps:
# 1. Load URDF/Xacro
# 2. Generate collision matrix (ACM)
# 3. Define planning groups (arm, gripper)
# 4. Define end effectors
# 5. Define named poses (home, ready)
# 6. Configure controllers
# 7. Generate configuration package
```

### 2. SRDF (Semantic Robot Description Format)

SRDF defines planning groups, end effectors, and virtual joints.

```xml
<?xml version="1.0"?>
<robot name="my_robot">
    <!-- Planning groups -->
    <group name="panda_arm">
        <chain base_link="panda_link0" tip_link="panda_link8"/>
    </group>
    
    <group name="hand">
        <link name="panda_hand"/>
        <link name="panda_leftfinger"/>
        <link name="panda_rightfinger"/>
        <joint name="panda_finger_joint1"/>
        <joint name="panda_finger_joint2"/>
    </group>
    
    <!-- End effector -->
    <end_effector name="panda_hand" parent_link="panda_link8" group="hand"/>
    
    <!-- Virtual joint for mobile base -->
    <virtual_joint name="virtual_base" type="planar" parent_frame="odom" child_link="base_link"/>
    
    <!-- Named states -->
    <group_state name="ready" group="panda_arm">
        <joint name="panda_joint1" value="0"/>
        <joint name="panda_joint2" value="-0.785"/>
        <joint name="panda_joint3" value="0"/>
        <joint name="panda_joint4" value="-2.356"/>
        <joint name="panda_joint5" value="0"/>
        <joint name="panda_joint6" value="1.571"/>
        <joint name="panda_joint7" value="0.785"/>
    </group_state>
    
    <!-- Disable collision between adjacent links -->
    <disable_collisions link1="panda_link0" link2="panda_link1" reason="Adjacent"/>
    <disable_collisions link1="panda_link1" link2="panda_link2" reason="Adjacent"/>
    <!-- ... -->
</robot>
```

### 3. Kinematics Configuration

Choose the right IK solver for your application.

**kinematics.yaml:**
```yaml
panda_arm:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin
  kinematics_solver_search_resolution: 0.005
  kinematics_solver_timeout: 0.005
  kinematics_solver_attempts: 3

hand:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin
  kinematics_solver_search_resolution: 0.005
  kinematics_solver_timeout: 0.005
  kinematics_solver_attempts: 3
```

**Solver comparison:**

| Solver | Speed | Accuracy | Setup | Best For |
|--------|-------|----------|-------|----------|
| KDL | Medium | Good | Easy | General purpose, prototyping |
| IKFast | Very Fast | High | Hard | Production, repeated queries |
| TracIK | Fast | High | Easy | Real-time applications |
| BioIK | Medium | High | Medium | Complex constraints, humanoids |
| LMA | Medium | Good | Easy | Alternative to KDL |

**TracIK configuration:**
```yaml
panda_arm:
  kinematics_solver: trac_ik_kinematics_plugin/TRAC_IKKinematicsPlugin
  kinematics_solver_timeout: 0.005
  kinematics_solver_attempts: 3
  solve_type: Speed  # Speed, Distance, Manipulation1, Manipulation2
```

**IKFast setup:**
```bash
# Install OpenRAVE dependencies
sudo apt install openrave0.8-dp-dev

# Generate IKFast plugin
python3 `openrave-config --python-dir`/openravepy/_openravepy_/ikfast.py \
  --robot=my_robot.robot.xml \
  --baselink=0 \
  --eelink=7 \
  --freejoint=6 \
  --savefile=output_ikfast61.cpp \
  --iktype=transform6d
```

### 4. Motion Planning Pipeline

Configure planners for different use cases.

**ompl_planning.yaml:**
```yaml
planning_plugin: ompl_interface/OMPLPlanner
request_adapters: >-
    default_planner_request_adapters/AddTimeOptimalParameterization
    default_planner_request_adapters/ResolveConstraintFrames
    default_planner_request_adapters/FixWorkspaceBounds
    default_planner_request_adapters/FixStartStateBounds
    default_planner_request_adapters/FixStartStateCollision
    default_planner_request_adapters/FixStartStatePathConstraints
start_state_max_bounds_error: 0.1

panda_arm:
  planner_configs:
    - SBLkConfigDefault
    - ESTkConfigDefault
    - LBKPIECEkConfigDefault
    - BKPIECEkConfigDefault
    - KPIECEkConfigDefault
    - RRTkConfigDefault
    - RRTConnectkConfigDefault
    - RRTstarkConfigDefault
    - TRRTkConfigDefault
    - PRMkConfigDefault
    - PRMstarkConfigDefault
    - FMTkConfigDefault
    - BFMTkConfigDefault
    - PDSTkConfigDefault
    - STRIDEkConfigDefault
    - BiTRRTkConfigDefault
    - LBTRRTkConfigDefault
    - BiESTkConfigDefault
    - ProjESTkConfigDefault
    - LazyPRMkConfigDefault
    - LazyPRMstarkConfigDefault
    - SPARSkConfigDefault
    - SPARStwokConfigDefault
    - TrajOptDefault

planner_configs:
  RRTkConfigDefault:
    type: geometric::RRT
    range: 0.0
    goal_bias: 0.05
    
  RRTConnectkConfigDefault:
    type: geometric::RRTConnect
    range: 0.0
    
  RRTstarkConfigDefault:
    type: geometric::RRTstar
    range: 0.0
    goal_bias: 0.05
    delay_collision_checking: 1
    
  PRMkConfigDefault:
    type: geometric::PRM
    max_nearest_neighbors: 10
    
  PRMstarkConfigDefault:
    type: geometric::PRMstar
```

**Planner selection guide:**

| Planner | Type | Speed | Optimality | Best For |
|---------|------|-------|------------|----------|
| RRT | Sampling | Fast | No | Quick solutions, exploration |
| RRTConnect | Sampling | Very Fast | No | Bi-directional, fast planning |
| RRT* | Sampling | Medium | Asymptotic | Path quality matters |
| PRM | Roadmap | Slow (preprocess) | No | Multiple queries |
| PRM* | Roadmap | Slow | Asymptotic | High-quality roadmap |
| CHOMP | Optimization | Medium | Local | Smooth trajectories |
| STOMP | Stochastic | Medium | No | Noisy environments |
| TrajOpt | Optimization | Fast | Local | Fast smooth planning |

### 5. Joint Limits

Define realistic velocity and acceleration limits.

**joint_limits.yaml:**
```yaml
joint_limits:
  panda_joint1:
    has_velocity_limits: true
    max_velocity: 2.1750
    has_acceleration_limits: true
    max_acceleration: 3.75
    has_jerk_limits: true
    max_jerk: 5000
    
  panda_joint2:
    has_velocity_limits: true
    max_velocity: 2.1750
    has_acceleration_limits: true
    max_acceleration: 1.875
    has_jerk_limits: true
    max_jerk: 5000
    
  # ... more joints
  
  panda_finger_joint1:
    has_velocity_limits: true
    max_velocity: 0.1
    has_acceleration_limits: true
    max_acceleration: 1.0
```

**Cartesian limits (for Pilz planner):**
```yaml
cartesian_limits:
  max_trans_vel: 1.0
  max_trans_acc: 2.25
  max_trans_dec: -5.0
  max_rot_vel: 1.57
```

## Common Patterns

### Pattern 1: Basic Motion Planning (C++)

```cpp
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/msg/display_trajectory.hpp>

class MotionPlanner {
public:
    explicit MotionPlanner(const rclcpp::Node::SharedPtr& node)
        : node_(node),
          move_group_(std::make_shared<moveit::planning_interface::MoveGroupInterface>(
              node, "panda_arm")),
          planning_scene_interface_(node) {
        
        // Set planning parameters
        move_group_->setPlanningTime(10.0);
        move_group_->setNumPlanningAttempts(5);
        move_group_->setMaxVelocityScalingFactor(0.5);
        move_group_->setMaxAccelerationScalingFactor(0.5);
        
        RCLCPP_INFO(node_->get_logger(), "Planning frame: %s", 
                   move_group_->getPlanningFrame().c_str());
        RCLCPP_INFO(node_->get_logger(), "End effector link: %s",
                   move_group_->getEndEffectorLink().c_str());
    }

    bool planToJointGoal(const std::vector<double>& joint_values) {
        move_group_->setJointValueTarget(joint_values);
        move_group_->setPlannerId("RRTConnectkConfigDefault");
        
        moveit::planning_interface::MoveGroupInterface::Plan plan;
        bool success = (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS);
        
        if (success) {
            RCLCPP_INFO(node_->get_logger(), "Plan found! Executing...");
            move_group_->execute(plan);
        } else {
            RCLCPP_ERROR(node_->get_logger(), "Planning failed!");
        }
        
        return success;
    }

    bool planToPoseGoal(const geometry_msgs::msg::Pose& target_pose) {
        move_group_->setPoseTarget(target_pose);
        move_group_->setGoalTolerance(0.01);  // 1cm tolerance
        move_group_->setGoalOrientationTolerance(0.05);  // ~3 degrees
        
        moveit::planning_interface::MoveGroupInterface::Plan plan;
        bool success = (move_group_->plan(plan) == moveit::core::MoveItErrorCode::SUCCESS);
        
        if (success) {
            move_group_->execute(plan);
        }
        
        return success;
    }

    bool planCartesianPath(const std::vector<geometry_msgs::msg::Pose>& waypoints) {
        moveit_msgs::msg::RobotTrajectory trajectory;
        const double jump_threshold = 0.0;
        const double eef_step = 0.01;
        
        double fraction = move_group_->computeCartesianPath(
            waypoints, eef_step, jump_threshold, trajectory);
        
        RCLCPP_INFO(node_->get_logger(), "Cartesian path: %.2f%% achieved", fraction * 100.0);
        
        if (fraction > 0.9) {
            moveit::planning_interface::MoveGroupInterface::Plan plan;
            plan.trajectory_ = trajectory;
            move_group_->execute(plan);
            return true;
        }
        
        return false;
    }

private:
    rclcpp::Node::SharedPtr node_;
    std::shared_ptr<moveit::planning_interface::MoveGroupInterface> move_group_;
    moveit::planning_interface::PlanningSceneInterface planning_scene_interface_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("motion_planner");
    
    // Spin in background for service callbacks
    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(node);
    std::thread executor_thread([&executor]() { executor.spin(); });
    
    MotionPlanner planner(node);
    
    // Plan to named target
    planner.planToJointGoal({0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785});
    
    executor_thread.join();
    rclcpp::shutdown();
    return 0;
}
```

### Pattern 2: Planning Scene and Collision Objects

```cpp
void addCollisionObjects() {
    moveit::planning_interface::PlanningSceneInterface psi;
    
    std::vector<moveit_msgs::msg::CollisionObject> collision_objects;
    
    // Add table
    moveit_msgs::msg::CollisionObject table;
    table.id = "table";
    table.header.frame_id = "panda_link0";
    
    shape_msgs::msg::SolidPrimitive table_primitive;
    table_primitive.type = table_primitive.BOX;
    table_primitive.dimensions = {0.6, 1.0, 0.05};  // x, y, z
    
    geometry_msgs::msg::Pose table_pose;
    table_pose.position.x = 0.5;
    table_pose.position.y = 0.0;
    table_pose.position.z = -0.025;
    table_pose.orientation.w = 1.0;
    
    table.primitives.push_back(table_primitive);
    table.primitive_poses.push_back(table_pose);
    table.operation = table.ADD;
    
    collision_objects.push_back(table);
    
    // Add box to pick
    moveit_msgs::msg::CollisionObject box;
    box.id = "box";
    box.header.frame_id = "panda_link0";
    
    shape_msgs::msg::SolidPrimitive box_primitive;
    box_primitive.type = box_primitive.BOX;
    box_primitive.dimensions = {0.05, 0.05, 0.05};
    
    geometry_msgs::msg::Pose box_pose;
    box_pose.position.x = 0.5;
    box_pose.position.y = 0.0;
    box_pose.position.z = 0.025;
    box_pose.orientation.w = 1.0;
    
    box.primitives.push_back(box_primitive);
    box.primitive_poses.push_back(box_pose);
    box.operation = box.ADD;
    
    collision_objects.push_back(box);
    
    psi.applyCollisionObjects(collision_objects);
    
    // Attach object to gripper
    moveit_msgs::msg::AttachedCollisionObject attached_object;
    attached_object.link_name = "panda_hand";
    attached_object.object = box;
    attached_object.touch_links = {"panda_hand", "panda_leftfinger", "panda_rightfinger"};
    
    psi.applyAttachedCollisionObject(attached_object);
}

void removeCollisionObject(const std::string& id) {
    moveit::planning_interface::PlanningSceneInterface psi;
    
    std::vector<std::string> object_ids;
    object_ids.push_back(id);
    psi.removeCollisionObjects(object_ids);
}
```

### Pattern 3: Pick and Place Pipeline

```cpp
#include <moveit/task_constructor/solvers.h>
#include <moveit/task_constructor/stages.h>
#include <moveit/task_constructor/task.h>

namespace mtc = moveit::task_constructor;

class PickPlaceTask {
public:
    PickPlaceTask(const rclcpp::Node::SharedPtr& node, 
                  const std::string& task_name)
        : node_(node), task_name_(task_name) {}

    bool init(const geometry_msgs::msg::Pose& pick_pose,
              const geometry_msgs::msg::Pose& place_pose) {
        
        task_.stages()->setName(task_name_);
        task_.loadRobotModel(node_);
        
        // Sampling planners
        auto sampling_planner = std::make_shared<mtc::solvers::PipelinePlanner>(node_);
        sampling_planner->setProperty("planner", "RRTConnectkConfigDefault");
        
        // Cartesian planner for approach/retreat
        auto cartesian_planner = std::make_shared<mtc::solvers::CartesianPath>();
        cartesian_planner->setMaxVelocityScalingFactor(0.5);
        cartesian_planner->setMaxAccelerationScalingFactor(0.5);
        cartesian_planner->setStepSize(0.01);
        
        // Task stages
        auto stage_state_current = std::make_unique<mtc::stages::CurrentState>("current");
        task_.add(std::move(stage_state_current));
        
        // Open hand
        auto stage_open_hand = std::make_unique<mtc::stages::MoveTo>("open hand", sampling_planner);
        stage_open_hand->setGroup("hand");
        stage_open_hand->setGoal("open");
        task_.add(std::move(stage_open_hand));
        
        // Move to pick
        auto stage_move_to_pick = std::make_unique<mtc::stages::Connect>(
            "move to pick", mtc::stages::Connect::GroupPlannerVector{{"panda_arm", sampling_planner}});
        stage_move_to_pick->setTimeout(5.0);
        task_.add(std::move(stage_move_to_pick));
        
        // Pick container
        auto grasp = std::make_unique<mtc::SerialContainer>("pick object");
        
        // Approach
        auto stage_approach = std::make_unique<mtc::stages::MoveRelative>("approach object", cartesian_planner);
        stage_approach->properties().configureInitFrom(mtc::Stage::PARENT, {"group"});
        stage_approach->setMinMaxDistance(0.1, 0.15);
        
        geometry_msgs::msg::Vector3Stamped vec;
        vec.header.frame_id = "panda_hand";
        vec.vector.z = 1;
        stage_approach->setDirection(vec);
        grasp->insert(std::move(stage_approach));
        
        // Generate grasp pose
        auto stage_grasp_pose = std::make_unique<mtc::stages::GenerateGraspPose>("generate grasp pose");
        stage_grasp_pose->properties().configureInitFrom(mtc::Stage::PARENT);
        stage_grasp_pose->setPreGraspPose("open");
        stage_grasp_pose->setObject("box");
        stage_grasp_pose->setAngleDelta(M_PI / 6);
        stage_grasp_pose->setMonitoredStage(task_.stages()->findChild("current"));
        
        // Compute IK
        auto wrapper = std::make_unique<mtc::stages::ComputeIK>("grasp pose IK", std::move(stage_grasp_pose));
        wrapper->setMaxIKSolutions(8);
        wrapper->setMinSolutionDistance(1.0);
        wrapper->setIKFrame("panda_hand");
        wrapper->properties().configureInitFrom(mtc::Stage::PARENT, {"target_pose"});
        grasp->insert(std::move(wrapper));
        
        // Allow collision
        auto stage_allow_collision = std::make_unique<mtc::stages::ModifyPlanningScene>("allow collision");
        stage_allow_collision->allowCollisions("box", 
            task_.getRobotModel()->getJointModelGroup("hand")->getLinkModelNamesWithCollisionGeometry(), 
            true);
        grasp->insert(std::move(stage_allow_collision));
        
        // Close hand
        auto stage_close_hand = std::make_unique<mtc::stages::MoveTo>("close hand", sampling_planner);
        stage_close_hand->setGroup("hand");
        stage_close_hand->setGoal("close");
        grasp->insert(std::move(stage_close_hand));
        
        // Attach object
        auto stage_attach = std::make_unique<mtc::stages::ModifyPlanningScene>("attach object");
        stage_attach->attachObject("box", "panda_hand");
        grasp->insert(std::move(stage_attach));
        
        // Lift
        auto stage_lift = std::make_unique<mtc::stages::MoveRelative>("lift object", cartesian_planner);
        stage_lift->properties().configureInitFrom(mtc::Stage::PARENT, {"group"});
        stage_lift->setMinMaxDistance(0.03, 0.05);
        vec.vector.z = -1;
        stage_lift->setDirection(vec);
        grasp->insert(std::move(stage_lift));
        
        task_.add(std::move(grasp));
        
        // Plan task
        try {
            task_.init();
            return task_.plan(5);  // 5 planning attempts
        } catch (const mtc::InitStageException& e) {
            RCLCPP_ERROR_STREAM(node_->get_logger(), "Task initialization failed: " << e);
            return false;
        }
    }

    bool execute() {
        if (task_.solutions().empty()) {
            RCLCPP_ERROR(node_->get_logger(), "No solutions found");
            return false;
        }
        
        return task_.execute(*task_.solutions().front()) == mtc::Task::SUCCESS;
    }

private:
    rclcpp::Node::SharedPtr node_;
    std::string task_name_;
    mtc::Task task_;
};
```

### Pattern 4: Python Planning Interface

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from moveit.planning import MoveItPy
from moveit.core.kinematic_constraints import construct_joint_constraint
from geometry_msgs.msg import Pose, PoseStamped

class MoveItInterface(Node):
    def __init__(self):
        super().__init__('moveit_interface')
        
        # Initialize MoveItPy
        self.panda = MoveItPy(node_name="moveit_py")
        self.arm = self.panda.get_planning_component("panda_arm")
        
        self.get_logger().info("MoveIt interface initialized")

    def plan_to_named_target(self, target_name: str):
        """Plan to a named joint configuration."""
        self.arm.set_start_state_to_current_state()
        
        # Set goal from named target
        self.arm.set_goal_state(configuration_name=target_name)
        
        # Plan
        plan_result = self.arm.plan()
        
        if plan_result:
            self.get_logger().info(f"Plan found, executing to {target_name}")
            self.arm.execute()
            return True
        
        self.get_logger().error("Planning failed")
        return False

    def plan_to_pose(self, target_pose: Pose):
        """Plan to a Cartesian pose."""
        self.arm.set_start_state_to_current_state()
        
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = "panda_link0"
        pose_stamped.pose = target_pose
        
        self.arm.set_goal_state(pose_stamped_msg=pose_stamped, 
                               pose_link="panda_hand")
        
        plan_result = self.arm.plan()
        
        if plan_result:
            self.arm.execute()
            return True
        return False

    def plan_cartesian_path(self, waypoints: list):
        """Plan through multiple waypoints."""
        from moveit.core.robot_state import RobotState
        
        self.arm.set_start_state_to_current_state()
        
        # Set multi-waypoint goal
        self.arm.set_goal_state(waypoint_poses=waypoints,
                               waypoint_link="panda_hand",
                               waypoint_frame_id="panda_link0")
        
        plan_result = self.arm.plan()
        
        if plan_result:
            self.arm.execute()
            return True
        return False

def main():
    rclpy.init()
    node = MoveItInterface()
    
    # Plan to ready position
    node.plan_to_named_target("ready")
    
    # Plan to a specific pose
    target_pose = Pose()
    target_pose.position.x = 0.5
    target_pose.position.y = 0.0
    target_pose.position.z = 0.5
    target_pose.orientation.w = 1.0
    
    node.plan_to_pose(target_pose)
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Pattern 5: Constrained Planning

```cpp
// Plan with orientation constraint
void planWithOrientationConstraint() {
    moveit_msgs::msg::OrientationConstraint ocm;
    ocm.link_name = "panda_hand";
    ocm.header.frame_id = "panda_link0";
    ocm.orientation.w = 1.0;
    ocm.absolute_x_axis_tolerance = 0.1;
    ocm.absolute_y_axis_tolerance = 0.1;
    ocm.absolute_z_axis_tolerance = 0.1;
    ocm.weight = 1.0;
    
    moveit_msgs::msg::Constraints constraints;
    constraints.orientation_constraints.push_back(ocm);
    
    move_group_->setPathConstraints(constraints);
    move_group_->setPlanningTime(30.0);  // Longer for constrained planning
    
    // Plan
    geometry_msgs::msg::Pose target;
    target.position.x = 0.5;
    target.position.y = 0.0;
    target.position.z = 0.5;
    target.orientation.w = 1.0;
    
    move_group_->setPoseTarget(target);
    move_group_->move();
    
    // Clear constraints
    move_group_->clearPathConstraints();
}

// Plan with position constraint (keep end-effector in box)
void planWithPositionConstraint() {
    moveit_msgs::msg::PositionConstraint pcm;
    pcm.link_name = "panda_hand";
    pcm.header.frame_id = "panda_link0";
    
    shape_msgs::msg::SolidPrimitive box;
    box.type = box.BOX;
    box.dimensions = {0.1, 0.1, 0.1};  // 10cm cube
    
    pcm.constraint_region.primitives.push_back(box);
    pcm.constraint_region.primitive_poses.push_back(target_pose_);
    pcm.weight = 1.0;
    
    moveit_msgs::msg::Constraints constraints;
    constraints.position_constraints.push_back(pcm);
    
    move_group_->setPathConstraints(constraints);
    move_group_->move();
    move_group_->clearPathConstraints();
}
```

## Anti-Patterns

### ❌ Using default planning time
Using default 5s planning time often leads to suboptimal plans or failures.

**What happens:** Plans fail on complex queries, or return low-quality paths.

### ✅ Tune planning time for query complexity
```cpp
// Simple motions
move_group_->setPlanningTime(1.0);

// Complex constrained motions
move_group_->setPlanningTime(30.0);

// Pre-compute for repeated queries
move_group_->setPlannerId("PRMkConfigDefault");  // Preprocess
```

### ❌ Ignoring collision checking performance
Not using Allowed Collision Matrix (ACM) causes unnecessary collision checks.

**What happens:** Planning is 10-100x slower than necessary.

### ✅ Configure ACM properly
```xml
<disable_collisions link1="link1" link2="link2" reason="Adjacent"/>
<disable_collisions link1="base_link" link2="table" reason="Never"/>
```

### ❌ Planning without joint limits
Using URDF limits only ignores acceleration constraints.

**What happens:** Jerky motions, motor overload, safety violations.

### ✅ Define realistic limits
```yaml
joint_limits:
  joint1:
    max_velocity: 2.0
    max_acceleration: 5.0  # Critical for smooth motion
    max_jerk: 10000
```

### ❌ Not validating IK solutions
Assuming all IK solutions are valid.

**What happens:** Robot reaches joint limits or self-collisions.

### ✅ Validate before execution
```cpp
moveit::core::RobotStatePtr state = move_group_->getCurrentState();
bool ik_valid = state->setFromIK(joint_model_group, target_pose);
if (!ik_valid) {
    RCLCPP_ERROR("IK failed!");
    return;
}
// Check collisions
collision_detection::CollisionRequest req;
collision_detection::CollisionResult res;
planning_scene_->checkCollision(req, res, *state);
if (res.collision) {
    RCLCPP_ERROR("IK solution in collision!");
}
```

## Configuration Reference

### move_group.launch.py

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder

def generate_launch_description():
    moveit_config = (
        MoveItConfigsBuilder("panda", package_name="panda_moveit_config")
        .robot_description(file_path="config/panda.urdf.xacro")
        .robot_description_semantic(file_path="config/panda.srdf")
        .trajectory_execution(file_path="config/moveit_controllers.yaml")
        .planning_pipelines(
            pipelines=["ompl", "chomp", "pilz_industrial_motion_planner"]
        )
        .to_moveit_configs()
    )

    move_group_node = Node(
        package="moveit_ros_move_group",
        executable="move_group",
        output="screen",
        parameters=[
            moveit_config.to_dict(),
            {"use_sim_time": True},
            {"publish_robot_description_semantic": True},
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", moveit_config.package_path / "config/moveit.rviz"],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument("use_sim_time", default_value="true"),
        move_group_node,
        rviz_node,
    ])
```

### Controller Configuration

**ros_controllers.yaml:**
```yaml
controller_manager:
  ros__parameters:
    update_rate: 1000  # Hz
    
    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController
      
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

joint_trajectory_controller:
  ros__parameters:
    joints:
      - panda_joint1
      - panda_joint2
      - panda_joint3
      - panda_joint4
      - panda_joint5
      - panda_joint6
      - panda_joint7
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity
    gains:
      panda_joint1: {p: 100.0, i: 0.0, d: 10.0}
      panda_joint2: {p: 100.0, i: 0.0, d: 10.0}
```

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| "No IK solution found" | IK solver timeout or unreachable pose | Increase timeout, check pose feasibility, try different solver |
| Planning fails silently | Goal in collision | Check planning scene, use valid pose |
| Jerky trajectory | Missing acceleration limits | Define joint_limits.yaml properly |
| Slow planning | No ACM or dense collision mesh | Configure ACM, simplify collision meshes |
| Controller fails to follow path | Inadequate gains or limits | Tune controller gains, check velocity limits |
| "Link not in model" | SRDF/URDF mismatch | Regenerate SRDF, check frame names |
| Trajectory execution fails | Controller not active | Start controller via ros2_control |
| Collision object not visible | Wrong frame_id | Use planning frame (usually base_link) |
| Pick fails at grasp | Missing allow collision | Add allowCollision stage |
| MoveIt crashes on startup | Missing robot_description | Check robot_state_publisher is running |

## Workflow Integration

- **Before this:** Use `robot-modeling` to create URDF/Xacro with proper collision meshes
- **With this:** Use `ros2-control` for hardware interfaces and controller configuration
- **After this:** Use `grasping-force-control` for force/torque controlled manipulation
- **Related:** Use `gazebo` for simulation before hardware deployment

## Further Reading

- [MoveIt Documentation](https://moveit.ros.org/)
- [MoveIt2 Tutorials](https://moveit.picknik.ai/humble/doc/tutorials/tutorials.html)
- [OMPL Documentation](https://ompl.kavrakilab.org/)
- Related skills: `robot-modeling`, `ros2-control`, `grasping-force-control`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering MoveIt2 configuration and planning
- Includes OMPL, kinematics, collision checking, MTC