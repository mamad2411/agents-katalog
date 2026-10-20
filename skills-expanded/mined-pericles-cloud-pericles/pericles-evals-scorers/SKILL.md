---
name: pericles-evals-scorers
version: 2026.05.1
description: >
  How to write Mastra scorers and gate Skills on them in Pericles. Use this WHENEVER
  you create or modify a scorer, promote a Skill toward published, or investigate a
  quality regression. Reflects the real createScorer API (@mastra/core/scores) with
  an LLM judge + preprocess, the three existing scorers in monitoring-scorer.ts, the
  no-eval-no-publish rule, the promotion gate, and drift detection.
doctrine_refs: [Manifest §3, §5; Ops §5]
depends_on: [pericles-mastra-tool]
last_reconciled: 2026-05-28
---

# Pericles Evals & Scorers (build skill)

Evals are how a Skill earns and keeps the right to run. The platform ships three
scorers; treat them as the model. **No Skill reaches `published` without an
`eval_criteria` reference, and a published Skill that regresses is caught — at
promotion and continuously in production.**

## When to use this skill

Writing/modifying a scorer; setting a Skill's `eval_criteria`; promoting a Skill from
`draft`/`poc` to `published`; diagnosing a drift alert.

## The real scorer API (as in monitoring-scorer.ts)

Scorers use `createScorer` from `@mastra/core/scores` with an LLM judge and a
`.preprocess()` step. `@mastra/evals` is also a dependency. The existing three live in
`backend/src/mastra/scorers/monitoring-scorer.ts` and are registered in
`backend/src/mastra/index.ts`:

```ts
import { createScorer } from '@mastra/core/scores';

export const relevanceScorer = createScorer({
  name: 'Geographic and Risk Type Relevance',   // human-readable; shows in dashboards
  description: 'Evaluates if detected events are geographically relevant…',
  type: 'agent',
  judge: {
    model: 'openai/gpt-4o-mini',
    instructions: 'You are an expert evaluator… Return only structured JSON matching the schema.',
  },
})
  .preprocess(({ run }) => {
    // extract events + org context from the agent output
  })
  // … generateScore / analyze steps per the Mastra scores API
  ;
```

- `relevanceScorer` — geographic + risk-type relevance to the org.
- `severityAccuracyScorer` — calibration of the 0.0–1.0 severity.
- `deduplicationScorer` — duplicate-detection effectiveness.

Reuse these where applicable before authoring new ones. For LLM-judge scorers, **pin
the judge model and instructions** so scores are comparable across versions. The
`name` is a human string used in dashboards and the promotion gate.

## The promotion gate (draft/poc → published)

- Passing scorer suite against a **versioned reference test set**.
- **Every scorer above its declared threshold.**
- **No scorer regressing more than 5%** vs the prior published version on the same set.
- Functional Skills: verify `data_access.pattern` matches behavior
  (`pericles-functional-agent`).
- Tool-binding Skills: security review. Knowledge-source Skills: provenance review.

A broken eval blocks merge. PoC Skills (e.g. Validation Agent) are flag-gated and
excluded from the default Skill Stack until promoted.

### Validation Agent special case

Its eval suite MUST include cases where Validation rejects events Monitoring confirmed
(and vice versa) — impossible unless it genuinely reaches beyond Monitoring's view. The
suite is also the proof it is `pre_validation` rather than confidence-scoring on
Monitoring's output.

## Production drift detection

Track each Skill's scorer means over 7 / 30 / 90 days; alert when the 7-day rolling
mean drops more than two standard deviations below the 90-day baseline; auto-create a
remediation ticket to the owner; >2 weeks unresolved → quarterly doctrine audit.
Scores log per invocation (`eval_scores`) — `pericles-observability`. Note Mastra
`observability.default.enabled` is on (AI tracing), which feeds the eval pipeline.

## What this forbids

Promoting any Skill to `published` without `eval_criteria`; merging a change that
breaks the suite or regresses a scorer >5%; promoting Validation from PoC without
rejection/confirmation divergence cases; silently changing a judge model/rubric or
test set so historical comparisons break (version them).

## templates/scorer.template.ts

A scaffold matching the real `createScorer` API is in `templates/scorer.template.ts`.

## Existing standards (read alongside)

`backend/src/mastra/scorers/monitoring-scorer.ts`; `CLAUDE.md` (scorers in the Mastra
config); `.claude/rules/06-mastra.md`; `.cursor/rules/700-ai/701-mastra-agent-core-standards-auto.mdc`.

## Open questions

- The exact post-`preprocess` step names (`generateScore`/`analyze`) in
  `@mastra/core/scores@^0.x` — confirm against the installed version and update the
  template.

## Changelog

- 2026.05.1 — Reconciled to the real createScorer API (@mastra/core/scores, LLM judge
  gpt-4o-mini, .preprocess); cited monitoring-scorer.ts and @mastra/evals.
- 2026.05.0 — Initial draft.
