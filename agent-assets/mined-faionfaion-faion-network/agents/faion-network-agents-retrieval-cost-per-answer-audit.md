# Retrieval Cost Per Answer Audit

## Summary

**One-sentence:** Produces a Retrieval Cost Ledger — ten real queries measured end to end — that yields the two numbers every downstream retrieval decision needs: median tokens per lookup and the overhead ratio of retrieval spend to delivered body.

**One-paragraph:** Retrieval is billed on what it reads, not on what it returns. Almost nobody measures the difference. The published spread between structures is 380x on the same corpus and the same model, so a structure choice made without a number is a guess with three orders of magnitude of room in it. This methodology is the measurement, not the choice: ten representative queries, per query the index tokens, the candidate tokens, the delivered-body tokens and whether the answer was correct, then two derived numbers. The overhead ratio is the one that surprises people — a system can deliver a 3.3k-token answer while spending 33k getting there and never notice, because the bill arrives as latency and context pressure rather than as a line item. The ledger is the required input to `context-graph-engineering`, whose gate refuses to run without it.

**Ефективно для:**

- Anyone about to choose, replace or "upgrade" a retrieval structure — the ledger is the only honest starting point.
- Systems where retrieval got slowly more expensive and no one can say when or by how much.
- Deciding whether a hierarchy needs compressing before anything more elaborate is considered.
- Settling a graph-versus-tree-versus-flat argument with a measurement instead of a preference.

## Applies If (ALL must hold)

- A retrieval structure exists and is queried repeatedly by an LLM or agent.
- Token counts per call are observable — from the provider's usage field, a proxy log, or a local tokenizer over the exact strings sent.
- At least ten real queries can be collected that reflect actual traffic, not a demo set.

## Skip If (ANY kills it)

- The whole corpus fits in the context window and is dumped whole — there is no retrieval to audit.
- Retrieval is a single lookup by known primary key with no index read — cost is the row, and there is nothing to measure.
- No one can obtain token counts and no local tokenizer is available; an estimated ledger is worse than none, because it will be cited as measurement.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Six testable rules. R1 fixes what counts as a lookup; R5 is the reference table that lets a reader place their own number. |
| `content/02-output-contract.xml` | The Retrieval Cost Ledger: every field, the derived numbers, and the consistency rules the validator enforces. |
| `content/03-failure-modes.xml` | Six ways a cost audit produces a confidently wrong number. |
| `content/06-decision-tree.xml` | Routing from the measured overhead ratio to compress / restructure / leave alone. |
| `scripts/validate-retrieval-cost-per-answer-audit.py` | Validates a ledger; recomputes the medians and the overhead ratio from the rows. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/retrieval-cost-ledger.yaml` | Fill-in ledger with ten rows; ships valid against the contract. |
| `templates/measure-lookup.md.j2` | Instrumentation recipe: where to put the counter for the four common retrieval shapes. |
| `templates/measure-lookup.md` | Instrumentation recipe: where to put the counter for the four common retrieval shapes. Generated from `templates/measure-lookup.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `context-graph-engineering` — consumes this ledger. Its `Skip If` refuses the methodology outright when the incumbent cost is unmeasured; this is the upstream that supplies it.
- `inference-cost-unit-economics` — money per feature and gross margin. This methodology is one input to it, denominated in tokens per lookup rather than currency per outcome.
- `rag-eval-retrieval-metrics` — recall and MRR. Correctness here is a coarse binary used only to make cost-per-correct-answer computable; use that methodology for real quality measurement.
- `retrieval-drift-alerting-recipe` — after the ledger establishes a baseline, that recipe watches it for movement.
