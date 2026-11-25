---
name: control-systems
description: Control theory for robotics including PID, LQR, MPC, state-space representation, system identification, trajectory generation, and splines. Use when designing robot controllers or analyzing dynamic systems.
category: control
tags: [control-theory, pid, lqr, mpc, state-space, trajectory, dynamics]
version: "1.0.0"
---

# Control Systems

Control theory is the mathematical foundation for robot motion and stability. This skill covers classical control (PID), modern control (LQR, state-space), and optimal control (MPC) for robotic systems.

## When to Use

- Tuning PID controllers for motors and joints
- Designing LQR controllers for optimal performance
- Implementing MPC for constrained systems
- Performing system identification on hardware
- Generating smooth trajectories (splines, Bezier)
- Analyzing stability of control loops
- Implementing feedforward control
- Tuning cascaded control architectures

## Quick Start

```bash
# Python control library
pip install control

# Optimization for MPC
pip install cvxpy casadi

# SciPy for signal processing
pip install scipy numpy
```

**Simple PID Controller:**
```python
import numpy as np

class PIDController:
    """Discrete PID controller."""
    
    def __init__(self, Kp, Ki, Kd, dt, output_limit=None):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.output_limit = output_limit
        
        self.integral = 0
        self.prev_error = 0
        self.prev_measurement = 0
        
    def reset(self):
        """Reset controller state."""
        self.integral = 0
        self.prev_error = 0
        self.prev_measurement = 0
        
    def update(self, setpoint, measurement):
        """Update controller."""
        error = setpoint - measurement
        
        # Proportional
        P = self.Kp * error
        
        # Integral (with anti-windup)
        self.integral += error * self.dt
        if self.output_limit:
            self.integral = np.clip(self.integral, 
                                    -self.output_limit / self.Ki,
                                    self.output_limit / self.Ki)
        I = self.Ki * self.integral
        
        # Derivative (on measurement to avoid derivative kick)
        d_measurement = (measurement - self.prev_measurement) / self.dt
        D = -self.Kd * d_measurement
        
        # Output
        output = P + I + D
        
        if self.output_limit:
            output = np.clip(output, -self.output_limit, self.output_limit)
        
        # Store for next iteration
        self.prev_error = error
        self.prev_measurement = measurement
        
        return output
```

## Core Concepts

### 1. PID Control

**Standard Form vs. Parallel Form:**

| Form | Equation | Use Case |
|------|----------|----------|
| Standard | $K_p(e + \frac{1}{T_i}\int e + T_d \frac{de}{dt})$ | Tuning, industrial |
| Parallel | $K_p e + K_i \int e + K_d \frac{de}{dt}$ | Implementation |

**Tuning Methods:**

```python
def tune_pid(method='ziegler_nichols', Ku=None, Tu=None):
    """
    Tune PID using various methods.
    
    Ziegler-Nichols: Requires ultimate gain (Ku) and period (Tu)
    from relay feedback test.
    """
    if method == 'ziegler_nichols':
        # Classic Ziegler-Nichols
        Kp = 0.6 * Ku
        Ki = Kp / (0.5 * Tu)
        Kd = Kp * 0.125 * Tu
        
    elif method == 'no_overshoot':
        # Aggressive, no overshoot
        Kp = 0.2 * Ku
        Ki = Kp / (0.5 * Tu)
        Kd = Kp * 0.33 * Tu
        
    elif method == 'pessen_integral':
        # Pessen Integral Rule
        Kp = 0.7 * Ku
        Ki = Kp / (0.4 * Tu)
        Kd = Kp * 0.15 * Tu
        
    return Kp, Ki, Kd
```

**Anti-Windup Strategies:**

```python
class PIDWithAntiWindup(PIDController):
    """PID with back-calculation anti-windup."""
    
    def __init__(self, Kp, Ki, Kd, dt, output_limit, Tt=None):
        super().__init__(Kp, Ki, Kd, dt, output_limit)
        # Tracking time constant
        self.Tt = Tt if Tt is not None else np.sqrt(Kd / Ki) if Ki > 0 else 0.1
        
    def update(self, setpoint, measurement):
        error = setpoint - measurement
        
        # Compute "ideal" output
        P = self.Kp * error
        I = self.Ki * self.integral
        d_error = (error - self.prev_error) / self.dt
        D = self.Kd * d_error
        
        v = P + I + D
        
        # Saturate output
        u = np.clip(v, -self.output_limit, self.output_limit)
        
        # Back-calculate integral to prevent windup
        self.integral += (error + (u - v) / self.Tt) * self.dt
        
        self.prev_error = error
        return u
```

