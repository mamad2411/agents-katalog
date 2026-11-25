---
name: robot-architecture
description: Robot software architecture with behavior trees, FSMs, component design, state estimation, and multi-robot coordination.
category: architecture
tags: [robot-architecture, behavior-trees, fsm, state-estimation, multi-robot, components]
version: "1.0.0"
---

# Robot Architecture

Software architecture patterns for robust robot systems. This skill covers behavior trees, FSMs, state estimation, and distributed systems.

## The robot software stack

Every robot system follows a layered architecture. Information flows up through perception; decisions flow down through control. Keep the application layer away from direct hardware access.

```
Application layer    — Mission planning, task allocation, UI
Behavioral layer     — Behavior trees, FSMs, decision-making
Functional layer     — Perception, planning, control, estimation
Communication layer — ROS2, DDS, shared memory
Hardware abstraction — Drivers, sensor/actuator interfaces
Hardware layer      — Cameras, LiDARs, motors, grippers
```

## When to Use

- Designing robot behavior hierarchies
- Implementing fault-tolerant state machines
- Architecting multi-robot systems
- Designing component-based software
- Implementing state estimation pipelines
- Creating reusable robot behaviors

## Quick Start

```bash
# Install behavior tree libraries
sudo apt install ros-humble-behaviortree-cpp-v3

# For state estimation
sudo apt install ros-humble-robot-localization
```

## Core Concepts

### 1. Behavior Trees

Hierarchical task decomposition for robot behaviors.

```xml
<!-- behavior_tree.xml -->
<root main_tree_to_execute="MainTree">
  <BehaviorTree ID="MainTree">
    <Sequence>
      <!-- Initialization -->
      <Action ID="InitializeRobot"/>
      
      <!-- Main loop -->
      <ReactiveSequence>
        <!-- Check preconditions -->
        <Condition ID="BatteryOK"/>
        <Condition ID="EmergencyStopClear"/>
        
        <!-- Execute mission -->
        <Selector>
          <Sequence>
            <Condition ID="GoalReached"/>
            <Action ID="CelebrateSuccess"/>
          </Sequence>
          <Sequence>
            <Action ID="ComputePath"/>
            <Action ID="FollowPath"/>
          </Sequence>
        </Selector>
      </ReactiveSequence>
    </Sequence>
  </BehaviorTree>
</root>
```

**C++ Behavior Tree implementation:**
```cpp
#include <behaviortree_cpp_v3/bt_factory.h>

class ComputePath : public BT::SyncActionNode {
public:
    ComputePath(const std::string& name, const BT::NodeConfiguration& config)
        : BT::SyncActionNode(name, config) {}
    
    static BT::PortsList providedPorts() {
        return {BT::InputPort<geometry_msgs::Pose>("goal"),
                BT::OutputPort<nav_msgs::Path>("path")};
    }
    
    BT::NodeStatus tick() override {
        auto goal = getInput<geometry_msgs::Pose>("goal");
        if (!goal) {
            throw BT::RuntimeError("missing required input [goal]");
        }
        
        // Compute path
        nav_msgs::Path path = planner_->plan(goal.value());
        
        setOutput("path", path);
        return BT::NodeStatus::SUCCESS;
    }
    
private:
    std::shared_ptr<PathPlanner> planner_;
};

// Register and use
BT::BehaviorTreeFactory factory;
factory.registerNodeType<ComputePath>("ComputePath");

auto tree = factory.createTreeFromFile("behavior_tree.xml");
tree.tickRoot();
```

### 2. Finite State Machines

Explicit state management for robot modes.

```python
from transitions import Machine

class RobotStateMachine:
    states = ['idle', 'initializing', 'ready', 'executing', 'paused', 'error']
    
    def __init__(self):
        self.machine = Machine(
            model=self,
            states=RobotStateMachine.states,
            initial='idle'
        )
        
        # Transitions
        self.machine.add_transition('initialize', 'idle', 'initializing')
        self.machine.add_transition('init_complete', 'initializing', 'ready')
        self.machine.add_transition('start_mission', 'ready', 'executing')
        self.machine.add_transition('pause', 'executing', 'paused')
        self.machine.add_transition('resume', 'paused', 'executing')
        self.machine.add_transition('complete', 'executing', 'ready')
        self.machine.add_transition('fault', '*', 'error')
        self.machine.add_transition('reset', 'error', 'idle')
        
        # Callbacks
        self.machine.on_enter_executing('on_start_execution')
        self.machine.on_enter_error('on_enter_error')
    
    def on_start_execution(self):
        print("Starting mission execution")
        self.mission_start_time = time.time()
    
    def on_enter_error(self):
        print("Entering error state!")
        self.estop_trigger()
```

### 3. State Estimation

Kalman filters for sensor fusion.

