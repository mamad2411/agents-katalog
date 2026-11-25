---
name: constitutional-reasoning
description: >
  Self-critique and Constitutional AI reasoning skill. Makes Claude evaluate its
  own outputs against a set of user-defined or auto-generated principles, then
  revise until the output satisfies all of them. Reduces hallucination, over-confidence,
  and sycophancy by forcing Claude to argue against its own answer before finalising.
  Generates a principle set from the user's domain, runs critique passes, surfaces
  violations, revises, and repeats until no principles are violated or the user
  accepts the output.
  Use when user says: critique your own answer, check yourself, apply your principles,
  constitutional AI, self-review, fact-check this, argue against your own output,
  steelman the opposite, what are you getting wrong, is this actually correct,
  audit your answer, find your own mistakes, what assumptions are you making, reduce
  hallucination, double-check yourself, run a critique pass, apply a rubric.
  Do NOT activate for: creative work where principles would suppress quality,
  requests that explicitly want a single confident answer without review.
  First response: "Constitutional Reasoning active. Paste your question or the
  output you want critiqued. I'll define the principle set, then run critique passes
  until violations are resolved."
license: Apache 2.0
---

# Constitutional Reasoning

Claude gives confident answers that are wrong. Not because it's lying — because it's
predicting what a correct answer looks like. It pattern-matches to plausible outputs.
The first draft is optimized for coherence, not accuracy.

Constitutional AI solves this by making the model evaluate its output against explicit
principles before finalizing. This skill operationalises that loop: define principles,
run critique, surface violations, revise, repeat.

---

## SLASH COMMANDS

| Command | Action |
| --- | --- |
| `/constitution <domain>` | Auto-generate a principle set for a specific domain |
| `/add-principle <principle>` | Add a custom principle to the active constitution |
| `/critique <output>` | Run one critique pass on an output and list violations |
| `/revise` | Revise the output to fix all listed violations |
| `/loop <n>` | Run n critique-revise cycles automatically |
| `/show-constitution` | Display the active principle set |
| `/violations` | List all unresolved violations from the last critique pass |
| `/diff` | Show exactly what changed between original and revised output |
| `/certify` | Declare the output clean — list any principles still soft-violated |
| `/trust-score` | Score the output's reliability 0–10 with a calibration justification |
| `/reset` | Clear the constitution and start fresh |

---

## HIGH-LEVEL WORKFLOW

```text
User provides output or question to evaluate
    │
    ├─ Phase 1: Constitution Generation
    │     Define principles relevant to the domain and task
    │
    ├─ Phase 2: Initial Output
    │     Generate or receive the answer to be evaluated
    │
    ├─ Phase 3: Critique Pass
    │     Test the output against every principle; list violations
    │
    ├─ Phase 4: Revision
    │     Rewrite to fix violations without introducing new ones
    │
    ├─ Phase 5: Re-critique
    │     Re-run the critique pass on the revised output
    │
    └─ Phase 6: Certification
          Declare the output clean or flag residual soft violations
```

---

## PHASE 1 — CONSTITUTION GENERATION

A constitution is a list of principles the output must satisfy. Principles are
falsifiable — each one can be checked against the output with a PASS or FAIL.

### Domain-specific principle templates

**Factual / research output:**
```text
P1: Every specific claim is either (a) sourced from the provided context,
    or (b) explicitly flagged as inference with a confidence qualifier.
P2: No number, date, name, or statistic is stated with more certainty than
    the evidence supports.
P3: Uncertainty is expressed in calibrated terms ("likely", "unclear",
    "insufficient data") — not suppressed.
P4: The output does not contradict any claim made in the source material.
P5: Alternative interpretations of ambiguous evidence are surfaced.
```

**Code output:**
```text
P1: Every function does what its name and docstring claim.
P2: No assumption about input type, range, or availability is unstated.
P3: Error paths are handled or explicitly noted as out of scope.
P4: No variable is used before it is assigned.
P5: No library or API is called with parameters that contradict its specification.
```

