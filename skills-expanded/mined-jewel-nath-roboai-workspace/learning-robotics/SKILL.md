---
name: learning-robotics
description: Robot learning with imitation learning, behavior cloning, DAgger, reinforcement learning, reward shaping, and VLA models.
category: ai
tags: [robot-learning, imitation-learning, rl, reinforcement-learning, behavior-cloning, vla, dagger]
version: "1.0.0"
---

# Learning for Robotics

Robot learning enables adaptive behaviors through demonstration and experience. This skill covers imitation learning, RL, and vision-language-action models.

## When to Use

- Teaching robots through human demonstration
- Training policies via reinforcement learning
- Implementing behavior cloning from expert data
- Using DAgger for iterative improvement
- Deploying VLA models for instruction following
- Reward engineering for complex tasks

## Quick Start

```bash
# Install robot learning libraries
pip install stable-baselines3 gymnasium-robotics

# For imitation learning
pip install imitation lerobot

# For VLA models
pip install transformers torch
```

## Core Concepts

### 1. Imitation Learning (Behavior Cloning)

Learn policies from expert demonstrations.

```python
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

class DemonstrationDataset(Dataset):
    def __init__(self, trajectories):
        """
        trajectories: list of {'obs': [...], 'action': [...]}
        """
        self.data = []
        for traj in trajectories:
            for obs, act in zip(traj['obs'], traj['action']):
                self.data.append((obs, act))
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        obs, act = self.data[idx]
        return torch.FloatTensor(obs), torch.FloatTensor(act)

class BCModel(nn.Module):
    def __init__(self, obs_dim, action_dim, hidden_dim=256):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(obs_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # For normalized actions
        )
    
    def forward(self, obs):
        return self.network(obs)

def train_behavior_cloning(model, dataset, epochs=100):
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
    criterion = nn.MSELoss()
    
    for epoch in range(epochs):
        total_loss = 0
        for obs, action in dataloader:
            pred_action = model(obs)
            loss = criterion(pred_action, action)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch}: Loss = {total_loss/len(dataloader):.4f}")
```

### 2. DAgger (Dataset Aggregation)

Iteratively improve policy by collecting data from student.

```python
class DAgger:
    def __init__(self, model, expert_policy):
        self.model = model
        self.expert = expert_policy
        self.dataset = []
    
    def run_iteration(self, env, num_episodes=10):
        """Collect data using current policy with expert corrections."""
        for episode in range(num_episodes):
            obs, _ = env.reset()
            done = False
            
            while not done:
                # Student action
                with torch.no_grad():
                    student_action = self.model(
                        torch.FloatTensor(obs)
                    ).numpy()
                
                # Query expert for "correct" action
                expert_action = self.expert.predict(obs)
                
                # Store (obs, expert_action) pair
                self.dataset.append((obs, expert_action))
                
                # Execute student action (with noise)
                action = student_action + np.random.normal(0, 0.1)
                obs, _, done, _, _ = env.step(action)
        
        # Retrain on aggregated data
        self._retrain()
    
    def _retrain(self):
        """Retrain model on all collected data."""
        dataset = DemonstrationDataset([
            {'obs': [d[0] for d in self.dataset],
             'action': [d[1] for d in self.dataset]}
        ])
        train_behavior_cloning(self.model, dataset, epochs=50)
```

### 3. Reinforcement Learning

Train policies through trial and error.

```python
from stable_baselines3 import PPO, SAC
from stable_baselines3.common.env_util import make_vec_env

# Create vectorized environment
env = make_vec_env("Pendulum-v1", n_envs=8)

# PPO for discrete or continuous actions
model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    verbose=1
)

# Train
model.learn(total_timesteps=1_000_000)

# Save
model.save("ppo_robot")

# Load and deploy
model = PPO.load("ppo_robot")
```

