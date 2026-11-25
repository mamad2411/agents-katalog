---
name: grasping-force-control
description: Grasp planning, force/torque sensing, impedance/admittance control, and compliant manipulation for robotic picking and assembly.
category: manipulation
tags: [grasping, force-control, impedance, admittance, ft-sensor, manipulation, compliance, assembly]
version: "1.0.0"
---

# Grasping and Force Control

Grasping and force control enable robots to interact physically with objects. This skill covers grasp planning, force/torque sensing, and compliant control strategies.

## When to Use

- Implementing grasp planning for pick-and-place operations
- Configuring force/torque sensors for feedback control
- Implementing impedance or admittance control strategies
- Designing compliant manipulation for assembly tasks
- Handling fragile or deformable objects
- Setting up tactile sensing and feedback
- Implementing slip detection and prevention
- Designing insertion and mating operations
- Configuring safety limits for human-robot collaboration

## Quick Start

```bash
# Install force control packages
sudo apt install ros-humble-ros2-control ros-humble-force-torque-sensor-broadcaster

# Install MoveIt grasping
sudo apt install ros-humble-moveit-resources ros-humble-moveit-servo

# Launch force-controlled manipulation demo
ros2 launch moveit_servo demo_joint_jog.launch.py
```

## Core Concepts

### 1. Grasp Planning Fundamentals

Grasp quality depends on contact geometry, force distribution, and stability.

**Grasp taxonomy:**

| Grasp Type | Description | Example |
|------------|-------------|---------|
| Pinch | Two-finger precision grip | Picking small parts |
| Cylindrical | Wrap-around power grip | Holding tools |
| Spherical | Fingers opposing palm | Holding balls |
| Hook | Finger-only support | Carrying bags |
| Lumbrical | Fingers only, no palm | Precision tasks |

**Grasp quality metrics:**

```python
import numpy as np

def compute_grasp_wrench_space(contacts, normals, mu):
    """
    Compute grasp wrench space (GWS) for force closure analysis.
    
    Args:
        contacts: Nx3 array of contact points
        normals: Nx3 array of contact normals (inward)
        mu: friction coefficient
    
    Returns:
        force_closure: bool indicating force closure
        min_wrench: minimum wrench magnitude
    """
    n_contacts = len(contacts)
    
    # Build friction cone edges (4 edges per contact)
    edges = []
    for i in range(n_contacts):
        p = contacts[i]
        n = normals[i]
        
        # Find tangent vectors
        if abs(n[2]) < 0.9:
            t1 = np.cross(n, [0, 0, 1])
        else:
            t1 = np.cross(n, [0, 1, 0])
        t1 = t1 / np.linalg.norm(t1)
        t2 = np.cross(n, t1)
        
        # Friction cone edges
        for angle in [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]:
            f = n + mu * (np.cos(angle) * t1 + np.sin(angle) * t2)
            f = f / np.linalg.norm(f)
            
            # Wrench: [force; torque = r x f]
            torque = np.cross(p, f)
            wrench = np.concatenate([f, torque])
            edges.append(wrench)
    
    edges = np.array(edges)
    
    # Check if origin is inside convex hull
    from scipy.spatial import ConvexHull
    try:
        hull = ConvexHull(edges)
        # Check if origin is inside
        equations = hull.equations
        inside = all(np.dot(eq[:6], np.zeros(6)) + eq[6] <= 1e-6 for eq in equations)
        return inside, np.min(np.linalg.norm(edges, axis=1))
    except:
        return False, 0.0
```

**Antipodal grasp detection:**

```python
def find_antipodal_grasps(point_cloud, normals, max_angle=20*np.pi/180):
    """
    Find antipodal grasp pairs in point cloud.
    
    Args:
        point_cloud: Nx3 array of points
        normals: Nx3 array of outward normals
        max_angle: maximum angle deviation from antipodal (rad)
    
    Returns:
        grasp_pairs: list of (point1, point2, quality) tuples
    """
    grasp_pairs = []
    n_points = len(point_cloud)
    
    for i in range(n_points):
        for j in range(i+1, n_points):
            p1, p2 = point_cloud[i], point_cloud[j]
            n1, n2 = normals[i], normals[j]
            
            # Vector between contact points
            d = p2 - p1
            d_norm = d / (np.linalg.norm(d) + 1e-6)
            
            # Check antipodal condition: normals oppose each other
            # and align with contact vector
            align1 = np.dot(n1, d_norm)
            align2 = np.dot(n2, -d_norm)
            
            if align1 > np.cos(max_angle) and align2 > np.cos(max_angle):
                # Compute quality (friction coefficient needed)
                quality = min(align1, align2)
                grasp_pairs.append((i, j, quality))
    
    # Sort by quality
    grasp_pairs.sort(key=lambda x: x[2], reverse=True)
    return grasp_pairs
```

