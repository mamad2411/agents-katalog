---
name: pi-skillopt
description: "Use when: running SkillOpt, training a skill, evaluating a skill, using the local mitko model on port 8000, working with the dotnetdebug benchmark, adding a benchmark, adding a backend, or optimizing agent instructions with SkillOpt in this repository."
---

# PI SkillOpt Operator

Use this skill when the user wants the agent to operate the **SkillOpt** repository: run experiments, evaluate skills, configure local models, inspect outputs, or extend the repo with new benchmarks/backends.

## Core repo facts

- SkillOpt optimizes a **skill document / system prompt**, not model weights.
- The repo supports a generic local OpenAI-compatible backend named `openai_compat`.
- The local example model config is `configs/dotnetdebug/local_mitko.yaml`.
- That config uses model `mitko` at `http://localhost:8000/v1` for both optimizer and target.
- The runnable sample benchmark is `dotnetdebug`.
- The sample dataset is `data/dotnetdebug/tasks.json`.
- The seed skill is `skillopt/envs/dotnetdebug/skills/initial.md`.
- Training entry point: `scripts/train.py`.
- Eval-only entry point: `scripts/eval_only.py`.

## Default workflow

1. Identify the user goal:
   - run a SkillOpt training job
   - evaluate an existing skill
   - inspect outputs from a previous run
   - add or modify a benchmark
   - add or modify a backend
2. Confirm the benchmark, backend, target model, and desired output directory.
3. Prefer a **small smoke test first** before a larger run.
4. Use existing configs when possible instead of inventing new ones.
5. After a run, report:
   - exact command used
   - output directory
   - best skill path
   - headline metrics
   - next recommended action

## Local model workflow

When the user asks to use a local model or mentions `mitko`, `localhost:8000`, or an OpenAI-compatible endpoint:

- Prefer `model.backend: openai_compat`.
- Set both `optimizer_backend` and `target_backend` to `openai_compat` unless the user explicitly wants a mixed setup.
- Use `configs/dotnetdebug/local_mitko.yaml` when the task is the built-in dotnet debugging example.
- Keep smoke tests small, for example:
  - `train.num_epochs=1`
  - `train.batch_size=2`
  - `gradient.analyst_workers=1`
  - `gradient.minibatch_size=2`
  - `env.workers=1`
  - `env.limit=2`

## Common commands

Activate the environment first if `.venv` exists:

```bash
source .venv/bin/activate
```

Small local training run:

```bash
python3 scripts/train.py \
  --config configs/dotnetdebug/local_mitko.yaml \
  --cfg-options \
    train.num_epochs=1 \
    train.batch_size=2 \
    gradient.analyst_workers=1 \
    gradient.minibatch_size=2 \
    env.workers=1 \
    env.limit=2 \
    optimizer.learning_rate=2 \
    env.out_root=outputs/dotnetdebug_smoke
```

Eval-only run:

```bash
python3 scripts/eval_only.py \
  --config configs/dotnetdebug/local_mitko.yaml \
  --skill outputs/dotnetdebug_smoke/best_skill.md \
  --split test \
  --cfg-options env.limit=2 env.workers=1 env.out_root=outputs/dotnetdebug_eval_smoke
```

## Extension workflow

When adding a new benchmark:

- Create files under `skillopt/envs/<benchmark>/`.
- Add config under `configs/<benchmark>/default.yaml`.
- Register the adapter in both:
  - `scripts/train.py`
  - `scripts/eval_only.py`
- Add or update docs when the new benchmark is user-facing.

When adding a new backend:

- Add the backend module under `skillopt/model/`.
- Update backend normalization and defaults in `skillopt/model/common.py`.
- Update allowed runtime backends in `skillopt/model/backend_config.py`.
- Update dispatch in `skillopt/model/__init__.py`.
- Expose config in `skillopt/config.py`, `configs/_base_/default.yaml`, and CLI entry points.

## Guardrails

- Do not describe SkillOpt as model fine-tuning.
- Do not start with a long expensive run if a smoke test can validate the setup first.
- Prefer repo-native paths and configs over ad hoc scripts.
- If editing benchmark/backend code, validate syntax/errors after changes.
- If a run fails, report the **first concrete failure point** and propose the smallest next fix.

## Response checklist

Before finishing, make sure the response includes:

- the chosen benchmark/config/backend
- the exact command(s) to run
- where outputs will be written
- what artifact to inspect next (`best_skill.md`, eval summary, predictions, patches, etc.)