**Custom robot environment:**
```python
import gymnasium as gym
from gymnasium import spaces

class PickPlaceEnv(gym.Env):
    def __init__(self):
        super().__init__()
        
        # Observation: [gripper_pos(3), gripper_open(1), object_pos(3), target_pos(3)]
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(10,), dtype=np.float32
        )
        
        # Action: [dx, dy, dz, gripper]
        self.action_space = spaces.Box(
            low=-1, high=1, shape=(4,), dtype=np.float32
        )
    
    def reset(self, seed=None):
        # Initialize scene
        self.gripper_pos = np.array([0.5, 0.0, 0.5])
        self.object_pos = np.random.uniform([0.3, -0.2, 0.1], [0.7, 0.2, 0.1])
        self.target_pos = np.random.uniform([0.3, -0.2, 0.0], [0.7, 0.2, 0.0])
        
        return self._get_obs(), {}
    
    def step(self, action):
        # Execute action
        self.gripper_pos += action[:3] * 0.01  # 1cm per step
        gripper_open = action[3] > 0
        
        # Check grasp
        distance_to_object = np.linalg.norm(self.gripper_pos - self.object_pos)
        
        # Compute reward (shaped)
        reward = self._compute_shaped_reward(distance_to_object, gripper_open)
        
        # Check success
        success = distance_to_object < 0.02 and not gripper_open
        
        return self._get_obs(), reward, success, False, {}
    
    def _compute_shaped_reward(self, dist, gripper_open):
        # Distance reward
        dist_reward = -dist
        
        # Grasp reward when close
        grasp_reward = 0
        if dist < 0.05 and not gripper_open:
            grasp_reward = 10
        
        # Placement reward
        place_reward = 0
        if not gripper_open:  # Holding object
            dist_to_target = np.linalg.norm(self.object_pos - self.target_pos)
            place_reward = -dist_to_target
        
        return dist_reward + grasp_reward + place_reward
```

### 4. Reward Shaping

Guide learning with intermediate rewards.

```python
class RewardShaper:
    def __init__(self):
        self.prev_distance = None
    
    def potential_based_shaping(self, state, action, next_state, base_reward):
        """Potential-based reward shaping preserves optimal policy."""
        # Define potential function
        def potential(s):
            # Distance to goal
            return -np.linalg.norm(s['robot'] - s['goal'])
        
        # Shaped reward
        phi_s = potential(state)
        phi_s_next = potential(next_state)
        
        shaped_reward = base_reward + 0.99 * phi_s_next - phi_s
        return shaped_reward
    
    def dense_rewards(self, env_state):
        """Multiple dense reward components."""
        rewards = {
            'distance_to_goal': -env_state['distance'],
            'heading_alignment': np.cos(env_state['heading_error']),
            'velocity_towards_goal': env_state['forward_vel'] * np.cos(env_state['heading_error']),
            'action_smoothness': -np.linalg.norm(env_state['action'] - env_state['prev_action']),
            'energy_penalty': -0.01 * np.sum(env_state['torque'] ** 2)
        }
        
        # Weighted sum
        weights = {'distance_to_goal': 1.0, 'heading_alignment': 0.5, 
                  'velocity_towards_goal': 1.0, 'action_smoothness': 0.1,
                  'energy_penalty': 0.01}
        
        return sum(rewards[k] * weights[k] for k in rewards)
```

## Anti-Patterns

### ❌ Sparse rewards without shaping
Only rewarding final success makes learning extremely slow.

**What happens:** No learning signal, random exploration fails.

### ✅ Dense, shaped rewards
```python
reward = -distance + alignment_bonus + progress_bonus - action_penalty
```

### ❌ Distribution mismatch in BC
Training on expert data only, testing on student distribution.

**What happens:** Compounding errors, policy diverges.

### ✅ Use DAgger or noise injection
```python
# Add noise to expert actions during collection
action = expert_action + np.random.normal(0, noise_std)
```

## Configuration Reference

| Algorithm | Data Needed | Sample Efficiency | Best For |
|-----------|-------------|-------------------|----------|
| Behavior Cloning | Expert demos only | High (offline) | Simple tasks |
| DAgger | Expert queries | Medium | Distribution shift |
| PPO | None | Low (online) | Complex dynamics |
| SAC | None | Medium (online) | Continuous control |
| VLA | Internet + robot data | High (pretrained) | Language instruction |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| BC policy fails | Distribution shift | Use DAgger, add noise |
| RL not learning | Poor reward shaping | Add dense rewards |
| Unstable training | Learning rate too high | Reduce LR, use LR schedule |
| Poor generalization | Overfitting to demos | Data augmentation |

## Common Patterns

### Behavior Cloning Data Collection Pipeline

Collect demonstrations from a teleoperated robot and save them in the HDF5 format used by most imitation learning libraries. The pipeline records synchronised observation-action pairs at a fixed rate.

