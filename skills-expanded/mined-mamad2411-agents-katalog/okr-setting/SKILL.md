---
name: okr-setting
description: Set OKRs — one ambitious Objective, 3–5 measurable Key Results with baselines + targets + confidence, named Anti-OKRs, weekly confidence cadence.
---

# okr-setting

> Andy Grove's OKR. **O** is qualitative + ambitious. **KRs** are measurable + time-boxed. Confidence at 0.5–0.7 average — anything higher is sandbagging.

## When to use

- A team or org is setting OKRs for the next cycle.
- Existing OKRs read as task lists, not outcomes; reset.

## Inputs

- The cycle (Q3 2026, H1, etc.).
- The team or organization scope.
- Last cycle's results (if any) for calibration.

## Procedure

1. Read [`OKR.md`](../../templates/OKR.md).
2. Write `docs/okrs/<scope>-<cycle>.md`:
   - **Objective**: one qualitative sentence. If it contains a metric, it's probably a KR misclassified.
   - **Key Results**: 3–5. Each is verb + metric + target + deadline. Day-0 baseline named so end-of-cycle grading is unambiguous.
   - **Confidence**: 0.0–1.0 per KR at start. Average aims for 0.5–0.7. Updated weekly through the cycle.
   - **Anti-OKRs**: 2–4 things this cycle is explicitly NOT trying to do. Cuts later debates.
   - **Initiatives**: the work that moves KRs, mapped 1:1 from initiative → KR. Initiatives are *output*; KRs are *outcome*. Don't confuse.
3. Sandbagging guard: re-score confidence. If every KR is 0.9, the OKRs are too easy; pick one to make harder.

## Quality bar

- Objective is one sentence, qualitative, no metric.
- 3–5 KRs. More than 5 = O is fuzzy; cut.
- Each KR has baseline + target + deadline.
- At least one KR is a "bet" (confidence ≤ 0.5).
- Anti-OKRs are present.
- Initiative → KR mapping is explicit.

## Output

- File: `docs/okrs/<scope>-<cycle>.md`.
- Summary listing the Objective + KR count + average confidence.

## Anti-patterns to avoid

- Objective is a task ("Ship the new admin panel"). That's a project, not an O.
- KR without a baseline. End-of-cycle grading becomes a debate, not a measurement.
- All KRs at 0.9 (sandbagging) or all at 0.1 (theatrics).
- No Anti-OKRs. Scope creeps.
- Cargo-cult cascade ("VP's KRs become my Os become my reports' KRs"). Each level should set its own.