**Derivative Filter:**

```python
class PIDWithFilter(PIDController):
    """PID with filtered derivative."""
    
    def __init__(self, Kp, Ki, Kd, dt, N=10, **kwargs):
        """
        N: derivative filter coefficient (higher = less filtering)
        Typical: 5-20
        """
        super().__init__(Kp, Ki, Kd, dt, **kwargs)
        self.N = N
        self.D_component = 0
        
    def update(self, setpoint, measurement):
        error = setpoint - measurement
        
        # Proportional
        P = self.Kp * error
        
        # Integral
        self.integral += error * self.dt
        I = self.Ki * self.integral
        
        # Filtered derivative
        # D_k = N*Kd*(e_k - e_{k-1})/dt + (1 - N*dt)*D_{k-1}
        alpha = self.N * self.dt
        self.D_component = (alpha * self.Kd * (error - self.prev_error) / self.dt 
                           + (1 - alpha) * self.D_component)
        D = self.D_component
        
        self.prev_error = error
        
        return P + I + D
```

### 2. State-Space Control

**State-Space Representation:**

```python
import numpy as np
from scipy.linalg import solve_continuous_are, solve_discrete_are

class StateSpaceController:
    """Linear state-space controller."""
    
    def __init__(self, A, B, C, D=None, dt=None):
        """
        Continuous: dx/dt = Ax + Bu, y = Cx + Du
        Discrete: x[k+1] = Ax[k] + Bu[k], y[k] = Cx[k] + Du[k]
        """
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)
        self.D = np.zeros((C.shape[0], B.shape[1])) if D is None else np.array(D)
        self.dt = dt
        
        self.n_states = A.shape[0]
        self.n_inputs = B.shape[1]
        self.n_outputs = C.shape[0]
        
        self.x = np.zeros(self.n_states)
        
    def update(self, u):
        """Update state with input u."""
        if self.dt is None:
            # Continuous - use simple Euler (for small dt)
            dx = self.A @ self.x + self.B @ np.atleast_1d(u)
            self.x += dx * 0.001  # Assuming small dt
        else:
            # Discrete
            self.x = self.A @ self.x + self.B @ np.atleast_1d(u)
        
        y = self.C @ self.x + self.D @ np.atleast_1d(u)
        return y
    
    def get_output(self):
        """Get current output."""
        return self.C @ self.x
    
    def set_state(self, x):
        """Set state (for observer)."""
        self.x = np.array(x)
```

**Linear Quadratic Regulator (LQR):**

```python
class LQRController:
    """LQR optimal controller."""
    
    def __init__(self, A, B, Q, R, dt=None):
        """
        Minimize J = integral(x'Qx + u'Ru)dt
        """
        self.A = np.array(A)
        self.B = np.array(B)
        self.Q = np.array(Q)
        self.R = np.array(R)
        self.dt = dt
        
        # Solve Riccati equation
        if dt is None:
            # Continuous LQR
            P = solve_continuous_are(A, B, Q, R)
            self.K = np.linalg.inv(R) @ B.T @ P
        else:
            # Discrete LQR
            P = solve_discrete_are(A, B, Q, R)
            self.K = np.linalg.inv(R + B.T @ P @ B) @ B.T @ P @ A
        
        self.x = np.zeros(A.shape[0])
        
    def compute_control(self, x, x_desired=None):
        """Compute optimal control."""
        if x_desired is None:
            x_desired = np.zeros_like(x)
        
        error = x - x_desired
        u = -self.K @ error
        return u
    
    def get_gain(self):
        """Return LQR gain matrix."""
        return self.K
```

**Pole Placement:**

```python
from scipy.signal import place_poles

def place_controller_poles(A, B, desired_poles):
    """
    Place closed-loop poles at desired locations.
    
    desired_poles: Array of desired pole locations
                   (must be complex conjugate pairs for real systems)
    """
    result = place_poles(A, B, desired_poles)
    K = result.gain_matrix
    
    return K, result.computed_poles
```

### 3. Trajectory Generation

**Cubic Spline Interpolation:**

```python
from scipy.interpolate import CubicSpline

def generate_cubic_trajectory(waypoints, times):
    """
    Generate smooth trajectory through waypoints.
    
    waypoints: NxM array (N points, M dimensions)
    times: N array of time points
    """
    cs = CubicSpline(times, waypoints, bc_type='clamped')
    
    def evaluate(t):
        pos = cs(t)
        vel = cs(t, 1)
        acc = cs(t, 2)
        return pos, vel, acc
    
    return evaluate
```