```python
import numpy as np
from filterpy.kalman import KalmanFilter

class RobotStateEstimator:
    def __init__(self):
        # State: [x, y, theta, vx, vy, omega]
        self.kf = KalmanFilter(dim_x=6, dim_z=3)
        
        # State transition (constant velocity model)
        dt = 0.02  # 50 Hz
        self.kf.F = np.array([
            [1, 0, 0, dt, 0, 0],
            [0, 1, 0, 0, dt, 0],
            [0, 0, 1, 0, 0, dt],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        
        # Measurement: [x, y, theta] from localization
        self.kf.H = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0]
        ])
        
        # Covariances
        self.kf.R *= 0.1  # Measurement noise
        self.kf.Q *= 0.01  # Process noise
        self.kf.P *= 10   # Initial uncertainty
    
    def predict(self):
        self.kf.predict()
    
    def update_with_odometry(self, x, y, theta):
        z = np.array([x, y, theta])
        self.kf.update(z)
    
    def update_with_imu(self, vx, vy, omega):
        # Velocity measurement
        H_vel = np.array([
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])
        z_vel = np.array([vx, vy, omega])
        self.kf.update(z_vel, H_vel)
    
    def get_state(self):
        return {
            'position': self.kf.x[:3],
            'velocity': self.kf.x[3:],
            'covariance': self.kf.P
        }
```

### 4. Multi-Robot Coordination

Distributed coordination patterns.

```python
import rclpy
from rclpy.node import Node

class FleetCoordinator(Node):
    def __init__(self):
        super().__init__('fleet_coordinator')
        
        self.robots = {}  # robot_id -> status
        
        # Auction-based task allocation
        self.task_queue = []
        self.auction_in_progress = False
        
        self.create_subscription(RobotStatus, '/fleet/status', self.status_callback)
        self.create_publisher(TaskAssignment, '/fleet/assignments', 10)
    
    def allocate_task(self, task):
        """Auction-based task allocation."""
        if not self.robots:
            self.task_queue.append(task)
            return
        
        # Request bids
        bids = {}
        for robot_id, status in self.robots.items():
            if status['available']:
                bid = self.compute_bid(robot_id, task)
                bids[robot_id] = bid
        
        # Winner takes task
        if bids:
            winner = min(bids, key=bids.get)
            self.assign_task(winner, task)
    
    def compute_bid(self, robot_id, task):
        """Compute cost for robot to execute task."""
        robot_pos = self.robots[robot_id]['position']
        task_pos = task['position']
        
        distance = np.linalg.norm(robot_pos - task_pos)
        battery_factor = 1.0 / self.robots[robot_id]['battery']
        
        return distance * battery_factor
```

## Configuration Reference

| Pattern | Use Case | Complexity | Flexibility |
|---------|----------|------------|-------------|
| Behavior Trees | Task sequences | Medium | High |
| FSM | Mode management | Low | Low |
| State Machine | Complex logic | Medium | Medium |
| Multi-agent | Fleet coordination | High | High |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| BT tick fails | Missing blackboard entry | Check port connections |
| State explosion | Too many FSM states | Use hierarchical FSM |
| Estimation drift | Poor sensor fusion | Tune Q/R matrices |

## Common Patterns

### Pattern 1: Hierarchical Behavior Tree with Reactive Safety Layer

A two-tier BT where the outer `ReactiveSequence` continuously monitors safety
conditions and the inner subtree handles the mission. Any safety failure preempts
the mission immediately.

```cpp
// safety_condition.hpp
#pragma once
#include <behaviortree_cpp_v3/bt_factory.h>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/battery_state.hpp>

class BatteryOK : public BT::ConditionNode {
public:
    BatteryOK(const std::string& name, const BT::NodeConfiguration& config)
        : BT::ConditionNode(name, config) {}

    static BT::PortsList providedPorts() {
        return {BT::InputPort<double>("min_voltage", 11.0, "Minimum safe voltage")};
    }

    BT::NodeStatus tick() override {
        auto min_v = getInput<double>("min_voltage").value();
        double voltage = 0.0;
        if (!getInput<double>("battery_voltage", voltage)) {
            return BT::NodeStatus::FAILURE;
        }
        return (voltage >= min_v) ? BT::NodeStatus::SUCCESS
                                   : BT::NodeStatus::FAILURE;
    }
};

class EmergencyStopClear : public BT::ConditionNode {
public:
    EmergencyStopClear(const std::string& name, const BT::NodeConfiguration& config)
        : BT::ConditionNode(name, config) {}

    static BT::PortsList providedPorts() { return {}; }

    BT::NodeStatus tick() override {
        bool estop = false;
        getInput<bool>("estop_active", estop);
        return estop ? BT::NodeStatus::FAILURE : BT::NodeStatus::SUCCESS;
    }
};
```

