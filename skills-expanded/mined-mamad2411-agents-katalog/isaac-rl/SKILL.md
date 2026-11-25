---
name: isaac-rl
description: >
  Expert guidance for NVIDIA Isaac Sim/Lab and reinforcement learning for robotics.
  Use this skill whenever the user is working with: Isaac Sim, Isaac Lab, Omniverse,
  USD, Universal Scene Description, reinforcement learning, RL, PPO, SAC, TD3,
  reward function, reward design, observation space, action space, policy,
  policy network, value function, critic network, actor-critic, advantage estimation,
  domain randomization, curriculum learning, sim-to-real, sim2real, transfer learning,
  humanoid, bipedal, locomotion, walking, running, standing, balance,
  Unitree, Unitree G1, Unitree Go2, unitree_sdk2, unitree_ros2,
  training loop, training curve, reward shaping, reward engineering,
  gymnasium, gym environment, vectorized environment, parallel environment,
  Isaac Gym, PhysX, GPU simulation, GPU-accelerated simulation,
  rsl_rl, rl_games, skrl, stable-baselines3,
  joint position control, joint velocity control, torque control, PD control,
  MDP, Markov decision process, episode, rollout, trajectory,
  TensorBoard, training metrics, convergence, hyperparameter tuning,
  URDF, MJCF, robot model, articulation, rigid body,
  terrain generation, rough terrain, stairs, slopes,
  actuator network, actuator model, motor dynamics,
  system identification, parameter estimation,
  policy deployment, policy export, ONNX, TensorRT,
  the robot keeps falling, training not converging, reward hacking,
  policy doesn't transfer, sim-to-real gap, robot walks weird,
  training is slow, need more GPUs, reward is stuck,
  how to design rewards, what observations to use.
---

# Isaac Sim/Lab & Reinforcement Learning

> **Quick navigation**
> - Isaac Sim installation, USD scenes, sensors, headless mode --> `references/isaac-sim-basics.md`
> - Isaac Lab environments, observations, actions, rewards --> `references/isaac-lab-envs.md`
> - PPO training, hyperparameters, monitoring, curriculum --> `references/rl-training.md`
> - Physics/sensor/terrain randomization --> `references/domain-randomization.md`
> - Unitree G1 hardware, SDK, Isaac Lab models --> `references/unitree-g1.md`
> - Sim-to-real transfer, deployment, safety --> `references/sim-to-real.md`

---

## RL Core Concepts

### The Core Loop: Markov Decision Process (MDP)

| RL Concept | What It Is |
|---|---|
| **Environment** | The simulator (Isaac Sim). It holds the world state and responds to actions. |
| **Agent (Policy)** | A neural network that decides what to do. It sends actions and receives observations + reward. |
| **Observation** | What the agent sees: joint angles, velocities, IMU data, foot contacts. A vector of floats. |
| **Action** | What the agent does: target joint positions, velocities, or torques. Also a vector of floats. |
| **Reward** | A single number telling the agent how good its last action was. Positive = good, negative = bad. |
| **Episode** | One attempt from start to termination (robot falls, timeout reached). |
| **Policy** | The learned function mapping observations to actions. Starts random, gets better through training. |
| **Training** | Millions of episodes where the policy is gradually improved based on which actions led to higher rewards. |

The **Markov Decision Process (MDP)** is the formal framework: at each timestep, the agent
observes state `s`, takes action `a`, receives reward `r`, and transitions to new state `s'`.
The goal is to learn a policy that maximizes cumulative reward over an episode.

```
 +----------+     action      +--------------+
 |  Agent   | -------------> |  Environment |
 |  (Policy)|                | (Isaac Sim)  |
 |          | <------------- |              |
 +----------+   observation  +--------------+
                + reward
```

### Why RL Is Hard (Honest Assessment)

RL is not like supervised learning. In supervised learning, you have labeled data and clear
loss functions. In RL:

- **No labels.** The agent must discover good behavior through trial and error.
- **Sparse signal.** The reward might be zero for thousands of steps before something useful happens.
- **Credit assignment.** If the robot falls at step 500, which of the 500 actions caused it?
- **Non-stationary.** The data distribution changes as the policy improves.
- **Reward design is an art.** A bad reward function trains a bad policy, even if training "succeeds."

