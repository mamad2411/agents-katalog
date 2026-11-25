---
name: mujoco
description: MuJoCo physics simulation, contact modeling, MJCF format, optimal control, and DeepMind integration for robotics research.
category: simulation
tags: [mujoco, physics, simulation, mjcf, contact, optimal-control, deepmind, robotics]
version: "1.0.0"
---

# MuJoCo

MuJoCo (Multi-Joint dynamics with Contact) is a high-performance physics engine for robotics. This skill covers MJCF modeling, contact dynamics, and optimal control.

## When to Use

- Research-grade physics simulation with accurate contact modeling
- Model Predictive Control (MPC) and trajectory optimization
- Reinforcement learning with fast simulation (1000+ FPS)
- Biomechanics and humanoid robotics
- Sim-to-real transfer requiring precise dynamics
- Optimal control and state estimation research

## Quick Start

```bash
# Install MuJoCo
pip install mujoco

# Download models
git clone https://github.com/deepmind/mujoco_menagerie.git

# Basic usage
python -c "import mujoco; print(mujoco.__version__)"
```

## Core Concepts

### 1. MJCF (Model XML Format)

MuJoCo's native modeling format.

```xml
<mujoco model="robot">
  <compiler angle="radian" meshdir="meshes/"/>
  
  <asset>
    <texture name="grid" type="2d" builtin="checker" width="512" height="512"/>
    <material name="grid" texture="grid" texrepeat="8 8" reflectance="0.1"/>
    <mesh name="chassis" file="chassis.stl" scale="0.001 0.001 0.001"/>
  </asset>
  
  <worldbody>
    <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
    <geom name="floor" size="100 100 0.1" type="plane" material="grid"/>
    
    <body name="robot" pos="0 0 0.5">
      <freejoint/>
      <geom name="chassis_geom" type="mesh" mesh="chassis" mass="10"/>
      
      <body name="wheel_left" pos="-0.2 0.3 0">
        <joint name="wheel_left_joint" type="hinge" axis="0 1 0"/>
        <geom name="wheel_left_geom" type="cylinder" size="0.1 0.05" mass="1"/>
      </body>
      
      <body name="wheel_right" pos="-0.2 -0.3 0">
        <joint name="wheel_right_joint" type="hinge" axis="0 1 0"/>
        <geom name="wheel_right_geom" type="cylinder" size="0.1 0.05" mass="1"/>
      </body>
    </body>
  </worldbody>
  
  <actuator>
    <motor name="left_motor" joint="wheel_left_joint" gear="1" ctrlrange="-100 100"/>
    <motor name="right_motor" joint="wheel_right_joint" gear="1" ctrlrange="-100 100"/>
  </actuator>
  
  <sensor>
    <accelerometer name="imu_accel" site="imu_site"/>
    <gyro name="imu_gyro" site="imu_site"/>
    <jointpos name="wheel_left_pos" joint="wheel_left_joint"/>
    <jointvel name="wheel_left_vel" joint="wheel_left_joint"/>
  </sensor>
</mujoco>
```

**Python loading and basic simulation:**
```python
import mujoco
import numpy as np

# Load model
model = mujoco.MjModel.from_xml_path("robot.xml")
data = mujoco.MjData(model)

# Simulation loop
duration = 10.0  # seconds
while data.time < duration:
    # Set control inputs
    data.ctrl[0] = 10.0   # Left wheel torque
    data.ctrl[1] = 10.0   # Right wheel torque
    
    # Step simulation
    mujoco.mj_step(model, data)
    
    # Access state
    position = data.qpos  # Joint positions
    velocity = data.qvel  # Joint velocities
    sensor_data = data.sensordata
```

### 2. Contact Modeling

MuJoCo's soft contact model prevents penetration while remaining differentiable.