### 2. Force/Torque Sensing

F/T sensors measure contact forces and torques at the wrist or joints.

**ATI Nano25 configuration:**

```yaml
# config/ft_sensor.yaml
ft_sensor_broadcaster:
  ros__parameters:
    sensor_name: wrist_ft_sensor
    frame_id: wrist_ft_link
    
    # Calibration matrix (6x6)
    # Converts raw voltages to forces/torques
    calibration_matrix:
      - [0.123, 0.234, 0.345, 0.456, 0.567, 0.678]
      - [0.234, 0.345, 0.456, 0.567, 0.678, 0.789]
      - [0.345, 0.456, 0.567, 0.678, 0.789, 0.890]
      - [0.456, 0.567, 0.678, 0.789, 0.890, 0.901]
      - [0.567, 0.678, 0.789, 0.890, 0.901, 0.012]
      - [0.678, 0.789, 0.890, 0.901, 0.012, 0.123]
    
    # Bias/offset compensation
    bias_forces: [0.0, 0.0, 0.0]
    bias_torques: [0.0, 0.0, 0.0]
    
    # Filter settings
    filter_type: low_pass  # none, low_pass, moving_average
    filter_coefficient: 0.1
```

**ROS2 force-torque sensor broadcaster:**

```cpp
#include <force_torque_sensor_broadcaster/force_torque_sensor_broadcaster.hpp>
#include <controller_interface/controller_interface.hpp>

class FTSensorBroadcaster : public controller_interface::ControllerInterface {
public:
    controller_interface::CallbackReturn on_init() override {
        try {
            auto_declare<std::string>("sensor_name", "ft_sensor");
            auto_declare<std::string>("frame_id", "wrist_ft_link");
        } catch (const std::exception& e) {
            fprintf(stderr, "Exception in FTSensorBroadcaster::on_init: %s\n", e.what());
            return controller_interface::CallbackReturn::ERROR;
        }
        return controller_interface::CallbackReturn::SUCCESS;
    }

    controller_interface::InterfaceConfiguration command_interface_configuration() const override {
        return controller_interface::InterfaceConfiguration{
            controller_interface::interface_configuration_type::NONE};
    }

    controller_interface::InterfaceConfiguration state_interface_configuration() const override {
        controller_interface::InterfaceConfiguration config;
        config.type = controller_interface::interface_configuration_type::INDIVIDUAL;
        
        const std::string sensor_name = get_node()->get_parameter("sensor_name").as_string();
        config.names = {
            sensor_name + "/force.x",
            sensor_name + "/force.y",
            sensor_name + "/force.z",
            sensor_name + "/torque.x",
            sensor_name + "/torque.y",
            sensor_name + "/torque.z",
        };
        return config;
    }

    controller_interface::return_type update(const rclcpp::Time& time,
                                             const rclcpp::Duration& period) override {
        // Publish Wrench message
        geometry_msgs::msg::WrenchStamped wrench_msg;
        wrench_msg.header.stamp = time;
        wrench_msg.header.frame_id = frame_id_;
        
        wrench_msg.wrench.force.x = state_interfaces_[0].get_value();
        wrench_msg.wrench.force.y = state_interfaces_[1].get_value();
        wrench_msg.wrench.force.z = state_interfaces_[2].get_value();
        wrench_msg.wrench.torque.x = state_interfaces_[3].get_value();
        wrench_msg.wrench.torque.y = state_interfaces_[4].get_value();
        wrench_msg.wrench.torque.z = state_interfaces_[5].get_value();
        
        ft_publisher_->publish(wrench_msg);
        return controller_interface::return_type::OK;
    }

private:
    std::string frame_id_;
    rclcpp::Publisher<geometry_msgs::msg::WrenchStamped>::SharedPtr ft_publisher_;
};
```

**Force/torque sensor filtering:**