**Minimum Jerk Trajectory:**

```python
class MinimumJerkTrajectory:
    """
    5th-order polynomial minimizing integral of jerk squared.
    """
    
    def __init__(self, start, end, duration):
        self.start = np.array(start)
        self.end = np.array(end)
        self.T = duration
        
        # Compute coefficients for each dimension
        self.coeffs = self._compute_coeffs()
        
    def _compute_coeffs(self):
        """Compute polynomial coefficients."""
        # Boundary conditions: pos, vel, acc at t=0 and t=T
        # For minimum jerk: start/end vel and acc are zero
        
        T = self.T
        T2, T3, T4, T5 = T**2, T**3, T**4, T**5
        
        coeffs = []
        for i in range(len(self.start)):
            # System matrix for boundary conditions
            M = np.array([
                [1, 0, 0, 0, 0, 0],      # p(0) = start
                [0, 1, 0, 0, 0, 0],      # v(0) = 0
                [0, 0, 2, 0, 0, 0],      # a(0) = 0
                [1, T, T2, T3, T4, T5],  # p(T) = end
                [0, 1, 2*T, 3*T2, 4*T3, 5*T4],  # v(T) = 0
                [0, 0, 2, 6*T, 12*T2, 20*T3]     # a(T) = 0
            ])
            
            b = np.array([self.start[i], 0, 0, self.end[i], 0, 0])
            c = np.linalg.solve(M, b)
            coeffs.append(c)
            
        return np.array(coeffs)
    
    def evaluate(self, t):
        """Evaluate trajectory at time t."""
        t = np.clip(t, 0, self.T)
        
        T = np.array([1, t, t**2, t**3, t**4, t**5])
        Td = np.array([0, 1, 2*t, 3*t**2, 4*t**3, 5*t**4])
        Tdd = np.array([0, 0, 2, 6*t, 12*t**2, 20*t**3])
        
        pos = self.coeffs @ T
        vel = self.coeffs @ Td
        acc = self.coeffs @ Tdd
        
        return pos, vel, acc
```

**Trapezoidal Velocity Profile:**

```python
class TrapezoidalProfile:
    """Trapezoidal velocity profile for point-to-point motion."""
    
    def __init__(self, distance, vmax, amax):
        """
        Generate trapezoidal velocity profile.
        
        distance: Total distance to travel
        vmax: Maximum velocity
        amax: Maximum acceleration
        """
        self.d = distance
        self.vmax = vmax
        self.amax = amax
        
        # Compute profile parameters
        self.t_acc = vmax / amax  # Acceleration time
        self.d_acc = 0.5 * amax * self.t_acc**2  # Distance during accel
        
        if 2 * self.d_acc >= distance:
            # Triangular profile (never reaches vmax)
            self.t_acc = np.sqrt(distance / amax)
            self.vmax = amax * self.t_acc
            self.t_const = 0
        else:
            # Trapezoidal profile
            self.t_const = (distance - 2 * self.d_acc) / vmax
            
        self.T = 2 * self.t_acc + self.t_const
        
    def evaluate(self, t):
        """Evaluate profile at time t."""
        t = np.clip(t, 0, self.T)
        
        if t < self.t_acc:
            # Acceleration phase
            pos = 0.5 * self.amax * t**2
            vel = self.amax * t
            acc = self.amax
        elif t < self.t_acc + self.t_const:
            # Constant velocity phase
            t_const = t - self.t_acc
            pos = self.d_acc + self.vmax * t_const
            vel = self.vmax
            acc = 0
        else:
            # Deceleration phase
            t_dec = t - self.t_acc - self.t_const
            pos = self.d - 0.5 * self.amax * (self.t_acc - t_dec)**2
            vel = self.vmax - self.amax * t_dec
            acc = -self.amax
            
        return pos, vel, acc
    
    def get_duration(self):
        """Return total duration."""
        return self.T
```

### 4. Model Predictive Control (MPC)

**Linear MPC with CVXPY:**

