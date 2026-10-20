---
name: humanoid-embodied-ai-open-stack-2026
description: Maps the 2026 open-source humanoid/embodied-AI stack — Psi0 (2.8K★ Apache-2.0 VLA foundation model for humanoid loco-manipulation, egocentric-video pretraining + <80-trajectory fine-tuning), UniT (XPeng's unified physical language tokenizer for human-to-humanoid transfer, 10k-hour Fe0 follow-up), HY-Embodied-VLM-1.0 (Tencent's ~3B-activated MoE embodied VLM), EgoHumanoid (robot-free egocentric demos, +51% over robot-only baselines), HoloMotion (whole-body control foundation), and GR00T WholeBodyControl — as a capability-survey and adoption-guidance skill. Use when [covering humanoid robotics or embodied AI in content, advising on which open embodied stack to adopt or build on, tracking open-weights expansion beyond LLMs into robotics, or comparing robot-data acquisition strategies]. NOT for [industrial fixed-arm automation selection, purchasing decisions for specific robot hardware, or safety certification for physical deployment].
---

# Humanoid & Embodied AI Open Stack 2026

## Overview
2026 is the year open weights crossed from language into the physical world. A coherent open-source humanoid stack now exists end-to-end — foundation VLA models, data pipelines, whole-body controllers, simulators — much of it Apache-2.0, much of it from Chinese labs and universities, with egocentric *human* video replacing scarce robot teleoperation data as the scaling input. This is the single biggest open-AI frontier expansion of the cycle and the clearest "open wins on usage" datapoint beyond text models.

## The Stack (top-down)

