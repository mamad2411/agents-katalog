---
name: appsec-vuln-audit
description: >-
  Audit code for vulnerabilities against a threat model, then deduplicate,
  verify in context, and filter to what is actually reachable. Use when asked
  to review code for security bugs, run or interpret SAST, check whether a
  finding is a false positive, or reduce a noisy findings list to the ones
  worth a human's time.
allowed-tools: Read, Grep, Glob, Bash
---

# AppSec pipeline · Phase 3 — Analysis and filtering

Covers **stages 7–10**. This is where findings are produced — and, more
importantly, where most of them are thrown away.

The hard problem in application security is not finding candidate defects. It
is that a scanner emits hundreds and a human can act on ten. Every stage after
7 exists to shrink the list without losing the true positives.

## When to use this

When you have a threat model and a budget, or when handed a raw findings file
that nobody trusts. Stages 8–10 work on any findings list, including one from a
third-party scanner.

## Inputs

| Input | Required | Notes |
|---|---|---|
| `threat_model` + `plan.selected` | preferred | from appsec-threat-model |
| Source worktree | yes | verification needs the code, not just the finding |
| Existing findings | optional | run stages 8–10 alone to clean a noisy list |

## Procedure

**Stage 7 — Vulnerability auditing.** For each selected threat, examine the
path from entry to sink and decide whether the weakness is actually present.
Record for each finding: `cwe`, `file`, `line`, `unit`, the **evidence** (the
specific expression that is unsafe), and the **sanitiser** you looked for and
did not find. A finding that cannot name what was missing is a guess.

Three generations of analysis, and they are complementary, not competing:
grep-class pattern matching (fast, no dataflow), taint analysis (dataflow, no
semantics), and model-assisted review (semantics, no guarantees). Use the
cheapest one that can answer the question, and never let the third overrule the
second on a question of reachability — the model does not execute the program.

**Stage 8 — Deduplication.** The same defect appears many times: once per
scanner, once per path, once per call site. Collapse on the **defect identity**
— `(cwe, file, unit, sink_expression)` — not on the message text. Keep the
count: `occurrences` is signal about how exposed the defect is.

Match paths by parent directory plus filename tail. Deduplicating on a bare
basename silently merges two different files and loses a real finding.

**Stage 9 — Contextual verification.** For each surviving finding, look at the
surrounding code for the thing that makes it not-a-bug: a validator upstream, a
framework escaping the parameter, a type that cannot hold the payload, a caller
that only ever passes a constant. Record the verdict and the reason:
`confirmed`, `mitigated_by <what>`, or `needs_human`.

`needs_human` is a legitimate verdict and must stay available. A pipeline that
must decide will decide wrongly under uncertainty.

**Stage 10 — Feasibility filtering.** Drop what an attacker cannot actually
reach: code behind a feature flag that is off, an admin-only path in a service
with no admin, a sink whose input is fully constant. Record *why* each drop was
made, because the next scan will rediscover it and the reason is what stops
that work being repeated.

## Example

**Input** — the fixture committed at the top of [`scripts/appsec_vuln_audit.py`](scripts/appsec_vuln_audit.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
call graph:
   http_get_report   → ['load_report']
   http_health       → —
   load_report       → —
   legacy_export     → —
   debug_dump        → —
   dispatch          → —
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "findings": [
    {"id": "str", "cwe": "CWE-89", "file": "str", "line": 0, "unit": "str",
     "evidence": "str", "missing_control": "str",
     "occurrences": 1, "verdict": "confirmed|mitigated|needs_human",
     "verdict_reason": "str", "feasible": true, "confidence": 0.0}
  ],
  "dropped": [{"id": "str", "stage": 8, "why": "str"}],
  "counts": {"raw": 0, "deduped": 0, "verified": 0, "feasible": 0}
}
```

`counts` must be monotonically non-increasing across the four stages. If it is
not, the pipeline invented findings after the audit stage — stop and report.

## Failure modes

- **Confusing conformance with accuracy.** Output that matches this schema
  perfectly can still be entirely wrong. Schema validity is close to free;
  correctness is the expensive part. Never report conformance as a quality
  metric.
- **Dropping silently.** Every drop needs a stage and a reason.
- **Letting a model overrule dataflow on reachability.** It may propose a path;
  it may not confirm one.
- **Suppressing `needs_human` to look decisive.** Uncertainty that is hidden
  becomes someone's incident.

## Handoff

Feasible, confirmed findings go to **appsec-exploit-validate** for proof.
Everything else goes to **appsec-triage-report** with its verdict intact.