Humanoid locomotion is among the hardest RL tasks because bipedal balance is inherently unstable
(unlike wheeled robots), the action space is high-dimensional (20+ joints), and small errors
compound quickly (one bad joint command and the robot falls).

Expect: weeks of iteration on reward functions, hyperparameters, and domain randomization before
getting a walking policy that transfers to real hardware.

---

## Isaac Ecosystem Overview

NVIDIA has several overlapping tools. Here is what each one does and which to use.

### Isaac Sim vs Isaac Lab vs Isaac Gym

| Tool | What It Is | Status | Use When |
|---|---|---|---|
| **Isaac Sim** | Full robot simulator built on Omniverse. Renders photorealistic scenes, simulates physics (PhysX 5), supports cameras, LiDAR, IMU. | Active, primary simulator | You need sensor simulation (camera, LiDAR), photorealistic rendering, or complex scene building. |
| **Isaac Lab** | RL framework built on top of Isaac Sim. Provides environment abstractions, vectorized simulation, reward/observation APIs. Successor to Isaac Gym. | Active, primary RL framework | You are training RL policies. This is your main tool. |
| **Isaac Gym** (legacy) | Standalone GPU-accelerated RL environment. Pioneered massively parallel simulation. | Deprecated, replaced by Isaac Lab | Do not start new projects with Isaac Gym. Migrate to Isaac Lab. |
| **Omniverse** | Platform layer providing USD scene management, RTX rendering, and extension system. Isaac Sim is an Omniverse app. | Active, underlying platform | You need to create custom extensions or integrate with other Omniverse tools. |

**Bottom line:** Use **Isaac Lab** for RL training. It runs on top of Isaac Sim
and gives you everything needed for humanoid locomotion training.

### The Software Stack

```
+------------------------------------------+
|            Your Training Script           |
|   (Python: env config, reward, train)     |
+------------------------------------------+
|              Isaac Lab                     |
|   (Environment API, vectorized envs,      |
|    reward/obs/action abstractions)         |
+------------------------------------------+
|              Isaac Sim                     |
|   (Omniverse, USD scenes, PhysX 5,        |
|    sensor simulation, rendering)           |
+------------------------------------------+
|           NVIDIA GPU + Driver              |
|   (CUDA, PhysX GPU, RTX for rendering)    |
+------------------------------------------+
```

---

## Which RL Algorithm?

For robotics locomotion, three algorithms dominate. Here is when to use each.

| Algorithm | Type | Best For | Pros | Cons | Use This When |
|---|---|---|---|---|---|
| **PPO** | On-policy, actor-critic | Locomotion, manipulation, most robotics tasks | Stable, forgiving hyperparameters, works well with parallel envs | Sample-inefficient (needs millions of steps), on-policy = can't reuse old data | **Default choice.** Start here. Most Isaac Lab examples use PPO. |
| **SAC** | Off-policy, actor-critic | Tasks requiring sample efficiency, continuous control | Sample-efficient, automatic entropy tuning, reuses past experience | More hyperparameters to tune, can be unstable with parallel envs | You have limited compute or need faster iteration. Less common for locomotion. |
| **TD3** | Off-policy, actor-critic | Continuous control, when SAC's entropy is problematic | Addresses overestimation bias, deterministic policy | Requires careful tuning, less explored for humanoid tasks | SAC doesn't work for your specific task. Rare choice for locomotion. |

**Recommendation for Unitree G1 locomotion: Start with PPO.** The Isaac Lab ecosystem, research
papers, and community examples overwhelmingly use PPO for humanoid walking. Switch to SAC only
if you have a specific reason (limited GPU time, need sample efficiency).

---

## Training Workflow Overview

This is the end-to-end workflow for training a locomotion policy:

```
1. ENVIRONMENT SETUP
   Define observation space, action space, scene
   "What does the robot see? What can it do?"
        |
        v
2. REWARD DESIGN
   Define reward components and weights
   "What behavior do we want to encourage/discourage?"
        |
        v
3. DOMAIN RANDOMIZATION
   Randomize physics, sensors, terrain
   "Make training harder so the policy generalizes"
        |
        v
4. TRAINING
   Run PPO for millions of steps across thousands of parallel envs
   "Let the policy learn through trial and error"
        |
        v
5. EVALUATION
   Test trained policy in simulation
   "Does it walk? Does it handle perturbations?"
        |
        v
6. ITERATION
   Adjust rewards, randomization, hyperparameters
   "Training rarely works on the first try"
        |
        v
7. SIM-TO-REAL TRANSFER
   Deploy to Unitree G1 hardware
   "Does the learned behavior work on the real robot?"
```