```python
#!/usr/bin/env python3
"""
data_collector.py — ROS 2 node that records teleoperation demonstrations.

Records to HDF5 files compatible with the imitation library and LeRobot.

Usage
-----
ros2 run orbibot_agent data_collector --ros-args -p output_dir:=/data/demos
"""
import os
import time
import json
import threading
from dataclasses import dataclass, field
from typing import Optional

import h5py
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge


@dataclass
class Transition:
    obs_image: Optional[np.ndarray] = None   # (H, W, C) uint8
    obs_scan: Optional[np.ndarray] = None    # (N,) float32
    obs_odom: Optional[np.ndarray] = None    # [x, y, yaw, vx, vy, vyaw]
    action: Optional[np.ndarray] = None      # [vx, vy, vyaw]
    timestamp: float = 0.0


class DemoCollector(Node):
    """Subscribes to robot topics and records synchronised demonstrations.

    Parameters
    ----------
    output_dir : str
        Directory where HDF5 episode files are written.
    record_hz : float
        Observation-action sampling rate (default 10 Hz).
    """

    def __init__(self):
        super().__init__("demo_collector")
        self.declare_parameter("output_dir", "/tmp/demos")
        self.declare_parameter("record_hz", 10.0)

        output_dir = self.get_parameter("output_dir").value
        record_hz = self.get_parameter("record_hz").value
        os.makedirs(output_dir, exist_ok=True)

        self._output_dir = output_dir
        self._bridge = CvBridge()
        self._lock = threading.Lock()
        self._latest = Transition()
        self._episode: list[Transition] = []
        self._recording = False
        self._episode_count = 0

        # Subscribers
        self.create_subscription(Image, "/camera/color/image_raw", self._image_cb, 10)
        self.create_subscription(LaserScan, "/scan", self._scan_cb, 10)
        self.create_subscription(Odometry, "/odometry/filtered", self._odom_cb, 10)
        self.create_subscription(Twist, "/cmd_vel", self._action_cb, 10)

        # Keyboard control via topic (ros2 topic pub /record std_msgs/String "data: 'start'")
        from std_msgs.msg import String
        self.create_subscription(String, "/record", self._record_cmd_cb, 10)

        self._timer = self.create_timer(1.0 / record_hz, self._sample)
        self.get_logger().info(f"DemoCollector ready — output: {output_dir}")

    # ---------------------------------------------------------------
    def _image_cb(self, msg: Image) -> None:
        img = self._bridge.imgmsg_to_cv2(msg, desired_encoding="rgb8")
        # Resize to 128x128 to save disk space
        import cv2
        img = cv2.resize(img, (128, 128))
        with self._lock:
            self._latest.obs_image = img

    def _scan_cb(self, msg: LaserScan) -> None:
        ranges = np.array(msg.ranges, dtype=np.float32)
        ranges = np.clip(ranges, msg.range_min, msg.range_max)
        ranges = np.nan_to_num(ranges, nan=msg.range_max)
        with self._lock:
            self._latest.obs_scan = ranges

    def _odom_cb(self, msg: Odometry) -> None:
        import math
        q = msg.pose.pose.orientation
        yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y ** 2 + q.z ** 2))
        obs = np.array([
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            yaw,
            msg.twist.twist.linear.x,
            msg.twist.twist.linear.y,
            msg.twist.twist.angular.z,
        ], dtype=np.float32)
        with self._lock:
            self._latest.obs_odom = obs

    def _action_cb(self, msg: Twist) -> None:
        action = np.array([
            msg.linear.x, msg.linear.y, msg.angular.z
        ], dtype=np.float32)
        with self._lock:
            self._latest.action = action

    def _sample(self) -> None:
        if not self._recording:
            return
        with self._lock:
            t = Transition(
                obs_image=self._latest.obs_image.copy() if self._latest.obs_image is not None else None,
                obs_scan=self._latest.obs_scan.copy() if self._latest.obs_scan is not None else None,
                obs_odom=self._latest.obs_odom.copy() if self._latest.obs_odom is not None else None,
                action=self._latest.action.copy() if self._latest.action is not None else None,
                timestamp=time.time(),
            )
        if t.obs_odom is not None and t.action is not None:
            self._episode.append(t)

    def _record_cmd_cb(self, msg) -> None:
        cmd = msg.data.strip().lower()
        if cmd == "start":
            self._episode = []
            self._recording = True
            self.get_logger().info("Recording started")
        elif cmd == "stop":
            self._recording = False
            self._save_episode()

    def _save_episode(self) -> None:
        if not self._episode:
            self.get_logger().warning("No transitions recorded — skipping save")
            return
        self._episode_count += 1
        path = os.path.join(self._output_dir, f"episode_{self._episode_count:04d}.hdf5")
        with h5py.File(path, "w") as f:
            f.create_dataset("obs/odom",  data=np.stack([t.obs_odom  for t in self._episode]))
            f.create_dataset("action",    data=np.stack([t.action    for t in self._episode]))
            f.create_dataset("timestamp", data=np.array([t.timestamp for t in self._episode]))
            if self._episode[0].obs_image is not None:
                f.create_dataset("obs/image", data=np.stack([t.obs_image for t in self._episode]),
                                 compression="gzip", compression_opts=4)
            if self._episode[0].obs_scan is not None:
                f.create_dataset("obs/scan", data=np.stack([t.obs_scan for t in self._episode]))
        self.get_logger().info(
            f"Saved episode {self._episode_count} ({len(self._episode)} transitions) → {path}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = DemoCollector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

---

### DAgger Iterative Improvement Loop

Full DAgger loop that alternates between running the student policy on the real (or simulated) robot, querying an expert for corrections, retraining, and evaluating improvement.

```python
"""
dagger_loop.py — DAgger iterative policy improvement for navigation.

Requires:
  pip install imitation stable-baselines3 gymnasium
"""
import numpy as np
import torch
import gymnasium as gym
from imitation.algorithms import dagger
from imitation.data import rollout
from imitation.data.wrappers import RolloutInfoWrapper
from imitation.policies.serialize import load_policy
from stable_baselines3 import BC
from stable_baselines3.common.vec_env import DummyVecEnv


