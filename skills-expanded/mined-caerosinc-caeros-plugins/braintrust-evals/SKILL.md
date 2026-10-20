---
name: braintrust-evals
description: Write and run Braintrust evaluations with the Eval() SDK, custom scorers, and autoevals in TypeScript or Python. Use when creating experiments, scoring model outputs, or comparing prompt and model changes.
---

# Braintrust Evals

An eval has three parts: **data** (test cases with `input`, optional
`expected`, `metadata`), **task** (the function under test, usually an LLM
call), and **scores** (functions returning 0 to 1). Each run creates an
experiment in a project for side-by-side comparison.

## TypeScript

```typescript
// my_eval.eval.ts
import { Eval, initDataset } from "braintrust";
import { Factuality } from "autoevals";

Eval("My Project", {
  experimentName: "prompt-v2",
  data: initDataset("My Project", { dataset: "My dataset" }),
  // or inline: data: () => [{ input: "...", expected: "..." }],
  task: async (input) => await callModel(input),
  scores: [Factuality],
  metadata: { model: "gpt-5-mini" },
  trialCount: 3,
});
```

Run with `bt eval my_eval.eval.ts` (add `--watch` for re-runs on save).

## Python

```python
# eval_qa.py
from braintrust import Eval, init_dataset
from autoevals import Factuality

Eval(
    "My project",
    experiment_name="prompt-v2",
    data=init_dataset(project="My project", name="My dataset"),
    task=lambda input: call_model(input),
    scores=[Factuality],
    metadata={"model": "gpt-5-mini"},
    trial_count=3,
)
```

Run with `bt eval eval_qa.py`.

## Scorers

Custom scorer: a plain function over `(input, expected, output)` returning a
number in [0, 1] (or a dict/object with `name` and `score`):

```python
def exact_match(input, expected, output):
    return 1 if output == expected else 0
```

The `autoevals` library (`npm i autoevals` / `pip install autoevals`) ships
maintained scorers: heuristic (`Levenshtein`, `ExactMatch`, JSON validity)
and LLM-based (`Factuality`, `ClosedQA`, `Battle`, moderation, RAG metrics).
LLM-based scorers need a model provider key configured (env var or Braintrust
AI proxy). Mix several scorers per eval; each becomes a column.

## Useful knobs

- `trialCount` / `trial_count`: run each input N times to measure variance in
  nondeterministic tasks.
- `metadata`: record model, prompt version, git SHA; filterable in the UI and
  essential for comparing experiments later.
- `expected` is optional: scorers that only inspect `output` (format checks,
  moderation) work without ground truth.
- Data can be an inline array, a generator, or `initDataset` referencing a
  dataset stored in Braintrust (versioned, editable in the UI).

## Workflow

1. Start with 10 to 20 representative cases inline, then promote to a stored
   dataset.
2. Add failing production logs to the dataset (hill climbing): `expected` can
   be auto-populated from prior good outputs.
3. Run on every prompt or model change; open the experiment diff view to see
   per-case regressions, not just aggregate score.
4. Verify current SDK signatures via the bundled Braintrust MCP server's docs
   search when in doubt; the SDK evolves quickly.
