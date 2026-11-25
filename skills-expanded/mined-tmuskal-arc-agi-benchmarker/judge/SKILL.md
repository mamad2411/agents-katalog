---
description: LLM-as-judge shim for LongMemEval - wraps upstream get_anscheck_prompt and calls Anthropic (default) or OpenAI (fallback) with exponential backoff
---

# LongMemEval Judge

You are invoking the judge shim manually (e.g. to re-score an existing `item-results.jsonl` with a different judge model). Normally the `run-benchmark` skill calls the judge inline.

## Step 1: Resolve venv and config (same pattern as other skills).

## Step 2: Choose provider + model

- Default: `anthropic` / `claude-opus-4-6`.
- Fallback: `openai` / `gpt-4o`.
- The shim auto-falls-back if the chosen provider's API key is unset, or if the call fails after 6 backoff tries.

## Step 3: Single-item smoke test

```bash
$VENV_PYTHON -c "
import sys, json
sys.path.insert(0, 'plugins/longmemeval-benchmarker/scripts')
from judge_shim import judge
from pathlib import Path

out = judge(
    question_type='single-session-user',
    question='What is my dog\\'s name?',
    answer='Rex',
    hypothesis='Your dog is named Rex.',
    longmemeval_root=Path('longmemeval'),
    provider='anthropic',
    model='claude-opus-4-6',
)
print(json.dumps(out, indent=2))
"
```

## Step 4: Re-judge an existing run

Iterate over `item-results.jsonl`, call `judge()` with a new model, write to `item-results.<newmodel>.jsonl` alongside the original (do NOT overwrite).

```bash
$VENV_PYTHON -c "
import sys, json
from pathlib import Path
sys.path.insert(0, 'plugins/longmemeval-benchmarker/scripts')
from judge_shim import judge
from checkpoint_io import append_jsonl

run_dir = Path('.longmemeval-benchmarks/runs/<RUN_ID>')
out_path = run_dir / 'item-results.rejudge.jsonl'
for line in (run_dir / 'item-results.jsonl').read_text().splitlines():
    r = json.loads(line)
    j = judge(r['question_type'], r['question'], r['answer'], r['hypothesis'],
              Path('longmemeval'), provider='openai', model='gpt-4o')
    r['judgment'] = {'model': j['model'], 'label': j['label'], 'raw': j['raw']}
    append_jsonl(out_path, r)
print('wrote', out_path)
"
```

## Notes

- The shim imports `get_anscheck_prompt` from `longmemeval/src/evaluation/evaluate_qa.py` (L21-47). Do not reimplement.
- `backoff.expo` with `max_tries=6` + full jitter is used on every API call.