```python
# Contact parameters in MJCF
"""
<geom name="foot" size="0.05" friction="1.0 0.005 0.0001"
      solimp="0.9 0.95 0.001" solref="0.02 1"/>
"""

# solimp: impedance parameters (dmin, dmax, width)
# solref: reference parameters (timeconst, dampratio)

# Access contact data
def print_contacts(model, data):
    for i in range(data.ncon):
        contact = data.contact[i]
        print(f"Contact {i}: {contact.geom1} - {contact.geom2}")
        print(f"  Position: {contact.pos}")
        print(f"  Normal force: {data.cfrc_ext[contact.geom2]}")
```

### 3. Optimal Control with mocap

Model Predictive Control using MuJoCo's optimal control solvers.

```python
import mujoco
from mujoco import minimize

# Define trajectory optimization problem
def make_trajectory_problem(model, data, horizon=100):
    # State: [qpos, qvel]
    # Control: joint torques
    
    def cost(state, control):
        # Target state cost
        target_pos = np.array([1.0, 0.0, 0.5])
        pos_cost = np.sum((state[:3] - target_pos) ** 2)
        
        # Control cost
        ctrl_cost = 0.01 * np.sum(control ** 2)
        
        return pos_cost + ctrl_cost
    
    def dynamics(state, control):
        # Set state and control
        data.qpos[:] = state[:model.nq]
        data.qvel[:] = state[model.nq:]
        data.ctrl[:] = control
        
        # Step physics
        mujoco.mj_step(model, data)
        
        # Return next state
        return np.concatenate([data.qpos, data.qvel])
    
    return cost, dynamics

# Solve with iterative LQR (iLQR)
from scipy.optimize import minimize

def ilqr_solve(model, data, x0, horizon=100):
    # Initialize trajectory
    states = [x0 for _ in range(horizon + 1)]
    controls = [np.zeros(model.nu) for _ in range(horizon)]
    
    for iteration in range(100):
        # Forward pass
        for t in range(horizon):
            states[t+1] = dynamics(states[t], controls[t])
        
        # Backward pass (compute gradients)
        # ... (implement LQR backward pass)
        
        # Update controls
        # ...
    
    return states, controls
```

### 4. Reinforcement Learning Integration

Fast simulation for RL training.

```python
import gymnasium as gym
from gymnasium import spaces

class MuJoCoRobotEnv(gym.Env):
    def __init__(self, xml_path, frame_skip=5):
        super().__init__()
        
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)
        self.frame_skip = frame_skip
        
        # Action space: joint torques
        self.action_space = spaces.Box(
            low=self.model.actuator_ctrlrange[:, 0],
            high=self.model.actuator_ctrlrange[:, 1],
            dtype=np.float32
        )
        
        # Observation space: joint positions, velocities, sensor data
        obs_dim = self.model.nq + self.model.nv + self.model.nsensordata
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32
        )
    
    def reset(self, seed=None):
        super().reset(seed=seed)
        
        # Reset to keyframe or default
        mujoco.mj_resetData(self.model, self.data)
        
        # Randomize initial state
        self.data.qpos[:] += np.random.randn(self.model.nq) * 0.01
        
        return self._get_obs(), {}
    
    def step(self, action):
        # Apply action
        self.data.ctrl[:] = action
        
        # Simulate with frame skip
        for _ in range(self.frame_skip):
            mujoco.mj_step(self.model, self.data)
        
        # Compute reward
        reward = self._compute_reward()
        
        # Check termination
        terminated = self._check_termination()
        
        return self._get_obs(), reward, terminated, False, {}
    
    def _get_obs(self):
        return np.concatenate([
            self.data.qpos,
            self.data.qvel,
            self.data.sensordata
        ])
    
    def _compute_reward(self):
        # Example: reward for forward velocity
        return self.data.qvel[0]  # x-direction velocity
    
    def _check_termination(self):
        # Terminate if robot falls
        return self.data.qpos[2] < 0.3  # z-position check
```

## Configuration Reference

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| timestep | Simulation timestep | 0.002 s |
| integrator | Integration method | Euler, RK4, implicit |
| iterations | Solver iterations | 50-100 |
| solver | Constraint solver | Newton, CG |
| cone | Friction cone | pyramidal, elliptic |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Unstable simulation | Large timestep | Reduce timestep, increase iterations |
| Slow simulation | Complex mesh collisions | Use primitive geom approximations |
| Contact jitter | Too stiff contacts | Increase solimp width |
| Joint oscillation | High gains | Reduce controller gains |

