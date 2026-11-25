---
name: mobile-design-review
description: Audit mobile product briefs, UX architectures, UI specifications, design-system artifacts, screenshots, prototypes, or implemented apps for product fit, task completion, information architecture, state coverage, visual consistency, native iOS/Android behavior, accessibility, privacy, ethics, brand differentiation, and implementation readiness. Use when Codex needs blockers, P0-P3 findings, a 100-point score, evidence-backed fixes, verification steps, regression review, or a release/design handoff decision.
---

# Mobile Design Review

Produce an evidence-backed quality decision, not taste commentary. Every finding names the affected artifact/location, user impact, concrete fix, and verification method.

## Select review mode

- **Package review**: audit brief, Design DNA, UX architecture, wireframe, design system, UI specification, prototype, and code handoff together.
- **Visual review**: audit screenshots, Figma frames, or rendered concepts against upstream contracts.
- **Implementation review**: audit a running app or code plus visual/system behavior.
- **Regression review**: verify that selected prior findings are fixed without introducing new failures.

Review only what the user supplied or authorized. Do not modify designs or code unless the user also requests fixes.

## Establish the evidence contract

Inventory every source with stable IDs, path/URL, version/date, platform, and limitation. Validate structured upstream artifacts when validators exist.

Separate:

- `observed`: directly present in an artifact or runtime.
- `derived`: found by deterministic schema, coverage, contrast, target-size, or consistency checks.
- `risk`: plausible failure needing prototype/device/user validation.
- `not-tested`: required check that the available evidence cannot establish.

Do not claim contrast, screen-reader behavior, target size, animation performance, delivery semantics, or platform compliance from a prose specification alone.

## Follow the workflow

### 1. Reconstruct the contract

Extract primary user, core task, activation, must requirements, non-goals, trust boundaries, screen/state coverage, design principles, platform targets, and acceptance signals. Resolve conflicting sources by authority and date; report unresolved conflicts.

### 2. Run deterministic checks first

Run available JSON/schema validators and inspect missing/extra IDs, state coverage, orphan components/screens, token provenance, broken references, duplicate responsibilities, and empty acceptance signals. Record tool results as evidence; a passing schema is not a passing design.

### 3. Review critical flows end to end

Trace activation, dominant loop, failure/recovery, permission denial, destructive actions, interrupted work, and exit. Check whether each step communicates system truth and preserves user control.

### 4. Review every quality dimension

Use [references/review-rubric.md](references/review-rubric.md). Inspect:

- Product and task match.
- Information architecture and UX.
- Visual hierarchy and consistency.
- Platform-native behavior.
- State and recovery completeness.
- Accessibility, privacy, and ethics.
- Brand differentiation and anti-copying.

For rendered or implemented UI, read [references/visual-review-method.md](references/visual-review-method.md) and inspect each supplied view rather than filenames alone.

### 5. Classify severity

- `P0`: safety, privacy, security, irreversible data loss, legal exposure, or core task impossible for most users. Release blocker.
- `P1`: core task, trust, accessibility, or platform failure with major impact and no acceptable workaround. Fix before release/design handoff.
- `P2`: comprehension, efficiency, recovery, consistency, or maintainability problem with a workaround. Schedule before polish.
- `P3`: low-impact refinement or visual polish.

Mark `blocker: true` only for P0 or an explicit rubric blocker. Do not inflate severity to make the report look important.

### 6. Write actionable findings

Each finding must answer:

1. What is wrong or unverified?
2. Where is the evidence?
3. Which user/task is affected?
4. What consequence follows?
5. What exact change is recommended?
6. How will a reviewer prove it is fixed?

Keep separate issues separate when they have different owners or verification methods. Combine repeated instances under one system-level finding when the same fix resolves them.

### 7. Score without hiding blockers

Score out of 100 using the fixed dimension maximums. Every deduction references one or more finding IDs. A high score never overrides a blocker. Treat untested high-risk requirements as findings or explicit release conditions, not automatic passes.

### 8. Make a decision

Use one result:

- `pass`: no blocker or P1; ready for the stated next stage.
- `conditional-pass`: no blocker; P1 or required validation remains, with explicit conditions.
- `fail`: one or more blockers.

Name the next stage: wireframe, visual production, implementation, usability test, beta, or release.

### 9. Produce and validate

When files are requested or this Skill is part of a workflow, create:

- `review-report.md` using [assets/review-report-template.md](assets/review-report-template.md).
- `review.json` using [assets/review-template.json](assets/review-template.json) and [references/review-schema.md](references/review-schema.md).

Run `python3 scripts/validate_review.py <path-to-review.json>` and fix every error.

## Run the quality gate

Do not finish until every score deduction traces to a finding, every P0 is a blocker, every P1 has an owner/verification path, missing tests are distinguished from observed failure, and the decision matches the issue set.