Each step has its own reference file with detailed guidance. The most time will be spent
in the **Reward Design <--> Training <--> Evaluation** loop (steps 2-6).

---

## Common RL Failure Diagnosis

When training goes wrong (it will), use this table to diagnose the issue.

| Symptom | Likely Cause | First Action |
|---|---|---|
| Reward stays flat at zero | Reward function is too sparse; agent never accidentally gets reward | Add dense reward shaping (e.g., reward for moving forward even slightly). See `references/rl-training.md` |
| Reward increases then crashes to zero | Learning rate too high; policy updates too aggressive | Reduce learning rate by 2-5x; reduce PPO clip range from 0.2 to 0.1 |
| Reward increases but robot walks weird | Reward hacking: agent found an exploit (e.g., sliding on knees) | Add penalty terms (energy, smoothness, joint limit). See `references/isaac-lab-envs.md` |
| Robot falls immediately every episode | Action scale too large; observation missing critical info (e.g., no IMU) | Check action space scaling; verify observations include orientation and angular velocity |
| Training is extremely slow | Too few parallel environments; GPU underutilized | Increase num_envs (try 4096); check GPU utilization with `nvidia-smi` |
| Policy works in sim, fails on real robot | Sim-to-real gap: physics/sensors differ from reality | Increase domain randomization; add actuator modeling. See `references/sim-to-real.md` |
| Loss is NaN | Observation or reward contains inf/NaN; numerical instability | Add observation clipping; check for division by zero in reward |
| Agent spins in circles | Reward doesn't penalize deviation from heading; reward for velocity but not direction | Add heading reward component or directional velocity reward |
| Robot stands but never walks | Standing is a local optimum (standing = no fall penalty, no negative reward) | Add forward velocity reward that outweighs the safety of standing still |
| Training converges but performance is mediocre | Suboptimal hyperparameters or reward weights | Try curriculum learning: start easy, progressively harder. See `references/rl-training.md` |

---

## GPU Requirements and Cloud Options

RL training for humanoid locomotion is GPU-intensive. Here are practical guidelines.

### Minimum Hardware

| Component | Minimum | Recommended | Notes |
|---|---|---|---|
| GPU | RTX 3070 (8 GB VRAM) | RTX 4090 (24 GB VRAM) | More VRAM = more parallel environments |
| CPU | 8 cores | 16+ cores | Data processing between GPU steps |
| RAM | 32 GB | 64 GB | Isaac Sim is memory-hungry |
| Disk | 50 GB free (SSD) | 100 GB+ NVMe | Isaac Sim installation is ~30 GB |
| OS | Ubuntu 22.04 | Ubuntu 22.04 | Windows works but Linux is primary target |

### Parallel Environments vs VRAM

| VRAM | Approx. Max Envs (Humanoid) | Training Speed |
|---|---|---|
| 8 GB | ~512 | Slow, but usable for initial experiments |
| 12 GB | ~1024 | Reasonable for development |
| 24 GB | ~4096 | Good training speed |
| 48 GB (A6000) | ~8192+ | Fast training, production runs |
| 80 GB (A100/H100) | ~16384+ | Research-grade speed |

### Cloud GPU Options

| Provider | GPU | Approx. Cost/hr | Notes |
|---|---|---|---|
| **Lambda Labs** | A100 80GB | $1.10-2.00 | Cheapest A100s, popular for RL research |
| **Vast.ai** | RTX 4090 / A100 | $0.30-1.50 | Marketplace pricing, variable availability |
| **AWS** | A10G (g5), A100 (p4d) | $1.00-32.00 | Reliable but expensive; p4d instances for serious training |
| **GCP** | A100, H100 | $2.00-8.00 | Good availability; use preemptible for cost savings |
| **Azure** | A100, H100 | $2.00-8.00 | Similar to GCP |
| **RunPod** | RTX 4090 / A100 | $0.40-2.00 | Simple interface, good for spot instances |