## Workflow Integration

- **With:** Use `isaac-sim` for photorealistic rendering of MuJoCo trajectories
- **Before:** Use `control-systems` for MPC theory
- **After:** Use `sim-to-real` for transferring policies

## Common Patterns

### Pattern 1: Parallel Simulation Rollouts for MPC

Run many simulation copies simultaneously for model predictive control sampling.

```python
import mujoco
import numpy as np
from multiprocessing import Pool
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class RolloutResult:
    controls: np.ndarray
    total_cost: float
    final_state: np.ndarray


def rollout_worker(args: Tuple) -> RolloutResult:
    """Worker function for parallel simulation rollout."""
    xml_path, initial_qpos, initial_qvel, controls, horizon = args

    model = mujoco.MjModel.from_xml_path(xml_path)
    data = mujoco.MjData(model)

    # Set initial state
    data.qpos[:] = initial_qpos
    data.qvel[:] = initial_qvel
    mujoco.mj_forward(model, data)

    total_cost = 0.0
    target_pos = np.array([2.0, 0.0])  # goal position (x, y)

    for t in range(horizon):
        data.ctrl[:] = controls[t]
        mujoco.mj_step(model, data)

        # Running cost: distance to goal + control effort
        pos_cost = np.linalg.norm(data.qpos[:2] - target_pos) ** 2
        ctrl_cost = 0.01 * np.sum(controls[t] ** 2)
        total_cost += pos_cost + ctrl_cost

    # Terminal cost
    total_cost += 10.0 * np.linalg.norm(data.qpos[:2] - target_pos) ** 2

    return RolloutResult(
        controls=controls,
        total_cost=total_cost,
        final_state=np.concatenate([data.qpos.copy(), data.qvel.copy()])
    )


class MPPIController:
    """Model Predictive Path Integral controller using MuJoCo rollouts."""

    def __init__(self, xml_path: str, horizon: int = 30, n_samples: int = 512,
                 temperature: float = 0.1, noise_sigma: float = 0.5):
        self.xml_path = xml_path
        self.horizon = horizon
        self.n_samples = n_samples
        self.temperature = temperature
        self.noise_sigma = noise_sigma

        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)

        # Nominal control sequence (warm-started)
        self.nominal_controls = np.zeros((horizon, self.model.nu))

    def compute_action(self, current_qpos: np.ndarray,
                       current_qvel: np.ndarray) -> np.ndarray:
        """Compute optimal action via MPPI sampling."""
        # Generate perturbed control sequences
        noise = np.random.randn(self.n_samples, self.horizon, self.model.nu)
        noise *= self.noise_sigma
        perturbed = self.nominal_controls[np.newaxis] + noise  # (N, H, nu)

        # Clip to actuator limits
        ctrl_min = self.model.actuator_ctrlrange[:, 0]
        ctrl_max = self.model.actuator_ctrlrange[:, 1]
        perturbed = np.clip(perturbed, ctrl_min, ctrl_max)

        # Parallel rollouts
        args_list = [
            (self.xml_path, current_qpos.copy(), current_qvel.copy(),
             perturbed[i], self.horizon)
            for i in range(self.n_samples)
        ]

        with Pool(processes=8) as pool:
            results: List[RolloutResult] = pool.map(rollout_worker, args_list)

        costs = np.array([r.total_cost for r in results])

        # MPPI update: weighted average of perturbations
        beta = np.min(costs)
        weights = np.exp(-(costs - beta) / self.temperature)
        weights /= np.sum(weights)

        # Weighted sum of noise
        weighted_noise = np.einsum('n,nhd->hd', weights, noise)
        self.nominal_controls = np.clip(
            self.nominal_controls + weighted_noise, ctrl_min, ctrl_max
        )

        # Shift nominal sequence (receding horizon)
        action = self.nominal_controls[0].copy()
        self.nominal_controls = np.roll(self.nominal_controls, -1, axis=0)
        self.nominal_controls[-1] = 0.0

        return action
```

