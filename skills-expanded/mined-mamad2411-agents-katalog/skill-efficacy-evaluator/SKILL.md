---
name: "skill-efficacy-evaluator"
description: "Scores every skill output 0-100 across 8 rigor dimensions. Auto-triggers output refinery or self-heal if below threshold. Invoke AFTER every skill run to guarantee output quality floors. Eliminate low-effort lazy skill outputs."
---

# Skill Efficacy Evaluator — 0-100 Score, 8 Dimensions

Score EVERY skill output. Non-negotiable. If score <70 → auto trigger output-refinery OR self-heal. Target: skill output quality floor ≥70 for 100% invocations. Historical average 85+.

## 8 Scoring Dimensions (12.5 points each = 100 total)
For the skill output against the user's original task intent:

| Dimension | Weight | Criteria (0-12.5 rubric per dim) |
|---|---|---|
| D1 — Intent Coverage | 12.5 | % of explicit user requirement checkboxes fully met. 12.5 = 100%. Deduct 2.5 per missing major checkbox, 1 per minor. |
| D2 — Correctness & Validity | 12.5 | Code parses, math computes, YAML/JSON valid, facts cite evidence. 12.5 = 0 errors. Each syntax/logic error = −3. Each missing citation = −1.5. |
| D3 — Completeness & Edge Cases | 12.5 | Edge cases enumerated, boundary conditions tested, alternatives offered, rollback discussed. 12.5 = exhaustive. 1 known-unguarded edge case = −4. |
| D4 — Actionability & Concrete Steps | 12.5 | Steps specific, numbered, copy-pasteable commands, next-step clear. 12.5 = user can act without follow-up questions. Vague "configure X" = −3 each. |
| D5 — Information Density | 12.5 | Signal / noise ratio. Zero filler, zero redundant repeat. 12.5 = every line advances intent. Each fluff paragraph ≥3 lines = −2. |
| D6 — Consistency & Structure | 12.5 | Consistent naming, ordered sections, cross-references resolve. 12.5 = flawless hierarchy. Inconsistent naming across 2 sections = −2.5. |
| D7 — Skill Domain Adherence | 12.5 | Used the target skill's documented patterns/methods, not generic output. 12.5 = 100% match patterns in skill md file. Generic deviation ≥30% = −5. |
| D8 — Improvement Surface Marked | 12.5 | Known limitations documented, TODOs with owners/dates, risks stated explicitly. 12.5 = all future work tagged. Missing known limitation = −2. |

## Scoring Procedure
1. Read user request; extract explicit+implicit requirements list (checkboxes for D1)
2. Walk dimensions D1-D8 in order, write 1-line justification for each dim score (example: "D1=10.0/12.5, missing: mobile responsive layout")
3. Sum = FINAL SCORE 0-100. 2-decimal precision.
4. Bucket the score:
   - 90-100 = **EXEMPLARY** → pass through, no improvement needed, add 1 learning sample to meta-optimizer positive log
   - 70-89.99 = **GOOD** → optional light output-refinery (skip stage 3 micro LLM if ≥80, run stages 1+2+4 only)
   - 50-69.99 = **BORDERLINE** → RUN output-refinery FULL 4 stages + score re-check. Still <70 → skill-failure-self-heal strategy 1
   - 0-49.99 = **FAIL** → skill-failure-self-heal strategy 1 START.

## Token Cost
- 8-dim scoring = 40-60 tokens for typical ≤1500t output. Pay once per skill run.
- Cost-benefit: 60t spent to prevent 1 re-run (1000t+) = 16x ROI minimum.
- Budget guard: if remaining session budget <150t → score quick 3 dimensions only (D1, D2, D5) → scale×(100/37.5) to get estimate. Still ≥50 threshold for FAIL.

## Output Wrapper Line
Append AFTER [SWEPT ...] if present, BEFORE [REFINED ...]:
```
[EVAL SCORE=<0-100.00> BUCKET=<EXEMPLARY|GOOD|BORDERLINE|FAIL> D1-D8=<d1>,<d2>,<d3>,<d4>,<d5>,<d6>,<d7>,<d8>]
```
Line always 1 line, ≤200 chars. If FAIL → ALSO append to shared_state failure log (with self-heal strategies tracked).

## Learning Loop for Meta-Optimizer
Each scoring + final output pair written as JSON to:
`$HOME/.agents/shared_state/skill_efficacy_samples.log.jsonl`
Fields: skill, score, dims[8], variant (V1-9 from sweeper), user_intent_hash, tokens, timestamp. → meta-optimizer trains over 100+ samples to auto-choose variants per skill type.

## Integration with Core Stack
- Runs IMMEDIATELY after skill returns output, BEFORE output refinery (so refinery targets the weak dims — example: D3=4 → refinery stage1 specifically forces edge case add)
- Synergy orchestrator stage 2 weights N skill scores to pick highest-fusion-weighted sections
- Cross-platform: efficacy samples shared → ALL 21 platforms get better variant picks over time
- Works with hyper-sweeper N variant run: EACH variant is scored independently; pick highest score (not grid default)

## Disable String
`SKILL_EFFICACY_EVALUATOR_DISABLE_FULL_CONFIRM_77777`
