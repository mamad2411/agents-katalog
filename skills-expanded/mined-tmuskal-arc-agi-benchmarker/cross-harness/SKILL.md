---
description: Cross-harness benchmarking for LongMemEval - emit instruction packs for Codex/Gemini/OpenCode and ingest their results into a comparable scorecard
---

# LongMemEval Cross-Harness

## Step 1: Parse args

| Argument | Values |
|---|---|
| `<action>` | `emit` / `import` |
| `--harness` | `codex` / `gemini` / `opencode` |
| `--run-id` | required for `import` |
| `--results-path` | path to foreign `item-results.jsonl` (for `import`) |

## Step 2: `emit` — write instruction pack

Produce `.longmemeval-benchmarks/cross-harness/<harness>-instructions.md` containing:

1. Link to the LongMemEval repo.
2. The exact dataset file to use (`cfg.datasetPath`).
3. The exact schema for `item-results.jsonl` (copy from `SPEC.md`).
4. Instructions: for each item, produce a hypothesis. Emit one jsonl line per item with the schema fields. Do NOT judge — return the raw hypotheses. The Claude harness will re-judge for fairness.
5. The output jsonl file they should produce, and how to hand it back.

## Step 3: `import` — judge foreign hypotheses

Re-judge the foreign hypotheses with our judge (so judge model is constant across harnesses):

```bash
$VENV_PYTHON -c "
import json, sys, uuid
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, 'plugins/longmemeval-benchmarker/scripts')
from checkpoint_io import append_item_result, mark_completed, write_atomic_json
from judge_shim import judge

cfg = json.load(open('.longmemeval-benchmarks/config.json'))
harness = '<HARNESS>'
run_id = '<RUN_ID>'
foreign = Path('<RESULTS_PATH>')

run_dir = Path(cfg['runs_dir']) / run_id
run_dir.mkdir(parents=True, exist_ok=True)
meta = {
    'schemaVersion': '1.0.0', 'runId': run_id, 'harness': harness,
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'datasetVariant': cfg['datasetVariant'], 'datasetPath': cfg['datasetPath'],
    'maxEvals': cfg['maxEvals'], 'seed': cfg['seed'],
    'targetModel': 'foreign', 'judgeModel': cfg['judgeModel'], 'judgeProvider': cfg['judgeProvider'],
    'harness_config': {'model': 'foreign', 'plugins': [], 'skills': [], 'mcp_servers': []},
    'status': 'running', 'plugin_version': '1.0.0',
}
write_atomic_json(run_dir / 'run-meta.json', meta)

for line in foreign.read_text().splitlines():
    if not line.strip(): continue
    r = json.loads(line)
    j = judge(r['question_type'], r['question'], r['answer'], r['hypothesis'],
              Path(cfg['longmemeval_root']),
              provider=cfg['judgeProvider'], model=cfg['judgeModel'])
    r['judgment'] = {'model': j['model'], 'label': j['label'], 'raw': j['raw']}
    r.setdefault('schemaVersion', '1.0.0')
    append_item_result(run_dir, r)
    mark_completed(run_dir, r['question_id'])

meta['status'] = 'completed'
write_atomic_json(run_dir / 'run-meta.json', meta)
print('imported run', run_id)
"
```

## Step 4: Report + compare

Run `/longmemeval-report <run_id>` on the imported run, then `/longmemeval-compare-runs <claude_run> <imported_run>`.
