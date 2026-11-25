---
name: isaaclab-rl-skillkit
description: Use when developing, customizing, authoring, debugging, reviewing, or porting IsaacLab reinforcement-learning projects that use ManagerBasedRLEnv, DirectRLEnv, DirectMARLEnv, isaaclab_tasks registration, manager terms, direct env hooks, observations, rewards, terminations, events, commands, curriculum, actions, sensors, scenes, RSL-RL wrappers, runner configs, distillation, export, skrl, rl_games, sb3, or version-specific IsaacLab APIs.
---

# isaaclab-rl-skillkit

## Required load order

- Read the repo's `AGENTS.md`, local docs, task docs, and training scripts before editing.
- Start with [selection-guide.md](references/workflow/selection-guide.md) unless the workflow is already proven.
- Then load exactly one workflow map:
  - manager-based -> [manager-based.md](references/workflow/manager-based.md)
  - direct RL or direct MARL -> [direct.md](references/workflow/direct.md)
- Then load [edit-layer-decision-tree.md](references/workflow/edit-layer-decision-tree.md) before choosing files to edit.
- Then load exactly one intent recipe.
- Then load exactly one source router.
- Then load exactly one source leaf doc.
- Only load [official-docs.md](references/fallback/official-docs.md) if local code and skill references are insufficient.

## Load recipes by intent

- Existing manager-based task customization -> [manager-customization.md](references/recipes/manager-customization.md)
- Existing direct RL or direct MARL customization -> [direct-customization.md](references/recipes/direct-customization.md)
- New task or variant -> [task-authoring.md](references/recipes/task-authoring.md), then [manager-task-authoring.md](references/recipes/manager-task-authoring.md) or [direct-task-authoring.md](references/recipes/direct-task-authoring.md)
- RSL-RL wrapper, runner, model, loss, distillation, logging, checkpoint, or export -> [training-extension.md](references/recipes/training-extension.md)
- Cross-layer env/wrapper/runner/model/registration changes -> [architecture-modification.md](references/recipes/architecture-modification.md)
- Nonstandard downstream repo layout -> [repo-portability-guide.md](references/portability/repo-portability-guide.md)
- Debugging or completion checks -> [validation-checklists.md](references/recipes/validation-checklists.md)
- Direct MARL true multi-agent semantics or `skrl`/`rl_games`/`sb3` boundaries -> [scope-boundaries.md](references/recipes/scope-boundaries.md)

## Load source routers by package

- `source/isaaclab/isaaclab` core package -> [router.md](references/source/isaaclab/router.md)
- `source/isaaclab_assets/isaaclab_assets` assets package -> [router.md](references/source/isaaclab_assets/router.md)
- `source/isaaclab_rl/isaaclab_rl` wrappers and backend integrations -> [router.md](references/source/isaaclab_rl/router.md)
- `source/isaaclab_tasks/isaaclab_tasks` task families and registration -> [router.md](references/source/isaaclab_tasks/router.md)
- `source/isaaclab_mimic/isaaclab_mimic` mimic package -> [router.md](references/source/isaaclab_mimic/router.md)

## Working rules

- Treat the local IsaacLab baseline as `2.1.0` when `VERSION` says `2.1.0`.
- Prefer local project patterns, task family structure, and vendored `rsl_rl` code over memory.
- Search by symbols when paths differ: `gym.register`, `ManagerBasedRLEnvCfg`, `DirectRLEnvCfg`, `DirectMARLEnvCfg`, `ObsTerm`, `_get_observations`, `RslRlVecEnvWrapper`.
- Do not collapse intentional newer guidance to the checked-out tree. Mark it as newer than the local baseline and verify it against official docs before using it.
- If runtime validation is needed, use the repo-intended IsaacLab Python entrypoint, not system Python.
