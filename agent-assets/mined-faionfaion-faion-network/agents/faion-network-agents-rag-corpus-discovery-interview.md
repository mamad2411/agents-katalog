# RAG Corpus Discovery Interview

## Summary

**One-sentence:** Structured SME interview that audits the corpus (sources, freshness, sensitivity, licensing) before any embedding choice — five-interview minimum before synthesis.

**One-paragraph:** Current rag-architecture methodology jumps to chunking + embedding without auditing the corpus. Wrong corpus → wrong embeddings → wrong retriever. This methodology produces a `corpus-discovery-report.json` based on ≥5 SME interviews (past-behaviour anchored, non-leading prompts) with full transcripts and tagged-quote evidence. Output: a versioned interview bundle the RAG engineer consumes before picking chunking strategy.

**Ефективно для:**

- Embed RAG в existing product — audit corpus state перед wiring.
- 5+ SME interviews для розуміння corpus realities.
- Non-leading prompts; past-behaviour anchored questions.
- Transcripts + tagged-quote evidence для synthesis.
- Bridge до downstream [[rag-bench-harness-template]] спеку.

## Applies If (ALL must hold)

- RAG project planning kickoff — pre-architecture phase.
- ≥5 SMEs available within the review window.
- Recording + transcript pipeline available.
- Named accountable owner.

## Skip If (ANY kills it)

- Corpus already documented in a recent (≤6mo) audit.
- &lt;5 SMEs available (would-be synthesis premature).
- One-shot prototype with no production stakes.
- No recording / transcript capability (notes-only is rejected).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| SME roster (≥5 names + roles) | YAML | platform |
| Interview guide template | Markdown | research repo |
| Recording + transcript tools | tool config | research repo |
| Consent forms | PDF | legal |
| Named accountable owner | string | ownership log |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `[[rag-bench-harness-template]]` | Downstream consumer of corpus audit findings. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules + run/skip terminals | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for corpus-discovery-report + examples | ~700 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns | ~900 |
| `content/04-procedure.xml` | essential | 5-step: roster → schedule → interview → transcribe → synthesise | ~700 |
| `content/05-examples.xml` | essential | Worked example: 7-SME KB audit | ~700 |
| `content/06-decision-tree.xml` | essential | Routes interview count + consent state to synthesis | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-guide` | sonnet | Anti-leading-question rewriting. |
| `tag-quotes` | sonnet | Per-quote evidence tagging. |
| `synthesise-findings` | opus | Cross-interview pattern detection. |

## Templates

| File | Purpose |
|------|---------|
| `templates/corpus-discovery-report.json` | JSON skeleton matching 02-output-contract. |
| `templates/corpus-discovery-report.md.j2` | Narrative interview-bundle template. |
| `templates/corpus-discovery-report.md` | Narrative interview-bundle template. Generated from `templates/corpus-discovery-report.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rag-corpus-discovery-interview.py` | Validate corpus-discovery-report | Pre-commit + before rag-bench spec |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[rag-bench-harness-template]]
- [[production-trace-mining-for-training-data]]
- [[pii-scrubbing-recipe-for-eval-sets]]

## Decision tree

See `content/06-decision-tree.xml`. The tree blocks synthesis if interview count &lt;5 or consent missing; routes to rag-bench spec on green. Walk it before claiming "we know the corpus".
