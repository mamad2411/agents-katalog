---
name: audit-schema-design
description: Database schema design checklist (indexes, foreign keys, constraints). Use when reviewing migrations, new tables or columns, slow queries, missing indexes, foreign-key and ON DELETE behavior, or integrity rules enforced only in app code.
---

Read `../audit/references/operability/schema-design.md` and apply its checklist
to the code the user specified (or the current diff if none was given). If the
target is larger than a diff — a module, service, or whole repo — follow
`../audit/references/methodology/scope.md` first. Verify each candidate with
`../audit/references/methodology/verify.md` before reporting. Report surviving
findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
