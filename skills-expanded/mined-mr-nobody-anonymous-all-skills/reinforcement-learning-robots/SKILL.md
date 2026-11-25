---
name: reinforcement-learning-robots
description: "Use when training RL policies for robots (locomotion, manipulation, navigation), debugging reward hacking or sim-to-real transfer failures, choosing between scripted and learned control, or setting up Isaac Gym/Lab massively-parallel training. Provides PPO configuration, reward shaping patterns, domain randomization ranges, and safe-RL constraints that work on real hardware."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Reinforcement Learning for Robots

RL on robots is a different discipline from RL on Atari. The state-action space is continuous, episodes are expensive, the simulator never matches reality, and a bad policy can destroy a $50k robot in 200 ms. This skill encodes the workflow that actually ships: **train massively parallel in simulation, shape rewards carefully, randomize the sim until the real world looks like just another sample, and deploy with hard safety layers the policy cannot override.**

## 0. The decision that comes first: should you use RL at all?

RL is the *last* tool, not the first. Use this table before writing a single line of training code.

| Problem | Use RL? | Better alternative |
|---|---|---|
| Pick-and-place, known objects, structured cell | **No** | Scripted motion + standard grasp planner (GPD, Contact-GraspNet for perception only) |
| Quadruped/biped locomotion over rough terrain | **Yes** | This is RL's flagship win (ANYmal, Spot research stacks, Unitree RL controllers) |
| Trajectory tracking on a fixed-base arm | **No** | Inverse dynamics + PID/impedance control. Solved since the 1980s. |
| In-hand reorientation, dexterous manipulation | **Yes** | RL (+ domain randomization) is state of the art (OpenAI Dactyl lineage, LEAP hand work) |
| Drone waypoint flight | **No** | Geometric/SE(3) controller + minimum-snap trajectories |
| Drone agile flight near actuator limits (racing) | **Yes** | RL beats MPC at the edge of the envelope (Swift, 2023) |
| Mobile robot navigation in mapped space | **No** | Nav2 / A* + DWB / MPPI local planner |
| Contact-rich insertion with tight tolerance (<0.5 mm) | **Maybe** | Try impedance control + spiral search first; RL residual on top if that fails |
| Anything with a hard correctness requirement and no recovery (surgical, nuclear) | **No** | Verified classical control. RL gives no guarantees. |

**Rule of thumb:** if a competent engineer can write the controller in two weeks of scripting, the script will be more reliable, more debuggable, and certifiable. RL earns its complexity only when the dynamics are too hard to model (contact, deformables, aerodynamic stall) or the behavior space is too rich to enumerate (recovery from arbitrary pushes).

**Residual RL** is the pragmatic middle: a classical controller provides the baseline action, RL learns a small corrective delta (bounded, e.g. ±10% of actuator range). You keep the safety and sample-efficiency of the script and gain adaptation. Start here for manipulation.

## 1. Why direct RL on real hardware mostly fails

Everyone tries it once. Here is why it fails, so you don't have to rediscover it:

1. **Sample complexity.** PPO needs 10⁷–10⁹ environment steps for locomotion. At real-time (say 50 Hz control), 10⁸ steps = 23 days of *continuous* robot operation, ignoring resets, crashes, and repairs. Isaac Lab does 10⁸ steps in ~1 hour on one RTX 4090 with 4096 parallel envs.
2. **Exploration breaks robots.** Early-training policies output near-random torques. Random torques on a legged robot = falls; on an arm = self-collision and joint-limit slams. Each fall costs reset time and accumulates mechanical wear.
3. **Resets are the hidden cost.** Sim resets are free (`env.reset()`). Real resets need a human or a reset mechanism. Autonomous-reset research exists but adds a second hard problem.
4. **Non-stationarity.** Motors heat up, batteries sag, cables wear. The MDP changes under you mid-training; the learning curve never converges.
5. **No replay of catastrophic states.** The most informative transitions (near-falls) are exactly the ones you can't afford to collect.

Exceptions where real-world RL works: sample-efficient off-policy methods (SAC, REDQ, DroQ) fine-tuning a sim-pretrained policy for <1 hour of data; tasks with cheap automatic resets (in-hand manipulation over a tray); learned residuals with tight bounds. These are fine-tuning regimes, not training-from-scratch regimes.

