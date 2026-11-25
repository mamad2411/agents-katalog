---
name: deep-review
description: "Review a change against configured project rules, enforcers and recorded decisions."
---

# Deep Review

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Read every `routine.ruleSources` entry: instruction files, ADRs, enforcer tables and recorded
“do not change back” decisions. Inspect changed code and its callers against each applicable rule.
Catch a cleanup that silently undoes a recorded decision. Quote the rule and cite its source and
the changed line. Check whether an existing decision already settles a reported defect; do not
re-raise settled policy as a new defect. A misimplemented decision still counts. With no sources,
report a coverage gap and request the project's rules, rather than inventing them.
