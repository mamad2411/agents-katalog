---
name: plamen-l1
description: "Launch the Plamen deterministic L1 infrastructure audit pipeline"
---

# plamen-l1

Use the base plamen skill and `plamen/plamen-l1-wizard.md`. New configs must set `pipeline = l1` and `cli_backend = codex`.

Do not manually orchestrate phases. Do not spawn audit agents yourself.
Do not ask a model-selection question from inside Codex.
