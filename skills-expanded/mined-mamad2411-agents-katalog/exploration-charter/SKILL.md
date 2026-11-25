---
name: exploration-charter
version: 1.0.0
description: Format and conventions for exploratory test charters and session reports — writing or reviewing a persona exploration session, generating charters from persona jobs, and triaging session findings into work items. Also holds the persona spec schema. Used by persona-runner, boundary-prober, and journey-orchestrator. Do NOT use for test-case design technique (that is qa-techniques) or for deciding whether a failure is a bug vs. a flake (that is qa-triage).
---

# Exploration Charter

Reference material for this skill:
- `personas-schema-template.yaml` — the persona spec schema, emitted by `persona-discovery` and consumed by the three exploration agents.

## Charter

One line:

```
Explore <target> as <persona> with <resources> to discover <information>
```

Plus: step budget, preconditions, and out-of-scope list. **A charter that does not name what information it seeks is not a charter — reject it.**

## Session report

- **Header** — persona, charter, environment, build/commit, timebox, actual steps used
- **Coverage log** — what was touched; explicitly list what was in scope but skipped
- **Findings** — id, severity, repro steps, expected, actual, evidence, persona impact
- **Questions** — anything undeterminable, each with what would resolve it
- **Session debrief** — three numbers: % effort on the charter, % on investigating findings, % on setup and friction. **High setup % is itself a reportable problem.**

## Severity

Rate by **persona impact**, not by technical interest: does it block a ranked job, degrade it, or merely annoy. A cosmetic defect blocking a rank-1 job outranks a sophisticated defect on a rank-5 job.

Where a finding is a security or authorization issue, use `security-engineer`'s severity scale (Critical / High / Medium / Low / Informational) instead, so it composes directly with that agent's own findings. Never mix the two scales in one list without labeling which is in use.

## Triage

Deduplicate against prior sessions before filing, **within this project only** — follow the `project-memory` skill's isolation principle; a finding pattern from a different project is not a duplicate here.

A finding becomes a regression test **only once it is reproducible from a clean state**; otherwise it stays a finding with the non-determinism documented. For the bug-vs-bad-test-vs-flake decision itself, load `qa-triage` — that judgment belongs to `qa-engineer`, not to the session report.
