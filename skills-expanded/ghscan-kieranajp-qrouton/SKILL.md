---
name: qrouton-evals
description: Create, change, run, or interpret qrouton's eval/, internal/evalharness/, and cmd/qrouton-eval/ workflows. Do not use for ordinary application or unit-test work.
---

# Work with qrouton evaluations

Read `eval/README.md` before changing or running the harness. Preserve launch/eval prompt parity through `prompts.Stamp`, and keep scenario workspaces as real `session.Manifest` fixtures.

Use `--no-judge` for deterministic structural runs, narrowing by runner and scenario when useful:

```sh
go run ./cmd/qrouton-eval --runner codex --scenario <scenario> --no-judge
```

Pairwise judging and smoke tests invoke authenticated model CLIs. Run them only when that external evidence is requested and the environment is ready; smoke tests use `QROUTON_EVAL_SMOKE=1 go test ./internal/evalharness -run Smoke`.

Evals are opt-in and do not run in CI. Report the mode, runner, scenario, samples, and any judge or authentication evidence that was not run.
