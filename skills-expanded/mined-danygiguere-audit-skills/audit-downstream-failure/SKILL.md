---
name: audit-downstream-failure
description: Downstream failure and resilience checklist. Use when code calls a remote dependency (HTTP API, RPC, database, cache) or adds timeouts, retries, fallbacks, or health probes — missing or over-budget timeouts, retries on non-idempotent calls or non-retryable errors, retry storms, security checks that fail open, optional dependencies failing critical flows, errors treated as empty results, liveness probes that ping dependencies.
---

Read `../audit/references/operability/downstream-failure.md` and apply its
checklist to the code the user specified (or the current diff if none was
given). If the target is larger than a diff — a module, service, or whole repo —
follow `../audit/references/methodology/scope.md` first. Verify each candidate
with `../audit/references/methodology/verify.md` before reporting. Report
surviving findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
