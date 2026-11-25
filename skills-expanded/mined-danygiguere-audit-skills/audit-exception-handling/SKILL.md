---
name: audit-exception-handling
description: Exception and error-handling audit checklist. Use when reviewing try/catch blocks, error propagation, empty or overly broad catches, rethrowing, cleanup/finally paths, async error handling, or whether errors map to the right HTTP status (404 vs 403, 401, 422, 409).
---

Read `../audit/references/correctness/exception-handling.md` and apply its
checklist to the code the user specified (or the current diff if none was
given). If the target is larger than a diff — a module, service, or whole repo —
follow `../audit/references/methodology/scope.md` first. Verify each candidate
with `../audit/references/methodology/verify.md` before reporting. Report
surviving findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