```xml
<!-- hierarchical_mission.xml -->
<root main_tree_to_execute="MissionTree">
  <BehaviorTree ID="MissionTree">
    <!-- Outer reactive sequence: safety preempts everything -->
    <ReactiveSequence name="SafetyGuard">
      <BatteryOK min_voltage="11.0" battery_voltage="{battery_voltage}"/>
      <EmergencyStopClear estop_active="{estop_active}"/>

      <!-- Inner mission subtree only runs when safe -->
      <SubTree ID="MissionSubTree" goal="{current_goal}"/>
    </ReactiveSequence>
  </BehaviorTree>

  <BehaviorTree ID="MissionSubTree">
    <Selector name="MissionSelector">
      <!-- If goal already reached, succeed immediately -->
      <Condition ID="GoalReached" goal="{goal}" threshold="0.15"/>

      <!-- Otherwise navigate -->
      <Sequence name="NavigateToGoal">
        <Action ID="ComputePath" goal="{goal}" path="{current_path}"/>
        <Action ID="FollowPath"  path="{current_path}"/>
        <Action ID="AnnounceArrival"/>
      </Sequence>

      <!-- Recovery fallback -->
      <Sequence name="Recovery">
        <Action ID="ClearCostmap"/>
        <Action ID="RotateInPlace" angle="3.14159"/>
      </Sequence>
    </Selector>
  </BehaviorTree>
</root>
```

```cpp
// mission_node.cpp
#include <rclcpp/rclcpp.hpp>
#include <behaviortree_cpp_v3/bt_factory.h>

class MissionExecutorNode : public rclcpp::Node {
public:
    MissionExecutorNode() : Node("mission_executor") {
        // Register all action/condition nodes
        factory_.registerNodeType<BatteryOK>("BatteryOK");
        factory_.registerNodeType<EmergencyStopClear>("EmergencyStopClear");
        // ... register remaining nodes

        tree_ = factory_.createTreeFromFile(
            ament_index_cpp::get_package_share_directory("orbibot_bringup")
            + "/bt/hierarchical_mission.xml"
        );

        // Tick the tree at 10 Hz
        timer_ = create_wall_timer(
            std::chrono::milliseconds(100),
            [this]() { tree_.tickRoot(); }
        );
    }

private:
    BT::BehaviorTreeFactory factory_;
    BT::Tree tree_;
    rclcpp::TimerBase::SharedPtr timer_;
};
```

### Pattern 2: Pure Python FSM with ROS 2 Integration

A state machine that owns ROS 2 publishers/subscribers and maps cleanly to a
lifecycle without using external state machine libraries.

```python
# robot_fsm.py
from __future__ import annotations

import time
from enum import Enum, auto
from typing import Callable, Dict, Optional

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class RobotState(Enum):
    IDLE = auto()
    INITIALIZING = auto()
    READY = auto()
    NAVIGATING = auto()
    PAUSED = auto()
    RECOVERING = auto()
    ERROR = auto()


# Allowed transitions: {from_state: {event: to_state}}
TRANSITIONS: Dict[RobotState, Dict[str, RobotState]] = {
    RobotState.IDLE: {
        'start_init': RobotState.INITIALIZING,
    },
    RobotState.INITIALIZING: {
        'init_ok': RobotState.READY,
        'fault': RobotState.ERROR,
    },
    RobotState.READY: {
        'navigate': RobotState.NAVIGATING,
        'fault': RobotState.ERROR,
    },
    RobotState.NAVIGATING: {
        'pause': RobotState.PAUSED,
        'goal_reached': RobotState.READY,
        'obstacle': RobotState.RECOVERING,
        'fault': RobotState.ERROR,
    },
    RobotState.PAUSED: {
        'resume': RobotState.NAVIGATING,
        'cancel': RobotState.READY,
        'fault': RobotState.ERROR,
    },
    RobotState.RECOVERING: {
        'recovery_ok': RobotState.NAVIGATING,
        'recovery_failed': RobotState.ERROR,
    },
    RobotState.ERROR: {
        'reset': RobotState.IDLE,
    },
}


class RobotFSM(Node):
    """ROS 2 node that encapsulates the complete robot state machine."""

    def __init__(self):
        super().__init__('robot_fsm')

        self._state = RobotState.IDLE
        self._state_entry_time: float = time.time()

        # Entry/exit hooks keyed by state
        self._on_enter: Dict[RobotState, Callable] = {
            RobotState.INITIALIZING: self._on_enter_initializing,
            RobotState.NAVIGATING:   self._on_enter_navigating,
            RobotState.RECOVERING:   self._on_enter_recovering,
            RobotState.ERROR:        self._on_enter_error,
        }
        self._on_exit: Dict[RobotState, Callable] = {
            RobotState.NAVIGATING: self._on_exit_navigating,
        }

        # ROS interfaces
        self._cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self._state_pub = self.create_publisher(String, '/orbibot/fsm_state', 10)
        self._event_sub = self.create_subscription(
            String, '/orbibot/fsm_event', self._on_event_msg, 10
        )

        # Publish state at 5 Hz
        self.create_timer(0.2, self._publish_state)
        self.get_logger().info(f'FSM started in state: {self._state.name}')

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def state(self) -> RobotState:
        return self._state

    def trigger(self, event: str) -> bool:
        """Fire a transition event. Returns True if the transition was valid."""
        allowed = TRANSITIONS.get(self._state, {})
        if event not in allowed:
            self.get_logger().warn(
                f'Event "{event}" not valid in state {self._state.name}'
            )
            return False

        next_state = allowed[event]
        self._transition(next_state)
        return True

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _transition(self, next_state: RobotState):
        self.get_logger().info(
            f'FSM: {self._state.name} → {next_state.name}'
        )

        # Exit current state
        if self._state in self._on_exit:
            self._on_exit[self._state]()

        self._state = next_state
        self._state_entry_time = time.time()

        # Enter next state
        if next_state in self._on_enter:
            self._on_enter[next_state]()

    def _on_event_msg(self, msg: String):
        self.trigger(msg.data)

    def _publish_state(self):
        self._state_pub.publish(String(data=self._state.name))

    # ------------------------------------------------------------------
    # State entry/exit callbacks
    # ------------------------------------------------------------------

    def _on_enter_initializing(self):
        self.get_logger().info('Hardware initialization starting...')

    def _on_enter_navigating(self):
        self.get_logger().info('Navigation started')

    def _on_exit_navigating(self):
        # Stop motors when leaving navigating
        self._cmd_vel_pub.publish(Twist())

    def _on_enter_recovering(self):
        self.get_logger().warn('Entering recovery behaviour')
        # Back up slowly for 1 second
        msg = Twist()
        msg.linear.x = -0.1
        self._cmd_vel_pub.publish(msg)
        # Schedule recovery completion check
        self.create_timer(1.5, self._check_recovery, oneshot=True)

    def _check_recovery(self):
        self._cmd_vel_pub.publish(Twist())  # stop
        self.trigger('recovery_ok')

    def _on_enter_error(self):
        self.get_logger().error('Robot in ERROR state — all motion stopped')
        self._cmd_vel_pub.publish(Twist())


def main():
    rclpy.init()
    node = RobotFSM()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Pattern 3: Component Lifecycle Pattern

Decouple component construction from activation using ROS 2 Lifecycle nodes.
Each component follows configure → activate → deactivate → cleanup.

```python
# lidar_component.py
import rclpy
from rclpy.lifecycle import LifecycleNode, TransitionCallbackReturn, State
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


