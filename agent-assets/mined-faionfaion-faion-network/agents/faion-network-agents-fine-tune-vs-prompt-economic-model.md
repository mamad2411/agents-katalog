# Fine-tune vs Prompt Economic Model

## Summary

**One-sentence:** Produces a filled spreadsheet (token spend, tuning cost, latency wins, vendor risk premium, break-even months) that turns the FT vs prompt debate into one number per scenario.

**One-paragraph:** Decision frameworks are conceptual; what builders actually need is the spreadsheet. This methodology produces a filled `economic-model.json` (machine-readable) + `economic-model.xlsx`-equivalent (human-readable) with inputs (volume, $/k tokens current+ft, training cost, ops overhead, vendor risk premium) and outputs (monthly delta $, NPV over 12 months, break-even month, sensitivity table). Scenarios required: base, 50% volume drop, 50% volume rise, +30% prompt+RAG cost reduction by year-end.

**Ефективно для:** RFC numbers backing `[[fine-tune-vs-prompt-decision-tree]]`, FinOps challenges, board / investor questions on AI roadmap cost, eng manager pitching the FT spend.

## Applies If (ALL must hold)

- Production workload with measurable daily token volume.
- Current $/k tokens known (provider invoice).
- Candidate fine-tune training cost + hosting $/k tokens estimable.
- Decision owner will use the numbers (not theatre).

## Skip If (ANY kills it)

- No production traffic — model has no input data.
- Less than $500/mo annualised spend — overhead exceeds savings.
- Provider locks both prompt and FT into the same $/k bucket (no economic difference).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Daily token volume | int (input_tok, output_tok per day) | observability |
| Current $/k tokens | float (input + output) | provider invoice |
| FT hosting $/k tokens | float | vendor quote |
| FT training cost | float (one-off) | vendor quote |
| Ops overhead | float ($/month, incl monitoring + on-call) | eng manager |
| Vendor risk premium | float % | infosec/finance |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[fine-tune-vs-prompt-decision-tree]]` | Decision artefact consumes these numbers. |
| `[[finetune-cost-vs-prompt-decision]]` | Sibling decision-record. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: ops overhead present, 4 scenarios, sensitivity table, vendor-risk %, monthly + NPV, break-even computed | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for `economic-model.json` + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: hidden ops, single scenario, ignored risk premium, units mismatch | ~600 |
| `content/04-procedure.xml` | recommended | 7 steps: gather → unit-normalise → 4 scenarios → sensitivity → NPV → write narrative → sign | ~700 |
| `content/05-examples.xml` | recommended | One worked model: support classifier 50k req/day | ~600 |
| `content/06-decision-tree.xml` | essential | Use-or-skip and scenario-fan-out branches | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Unit-normalise inputs | haiku | Tokens → $/month conversion. |
| Compute 4 scenarios | sonnet | Arithmetic + scenario logic. |
| Write narrative | opus | Synthesis for human reader. |

## Templates

| File | Purpose |
|------|---------|
| `templates/economic-model.py` | Stdlib kernel: inputs JSON -> four scenarios, sensitivity table, monthly delta + 12-month NPV + break-even, recommendation; prints the economic-model.json artefact. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[fine-tune-vs-prompt-decision-tree]]` — consumes these numbers
- `[[finetune-cost-vs-prompt-decision]]` — sibling decision-record

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters preconditions, then iterates the 4 scenarios; if break-even &gt; 12 months in 3+ scenarios the recommendation surfaces as "do not FT".