class ExpertPolicy:
    """Wraps a hand-coded or pre-trained expert for DAgger queries.

    Args:
        env: gymnasium environment (used for action space info)
    """

    def __init__(self, env: gym.Env):
        self._env = env

    def predict(self, obs: np.ndarray, state=None, deterministic: bool = True):
        """Return expert action for the given observation.

        Replace this with your actual expert: a human operator via
        joystick, a classical planner, or a privileged simulation policy.
        """
        # Example: simple proportional navigation to goal
        goal_dist = np.linalg.norm(obs[:2])      # Assume obs[0:2] = [dx, dy]
        goal_angle = np.arctan2(obs[1], obs[0])
        vx = np.clip(goal_dist * 0.5, -1.0, 1.0)
        vyaw = np.clip(goal_angle * 1.0, -2.0, 2.0)
        action = np.array([vx, 0.0, vyaw], dtype=np.float32)
        return action, state


def run_dagger(
    env_id: str = "NavEnv-v0",
    n_iterations: int = 10,
    episodes_per_iter: int = 5,
    train_epochs_per_iter: int = 20,
    beta_start: float = 1.0,    # Initially follow expert 100%
    beta_decay: float = 0.9,    # Each iter: more student, less expert
) -> torch.nn.Module:
    """Run the DAgger algorithm and return the trained policy.

    Args:
        env_id: gymnasium environment ID
        n_iterations: number of DAgger iterations
        episodes_per_iter: rollout episodes per iteration
        train_epochs_per_iter: BC training epochs after each data collection
        beta_start: initial expert mixing probability
        beta_decay: multiplicative decay of beta per iteration
    """
    env = DummyVecEnv([lambda: RolloutInfoWrapper(gym.make(env_id))])
    obs_dim = env.observation_space.shape[0]
    act_dim = env.action_space.shape[0]

    # Initialise student policy
    from orbibot_agent.learning.bc_model import BCModel  # your BCModel from Core Concepts
    student = BCModel(obs_dim, act_dim)
    optimizer = torch.optim.Adam(student.parameters(), lr=3e-4)
    criterion = torch.nn.MSELoss()

    expert = ExpertPolicy(env)
    dataset: list[tuple[np.ndarray, np.ndarray]] = []
    beta = beta_start

    for iteration in range(n_iterations):
        print(f"\n--- DAgger iteration {iteration + 1}/{n_iterations}  beta={beta:.3f} ---")

        # 1. Collect rollouts: follow student with probability (1 - beta),
        #    follow expert with probability beta
        new_pairs: list[tuple[np.ndarray, np.ndarray]] = []
        obs_batch = env.reset()
        for _ in range(episodes_per_iter * 200):   # 200 steps per episode max
            with torch.no_grad():
                student_action = student(torch.FloatTensor(obs_batch)).numpy()
            expert_action, _ = expert.predict(obs_batch[0])

            # Mix: use expert with probability beta
            if np.random.rand() < beta:
                action = expert_action[np.newaxis]
            else:
                action = student_action

            # Always label with the expert action (DAgger key insight)
            new_pairs.append((obs_batch[0].copy(), expert_action.copy()))

            obs_batch, _, done, _ = env.step(action)
            if done[0]:
                obs_batch = env.reset()

        dataset.extend(new_pairs)
        print(f"  Dataset size: {len(dataset)} transitions")

        # 2. Retrain student on all aggregated data
        obs_arr = torch.FloatTensor(np.array([d[0] for d in dataset]))
        act_arr = torch.FloatTensor(np.array([d[1] for d in dataset]))
        for epoch in range(train_epochs_per_iter):
            pred = student(obs_arr)
            loss = criterion(pred, act_arr)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        print(f"  Training loss after retraining: {loss.item():.5f}")

        # 3. Evaluate student (pure student, no expert mixing)
        success = _evaluate_policy(student, env, n_episodes=5)
        print(f"  Student success rate: {success:.0%}")

        beta *= beta_decay  # Reduce expert mixing

    return student


