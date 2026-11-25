---
name: infermind-artifact-export
description: Export and validate InferMind skill-driven run artifacts, including InferIR, trajectory summaries, stage decisions, and validation reports.
---

# Artifact Export

Use this skill at the end of each run or when validating an intermediate run directory.

Export summary artifacts:

```bash
python plugins/infermind/scripts/export_run.py --infer-ir infer_ir.json --run-dir runs/<task>/<timestamp>
```

Validate:

```bash
python plugins/infermind/scripts/validate_artifacts.py --run-dir runs/<task>/<timestamp> --min-nodes 6
```

Artifacts should be readable and sufficient for a future Codex session to resume the optimization without relying on chat history.
