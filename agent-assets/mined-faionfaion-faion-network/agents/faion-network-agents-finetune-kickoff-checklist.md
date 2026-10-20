# Fine-tune Kickoff Checklist

## Summary

**One-sentence:** Produces a kickoff-gate checklist (eval baseline, data quality bar, hold-out slice, eval-during-training cadence, rollback plan) that fine-tune jobs MUST pass before training spend is approved.

**One-paragraph:** Every fine-tune-openai-* methodology covers HOW to train. None covers the kickoff gate: did we even confirm fine-tuning is the right tool, do we have eval + hold-out, does the data pass quality checks, is rollback wired in. This methodology produces the 12-item gate the team signs before sending the first training file. Single artefact: `kickoff-checklist.json` with all items marked yes/no/n-a + owner.

**Ефективно для:** ml-engineer pre-training gate, founder/CTO sign-off on training spend, FinOps challenges, the team running fine-tune for the third time and tired of avoidable failures.

## Applies If (ALL must hold)

- Team has decided to fine-tune (e.g. via `[[finetune-cost-vs-prompt-decision]]`).
- Training dataset candidate exists (≥1k examples).
- Eval set exists for the workload.
- A named owner (ml engineer) will run the job.

## Skip If (ANY kills it)

- Still in fine-tune vs prompt debate — run `[[finetune-cost-vs-prompt-decision]]` first.
- LoRA/QLoRA experiment with ≤ $10 budget — overhead > savings.
- Provider-hosted automated tuning where ALL checks are vendor-default — verify vendor defaults instead.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Decision record (FT recommended) | JSON | `[[finetune-cost-vs-prompt-decision]]` output |
| Training dataset | JSONL with `messages` per row | data lake |
| Eval set + baseline score | JSONL + float | eval harness |
| Rollback plan | text | runbook |
| Provider account + budget cap | account id + $ | finops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[finetune-cost-vs-prompt-decision]]` | Upstream — gates whether to even run this. |
| `[[eval-set-stratified-sampling-recipe]]` | Hold-out design. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: decision record present, baseline score, hold-out 10%, dedup, PII scrub, train-loss watch, rollback wired | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the checklist + valid/invalid examples | ~600 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: no hold-out, leaky dedup, no rollback, eval-during-training missing | ~600 |
| `content/06-decision-tree.xml` | essential | Gate-pass tree | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Fill items from artefacts | haiku | Mechanical extraction. |
| Check hold-out is disjoint from train | sonnet | Bounded set ops. |
| Approve / reject narrative | opus | High-stakes summary. |

## Templates

| File | Purpose |
|------|---------|
| `templates/kickoff-checklist.schema.json` | JSON Schema for the artefact. |
| `templates/kickoff-checklist.example.json` | Worked filled example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-finetune-kickoff-checklist.py` | Validate the checklist JSON against schema + rules. | Before training submission. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/`
- `[[finetune-cost-vs-prompt-decision]]` — upstream gate
- `[[eval-set-stratified-sampling-recipe]]` — hold-out design

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: decision record present, ≥1k examples, eval baseline known, owner named → run; else skip and resolve upstream gaps.