def _evaluate_policy(policy, env, n_episodes: int = 10) -> float:
    """Run n_episodes with the student policy and return success rate."""
    successes = 0
    for _ in range(n_episodes):
        obs = env.reset()
        for _ in range(300):
            with torch.no_grad():
                action = policy(torch.FloatTensor(obs)).numpy()
            obs, reward, done, info = env.step(action)
            if done[0]:
                successes += info[0].get("success", False)
                break
    return successes / n_episodes
```

---

### Reward Shaping for Navigation

Practical reward functions for mobile robot navigation tasks, covering both potential-based shaping (which preserves the optimal policy) and multi-component dense rewards.

```python
"""
navigation_rewards.py — Reward components for mobile robot navigation RL training.

Compatible with stable-baselines3 custom environments.
"""
import math
import numpy as np


class NavigationRewardShaper:
    """Composite reward shaper for wheeled robot navigation.

    All rewards are additive; weights control their relative importance.
    Use potential_based_shaping() when you need convergence guarantees
    (Ng et al., 1999 shows it preserves the optimal policy).

    Args:
        goal_threshold_m: distance (m) within which task is considered done
        collision_threshold_m: distance (m) to nearest obstacle triggering penalty
        gamma: RL discount factor (used in potential-based shaping)
    """

    def __init__(
        self,
        goal_threshold_m: float = 0.2,
        collision_threshold_m: float = 0.3,
        gamma: float = 0.99,
    ):
        self._goal_thresh = goal_threshold_m
        self._collision_thresh = collision_threshold_m
        self._gamma = gamma

    # ------------------------------------------------------------------
    def compute(self, state: dict, action: np.ndarray, next_state: dict) -> float:
        """Compute total shaped reward for a (s, a, s') transition.

        Args:
            state: dict with keys: robot_pos (2,), goal_pos (2,),
                   scan_ranges (N,), heading_error (rad), velocity (m/s)
            action: [vx, vy, vyaw]
            next_state: same keys as state

        Returns:
            Shaped scalar reward.
        """
        reward = 0.0

        # --- Terminal rewards (large, unweighted) ---
        dist_to_goal = np.linalg.norm(next_state["robot_pos"] - next_state["goal_pos"])
        if dist_to_goal < self._goal_thresh:
            return 100.0   # Goal reached — end episode

        min_obstacle_dist = np.min(next_state["scan_ranges"])
        if min_obstacle_dist < self._collision_thresh:
            return -50.0   # Collision — end episode

        # --- Dense shaping terms ---
        reward += self._progress_reward(state, next_state)
        reward += self._heading_reward(next_state)
        reward += self._obstacle_clearance_reward(next_state)
        reward += self._action_smoothness_penalty(state, action)
        reward += self._time_penalty()

        return float(reward)

    # ------------------------------------------------------------------
    def _progress_reward(self, state: dict, next_state: dict) -> float:
        """Reward proportional to reduction in distance to goal.

        This is equivalent to potential-based shaping with Φ(s) = -dist_to_goal.
        """
        prev_dist = np.linalg.norm(state["robot_pos"] - state["goal_pos"])
        curr_dist = np.linalg.norm(next_state["robot_pos"] - next_state["goal_pos"])
        # Scale: 1 reward point per metre of progress
        return float((prev_dist - curr_dist) * 10.0)

    def _heading_reward(self, next_state: dict) -> float:
        """Reward for facing the goal (+1 when aligned, 0 when perpendicular)."""
        alignment = math.cos(next_state["heading_error"])
        return float(alignment * 0.3)

    def _obstacle_clearance_reward(self, next_state: dict) -> float:
        """Small reward for maintaining safe distance from obstacles."""
        min_dist = np.min(next_state["scan_ranges"])
        safe_dist = 0.8  # metres
        if min_dist < safe_dist:
            # Linear penalty that reaches -2 at the collision threshold
            return float(-2.0 * (safe_dist - min_dist) / safe_dist)
        return 0.0

    def _action_smoothness_penalty(self, state: dict, action: np.ndarray) -> float:
        """Penalise large velocity changes (jerk) to encourage smooth motion."""
        prev_action = state.get("prev_action", np.zeros_like(action))
        jerk = np.linalg.norm(action - prev_action)
        return float(-0.05 * jerk)

    def _time_penalty(self) -> float:
        """Small per-step penalty to encourage reaching the goal quickly."""
        return -0.01


