---
name: vla-foundation-models
description: "Use when building, fine-tuning, deploying, or safety-wrapping Vision-Language-Action (VLA) models for robot manipulation — RT-2, OpenVLA, pi0, Octo, ACT, diffusion policies, ALOHA-style teleop data collection, action chunking, latency budgeting. Provides exact model specs, inference-rate math, working OpenVLA/ACT/pi0 deployment code, dataset formats (RLDS/LeRobot), the failure modes that ruin runs, and hard safety-wrapper patterns for learned policies."
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


# Vision-Language-Action (VLA) Foundation Models

Expert knowledge for deploying learned manipulation policies on real hardware.
Covers the Tesla/Figure direction: a single network maps `(camera images, language instruction, proprioception) → action tokens/chunks`, replacing the classical perceive→plan→control pipeline.

---

## 1. Core Concept — What a VLA Actually Computes

```
Inputs (per inference step):
  - 1..N RGB images (typically 224x224 or 256x256, ImageNet-normalized OR [-1,1])
  - Language instruction string ("pick up the red block and place it in the bin")
  - Proprioception: joint positions q (and sometimes gripper state), 6-14 DoF
Outputs (one of three families):
  A. Discrete action TOKENS  (RT-2, OpenVLA): each action dim binned into 256 bins,
     emitted autoregressively like text tokens. 7 tokens = [Δx Δy Δz Δroll Δpitch Δyaw gripper]
  B. Action CHUNK regression (ACT): one forward pass → k×D matrix of future actions
     (k=50-100 timesteps), trained with L1 loss + CVAE latent
  C. Diffusion/flow head (Diffusion Policy, pi0, Octo-diffusion): iteratively denoise
     an action chunk; pi0 uses flow matching (10 integration steps typical)
```

**Action space conventions — get this wrong and the robot lunges:**

| Convention | Meaning | Used by |
|---|---|---|
| Delta EEF pose | Δ position (m) + Δ rotation (axis-angle or RPY) in base or EEF frame | RT-1/RT-2, OpenVLA (BridgeData) |
| Absolute joint positions | target q per joint (rad) | ACT/ALOHA, pi0 (most configs) |
| Delta joint positions | q_target = q_now + Δq | some Octo configs |
| Normalized | all dims scaled to [-1,1] using dataset q01/q99 quantiles | OpenVLA, Octo, LeRobot |

**Always un-normalize with the SAME statistics used in training** (OpenVLA ships `dataset_statistics.json`; LeRobot stores `stats` in the dataset card). Using mean/std when the model was trained with q01/q99 quantile scaling produces ~2x amplitude actions — the classic "robot slams into table on step 1" bug.

Gripper: usually a continuous value where dataset semantics differ — BridgeData: +1=open, 0=close; ALOHA: gripper joint position in rad; some datasets invert. Verify by replaying one training episode before any live run.

---

## 2. Model Landscape (as of 2025)

| Model | Params | Backbone | Action head | Control rate achievable | Hardware to run | Open weights |
|---|---|---|---|---|---|---|
| RT-2 (Google) | 12B/55B | PaLI-X / PaLM-E | 256-bin tokens, autoregressive | 1-3 Hz (cloud TPU) | TPU cluster | No |
| OpenVLA | 7B | Prismatic (SigLIP+DINOv2 → Llama-2 7B) | 7 discrete tokens | ~6 Hz on RTX 4090 (bf16), ~3 Hz on 3090 | 16 GB VRAM bf16, 8 GB int4 | Yes (Apache 2.0-ish, check card) |
| OpenVLA-OFT | 7B | same + parallel decoding | continuous chunk, L1 | 25-50 Hz effective via chunks | RTX 4090 | Yes |
| Octo | 27M/93M | ViT + transformer | diffusion head, chunk=4 | 10+ Hz on laptop GPU | 4 GB VRAM | Yes (MIT) |
| ACT | ~80M | ResNet18 ×4 cams + transformer CVAE | chunk regression k=100 | 50 Hz on RTX 3060 | 6 GB VRAM | Yes (MIT) |
| Diffusion Policy | 20-300M | ResNet/ViT + U-Net or DiT denoiser | 16-step chunk, DDIM ~10 steps | 10 Hz | 8 GB VRAM | Yes (MIT) |
| pi0 (Physical Intelligence) | 3.3B | PaliGemma 3B + 300M flow-matching action expert | flow matching, chunk=50 | chunk every ~100 ms on 4090 → 50 Hz execution | 16+ GB VRAM (bf16) | Yes (openpi repo) |
| pi0-FAST | 3.3B | same + FAST action tokenizer (DCT-based) | autoregressive tokens | slower inference than pi0 flow | 16 GB | Yes |
| SmolVLA (LeRobot) | 450M | SmolVLM | flow matching chunk | 15+ Hz on consumer GPU | 4 GB | Yes (Apache) |