class LidarComponent(LifecycleNode):
    """Lifecycle-managed LiDAR subscriber with configurable parameters."""

    def __init__(self):
        super().__init__('lidar_component')

    # ------------------------------------------------------------------
    # Lifecycle transitions
    # ------------------------------------------------------------------

    def on_configure(self, state: State) -> TransitionCallbackReturn:
        """Declare parameters and allocate non-communicating resources."""
        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('max_range', 12.0)

        self._scan_topic = self.get_parameter('scan_topic').value
        self._max_range = self.get_parameter('max_range').value
        self._latest_scan: LaserScan | None = None

        self.get_logger().info(
            f'LidarComponent configured — topic: {self._scan_topic}'
        )
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state: State) -> TransitionCallbackReturn:
        """Create publishers/subscribers only when activating."""
        self._scan_sub = self.create_subscription(
            LaserScan,
            self._scan_topic,
            self._scan_callback,
            qos_profile_sensor_data,
        )
        self.get_logger().info('LidarComponent activated')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state: State) -> TransitionCallbackReturn:
        """Tear down subscriptions but keep configuration."""
        self.destroy_subscription(self._scan_sub)
        self.get_logger().info('LidarComponent deactivated')
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state: State) -> TransitionCallbackReturn:
        """Release all resources."""
        self._latest_scan = None
        self.get_logger().info('LidarComponent cleaned up')
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, state: State) -> TransitionCallbackReturn:
        return TransitionCallbackReturn.SUCCESS

    # ------------------------------------------------------------------
    # Operational callbacks
    # ------------------------------------------------------------------

    def _scan_callback(self, msg: LaserScan):
        # Filter by max range
        import numpy as np
        ranges = np.array(msg.ranges)
        ranges[ranges > self._max_range] = float('inf')
        msg.ranges = ranges.tolist()
        self._latest_scan = msg

    def get_latest_scan(self) -> LaserScan | None:
        return self._latest_scan


def main():
    rclpy.init()
    node = LidarComponent()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Pattern 4: Blackboard-Driven Shared State Between BT Nodes

Use the BehaviorTree.CPP blackboard to pass data between action and condition
nodes without tight coupling.

