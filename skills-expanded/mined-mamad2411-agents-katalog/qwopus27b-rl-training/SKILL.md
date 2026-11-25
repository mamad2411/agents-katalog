---
name: qwopus27b-rl-training
description: Prepare, validate, launch-plan, monitor, resume, and stop configurable Qwopus 27B reinforcement-learning workflows for GRPO or GSPO. Use when Codex needs to turn an editable Goal template and user config into a safe local or SSH RL training plan without overstating dry-run results or relabeling SFT, GRPO, GSPO, or other algorithms.
---

# Qwopus 27B RL Training

Use this skill to prepare a guarded RL training workflow for Qwopus 27B. The repository includes `train_code/Qwopus3.6-27B-GSPO/qwopus3_6_27b_gspo_training.py` as a publication-safe GSPO-style tutorial and `train_code/Qwopus3-5-27b-Colab.ipynb` as a Qwopus 27B SFT tutorial. Do not claim an implementation is RL unless inspection finds GRPO, GSPO, or another RL trainer in the referenced script.

## Resources

- `assets/GOAL_TEMPLATE.md`: editable Codex Goal template.
- `assets/USER_CONFIG.example.env`: public-safe configuration example.
- `scripts/render_goal.py`: renders the template from a config file.
- `references/TRAINING_CHECKLIST.md`: validation checklist for local and SSH runs.

## Algorithm Detection

Before naming the algorithm:

1. Inspect the requested tutorial, notebook, or script path.
2. Treat imports or trainer construction as the source of truth.
3. Map `GSPOConfig` or `GSPOTrainer` to `GSPO` when those API names exist.
4. Map `GRPOConfig` or `GRPOTrainer` plus GSPO-style settings such as `importance_sampling_level="sequence"`, `loss_type="dr_grpo"`, and `mask_truncated_completions=True` to `GSPO-style`, not plain GRPO.
5. Map `GRPOConfig` or `GRPOTrainer` without GSPO-style settings to `GRPO`.
6. Map `SFTTrainer` or `SFTConfig` to `SFT`, not RL.
7. If the implementation cannot be inspected, say the algorithm is unverified and stop before launch.

Default `ALGORITHM` may be `GRPO` or `GSPO`, but the selected implementation must match.

## Safety Defaults

Keep these defaults unless the user explicitly overrides them:

```text
DRY_RUN=true
ALLOW_LONG_TRAINING=false
ALLOW_HF_UPLOAD=false
ALLOW_DESTRUCTIVE_ACTIONS=false
```

Never claim a completed training run from a dry run. A dry run can only validate configuration, imports, dataset schema, reward functions, trainer construction, launch commands, monitoring commands, resume commands, and stop commands.

## Execution Modes

Support both modes:

- `local`: run checks and launch commands in the local checkout.
- `ssh`: prepare explicit remote commands using a user-provided placeholder host. Do not embed private SSH aliases in templates or public docs.

## Required Checks

Perform the feasible checks before launch:

- Environment and dependency checks.
- Dataset schema checks.
- Reward-function unit tests or small sample tests.
- Trainer-construction smoke test without long training.
- Output-directory and checkpoint policy review.
- Launch plan, monitoring command, resume command, and stop command.

## Memory Pressure

Do not silently reduce training quality just to fit memory. Recommend changes in this order:

1. Reduce context length.
2. Reduce per-device batch size.
3. Reduce number of generated completions.
4. Reduce LoRA rank when appropriate.
5. Increase gradient accumulation to recover optimizer batch size.
6. Use stronger hardware or SSH mode.

Record every reduction in the launch plan.