### Foundation VLA / VLM models
| Project | Org | License | What it does | Key numbers |
|---|---|---|---|---|
| **Psi0 (Ψ₀)** | USC PSI Lab (Wei et al.) | Apache 2.0 | Open VLA foundation model for humanoid loco-manipulation; Qwen3-VL-2B backbone + flow-based diffusion action expert (~500M) + RL low-level controller | 2,814★; new skills from as few as **80 teleop trajectories**; Best Paper, 3D-LLM/VLA workshop CVPR 2026; pretrains on EgoDex (Apple's egocentric human video) + Humanoid Everyday |
| **UniT** | XPeng Robotics (+Tsinghua, HKU) | Apache 2.0 | **Unified Latent Action Tokenizer via visual anchoring** — learns a shared "physical language" so human kinematics map to humanoid actions; policy + world-model branches | SOTA data efficiency on RoboCasa GR1 (66.4% ID success); zero-shot real-world task transfer; follow-up **Fe0** scales to ~**10k hours** (≈1,587× the teleop anchor) across heterogeneous robots |
| **HY-Embodied-VLM-1.0** | Tencent Hunyuan / Robotics X | Apache 2.0 | Efficient MoE embodied VLM: Hy3-A3B backbone + Hy-ViT2; action-centric 3-level capability taxonomy | ~**3B activated** (of ~30B); best on 19 of 38 embodied benchmarks; +8.4% over Hy-Embodied-0.5; ships HF + vLLM inference |
| **HEX** | Cognition2Action Lab | open (checkpoints + 8 real-task datasets) | Whole-body VLA for full-sized humanoids; body-part slot alignment for cross-embodiment transfer | Qwen-VL backbone + flow-matching action head; arm/hand/waist actions + RL legs |

### Data & learning frameworks
- **EgoHumanoid** (OpenDriveLab, RSS 2026, Apache 2.0) — first framework learning whole-body loco-manipulation from **egocentric human demos** (PICO VR + ZED): view alignment + action alignment pipelines; robot-free egocentric data **outperforms robot-only baselines by +51%**, especially in unseen environments. π0.5-based, deploys on Unitree G1.
- **OpenHLM** (Apache 2.0) — empirical recipe for whole-body loco-manipulation: one-variable-at-a-time experiment roadmap; beats GR00T N1.6 and Ψ₀ baselines on a long-horizon task using **less than half** the demonstration time; HuMI human-data pipeline included.
- **Humanoid Everyday / RoboCOIN / AgiBot World** — the open humanoid datasets layer (Unitree G1/H1, Kuavo platforms).

### Control, sim, and platform
- **HoloMotion** (Horizon Robotics, Apache 2.0) — whole-body-control foundation model; v1.3 scaled 60M→0.4B params, 80→2,000+ hours motion data, ~300 FPS policy inference; four-phase roadmap: any pose → any command → any terrain → any embodiment.
- **GR00T WholeBodyControl / SONIC** (NVIDIA) — the de-facto low-level whole-body controller most VLA stacks integrate (Ψ₀, OpenHLM, EgoHumanoid all use it).
- **SIMPLE** (Psi-lab) — MuJoCo+Isaac Sim humanoid benchmark with 6 open whole-body tasks; **Genesis-Humanoid** (UMass, MIT) — 200k RL steps/sec all-in-one humanoid research platform with sim-real duality.
- **OpenTrajBooster / AMO** — open VR teleoperation + whole-body controller stacks for Unitree G1 data collection.

## The Three Structural Insights
1. **Egocentric human video is the data unlock.** The recurring pattern (Psi0's EgoDex pretraining, EgoHumanoid's +51%, UniT's 10k-hour Fe0): robots are data-starved but humans aren't. Human-first data pipelines with embodiment-alignment (view + action retargeting) are how the gap closes — this is the robotics version of "open weights plus cheap data beats closed everything."
2. **Hierarchical System-2/System-1/System-0 architecture has converged.** A VL backbone (reasoning) + diffusion/flow action expert (skills) + RL low-level controller (physics) is now the consensus architecture across Psi0, HEX, and HY-Embodied — a stable abstraction for anyone building in the space.
3. **Open weights won the humanoid layer the way they won the LLM layer.** The majority of the above is Apache-2.0 with released checkpoints and datasets on Hugging Face; the ecosystem is reusing LeRobot formats and GR00T controllers — composability standards are forming in public.

## When to Use
- Content: "Open source just invaded robotics" / "Your next robot runs on Apache 2.0."
- Advising teams choosing a stack: which foundation model, which controller, which data strategy.
- Tracking open-AI frontier expansion beyond text/code (community-growth framing: new commons forming).
- Comparing data strategies: teleop vs egocentric vs sim generation.

## NOT For
- Specific robot hardware procurement or safety certification.
- Fixed-arm industrial automation (different maturity curve, mostly closed tooling).
- Claims of household deployment readiness — all real-world results are lab-grade; treat demos as capability evidence, not product readiness.

## Core Process / Workflow
### Stack selection decision table
| Goal | Recommended base |
|---|---|
| Fine-tune a humanoid policy with minimal teleop data | **Psi0** (80-trajectory fine-tuning recipe + open data) |
| Transfer human motion/skills across embodiments | **UniT** tokenizer (unified physical language) |
| Efficient embodied reasoning on modest hardware | **HY-Embodied-VLM-1.0** (3B-activated MoE, vLLM) |
| Whole-body control foundation / motion imitation | **HoloMotion** + GR00T/SONIC controller |
| Learn from human egocentric video only | **EgoHumanoid** pipeline (view+action alignment) |
| Benchmarking | **SIMPLE** (MuJoCo/Isaac) |

### Evaluation discipline (hype-resistance drill)
1. Distinguish **measured vs vendor-claimed**: most benchmark tables are vendor-run; prefer independently reproduced numbers (the library's claim-verification ladder).
2. Check **simulation vs real**: RoboCasa/SIMPLE results ≠ real-world capability; require real-robot videos.
3. Check **data provenance**: which datasets (EgoDex, Humanoid Everyday, proprietary teleop) and how much robot data the recipe actually needs.
4. Note **license**: Apache 2.0 vs "Other" (Ψ0 repo says Apache in README; HY-Embodied-VLM weights are Apache; verify per-release).
5. Track **hardware prerequisites**: e.g., HY-Embodied full BF16 inference ~86GB across GPUs; Psi0 fine-tuning VRAM tiers are documented per config.

## A-Tech Alignment
- **Open source:** the flagship evidence that the open-weight wave generalizes beyond LLMs — Apache-2.0 foundation models + open datasets + open controllers = a new commons forming in public; direct continuation of the Mozilla "harness layer" thesis into physical AI.
- **Privacy:** egocentric human video pipelines raise consent questions (filmed humans as training data) — A-Tech's data-rights framing extends to embodied datasets; on-robot inference (edge) is the privacy-preserving deployment posture.
- **Financial freedom:** open stacks collapse the entry cost of robotics R&D (a 4090-class GPU covers inference for several of these models); human-data pipelines let small teams substitute capture time for capital.
- **Practical:** stack selection table + five-point evaluation drill; evergreen explainer content with concrete model names.

## References
- Primary: Psi0 (github.com/physical-superintelligence-lab/Psi0, arXiv:2603.12263); UniT (github.com/xpeng-robotics/UniT, arXiv:2604.19734) + Fe0 blog; HY-Embodied (github.com/Tencent-Hunyuan/HY-Embodied, arXiv:2607.12894); EgoHumanoid (OpenDriveLab, arXiv:2602.10106); OpenHLM (arXiv:2606.22174); HoloMotion (HorizonRobotics, arXiv:2605.15336); HEX (arXiv:2604.07993); SIMPLE; GR00T WholeBodyControl.
- Pairs with: `embodied-ai-interface-design`, `bitnet-on-device-training-framework` (edge efficiency), `open-weight-agentic-model-wave` (the LLM-layer counterpart), `mozilla-open-source-ai-state-2026` (harness-layer thesis), `neurodiversity-ai-inclusive-design` (assistive robotics angle).