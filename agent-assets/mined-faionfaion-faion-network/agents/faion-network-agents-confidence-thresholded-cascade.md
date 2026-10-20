# Confidence-Thresholded Cascade

## Summary

**One-sentence:** Sends each request to a cheap model first, accepts when self-reported confidence clears a calibrated threshold, escalates otherwise, cutting cost 50-95% on mixed-difficulty traffic without quality regression.

**One-paragraph:** Send the request to a cheap model first. The cheap model returns an answer AND a confidence score. If confidence is above threshold, accept it; otherwise escalate to the expensive model. This is FrugalGPT's core insight — most production tasks are easy, and a calibrated cheap model can self-detect when it is out of its depth. Production deployments routinely report 50-95% cost reductions while matching or exceeding strong-model-only baselines on benchmarks.

**Ефективно для:** високооб'ємного трафіку класифікації, тріажу, FAQ-ботів, де якість виміряна евалом, а 70-90% запитів насправді тривіальні.

## Applies If (ALL must hold)

- High-volume traffic where cost dominates (chatbots, classifiers, batch processing).
- Task difficulty is mixed (some easy, some hard) so cascade has room to adapt.
- Latency tolerates one extra round-trip on the escalated fraction.
- Confidence is elicitable on the task (classification, factual extraction, structured output).

## Skip If (ANY kills it)

- Mission-critical decisions where any error has high cost — go straight to the strong model.
- Tasks where "confidence" is meaningless (creative writing, open-ended planning).
- Cold-start with no eval data — cheap model has not learned its limits yet.
- Latency-critical interactive flows where the second hop blows the user-perceived budget.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Eval set of 100+ tasks with ground truth | List of `{input, expected_output}` | Engineering eval pipeline |
| Cheap model output schema | Pydantic BaseModel with `reasoning`, `answer`, `confidence_0_to_1` | Application code |
| Strong model output schema | Pydantic BaseModel with `reasoning`, `answer` | Application code |
| Provider keys (cheap + strong) | Env vars or secret manager | Deployment config |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| `embedded-scratchpad-field` | Reasoning must come before confidence in the cheap-model schema. |
| `enum-constraints-closed-vocabularies` | Closed answer sets stabilize confidence calibration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Calibration + escalation rules (5 testable rules) | ~1000 |
| `content/02-output-contract.xml` | essential | CheapAnswer + StrongAnswer schemas, cascade contract | ~900 |
| `content/03-failure-modes.xml` | essential | Uncalibrated threshold, always-escalate, deep cascades | ~800 |
| `content/04-procedure.xml` | recommended | Eval → calibrate → deploy → monitor loop | ~900 |
| `content/05-examples.xml` | recommended | Customer-support, FAQ, code-review triage worked examples | ~700 |
| `content/06-decision-tree.xml` | essential | Should this task use cascade, single-strong, or three-level? | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Run the cheap leg of the cascade | haiku | This is the cheap model by definition |
| Run the escalated leg | sonnet or opus | Strong model picks up when the cheap leg defers |
| Calibrate threshold from eval data | sonnet | One-shot offline analysis, no loop |
| Design a new cascade for a new task | opus | Architectural tradeoffs across confidence elicitation, latency, cost |

## Templates

| File | Purpose |
|------|---------|
| `templates/two-level-cascade-pydantic.py` | Python implementation of two-level cascade with Pydantic + Anthropic client (covers core cascade pattern) |
| `templates/_smoke-test.json` | Minimum viable cheap-model output for self-test of the validator |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-confidence-thresholded-cascade.py` | Validates a cascade output schema and threshold settings | Pre-commit on any change to the cascade module |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[embedded-scratchpad-field]]
- [[enum-constraints-closed-vocabularies]]
- [[gateway-fallback-chain]]

## Decision tree

See `content/06-decision-tree.xml`. The root question asks whether the task has high volume AND elicitable confidence. The tree then branches by criticality (mission-critical → single-strong only) and by difficulty distribution (uniform → two-level enough; long-tail → three-level worth the cost). Each leaf maps to a concrete rule in `01-core-rules.xml`.