class SparseWithShapingWrapper(gym.Wrapper):
    """Gymnasium wrapper that replaces the base env's reward with shaped rewards.

    Usage
    -----
    env = SparseWithShapingWrapper(gym.make("NavEnv-v0"))
    model = PPO("MlpPolicy", env)
    model.learn(1_000_000)
    """

    def __init__(self, env: gym.Env):
        super().__init__(env)
        self._shaper = NavigationRewardShaper()
        self._prev_obs = None

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._prev_obs = obs
        return obs, info

    def step(self, action):
        obs, _base_reward, terminated, truncated, info = self.env.step(action)
        state = self._obs_to_state_dict(self._prev_obs)
        next_state = self._obs_to_state_dict(obs)
        shaped_reward = self._shaper.compute(state, action, next_state)
        self._prev_obs = obs
        return obs, shaped_reward, terminated, truncated, info

    def _obs_to_state_dict(self, obs: np.ndarray) -> dict:
        """Convert flat observation vector to state dict expected by shaper."""
        return {
            "robot_pos":     obs[0:2],
            "goal_pos":      obs[2:4],
            "heading_error": float(obs[4]),
            "scan_ranges":   obs[5:],
            "prev_action":   np.zeros(3),
        }
```

---

### Policy Evaluation and Deployment

Evaluate a trained policy across multiple test scenarios and export it for inference on-robot.

```python
"""
policy_eval_deploy.py — Evaluation suite and ONNX export for learned policies.

Usage
-----
# Evaluate
python policy_eval_deploy.py --model ppo_nav.zip --env NavEnv-v0 --n_episodes 100

# Export to ONNX for edge deployment
python policy_eval_deploy.py --model ppo_nav.zip --export ppo_nav.onnx
"""
import argparse
import json
import time
from pathlib import Path

import numpy as np
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym


class PolicyEvaluator:
    """Comprehensive evaluation of a trained SB3 policy.

    Computes mean reward, success rate, average episode length,
    and per-scenario breakdown.
    """

    def __init__(self, model_path: str, env_id: str):
        self._model = PPO.load(model_path)
        self._env_id = env_id

    def evaluate(
        self,
        n_episodes: int = 100,
        render: bool = False,
        seed: int = 42,
    ) -> dict:
        """Run full evaluation and return metrics dict."""
        env = DummyVecEnv([lambda: gym.make(self._env_id, render_mode="human" if render else None)])

        mean_reward, std_reward = evaluate_policy(
            self._model,
            env,
            n_eval_episodes=n_episodes,
            deterministic=True,
        )

        # Custom metrics: success rate, episode length
        successes = 0
        episode_lengths = []
        for ep in range(n_episodes):
            obs = env.reset()
            done = False
            length = 0
            while not done:
                action, _ = self._model.predict(obs, deterministic=True)
                obs, _, done_arr, info = env.step(action)
                done = done_arr[0]
                length += 1
            successes += info[0].get("success", False)
            episode_lengths.append(length)

        metrics = {
            "mean_reward": float(mean_reward),
            "std_reward": float(std_reward),
            "success_rate": successes / n_episodes,
            "mean_episode_length": float(np.mean(episode_lengths)),
            "n_episodes": n_episodes,
        }
        return metrics

    def export_onnx(self, output_path: str, obs_dim: int) -> None:
        """Export policy network to ONNX for edge inference.

        The exported model accepts a float32 tensor of shape (1, obs_dim)
        and outputs a float32 tensor of shape (1, action_dim).
        """
        policy_net = self._model.policy
        policy_net.eval()

        dummy_input = torch.zeros(1, obs_dim)
        torch.onnx.export(
            policy_net,
            dummy_input,
            output_path,
            input_names=["observation"],
            output_names=["action"],
            dynamic_axes={"observation": {0: "batch_size"}, "action": {0: "batch_size"}},
            opset_version=17,
        )
        print(f"Exported ONNX model to {output_path}")


class ONNXPolicyNode:
    """Lightweight ONNX inference for on-robot deployment (no SB3 dependency).

    Args:
        onnx_path: path to exported ONNX model
        action_scale: multiply raw network output by this factor
    """

    def __init__(self, onnx_path: str, action_scale: float = 1.0):
        import onnxruntime as ort
        self._session = ort.InferenceSession(
            onnx_path,
            providers=["CPUExecutionProvider"],
        )
        self._input_name = self._session.get_inputs()[0].name
        self._action_scale = action_scale

    def predict(self, obs: np.ndarray) -> np.ndarray:
        """Run inference. obs shape: (obs_dim,) or (1, obs_dim)."""
        if obs.ndim == 1:
            obs = obs[np.newaxis]
        result = self._session.run(None, {self._input_name: obs.astype(np.float32)})
        return result[0][0] * self._action_scale


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--env", default="NavEnv-v0")
    parser.add_argument("--n_episodes", type=int, default=100)
    parser.add_argument("--export", default=None, help="ONNX output path")
    args = parser.parse_args()

    evaluator = PolicyEvaluator(args.model, args.env)
    metrics = evaluator.evaluate(n_episodes=args.n_episodes)
    print(json.dumps(metrics, indent=2))

    if args.export:
        obs_dim = gym.make(args.env).observation_space.shape[0]
        evaluator.export_onnx(args.export, obs_dim)
