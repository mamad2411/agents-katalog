---
name: audit-data-exposure
description: Data over-exposure checklist. Use when reviewing API responses, serializers, error messages, or logs for leaked fields, PII, or internal details.
---

Read `../audit/references/access-data-security/data-exposure.md` and apply its
checklist to the code the user specified (or the current diff if none was
given). If the target is larger than a diff — a module, service, or whole repo —
follow `../audit/references/methodology/scope.md` first. Verify each candidate
with `../audit/references/methodology/verify.md` before reporting. Report
surviving findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