```python
import cvxpy as cp

class LinearMPC:
    """Linear MPC using CVXPY."""
    
    def __init__(self, A, B, Q, R, Qf, N, u_min, u_max):
        """
        MPC with prediction horizon N.
        
        A, B: System dynamics
        Q, R: Stage costs
        Qf: Terminal cost
        N: Prediction horizon
        u_min, u_max: Input constraints
        """
        self.A = A
        self.B = B
        self.Q = Q
        self.R = R
        self.Qf = Qf
        self.N = N
        self.u_min = u_min
        self.u_max = u_max
        
        self.nx = A.shape[0]
        self.nu = B.shape[1]
        
    def solve(self, x0, x_ref=None):
        """
        Solve MPC optimization.
        
        x0: Current state
        x_ref: Reference trajectory (N+1, nx)
        """
        if x_ref is None:
            x_ref = np.zeros((self.N + 1, self.nx))
        
        # Decision variables
        x = cp.Variable((self.N + 1, self.nx))
        u = cp.Variable((self.N, self.nu))
        
        # Cost function
        cost = 0
        for k in range(self.N):
            cost += cp.quad_form(x[k] - x_ref[k], self.Q)
            cost += cp.quad_form(u[k], self.R)
        cost += cp.quad_form(x[self.N] - x_ref[self.N], self.Qf)
        
        # Constraints
        constraints = [x[0] == x0]
        for k in range(self.N):
            constraints += [x[k + 1] == self.A @ x[k] + self.B @ u[k]]
            constraints += [self.u_min <= u[k], u[k] <= self.u_max]
        
        # Solve
        problem = cp.Problem(cp.Minimize(cost), constraints)
        problem.solve(solver=cp.OSQP)
        
        if problem.status == 'optimal':
            return u.value[0], x.value, u.value
        else:
            return None, None, None
```

### 5. System Identification

**Least Squares Identification:**

```python
def identify_first_order(data, dt):
    """
    Identify first-order system: tau * dy/dt + y = K * u
    
    Returns: K (gain), tau (time constant)
    """
    t = data['time']
    u = data['input']
    y = data['output']
    
    # Compute derivatives using finite differences
    dy = np.gradient(y, dt)
    
    # Form regression matrix: [dy/dt, y] * [tau; 1] = K * u
    # Actually: tau * dy/dt = -y + K * u
    # Reformulate: dy/dt = -1/tau * y + K/tau * u
    
    Phi = np.column_stack([y, u])
    theta = np.linalg.lstsq(Phi, dy, rcond=None)[0]
    
    tau = -1 / theta[0]
    K = theta[1] * tau
    
    return K, tau
```

**Frequency Domain Identification:**

```python
from scipy.fft import fft, fftfreq

def frequency_response(data, dt):
    """
    Estimate frequency response from input-output data.
    """
    u = data['input']
    y = data['output']
    
    # Compute FFT
    U = fft(u)
    Y = fft(y)
    freqs = fftfreq(len(u), dt)
    
    # Frequency response
    H = Y / U
    
    # Only positive frequencies
    pos_freqs = freqs[:len(freqs)//2]
    pos_H = H[:len(H)//2]
    
    return pos_freqs, pos_H
```

## Common Patterns

### Pattern 1: Cascaded Control

```python
class CascadedController:
    """
    Cascaded position-velocity control.
    Outer loop: Position control (slow)
    Inner loop: Velocity control (fast)
    """
    
    def __init__(self, Kp_pos, Ki_pos, Kp_vel, Ki_vel, dt):
        self.pos_controller = PIDController(Kp_pos, Ki_pos, 0, dt)
        self.vel_controller = PIDController(Kp_vel, Ki_vel, 0, dt)
        
    def update(self, pos_setpoint, pos_meas, vel_meas):
        """
        Update cascaded controller.
        
        Returns: Torque/force command
        """
        # Outer loop: position -> velocity command
        vel_cmd = self.pos_controller.update(pos_setpoint, pos_meas)
        
        # Inner loop: velocity -> torque command
        torque_cmd = self.vel_controller.update(vel_cmd, vel_meas)
        
        return torque_cmd
```

### Pattern 2: Feedforward + Feedback

```python
class FeedforwardFeedbackController:
    """Combined feedforward and feedback control."""
    
    def __init__(self, Kp, Ki, Kd, dt, mass=1.0, damping=0.1):
        self.pid = PIDController(Kp, Ki, Kd, dt)
        self.mass = mass
        self.damping = damping
        
    def compute_feedforward(self, pos_desired, vel_desired, acc_desired):
        """Compute feedforward torque based on desired trajectory."""
        # Simple mass-damper model: tau = m*a + b*v
        return self.mass * acc_desired + self.damping * vel_desired
        
    def update(self, setpoint, measurement, trajectory_point):
        """
        Update with feedforward and feedback.
        
        trajectory_point: (pos, vel, acc) desired
        """
        # Feedforward
        tau_ff = self.compute_feedforward(*trajectory_point)
        
        # Feedback
        tau_fb = self.pid.update(setpoint, measurement)
        
        return tau_ff + tau_fb
```