**Default workflow: sim-first, always.**

## 2. Reference pipeline (sim-first, Isaac Lab + PPO)

```
1. Model the robot          → URDF/MJCF, verify masses & inertias against CAD (±10%)
2. Build the env in Isaac Lab → 2048–8192 parallel envs, GPU PhysX
3. Define obs/action/reward → start from a known-working config (Section 4–5)
4. Train PPO                → rsl_rl or rl_games or skrl; 1–10k iterations
5. Inspect in sim           → look for reward hacking BEFORE transfer
6. Add domain randomization → retrain; policy must stay robust across DR ranges
7. Sim-to-sim transfer test → e.g. Isaac → MuJoCo. If it fails here, real will fail worse
8. Deploy on hardware       → ONNX/TorchScript export, runs inside the RT control loop
   with safety layer        → action clipping, joint-limit shield, e-stop, watchdog
9. (Optional) real fine-tune → off-policy, tiny LR, frozen early layers
```

### Frameworks (2025 state)

- **Isaac Lab** (successor to Isaac Gym Preview / Orbit): GPU-parallel PhysX, the de facto standard for locomotion and increasingly manipulation. Pairs with `rsl_rl` (ETH's lean PPO), `rl_games`, or `skrl`.
- **MuJoCo + MJX (Brax v2 backend)**: JAX-based, also massively parallel, better contact fidelity for manipulation; good as the sim-to-sim validation target.
- **Genesis / ManiSkill 3**: newer GPU-parallel options for manipulation.
- **Stable-Baselines3**: fine for prototyping with ≤16 envs; too slow as the main training stack for robotics. Don't build production locomotion on it.

## 3. PPO is the default. Configuration that works.

PPO wins in robotics not because it's the most sample-efficient (SAC is better per-sample) but because it is *stable under massive parallelism*, tolerant of hyperparameters, and on-policy (no replay buffer staleness when the env count is huge). With 4096 envs, wall-clock beats sample efficiency.

### Starting hyperparameters (locomotion, Isaac Lab / rsl_rl conventions)

```python
# These are the values used (with minor variation) by virtually every
# published quadruped/biped RL result since 2021. Change them last.
num_envs            = 4096
rollout_steps       = 24            # per env per update (24*4096 ≈ 98k transitions/update)
learning_rate       = 1.0e-3        # with adaptive schedule keyed on KL
desired_kl          = 0.01          # adapt LR: halve if KL > 2x target, raise if < 0.5x
gamma               = 0.99          # horizon ≈ 1/(1-γ) = 100 steps; at 50 Hz that is 2 s
gae_lambda          = 0.95
clip_param          = 0.2
entropy_coef        = 0.005         # locomotion; 0.0–0.01. Higher → wasteful gaits
value_loss_coef     = 1.0
num_mini_batches    = 4
num_learning_epochs = 5
max_grad_norm       = 1.0
# Network: MLP [512, 256, 128], ELU activations. Separate actor/critic bodies.
# Policy outputs mean; log_std is a learned state-independent parameter,
# init log_std = 0.0 (std = 1.0 in normalized action space).
```

Key adjustments by domain:
- **Manipulation (sparse-ish rewards, longer horizon):** `gamma = 0.995–0.998`, longer rollouts (32–64), consider asymmetric actor-critic (critic sees privileged state: object pose, friction; actor sees only deployable obs).
- **High-frequency control (>100 Hz):** raise gamma so the effective horizon in *seconds* stays 1.5–3 s. `γ = exp(-dt / horizon_seconds)`. Example: 200 Hz, 2 s horizon → γ = exp(-0.005/2) ≈ 0.9975.
- **If training diverges:** first suspect reward scale (normalize rewards or use a running return normalizer), then observation scale (normalize every obs channel to roughly [-1, 1] or use running mean/std), then LR.

### The math you actually need

PPO clipped objective:

L(θ) = E[ min( r·Â, clip(r, 1−ε, 1+ε)·Â ) ],  r = π_θ(a|s) / π_old(a|s)

What matters in practice:
- **Advantage normalization** (per-batch, zero mean unit std) is not optional. Without it, reward scale leaks into the gradient scale and training is brittle.
- **GAE:** Â_t = Σ (γλ)^k δ_{t+k}, δ_t = r_t + γV(s_{t+1}) − V(s_t). λ=0.95 trades bias/variance; lowering λ (0.9) stabilizes noisy contact-rich tasks at the cost of bias.
- **Bootstrap on timeouts, not terminations.** When an episode ends by *time limit*, the correct target is r + γV(s'); when it ends by *failure* (fall), the target is just r. Conflating these is the single most common silent bug in custom envs — it teaches the policy that surviving to the time limit is equivalent to dying. Isaac Lab's `time_outs` tensor exists exactly for this; rsl_rl handles it if you pass it through.

### Action space design

- Output **target joint positions** for a PD controller, not torques. PD targets give the policy a stable inner loop; torque policies are far harder to train and transfer.
  - `τ = Kp(q_target − q) − Kd·q̇` with Kp/Kd matched to the real actuator gains.
  - Typical quadruped: Kp = 20–40 N·m/rad, Kd = 0.5–1.0. Get the real values from the actuator config and use the same in sim.
- Scale: policy outputs in [-1, 1] (tanh or clipped Gaussian), mapped as `q_target = q_default + action_scale * a`, with `action_scale ≈ 0.25–0.5 rad` for legs. Bigger scale → faster learning, wilder motion.
- Control at 50 Hz policy / 200+ Hz PD inner loop (sim decimation 4 at dt=0.005 is the standard pattern).

## 4. Observation design

Deployable observation vector (quadruped example, all body-frame):

```
base linear velocity        (3)   ← often *removed* for real deployment (hard to estimate);
                                     use a learned estimator or train without it
base angular velocity       (3)   ← from IMU gyro, reliable
projected gravity vector    (3)   ← from IMU orientation; encodes tilt without yaw
commanded velocity          (3)   ← vx, vy, ωz
joint positions − default   (12)
joint velocities            (12)  ← noisy on real hardware; add matching noise in sim
previous action             (12)  ← critical for smoothness; policy sees what it did
```

Rules:
- **Never feed the policy anything you cannot measure on the robot at deploy time.** World-frame position, true contact states, object mass — these go to the *critic only* (asymmetric actor-critic) or to a teacher policy that is later distilled (teacher-student, à la ANYmal "learning by cheating").
- Add observation noise in sim matching real sensor specs: gyro σ≈0.2 rad/s additive, joint pos σ≈0.01 rad, joint vel σ≈1.5 rad/s. If you train without noise, the real policy chatters.
- Stack history (5–50 frames) or use the previous-action channel to let the policy implicitly estimate velocities and contact; for adaptation to varying dynamics, an explicit history encoder (RMA-style: 50-step history → latent) transfers better than a recurrent policy and is easier to debug.

## 5. Reward shaping — the actual art

A robotics reward is always a sum: one **task term** plus many **regularizers**. The task term says *what*; the regularizers say *how* without breaking hardware.

### Sparse vs dense

- Sparse ("+1 at goal") is unbiased but untrainable for most robot tasks — exploration never finds the reward. 
- Dense shaping biases the solution but makes learning possible. The discipline: keep the task term dominant, keep every shaping term *small and justified*, and check final behavior against the sparse criterion ("does it actually reach the goal?"), not against the shaped return.
- Potential-based shaping `F = γΦ(s') − Φ(s)` provably preserves the optimal policy. Distance-to-goal deltas are the common instance: reward `d_prev − d_curr`, not `−d_curr` (the latter rewards merely *existing* close to the goal and can be farmed by hovering).

### Canonical locomotion reward (velocity tracking, weights that work)

```python
# dt = 0.02 (50 Hz). Weights are per-step contributions.
rew_lin_vel  =  1.0  * exp(-|v_cmd_xy - v_xy|^2 / 0.25)   # task: track commanded velocity
rew_ang_vel  =  0.5  * exp(-(w_cmd_z - w_z)^2 / 0.25)     # task: track commanded yaw rate
rew_z_vel    = -2.0  * v_z^2                               # don't bounce
rew_roll_pitch_rate = -0.05 * |w_xy|^2                     # don't wobble
rew_orient   = -5.0  * |gravity_xy|^2                      # stay upright (projected gravity)
rew_torque   = -2e-4 * |tau|^2                             # energy penalty
rew_joint_acc= -2.5e-7 * |qdd|^2                           # smoothness (joint accel)
rew_action_rate = -0.01 * |a_t - a_{t-1}|^2                # smoothness (action delta)
rew_air_time =  1.0  * sum(feet_air_time - 0.5) on touchdown  # encourages real steps,
                                                            # kills the "vibrating shuffle"
rew_collision= -1.0  * (undesired contacts: knees, body)
rew_joint_limits = -10.0 * relu(|q| - 0.95*q_limit)        # soft barrier before hard limit
```

Tuning method: **enable the task term alone first.** Confirm the policy learns *something* (it will be ugly — flailing, sliding). Then add regularizers one at a time, retraining or annealing in, watching that task performance survives. If you start with all penalties on, the policy often learns the local optimum of "stand perfectly still" — the penalties dominate before the task gradient is found. A standard fix is a curriculum on penalty weights (scale from 0.1× to 1× over the first 1000 iterations).

### Common shaping terms and what they're for

| Term | Form | Purpose | Failure if missing |
|---|---|---|---|
| Alive bonus | +c per step (c≈0.5–2) | keeps episodes long enough to learn in early training | instant suicide-reset farming if termination ends penalty streams |
| Energy/torque | −w·‖τ‖² or −w·‖τ·q̇‖ | hardware thermal limits, battery, natural motion | motors saturate and overheat on real robot |
| Action rate | −w·‖a_t − a_{t−1}‖² | actuator bandwidth, gearbox wear | 25 Hz chatter, policy exploits sim's perfect actuators |
| Joint accel | −w·‖q̈‖² | smoothness, transfer | jerky motion that real actuators can't track |
| Self-collision / undesired contact | −w per contact | obvious | robot drags knees, transfer breaks |
| Foot slip | −w·‖v_foot‖² while in contact | real friction ≠ sim friction | gait relies on sliding, fails on real floor |
| Symmetry (mirror loss or reward) | penalize L/R asymmetry | natural gaits, faster learning | limping gaits that "work" in sim |

### Reward hacking — the catalog

The policy is an adversarial optimizer against your reward. Things real teams have shipped into training and regretted:

- **Alive-bonus farming:** alive bonus too large relative to task → robot stands still forever. Fix: alive bonus ≤ achievable task reward per step, or replace with termination penalty (−10 on fall) instead.
- **Early-termination escape:** if total per-step reward is *net negative* (heavy penalties), the optimal policy is to terminate ASAP — the robot learns to dive. Audit: log mean per-step reward; if negative, the death incentive exists.
- **Vibration locomotion:** velocity reward + no air-time/slip terms → robot vibrates feet at high frequency and skates. Looks fine in sim (perfect contacts), zero transfer.
- **Distance-reward hovering:** `−d` reward → robot approaches and orbits the goal forever, never finishing. Use delta-distance or a sparse completion bonus that dominates.
- **Timeout/termination conflation (Section 3):** policy learns time-limit survival = death, behavior degrades near episode end (e.g., robot collapses at t = T−5).
- **Sensor-frame exploit:** reward computed in world frame while obs are body frame → policy finds yaw drift that inflates measured reward.
- **Sim physics exploits:** penetration impulses, contact softness, or solver artifacts harvested for free energy (the classic "hopping on its own foot"). Sim-to-sim validation (Section 7) catches these.

**Debugging methodology:** log every reward term separately, per-iteration mean. The first question on any weird behavior is "which term is paying for this?" — the answer is in the curves. Render rollouts at every 100–500 iterations; reward curves alone lie.

## 6. Domain randomization — making reality in-distribution

The sim-to-real gap is closed not by making sim perfect but by training a policy robust to a *distribution* of sims that contains reality.

### What to randomize, with starting ranges (legged robot)

```python
# Physics (resampled per env per episode)
friction_coeff      : uniform(0.4, 1.25)       # the single most important one
restitution         : uniform(0.0, 0.4)
added_base_mass     : uniform(-1.0, +3.0) kg   # payload variation
com_displacement    : uniform(-0.05, +0.05) m  # per axis
motor_strength      : uniform(0.8, 1.2) x nominal   # torque scaling per joint
Kp, Kd factors      : uniform(0.9, 1.1)        # gain mismatch
joint_friction      : uniform(0.0, 0.05)
# Latency & noise (per step)
action_delay        : 0–20 ms (hold previous action; randomize per episode)
observation_noise   : per-channel Gaussians matching sensor datasheets (Section 4)
# Perturbations
push_robot          : random base velocity impulse 0.5–1.0 m/s every 5–15 s
# Terrain (locomotion)
terrain             : curriculum over flat → rough → stairs → slopes
                      (Isaac Lab terrain generator; difficulty advances per-env on success)
```

Manipulation adds: object mass (±50%), object friction, object scale (±5–10%), grasp-frame offsets, camera extrinsics (±2 cm, ±2°), visual DR (textures, lighting) if the policy consumes pixels.

### How to apply it correctly

- **Randomize at episode reset, not per step** (except noise/delay). The policy should experience a *consistent* world within an episode so it can adapt to it; per-step physics randomization just looks like noise and forces over-conservative behavior.
- **Too much DR is a real failure mode:** the policy becomes uniformly mediocre or refuses to walk fast. Symptoms: sim performance drops >30% when DR is enabled and never recovers. Fix: narrow ranges, or use a curriculum on DR width, or give the policy adaptation capacity (history encoder / RMA latent) so it can *identify* the current world instead of being blind-robust to all of them.
- **Latency randomization is disproportionately important.** A 15 ms unmodeled delay is enough to destabilize a learned biped controller. Measure your real control-loop latency (timestamp at sensor → timestamp at actuator command) and center the DR range on it.
- **Actuator modeling beats actuator randomization for high-performance systems.** ETH's actuator-net approach: collect real actuator data (command → torque, with history), fit a small MLP, use it in sim. For SEAs and quasi-direct-drive with significant dynamics, this is the difference between transfer and no transfer.

## 7. Sim-to-real transfer checklist

Run before touching hardware. Each item has killed a deployment somewhere.

1. **Sim-to-sim transfer:** export the policy, run it in a *different* simulator (Isaac→MuJoCo). Performance drop >20% means the policy exploits engine-specific physics. Fix before proceeding.
2. **System identification basics:** masses/inertias within ±10% of CAD, real PD gains in sim, measured latency in DR range, real joint limits and torque limits (with the *real* torque-speed curve, not just the peak number).
3. **Frequency audit:** policy inference on the target compute (Jetson/NUC) must complete well under the control period. Measure p99, not mean. ONNX Runtime or TensorRT export; no Python GC pauses inside the loop — run inference in the RT process or a pinned thread.
4. **Observation parity test:** record real sensor data while the robot is *suspended/hand-moved*, feed through the policy obs pipeline, compare each channel's range/sign/units against sim logs. Unit and sign errors (deg vs rad, gyro axis flipped) are the #1 first-deploy killer.
5. **Action parity:** command zero-action (a=0 → default pose) on the real robot first. The robot should hold its default stance under the PD law. If it lunges, your scale/offset/ordering is wrong.
6. **Joint-order audit:** sim joint ordering (often alphabetical or kinematic-tree order) vs driver ordering. Permutation bugs produce a robot that "breakdances" instantly.
7. **Gradual deployment:** robot on a stand → gantry/harness → hand-spotted on soft ground → free. Lower commanded velocities first.

## 8. Safety layer — non-negotiable on hardware

The policy is a function approximator; it WILL output something insane eventually (out-of-distribution obs, sensor glitch, NaN). Safety is enforced *outside* the policy, in deterministic code the policy cannot override:

```python
def safety_shield(action, state):
    # 1. NaN/inf guard — first, always
    if not np.all(np.isfinite(action)):
        return DAMPING_MODE          # q_target=q, Kp=0, high Kd: limp safely
    # 2. Action clipping to trained range
    action = np.clip(action, -1.0, 1.0)
    q_target = q_default + ACTION_SCALE * action
    # 3. Joint position limits (with margin) and rate limit
    q_target = np.clip(q_target, q_min + 0.05, q_max - 0.05)
    q_target = np.clip(q_target, prev_target - MAX_DELTA, prev_target + MAX_DELTA)
    # 4. State-trigger fallbacks (checked every cycle)
    if abs(state.roll) > 0.8 or abs(state.pitch) > 0.8:   # rad
        return DAMPING_MODE          # falling: don't fight it, go compliant
    if state.any_joint_temp > TEMP_LIMIT or state.comms_age > 50e-3:
        return DAMPING_MODE          # thermal / watchdog
    return q_target
```

Plus: hardware e-stop (cuts motor power, not software), software watchdog (if the policy process misses 2 cycles → damping), torque limits enforced in the motor driver (the last line of defense), and a velocity-limited "safe mode" for all first runs.

**Safe RL during training** (when some real-world interaction is unavoidable): constrained RL (Lagrangian PPO with a cost critic, budget d: E[Σ c_t] ≤ d) for soft constraints like energy and smoothness; **control-barrier-function (CBF) shields or predictive safety filters** for hard constraints (joint limits, collision) — the filter projects the policy action onto the safe set every step. Reward penalties alone are NOT a safety mechanism; they shift probabilities, they do not bound behavior.

## 9. Minimal Isaac Lab environment skeleton

```python
# Isaac Lab (direct workflow style) — the parts people get wrong, annotated.
from isaaclab.envs import DirectRLEnv, DirectRLEnvCfg

class WalkEnv(DirectRLEnv):
    def _get_observations(self):
        obs = torch.cat([
            self.base_ang_vel * 0.25,            # scale to ~[-1,1]
            self.projected_gravity,
            self.commands * torch.tensor([2.0, 2.0, 0.25], device=self.device),
            (self.joint_pos - self.default_joint_pos) * 1.0,
            self.joint_vel * 0.05,
            self.actions,                         # previous action
        ], dim=-1)
        obs += torch.randn_like(obs) * self.cfg.obs_noise_std   # noise AFTER scaling
        return {"policy": obs}

    def _apply_action(self):
        # action -> PD target; PD runs at sim dt, policy at sim dt * decimation
        self.joint_pos_target = self.default_joint_pos + 0.25 * self.actions

    def _get_dones(self):
        died = self.projected_gravity[:, 2] > -0.5        # tilted past ~60 deg
        time_out = self.episode_length_buf >= self.max_episode_length
        return died, time_out      # KEEP SEPARATE — bootstrapping depends on it

    def _get_rewards(self):
        # compute each term into self.extras["log"][name] for per-term curves
        ...
```

Training run sanity targets (quadruped velocity tracking, 4096 envs, RTX 4090): visible tracking by iteration ~300, decent gait by ~1000, converged by 3000–10000; ~30–100k steps/s throughput. If you're 10× slower, something is on CPU that shouldn't be.

## 10. Debugging methodology (in order)

1. **Can't learn at all (flat reward):** task reward reachable by random exploration? Print reward stats from a random policy — if the task term is identically zero, you need denser shaping or a curriculum. Check obs normalization (any channel with |mean| > 5 or std > 10 is poisoning the MLP).
2. **Learns, then collapses:** KL spike → LR too high or advantage normalization missing; check for NaNs in obs (a single env hitting a physics explosion contaminates the batch — add `torch.nan_to_num` + env reset on non-finite state).
3. **Good return, bad behavior:** reward hacking. Per-term reward logs + rendered rollouts (Section 5).
4. **Good in train sim, bad in test sim:** physics exploit or DR too narrow (Section 6–7).
5. **Good in all sims, bad on robot:** obs parity (units, signs, joint order), latency, actuator model. Record real obs, replay through sim policy, diff the actions against sim rollouts at matched states.
6. **Works on robot, degrades over minutes:** thermal derating (motor torque drops when hot — add motor-strength DR down to 0.7×), battery sag, state estimator drift.

## 11. What good looks like (calibration points)

- Quadruped velocity-tracking locomotion: ~1–4 hours training on one consumer GPU, transfers with friction/mass/latency DR + push perturbations. This is now a solved, reproducible result (Isaac Lab ships working configs for Unitree Go2/A1, ANYmal).
- Bipeds: same recipe, add symmetry loss and longer training (10–20k iterations); much tighter latency/actuator-model requirements.
- Dexterous in-hand reorientation: 10⁹+ steps, heavy DR, teacher-student with privileged object state; expect weeks of iteration, not days.
- If your task is "move arm from A to B avoiding known obstacles" and you're reaching for RL — go back to Section 0. MoveIt will do it this afternoon.
