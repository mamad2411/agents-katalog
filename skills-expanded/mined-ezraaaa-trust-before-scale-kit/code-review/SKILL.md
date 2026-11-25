---
name: code-review
description: "Review correctness on the settled change and identify concrete regressions with evidence."
---

# Code Review

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Read the settled diff and the surrounding callers, tests and contracts. Check intended behaviour,
authorization boundaries, errors, data migration, compatibility and test assertions that actually
prove outcomes. Trace reachability before alleging an unconditional effect. Name concrete input,
wrong outcome and file:line, rather than speculative style preferences.
Use the planned level: medium for tests/tooling, high for behaviour, xhigh for security. Never
request max or ultra unless the owner asks. If a different-model cross-review is the correctness
read, record the conditional deferral; if it produces no review, perform correctness one level
higher before merge (ceiling xhigh; at the ceiling use a fresh independent reviewer and name it).