### Pattern 3: ROS2 Controller Node

```python
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

class JointPositionController(Node):
    """ROS2 joint position controller with PID."""
    
    def __init__(self):
        super().__init__('joint_controller')
        
        # Parameters
        self.declare_parameter('Kp', 100.0)
        self.declare_parameter('Ki', 10.0)
        self.declare_parameter('Kd', 10.0)
        
        Kp = self.get_parameter('Kp').value
        Ki = self.get_parameter('Ki').value
        Kd = self.get_parameter('Kd').value
        
        self.controller = PIDController(Kp, Ki, Kd, dt=0.01)
        
        # Subscribers
        self.state_sub = self.create_subscription(
            JointState, '/joint_states', self.state_callback, 10)
        self.cmd_sub = self.create_subscription(
            Float64, '/joint_position_cmd', self.command_callback, 10)
        
        # Publisher
        self.effort_pub = self.create_publisher(
            Float64, '/joint_effort_cmd', 10)
        
        # Timer
        self.timer = self.create_timer(0.01, self.control_loop)
        
        self.current_position = 0.0
        self.setpoint = 0.0
        
    def state_callback(self, msg):
        self.current_position = msg.position[0]
        
    def command_callback(self, msg):
        self.setpoint = msg.data
        
    def control_loop(self):
        effort = self.controller.update(self.setpoint, self.current_position)
        
        msg = Float64()
        msg.data = effort
        self.effort_pub.publish(msg)
```

## Anti-Patterns

### ❌ Derivative on error
Using derivative of error causes derivative kick on setpoint changes.

**What happens:** Large control spikes when setpoint changes.

### ✅ Derivative on measurement
```python
# Wrong
D = Kd * (error - prev_error) / dt

# Right
D = -Kd * (measurement - prev_measurement) / dt
```

### ❌ No integrator anti-windup
Integrator winds up during saturation, causing overshoot.

**What happens:** System overshoots, oscillates, takes long to settle.

### ✅ Implement anti-windup
```python
# Limit integral term
self.integral = np.clip(self.integral, -integral_limit, integral_limit)
```

### ❌ Ignoring sampling time
Using continuous PID gains on discrete system.

**What happens:** Instability, poor performance.

### ✅ Discrete PID design
```python
# Convert continuous to discrete using Tustin/bilinear
from scipy.signal import cont2discrete

A_disc, B_disc, _, _, _ = cont2discrete((A, B, C, D), dt, method='zoh')
```

## Configuration Reference

### PID Tuning Guidelines

| System Type | Kp Start | Ki Start | Kd Start | Notes |
|-------------|----------|----------|----------|-------|
| Temperature | Small | Very Small | 0 | Slow, integrating |
| Position | Medium | Small | Medium | Second-order |
| Velocity | Medium | Small | 0 | First-order |
| Current/Torque | Large | Medium | Small | Fast, electrical |

### LQR Weight Selection

| State | High Weight | Low Weight |
|-------|-------------|------------|
| Position error | Tight tracking | Loose tracking |
| Velocity | Smooth motion | Aggressive motion |
| Control effort | Energy saving | Performance |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| Oscillation | Too high gain / phase lag | Reduce gain or add derivative |
| Slow response | Low gain | Increase Kp |
| Steady-state error | Missing integral | Add Ki term |
| Overshoot | High gain or integrator windup | Reduce Kp, add anti-windup |
| Noise amplification | Derivative on noisy signal | Add filter or reduce Kd |
| Integrator windup | Saturation without anti-windup | Implement anti-windup |
| Unstable | Wrong sign or too high gain | Check signs, reduce gains |
| Delayed response | Sampling too slow | Increase control rate |

## Workflow Integration

- **Before this:** Use `ros2-control` for hardware interfaces
- **After this:** Use `realtime-motor-control` for low-level motor control
- **Parallel with:** Use `path-planning` for trajectory generation
- **For simulation:** Use `gazebo` to test controllers

## Further Reading

- "Feedback Systems" by Åström and Murray
- "Modern Control Engineering" by Ogata
- Related skills: `realtime-motor-control`, `ros2-control`, `path-planning`

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering PID, LQR, MPC, trajectory generation, system ID