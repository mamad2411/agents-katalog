---
name: what-breaks
description: Pre-mortem — assume the plan already failed and hunt the reasons before you commit. Adversarial failure-mode analysis ranked by likelihood and impact, with concrete mitigations. For pressure-testing an idea, change, or plan.
argument-hint: <the plan/idea/change to stress-test> (or leave empty to use the current plan in context)
allowed-tools: Bash, Read, Glob, Grep
---

Stress-test a plan, idea, or change by assuming it has already failed and working backwards to why. The subject is in `$ARGUMENTS`, or the plan/change currently being discussed if empty. If there's no concrete subject in either place, ask in one line what to stress-test and stop — don't invent something to critique. Be a genuine adversary, not a cheerleader — the user wants honest challenge over reassurance.

## Step 1 — Ground yourself in reality
If the subject touches code or this project, look at the actual relevant files/config first — don't critique in the abstract. Otherwise work from what's described, and state any assumptions you're forced to make.

## Step 2 — Run the pre-mortem
It's months later and this failed. Enumerate the failure modes across these angles — only the ones that genuinely apply:
- **Technical** — what breaks, edge cases, scale, dependencies, data loss/corruption.
- **Assumptions** — what's being taken for granted that might be false.
- **Human / process** — misuse, the step someone forgets, handoff gaps.
- **External** — third-party/API/cost/policy/timing risks outside your control.
- **Second-order** — what this fixes but breaks elsewhere.

## Step 3 — Rank and report
For each real risk: `**[High / Med / Low]** — what fails, why, and the concrete mitigation or early-warning sign.`
Order by likelihood × impact. Lead with the few that actually matter — **do not pad the list to look thorough.**

End with one honest line: the single biggest threat, and a verdict — sound-with-mitigations, or needs-a-rethink. No false alarms, no false comfort.