```cpp
// navigation_actions.hpp
#pragma once
#include <behaviortree_cpp_v3/bt_factory.h>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <nav_msgs/msg/path.hpp>

// ---------- Condition: is the robot within `threshold` of `goal`? ----------
class GoalReached : public BT::ConditionNode {
public:
    GoalReached(const std::string& name, const BT::NodeConfiguration& cfg)
        : BT::ConditionNode(name, cfg) {}

    static BT::PortsList providedPorts() {
        return {
            BT::InputPort<geometry_msgs::msg::PoseStamped>("goal"),
            BT::InputPort<geometry_msgs::msg::PoseStamped>("robot_pose"),
            BT::InputPort<double>("threshold", 0.15, "Goal tolerance in metres"),
        };
    }

    BT::NodeStatus tick() override {
        auto goal = getInput<geometry_msgs::msg::PoseStamped>("goal");
        auto pose = getInput<geometry_msgs::msg::PoseStamped>("robot_pose");
        auto tol  = getInput<double>("threshold");
        if (!goal || !pose || !tol) return BT::NodeStatus::FAILURE;

        double dx = goal->pose.position.x - pose->pose.position.x;
        double dy = goal->pose.position.y - pose->pose.position.y;
        double dist = std::sqrt(dx * dx + dy * dy);

        return (dist <= tol.value()) ? BT::NodeStatus::SUCCESS
                                     : BT::NodeStatus::FAILURE;
    }
};

// ---------- Action: plan a path and write it to the blackboard ----------
class ComputePath : public BT::StatefulActionNode {
public:
    ComputePath(const std::string& name, const BT::NodeConfiguration& cfg)
        : BT::StatefulActionNode(name, cfg) {}

    static BT::PortsList providedPorts() {
        return {
            BT::InputPort<geometry_msgs::msg::PoseStamped>("goal"),
            BT::OutputPort<nav_msgs::msg::Path>("path"),
        };
    }

    BT::NodeStatus onStart() override {
        auto goal = getInput<geometry_msgs::msg::PoseStamped>("goal");
        if (!goal) return BT::NodeStatus::FAILURE;

        // Launch async planning (non-blocking)
        planning_future_ = std::async(std::launch::async, [this, goal]() {
            return planner_->plan(goal.value());
        });
        return BT::NodeStatus::RUNNING;
    }

    BT::NodeStatus onRunning() override {
        if (planning_future_.wait_for(std::chrono::milliseconds(0))
            != std::future_status::ready) {
            return BT::NodeStatus::RUNNING;
        }

        auto path = planning_future_.get();
        if (path.poses.empty()) return BT::NodeStatus::FAILURE;

        setOutput("path", path);
        return BT::NodeStatus::SUCCESS;
    }

    void onHalted() override { /* cancel planning if needed */ }

private:
    std::shared_ptr<PathPlanner> planner_;
    std::future<nav_msgs::msg::Path> planning_future_;
};
```

### Pattern 5: Health-Check Publisher for All Components

Every component publishes a `diagnostic_msgs/DiagnosticArray` so the system
monitor can detect silent failures.

```python
# health_mixin.py
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from rclpy.node import Node
import time


class HealthCheckMixin:
    """Mixin that adds a periodic health-check publisher to any ROS 2 node.

    Usage:
        class MyNode(HealthCheckMixin, Node):
            def __init__(self):
                Node.__init__(self, 'my_node')
                HealthCheckMixin.__init__(self, publish_rate_hz=1.0)
    """

    def __init__(self, publish_rate_hz: float = 1.0,
                 stale_timeout_s: float = 5.0):
        assert isinstance(self, Node), 'HealthCheckMixin requires a Node subclass'

        self._health_pub = self.create_publisher(
            DiagnosticArray, '/diagnostics', 10
        )
        self._health_timer = self.create_timer(
            1.0 / publish_rate_hz, self._publish_health
        )
        self._last_activity_time: float = time.time()
        self._stale_timeout_s = stale_timeout_s
        self._health_details: dict = {}

    def mark_active(self, detail_key: str = '', detail_value: str = ''):
        """Call this on every message received / work item processed."""
        self._last_activity_time = time.time()
        if detail_key:
            self._health_details[detail_key] = detail_value

    def _publish_health(self):
        age = time.time() - self._last_activity_time
        if age > self._stale_timeout_s:
            level = DiagnosticStatus.WARN
            msg_text = f'No activity for {age:.1f} s'
        else:
            level = DiagnosticStatus.OK
            msg_text = 'OK'

        status = DiagnosticStatus()
        status.level = level
        status.name = self.get_name()
        status.message = msg_text
        status.hardware_id = 'software'
        status.values = [
            KeyValue(key=k, value=v)
            for k, v in self._health_details.items()
        ]
        status.values.append(
            KeyValue(key='last_activity_age_s', value=f'{age:.2f}')
        )

        arr = DiagnosticArray()
        arr.header.stamp = self.get_clock().now().to_msg()
        arr.status = [status]
        self._health_pub.publish(arr)


# Concrete node using the mixin
class ObstacleDetectorNode(HealthCheckMixin, Node):
    def __init__(self):
        Node.__init__(self, 'obstacle_detector')
        HealthCheckMixin.__init__(self, publish_rate_hz=1.0)

        from sensor_msgs.msg import LaserScan
        from rclpy.qos import qos_profile_sensor_data
        self._sub = self.create_subscription(
            LaserScan, '/scan', self._scan_cb, qos_profile_sensor_data
        )

    def _scan_cb(self, msg):
        self.mark_active('scan_stamp', str(msg.header.stamp.sec))
        # ... obstacle detection logic
```

## Anti-Patterns

### Anti-Pattern 1: The God Node

