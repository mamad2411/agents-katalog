---
name: full-product-review
description: Perform repository-grounded full product reviews that assess what is working, what needs improvement, which structural issues should be revisited, and which underlying technical or delivery risks need action. Use when Codex is asked for a full product review, product audit, stabilization plan, architecture posture review, or an executive summary of product health with prioritized findings.
---

# Full Product Review

Run a broad but evidence-backed product review. Produce a standardized review pack and a concise findings summary that separates current strengths from near-term risks, structural issues, and gated major-work decisions.

## Quick Start

1. Confirm repo root, branch, dirty worktree, user-specified scope, and available evidence sources.
2. Scaffold the review pack:
   `python3 scripts/scaffold_review.py --repo-root . --product-name "<product-name>"`
3. Inspect code, docs, tests, backlog, prior audits, release surfaces, and any available incident or usage signals.
4. Score the product using `references/review-rubric.md`.
5. Record only evidence-backed findings in the review pack defined in `references/output-format.md`.
6. Finish with the exact final summary format from `references/output-format.md`.

## Review Priorities

- what is working and should be preserved
- what is degraded, fragile, or regressing now
- structural issues that need deliberate revisiting
- underlying technical issues that create repeated bugs, support load, or hidden cost
- the smallest next sequence that improves posture without defaulting to rewrite

## Evidence Rules

- Do not invent customer, incident, or operational signals. If they are missing, call that out explicitly.
- Prefer current repo evidence over historical review text. Reconcile drift instead of copying older conclusions forward.
- Promote only findings with direct evidence: code paths, config, missing tests, broken flows, stale docs, issue trails, or operational artifacts.
- Separate `Open`, `Partially Resolved`, `Resolved`, `Needs Re-check`, `Deferred`, and `Obsolete`.
- Distinguish symptoms from root causes. Merge duplicate findings under one canonical ID when they share the same cause.
- Default against recommending major re-architecture. Recommend it only when the evidence shows repeated incidents, blocked delivery, or unresolved high-severity structural risk.

## Workflow

### 1. Build context

Inspect:

- primary user flows and product surfaces
- architecture, trust boundaries, and data movement
- release workflow, CI, and operational safeguards
- backlog, TODO hotspots, prior audits, and open regressions
- cost-sensitive paths, heavy queries, jobs, or integrations

If available, also use:

- support trends
- analytics or conversion data
- uptime or incident records
- customer complaints or operator runbooks

### 2. Scaffold artifacts

Use `scripts/scaffold_review.py` to create the standard review folder under `docs/reviews/`. Unless the user asks otherwise, keep the default dated folder name so reviews remain comparable over time.

### 3. Score current state

Use the five-axis scorecard from `references/review-rubric.md`:

- Product
- Reliability
- Security/Tenant
- Delivery
- Cost

Do not inflate scores. A `3/5` should mean usable but materially constrained, not "good enough."

### 4. Write the ledger first

Populate `30-findings-ledger.md` before narrative files. Every summary claim should trace back to at least one ledger item or explicit positive evidence in the repo.

### 5. Synthesize decisions and plan

- Put the executive posture, strengths, risks, and major recommendation in `10-executive-summary.md`.
- Put supporting narrative for each axis in `20-scorecard.md`.
- Put root-cause and architecture guidance in `40-structural-issues.md`.
- Put sequenced next steps in `50-priority-plan.md`.
- Preserve the difference between immediate hardening, staged structural work, and gated major work.

## Output Requirements

Produce the review pack defined in `references/output-format.md`:

- `00-index.md`
- `10-executive-summary.md`
- `20-scorecard.md`
- `30-findings-ledger.md`
- `40-structural-issues.md`
- `50-priority-plan.md`

If evidence is thin, still produce the pack. Put uncertainty and missing signals in `40-structural-issues.md` and the final summary instead of filling gaps with speculation.

## Final Response

Return a concise summary that includes:

- overall posture scores
- resolved or partially resolved items when relevant
- open P0 and P1 risks
- what is working
- structural issues to revisit
- underlying technical issues
- recommended sequence
- major-work recommendation or gate

Follow the exact summary format in `references/output-format.md`.

## References

- Review rubric: `references/review-rubric.md`
- Output pack and summary format: `references/output-format.md`