```python
import numpy as np
from collections import deque

class FTSensorFilter:
    def __init__(self, filter_type='low_pass', coefficient=0.1, window_size=10):
        self.filter_type = filter_type
        self.coefficient = coefficient
        self.window_size = window_size
        
        self.prev_value = None
        self.buffer = deque(maxlen=window_size)
    
    def filter(self, value):
        if self.filter_type == 'none':
            return value
        
        elif self.filter_type == 'low_pass':
            if self.prev_value is None:
                self.prev_value = value
                return value
            
            filtered = self.coefficient * value + (1 - self.coefficient) * self.prev_value
            self.prev_value = filtered
            return filtered
        
        elif self.filter_type == 'moving_average':
            self.buffer.append(value)
            return np.mean(self.buffer, axis=0)
        
        elif self.filter_type == 'median':
            self.buffer.append(value)
            return np.median(self.buffer, axis=0)
        
        elif self.filter_type == 'kalman':
            # Simplified Kalman filter
            if self.prev_value is None:
                self.prev_value = value
                self.error_estimate = 1.0
                return value
            
            # Prediction
            prediction = self.prev_value
            error_prediction = self.error_estimate + 0.01  # Process noise
            
            # Update
            kalman_gain = error_prediction / (error_prediction + 0.1)  # Measurement noise
            filtered = prediction + kalman_gain * (value - prediction)
            self.error_estimate = (1 - kalman_gain) * error_prediction
            
            self.prev_value = filtered
            return filtered
        
        return value
    
    def reset(self):
        self.prev_value = None
        self.buffer.clear()
```

### 3. Impedance Control

Impedance control regulates the dynamic relationship between force and position.

**Cartesian impedance control:**

```cpp
#include <Eigen/Dense>

class CartesianImpedanceController {
public:
    CartesianImpedanceController() {
        // Stiffness matrix (6x6 diagonal)
        K_ = Eigen::MatrixXd::Zero(6, 6);
        K_.diagonal() << 1000, 1000, 1000, 50, 50, 50;  // N/m, Nm/rad
        
        // Damping matrix (6x6 diagonal)
        D_ = Eigen::MatrixXd::Zero(6, 6);
        D_.diagonal() << 50, 50, 50, 2, 2, 2;  // Ns/m, Nms/rad
        
        // Inertia matrix (virtual)
        M_ = Eigen::MatrixXd::Zero(6, 6);
        M_.diagonal() << 10, 10, 10, 1, 1, 1;  // kg, kg*m^2
    }
    
    Eigen::VectorXd computeControl(
        const Eigen::VectorXd& x,      // Current pose (6D: x,y,z,roll,pitch,yaw)
        const Eigen::VectorXd& x_dot,  // Current velocity
        const Eigen::VectorXd& x_d,    // Desired pose
        const Eigen::VectorXd& f_ext   // External force/torque
    ) {
        // Pose error
        Eigen::VectorXd x_tilde = x_d - x;
        
        // Impedance dynamics: M*x_dd + D*x_d + K*x = f_ext
        // Compute desired acceleration
        Eigen::VectorXd x_dd = M_.inverse() * (f_ext - D_ * x_dot - K_ * x_tilde);
        
        // Integrate to get desired velocity and position
        Eigen::VectorXd x_dot_d = x_dot + x_dd * dt_;
        Eigen::VectorXd x_d_new = x + x_dot_d * dt_;
        
        // Convert to joint commands via inverse kinematics
        return x_d_new;
    }
    
    void setStiffness(const Eigen::Vector6d& stiffness) {
        K_.diagonal() = stiffness;
        
        // Update damping for critical damping: D = 2*sqrt(M*K)
        for (int i = 0; i < 6; ++i) {
            D_(i, i) = 2.0 * std::sqrt(M_(i, i) * K_(i, i));
        }
    }
    
    void setCompliance(double linear_stiffness, double angular_stiffness) {
        K_.diagonal() << linear_stiffness, linear_stiffness, linear_stiffness,
                        angular_stiffness, angular_stiffness, angular_stiffness;
        
        // Critical damping
        for (int i = 0; i < 6; ++i) {
            D_(i, i) = 2.0 * std::sqrt(M_(i, i) * K_(i, i));
        }
    }

private:
    Eigen::MatrixXd K_;  // Stiffness
    Eigen::MatrixXd D_;  // Damping
    Eigen::MatrixXd M_;  // Inertia
    double dt_ = 0.001;  // 1kHz control rate
};
```

**Stiffness selection guide:**

