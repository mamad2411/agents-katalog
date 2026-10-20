# Production Trace Mining for Training Data

## Summary

**One-sentence:** Pinned method to mine PII-scrubbed production traces into a fine-tune candidate dataset — labels inferred, capability stratified, owner and review cadence locked in.

**One-paragraph:** Production traffic is the richest source of training data for any deployed LLM-agent, but most teams either ignore it (and stay stuck on prompt engineering) or dump it raw into a fine-tune (and leak PII, overfit on noise). This methodology turns the recurring "fine-tune vs prompt-engineer" decision into a reviewable spec: which traces qualify, how labels are inferred, how capabilities are stratified, who owns the dataset, when it expires. Output is a `trace-mining-spec.json` artefact downstream fine-tune jobs consume without re-deriving rationale.

**Ефективно для:**

- "Fine-tune vs prompt-engineer" decision (4-week worst-case cadence).
- Перетворити stale prompt-eng practice на data-driven cycle.
- PII-scrub + label inference + capability strat в одному spec'у.
- Versioned dataset з owner + retention + outcome review.
- Команда вже має eval harness, але fine-tune ще ні.

## Applies If (ALL must hold)

- Recurring "fine-tune vs prompt-engineer" decision on the operating cadence.
- Production traces are PII-scrubbed (see `pii-scrubbing-recipe-for-eval-sets`).
- Named accountable owner exists.
- Repository / wiki space hosts the versioned spec.

## Skip If (ANY kills it)

- Greenfield prototype без production users.
- Fewer than 3 instances per year — review cadence costs more than it returns.
- Regulator mandates a different template — defer to legal.
- No PII-scrub recipe locked — block on `pii-scrubbing-recipe-for-eval-sets` first.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| PII-scrubbed traces (≥1000 rows) | JSONL | warehouse |
| Capability taxonomy | YAML | platform |
| Label inference rules (heuristic + LLM judge) | YAML | ML repo |
| Named accountable owner | string | ownership log |
| Retention window (days) | int | legal repo |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[pii-scrubbing-recipe-for-eval-sets]]` | PII scrub precondition. |
| `solo/sdd/sdd/sdd-document-templates` | Document-as-code conventions. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: scrub → stratify → label → audit → commit | ~800 |
| `content/05-examples.xml` | essential | Worked example: 5000-trace sample → spec | ~700 |
| `content/06-decision-tree.xml` | essential | Routes traffic volume + label confidence to mining strategy | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-spec` | haiku | Template fill. |
| `infer-labels` | sonnet | Per-row judgment with heuristic + LLM-judge. |
| `outcome-review` | opus | Cross-cycle synthesis. |

## Templates

| File | Purpose |
|------|---------|
| `templates/trace-mining-spec.json` | JSON skeleton matching 02-output-contract. |
| `templates/trace-mining-spec.md.j2` | Narrative skeleton for human review. |
| `templates/trace-mining-spec.md` | Narrative skeleton for human review. Generated from `templates/trace-mining-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-production-trace-mining-for-training-data.py` | Validate trace-mining-spec | Pre-commit + before fine-tune job |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[pii-scrubbing-recipe-for-eval-sets]]
- [[prompt-ab-power-calculator]]
- [[rag-corpus-discovery-interview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree decides between high-volume heuristic labeling and low-volume LLM-judge labeling, and routes out if PII-scrub is not yet locked. Walk it before drafting the spec; mining without a scrub recipe leaks PII into the training set.
