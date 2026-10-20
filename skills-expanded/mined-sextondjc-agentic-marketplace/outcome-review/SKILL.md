---
name: outcome-review
description: Use when intended outcomes must be compared with actual post-ship results so teams can decide whether to expand, iterate, hold, or retire a delivered change.
---

# Outcome Review

## Specialization

Evaluate whether delivered work achieved its intended outcome.

This skill focuses on post-ship result review rather than release execution. It compares expected outcomes to actual signals and recommends the next product or delivery decision.

## Objective

Produce an outcome review artifact that states what was expected, what actually happened, what confidence exists in the result, and what decision should follow.

## Trigger Conditions

- A shipped change has enough time-in-market or early-life data for review.
- Teams need to know whether to expand, iterate, hold, or retire a change.
- Delivery learning should be tied to outcome evidence, not only to release process.
- Agents need a deterministic post-ship decision workflow based on result evidence.

## Scope Boundaries

In scope:

- Expected versus actual outcome comparison.
- Signal quality and confidence review.
- Decision recommendation.
- Follow-up action definition.

Out of scope:

- Incident root-cause analysis.
- Release gate approval.
- New discovery from scratch.
- Detailed experimentation execution.

## Inputs

- Original outcome statement or change objective.
- Success signals and guardrails defined before ship, when available.
- Actual post-ship results and contextual notes.
- Review window and affected segment or scope.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Expected-versus-actual outcome table.
- Signal quality note describing evidence confidence and caveats.
- Decision recommendation: expand, iterate, hold, or retire.
- Follow-up action list with owner and trigger.
- Residual uncertainty note where attribution is weak or mixed.

## Deterministic Workflow

1. Restate the original intended outcome and success signals.
2. Define the review window and segment under review.
3. Gather actual outcome signals and note major confounders.
4. Compare expected versus actual results in one table.
5. Evaluate confidence in the signals and identify attribution limits.
6. Choose one recommendation: expand, iterate, hold, or retire.
7. Record the follow-up actions, owners, and re-review trigger.
8. Publish the review artifact as a durable decision record.

## Outcome Decision Rules

- Expand when results beat or meet the target with acceptable guardrails and confidence.
- Iterate when the direction is promising but the result or experience needs change.
- Hold when the signal is inconclusive, unstable, or not yet mature enough.
- Retire when the change fails its outcome or creates unacceptable side effects.

## Artifact Contract

| Artifact | Minimum Fields |
|---|---|
| Outcome table | Intended outcome, expected signal, actual signal, variance |
| Signal quality note | Confidence, caveats, attribution limits |
| Decision record | Recommendation, rationale, review date |
| Follow-up list | Action, owner, target or trigger |

## Anti-Patterns

- Calling a release successful without checking outcomes.
- Treating weak correlation as strong causation.
- Avoiding a decision by endlessly extending the review window.
- Recording follow-up ideas without owners or triggers.

## Done Criteria

- All required outputs exist.
- Expected and actual results are compared explicitly.
- One recommendation is recorded.
- Follow-up actions and uncertainty notes are present.
- Source catalog entries are current for this evaluation cycle.

## Workflow

1. Capture inputs and constraints.
2. Execute this skill's deterministic steps.
3. Publish outputs with status and next actions.

## Execution Context
### Input Context

- Request objective and scope boundary.
- Applicable constraints and required outputs.

### Process Context

- Follow this skill's deterministic workflow from intake to closure.
- Record ownership and decisions for required outputs.

### Output Context

- Deliverables with explicit completion status.
- Residual risks and next actions.
## References Assets

- [Reference assets](./references/README.md)
