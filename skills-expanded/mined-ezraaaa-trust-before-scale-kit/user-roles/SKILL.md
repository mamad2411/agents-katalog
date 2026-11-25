---
name: user-roles
description: "Review what each configured role can see and do across a changed journey."
---

# User Roles

Config: `.agents/trust-before-scale.json` (else `.claude/trust-before-scale.json`), `routine.extension`,
the host instructions, and the planned base, range and changed surfaces. A missing configured input is a
gap, never a pass. Prefer the host capability in `routine.passes` (commands in `docs/harnesses.md`); this
skill is the fallback. Never invent project rules or roles. In a blind eval with config hidden, use the
routine inputs the prompt supplies and report missing source files.

Report: the command or brief, the reviewed full head SHA, scope, findings (checked file:line, severity, introduced,
worsened or pre-existing), a clean verdict or why no review happened, and limits. Route findings through
the routine. A report with no review is not clean. Never merge.

Use roles, pressures and real tasks in `routine.personas`; check applicable policy in
`routine.ruleSources`. Review each role independently, including restricted and revoked roles:
what they see, what they can invoke directly, whether the flow finishes, and whether messages and
sample data are truthful. Check role-specific actions, cross-role handoffs, navigation and denial
states. UI hiding does not prove authorization; coordinate with the security pass.
For a new surface do this before building and again after. If roles are absent, report the gap
and ask for them; do not assume a business hierarchy. Every finding names role, task, consequence
and fix. Missing capability goes to an issue, not an expansion of the current slice.