**Choosing:**
- Single fixed task, 50-200 teleop demos, bimanual or single arm → **ACT**. Simplest, trains in hours on one GPU, runs fast.
- Need multimodal action distributions (multiple valid grasp strategies in data) → **Diffusion Policy** (ACT's CVAE mode-averages; diffusion doesn't).
- Want language conditioning + generalization from a pretrained robot foundation model, fine-tuned on 50+ demos → **OpenVLA (LoRA fine-tune)** or **pi0** via openpi, or **SmolVLA** if VRAM-poor.
- Research on cheap hardware → **Octo** or **SmolVLA**.

---

## 3. ALOHA-Style Teleop Data Collection

VLA quality is ~80% data quality. The ALOHA recipe (leader-follower joint copying):

```
Leader arms (human-moved, gravity-compensated or low-friction)
   └─ read leader joint positions at 50 Hz
        └─ command follower arm to same joint positions (position control)
             └─ record per timestep: follower q (14-dim for bimanual),
                action = LEADER q (not follower!), 3-4 camera RGB @ 50 Hz
```

**Critical detail everyone gets wrong:** the recorded *action* is the **leader** joint position, the *observation* is the **follower** joint position. The gap between them encodes the force/intent signal. Recording follower q as action trains a policy that lags and never makes contact firmly.

Hardware numbers (ALOHA / ALOHA-2, Trossen ViperX/WidowX class):
- Control + record rate: **50 Hz** (DT = 0.02 s). Lower than 30 Hz makes teleop feel mushy and chunks stale.
- Cameras: 3-4× USB (e.g. Logitech C922 / RealSense RGB only), 480×640 @ 50 fps capture, resized to 224×224 for training. Two wrist cams + one/two static.
- Dynamixel servos on leader: torque off (or current-limited ~20 mA for gravity comp); follower: position mode, P gain tuned so step response < 100 ms without oscillation.
- USB bandwidth: 4 uncompressed 640×480 MJPEG streams ≈ fine on one USB 3.0 root hub; **uncompressed YUYV will not fit** — force MJPEG: `v4l2-ctl -d /dev/video0 --set-fmt-video=width=640,height=480,pixelformat=MJPG`.

