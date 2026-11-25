---
name: reviewer-response-pack
description: Use when the user needs to answer reviewer comments, build a response matrix, classify revision requests, audit a response letter, verify a revised manuscript against review comments, or prepare a revise-and-resubmit package.
---

# Reviewer Response Pack

Use this skill after peer-review feedback arrives. It is not a generic paper review skill. Its job is to preserve each editor/reviewer concern, map it to real manuscript action or unresolved author input, and produce an auditable response package.

## Required Contract

Before drafting, read:

- `<VELA_RUNTIME_ROOT>/skills/catalog/peer_review_workflow.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/publication_style_rules.json`
- `<VELA_RUNTIME_ROOT>/skills/catalog/writing_quality_rules.json`

Use the `revision_response_review` mode in `peer_review_workflow.json`.

## Input Readiness

Accepted inputs:

- editor decision letter
- reviewer comments
- response draft
- revised manuscript
- tracked-change summary
- author notes
- figure/table/supplement change list
- target journal or submission system constraints

If reviewer boundaries, comment segmentation, or manuscript version is unclear, flag it. Do not invent reviewer structure.

## Workflow

1. Identify mode:
   - `triage-only`: classify comments and blockers
   - `draft`: build response letter from supplied facts
   - `audit`: check an existing response draft
   - `revise`: revise the response package
   - `verification-review`: verify whether claimed changes actually appear in the revised manuscript
2. Extract editor instructions first and assign IDs such as `E.1`; then split reviewer comments as `R1.1`, `R1.2`, `R2.1`.
3. Preserve each comment's meaning before responding.
4. Classify each item:
   - severity: `minor`, `major`, `blocking`, `unclear`
   - category: theory, literature, method, identification, measurement, evidence, statistics, citation, figure/table, reproducibility, ethics, writing, scope
   - risk: low, medium, high, blocking
5. Map each item to an action:
   - `ACCEPT_TEXT`
   - `ACCEPT_ANALYSIS`
   - `ACCEPT_FIGURE_TABLE`
   - `CLARIFY_EXISTING`
   - `ADD_CITATION_VERIFIED`
   - `SOFTEN_CLAIM`
   - `PARTIAL`
   - `DISAGREE_WITH_EVIDENCE`
   - `OUT_OF_SCOPE`
   - `AUTHOR_INPUT_NEEDED`
   - `BLOCKING`
6. Build the response strategy summary before drafting prose.
7. Draft point-by-point responses only for items with enough facts.
8. For every claimed change, include manuscript location, figure/table/supplement location, citation evidence, or an explicit placeholder.
9. For response prose and revised wording, run the local stop-slop surface scan through `writing_quality_rules.json`: remove throat-clearing, performative emphasis, vague importance claims, binary-reversal formulas, negative-listing setups, mechanical `rather than` / `since` / `however` / `therefore` / `not only but also` transitions, hidden-actor prose, uniform short paragraph blocks, and rhythmically over-polished paragraph endings. Keep reviewer respect, factual precision, legitimate hedging, contribution posture, and unchanged manuscript claims.
10. Run verification:
   - every comment answered or explicitly unresolved
   - every "we have..." statement tied to real evidence
   - no invented line numbers, analyses, citations, figures, data, or appendices
   - disagreement first acknowledges the concern
   - limitations are not hidden
   - the response does not over-concede, apologize for supported contributions, or rewrite a defensible claim as a limitation
   - Chinese terms in revised manuscript wording follow Chinese literature and established Chinese academic usage rather than ad hoc English-to-Chinese translation

## Re-Review Verification

When the user asks whether revisions addressed comments, produce a verification matrix:

| ID | Original comment | Author claim | Claimed location | Verified status | Residual issue | Required next action |
|---|---|---|---|---|---|---|

Use these statuses:

- `FULLY_ADDRESSED`
- `PARTIALLY_ADDRESSED`
- `NOT_ADDRESSED`
- `MADE_WORSE`
- `CANNOT_VERIFY`

If author notes say only "已修改" or "addressed as suggested", mark `CANNOT_VERIFY` until the real location and change are supplied.

## Output Contract

Default output:

```markdown
# Reviewer Response Pack

## Response Strategy Summary
- Decision type:
- Overall posture:
- Major risks:
- Suggested order:
- Readiness:

## Comment-Response Tracker
| ID | Reviewer concern | Category | Severity | Action | Missing author input | Readiness | Risk |
|---|---|---|---|---|---|---|---|

## Draft Point-By-Point Response

## Manuscript Change Checklist

## Revision Verification Matrix

## Missing Information And Blockers

## 中文核对
```

## Red Lines

- Do not ignore any reviewer comment.
- Do not change the meaning of a reviewer comment.
- Do not claim a revision was made unless the user supplied it or it is visible in the revised manuscript.
- Do not invent line numbers, page numbers, figure panels, citations, statistical results, sample sizes, data availability, or supplementary materials.
- Do not cite time, money, or convenience as the main reason for not doing requested work.
- Do not draft around missing ethics, compliance, or data-integrity requirements.
- Do not let response writing bypass `citation-verifier`, `writing-reference-capture`, or the peer-review protocol gate.
- Do not over-weaken supported claims just to sound polite. If a claim is evidence-backed, preserve it and clarify its boundary.