### Pattern 2: Contact-Aware Grasping Simulation

Simulate object grasping with contact force feedback.

```python
import mujoco
import numpy as np


class GraspSimulator:
    """Simulate robotic grasping with contact force monitoring."""

    GRASP_FORCE_THRESHOLD = 5.0    # Newtons — minimum to confirm grasp
    SLIP_FORCE_THRESHOLD = 50.0    # Newtons — maximum before slip

    def __init__(self, xml_path: str):
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)

        # Finger actuator IDs (adjust to your model)
        self._finger1_act = mujoco.mj_name2id(
            self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, 'finger1'
        )
        self._finger2_act = mujoco.mj_name2id(
            self.model, mujoco.mjtObj.mjOBJ_ACTUATOR, 'finger2'
        )

        # Object geom ID to monitor
        self._object_geom = mujoco.mj_name2id(
            self.model, mujoco.mjtObj.mjOBJ_GEOM, 'object'
        )

    def get_contact_forces(self) -> dict:
        """Extract contact forces on the object geom."""
        forces = {'normal': [], 'tangential': [], 'contacts': []}

        for i in range(self.data.ncon):
            contact = self.data.contact[i]

            # Check if this contact involves the object
            if (contact.geom1 == self._object_geom or
                    contact.geom2 == self._object_geom):

                # Extract 6D contact wrench [fx, fy, fz, tx, ty, tz]
                contact_force = np.zeros(6)
                mujoco.mj_contactForce(self.model, self.data, i, contact_force)

                normal_force = abs(contact_force[0])
                tangential_force = np.linalg.norm(contact_force[1:3])

                forces['normal'].append(normal_force)
                forces['tangential'].append(tangential_force)
                forces['contacts'].append({
                    'pos': contact.pos.copy(),
                    'normal': contact.frame[:3].copy(),
                    'normal_force': normal_force,
                })

        return forces

    def execute_grasp(self, target_force: float = 20.0,
                      max_steps: int = 2000) -> dict:
        """Execute a grasp and return outcome metrics."""
        grasp_result = {
            'success': False,
            'peak_normal_force': 0.0,
            'contact_count': 0,
            'steps_to_grasp': 0,
        }

        for step in range(max_steps):
            # Proportional finger closing
            current_force = 0.0
            forces = self.get_contact_forces()
            if forces['normal']:
                current_force = np.mean(forces['normal'])

            # Force control: close fingers until target force
            error = target_force - current_force
            ctrl_delta = np.clip(0.001 * error, -0.01, 0.01)

            self.data.ctrl[self._finger1_act] += ctrl_delta
            self.data.ctrl[self._finger2_act] += ctrl_delta

            mujoco.mj_step(self.model, self.data)

            # Update metrics
            if forces['normal']:
                peak = max(forces['normal'])
                grasp_result['peak_normal_force'] = max(
                    grasp_result['peak_normal_force'], peak
                )
                grasp_result['contact_count'] = len(forces['contacts'])

                # Check success: sufficient force, not slipping
                if (current_force >= self.GRASP_FORCE_THRESHOLD and
                        peak < self.SLIP_FORCE_THRESHOLD and
                        len(forces['contacts']) >= 2):
                    grasp_result['success'] = True
                    grasp_result['steps_to_grasp'] = step
                    break

        return grasp_result

    def check_lift_stability(self, lift_height: float = 0.1,
                              steps: int = 500) -> bool:
        """After grasping, verify the object stays in the gripper during lift."""
        object_body = mujoco.mj_name2id(
            self.model, mujoco.mjtObj.mjOBJ_BODY, 'object'
        )
        initial_z = self.data.xpos[object_body, 2]

        # Apply upward lift via robot arm joints
        for _ in range(steps):
            mujoco.mj_step(self.model, self.data)

        final_z = self.data.xpos[object_body, 2]
        return (final_z - initial_z) >= (lift_height * 0.8)
```