❌ **Wrong — one node does everything, impossible to test or maintain:**
```python
class OrbiBotNode(Node):
    """Controls motors, reads LiDAR, runs SLAM, plans paths, manages battery,
       serves HTTP API, and plays audio — all in one class."""

    def __init__(self):
        super().__init__('orbibot')
        self._serial = serial.Serial('/dev/motordriver', 115200)
        self._lidar = RPLidar('/dev/lidar')
        self._slam = SlamToolbox()
        self._nav2 = Nav2Client()
        self._battery_monitor = BatteryMonitor()
        self._http_server = HTTPServer(port=8082)
        # ... 500 more lines of unrelated concerns

    def _scan_callback(self, msg):
        self._slam.update(msg)          # SLAM concern
        self._nav2.update_costmap(msg)  # Navigation concern
        self._check_obstacles(msg)      # Safety concern
        # ... all mixed together
```

✅ **Correct — one node, one responsibility. Compose via launch:**
```python
# hardware_node.py — ONLY talks to motor driver serial
class HardwareNode(Node):
    def __init__(self):
        super().__init__('hardware_node')
        self._driver = RosmasterDriver('/dev/motordriver')
        self._cmd_vel_sub = self.create_subscription(
            Twist, 'cmd_vel', self._cmd_vel_cb, 10
        )
        self._odom_pub = self.create_publisher(Odometry, 'odom', 10)

# lidar_node.py — ONLY manages LiDAR driver
class LidarNode(Node):
    def __init__(self):
        super().__init__('lidar_node')
        # publishes /scan — nothing else

# slam_node.py — ONLY runs SLAM
# nav2 is a separate process entirely
# orbibot_bringup/launch/robot.launch.py composes them all
```

### Anti-Pattern 2: Spaghetti Callbacks with Shared Mutable State

❌ **Wrong — multiple callbacks write the same variable without synchronisation:**
```python
class MotionController(Node):
    def __init__(self):
        super().__init__('motion_controller')
        self.target_velocity = Twist()      # shared, unprotected
        self.current_pose = Pose()          # shared, unprotected

        self.create_subscription(Twist, 'cmd_vel', self._cmd_cb, 10)
        self.create_subscription(Odometry, 'odom',  self._odom_cb, 10)
        self.create_timer(0.02, self._control_loop)

    def _cmd_cb(self, msg):
        self.target_velocity = msg          # races with _control_loop

    def _odom_cb(self, msg):
        self.current_pose = msg.pose.pose   # races with _control_loop

    def _control_loop(self):
        error = compute_error(self.current_pose, self.target_velocity)
        # state may be partially written by another callback!
```

✅ **Correct — use a `MutuallyExclusiveCallbackGroup` or a lock:**
```python
import threading
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

class MotionController(Node):
    def __init__(self):
        super().__init__('motion_controller')

        self._lock = threading.Lock()
        self._target_velocity = Twist()
        self._current_pose = Pose()

        # All callbacks in the same MutuallyExclusiveCallbackGroup
        # are serialised — they never run concurrently
        cb_group = MutuallyExclusiveCallbackGroup()

        self.create_subscription(
            Twist, 'cmd_vel', self._cmd_cb, 10, callback_group=cb_group
        )
        self.create_subscription(
            Odometry, 'odom', self._odom_cb, 10, callback_group=cb_group
        )
        self.create_timer(0.02, self._control_loop, callback_group=cb_group)

    def _cmd_cb(self, msg):
        self._target_velocity = msg       # safe: serialised by callback group

    def _odom_cb(self, msg):
        self._current_pose = msg.pose.pose

    def _control_loop(self):
        # Never races with the subscription callbacks
        error = compute_error(self._current_pose, self._target_velocity)
```

### Anti-Pattern 3: Tight Coupling Between Behaviour and Hardware

❌ **Wrong — behaviour node directly imports the hardware driver:**
```python
# navigate_to_goal.py — a "behaviour" that knows about serial hardware
from orbibot_hardware.rosmaster_driver import RosmasterDriver

class NavigateToGoal:
    def __init__(self):
        self._driver = RosmasterDriver('/dev/motordriver')   # hardware dependency!

    def execute(self, goal_pose):
        path = self._plan(goal_pose)
        for waypoint in path:
            vel = self._compute_vel(waypoint)
            self._driver.send_velocity(vel)   # directly drives motors
```

✅ **Correct — behaviours publish to topics; hardware node subscribes:**
```python
# navigate_to_goal.py — publishes Twist; knows nothing about hardware
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped

class NavigateToGoal(Node):
    def __init__(self):
        super().__init__('navigate_to_goal')
        # Publishes velocity commands — hardware abstracted behind /cmd_vel
        self._cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self._goal_sub = self.create_subscription(
            PoseStamped, 'goal_pose', self._goal_cb, 10
        )

    def _goal_cb(self, goal: PoseStamped):
        path = self._plan(goal)
        for waypoint in path:
            cmd = self._compute_vel(waypoint)
            self._cmd_vel_pub.publish(cmd)  # hardware-agnostic

# hardware_node.py subscribes to /cmd_vel — totally decoupled from planning
```

