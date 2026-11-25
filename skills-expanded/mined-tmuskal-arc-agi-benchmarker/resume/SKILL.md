---
description: Detect an incomplete LongMemEval run and continue it from the last checkpoint
---

# LongMemEval Resume

## Step 1: Resolve venv.

## Step 2: Find the most recent incomplete run

```bash
$VENV_PYTHON -c "
import json
from pathlib import Path
d = Path('.longmemeval-benchmarks/runs')
incomplete = []
for r in sorted(d.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
    meta_path = r / 'run-meta.json'
    if not meta_path.exists(): continue
    meta = json.load(open(meta_path))
    if meta.get('status') != 'completed':
        incomplete.append((r.name, meta.get('status'), meta.get('datasetVariant')))
for name, st, v in incomplete[:5]:
    print(f'{name}  status={st}  variant={v}')
"
```

## Step 3: Pick target run

If args include a `<run_id>`, use that. Else pick the most recent incomplete run.

## Step 4: Continue

Invoke the `run-benchmark` skill with `--run-id <runId>`. The checkpoint loader filters out `question_id`s already present in `questions_completed.jsonl`, so execution picks up where it left off. The `maxEvals` cap applies to the REMAINING items in the cap, not the already-done ones.

## Step 5: Finalize

Once finished, rewrite `run-meta.json` with `status=completed` and invoke the `report` skill.
