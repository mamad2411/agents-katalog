# Competitor Analysis

## Purpose
Run evidence-disciplined competitor teardowns: decompose rival interfaces and workflows into atomic observations, separate observed evidence from inference, score against heuristics, and convert findings into ranked, actionable opportunities — never vibe-based opinions.

## Use when
- Planning a feature and needing to know how named competitors solve the same user goal.
- Decomposing competitor onboarding, checkout, settings, or core-loop workflows step by step.
- Building a feature-comparison matrix or positioning argument backed by captured evidence.
- Auditing competitor accessibility, IA, or performance ergonomics for gap analysis.

## Do not use when
- Conducting original user research with your own users (use `design-research`).
- Writing final component props or API contracts (use `component-specification`).
- Copying competitor visual design wholesale — analysis informs decisions, it does not replace design.

## Required context
- Competitor set: named products/versions and in-scope workflows for teardown.
- Evaluation dimensions: ergonomics, IA, accessibility, performance, pricing-relevant UX.
- Evidence corpus: screenshots, recordings, docs URLs with capture dates.

## Procedure
1. **Scope the Teardown**: Name 3–5 competitors with exact versions/platforms and 1–3 workflows each (e.g., "Acme v4.2 iOS signup → first project"). Record capture dates; stale captures (> 90 days) are flagged, not trusted.
2. **Capture Atomic Evidence**: Walk each workflow click by click. Log one observation per row: screen, element, behavior, cost (clicks, time, errors). Example: "Step 4/9: plan picker pre-selects annual; monthly requires expanding a disclosure."
3. **Separate Evidence from Inference**: Every finding has two fields — `observed` (what happened, with screenshot ref) and `inferred` (why it matters, marked as hypothesis). Inferences without a validation plan are labeled `unvalidated`.
4. **Score Heuristics**: Rate each workflow on Nielsen Norman heuristics plus WCAG AA spot-checks (keyboard path, contrast, focus visibility). Use a fixed 1–5 rubric so competitors are comparable.
5. **Rank Opportunities**: Convert gaps into opportunities scored by (user impact × frequency) ÷ implementation cost. Top-3 opportunities each get a one-paragraph proposal with the evidence IDs that justify it.
6. **Verify**: Run `scripts/verify.sh`. Confirm every claim links to dated evidence, every inference is labeled, and the matrix is complete for the scoped workflows.

## Decision rules
- **No Claim Without Capture**: Any statement about a competitor must reference a dated screenshot, recording timestamp, or doc URL.
- **Evidence ≠ Inference**: Never present an interpretation ("their funnel is optimized") as an observation; keep the two fields physically separate.
- **Fixed Rubric**: All competitors scored on the same heuristic rubric; ad-hoc praise or criticism is not evidence.
- **Recency Label**: Captures older than 90 days are marked stale and excluded from opportunity ranking.

## Evidence required
- Teardown matrix with per-step observations and evidence links.
- Heuristic scorecards on the fixed 1–5 rubric for each scoped workflow.
- Ranked opportunity list with impact/cost rationale and evidence IDs.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Competitor teardown matrix with evidence-linked findings.
- Opportunity list ranked by user impact and implementation cost.
- Pattern-extraction notes separating observed evidence from inference.

## Stop conditions
- Teardown matrix complete with evidence links and ranked opportunities.
- All inferences labeled; stale captures excluded from ranking.
- Token budget exhausted.

## Escalation rules
- Escalate to product lead if the competitor set itself is disputed (market-definition decision, not analysis).
- Escalate immediately if analysis requires accessing competitors in ways that violate their ToS (scraping, credential sharing).