### Anti-Pattern 4: Missing Health Checks / Watchdog

❌ **Wrong — silent failure: node crashes but robot keeps driving:**
```python
class HardwareNode(Node):
    def __init__(self):
        super().__init__('hardware_node')
        self._sub = self.create_subscription(
            Twist, 'cmd_vel', self._cmd_cb, 10
        )
        # No watchdog — if cmd_vel stops arriving the robot never stops

    def _cmd_cb(self, msg):
        self._driver.send_velocity(msg.linear.x, msg.angular.z)
        # No timeout — motor keeps last command forever if upstream dies
```

✅ **Correct — command timeout watchdog stops the robot on upstream failure:**
```python
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist

CMD_TIMEOUT_S = 0.5   # module-level constant

class HardwareNode(Node):
    def __init__(self):
        super().__init__('hardware_node')
        self.declare_parameter('cmd_timeout', CMD_TIMEOUT_S)
        self._cmd_timeout = self.get_parameter('cmd_timeout').value
        self._last_cmd_time: float = 0.0

        self._sub = self.create_subscription(
            Twist, 'cmd_vel', self._cmd_cb, 10
        )
        # Watchdog runs at 20 Hz
        self.create_timer(0.05, self._watchdog)

    def _cmd_cb(self, msg: Twist):
        self._last_cmd_time = time.time()
        self._driver.send_velocity(msg.linear.x, msg.angular.z)

    def _watchdog(self):
        age = time.time() - self._last_cmd_time
        if age > self._cmd_timeout:
            # Stop motors — upstream may have crashed
            self._driver.send_velocity(0.0, 0.0)
            self.get_logger().warn(
                f'cmd_vel timeout ({age:.2f} s) — motors stopped',
                throttle_duration_sec=2.0,
            )
```

### Anti-Pattern 5: Using a Flat FSM for Complex Behaviour (State Explosion)

❌ **Wrong — 20+ states with O(N²) transitions for a simple task hierarchy:**
```python
states = [
    'idle', 'init_sensors', 'init_motors', 'init_nav',
    'ready_no_goal', 'ready_with_goal', 'planning', 'plan_failed',
    'navigating_normal', 'navigating_obstacle', 'navigating_recovery1',
    'navigating_recovery2', 'paused_nav', 'paused_recovery',
    'docking', 'charging', 'error_sensor', 'error_motor', 'error_nav',
    # ... every combination explodes
]
# 20 states × 20 states = 400 possible transitions to manage
```

✅ **Correct — use a hierarchical FSM or behaviour tree. Group related states:**
```python
# Top-level FSM: coarse modes
class RobotMode(Enum):
    OFFLINE = auto()
    ONLINE = auto()     # sub-FSM: READY / NAVIGATING / PAUSED
    CHARGING = auto()
    FAULT = auto()

# Sub-FSM only exists when mode == ONLINE
class NavigationState(Enum):
    READY = auto()
    PLANNING = auto()
    EXECUTING = auto()
    RECOVERING = auto()

class HierarchicalFSM(Node):
    def __init__(self):
        super().__init__('hierarchical_fsm')
        self._mode = RobotMode.OFFLINE
        self._nav_state: NavigationState | None = None

    def enter_online(self):
        self._mode = RobotMode.ONLINE
        self._nav_state = NavigationState.READY

    def start_navigation(self, goal):
        if self._mode != RobotMode.ONLINE:
            return
        self._nav_state = NavigationState.PLANNING
        # ... transition logic is scoped to navigation sub-FSM only
```

### Anti-Pattern 6: Blocking Calls Inside Callbacks

❌ **Wrong — long-running work blocks the ROS 2 executor:**
```python
class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner')
        self._goal_sub = self.create_subscription(
            PoseStamped, 'goal_pose', self._goal_cb, 10
        )

    def _goal_cb(self, msg: PoseStamped):
        # WRONG: A* on a large map blocks the thread for 500 ms+
        path = self._run_astar(msg)       # blocks all other callbacks!
        self._path_pub.publish(path)
```

✅ **Correct — offload work to a thread pool; callbacks stay non-blocking:**
```python
import concurrent.futures
from rclpy.callback_groups import ReentrantCallbackGroup

class PathPlannerNode(Node):
    def __init__(self):
        super().__init__('path_planner')
        self._executor_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self._path_pub = self.create_publisher(Path, 'planned_path', 10)

        cb_group = ReentrantCallbackGroup()
        self._goal_sub = self.create_subscription(
            PoseStamped, 'goal_pose', self._goal_cb, 10, callback_group=cb_group
        )

    def _goal_cb(self, msg: PoseStamped):
        # Submit work; callback returns immediately
        self._executor_pool.submit(self._plan_and_publish, msg)

    def _plan_and_publish(self, goal: PoseStamped):
        # Runs in background thread — does not block the executor
        path = self._run_astar(goal)
        self._path_pub.publish(path)

    def destroy_node(self):
        self._executor_pool.shutdown(wait=False)
        super().destroy_node()
```

