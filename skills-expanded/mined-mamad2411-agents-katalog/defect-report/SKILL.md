---
name: defect-report
description: >-
  Write a clear, reproducible defect (bug) report per ISTQB CTFL v4.0 §5.5 — the most
  frequent QA deliverable. Use when: "bug report," "defect report," "バグ報告,"
  "欠陥レポート," "file a bug," "write up this bug," "repro steps," "severity vs
  priority," or documenting something that's broken. Produces a structured report with
  the CTFL field set and an organization-specific injection section (tracker fields,
  severity/priority scales, triage routing). Output is a report document (design mode).
  Not for: prioritizing a whole test effort — use risk-based-testing; or finding the
  defects in the first place — use exploratory-testing. Related: exploratory-testing,
  risk-based-testing.
license: MIT
metadata:
  version: "1.0"
  istqb: "CTFL v4.0 §5.5 (Defect Management)"
  iso25010: [functional-suitability, performance-efficiency, compatibility, interaction-capability, reliability, security, maintainability, flexibility, safety]
  mode: [design]
---

# Defect Report

Turn an observed failure into a report the fixer can act on without coming back to
ask — reproducible, with expected vs actual stated, severity and priority separated.

## Objective

A defect report meeting the three CTFL v4.0 §5.5 objectives: (1) give those resolving
it enough information to fix it, (2) provide a means of tracking product quality, (3)
surface development/test process-improvement ideas. The failure mode this prevents:
"it's broken" tickets that bounce back for missing steps, missing expected result, or a
severity nobody can act on.

## Organization-specific inputs (fill these in)

The base model already knows how to write a bug. The value here is the org's specifics
— capture them once and this skill produces reports that fit your process:

- **Tracker + required fields**: Jira / Linear / GitHub Issues — which fields are
  mandatory, which labels/components are valid.
- **Severity scale**: define S1–S4 (or Blocker…Trivial) with concrete criteria (data
  loss? workaround exists? users affected?).
- **Priority scale** and the **severity-vs-priority policy** — they are independent
  (a typo in the logo = low severity, but high priority before a launch).
- **Triage routing / ownership**: which component routes to which team; the triage SLA.
- **Duplicate & linking policy**; the list of supported **environments**.
- **"Reproducible" bar**: how many attempts, what evidence is required to accept a repro.

## Context Discovery

- What was observed, and on what build/environment? (version, OS/browser, config, data)
- Which test or activity surfaced it (test case ID, exploratory charter, prod incident)?
- What evidence exists — logs, stack traces, screenshots, recordings, request IDs?
- Is it reproducible? How consistently, and from what starting state?

## Instructions

1. **Capture the CTFL §5.5 field set**: unique identifier; title (short summary); date
   observed, issuing org, author + role; test object + test environment; context (the
   test case / activity / SDLC phase / technique / data); description of the failure;
   expected vs actual results; severity; priority; status; references.

2. **Write a reproducible failure description**: numbered steps from a known starting
   state, minimal repro (strip irrelevant steps), and attach the evidence (logs,
   screenshots, recordings). If it is intermittent, say so and give the frequency.

3. **State expected AND actual explicitly**: "actual" alone is not a defect — the gap
   from expected behavior (cite the requirement/AC) is what makes it one.

4. **Separate severity from priority**: severity = impact on the product/stakeholders;
   priority = urgency to fix. Set both against the org scales; do not collapse them.

5. **One defect per report**; link duplicates and related reports rather than bundling.

6. **Stay factual and neutral**: describe behavior, not blame; do not speculate on root
   cause beyond what the evidence shows (root-causing is the fixer's job).

## Output Format

### design mode

```
# [ID] Title — short summary of the anomaly
- Status: open | Severity: S? | Priority: P? | Author (role): … | Date: …
- Test object / build: …    Environment: OS/browser/config/data
- Context: test case / activity / SDLC phase / technique / test data

## Steps to reproduce
1. … (from a known starting state)
2. …

## Expected result
…  (cite requirement / acceptance criterion)

## Actual result
…  (with evidence: logs / screenshots / recording / request-id)

## References
- Test case / requirement / related defects
```

## Anti-Patterns

- **"It doesn't work"** — no steps, no expected/actual. **Guard:** repro steps and
  expected-vs-actual are mandatory; a report without both is incomplete.
- **Severity = priority** — treating them as one field. **Guard:** define and set them
  independently against the org scales.
- **Not reproducible, no context** — a report nobody can act on. **Guard:** record the
  environment and steps from a known state; mark intermittent issues as such with a rate.
- **Blame or unsupported root-cause speculation** — "the backend dev broke X." **Guard:**
  factual behavior only; root cause belongs to the fixer unless evidence proves it.
- **Invented repro steps** — an agent writing steps it did not actually observe.
  **Guard:** report only observed behavior; label anything unconfirmed as unconfirmed.

## Related Skills

- `exploratory-testing` — surfaces the defects this skill documents (its session sheet
  feeds the report).
- `risk-based-testing` — defect severity/frequency feeds risk re-assessment.

## References

- ISTQB CTFL v4.0 Syllabus §5.5 (Defect Management): defect-report objectives, field
  set, and the defect workflow (log → analyze/classify → decide response → close)
- ISO/IEC/IEEE 29119-3 defines defect/incident report content (industry reference for
  the field set; CTFL v4.0 does not necessarily cite it explicitly)