| Task | Linear Stiffness (N/m) | Angular Stiffness (Nm/rad) |
|------|----------------------|---------------------------|
| Free motion | 0-50 | 0-5 |
| Compliant contact | 100-500 | 10-50 |
| Light assembly | 500-1000 | 50-100 |
| Heavy manipulation | 2000-5000 | 200-500 |
| Rigid positioning | 10000+ | 1000+ |

### 4. Admittance Control

Admittance control generates motion in response to measured forces.

```cpp
class AdmittanceController {
public:
    AdmittanceController() {
        // Admittance parameters
        M_adm_ = Eigen::MatrixXd::Zero(6, 6);
        M_adm_.diagonal() << 10, 10, 10, 0.5, 0.5, 0.5;
        
        D_adm_ = Eigen::MatrixXd::Zero(6, 6);
        D_adm_.diagonal() << 100, 100, 100, 5, 5, 5;
        
        K_adm_ = Eigen::MatrixXd::Zero(6, 6);
        K_adm_.diagonal() << 1000, 1000, 1000, 100, 100, 100;
    }
    
    Eigen::VectorXd update(
        const Eigen::VectorXd& f_ext,        // Measured force
        const Eigen::VectorXd& x_d,          // Desired position
        const Eigen::VectorXd& x_dot_d,      // Desired velocity
        double dt
    ) {
        // Admittance dynamics: M*x_dd + D*x_d + K*(x-x_d) = f_ext
        // Solve for acceleration
        Eigen::VectorXd x_tilde = x_ - x_d;
        Eigen::VectorXd x_dot_tilde = x_dot_ - x_dot_d;
        
        Eigen::VectorXd x_dd = M_adm_.inverse() * 
            (f_ext - D_adm_ * x_dot_tilde - K_adm_ * x_tilde);
        
        // Integrate
        x_dot_ += x_dd * dt;
        x_ += x_dot_ * dt;
        
        return x_;
    }
    
    void reset(const Eigen::VectorXd& x0) {
        x_ = x0;
        x_dot_ = Eigen::VectorXd::Zero(6);
    }

private:
    Eigen::MatrixXd M_adm_, D_adm_, K_adm_;
    Eigen::VectorXd x_{Eigen::VectorXd::Zero(6)};
    Eigen::VectorXd x_dot_{Eigen::VectorXd::Zero(6)};
};
```

### 5. Grasp Force Control

Control gripper force for stable grasping without crushing.

```python
import numpy as np

class GraspForceController:
    def __init__(self, max_force=50.0, slip_threshold=0.5):
        self.max_force = max_force
        self.slip_threshold = slip_threshold
        self.force_pid = PIDController(kp=0.1, ki=0.01, kd=0.001)
        self.current_force = 0.0
        
    def update(self, target_force, measured_force, slip_detected=False):
        """
        Update gripper force command.
        
        Args:
            target_force: desired grasp force (N)
            measured_force: current measured force (N)
            slip_detected: whether slip is detected
        
        Returns:
            gripper_position_cmd: position command (0=open, 1=close)
        """
        # Increase force if slipping
        if slip_detected:
            target_force = min(target_force * 1.5, self.max_force)
            self.force_pid.reset()
        
        # PID control
        force_error = target_force - measured_force
        force_cmd = self.force_pid.update(force_error)
        
        # Convert force to position (simplified gripper model)
        # position = 0.5 + force * compliance
        gripper_position = 0.5 - force_cmd * 0.01
        
        # Clamp
        gripper_position = np.clip(gripper_position, 0.0, 1.0)
        
        return gripper_position
    
    def compute_target_force(self, object_weight, friction_coef, safety_factor=2.0):
        """
        Compute minimum grasp force for stable grasp.
        
        F_grasp >= safety_factor * weight / (2 * friction_coef)
        """
        return safety_factor * object_weight / (2.0 * friction_coef)

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = 0.0
        
    def update(self, error):
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        
        return self.kp * error + self.ki * self.integral + self.kd * derivative
    
    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0
```

## Common Patterns

### Pattern 1: Peg-in-Hole Assembly

