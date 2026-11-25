---
name: simplify
description: "Simplify a planned change without changing behaviour; run before correctness review."
---

# Simplify

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Settle the shape before anyone reviews correctness. Use the explicit planned range; never rely
on an upstream-derived default. Reuse existing helpers, reduce duplication and unnecessary work,
and preserve observable behaviour, error handling, authorization, ordering and public interfaces.
Keep one writer in the checkout and wait for it to finish. Read the resulting diff for behaviour
change only, reverting accidental semantic changes. A simplification is fresh unreviewed code:
run whichever correctness read is selected after it settles. Report what changed and why.
