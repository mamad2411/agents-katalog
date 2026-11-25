---
description: Compare two LongMemEval runs - diff scorecards, harness_config, and per-question-type accuracy
---

# LongMemEval Compare Runs

## Step 1: Resolve venv. Parse two positional args: `<runIdA> <runIdB>`.

## Step 2: Load both run directories

```bash
$VENV_PYTHON -c "
import json
from pathlib import Path

def load(run_id):
    d = Path('.longmemeval-benchmarks/runs') / run_id
    return {
        'meta': json.load(open(d / 'run-meta.json')),
        'card': json.load(open(d / 'scorecard.json')),
    }

A = load('<RUN_A>')
B = load('<RUN_B>')
print(json.dumps({'A': A, 'B': B}, indent=2))
"
```

If `scorecard.json` is missing for a run, invoke the `report` skill on it first.

## Step 3: Produce diff table

Print markdown:

```
# Run Comparison

|  | A ({runA}) | B ({runB}) | Delta |
|---|---|---|---|
| variant | ... | ... | |
| target model | ... | ... | |
| judge model | ... | ... | |
| n_evaluated | ... | ... | +/- |
| overall_accuracy | ... | ... | +/-.XXX |
| single-session-user | ... | ... | +/- |
| single-session-assistant | ... | ... | +/- |
| multi-session | ... | ... | +/- |
| temporal-reasoning | ... | ... | +/- |
| knowledge-update | ... | ... | +/- |
| preference | ... | ... | +/- |
| abstention | ... | ... | +/- |
```

Also diff `harness_config` (model / plugins / skills / mcp_servers) and surface added/removed entries.

## Step 4: Highlights

Print the top-3 question types with the largest positive and negative deltas.
