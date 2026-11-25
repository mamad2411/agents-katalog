# Inspect Evaluation Harness Starter

Use this skill to run a deterministic Inspect evaluation harness over toy scientific-agent cases and compare a candidate solver against a weaker baseline.

## What This Skill Does

- defines a small local Inspect task set without external model credentials
- evaluates two deterministic solver variants on the same cases
- writes machine-readable accuracy summaries plus Inspect log files for both runs

## When To Use It

- when you need a runnable `evaluation-harnesses-for-scientific-agents` starter
- when you want a local Inspect example before wiring in real agents or model-backed solvers
- when you need a stable comparison harness for repository tests

## Run

```bash
./slurm/envs/agents/bin/python skills/scientific-agents-and-automation/inspect-evaluation-harness-starter/scripts/run_inspect_evaluation_harness.py \
  --cases skills/scientific-agents-and-automation/inspect-evaluation-harness-starter/examples/toy_eval_cases.json \
  --summary-out scratch/agents/inspect_evaluation_harness_summary.json \
  --log-dir scratch/agents/inspect-eval-logs
```

## Notes

- This starter intentionally avoids external model APIs so it can run in the repository sandbox.
- The candidate and baseline solvers are both deterministic; the purpose is to verify the harness and comparison surface, not to benchmark large models.
