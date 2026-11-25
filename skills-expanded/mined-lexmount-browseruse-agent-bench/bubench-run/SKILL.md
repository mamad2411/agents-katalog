---
name: bubench-run
description: Use this skill whenever the user describes a benchmark experiment using any combination of these parameters — agent (e.g. browser-use, skyvern), model (e.g. deepseek, minimax, claude, gemini, gpt), data/benchmark (e.g. LexBench-Browser), browser (e.g. Chrome-Local, lexmount), and tasks (specific IDs or "all"). Trigger phrases include "跑实验 agent=xxx model=xxx", "跑实验 agent xxx model xxx", "run [model] on [tasks]", "eval [model] results", "re-run [model]", or any request that specifies an agent + model + task set to execute or evaluate. Also triggers on requests to chain run→eval pipelines, check experiment progress, or read final results.
---

# BrowserUse-Bench Run & Eval Workflow

This skill guides running benchmark experiments on `browseruse-bench`: launching agent runs, evaluating results, and chaining multiple models in sequence — all using background processes and monitors so Claude stays responsive while jobs run.

## Key Commands

```bash
# Run a model on specific tasks (background)
uv run scripts/run.py --agent browser-use --data LexBench-Browser \
  --mode specific --model-name <model-name> \
  --task-ids <ids...> \
  > output/logs/run/<label>.log 2>&1 &

# Evaluate results (background)
uv run scripts/eval.py --agent browser-use --data LexBench-Browser \
  --model-id <model-id> \
  > output/logs/eval/<label>.log 2>&1 &

# Evaluate a specific timestamp directory (for incremental/second passes)
uv run scripts/eval.py --agent browser-use --data LexBench-Browser \
  --model-id <model-id> --timestamp <YYYYMMDD_HHMMSS> \
  > output/logs/eval/<label>.log 2>&1 &
```

## Model Name → Model ID Mapping (from config.yaml)

| `--model-name` | `--model-id` (in experiments path) |
|----------------|--------------------------------------|
| `deepseek`     | `deepseek-v4-pro`                    |
| `minimax`      | `MiniMax-M2.7`                       |
| `claude`       | `dmx-claude-opus-4-7`                |
| `gemini`       | `gemini-2.5-pro`                     |
| `gpt`          | `gpt-5.5`                            |

Always check `config.yaml` to confirm the current `model_id` before running eval — it must match the directory name under `experiments/`.

## Output Paths

```
experiments/LexBench-Browser/All/browser-use/<model-id>/<timestamp>/
  tasks/                     # one subdir per task
  tasks_eval_result/
    eval.log                 # live eval progress
    task_gpt-5.4_per_task_threshold_stepwise_summary.json
```

Run logs: `output/logs/run/<timestamp>.log`  
Eval logs: `output/logs/eval/<label>.log`

## Monitoring Pattern

Always use `Monitor` (not polling loops) to track background jobs.

**Run progress** (persistent — tasks take hours):
```bash
tail -f output/logs/run/<label>.log | grep --line-buffered \
  -E "\[[0-9]+/N\]\[[0-9]+\] (completed|failed)|Run complete|ERROR"
```

**Eval progress** (non-persistent — usually finishes in <1 hour):
```bash
tail -f experiments/.../tasks_eval_result/eval.log | grep --line-buffered \
  -E "PASS|FAIL|SUCCESS:|ERROR"
```

**Wait for process to exit** (to auto-chain next step):
```bash
until ! pgrep -f "eval.py.*<model-id>" > /dev/null 2>&1; do sleep 10; done \
  && echo "EVAL DONE"
```

**Wait for a task directory to appear** (before second eval pass):
```bash
until [ -d "experiments/.../tasks/<task-id>" ]; do sleep 10; done \
  && echo "TASK READY"
```

## Sequential Pipeline for Multiple Models

When chaining run→eval across several models, do them one at a time:

1. Start model A run (background + persistent monitor)
2. When run completes → start model A eval (background + monitor)
3. When eval completes → start model B run
4. Repeat

Don't start the next model's run until the current eval finishes — this avoids Chrome browser contention and keeps logs clean.

## Incremental Eval (the key trick)

By default, `eval.py` **skips tasks that already have results**. This enables:

- **First pass**: eval starts as soon as most tasks are done, skipping tasks not yet written
- **Second pass**: re-run eval after the run fully completes — it only evaluates the missing tasks (the ones that were still running during the first pass)
- **No `--force-reeval` needed** unless you actually want to re-score everything

Use `--timestamp <YYYYMMDD_HHMMSS>` to target a specific run directory when there are multiple timestamps for the same model.

## Reading Final Results

```bash
python3 -c "
import json
with open('experiments/LexBench-Browser/All/browser-use/<model-id>/<timestamp>/tasks_eval_result/task_gpt-5.4_per_task_threshold_stepwise_summary.json') as f:
    d = json.load(f)
s = d['overall_statistics']
print(f'Tasks: {s[\"total_tasks\"]}, Success: {s[\"successful_tasks\"]}, Rate: {s[\"success_rate\"]}%')
print(f'Successful IDs: {d[\"task_list\"][\"successful_task_ids\"]}')
"
```

Or use `find_latest_tasks_dir()` logic: latest timestamp = `max()` by directory name.

## Error Handling — What to Ignore

The following appear constantly in run logs and are **self-recovering** — don't intervene:
- `Result failed N/6 times: validation error` — model JSON parse retry, always recovers
- `net::ERR_CONNECTION_RESET / ERR_CONNECTION_TIMED_OUT` — network blip, agent retries
- `CDP requests failed or timed out: ax_tree` — browser DOM timeout, recovers on next step
- `Navigation failed: event handler timed out` — slow site, agent retries
- `Task X timed out after 600 seconds` — hit max time, still recorded as completed

Watch only for `[N/N][task-id] completed` or `Run complete` lines to know real progress.

If a task produces `ERROR [Agent] ❌ Stopping due to 5 consecutive failures` followed immediately by `[N/N][task-id] completed`, it recovered — no action needed.

## Standard Task Set (50 IDs)

The default task set used in LexBench-Browser experiments:

```
83 85 87 89 94 124 125 128 144 148 150 163 166 172 174 175 179 180 182 183
184 187 188 189 196 197 199 205 206 208 209 210 212 213 216 217 218 221 223
227 233 236 241 255 263 276 292 294 298 304
```

Pass as `--task-ids` (space-separated). When user says "tasks=50ids" or "standard tasks", use this list.

## Pre-flight Checklist

Before starting a run:
1. Confirm `browser_id: Chrome-Local` in `config.yaml` (or the intended browser)
2. Confirm `active_model` is set to the intended model name under the agent section
3. Or use `--model-name <name>` to override without editing config
4. Check `output/logs/` for any existing run/eval processes still active: `ps aux | grep -E "run.py|eval.py" | grep -v grep`