**Episode protocol:**
- 25-50 s episodes, 50-100 episodes minimum per task for ACT; 100-150 for harder tasks.
- Randomize object pose every episode (within the distribution you want at test time — the policy will NOT extrapolate beyond it).
- Keep camera mounts RIGID. A 2° camera shift between collection and deployment silently destroys performance (the #1 "it worked yesterday" cause).
- Reset to a consistent home pose before each episode; the policy learns the approach from home.
- Record failures? No — for BC, train only on successes (or successes + recoveries you demonstrated deliberately; demonstrated recoveries are extremely valuable).

**Recording loop (LeRobot-style, simplified):**

```python
import time
FPS = 50
DT = 1.0 / FPS

frames = []
t_next = time.perf_counter()
while recording:
    leader_q = leader.read_joint_positions()      # 14-dim, rad
    follower.write_goal_positions(leader_q)        # position command
    obs_q = follower.read_joint_positions()
    imgs = {name: cam.read() for name, cam in cameras.items()}  # threaded readers!
    frames.append({
        "observation.state": obs_q,
        "action": leader_q,                        # LEADER, not follower
        **{f"observation.images.{k}": v for k, v in imgs.items()},
        "timestamp": time.perf_counter(),
    })
    t_next += DT
    sleep = t_next - time.perf_counter()
    if sleep > 0: time.sleep(sleep)
    elif sleep < -DT: print(f"OVERRUN {-sleep*1000:.1f} ms")  # fix this before collecting
```

Camera reads MUST be on background threads (each `cv2.VideoCapture.read()` can block 10-30 ms; 4 serial reads blows the 20 ms budget). Use a latest-frame-wins ring buffer per camera.

**Dataset formats:**
- **RLDS / Open X-Embodiment**: TFDS episodic format. OpenVLA and Octo fine-tuning expect this.
- **LeRobotDataset v2** (HuggingFace): parquet + mp4-encoded video, `delta_timestamps` for chunk sampling. ACT/Diffusion/SmolVLA/pi0-via-lerobot use this. Convert with `lerobot` converters rather than hand-rolling.

---

## 4. ACT — Action Chunking with Transformers (the workhorse)

Architecture: 4× ResNet18 image encoders → transformer encoder (image feats + q + CVAE latent z) → transformer decoder emits k=100 future actions in one pass. CVAE encoder (training only) compresses the demonstrated action sequence into z (dim 32); at inference z = 0.

**Training config that works (don't deviate first try):**

```python
config = dict(
    chunk_size=100,            # k. 100 @ 50Hz = 2 s lookahead
    kl_weight=10.0,            # CVAE KL term; 10 is the magic number
    hidden_dim=512, dim_feedforward=3200,
    nheads=8, enc_layers=4, dec_layers=7,
    lr=1e-5, lr_backbone=1e-5, batch_size=8,
    num_steps=100_000,         # ~5-8 h on one 3090 for 50 episodes
    image_size=(480, 640),     # ACT keeps native-ish res
)
# Loss: L1(pred_chunk, gt_chunk) + kl_weight * KL(z_posterior || N(0,1))
# L1, not L2 — L2 mode-averages harder and gives mushy contact behavior.
```

**Temporal ensembling at inference (essential for smoothness):** run inference EVERY step; each timestep t has predictions from up to k overlapping chunks; blend with exponential weights:

```python
import numpy as np

class TemporalEnsembler:
    def __init__(self, k=100, action_dim=14, m=0.01):
        self.k, self.m = k, m
        self.buf = np.full((k, k, action_dim), np.nan)  # [age, offset, dim]
    def step(self, new_chunk):                # new_chunk: (k, action_dim)
        self.buf = np.roll(self.buf, 1, axis=0); self.buf[0] = new_chunk
        preds = np.array([self.buf[age, age] for age in range(self.k)
                          if not np.isnan(self.buf[age, age]).any()])
        w = np.exp(-self.m * np.arange(len(preds)))     # older chunks get... 
        # NOTE: ACT paper weights OLDER predictions HIGHER (w_i = exp(-m*i), i=0 oldest).
        # Both orderings appear in the wild; ACT reference: i indexes oldest-first.
        return (preds * w[:, None]).sum(0) / w.sum()
```

If your control loop can't afford inference every step, fall back to "execute first n actions of chunk, re-infer" (receding horizon, n = k/2 typical). Smoothness is worse; add an EMA filter on commanded q (`q_cmd = 0.8*q_cmd_prev + 0.2*q_new`) if joints chatter.

**ACT failure signatures:**
- Pauses then jerks mid-trajectory → chunk boundary discontinuity → use temporal ensembling.
- Gripper opens/closes at wrong times → gripper dim dominated by L1 of arm dims → check action normalization includes gripper; or weight gripper loss ×2.
- Policy hovers above object, never descends → camera moved since collection, or insufficient pose randomization (policy memorized pixel locations).
- Validation loss ↓ but success rate ~0 → loss is a weak proxy; evaluate with real rollouts every 10k steps. Best checkpoint is rarely the lowest-loss one — keep last 5 and roll out each.

---

## 5. Diffusion Policy

Predicts an action chunk by denoising. Use when demonstrations contain multiple distinct strategies (ACT's z=0 collapses these; diffusion samples one mode cleanly).

Key numbers:
- Prediction horizon T_p=16, observation horizon T_o=2, action execution horizon T_a=8 (execute 8 of 16, re-plan).
- Training: DDPM 100 noise steps; inference: DDIM 10 steps (≈10× speedup, negligible quality loss).
- CNN-based U-Net1D head is more robust to hyperparams than transformer head — start there.
- EMA of weights (decay 0.9999) is **mandatory** — non-EMA checkpoints visibly underperform.
- Inference latency: ~80-120 ms for 10 DDIM steps on RTX 3090 (ResNet18 encoder) → re-plan at ~8 Hz, execute at 50 Hz from chunk buffer.

```python
# Inference skeleton (diffusers-style)
naction = torch.randn(B, 16, action_dim, device=dev)
scheduler.set_timesteps(10)                       # DDIM
obs_cond = obs_encoder(images, agent_pos)         # computed ONCE per replan
for t in scheduler.timesteps:
    eps = noise_pred_net(naction, t, global_cond=obs_cond)
    naction = scheduler.step(eps, t, naction).prev_sample
action_chunk = unnormalize(naction[0, :8])        # execute T_a=8
```

---

## 6. OpenVLA — Fine-Tune and Deploy

7B Prismatic VLM; image → 256 visual tokens; action = 7 tokens from a 256-bin vocabulary overwritten onto the least-used Llama tokens.

**Inference server (run model on a GPU box, robot talks REST):**

```python
# Server (GPU box)
from transformers import AutoModelForVision2Seq, AutoProcessor
import torch

processor = AutoProcessor.from_pretrained("openvla/openvla-7b", trust_remote_code=True)
model = AutoModelForVision2Seq.from_pretrained(
    "openvla/openvla-7b", torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",   # 4090: yes; older GPUs: omit
    trust_remote_code=True).to("cuda:0")

def predict(image_pil, instruction: str, unnorm_key: str):
    prompt = f"In: What action should the robot take to {instruction.lower()}?\nOut:"
    inputs = processor(prompt, image_pil).to("cuda:0", dtype=torch.bfloat16)
    action = model.predict_action(**inputs, unnorm_key=unnorm_key, do_sample=False)
    return action   # 7-dim numpy: [Δx Δy Δz Δr Δp Δy gripper], already unnormalized
```

- `unnorm_key` selects which dataset's statistics to un-normalize with (e.g. `"bridge_orig"`). Wrong key = wrong action scale. For your fine-tune, it's your dataset name.
- `do_sample=False` (greedy). Sampling action tokens adds noise you don't want.
- bf16 on 4090: ~150-180 ms/inference → 5-6 Hz. int4 (bitsandbytes) fits 8 GB but ~2x slower per token on some GPUs — measure, don't assume.
- BridgeData models expect a **single 3rd-person camera at roughly the BridgeData viewpoint** and 256×256 center-cropped input. Wrist-cam-only input to a 3rd-person-trained model = garbage out.

**LoRA fine-tuning (the only sane path; full FT needs 8×A100):**
- r=32, lora_alpha=16, all-linear targets, batch 8-16 with grad accum, lr 5e-4 const, ~50k steps for 100 demos. Fits one 4090 (24 GB) with grad checkpointing at batch 2-4 + accumulation.
- Data must be in RLDS format; use the `rlds_dataset_builder` template repo. Fine-tune images: 224×224, same augmentation pipeline as pretraining (random crop ratio 0.9).
- After LoRA fine-tune, OpenVLA emits actions in YOUR dataset's action space (e.g. joint deltas if that's what you logged) — un-normalize with YOUR stats.

**Latency reality check:** at 5 Hz with single-action (non-chunked) output, OpenVLA is fine for quasi-static pick-and-place, hopeless for dynamic tasks. OpenVLA-OFT (parallel decoding + chunks + continuous head) fixes this — prefer it for new work.

---

## 7. pi0 / openpi Deployment

pi0 = PaliGemma 3B VLM + 300M action expert; flow matching head outputs a 50-step action chunk; trained on ~10k hours cross-embodiment then fine-tuned per robot.

```python
# openpi client-server pattern (recommended — keeps GPU off the robot)
# Server (GPU box):
#   uv run scripts/serve_policy.py policy:checkpoint --policy.config=pi0_aloha \
#       --policy.dir=checkpoints/pi0_aloha/my_task/29999
# Robot client:
from openpi_client import websocket_client_policy
policy = websocket_client_policy.WebsocketClientPolicy(host="192.168.1.50", port=8000)
obs = {
    "observation/state": q_14dim,
    "observation/image": img_base_224,        # exact key names depend on config!
    "observation/wrist_image": img_wrist_224,
    "prompt": "fold the towel",
}
chunk = policy.infer(obs)["actions"]          # (50, 14) absolute joint targets (ALOHA cfg)
for a in chunk[:25]:                          # execute half, then re-infer (overlap hides latency)
    robot.command_joint_positions(a); rate.sleep()   # 50 Hz
```

- Flow matching inference: 10 Euler steps, ~50-100 ms total on 4090 → new chunk every 0.5 s of executed motion with double-buffering (infer next chunk while executing current).
- Image keys and state ordering are config-specific (`src/openpi/training/config.py`) — mismatched key names fail silently with degraded behavior in some wrappers. Print the config's `input spec` and match exactly.
- Fine-tuning pi0 (LoRA) on your task: ~1×A100-80GB or 2×4090 with FSDP; 50-100 episodes in LeRobot format; convert via openpi's `compute_norm_stats` then train ~30k steps.

---

## 8. Latency Budget & Control Architecture

The non-negotiable math. A learned policy is safe and smooth only if staleness is bounded.

```
Total observation→actuation latency:
  camera exposure+readout     10-35 ms   (USB cam; global shutter GigE: 5-10 ms)
  image transport+decode       5-20 ms   (MJPEG decode ~5 ms; network adds RTT)
  preprocessing (resize/norm)  1-3 ms
  model inference              ACT 10 ms | DiffPolicy 100 ms | OpenVLA 180 ms | pi0 100 ms
  network back to robot        1-5 ms LAN
  controller interpolation     one control tick (1-20 ms)
```

**Rules:**
1. Robot-side control loop runs at fixed high rate (50-500 Hz) consuming from an action buffer. Inference fills the buffer asynchronously. NEVER block the control loop on inference.
2. Action chunks make slow models viable: model at 2 Hz emitting 50-step chunks @ 50 Hz = full coverage with 0.5 s margin. But chunks are open-loop — the longer you execute blind, the worse the reaction to disturbance. Execute ≤ half the chunk, re-plan.
3. Timestamp every observation; if `now - obs_timestamp > 150 ms` at inference time, drop and grab fresh.
4. Linear-interpolate between consecutive chunk actions if the chunk rate < controller rate; on real arms send through the vendor's streaming interface (Franka: `franka_ros2` joint impedance @ 1 kHz with your 50 Hz setpoints interpolated; UR: `servoJ` with lookahead_time=0.1, gain=300; Dynamixel: position goal @ 50 Hz is fine natively).

```python
# Canonical two-thread deployment skeleton
import threading, queue, time
action_buf = queue.Queue(maxsize=200)

def inference_thread():
    while run:
        obs = grab_latest_obs()                       # never stale > 150 ms
        chunk = policy.infer(obs)                     # slow, variable
        with buf_lock:
            drain(action_buf)                         # discard remainder of old chunk
            for a in chunk[:len(chunk)//2]: action_buf.put(a)

def control_thread():                                  # 50 Hz, hard real-time-ish
    t = time.perf_counter()
    while run:
        a = action_buf.get_nowait() if not action_buf.empty() else last_action  # HOLD on starvation
        a = safety_filter(a)                          # see §9 — NEVER skip
        robot.command(a); last_action = a
        t += 0.02; time.sleep(max(0, t - time.perf_counter()))
```

On buffer starvation: **hold last position** (arms) or **decelerate to stop** (mobile bases). Never repeat the last *velocity* command.

---

## 9. Safety-Wrapping Learned Policies (mandatory)

A VLA gives zero guarantees. Wrap every action in deterministic, non-learned checks. Defense in depth:

```python
import numpy as np

class SafetyFilter:
    def __init__(self, q_min, q_max, dq_max, workspace_aabb, dt=0.02):
        self.q_min, self.q_max = q_min, q_max          # joint limits, rad (use SOFT limits: 5° inside hard)
        self.dq_max = dq_max                            # per-joint rad/s cap, e.g. 1.5 (≈86°/s) for tabletop
        self.aabb = workspace_aabb                      # EEF box: ((xmin,ymin,zmin),(xmax,ymax,zmax))
        self.dt = dt; self.q_prev = None

    def __call__(self, q_cmd, q_meas):
        # 0. Sanity: NaN/Inf from the model happens. Treat as fault, hold.
        if not np.all(np.isfinite(q_cmd)): return q_meas, "NAN_FAULT"
        # 1. Joint position clamp
        q_cmd = np.clip(q_cmd, self.q_min, self.q_max)
        # 2. Rate limit vs MEASURED q (not previous command — windup otherwise)
        step = np.clip(q_cmd - q_meas, -self.dq_max*self.dt, self.dq_max*self.dt)
        q_cmd = q_meas + step
        # 3. Action-jump check: model output discontinuity > 15° on any joint = fault
        if self.q_prev is not None and np.max(np.abs(q_cmd - self.q_prev)) > 0.26:
            return self.q_prev, "JUMP_FAULT"
        # 4. Workspace check via FK — clamp EEF inside AABB (or fault & hold)
        p = forward_kinematics(q_cmd)
        if not in_box(p, self.aabb): return self.q_prev if self.q_prev is not None else q_meas, "WS_FAULT"
        self.q_prev = q_cmd
        return q_cmd, "OK"
```

Layer the rest:

| Layer | Mechanism | Numbers |
|---|---|---|
| Hardware E-stop | physical button cutting motor power | mandatory; test before every session |
| Force/torque limits | vendor collision detection (Franka: set `collision_behavior` thresholds ~20 N / 10 Nm for tabletop) | reflex stops in < 2 ms |
| Velocity caps | filter above + vendor speed limit (UR: reduced mode 250 mm/s near humans, ISO/TS 15066 speed-and-separation) | EEF ≤ 0.25 m/s with people in workspace |
| Watchdog | robot firmware stops if no command for > 100 ms | configure, don't assume |
| Episode timeout | kill episode after T_max (2-3× demo length) | prevents grinding against a fixture forever |
| Out-of-distribution guard | if camera image differs grossly from training (cheap: mean-pixel + embedding cosine vs training set < 0.7) → pause | crude but catches "someone moved the lamp" |
| Human gate for irreversibles | gripper force cap (Dynamixel: current limit register; Robotiq: force setting ≤ 40%) | a 7B model WILL eventually crush the object |

**Deployment ramp:** (1) replay a training episode open-loop — verifies action decode/unnorm/frame conventions with zero learned behavior; (2) run policy at 25% velocity scale with hand on E-stop; (3) full speed only after 10 clean low-speed episodes.

---

## 10. Debugging Checklist (in order — top items cause 90% of failures)

1. **Replay a training episode through your deployment code path** (decode → unnormalize → safety filter → robot). If replay doesn't reproduce the demo, the bug is in YOUR plumbing, not the model. Do this before ever blaming the policy.
2. **Normalization stats mismatch** — print `action.min/max` over one inferred chunk; compare to dataset stats. Off by ~2x → mean/std vs quantile confusion. Off by ~57x → degrees/radians.
3. **Camera mismatch** — overlay a live frame on a training frame (50% alpha). Any visible shift in viewpoint, crop, white balance, or resolution → fix the mount/crop, or re-collect. Also: BGR vs RGB (cv2 gives BGR; every training pipeline expects RGB).
4. **Wrong image preprocessing** — center-crop vs resize-distort, [0,1] vs [-1,1] vs ImageNet norm. Must byte-match training. Diff your preprocessed tensor against the training dataloader's output for the same raw frame.
5. **Stale observations** — log `inference_start - frame_timestamp`. > 100 ms = your camera thread is buffering; set `cv2.CAP_PROP_BUFFERSIZE=1` and use latest-frame threads.
6. **Proprioception ordering/units** — joint order must match training (ALOHA: [waist, shoulder, elbow, forearm_roll, wrist_angle, wrist_rotate, gripper] × 2 arms). Gripper raw ticks vs radians vs normalized.
7. **Chunk boundary jerk** — temporal ensembling (ACT) or overlap re-planning (diffusion/pi0); EMA on commands as last resort.
8. **Policy "almost" succeeds, off by 2 cm consistently** — TCP/tool offset differs from data collection (changed gripper fingers?), or table height changed.
9. **Works on episode-start states only** — your reset distribution at deployment is wider than collection. Collect more varied resets; for VLAs, also vary distractor objects.
10. **Language instruction ignored (multi-task model)** — instruction string must match training phrasing distribution; OpenVLA prompt template must be exact (`"In: What action should the robot take to {x}?\nOut:"`, instruction lowercased).
11. **GPU thermal throttling mid-episode** — inference latency creeping from 100→250 ms over minutes. `nvidia-smi dmon` while running; pin clocks or add cooling.
12. **It worked yesterday** → in order: camera moved, lighting changed (sunlight!), object swapped for a different instance, USB enumeration reordered cameras (bind by serial: udev rules, not /dev/videoN).

---

## 11. Quick Reference — Rates and Budgets

| Quantity | Value |
|---|---|
| Teleop/record rate (ALOHA) | 50 Hz, DT=20 ms, overruns must be 0 before collecting |
| ACT chunk / re-plan | k=100; ensemble every step, or execute 50 then re-infer |
| Diffusion Policy horizons | T_o=2, T_p=16, T_a=8; DDIM 10 steps |
| pi0 chunk | 50 steps @ 50 Hz; re-infer at half-chunk with double buffering |
| OpenVLA single-action rate | 5-6 Hz (4090 bf16) — quasi-static tasks only |
| Max tolerable obs staleness | 150 ms (manipulation), 50 ms (anything dynamic) |
| Command watchdog on robot | 100 ms no-command → hold/stop |
| Joint velocity cap (tabletop dev) | 1.5 rad/s per joint; EEF 0.25 m/s near humans (ISO/TS 15066) |
| Action jump fault threshold | > 15° (0.26 rad) between consecutive commands |
| Min demos: ACT single task | 50 (easy) – 150 (precise/bimanual) |
| Min demos: VLA LoRA fine-tune | 50-100 episodes, more diversity > more count |
| Eval protocol | ≥ 10 rollouts per checkpoint, randomized resets, report success rate not loss |
