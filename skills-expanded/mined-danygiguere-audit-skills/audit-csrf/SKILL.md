---
name: audit-csrf
description: Cross-site request forgery checklist. Use when reviewing state-changing endpoints in apps with cookie or session-based authentication — CSRF tokens, SameSite, origin checks. Does not apply to pure token-based APIs.
---

Read `../audit/references/access-data-security/csrf.md` and apply its checklist
to the code the user specified (or the current diff if none was given). If the
target is larger than a diff — a module, service, or whole repo — follow
`../audit/references/methodology/scope.md` first. Verify each candidate with
`../audit/references/methodology/verify.md` before reporting. Report surviving
findings with `file:line` references and a severity assigned per
`../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
