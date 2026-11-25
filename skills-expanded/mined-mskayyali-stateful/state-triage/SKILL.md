---
name: state-triage
description: Recommend evidence-aware risk and scope decisions for a complete Stateful condition inventory, recording likelihood, impact, confidence, rationale, and one of in, out-with-implication, or out for human confirmation. Use after state-list or state-audit and before specification. Do not persist recommendations or continue to specification until a human confirms them.
---

# Condition Triage

Make scope decisions cheap to review without transferring ownership to the agent.

## Procedure

1. Read the complete inventory and `STATEFUL.md`. Require the current iteration’s feature, platforms, commitments, constraints, and available evidence.
2. For each condition, recommend:
   - likelihood: `low`, `medium`, or `high`;
   - impact: `low`, `medium`, or `high`;
   - confidence: `hypothesis`, `informed`, or `measured`;
   - a one-sentence evidence-grounded rationale;
   - scope: `in`, `out-with-implication`, or `out`.
3. Do not equate likelihood with priority. Elevate irreversible, safety, security, privacy, regulatory, or high-blast-radius conditions even when rare.
4. For `out-with-implication`, name the concrete constraint on in-scope copy, naming, policy, data, architecture, or testing.
5. For `out`, record why it is deferred and what would trigger reconsideration.
6. Check dependencies and relationships. An in-scope condition cannot rely on an incompatible out-of-scope precondition without an explicit implication.
7. Summarise high-impact hypotheses separately; they require evidence collection, not confident-looking prose.
8. Present the full recommendation and stop. Ask the human to confirm or adjust.
9. Only after confirmation:
   - persist scope and priority;
   - set `status: triaged` unless a condition was already at a later status;
   - update `STATEFUL.md`;
   - preserve deferred conditions.

## Output

```text
| ID | Condition | Likelihood | Impact | Confidence | Recommended scope | Rationale / implication |
|---|---|---|---|---|---|---|

## Totals
In: <n> · Out-with-implication: <n> · Out: <n>
High-impact hypotheses: <n>

## Consistency flags
- <dependency or scope conflict>

Confirm or adjust? No decisions will be persisted until you do.
```

Include layers and failure cause when present.

## Failure modes

- Persisting agent recommendations before confirmation.
- Scoping by implementation difficulty rather than relevance.
- Treating `out` as deletion.
- Omitting the implication.
- Assigning false precision unsupported by evidence.
- Allowing high-impact hypotheses to disappear into a total.