## Workflow Integration

### Connection Map

```
robot-architecture
       │
       ├──► ros2_node_creation    — use node templates; MutuallyExclusiveCallbackGroup
       │                            for FSM nodes; LifecycleNode for components
       │
       ├──► nav2                  — BT nodes plug into Nav2's BehaviorTree.CPP runtime;
       │                            BehaviorTree.CPP v4 is bundled with Nav2 Jazzy;
       │                            NavigateToPose / NavigateThroughPoses are BT-driven
       │
       ├──► sensor-fusion-slam    — state estimation (EKF, Madgwick) feeds the
       │                            robot_pose blackboard entry consumed by BT
       │                            GoalReached conditions
       │
       ├──► safety-systems        — emergency-stop events trigger FSM 'fault'
       │                            transitions; watchdog timers are
       │                            HealthCheckMixin pattern above
       │
       └──► deployment-fleet      — HealthCheckMixin publishes to /diagnostics;
                                    see the deployment-fleet skill for aggregation
```

### How to Integrate with Nav2 (ROS 2 Jazzy)

```python
# orbibot_bringup/launch/robot.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    nav2_bringup = get_package_share_directory('nav2_bringup')

    return LaunchDescription([
        # 1. FSM node — manages robot modes
        Node(
            package='orbibot_bringup',
            executable='robot_fsm',
            name='robot_fsm',
            output='screen',
        ),

        # 2. Nav2 — uses its own BT internally
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup, 'launch', 'navigation_launch.py')
            ),
            launch_arguments={
                'use_sim_time': 'false',
                'params_file': os.path.join(
                    get_package_share_directory('orbibot_navigation'),
                    'config', 'nav2_params.yaml'
                ),
            }.items(),
        ),

        # 3. Mission executor — uses BT that calls Nav2 actions
        Node(
            package='orbibot_bringup',
            executable='mission_executor',
            name='mission_executor',
            output='screen',
        ),
    ])
```

### How to Integrate with sensor-fusion-slam

The EKF from `robot_localization` publishes `/odometry/filtered`. Feed this into
the BT blackboard via a small bridge node so BT conditions can check pose:

```python
# bt_pose_bridge.py
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped


class BTPoseBridge(Node):
    """Republishes /odometry/filtered as PoseStamped for BT blackboard."""

    def __init__(self):
        super().__init__('bt_pose_bridge')
        self._pose_pub = self.create_publisher(
            PoseStamped, '/orbibot/robot_pose', 10
        )
        self._odom_sub = self.create_subscription(
            Odometry, '/odometry/filtered', self._odom_cb, 10
        )

    def _odom_cb(self, msg: Odometry):
        pose_stamped = PoseStamped()
        pose_stamped.header = msg.header
        pose_stamped.pose = msg.pose.pose
        self._pose_pub.publish(pose_stamped)
```

```xml
<!-- In the BT XML, read robot_pose from topic via a Subtree or port remapping -->
<GoalReached
    goal="{current_goal}"
    robot_pose="{robot_pose}"
    threshold="0.15"/>
```

### How to Integrate with safety-systems

```python
# safety_bridge.py — converts safety events into FSM transitions
from std_msgs.msg import String, Bool


class SafetyBridge(Node):
    """Bridges safety-systems estop signals to FSM event topic."""

    def __init__(self):
        super().__init__('safety_bridge')

        self._fsm_event_pub = self.create_publisher(
            String, '/orbibot/fsm_event', 10
        )
        self._estop_sub = self.create_subscription(
            Bool, '/orbibot/estop', self._estop_cb, 10
        )

    def _estop_cb(self, msg: Bool):
        event = String()
        if msg.data:
            event.data = 'fault'      # triggers FSM → ERROR state
        else:
            event.data = 'reset'      # triggers FSM → IDLE on estop clear
        self._fsm_event_pub.publish(event)
```

### Skill Cross-References

| Task | Primary Skill | Secondary Skill |
|------|--------------|-----------------|
| Implement BT action nodes | **robot-architecture** | `ros2_node_creation` |
| Configure Nav2 BT plugins | **robot-architecture** | `nav2` |
| Set up EKF for pose | `sensor-fusion-slam` | **robot-architecture** |
| Add watchdog / e-stop | `safety-systems` | **robot-architecture** |
| Publish diagnostics | `deployment-fleet` | **robot-architecture** |
| Test FSM transitions | `guides/testing-strategy.md` | **robot-architecture** |
| Wrap in Lifecycle node | `ros2_lifecycle` | **robot-architecture** |

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering behavior trees, FSM, state estimation, multi-robot

### v1.1.0 (2026-03-27)
- Added Common Patterns: hierarchical BT with safety layer, pure-Python FSM, component lifecycle, blackboard data flow, health-check mixin
- Added Anti-Patterns: god node, spaghetti callbacks, tight coupling, missing watchdog, flat FSM state explosion, blocking callbacks
- Added Workflow Integration: nav2, sensor-fusion-slam, safety-systems, deployment-fleet cross-references with working code