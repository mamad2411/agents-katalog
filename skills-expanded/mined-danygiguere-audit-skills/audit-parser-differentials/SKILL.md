---
name: audit-parser-differentials
description: Parser/validator differential checklist. Use when reviewing validators, regexes, allowlists, URL or path parsing, content-type checks, or normalization — inputs a gate accepts but the downstream consumer interprets differently (unanchored regexes, startswith allowlists, two URL parsers, validate-then-reparse).
---

Read `../audit/references/input-api-dependency/parser-differentials.md` and
apply its checklist to the code the user specified (or the current diff if none
was given). If the target is larger than a diff — a module, service, or whole
repo — follow `../audit/references/methodology/scope.md` first. Verify each
candidate with `../audit/references/methodology/verify.md` before reporting.
Report surviving findings with `file:line` references and a severity assigned
per `../audit/references/methodology/severity.md`; if nothing survives, say the
checklist came back clean. Report only — do not change code unless the user asks
for a fix.
