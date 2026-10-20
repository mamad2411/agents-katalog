# Two-Pass: Free-Form Reasoning Then Structured Extraction

## Summary

**One-sentence:** Run the strong model in free text with NO format instruction in its prompt, then a cheap model with a strict schema over the transcript; recovers the accuracy that asking for a format costs on hard tasks (+6.8 pp, arXiv:2604.03616).

**One-paragraph:** Asking a model for a format while it is still reasoning measurably hurts accuracy — but the cost is in the prompt, not in the decoder. The Format Tax (arXiv:2604.03616, 2026-04-04) measures the format-requesting instruction and the grammar-constrained decode separately and finds 92% of statistically significant degradations already present with the instruction alone; the grammar mask adds little further harm. A format instruction compresses the visible reasoning channel before the model has finished solving, so it commits early. This methodology splits the work: pass 1 runs the strong model (extended thinking allowed) in free text with no schema, no field list and no "reply as JSON" anywhere in its prompt; pass 2 runs a cheap extractor with strict structured output over the transcript. The schema lands on the consumer; the reasoning never sees it. Decoupled two-pass recovers +6.8 pp on average and improves 42 of 72 model x task x format combinations — though frontier closed models have largely absorbed the tax, so the A/B rule still decides adoption.

**Ефективно для:**

- Math word problems, multi-step proofs, code generation з тонкими constraints — accuracy відновлюється (MATH-500 і ZebraLogic — найгірші під format instruction).
- Research synthesis: довгий аналіз → коротка структурна verdict.
- Legal / medical verdict tasks: ригідна schema без compromise на reasoning.
- Будь-який pipeline, де Opus extended thinking justified, але consumer хоче strict JSON.

## Applies If (ALL must hold)

- Task requires deep reasoning (math, proofs, multi-step code, research synthesis).
- Consumer requires strict JSON / Pydantic / Zod schema output.
- Latency budget allows two model calls (not sub-second).

## Skip If (ANY kills it)

- Simple extraction tasks (entities, sentiment, key-value) — single-pass strict SO is fine.
- Latency-critical (&lt; 1 s) paths — two calls always cost wall-clock.
- High-volume routes where doubled provider cost exceeds the accuracy gain.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strong-model client | Anthropic / OpenAI SDK | your provider |
| Extractor-model client | Haiku / GPT-4.1-nano / equivalent | your provider |
| Output schema | Pydantic / Zod / JSON Schema | consumer contract |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| none | This methodology is self-contained; no upstream artefact required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Background (why split, cost intuition) + 7 testable rules: two-pass-required, strong-model-free-text, extractor-deterministic, transcript-bounded, ab-vs-single-pass, strong-reasons-cheap-extracts, extractor-accuracy-gate — plus the 2026-08-04 causal correction, when-to-skip list, source links | 2800 |
| `content/02-output-contract.xml` | essential | JSON Schema for config + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with symptom/root-cause/fix (incl. extractor-input-bloat) | 1300 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 800 |
| `content/05-examples.xml` | recommended | Two-pass call pair (Opus thinking + Haiku strict) vs single-pass forced JSON; cache-friendly extractor prompt (python) | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on difficulty → latency → A/B delta → extractor accuracy → rule from 01-core-rules.xml | 550 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task_difficulty` | sonnet | Difficulty scoring needs light judgment. |
| `design_pass_pair` | sonnet | Picks models + thinking budget. |
| `run_ab_eval` | haiku | Mechanical eval execution. |
| `monitor_extraction_fidelity` | haiku | Schema-violation counting. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-two-pass-reason-then-extract.py` | Validate the config artefact against the schema | CI on each artefact change; pre-commit |

## Correction (1.2.0, 2026-08-04)

Up to 1.1.0 this methodology blamed the grammar mask for the accuracy loss. The prescription was right; the cause was wrong. Per arXiv:2604.03616 the loss sits overwhelmingly in the format INSTRUCTION in the prompt, so pass 1 must drop the schema from its prompt, not merely drop `response_format` from its request. Two knock-on corrections: a strict schema cannot cause a MISSING required field (constrained decoding makes the closing brace unreachable until it is emitted), so the ~30% required-field omission seen with the Anthropic Agent SDK `output_format=json_schema` on Sonnet 4.5 is an integration defect on that path rather than the format tax; and the production fix that followed it — plain text parsed into Pydantic — is the researched-correct shape, a one-pass degenerate form of what this methodology prescribes, not a superstitious workaround.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[weak-model-preselection]]
- [[tool-description-as-prompt]]
- [[schema-semantic-constraint-gap]] — what pass 2's schema still fails to enforce once you have it
- [[closed-set-output-validation]] — the exact check for pass-2 fields whose legal values you supplied

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, eval scores, stakes, noise ratio, etc.) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