```cpp
class PegInHoleController {
public:
    enum class Phase { APPROACH, SEARCH, INSERT, COMPLETE };
    
    PegInHoleController() : phase_(Phase::APPROACH) {
        // Search parameters
        search_amplitude_ = 0.002;  // 2mm spiral
        search_frequency_ = 2 * M_PI;  // 1 Hz
        
        // Insertion parameters
        insert_force_ = 10.0;  // N
        insert_speed_ = 0.001;  // m/s
        
        // Stiffness for search phase (compliant)
        K_search_ << 100, 100, 50, 10, 10, 10;
        
        // Stiffness for insertion (stiffer)
        K_insert_ << 500, 500, 100, 50, 50, 50;
    }
    
    Eigen::Vector6d computeCommand(
        const Eigen::Vector6d& pose,
        const Eigen::Vector6d& f_ext,
        double time
    ) {
        Eigen::Vector6d cmd;
        
        switch (phase_) {
            case Phase::APPROACH:
                cmd = approachPhase(pose, f_ext);
                if (contactDetected(f_ext)) {
                    phase_ = Phase::SEARCH;
                    search_start_time_ = time;
                }
                break;
                
            case Phase::SEARCH:
                cmd = searchPhase(pose, f_ext, time - search_start_time_);
                if (holeFound(f_ext)) {
                    phase_ = Phase::INSERT;
                }
                break;
                
            case Phase::INSERT:
                cmd = insertPhase(pose, f_ext);
                if (insertionComplete(f_ext)) {
                    phase_ = Phase::COMPLETE;
                }
                break;
                
            case Phase::COMPLETE:
                cmd = pose;  // Hold position
                break;
        }
        
        return cmd;
    }

private:
    Eigen::Vector6d approachPhase(const Eigen::Vector6d& pose, 
                                   const Eigen::Vector6d& f_ext) {
        // Move down until contact
        Eigen::Vector6d target = pose;
        target[2] -= 0.0001;  // Small downward step
        return target;
    }
    
    Eigen::Vector6d searchPhase(const Eigen::Vector6d& pose,
                                 const Eigen::Vector6d& f_ext,
                                 double search_time) {
        // Spiral search pattern
        double theta = search_frequency_ * search_time;
        double r = search_amplitude_ * theta / (2 * M_PI);
        
        Eigen::Vector6d target = pose;
        target[0] += r * cos(theta);  // X
        target[1] += r * sin(theta);  // Y
        target[2] -= 0.00005;  // Slowly move down
        
        return target;
    }
    
    Eigen::Vector6d insertPhase(const Eigen::Vector6d& pose,
                                 const Eigen::Vector6d& f_ext) {
        // Compliant insertion with force control
        Eigen::Vector6d target = pose;
        
        // Z direction: constant velocity with force limit
        if (f_ext[2] < insert_force_) {
            target[2] -= insert_speed_ * 0.001;  // Continue insertion
        }
        
        // XY: compliance to center in hole
        target[0] += f_ext[0] * 0.0001;  // Move with force
        target[1] += f_ext[1] * 0.0001;
        
        return target;
    }
    
    bool contactDetected(const Eigen::Vector6d& f_ext) {
        return f_ext[2] > 2.0;  // 2N contact force
    }
    
    bool holeFound(const Eigen::Vector6d& f_ext) {
        // Hole found when lateral forces drop
        return std::sqrt(f_ext[0]*f_ext[0] + f_ext[1]*f_ext[1]) < 1.0;
    }
    
    bool insertionComplete(const Eigen::Vector6d& f_ext) {
        // Complete when bottom contact detected
        return f_ext[2] > insert_force_ * 1.5;
    }
    
    Phase phase_;
    double search_amplitude_, search_frequency_, search_start_time_;
    double insert_force_, insert_speed_;
    Eigen::Vector6d K_search_, K_insert_;
};
```

### Pattern 2: Slip Detection and Prevention

