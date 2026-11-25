---
name: grill-with-docs-qa-filter
description: >-
  Supplemental decision-filtering policy for grill-with-docs. Use together
  with the primary skill when a user wants fewer, higher-value questions:
  automatically resolve routine decisions with the recommended default,
  reserve 5%-20% of decision points for major or genuinely controversial
  questions, and ask exactly one question at a time. This skill is not
  standalone and must not replace the primary skill's exploration,
  terminology, documentation, ADR, or decision-recording workflow.
---

# Grill with Docs: Q&A Filter

## Keep the primary workflow in control

Use this Skill only as a question-selection layer for `grill-with-docs`.

- Keep `grill-with-docs` as the primary workflow and source of truth.
- Apply this Skill only while selecting and presenting decisions.
- Do not repeat or replace code exploration, domain analysis, terminology work, documentation, ADR creation, or session closure.
- Return every resolved decision and its rationale to the primary workflow for recording.
- Follow `grill-with-docs` whenever instructions conflict outside the question-selection stage.

## Classify genuine decisions

Use the decision points and evidence already produced by the primary workflow. Do not manufacture extra decisions to satisfy a quota.

Classify each decision as:

- `auto`: adopt the recommended answer without interrupting the user.
- `ask`: present the decision because it is major or genuinely controversial.

Prefer `ask` when a decision:

- defines agent autonomy or human-control boundaries
- changes core business behavior or user experience
- affects permissions, safety, releases, irreversible data, or external side effects
- is expensive to reverse
- has multiple defensible business answers
- blocks several downstream decisions

Treat reversible defaults, naming, internal interfaces, component reuse, and ordinary implementation details as `auto` unless they materially change business behavior.

## Enforce the question budget

Let `N` be the number of genuine decision points and `Q` the number classified as `ask`.

For `N >= 5`, keep:

- `Q >= ceil(N * 5%)`
- `Q <= floor(N * 20%)`

For fewer than five decisions, ask at most one question and only when it is genuinely necessary.

Do not inflate `N` by splitting one decision into cosmetic sub-decisions.

For every `auto` decision:

1. Adopt the recommended answer.
2. Return the decision and rationale to `grill-with-docs` for unified recording.
3. Continue without asking the user.

## Review only high-value questions

When the host permits subagents and the user has authorized delegation, use one or two independent, read-only reviewers immediately before presenting an `ask` decision. Do not use reviewers to replace the primary workflow or run a parallel interview.

Give every reviewer the same neutral evidence:

- the precise decision
- established facts and constraints
- concrete business scenarios
- available alternatives

Do not reveal the primary agent's recommendation before reviewers respond.

Ask reviewers to provide:

- whether the decision is truly major or controversial
- their recommended answer
- the strongest counterargument
- missing evidence or risks

Use the results as an objectivity check. The primary agent remains responsible for the recommendation and the user interaction. If reviewers agree that the decision is not major, downgrade it to `auto`.

## Ask exactly one question

Present one decision per turn:

```text
Question: <clear business decision>

Current state: <necessary facts and scenarios>
Recommendation: <recommended answer>
Trade-off: <main benefit, cost, and independent review signal>

Should we proceed with <recommended answer>?
```

Do not append secondary questions.

After the user answers:

1. State the resolved decision briefly.
2. Return it to `grill-with-docs` for recording.
3. Recalculate affected downstream recommendations.
4. Continue with the next `ask` decision.
