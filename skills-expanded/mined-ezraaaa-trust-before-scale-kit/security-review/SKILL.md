---
name: security-review
description: "Review who can reach the changed surface and its data, including surrounding access paths."
---

# Security Review

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Scope to the surface, not only the changed lines: enumerate entry points, identities, tenants,
roles, collections, storage, queries, server handlers and visible clients that can reach the data.
Check authentication versus authorization, ownership, widened reads/writes, input validation,
secrets, logging, enumeration and revocation during a session. Follow indirect access paths and
negative cases. A client-side visibility check is not server authorization. Use role context from
`routine.personas` and policy in `routine.ruleSources`; missing policy is an owner question.
Introduced or widened unauthorized access blocks readiness until fixed or the slice is parked.
File pre-existing exposure before merge, with severity; never quote credentials in evidence.