### Pattern 3: System Identification via MuJoCo Derivatives

Identify real robot dynamics by fitting MuJoCo model parameters to observed data.

```python
import mujoco
import numpy as np
from scipy.optimize import minimize
from typing import List, Tuple


class SystemIdentifier:
    """Identify physical parameters by matching simulation to real data."""

    def __init__(self, xml_template_path: str):
        self.xml_template_path = xml_template_path
        # Parameters to identify: [wheel_radius, wheel_friction, motor_damping]
        self._param_names = ['wheel_radius', 'wheel_friction', 'motor_damping']

    def _build_model_with_params(self, params: np.ndarray) -> mujoco.MjModel:
        """Rebuild MJCF with candidate parameters."""
        wheel_radius, wheel_friction, motor_damping = params

        with open(self.xml_template_path, 'r') as f:
            xml_str = f.read()

        # Substitute parameters into XML string
        xml_str = xml_str.replace('__WHEEL_RADIUS__', f'{wheel_radius:.6f}')
        xml_str = xml_str.replace('__WHEEL_FRICTION__', f'{wheel_friction:.6f}')
        xml_str = xml_str.replace('__MOTOR_DAMPING__', f'{motor_damping:.6f}')

        return mujoco.MjModel.from_xml_string(xml_str)

    def simulate_trajectory(self, model: mujoco.MjModel,
                            controls: np.ndarray,
                            dt: float) -> np.ndarray:
        """Simulate robot given control sequence, return state trajectory."""
        data = mujoco.MjData(model)
        model.opt.timestep = dt
        states = []

        for ctrl in controls:
            data.ctrl[:] = ctrl
            mujoco.mj_step(model, data)
            states.append(np.concatenate([data.qpos.copy(), data.qvel.copy()]))

        return np.array(states)

    def identification_loss(self, params: np.ndarray,
                            real_states: np.ndarray,
                            controls: np.ndarray,
                            dt: float) -> float:
        """Compute MSE between simulated and real trajectories."""
        # Guard against unphysical parameters
        if np.any(params <= 0):
            return 1e9

        try:
            model = self._build_model_with_params(params)
        except Exception:
            return 1e9

        sim_states = self.simulate_trajectory(model, controls, dt)

        # Align lengths
        n = min(len(real_states), len(sim_states))
        loss = np.mean((real_states[:n] - sim_states[:n]) ** 2)
        return float(loss)

    def identify(self, real_states: np.ndarray,
                 controls: np.ndarray,
                 dt: float = 0.01,
                 initial_guess: np.ndarray = None) -> dict:
        """Run optimization to find best-fit parameters."""
        if initial_guess is None:
            initial_guess = np.array([0.05, 1.0, 0.1])  # defaults

        bounds = [(0.01, 0.15), (0.1, 5.0), (0.001, 1.0)]

        result = minimize(
            fun=self.identification_loss,
            x0=initial_guess,
            args=(real_states, controls, dt),
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': 200, 'ftol': 1e-8},
        )

        identified = {
            name: float(val)
            for name, val in zip(self._param_names, result.x)
        }
        identified['final_loss'] = float(result.fun)
        identified['success'] = result.success
        return identified


# Usage example
if __name__ == '__main__':
    import json

    # Load logged real-robot data
    with open('real_robot_log.json') as f:
        log = json.load(f)

    real_states = np.array(log['states'])  # (T, nq+nv)
    controls = np.array(log['controls'])   # (T, nu)

    ident = SystemIdentifier('robot_template.xml')
    params = ident.identify(real_states, controls, dt=0.01)
    print('Identified parameters:', params)
```

### Pattern 4: Headless Rendering for Visual RL

Generate camera observations in headless mode for visual reinforcement learning.

