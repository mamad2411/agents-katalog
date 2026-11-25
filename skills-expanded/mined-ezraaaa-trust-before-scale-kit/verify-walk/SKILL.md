---
name: verify-walk
description: "Walk changed journeys in a browser or simulator and report observable results on the exact head."
---

# Verify Walk

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Read `routine.coreFlows`, `routine.personas`, `routine.designSystem` and any walk requirements
in the extension. Use a browser or simulator appropriate to the configured surface; host setup is
in `docs/harnesses.md`. Walk changed journeys, role variants, empty/error states and recovery.
Check what is on screen and what actions actually do, not just internal state or test output.
For shared code, walk one consumer per application. Record device/browser, appearance, role,
steps, expected versus observed result and full head SHA. Use free ports where needed.
Mark each journey WALKED or INFERRED. INFERRED requires why it cannot be reached locally and a
walk-owed issue describing how to reproduce it. “No time” and “tests passed” are missing walks,
not exceptions. Do not claim an unavailable browser or simulator was used. A later edit invalidates
affected walk evidence; rerun before readiness. Never edit during gates or contend with another walk.
