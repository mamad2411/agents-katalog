# Closed-Set Output Validation

## Summary

**One-sentence:** Produces a Closed-Set Validation Contract: when the legal values of an output field are an enumerable set you supplied in the request, groundedness is set membership — exact, zero tokens, no model, no threshold — and the whole entailment stack is the wrong tool.

**One-paragraph:** Groundedness research is written for systems that generate prose, so it teaches claim decomposition and entailment scoring: split the answer into atomic claims, ask an NLI model whether each is supported, divide. That is an approximation, and the approximations are expensive and only ~64-77% balanced-accurate. But a large share of real LLM outputs are not prose at all — they are selections: an identifier, a slug, a category, a file path, a customer record, a ranked list of things you handed the model a moment ago. For those the exact answer is free. Compute `grounding_rate = |E ∩ C| / |E|` over emitted values `E` and the candidate set `C` you supplied, and you have a groundedness metric with no false positives, no threshold to tune, no judge cost and no dependency. This methodology gives the test for whether your space is genuinely closed, the contract for enforcing membership, the rule that a dropped value must be counted rather than logged, and the boundary line: mixed outputs have a closed field and an open field, and the metric only ever covers the closed one.

**Ефективно для:**

- Retrieval and search that returns identifiers from a candidate list rather than prose.
- Routing, classification and tool selection — the label space is the enum you wrote.
- Any pipeline about to add a groundedness scorer, a judge model or a RAG-eval dependency for a field whose legal values are already written down.
- Teams whose hallucination handling is a `logger.Warn` and who therefore have no idea what their rate is.

## Applies If (ALL must hold)

- At least one output field's legal values can be enumerated at request time.
- That enumeration comes from an artefact YOU supplied or control — not from the model's memory of the world.
- Something downstream acts on the value, so a wrong one has a consequence.

## Skip If (ANY kills it)

- The output is genuinely open prose and every field is free text — you need entailment, not membership.
- The candidate set is only knowable after the model answers (open-world lookup, arbitrary URL, novel identifier) — the space is not closed and pretending it is will drop valid answers.
- The set is closed but unbounded in practice (millions of members streamed at request time) and the membership check would cost more than the error it prevents.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Seven testable rules. R1 is the closedness test; R2-R4 are the enforcement and the metric; R5-R7 are the boundaries — mixed outputs, the anti-pattern, and the licences on the fallback scorers. |
| `content/02-output-contract.xml` | The Closed-Set Validation Contract: every field, the metric definition, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six failure modes with symptom, cause and the rule that prevents each. |
| `content/06-decision-tree.xml` | Routing from observable output shape to membership check / entailment / neither. |
| `scripts/validate-closed-set-output-validation.py` | Validates a contract; rejects log-only handling, unbaselined thresholds, non-commercial scorers and claim decomposition of short justification strings. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/closed-set-validation-contract.yaml` | Fill-in contract for a fully closed output; ships valid. |
| `templates/closed-set-validation-contract-mixed.yaml` | The common real case — a closed identifier field beside an open prose field, with the metric scoped honestly. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `hallucination-attribution-checklist` — attribution for open outputs; this methodology is the closed-set branch of the same question.
- `hallucination-detection-online` — the runtime scorers, their accuracies and their licences, for the open fields this contract deliberately does not cover.
- `llm-hallucination-test-patterns` — packages the membership check as a CI test class; this methodology defines the metric it asserts on.
- `schema-semantic-constraint-gap` — membership is the strongest instance of post-validating what the grammar cannot express; a `pattern` on an ID field is weaker than checking the ID is one you supplied.