```python
import mujoco
import mujoco.renderer
import numpy as np


class HeadlessRenderer:
    """Render MuJoCo scenes without a display for training visual policies."""

    def __init__(self, model: mujoco.MjModel, width: int = 84, height: int = 84):
        self.model = model
        self.data = mujoco.MjData(model)
        self.width = width
        self.height = height
        self._renderer = mujoco.Renderer(model, height=height, width=width)

    def render_rgb(self, camera_name: str = 'frontview') -> np.ndarray:
        """Render current state to RGB array (H, W, 3) uint8."""
        self._renderer.update_scene(self.data, camera=camera_name)
        return self._renderer.render()

    def render_depth(self, camera_name: str = 'frontview') -> np.ndarray:
        """Render depth map (H, W) float32 in metres."""
        self._renderer.enable_depth_rendering()
        self._renderer.update_scene(self.data, camera=camera_name)
        depth = self._renderer.render()
        self._renderer.disable_depth_rendering()
        return depth

    def render_segmentation(self, camera_name: str = 'frontview') -> np.ndarray:
        """Render geom segmentation mask (H, W) int32."""
        self._renderer.enable_segmentation_rendering()
        self._renderer.update_scene(self.data, camera=camera_name)
        seg = self._renderer.render()[:, :, 0]  # geom IDs in channel 0
        self._renderer.disable_segmentation_rendering()
        return seg

    def get_stacked_obs(self, n_frames: int = 4,
                        camera_name: str = 'frontview') -> np.ndarray:
        """Return last n_frames stacked as (n_frames*3, H, W) for CNNs."""
        if not hasattr(self, '_frame_buffer'):
            self._frame_buffer = np.zeros(
                (n_frames, 3, self.height, self.width), dtype=np.uint8
            )

        frame = self.render_rgb(camera_name)          # (H, W, 3)
        frame = frame.transpose(2, 0, 1)              # (3, H, W)
        self._frame_buffer = np.roll(self._frame_buffer, -1, axis=0)
        self._frame_buffer[-1] = frame

        return self._frame_buffer.reshape(-1, self.height, self.width)

    def close(self):
        self._renderer.close()
```

### Pattern 5: Keyframe-Based Motion Interpolation

Animate robot through keyframes defined in MJCF and use MuJoCo's kinematics to
interpolate smooth joint trajectories.

```python
import mujoco
import numpy as np
from scipy.interpolate import CubicSpline


class KeyframeMotionPlayer:
    """Play keyframe-defined motions using MuJoCo's native keyframe system."""

    def __init__(self, xml_path: str):
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)

    def list_keyframes(self) -> List[str]:
        """Return names of all keyframes defined in the model."""
        names = []
        for i in range(self.model.nkey):
            name = mujoco.mj_id2name(
                self.model, mujoco.mjtObj.mjOBJ_KEY, i
            )
            if name:
                names.append(name)
        return names

    def get_keyframe_qpos(self, keyframe_name: str) -> np.ndarray:
        """Extract joint positions for a named keyframe."""
        key_id = mujoco.mj_name2id(
            self.model, mujoco.mjtObj.mjOBJ_KEY, keyframe_name
        )
        if key_id < 0:
            raise ValueError(f'Keyframe not found: {keyframe_name}')
        return self.model.key_qpos[key_id].copy()

    def build_spline_trajectory(self, keyframe_names: List[str],
                                 durations: List[float],
                                 dt: float = 0.002) -> np.ndarray:
        """Build a smooth cubic spline trajectory through keyframe poses.

        Args:
            keyframe_names: Ordered list of keyframe names.
            durations: Time (seconds) to spend between successive keyframes.
            dt: Simulation timestep.

        Returns:
            Array of shape (T, nq) with joint positions at each step.
        """
        assert len(durations) == len(keyframe_names) - 1

        times = np.concatenate([[0.0], np.cumsum(durations)])
        waypoints = np.stack([
            self.get_keyframe_qpos(name) for name in keyframe_names
        ])

        # Fit cubic spline for each joint independently
        spline = CubicSpline(times, waypoints, bc_type='clamped')

        t_eval = np.arange(0, times[-1], dt)
        return spline(t_eval)  # (T, nq)

    def execute_trajectory(self, qpos_traj: np.ndarray,
                            kp: float = 200.0,
                            kd: float = 20.0):
        """Track a joint position trajectory with PD control."""
        for qpos_ref in qpos_traj:
            qpos_err = qpos_ref - self.data.qpos
            qvel_err = -self.data.qvel

            # PD torque for each actuated joint
            torque = kp * qpos_err[:self.model.nu] + kd * qvel_err[:self.model.nu]
            torque = np.clip(
                torque,
                self.model.actuator_ctrlrange[:, 0],
                self.model.actuator_ctrlrange[:, 1]
            )
            self.data.ctrl[:] = torque
            mujoco.mj_step(self.model, self.data)
```

