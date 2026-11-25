---
name: incident-rca
description: Root-cause analysis for bugs, incidents, and regressions — timeline, hypothesis testing with evidence, 5-whys, prevention rules feeding the memory loop. Use when investigating a production bug, an error log the user dropped in, or a recurring defect.
category: meta-process
---

# Incident / Bug Root-Cause Analysis

Turn "it broke" into an evidence-backed cause and a prevention rule. Pairs with bug-router (R-009)
and the feedback loop (R-010-09).

## Method

```text
1. REPRODUCE or capture: exact error, inputs, environment, frequency. No repro -> say so explicitly
   and work from logs/timeline with lower confidence (state it).
2. TIMELINE: what changed before it broke? (git log on the touching area, deploys, config, data,
   dependency bumps). Correlation candidates, not conclusions.
3. HYPOTHESES: list 2-4, each with a CHEAP TEST that would confirm/kill it. Test in cheapest-first
   order; record each result (journal, R-024-03).
4. ROOT CAUSE: apply 5-whys until you reach a process/design cause, not just the faulty line.
   "Null pointer" is a symptom; "contract change unannounced + no contract test" is a cause.
5. FIX + REGRESSION TEST: the fix ships WITH a test that fails before / passes after (evidence).
6. PREVENTION: write root_cause, prevention_rule, regression_check, recurrence_key into
   coding_error_feedback / feedback memory (R-006-17, R-010). Recurring pattern (>=3) -> draft a
   proposed rule (R-010-09).
```

## Classification discipline

```text
Blocker vs non-blocker per R-009 — never downgrade to pass QC (R-019-QC4).
Distinguish: defect (code wrong) / regression (was right, broke) / config / data / external.
The category changes who fixes it and where the prevention lands.
```

## Honesty bars

```text
No "probably fixed": done requires the regression test passing (R-023-03 evidence).
If two causes remain plausible, say which one you fixed and why the other is ruled out (or not).
```
