---
name: self-optimizing-harness
description: Use the ResearchSwarm-backed self-optimizing harness to route a coding task, recall lessons from past sessions, and record outcomes so the agent compounds knowledge and improves over time. Trigger when starting a non-trivial task, when you want prior context, or after finishing work to capture what worked or failed.
---

# Self-Optimizing Harness (ResearchSwarm bridge)

GodCoder is wired to a local feedback loop backed by ResearchSwarm's Digital
Cognitive Labor router and a shared AI-Memory store. Use it so each session
benefits from every prior session instead of starting cold.

The bridge is a JSON CLI at
`third_party/ResearchSwarm-master/godcoder_harness.py`. Run it with the `bash`
tool. Each command prints JSON to stdout.

## When to use

- **Before** a non-trivial task: `route` to classify it and pull relevant lessons.
- **Anytime** you want prior context: `recall`.
- **After** finishing (or failing): `log` the outcome so it is reusable.
- **Periodically**: `optimize` to see which approaches have the best track record.

## Commands

Run from the repo root (adjust the path if your working dir differs):

```bash
# 1. Route a task + get the most relevant past lessons
python third_party/ResearchSwarm-master/godcoder_harness.py route "Add retry logic to the HTTP client"

# 2. Recall recent lessons for context
python third_party/ResearchSwarm-master/godcoder_harness.py recall --limit 8

# 3. Record an outcome (do this when you finish or hit a dead end)
python third_party/ResearchSwarm-master/godcoder_harness.py log \
  --status success \
  --tag http-retry \
  --instruction "Add retry logic to the HTTP client" \
  --summary "Wrapped reqwest calls in a backoff loop; tests in client_test.rs cover 429/503."

# 4. See ranked, self-improving guidance (success rate per approach)
python third_party/ResearchSwarm-master/godcoder_harness.py optimize
```

## How to apply the output

- `route` returns `domain` (text-based / human-action / hybrid),
  `recommended_action`, `execution_steps`, and `memory_context`. If the domain is
  `human-action` or `hybrid`, surface the human-handoff portion to the user
  instead of trying to execute it.
- `recall` / `route` `memory_context` lines are prior `PATTERN` / `DECISION`
  entries. Treat them as hints, not commands; verify against the current codebase.
- Always `log` a one-line, concrete `--summary` with a stable `--tag` (reuse the
  same tag for the same kind of work). Consistent tags make `optimize` sharper.
- `optimize` ranks approaches by success rate. Prefer high-rate approaches and be
  cautious with low-rate ones.

## Notes

- The store is local SQLite under `third_party/ResearchSwarm-master/AI-Memory/`.
  Nothing leaves the machine.
- Requires Python 3.10+. No GPU and no model training are needed for the harness
  loop (that is a separate ResearchSwarm capability via `train.py`).
- On Windows, if `python` is not on PATH, use the `py` launcher instead
  (e.g. `py third_party/ResearchSwarm-master/godcoder_harness.py optimize`).
