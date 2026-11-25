---
name: audit-statelessness
description: Statelessness checklist for horizontally scaled apps. Use when reviewing services meant to run as multiple replicas — in-memory sessions or counters, module/static mutable state, local-disk uploads, process-local locks or schedulers, sticky-session assumptions, state lost on deploy.
---

Read `../audit/references/operability/statelessness.md` and apply its checklist
to the code the user specified (or the current diff if none was given). If the
target is larger than a diff — a module, service, or whole repo — follow
`../audit/references/methodology/scope.md` first. Verify each candidate with
`../audit/references/methodology/verify.md` before reporting. Report surviving
findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
