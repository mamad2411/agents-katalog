---
description: Generate a scorecard from a completed LongMemEval run - computes overall accuracy + per-question-type accuracy and writes scorecard.json
---

# LongMemEval Report

## Step 1: Resolve venv and config.

## Step 2: Parse args

| Argument | Default | Notes |
|---|---|---|
| `<run_id>` | `latest` | UUID or `latest` |
| `--format` | `markdown` | `markdown` / `json` / `summary` |

## Step 3: Resolve `latest`

Pick the most recently modified directory under `.longmemeval-benchmarks/runs/`.

```bash
$VENV_PYTHON -c "
from pathlib import Path
d = Path('.longmemeval-benchmarks/runs')
runs = sorted([p for p in d.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
print(runs[0].name if runs else '')
"
```

## Step 4: Compute + write scorecard.json

```bash
$VENV_PYTHON -c "
import json, sys
from pathlib import Path
sys.path.insert(0, 'plugins/longmemeval-benchmarker/scripts')
from scorecard import compute
from checkpoint_io import write_atomic_json

run_id = '<RUN_ID>'
run_dir = Path('.longmemeval-benchmarks/runs') / run_id
meta = json.load(open(run_dir / 'run-meta.json'))
variant = meta.get('datasetVariant', 'longmemeval_s')
cfg = json.load(open('.longmemeval-benchmarks/config.json'))
n_total = len(json.load(open(cfg['datasetPath'])))
card = compute(run_dir, n_total, variant, run_id)
write_atomic_json(run_dir / 'scorecard.json', card)
print(json.dumps(card, indent=2))
"
```

## Step 5: Render markdown

```
# LongMemEval Run {runId}

- Dataset: {datasetVariant}
- Evaluated: {n_evaluated} / {n_total}
- Overall accuracy: {overall_accuracy:.3f}

## Per question-type accuracy

| Type | Accuracy | n |
|---|---|---|
| single-session-user | ... | ... |
| single-session-assistant | ... | ... |
| multi-session | ... | ... |
| temporal-reasoning | ... | ... |
| knowledge-update | ... | ... |
| preference | ... | ... |
| abstention | ... | ... |
```

For `--format json`, print `scorecard.json` raw. For `--format summary`, print a single line: `runId  variant  n_eval/n_total  overall_acc`.
