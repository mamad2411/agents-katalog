---
description: List and preview LongMemEval items - shows dataset stats, per-question-type counts, and a truncated preview of a specific item by question_id
---

# LongMemEval Browse Tests

## Step 1: Resolve venv and config.

## Step 2: Summarize the dataset

```bash
$VENV_PYTHON -c "
import json
from collections import Counter
cfg = json.load(open('.longmemeval-benchmarks/config.json'))
items = json.load(open(cfg['datasetPath']))
print(f'Variant: {cfg[\"datasetVariant\"]}  Path: {cfg[\"datasetPath\"]}  n={len(items)}')
c = Counter(i['question_type'] for i in items)
for qt, n in sorted(c.items()):
    print(f'  {qt:<28} {n}')
"
```

## Step 3: Parse args

| Argument | Default |
|---|---|
| `<question_id>` | none — if omitted, list first 20 question_ids + types |
| `--max-sessions` | 3 |

## Step 4: Preview a specific item (truncated)

```bash
$VENV_PYTHON -c "
import json, sys
cfg = json.load(open('.longmemeval-benchmarks/config.json'))
items = json.load(open(cfg['datasetPath']))
qid = '<QUESTION_ID>'
it = next((x for x in items if x['question_id'] == qid), None)
if not it:
    print('not found'); sys.exit(1)
print('question_type :', it['question_type'])
print('question      :', it['question'])
print('answer        :', it['answer'])
sessions = it.get('haystack_sessions') or []
print(f'sessions      : {len(sessions)}')
for idx, s in enumerate(sessions[:3]):
    print(f'--- session {idx+1} ({len(s)} turns) ---')
    for t in s[:4]:
        c = (t.get('content') or '')[:200]
        print(f'  [{t.get(\"role\")}] {c}')
"
```

## Step 5: Summary output

Always end with one-line dataset summary so the user knows what's loaded. Never dump entire sessions — the `_s` variant is 115k tokens per item.
