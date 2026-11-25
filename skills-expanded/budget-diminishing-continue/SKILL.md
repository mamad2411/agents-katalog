---
name: budget-diminishing-continue
description: "Issue continuation nudges while the turn stays under budget, then halt once diminishing returns or the budget cap justify stopping."
metadata:
  author: ychampion
---

# SKILL: Budget Diminishing Continue
**Domain:** tool-orchestration  
**Trigger:** Apply when you have a task-level token budget and must decide between continuing and stopping while respecting diminishing returns.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
Track the cumulative tokens consumed per turn, issue a continuation nudge while the usage stays below `completionThreshold` (90% by default), and stop once token deltas shrink across repeated continuations. Diminishing-return detection keeps the loop from looping forever: once two cells in a row add fewer than `DIMINISHING_THRESHOLD` tokens, or the tracker reached several continuations, stop and emit the final completion payload. The tracker also guides `budgetDecision.action` so callers can differentiate between gentle nudges and hard stop signals.

## Key Rules
- Initialize `BudgetTracker` at turn start and update `continuationCount`, `lastDeltaTokens`, and `lastGlobalTurnTokens` after each continuation decision.
- Allow continuations only when under `budget * COMPLETION_THRESHOLD` and the last token deltas are meaningful; otherwise treat it as diminishing returns.
- When stoppage occurs due to diminishing returns, include the `completionEvent` that records counts, percentages, and elapsed duration so callers can log or surface why the turn ended.
- If the budget or agent ID is missing, return an immediate `stop` with `completionEvent = null` to avoid undefined behavior.
- Always compute the continuation message via `getBudgetContinuationMessage` so the user sees consistent phrasing and the tracker returns the tidy `pct`/`turnTokens` metrics.

## Example Application
If a query advances toward a 100k token budget, continue streaming until usage hits 90% or token growth slows; when the stop decision triggers, log the diminishing-returns flag so both user and telemetry know the stream ended intentionally.

## Anti-Patterns (What NOT to do)
- Do not keep continuing just because the earlier logic returned `continue`; re-run the decision each iteration to respect the latest token deltas.
- Do not drop the `completionEvent` data when stopping; it contains the telemetry the backend uses to tell budgets apart from user cancellations.
