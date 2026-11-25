---
name: audit-observability
description: Observability checklist. Use when checking whether errors, slow paths, or new endpoints would be visible in production — logging, metrics, tracing, alerts.
---

Read `../audit/references/operability/observability.md` and apply its checklist
to the code the user specified (or the current diff if none was given). If the
target is larger than a diff — a module, service, or whole repo — follow
`../audit/references/methodology/scope.md` first. Verify each candidate with
`../audit/references/methodology/verify.md` before reporting. Report surviving
findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
