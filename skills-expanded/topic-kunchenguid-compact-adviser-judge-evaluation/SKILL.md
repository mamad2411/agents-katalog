---
name: judge-evaluation
description: Use when changing or evaluating judge prompts, scoring thresholds, usage floors, or judgment eval corpora.
user-invocable: false
metadata:
  internal: true
---

- Judge design rule, measured: two one-sentence atomic questions composed in code beat any single question that folds two judgments together (TypeSafe's own guidance). Hill-climb prompt changes with `eval/tools/earn.py` (paired bootstrap) and read the usage-floor ladder with `eval/tools/schedule.py`; a clause stays only if it earns its place.
- Judgment eval harness: `packages/pi-extension/eval/`. Session transcripts, labels, worksheets, and results stay in gitignored `eval/local/`. See that README for the corpus contract and label rubric.
