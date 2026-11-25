---
name: appsec-triage-report
description: >-
  Calibrate severity and write the security report a team will actually act on.
  Use when asked to write up findings, assign or justify severity, produce a
  pentest or code-review report, summarise a scan for engineers or leadership,
  or decide what to escalate.
allowed-tools: Read, Write
---

# AppSec pipeline · Phase 5 — Reporting

Covers **stage 15**. Every earlier stage is measured here: a defect that was
found, deduplicated, verified and reproduced still counts for nothing if the
report gets it fixed slowly or not at all.

## When to use this

At the end of a review, or whenever findings must be handed to someone who did
not do the analysis.

## Inputs

`findings` (Phase 3), `validations` (Phase 4), and `plan.deferred` (Phase 2).
The last one is not optional — it is the scope statement.

## Procedure

**Calibrate severity, and show the calibration.** Severity is a function of
impact and reachability, and both are already computed upstream. State them:

| Severity | Requires |
|---|---|
| Critical | reproduced, unauthenticated path, sink is subprocess/deserialisation/credential |
| High | reproduced, or confirmed with an authenticated path to a dangerous sink |
| Medium | confirmed, feasible, but mitigated in depth or requires elevated access |
| Low | confirmed, not feasible in this deployment |
| Informational | needs_human, or hardening with no demonstrated path |

**A finding that did not reproduce may not be Critical.** If Phase 4 set
`reproduced: false`, cap it at Medium and say why in the same sentence — the
reader must not have to cross-reference an appendix to learn that the headline
finding is theoretical.

**Separate demonstrated from asserted.** Two sections, always. The credibility
of the whole report comes from the reader being able to tell them apart without
effort, and one overclaimed Critical costs more trust than ten honest Lows.

**Write for the person who will fix it.** Each finding needs: where it is, what
an attacker does with it, the observable that proves it, the fix, and what the
fix costs. Lead with the fix — the reader is deciding what to do, not learning
the CWE taxonomy.

**State the scope honestly.** What was analysed, what was deferred and why,
what the tooling cannot see. A report that hides its gaps invites the reader to
treat silence as coverage.

**Report accuracy, never conformance.** "100% schema-valid" is a statement
about the serialiser and is true of an empty result. If a false-positive rate
is known — Phase 4 measures one every run — report that instead.

## Example

**Input** — the fixture committed at the top of [`scripts/appsec_triage_report.py`](scripts/appsec_triage_report.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
id     rule sev  calibrated   score
----------------------------------------
F-01   high      critical         7   ← moved
F-02   high      low              0   ← moved
F-03   medium    critical         6   ← moved
F-04   high      medium           2   ← moved
F-05   medium    critical         6   ← moved
F-06   high      medium           2   ← moved
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
  "report": {
    "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0, "informational": 0},
    "demonstrated": [
      {"finding_id": "str", "severity": "critical|high|medium|low|informational",
       "severity_inputs": {"reproduced": true, "auth": "none|user|admin", "sink": "str"},
       "title": "str", "impact": "str", "observable": "str",
       "fix": "str", "fix_cost": "low|medium|high"}
    ],
    "asserted": [{"finding_id": "str", "severity": "str", "why_not_demonstrated": "str"}],
    "scope": {"analysed": ["str"], "deferred": ["str"], "blind_spots": ["str"]},
    "quality": {"validated": 0, "failed_to_reproduce": 0, "false_positive_rate": 0.0}
  }
}
```

## Failure modes

- **Severity without `severity_inputs`.** Unarguable, therefore unactionable.
- **Burying non-reproduction.** It belongs in the finding, not the appendix.
- **Sorting by severity alone.** Ties must break deterministically
  (`-severity_rank, cwe, file, line`) or two runs disagree and the diff between
  reports becomes unreadable.
- **Counting conformance as quality.** See above; it is the most common way an
  automated pipeline flatters itself.

## Handoff

This is the end of the pipeline. Feed `quality.false_positive_rate` back into
the next run's Phase 2 scoring — a pipeline that never learns from its own
misses repeats them at machine speed.