**Recommendation:** Start local with whatever NVIDIA GPU you have (even a 3060 works for
small experiments with ~256 envs). Move to cloud (Lambda Labs or Vast.ai) when you need
4096+ environments for serious training runs.

---

## Training Time Estimates (Humanoid Locomotion)

These are rough estimates for training a walking policy from scratch with PPO:

| Envs | GPU | Wall Time to Basic Walking | Wall Time to Robust Walking |
|---|---|---|---|
| 512 | RTX 3070 | 8-16 hours | 24-48 hours |
| 2048 | RTX 4090 | 2-4 hours | 8-16 hours |
| 4096 | RTX 4090 | 1-2 hours | 4-8 hours |
| 4096 | A100 | 30-60 min | 2-4 hours |

"Basic walking" = moves forward without falling. "Robust walking" = handles pushes, terrain,
speed changes. These numbers assume a reasonable reward function and hyperparameters; bad
design can make training take 10x longer or never converge.

---

## Isaac Lab Quick Start (Abridged)

For full details, see the reference files. Here is the minimum to get started:

### 1. Install Isaac Sim + Isaac Lab

```bash
# Install Isaac Sim (via pip, recommended for Isaac Lab)
# For Isaac Sim 4.5 (with Isaac Lab compatibility)
pip install 'isaacsim[all,extscache]==4.5.0' --extra-index-url https://pypi.nvidia.com

# For Isaac Sim 5.x (latest)
pip install 'isaacsim[all]' --extra-index-url https://pypi.nvidia.com

# Clone Isaac Lab
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# Create conda environment and install
./isaaclab.sh --install  # Linux

# Alternative: pip-based installation
pip install isaaclab isaaclab_tasks
```

### 2. Run a Built-in Example

```bash
# Train a humanoid to walk (Isaac Lab built-in task)
cd IsaacLab
python source/standalone/workflows/rsl_rl/train.py \
    --task Isaac-Velocity-Rough-Unitree-G1-v0 \
    --num_envs 4096 \
    --headless
```

### 3. Monitor Training

```bash
# In another terminal
tensorboard --logdir logs/rsl_rl/
# Open http://localhost:6006
```

### 4. Evaluate Trained Policy

```bash
python source/standalone/workflows/rsl_rl/play.py \
    --task Isaac-Velocity-Rough-Unitree-G1-v0 \
    --num_envs 16
```

---

## Project Structure for Custom Tasks

When creating your own locomotion task, organize files like this:

```
my_locomotion/
+-- __init__.py
+-- config/
|   +-- __init__.py
|   +-- g1_walking.py          # Environment config (obs, actions, rewards, scene)
|   +-- g1_walking_ppo.py      # PPO hyperparameters
+-- mdp/
|   +-- __init__.py
|   +-- rewards.py             # Custom reward functions
|   +-- observations.py        # Custom observation functions
|   +-- terminations.py        # Custom termination conditions
+-- train.py                   # Training entry point
+-- play.py                    # Evaluation entry point
+-- export_policy.py           # Export for deployment
```

See `references/isaac-lab-envs.md` for the full environment class structure and
`references/rl-training.md` for training configuration details.

---

## Reward Design Quick Reference

Reward design is the make-or-break skill in RL. Here are battle-tested patterns for
locomotion tasks.

### The Reward Equation

A locomotion reward function is typically a weighted sum of components:

```python
reward = (
    w1 * velocity_tracking      # Are we going where commanded?
    + w2 * alive_bonus           # Are we still standing?
    - w3 * energy_penalty        # Are we wasting energy?
    - w4 * smoothness_penalty    # Are we being jerky?
    - w5 * orientation_penalty   # Are we leaning too much?
)
```

### Reward Design Patterns

| Pattern | When to Use | Example |
|---|---|---|
| **Exponential tracking** | Rewarding velocity/position tracking | `exp(-||v_actual - v_target||^2 / sigma)` |
| **L2 penalty** | Penalizing unwanted quantities | `-||joint_torques||^2` |
| **Threshold bonus** | Rewarding binary conditions | `+0.5 if base_height > 0.6` |
| **Delta penalty** | Penalizing change rate | `-||action_t - action_{t-1}||^2` |
| **Cosine similarity** | Rewarding directional alignment | `dot(velocity, heading) / ||velocity||` |

