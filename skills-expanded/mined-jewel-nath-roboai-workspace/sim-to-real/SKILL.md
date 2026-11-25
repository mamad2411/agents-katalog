---
name: sim-to-real
description: Take a controller or learned policy from simulation (MuJoCo, Isaac Sim with Isaac Lab, Gazebo) to a real
  robot - measure the reality gap (actuators, latency, sensor noise, friction, mass, wrong URDF), system identification,
  domain randomisation, transferable observations and actions, staged go/no-go tests with e-stop and rosbag2 MCAP logs.
license: Apache-2.0
metadata:
  sources: []
  evidence: researched
  last_verified: 2026-11-19
---

# Sim-to-real transfer

Lets an agent move a controller or policy from simulation onto a real robot without breaking
either: find what differs, measure it, fit the simulator, randomise what stays uncertain, and test
in stages. Written for MuJoCo 4.0, Isaac Lab 3.0 and ROS 2 Jazzy with Gazebo Harmonic, from their
docs and sources and the papers cited; the recipes were not run.

## When to use

- A policy or controller works in simulation and is about to run on hardware for the first time.
- A transferred policy oscillates, drifts, slips, falls or is sluggish on the robot.
- Setting up training that must transfer: randomisation, noise, observations, actions, control rate.
- Fitting simulator parameters (friction, armature, damping, PD gains, delays, masses) to robot logs.
- Planning the first powered runs: stand, tether, e-stop, limits, logging.

Elsewhere: the URDF itself in [ros2-robot-description](../ros2-robot-description/SKILL.md);
controllers and hardware interfaces in [ros2-control](../ros2-control/SKILL.md); nodes and launch
in [ros2-core](../ros2-core/SKILL.md); Gazebo worlds in [sim-gazebo](../sim-gazebo/SKILL.md);
MuJoCo models in `sim-mujoco`; training algorithms in the later `learn-` skills.

## Quick start

The shortest safe path for a policy that already works in simulation:

1. Export the policy and write `deploy_spec.yaml`: joint order, default pose, action scale,
   observation terms and scales, PD gains, rates, limits ([deployment.md](references/deployment.md#the-deploy-spec)).
2. Run it in a second simulator through the same observation and action code
   ([mujoco.md](references/mujoco.md#sim-to-sim-runner-a-policy-trained-elsewhere-run-in-mujoco)).
3. Robot on a stand, motors powered: test the e-stop, then the sign and zero tests
   ([reality-gap.md](references/reality-gap.md#6-the-robot-description-is-wrong)).
4. Record, then run the policy on the stand:

```bash
ros2 bag record -s mcap -o stand_01 \
  --topics /joint_states /imu/data /policy/observation /policy/action /diagnostics
ros2 run my_robot_policy policy_runner --ros-args -p deploy_spec:=deploy_spec.yaml
```

5. Compare the bag with the same scenario in simulation in [Foxglove](../../wiki/tools/foxglove.md)
   or [PlotJuggler](../../wiki/tools/plotjuggler.md) before the robot leaves the stand.

## Workflow

1. **Pin the interface.** Everything the policy depends on goes into one deploy spec written at
   export time: joint names in training order, default pose, action scale and clip, observation
   terms in order with their scales, PD gains, effort limits, physics step and decimation.
   Isaac Lab 3.0's LEAPP export writes an equivalent file ([isaac-lab.md](references/isaac-lab.md#export)).
   *Check:* the sim-to-sim runner and the robot node both load the spec; every joint name exists in
   the driver's `/joint_states`.

2. **Check the robot description against the robot.** Sign, zero, pose, limit and IMU-frame tests,
   one joint at a time, small and slow ([reality-gap.md](references/reality-gap.md#6-the-robot-description-is-wrong)).
   Fix the URDF or the driver, never the policy.
   *Check:* +0.1 rad on each joint moves it the same way in sim and on the robot; tilting the robot
   nose down changes projected gravity with the same sign as in sim.

3. **Measure the gap, source by source.** Details and methods in
   [reality-gap.md](references/reality-gap.md).

   | Source | Measure on the robot | Model in sim |
   |---|---|---|
   | Actuators | Step, chirp and slow sweeps per joint; datasheet torque-speed; backlash by hand | PD gains, effort and velocity limits, DC motor curve, armature, friction |
   | Latency, rate | Command spike to measured motion; loop period histogram under load | Actuator and observation delay |
   | Sensors | Still recording: bias and noise; encoder resolution | Per-step noise, per-episode bias |
   | Contact | Tilt and pull tests on each floor | Friction per the engine's combine rule |
   | Mass, inertia | Scale per link and total; balance for centre of mass | Masses, CoM, inertia scaled to weighed totals |
   | Description | Tests of step 2 | Corrected URDF, calibration offsets |

   *Check:* each source has a value, its spread and a date in the project notes, or is marked
   unknown (and gets a wider range in step 5).

4. **Identify before you randomise.** Fit actuator parameters and delay on a bench or with the limb
   in the air, then masses and inertias, then contact. Replay the logged commands in the simulator
   and fit by least squares (`mujoco.sysid` in MuJoCo); use the dynamics regressor for inertias, an
   actuator network when the drive is too complex to model (Hwangbo et al. 2019), BAM for hobby
   servo friction ([system-identification.md](references/system-identification.md)).
   *Check:* on a held-out test the replay error is close to the fit error, and every fitted value
   is physical (no parameter stuck at its bound).

5. **Randomise what stays uncertain.** Centre each range on the identified value and make it about
   as wide as its uncertainty; give unmeasurable things (floor friction, payload, latency spread,
   pushes) wider ranges. Published ranges are starting points only
   ([ranges.md](references/ranges.md)): Tan et al. (RSS 2018) set theirs from measurements plus
   small margins, because wide ranges make policies conservative. Where to set them:
   [mujoco.md](references/mujoco.md), [isaac-lab.md](references/isaac-lab.md),
   [gazebo.md](references/gazebo.md).
   *Check:* the policy still learns the task, and its sim evaluation at the edges of every range
   is acceptable; sample from saved nominal values, never by compounding the live model.

6. **Design observations and actions that transfer.**
   - Observe only what the robot measures at the control rate: joint positions relative to the
     default pose, joint velocities, gyro, projected gravity (an IMU gives roll and pitch, not yaw,
     as Hwangbo et al. note), the last action, the command. Add noise matching step 3.
   - Keep privileged state (true base velocity, contact forces, friction) out of the actor: give it
     to the critic (asymmetric actor-critic, Pinto et al. 2018), to a teacher distilled into a
     student, or to an adaptation module (RMA, Kumar et al. RSS 2021).
   - Give the policy a short history of joint states and actions, or a recurrent network, so it can
     infer latency and actuator state; make the history longer than the total delay.
   - Act through joint position targets around the default pose, tracked by the drive's PD with the
     identified gains; scale and clip the same way in sim and on the robot.
   - Keep actions smooth with an action-rate penalty, or a low-pass filter that also runs on the
     robot.
   - Run the policy at `1 / (physics dt * decimation)` on the robot too, and model the measured
     delay in sim.

   *Check:* built from the same logged state, the observation vector from the robot code equals
   the sim's term by term (a unit test on a recorded sample).

7. **Validate in simulation, then in a second simulator.** Evaluate with randomisation and noise
   on, over many seeds and at range edges. Then run the exported policy, through the deploy spec
   and the robot's observation code, in a second simulator: MuJoCo for dynamics
   ([mujoco.md](references/mujoco.md)), Gazebo for the full ROS 2 stack
   ([gazebo.md](references/gazebo.md)). Also simulate the stand scenario (base fixed in the air) to
   have a reference for step 8.
   *Check (go/no-go):* the task works in the second simulator without retuning. If not, find which
   difference breaks it (contacts, actuator model, step size, an interface error) before any
   hardware run.

8. **Run on hardware in stages.** Write each stage's thresholds down before the run; compare with
   the sim reference, not with hope. Safety layers, the runner node and its stops are in
   [deployment.md](references/deployment.md).

   | Stage | Setup | Go when | Go back when |
   |---|---|---|---|
   | Bench | Powered, on a stand, no policy | E-stop cuts power; step 2 tests pass; latency measured; drive limits set | Any test fails |
   | Stand | Feet or wheels off the ground (arms: free space, no payload), soft start, logging | Tracking lag, oscillation and saturation look like the sim stand run | Oscillation, saturation, wrong signs |
   | Tethered | Harness or gantry takes the load, small commands | Planned runs complete without the harness taking load | Falls, slips, torque at limits |
   | Free | Spotter on the e-stop, clear area, commands widened step by step | Task performance within the margin set beforehand | Any new failure mode |

   Unitree's `unitree_rl_gym` deployment follows the same pattern: zero torque, move to the default
   pose, hold, then run the policy, with the robot hoisted at first and damping mode on exit.
   *Check:* every stage has a bag, a short note of what was seen, and a go or no-go decision.

9. **Log, review and close the loop.** Record the policy's observations and actions, commands, raw
   sensors and diagnostics in MCAP at every stage ([deployment.md](references/deployment.md#logging)).
   Compare commanded against measured joint positions, loop period, action and torque saturation
   with the sim plots; replay the logged commands in the simulator to see where the model departs.
   Feed what you learn back into step 4 or 5, not into ad hoc gains on the robot.
   *Check:* the replay of a real run in the updated simulator tracks the robot's joint
   trajectories more closely than before the change.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Oscillates or chatters on the robot only | Unmodelled latency; drive PD differs from sim; noisy joint velocity | Measure and model delay; identify the PD; train with velocity noise |
| Falls or jerks the moment the policy starts | Joint order or sign mismatch, wrong default pose, quaternion order | Map joints by name from the spec; sign test; MuJoCo is `w,x,y,z`, ROS and Isaac Lab 3.0 `x,y,z,w` |
| Legs sag, cannot lift, fast moves fall short | No torque-speed curve or voltage sag in sim; effort limit too generous | DC motor model; randomise motor strength; limits from the datasheet |
| Masses drift further each episode | Randomising with `*=` on the live model | Sample from saved nominal values every reset |
| Noise configured but absent in training | Isaac Lab `enable_corruption` false; MuJoCo sensor `noise` is metadata only | Turn corruption on; add noise in the observation code |
| Joint friction randomisation does nothing | `operation="scale"` on a default of zero | Use `"abs"`, or set the nominal value first |
| Works in Isaac Lab, fails in MuJoCo | Policy relies on one solver's contacts, or dt, gains, armature differ | Check the spec; widen contact randomisation; retrain |
| Slips on the real floor only | Floor friction not measured; engines combine friction differently | Tilt test; set values for the engine's combine rule |
| Sluggish, over-cautious gait on the robot | Ranges much wider than the real spread | Narrow ranges around identified values |
| Gazebo run looks nothing like MuJoCo | `gz_ros2_control` turns position commands into velocity commands | Gazebo for the ROS stack; dynamics checks in MuJoCo |
| Policy period wider on the robot than in sim | `rclpy` timer under load; logging on the same core | Measure the histogram; move the loop to C++ or a controller |
| Base velocity observation useless on the robot | Not measured; estimator error far above training noise | Drop it, or train with the estimator's error |
| Steady lean or drift | IMU bias or centre of mass offset not modelled | Per-episode bias; CoM randomisation; check IMU mounting |
| `ros2 bag record` rejects the topic list on Lyrical | Positional topics removed | `--topics /a /b` |

## Checks

Before reporting a transfer step done:

- The deploy spec exists, is generated from the training environment, and both runners load it.
- The exported model gives the training checkpoint's actions on a set of recorded observations.
- Sign, zero, pose, limit and IMU-frame tests passed and are written down.
- Each gap source has a measured value with spread, or is marked unknown and randomised wider.
- Identified parameters reproduce a held-out log in replay.
- The observation unit test passes on a recorded robot sample.
- The policy works in a second simulator through the robot's code path.
- The e-stop was tested this session; drive limits and the node's stops are active.
- Every hardware stage has an MCAP bag, a note and a go or no-go decision.

## Version and distro differences

- **Isaac Lab 2.x:** actuator limits `effort_limit`, `velocity_limit`, `effort_limit_sim`,
  `velocity_limit_sim` (3.0 renames them; `main` drops the old names); quaternions `w,x,y,z`; no
  observation delay fields; tasks under `manager_based/`.
- **MuJoCo:** actuator and sensor delays and `mujoco.sysid` need 3.5.0 or later, `<dcmotor>` 3.7.0,
  `body/simple` 3.11.0, `<pid>` 3.12.0. 4.0 splits the Python package into `mujoco-core` and
  `mujoco-studio`; uninstall `mujoco` before upgrading with pip.
- **rosbag2:** MCAP is the default storage on Jazzy and Lyrical. Positional topics are deprecated
  in Jazzy and removed in Lyrical. Humble defaults to sqlite3 and needs the separate
  `ros-humble-rosbag2-storage-mcap` package for `-s mcap`.
- **Gazebo:** Jazzy pairs with Harmonic, Lyrical with Jetty, Humble with Fortress (`ign` commands,
  `ignition-gazebo-*` plugin files); details in [gazebo.md](references/gazebo.md#distro-differences).

## Related

- References: [reality-gap.md](references/reality-gap.md),
  [system-identification.md](references/system-identification.md),
  [ranges.md](references/ranges.md), [mujoco.md](references/mujoco.md),
  [isaac-lab.md](references/isaac-lab.md), [gazebo.md](references/gazebo.md),
  [deployment.md](references/deployment.md).
- Wiki: [MuJoCo](../../wiki/tools/mujoco.md), [Isaac Sim](../../wiki/tools/isaac-sim.md),
  [Gazebo](../../wiki/tools/gazebo.md), [choose a simulator](../../wiki/guides/choose-a-simulator.md),
  [ros2_control](../../wiki/software/ros2-control.md), [URDF](../../wiki/software/urdf.md),
  [Foxglove](../../wiki/tools/foxglove.md), [PlotJuggler](../../wiki/tools/plotjuggler.md).
- Skills: [ros2-robot-description](../ros2-robot-description/SKILL.md),
  [ros2-control](../ros2-control/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [sim-gazebo](../sim-gazebo/SKILL.md), [ops-docker-ci](../ops-docker-ci/SKILL.md); later:
  `sim-mujoco`, Isaac Lab, LeRobot, `ops-bringup`, the `learn-` skills.
- Papers: Tobin et al., domain randomisation, IROS 2017 (arXiv:1703.06907); Peng et al., dynamics
  randomisation, ICRA 2018 (arXiv:1710.06537); Tan et al., RSS 2018 (arXiv:1804.10332); Hwangbo et
  al., actuator networks, Science Robotics 2019 (arXiv:1901.08652); OpenAI et al., automatic domain
  randomisation, 2019 (arXiv:1910.07113); Kumar et al., RMA, RSS 2021 (arXiv:2107.04034).
