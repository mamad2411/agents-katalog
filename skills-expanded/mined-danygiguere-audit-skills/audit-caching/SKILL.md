---
name: audit-caching
description: Caching correctness checklist. Use when reviewing caches — keys missing a user/tenant dimension, stale data after writes, cache stampede, cached errors, or per-user responses landing in a shared or CDN cache.
---

Read `../audit/references/operability/caching.md` and apply its checklist to the
code the user specified (or the current diff if none was given). If the target
is larger than a diff — a module, service, or whole repo — follow
`../audit/references/methodology/scope.md` first. Verify each candidate with
`../audit/references/methodology/verify.md` before reporting. Report surviving
findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