## Anti-Patterns

### Anti-Pattern 1: Reloading the Model Inside the Simulation Loop

❌ **Wrong — model loading is expensive and causes memory leaks:**
```python
def simulate_step(xml_path, qpos, ctrl):
    # WRONG: creates a new model every call
    model = mujoco.MjModel.from_xml_path(xml_path)  # ~50 ms each
    data = mujoco.MjData(model)
    data.qpos[:] = qpos
    data.ctrl[:] = ctrl
    mujoco.mj_step(model, data)
    return data.qpos.copy()

for step in range(10000):
    qpos = simulate_step('robot.xml', current_qpos, current_ctrl)
```

✅ **Correct — load once, reuse across steps:**
```python
class Simulator:
    def __init__(self, xml_path: str):
        # Load once at construction
        self.model = mujoco.MjModel.from_xml_path(xml_path)
        self.data = mujoco.MjData(self.model)

    def step(self, ctrl: np.ndarray) -> np.ndarray:
        self.data.ctrl[:] = ctrl
        mujoco.mj_step(self.model, self.data)
        return self.data.qpos.copy()

    def reset(self, qpos: np.ndarray = None, qvel: np.ndarray = None):
        mujoco.mj_resetData(self.model, self.data)
        if qpos is not None:
            self.data.qpos[:] = qpos
        if qvel is not None:
            self.data.qvel[:] = qvel
        mujoco.mj_forward(self.model, self.data)

sim = Simulator('robot.xml')
for step in range(10000):
    qpos = sim.step(current_ctrl)
```

### Anti-Pattern 2: Using `mj_step` Without Calling `mj_forward` After State Injection

❌ **Wrong — derived quantities are stale after manually setting qpos/qvel:**
```python
# WRONG: qpos was set but forward kinematics not updated
data.qpos[0] = 1.5
data.qpos[1] = 0.3
# At this point data.xpos, data.xmat, data.geom_xpos are wrong
contact_forces = get_contact_forces(model, data)  # reads stale xpos
print(data.xpos[1])  # Incorrect body position
```

✅ **Correct — always call `mj_forward` after injecting state:**
```python
data.qpos[0] = 1.5
data.qpos[1] = 0.3
mujoco.mj_forward(model, data)   # recomputes all derived quantities
# Now xpos, xmat, geom_xpos, site_xpos are all consistent
contact_forces = get_contact_forces(model, data)
print(data.xpos[1])  # Correct body position
```

### Anti-Pattern 3: Ignoring Actuator Control Range

❌ **Wrong — sending unclamped actions causes physics instability:**
```python
def apply_action(data, raw_action: np.ndarray):
    # WRONG: neural network may output any float
    data.ctrl[:] = raw_action   # could be 1e6, causes NaN
    mujoco.mj_step(model, data)
```

✅ **Correct — always clip to the model's declared control range:**
```python
def apply_action(model: mujoco.MjModel, data: mujoco.MjData,
                 raw_action: np.ndarray):
    ctrl_min = model.actuator_ctrlrange[:, 0]
    ctrl_max = model.actuator_ctrlrange[:, 1]
    data.ctrl[:] = np.clip(raw_action, ctrl_min, ctrl_max)
    mujoco.mj_step(model, data)
```

### Anti-Pattern 4: Sharing MjData Across Threads Without Locking

