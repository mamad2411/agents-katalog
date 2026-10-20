# Copilot Instructions — Rotaris

Canonical agent instructions live in [AGENTS.md](../AGENTS.md) — read that first
(architecture, naming, rules, workflow, commands, and the ReqToCode summary).
Scoped files:
[apps/rotaris/AGENTS.md](../apps/rotaris/AGENTS.md).
This file adds nothing of its own except the one rule that is non-negotiable in
every task.

## ReqToCode — MANDATORY

ALL production code and ALL tests trace to a requirement in `docs/requirements/`,
bidirectionally: `@traces(SWR.SWR_<n>)` on the implementation, `@verifies(SWR.SWR_<n>)`
on the covering test. Code with no requirement *is* spec drift — when no product
requirement covers the code, author a **technical requirement** rather than skipping
traceability. A broken trace is a broken build (verifier,
`.github/workflows/reqtocode.yml`).

Full rules: [AGENTS.md §Critical rules](../AGENTS.md#critical-rules--reqtocode-enforced-build-breaking).
Store format: [docs/requirements/README.md](../docs/requirements/README.md).
On **any** ReqToCode signal, or before **any** edit under `docs/requirements/`:
load the `reqtocode` skill and follow
[docs/reference/reqtocode-playbook.md](../docs/reference/reqtocode-playbook.md)
before doing anything else. Authoring a new requirement: `requirement-capture` skill.