```

---

## Anti-Patterns

### ❌ Sparse rewards without shaping
Only rewarding final success makes learning extremely slow.

**What happens:** No learning signal, random exploration fails.

### ✅ Dense, shaped rewards
```python
reward = -distance + alignment_bonus + progress_bonus - action_penalty
```

---

### ❌ Distribution mismatch in BC
Training on expert data only, testing on student distribution.

**What happens:** Compounding errors — small deviations lead to states never seen in training.

### ✅ Use DAgger or noise injection

```python
# Inject Gaussian noise into expert observations during data collection
# so the policy learns to recover from near-expert states
noise_std = 0.05  # Tune per task
noisy_obs = expert_obs + np.random.normal(0, noise_std, expert_obs.shape)
dataset.append((noisy_obs, expert_action))
```

---

### ❌ Training on raw pixel observations without normalisation

```python
# WRONG: pixel values in [0, 255] cause gradient instability
obs = np.array(image, dtype=np.float32)  # Values 0–255
model = BCModel(obs_dim=128*128*3, ...)
```

### ✅ Normalise observations before feeding to the network

```python
# Normalise pixels to [0, 1] and centre around the dataset mean
obs = np.array(image, dtype=np.float32) / 255.0
obs = (obs - obs_mean) / (obs_std + 1e-8)
```

---

### ❌ Reusing the same random seed for all evaluation episodes

```python
# WRONG: every episode starts in the same position — you only measure
# one scenario, not generalisation
for _ in range(100):
    env.reset(seed=42)   # Always the same start state
    ...
```

### ✅ Use different seeds and report mean ± std

```python
results = []
for seed in range(100):
    obs, _ = env.reset(seed=seed)
    # ... run episode ...
    results.append(episode_return)
print(f"Mean: {np.mean(results):.2f} ± {np.std(results):.2f}")
```

---

### ❌ Ignoring action limits at deployment time

```python
# WRONG: the policy may output values outside the physical limits
action, _ = model.predict(obs)
robot.send_velocity(action)  # Could command vx=5 m/s on a 1 m/s robot
```

### ✅ Clip actions to physical limits before sending

```python
MAX_LINEAR = 0.5   # m/s — match hardware_params.yaml
MAX_ANGULAR = 1.9  # rad/s

