---
name: run-gates
description: "Run the gates before review, ship, release or hotfix; report complete gate evidence."
---

# run-gates

1. Run `node scripts/gates.mjs` from the repository root (it needs no git flow). Follow [Gates](../../../docs/maintaining.md#gates); never skip or weaken a gate. `--quick` is diagnostic only and does not satisfy full verification.
2. For a PR, also run `node scripts/ci-local.mjs --pr <N>`; inspect its per-job logs, including NOT RUN jobs. Do not post status unless requested.
3. Report every gate as PASS / FAIL / NOT RUN with log paths and HEAD; disclose uncommitted changes, failures and missing environments. Evidence must be re-earned after changes. Stop release progression on failed or unrun required gates.

Tagging, pushing `main`/tags, creating a release and publishing the `gemini` branch need the owner's explicit go-ahead in that session. Stop before each unless that session's explicit go-ahead covers it.