### Iteration Strategy

1. **Start simple.** Begin with only velocity tracking + alive bonus + energy penalty.
2. **Add penalties one at a time.** When you see a specific bad behavior, add a targeted penalty.
3. **Watch for reward hacking after each change.** The agent will try to exploit the new reward.
4. **Log individual reward components.** Don't just look at total reward -- understand which
   components are driving behavior.
5. **Visual inspection is essential.** Numbers can lie. Watch the robot move in simulation.

---

## Debugging Checklist

When something goes wrong, work through this checklist in order:

### Environment Not Loading

- [ ] Is Isaac Sim installed correctly? Run `python -c "from isaacsim import SimulationApp"`
- [ ] Is Isaac Lab installed? Run `python -c "import isaaclab"`
- [ ] Are GPU drivers up to date? Run `nvidia-smi`
- [ ] Is there enough disk space? Isaac Sim needs ~30 GB free
- [ ] Is the URDF/USD model accessible at the configured path?

### Training Not Starting

- [ ] Is the task registered? Run `python -c "import gymnasium as gym; print([s for s in gym.registry.keys() if 'G1' in s])"`
- [ ] Do observation dimensions match the policy network input?
- [ ] Do action dimensions match the policy network output?
- [ ] Are all reward functions returning tensors of shape `(num_envs,)`?
- [ ] Is `num_envs` small enough for your GPU VRAM?

### Training Started But No Learning

- [ ] Is the reward function correct? Print reward components individually
- [ ] Are observations normalized? Check observation magnitudes (should be roughly [-5, 5])
- [ ] Is the action scale appropriate? Actions of 0.25 rad offset are a good starting point
- [ ] Is the learning rate reasonable? Try 1e-3 first
- [ ] Are there enough environments? Try at least 2048 for stable learning
- [ ] Is the episode length long enough? At least 10 seconds for locomotion

### Policy Learned But Behavior Is Wrong

- [ ] Is there reward hacking? Watch the robot in play mode with 16 envs
- [ ] Are reward weights balanced? No single component should dominate
- [ ] Is there a missing penalty? Common: knee contact, excessive base motion, foot sliding
- [ ] Does the observation include all needed info? Missing projected gravity = can't balance

---

## Key Terminology Quick Reference

| Term | Definition |
|---|---|
| **Articulation** | A robot model with joints in Isaac Sim. The G1 is an articulation with 23 DoF. |
| **DoF** | Degrees of freedom. Number of independent joints the robot can control. |
| **Rollout** | One episode of the agent interacting with the environment. |
| **Trajectory** | The sequence of (state, action, reward) tuples in a rollout. |
| **GAE** | Generalized Advantage Estimation. A technique to reduce variance in policy gradient estimates. |
| **Clip range** | PPO parameter controlling how much the policy can change per update. |
| **Entropy** | Measure of policy randomness. Higher entropy = more exploration. |
| **Curriculum** | Gradually increasing task difficulty during training. |
| **Proprioception** | Sensing the robot's own body state (joint positions, velocities, orientation). No cameras. |
| **Exteroception** | Sensing the external world (cameras, LiDAR). Adds complexity. |

---

## Reference File Index

| File | Read When |
|---|---|
| `references/isaac-sim-basics.md` | Setting up Isaac Sim, creating scenes, understanding USD, configuring physics, sensor simulation, headless mode, cloud GPUs |
| `references/isaac-lab-envs.md` | Designing RL environments, observation/action/reward spaces, vectorized environments, task registration, reset conditions |
| `references/rl-training.md` | Configuring PPO, tuning hyperparameters, monitoring training, curriculum learning, diagnosing training failures, using rsl_rl or rl_games |
| `references/domain-randomization.md` | Physics randomization, sensor noise, terrain generation, actuator modeling, scheduling randomization, building robust policies |
| `references/unitree-g1.md` | G1 hardware specs, unitree_sdk2, control modes, Isaac Lab G1 models, safety, deployment workflow |
| `references/sim-to-real.md` | Sim-to-real gap analysis, domain randomization strategy, system identification, policy export, deployment safety, real-world testing |