action, _ = model.predict(obs, deterministic=True)
action[0] = np.clip(action[0], -MAX_LINEAR, MAX_LINEAR)   # vx
action[1] = np.clip(action[1], -MAX_LINEAR, MAX_LINEAR)   # vy
action[2] = np.clip(action[2], -MAX_ANGULAR, MAX_ANGULAR) # vyaw
robot.send_velocity(action)
```

---

## Configuration Reference

| Algorithm | Data Needed | Sample Efficiency | Best For |
|-----------|-------------|-------------------|----------|
| Behavior Cloning | Expert demos only | High (offline) | Simple tasks |
| DAgger | Expert queries | Medium | Distribution shift |
| PPO | None | Low (online) | Complex dynamics |
| SAC | None | Medium (online) | Continuous control |
| VLA | Internet + robot data | High (pretrained) | Language instruction |

### Behavior Cloning Hyperparameters

| Parameter | Type | Recommended | Description |
|---|---|---|---|
| `learning_rate` | float | 3e-4 | Adam learning rate |
| `batch_size` | int | 32–256 | Mini-batch size for training |
| `hidden_dim` | int | 256–512 | Hidden layer width |
| `n_epochs` | int | 50–200 | Training epochs over dataset |
| `obs_noise_std` | float | 0.01–0.1 | Noise added to observations during collection |
| `train_val_split` | float | 0.8 | Fraction of demos used for training |

### DAgger Hyperparameters

| Parameter | Type | Recommended | Description |
|---|---|---|---|
| `n_iterations` | int | 5–20 | Number of data-collection + retrain cycles |
| `episodes_per_iter` | int | 5–20 | Rollout episodes per iteration |
| `beta_start` | float | 1.0 | Initial expert mixing probability |
| `beta_decay` | float | 0.8–0.95 | Multiplicative decay of beta per iteration |
| `train_epochs_per_iter` | int | 10–50 | BC epochs after each data collection round |

### PPO Hyperparameters (SB3 defaults)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `learning_rate` | float | 3e-4 | Adam learning rate |
| `n_steps` | int | 2048 | Rollout buffer size |
| `batch_size` | int | 64 | SGD mini-batch size |
| `n_epochs` | int | 10 | Epochs per policy update |
| `gamma` | float | 0.99 | Discount factor |
| `gae_lambda` | float | 0.95 | GAE lambda |
| `clip_range` | float | 0.2 | PPO clip parameter |

---

## Troubleshooting

| Symptom | Cause | Solution |
|---|---|---|
| BC policy fails at deployment but performs well in evaluation | Distribution shift — the policy encounters states not seen in demos | Collect more diverse demonstrations; use DAgger to close the loop; add Gaussian noise to observations during collection |
| RL not learning after 1M steps | Poor reward shaping — agent gets no signal | Add dense progress rewards (distance reduction); verify reward is non-zero on random rollouts with `env.step(env.action_space.sample())` |
| Training loss decreases but success rate stays at 0% | Model memorises demo actions but cannot generalise to new start positions | Check that observations include goal-relative coordinates, not absolute; add data augmentation (random start positions) |
| Unstable RL training — policy collapses after initial improvement | Learning rate too high or reward scale too large | Reduce LR by 5×; normalise rewards to zero mean / unit variance using `VecNormalize` wrapper from SB3 |
| DAgger beta reaches 0 but policy is still worse than expert | Too few DAgger iterations or expert is inconsistent | Increase `n_iterations`; verify expert actions are deterministic for the same observation |
| ONNX export works but inference on robot gives wrong actions | Action output scale differs between SB3 and ONNX session | Check whether SB3 applies `action_scale` internally; apply the same scaling after ONNX inference; verify observation normalisation matches training |
| Simulation-trained policy fails on real robot | Reality gap — dynamics, sensor noise, delays differ | Apply domain randomisation in simulation (add noise to physics, actuator delays); fine-tune on small real-robot dataset with BC |

---

## Workflow Integration

This skill connects to the following skills in the robot development lifecycle:

- **`gazebo`** — train RL policies in simulation before real-robot deployment; use `gymnasium` wrappers around Gazebo environments for SB3 compatibility; randomise physics parameters (`sim-to-real`) to close the reality gap.
- **`sim-to-real`** — after training in Gazebo, apply domain randomisation (sensor noise, actuator delays, floor friction) and fine-tune with a small set of real demonstrations collected via the DemoCollector node above.
- **`edge-ml-deployment`** — export trained policies to ONNX with `PolicyEvaluator.export_onnx()`, then quantise and deploy using TensorRT or ONNX Runtime on the Raspberry Pi 5 or Jetson; wrap the ONNX session in `ONNXPolicyNode` for ROS 2 integration.
- **`sensor-fusion-slam`** — define the observation space using EKF-filtered odometry (`/odometry/filtered`) and LiDAR scans; fused observations reduce noise and improve policy generalisation compared to raw sensor readings.
- **`deployment-fleet`** — publish policy inference latency and action magnitude as diagnostics; alert if inference exceeds 50 ms (would miss a 20 Hz control loop).
- **`safety-systems`** — wrap the learned policy's action output in the safety FSM; if the policy commands a velocity that would violate workspace limits or trigger a proximity stop, the safety layer clips or overrides it before sending to the motor driver.

### Typical Integration Sequence

```
1. Collect expert demonstrations on robot using DemoCollector node.
   ros2 topic pub /record std_msgs/String "data: 'start'"
   [teleoperate robot]
   ros2 topic pub /record std_msgs/String "data: 'stop'"

2. Train initial BC policy offline:
   python train_bc.py --demos /data/demos --output bc_policy.pt

3. Run DAgger in simulation (Gazebo) to close distribution shift:
   python dagger_loop.py --env OrbiNavGazebo-v0 --n_iterations 10

4. Evaluate in simulation across 100 random scenarios:
   python policy_eval_deploy.py --model ppo_nav.zip --n_episodes 100

5. Export to ONNX for edge deployment:
   python policy_eval_deploy.py --model ppo_nav.zip --export nav_policy.onnx

6. Deploy via ONNXPolicyNode in the ROS 2 stack:
   ros2 run orbibot_agent learned_policy_node --ros-args -p model:=nav_policy.onnx

7. Monitor via deployment-fleet; safety-systems provides velocity clipping backstop.
```

---

## Changelog

### v1.0.0 (2026-03-07)
- Initial release covering BC, DAgger, RL, reward shaping