❌ **Wrong — `MjData` is NOT thread-safe:**
```python
import threading

data = mujoco.MjData(model)  # shared across threads — WRONG

def thread_a():
    data.ctrl[0] = 10.0
    mujoco.mj_step(model, data)   # race condition

def thread_b():
    print(data.qpos[0])           # reads partially-written state

t1 = threading.Thread(target=thread_a)
t2 = threading.Thread(target=thread_b)
t1.start(); t2.start()
```

✅ **Correct — one MjData per thread, or protect access with a lock:**
```python
import threading

model = mujoco.MjModel.from_xml_path('robot.xml')   # MjModel is read-only, safe to share

def make_worker(ctrl_value: float):
    def worker():
        # Each thread owns its own MjData
        local_data = mujoco.MjData(model)
        local_data.ctrl[0] = ctrl_value
        mujoco.mj_step(model, local_data)
        print(f'Thread result qpos[0]: {local_data.qpos[0]:.4f}')
    return worker

threads = [threading.Thread(target=make_worker(float(i))) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

### Anti-Pattern 5: Using Dense Mesh Collisions for Fast Simulation

❌ **Wrong — triangle mesh contact is 100x slower than primitives:**
```xml
<!-- WRONG: full mesh used for collision -->
<geom name="wheel_col" type="mesh" mesh="wheel_hires" contype="1" conaffinity="1"/>
```

✅ **Correct — use a primitive geom for collision, mesh only for visual:**
```xml
<!-- Visual geom (no collision) -->
<geom name="wheel_vis" type="mesh" mesh="wheel_hires"
      contype="0" conaffinity="0" group="1"/>
<!-- Collision geom (primitive approximation, fast) -->
<geom name="wheel_col" type="cylinder" size="0.05 0.02"
      contype="1" conaffinity="1" rgba="0 0 0 0"/>
```

### Anti-Pattern 6: Using a Too-Large Timestep for Contact-Rich Tasks

❌ **Wrong — large timestep causes energy blow-up in contacts:**
```xml
<option timestep="0.02"/>  <!-- WRONG for contact-rich manipulation -->
```

```python
while data.time < 10.0:
    mujoco.mj_step(model, data)  # explodes after first contact
```

✅ **Correct — use small timestep and frame-skip in RL environments:**
```xml
<!-- physics timestep is small -->
<option timestep="0.002" integrator="implicitfast"/>
```

```python
PHYSICS_DT = 0.002   # 2 ms — stable for contacts
CONTROL_HZ = 50      # 20 ms control period
FRAME_SKIP = int(round(1.0 / (CONTROL_HZ * PHYSICS_DT)))  # = 10

for step in range(episode_length):
    data.ctrl[:] = policy(obs)
    for _ in range(FRAME_SKIP):          # physics runs at 500 Hz
        mujoco.mj_step(model, data)
    obs = get_observation(model, data)
```

### Anti-Pattern 7: Not Resetting `mj_resetData` Before Re-Running Episodes

❌ **Wrong — stale state from previous episode corrupts the next:**
```python
for episode in range(100):
    # WRONG: data still holds end-state of previous episode
    data.ctrl[:] = 0.0
    reward = run_episode(model, data)
```

✅ **Correct — full reset at the start of every episode:**
```python
for episode in range(100):
    # Full reset: zeroes qpos/qvel, clears contacts, resets time
    mujoco.mj_resetData(model, data)

    # Apply keyframe or domain randomization
    key_id = model.key('home').id
    data.qpos[:] = model.key_qpos[key_id]
    data.qpos += np.random.randn(model.nq) * 0.01   # domain rand
    mujoco.mj_forward(model, data)

    reward = run_episode(model, data)
```

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering MJCF, contact modeling, optimal control, RL

### v1.1.0 (2026-03-27)
- Added Common Patterns: MPPI rollouts, grasping simulation, system identification, headless rendering, keyframe interpolation
- Added Anti-Patterns: model reload in loop, missing mj_forward, unclipped actions, thread safety, mesh collision, timestep selection, episode reset