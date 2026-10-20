---
description: Training orchestration, metrics, curriculum, and checkpoint workflow
globs: pendulum_neat/training/**/*.py,training/**/*.py,pendulum_neat/evaluator.py,pendulum_neat/checkpoints.py
alwaysApply: false
---

# Training Pipeline

## Entry

`pendulum_neat.cli:cmd_train` → `pendulum_neat.training.runner.train()` → `TrainingRun.run()`.

## TrainingRun responsibilities

- Logger to `run_dir/logs/training_<timestamp>.log`
- `MetricsWriter` → `metrics.jsonl` (one JSON object per generation)
- Fields: `generation`, `avg_fitness`, `best_fitness`, `best_time_above`, `species`, `gravity`, `friction`, `curriculum_stage`, `boundary_exit_rate`, `max_cart_abs`
- `CurriculumManager` from `training.curriculum` (canonical import path)
- Checkpointing via `CheckpointStore` at `checkpoint_frequency`
- Optional trajectory clips in `clips/` when `record_every > 0`
- `training_progress.png` via matplotlib at end

## Resume

`pendulum-neat train --resume output/runs/<run>/checkpoint_final.pkl` restores population + curriculum state.

## Fitness evaluation

Always delegate to `self.evaluator.evaluate_genome()` with current curriculum gravity/friction. Never inline physics loops in the runner.

## Stagnation / early stop

Controlled by `neat.patience`, `neat.fitness_threshold`, `neat.no_fitness_termination` in config.

## Adding training features

- New per-generation metrics → extend `MetricsWriter` schema and document the JSONL fields.
- New stopping criteria → implement in `TrainingRun.run()` loop, add smoke test coverage.
- Do not block the evolution loop on viz or network I/O — keep recording optional/async-friendly.

## Outputs (gitignored)

All artifacts under `output/runs/<timestamp>/` — never reference absolute user paths in code.