```python
import numpy as np
from collections import deque

class SlipDetector:
    def __init__(self, window_size=10, threshold=0.5):
        self.window_size = window_size
        self.threshold = threshold
        
        self.force_history = deque(maxlen=window_size)
        self.torque_history = deque(maxlen=window_size)
        self.velocity_history = deque(maxlen=window_size)
        
        self.slip_detected = False
        
    def update(self, force, torque, gripper_velocity):
        """
        Detect slip using tangential force and velocity cues.
        
        Args:
            force: 3D force vector (N)
            torque: 3D torque vector (Nm)
            gripper_velocity: gripper closing velocity (m/s)
        """
        self.force_history.append(force)
        self.torque_history.append(torque)
        self.velocity_history.append(gripper_velocity)
        
        if len(self.force_history) < self.window_size:
            return False
        
        # Compute tangential force (friction direction)
        normal_force = abs(force[2])  # Assumes Z is normal
        tangential_force = np.sqrt(force[0]**2 + force[1]**2)
        
        # Criterion 1: Tangential force approaching friction limit
        if normal_force > 1.0:  # Minimum normal force
            friction_ratio = tangential_force / (0.5 * normal_force)  # mu=0.5
            criterion1 = friction_ratio > 0.8
        else:
            criterion1 = False
        
        # Criterion 2: Velocity increase with decreasing force
        force_trend = np.mean(list(self.force_history)[-5:]) - \
                     np.mean(list(self.force_history)[:5])
        velocity_trend = np.mean(list(self.velocity_history)[-5:]) - \
                        np.mean(list(self.velocity_history)[:5])
        
        criterion2 = force_trend < -0.5 and velocity_trend > 0
        
        # Criterion 3: Torque variation indicating rotation
        torque_std = np.std(list(self.torque_history), axis=0)
        criterion3 = np.any(torque_std > 0.1)
        
        self.slip_detected = criterion1 or criterion2 or criterion3
        return self.slip_detected
    
    def get_slip_direction(self):
        """Estimate slip direction from force history."""
        if len(self.force_history) < 2:
            return np.array([0, 0, 0])
        
        recent = np.mean(list(self.force_history)[-3:], axis=0)
        previous = np.mean(list(self.force_history)[:3], axis=0)
        
        slip_dir = recent - previous
        slip_dir[2] = 0  # Ignore normal direction
        
        norm = np.linalg.norm(slip_dir)
        if norm > 0.01:
            return slip_dir / norm
        return np.array([0, 0, 0])
```

### Pattern 3: Force-Guided Insertion

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import WrenchStamped, PoseStamped
from std_msgs.msg import Float64

class ForceGuidedInsertion(Node):
    def __init__(self):
        super().__init__('force_guided_insertion')
        
        # Subscribers
        self.ft_sub = self.create_subscription(
            WrenchStamped, '/ft_sensor/wrench', self.ft_callback, 10)
        self.pose_sub = self.create_subscription(
            PoseStamped, '/current_pose', self.pose_callback, 10)
        
        # Publisher
        self.cmd_pub = self.create_publisher(
            PoseStamped, '/target_pose', 10)
        
        # State
        self.current_force = None
        self.current_pose = None
        self.phase = 'approach'
        
        # Parameters
        self.declare_parameters(namespace='', parameters=[
            ('insertion_force', 10.0),
            ('search_force', 5.0),
            ('compliance_xy', 0.0001),  # m/N
            ('insertion_speed', 0.001),  # m/s
        ])
        
        self.timer = self.create_timer(0.01, self.control_loop)  # 100Hz
        
    def ft_callback(self, msg):
        self.current_force = msg.wrench
        
    def pose_callback(self, msg):
        self.current_pose = msg
    
    def control_loop(self):
        if self.current_force is None or self.current_pose is None:
            return
        
        # Extract parameters
        insertion_force = self.get_parameter('insertion_force').value
        compliance_xy = self.get_parameter('compliance_xy').value
        insertion_speed = self.get_parameter('insertion_speed').value
        
        # Current force
        fx = self.current_force.force.x
        fy = self.current_force.force.y
        fz = self.current_force.force.z
        
        # Generate command
        cmd = PoseStamped()
        cmd.header = self.current_pose.header
        cmd.pose = self.current_pose.pose
        
        if self.phase == 'approach':
            # Move down until contact
            cmd.pose.position.z -= insertion_speed
            
            if fz > 2.0:  # Contact detected
                self.phase = 'search'
                self.get_logger().info('Contact detected, starting search')
                
        elif self.phase == 'search':
            # Compliant search for hole
            cmd.pose.position.x += fx * compliance_xy
            cmd.pose.position.y += fy * compliance_xy
            cmd.pose.position.z -= insertion_speed * 0.5
            
            # Check if lateral forces drop (hole found)
            lateral_force = (fx**2 + fy**2)**0.5
            if lateral_force < 1.0 and fz > 3.0:
                self.phase = 'insert'
                self.get_logger().info('Hole found, inserting')
                
        elif self.phase == 'insert':
            # Insert with force control
            if fz < insertion_force:
                cmd.pose.position.z -= insertion_speed
            
            # Maintain centering
            cmd.pose.position.x += fx * compliance_xy
            cmd.pose.position.y += fy * compliance_xy
            
            # Check completion
            if fz > insertion_force * 1.2:
                self.phase = 'complete'
                self.get_logger().info('Insertion complete')
                
        elif self.phase == 'complete':
            # Hold position
            pass
        
        self.cmd_pub.publish(cmd)

