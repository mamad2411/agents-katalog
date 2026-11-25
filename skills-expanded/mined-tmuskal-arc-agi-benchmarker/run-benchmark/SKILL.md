---
description: Execute a LongMemEval benchmark run - drives per-item hypothesis generation and LLM-as-judge scoring with checkpointing, resumable, capped at 500 items by default
---

# LongMemEval Run Benchmark

You are driving a LongMemEval run. Per-item: generate a hypothesis with the target model, judge it with the judge model, append to `item-results.jsonl`, mark complete in `questions_completed.jsonl`.

> All relative paths assume the project root.

## Step 1: Pre-flight

Detect venv:

```bash
if [ -f ".longmemeval-venv/bin/python" ]; then
  VENV_PYTHON=".longmemeval-venv/bin/python"
elif [ -f ".longmemeval-venv/Scripts/python.exe" ]; then
  VENV_PYTHON=".longmemeval-venv/Scripts/python.exe"
else
  echo "ERROR: venv not found. Run /longmemeval-setup first."; exit 1
fi
```

Read config:

```bash
$VENV_PYTHON -c "import json; print(json.dumps(json.load(open('.longmemeval-benchmarks/config.json')), indent=2))"
```

## Step 2: Parse User Arguments

| Argument | Default | Notes |
|---|---|---|
| `--variant` | `longmemeval_s` | one of `_s / _m / _oracle` |
| `--max` | 500 | cap sequential evals |
| `--target-model` | config.targetModel | e.g. `claude-opus-4-6` |
| `--judge-model` | config.judgeModel | |
| `--run-id` | new UUID | supply to resume |

## Step 3: Resolve / Create Run Directory

If `--run-id` supplied, reuse `.longmemeval-benchmarks/runs/<runId>/`. Otherwise generate a UUID and create the directory with an initial `run-meta.json` (status=`running`).

Write `run-meta.json` via the atomic helper in `scripts/checkpoint_io.py`. Schema per `SPEC.md`.

## Step 4: Load Dataset & Filter Completed

```bash
PLUGIN=plugins/longmemeval-benchmarker
$VENV_PYTHON -c "
import json, sys
from pathlib import Path
sys.path.insert(0, '$PLUGIN/scripts')
from checkpoint_io import load_completed, filter_pending

cfg = json.load(open('.longmemeval-benchmarks/config.json'))
data_path = Path(cfg['datasetPath'])
items = json.load(open(data_path))
run_dir = Path(cfg['runs_dir']) / '$RUN_ID'
done = load_completed(run_dir)
pending = filter_pending(items, done)
print(f'total={len(items)} done={len(done)} pending={len(pending)}')
"
```

## Step 5: Drive the Loop

For each pending item (capped at `maxEvals`):

1. Call `generation_driver.generate_hypothesis(item, provider, model)` — returns hypothesis + tokens + latency.
2. Call `judge_shim.judge(question_type, question, answer, hypothesis, longmemeval_root, ...)` — returns `{model, provider, label, raw}`.
3. Build item result row (schema in `SPEC.md`).
4. `append_item_result(run_dir, row)` then `mark_completed(run_dir, question_id)`.

Minimal driver script (invoke from bash):

```bash
$VENV_PYTHON -c "
import json, sys, uuid
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, 'plugins/longmemeval-benchmarker/scripts')
from checkpoint_io import load_completed, append_item_result, mark_completed, write_atomic_json, filter_pending
from generation_driver import generate_hypothesis
from judge_shim import judge

cfg = json.load(open('.longmemeval-benchmarks/config.json'))
run_id = '$RUN_ID'
run_dir = Path(cfg['runs_dir']) / run_id
run_dir.mkdir(parents=True, exist_ok=True)

items = json.load(open(cfg['datasetPath']))
done = load_completed(run_dir)
pending = filter_pending(items, done)[:int(cfg.get('maxEvals', 500))]

lm_root = Path(cfg['longmemeval_root'])
tgt_provider = cfg['targetProvider']; tgt_model = cfg['targetModel']
judge_provider = cfg['judgeProvider']; judge_model = cfg['judgeModel']

for it in pending:
    qid = str(it['question_id']); qtype = it['question_type']
    gen = generate_hypothesis(it, provider=tgt_provider, model=tgt_model)
    j = judge(qtype, it['question'], it['answer'], gen['hypothesis'], lm_root,
              provider=judge_provider, model=judge_model)
    row = {
        'schemaVersion': '1.0.0',
        'question_id': qid, 'question_type': qtype,
        'question': it['question'], 'answer': it['answer'],
        'hypothesis': gen['hypothesis'],
        'judgment': {'model': j['model'], 'label': j['label'], 'raw': j['raw']},
        'latencyMs': gen['latencyMs'], 'tokensIn': gen['tokensIn'], 'tokensOut': gen['tokensOut'],
    }
    append_item_result(run_dir, row)
    mark_completed(run_dir, qid)
    print(f'{qid} [{qtype}] -> {j[\"label\"]}')

print('done')
"
```

## Step 6: Finalize run-meta.json

Set `status=completed`, `duration_seconds`. Atomic write.

## Step 7: Scorecard

Invoke the `report` skill or directly:

```bash
$VENV_PYTHON plugins/longmemeval-benchmarker/scripts/scorecard.py \
  .longmemeval-benchmarks/runs/$RUN_ID <N_TOTAL> <VARIANT> <RUN_ID>
```

## Notes

- Resume: re-run with the same `--run-id`. The completed set filters already-judged items.
- If a call fails after `backoff` exhausts retries, write `run-meta.status=failed` and stop; re-run to resume.
- Do not modify upstream files.