**Strategic / recommendation output:**
```text
P1: Every recommendation is tied to a stated constraint or goal.
P2: Tradeoffs of the recommended approach are explicitly listed.
P3: The output does not recommend an action whose prerequisites are unverified.
P4: No single point of failure is introduced without being named.
P5: The confidence level of the recommendation matches the evidence quality.
```

**Summary / synthesis output:**
```text
P1: No information present in the source is misrepresented in the summary.
P2: No information absent from the source is added to the summary.
P3: Proportionality is preserved — major points are not buried; minor points
    are not elevated.
P4: Conflicting information in the source is reflected as conflict, not resolved.
P5: The summary does not add causal claims the source does not make.
```

### Custom principle rules
- Must be falsifiable: "This is good" is not a principle. "No claim is unsupported" is.
- Must be checkable against the output alone (not against external knowledge)
- Phrase as constraints, not goals: "No X" or "Every Y" not "Be accurate"
- Maximum 8 principles per constitution — more dilutes attention

---

## PHASE 2 — CRITIQUE PASS

Run every principle against the output. For each principle, verdict: PASS or FAIL.
For every FAIL, provide:
1. The violated principle
2. The exact sentence or section that violates it
3. Why it violates the principle
4. What would make it pass

### Critique pass format

```text
CRITIQUE PASS [N]

P1: [principle text]
  Verdict: PASS

P2: [principle text]
  Verdict: FAIL
  Violating text: "[exact quote from output]"
  Violation: [one sentence: why this fails the principle]
  Fix: [one sentence: what the output should say instead]

P3: [principle text]
  Verdict: PASS

SUMMARY
  Violations: [N]
  Critical (blocks certification): [list]
  Soft (note but can certify): [list]
```

### Critique rules

- **Quote the exact violating text.** Do not paraphrase.
- **Do not soften violations.** "This could be interpreted as..." = FAIL, not soft-PASS.
- **A claim that cannot be verified from provided context = FAIL for factual principles,** unless flagged as inference.
- **Sycophantic language triggers P-confidence violation** ("clearly", "obviously", "undoubtedly" without evidence).
- **If the output omits a required element, that is a violation** even if nothing explicitly wrong is stated.

---

## PHASE 3 — REVISION

Rewrite the output to fix all FAIL verdicts. Rules:

1. Fix in order of severity (critical violations first)
2. Do not introduce new violations while fixing old ones
3. Do not remove accurate content to avoid failing a principle — rewrite it instead
4. Where a claim cannot be verified, add a calibration qualifier, do not delete the claim
5. After revision, explicitly re-check each previously-failed principle

### Calibration qualifier vocabulary

| Confidence level | Qualifier to use |
| --- | --- |
| Very high (near-certain) | "Evidence strongly indicates..." |
| High | "This is likely because..." |
| Medium | "This suggests, though isn't confirmed..." |
| Low | "One interpretation is..., though this is uncertain" |
| Very low | "Insufficient data to determine — this is speculative" |

---

## PHASE 4 — CERTIFICATION

After all critique-revise cycles, certify the output.

```text
CERTIFICATION

Constitution applied: [N principles]
Critique cycles run: [N]
Violations resolved: [N]

Status: CERTIFIED CLEAN
  — All [N] principles satisfied in final revision.

OR

Status: CERTIFIED WITH NOTES
  — [N] soft violations remain:
    · [principle]: [note — why it's soft, not critical]

Trust score: [X]/10
  [2 sentences: what drives the score up, what limits it]
```

### Trust score rubric

| Score | Meaning |
| --- | --- |
| 9–10 | Every claim sourced or qualified; no unchecked assumptions; all tradeoffs surfaced |
| 7–8 | Minor unqualified claims; tradeoffs mostly surfaced; no critical violations |
| 5–6 | Some claims lack support; some tradeoffs missing; 1–2 soft violations |
| 3–4 | Significant unsupported claims; important tradeoffs absent; overconfident language |
| 1–2 | Multiple critical violations; claims contradict source; hallucination likely |