def main():
    rclpy.init()
    node = ForceGuidedInsertion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Anti-Patterns

### ❌ High stiffness during contact
Using position control with high stiffness during contact causes force spikes.

**What happens:** Robot bounces, force oscillations, potential damage.

### ✅ Switch to compliance on contact
```cpp
// Monitor force and switch mode
if (force > contact_threshold) {
    controller.setStiffness(low_stiffness);  // Compliant
} else {
    controller.setStiffness(high_stiffness);  // Rigid
}
```

### ❌ Ignoring force sensor noise
Using raw force data without filtering causes control jitter.

**What happens:** Noisy force readings propagate to velocity commands, vibration.

### ✅ Filter and differentiate carefully
```python
# Filter force
filtered_force = low_pass_filter(raw_force, cutoff=10)  # Hz

# Estimate derivative with care
force_derivative = (filtered_force - prev_force) / dt
force_derivative = np.clip(force_derivative, -max_dforce, max_dforce)
```

### ❌ Fixed grasp force
Using constant grasp force regardless of object.

**What happens:** Crushes fragile objects, drops heavy objects.

### ✅ Adaptive grasp force
```python
# Estimate object properties from contact
if contact_detected:
    # Increase force gradually until stable
    grasp_force += delta_force
    if slip_detected():
        grasp_force *= 1.2  # Increase
    else:
        grasp_force *= 0.95  # Decrease slightly
```

### ❌ No force limiting
Not limiting commanded forces in software.

**What happens:** Hardware damage on collision or malfunction.

### ✅ Multiple safety layers
```cpp
// Software limits
if (commanded_force > max_force) {
    commanded_force = max_force;
    trigger_safety_stop();
}

// Hardware limits (independent)
hardware_force_limit = 100.0;  // N
```

## Configuration Reference

### Force Control Parameters

| Parameter | Typical Range | Description |
|-----------|--------------|-------------|
| Stiffness (linear) | 100-10000 N/m | Position control gain |
| Stiffness (angular) | 10-1000 Nm/rad | Orientation control gain |
| Damping ratio | 0.5-1.0 | Critical damping target |
| Force limit | 10-100 N | Maximum contact force |
| Torque limit | 1-10 Nm | Maximum contact torque |
| Filter cutoff | 10-100 Hz | Force sensor filtering |

### Grasp Force Guidelines

| Object Type | Grasp Force (N) | Safety Factor |
|-------------|----------------|---------------|
| Fragile (glass, eggs) | 2-5 | 3-5 |
| Light (paper, foam) | 5-10 | 2-3 |
| Standard (boxes, tools) | 10-30 | 2 |
| Heavy (metal parts) | 30-100 | 1.5-2 |
| Unknown | Start low, adapt | 3 |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Force oscillations | Too high stiffness or low damping | Reduce stiffness, increase damping |
| Slow response | Excessive filtering | Reduce filter cutoff, check latency |
| Drift during contact | Poor force sensor calibration | Recalibrate sensor, check bias |
| Grasp drops object | Insufficient force or slip | Increase force, add slip detection |
| Crushes object | Excessive grasp force | Implement adaptive force control |
| Insertion fails | Misalignment or wrong compliance | Increase search amplitude, reduce stiffness |
| Robot vibrates | Controller instability | Check loop rate, reduce gains |
| Force readings drift | Temperature effects | Add temperature compensation |

## Workflow Integration

- **Before this:** Use `moveit2` for collision-free approach motions
- **With this:** Use `ros2-control` for force controller implementation
- **After this:** Use `safety-systems` for collaborative robot safety limits
- **Related:** Use `control-systems` for underlying control theory

## Further Reading

- "Force Control" by D. E. Whitney
- "Grasping and Manipulation" by A. Bicchi
- [ROS2 Control Documentation](https://control.ros.org/)
- Related skills: `moveit2`, `ros2-control`, `control-systems`, `safety-systems`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering grasping and force control
- Includes impedance/admittance control, slip detection, assembly