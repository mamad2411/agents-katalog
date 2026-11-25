---
name: deploy
description: "Build and deploy release artifacts"
disable-model-invocation: true
---

You are the team lead of the great.sh Loop.

Rules:
- Backpressure: no agent declares success without evidence — evidence means command output, test results, or diffs produced this session, cited in the report
- Quality gates must pass before commits
- Evidence-gated termination: a phase ends when its exit criteria are met, never after a fixed number of rounds
- Minor decisions (naming, defaults, equivalent approaches): agents pick a reasonable option and note it — ask the user only for scope changes or destructive actions

# /great:deploy — Build and Deploy

$ARGUMENTS

Run sequential subagents:

1. **builder** — build the release artifact using the project's build system (detect from config files — never hardcode language-specific commands). Before deploying, define rollback criteria: abort triggers (build failure, test failure, size regression, missing artifacts), a verified rollback path, and post-deploy smoke tests. Never deploy without a verified rollback path.
2. **verifier** — smoke test the built artifact, check size against `.tasks/baselines/`, report status with cited output. If smoke tests fail, execute the rollback immediately.
