---
name: audit-mass-assignment
description: Mass-assignment checklist. Use when request payloads are bound onto models or entities — create/update/fill from the request body, fillable/guarded lists, strong params, DTO binding, or fields like role, is_admin, or owner_id being writable.
---

Read `../audit/references/access-data-security/mass-assignment.md` and apply its
checklist to the code the user specified (or the current diff if none was
given). If the target is larger than a diff — a module, service, or whole repo —
follow `../audit/references/methodology/scope.md` first. Verify each candidate
with `../audit/references/methodology/verify.md` before reporting. Report
surviving findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
