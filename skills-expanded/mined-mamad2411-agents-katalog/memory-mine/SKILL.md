---
name: memory-mine
description: Offline memory analysis — gaps, clusters, staleness, dedup over the drawer corpus. Use to mine memory between sessions, or /memory-mine. Not for live search (memory-search) or automatic decay.
---

# Memory-Mine

You are the **between-sessions intelligence pass** over the memory corpus. Decay runs automatically and
emits the staleness/gap maps; you do the deliberate, deeper analysis: where are the **knowledge gaps**
(topics with thin or no coverage), which drawers **cluster** (and should be generalized into a pattern),
what is going **stale**, and where are the **duplicates**. You produce a map of the corpus's health and
gaps so the next planning phase queries from strength. You analyze; you do not delete (that is `forget`,
provenance-gated) or research the gaps (that is `research`).

## What this does / does not do

Does: scan the drawer corpus and produce a gap map (under-covered topics), clusters (candidates for
pattern-tier generalization), a staleness summary, and duplicate candidates — with a receipt. Does
**not**: delete drawers (`forget`), research to fill gaps (`research`), or run automatically (decay does
the per-session staleness pass; memory-mine is the deliberate deeper analysis).

## When NOT to use

- You need a single fact now — that is `memory-search`, not a corpus-wide analysis.
- The corpus is tiny (a handful of drawers) — there is nothing to mine; coverage is trivially the whole set.

## Reference Routing

| Situation | Reference |
|---|---|
| The corpus + search | `library/systems/memory/memory-search.py` · `providers/` |
| Automatic decay (staleness/gap maps it already emits) | `library/systems/memory/decay.py` |
| Knowledge tiers (learning vs pattern — what a cluster generalizes into) | `engine/shared/references/knowledge-tiers.md` |

## Inputs

| Field | Required | Description |
|---|---|---|
| `scope` | no | a category/topic to focus the mine (else the whole corpus) |
| `min_cluster` | no | minimum drawers to call a cluster (default 3) |

## How to do it

### Step 1 — Inventory
Load the corpus (the drawers under `<workspace>/memory/`). Group by category; note counts, confidence,
and staleness distribution.

### Step 2 — Gap detection
Find under-covered areas: categories/topics the project touches (per receipts/project-map) but has thin
or no drawers for. A gap is a finding — it tells the next research/explore pass where to look.

### Step 3 — Clustering → pattern candidates
Find drawers that cluster on a topic. A cluster of `learning`-tier drawers is a candidate to **generalize**
into a `pattern`-tier drawer (`knowledge-tiers.md`) — surface the candidate; do not auto-promote (a
pattern is created by a deliberate generalization pass, never a single write-back).

### Step 4 — Staleness + dedup
Summarize what is going STALE/EXPIRED (decay already transitions; you report the trend) and flag duplicate
candidates (near-identical topic+evidence) for review by `forget` (which is provenance-gated).

### Step 5 — Emit the map + receipt
Write the corpus health/gap map to `<workspace>/memory/`; then the receipt.

## Output Contract

**memory-mine receipt** (`<workspace>/receipts/memory-mine-receipt-<timestamp>.json`): base +
`drawer_count`, `gaps` (array of under-covered topics), `clusters` (array — pattern candidates),
`staleness_summary` (`{fresh, aging, stale, expired}`), `dedup_candidates` (array), `map_path`,
`confidence`. persistence: Spec-Anchored.

## Proactive Triggers

- **A cluster of learning drawers on one topic**: surface it as a pattern-generalization candidate — do
  not auto-promote (only a deliberate pass creates a pattern).
- **A topic the project touches but has no drawers for**: record it as a gap — it directs the next research.
- **Duplicate-looking drawers**: flag for `forget` (provenance-gated); memory-mine never deletes.
- **The corpus is mostly STALE/EXPIRED**: the working set has rotted — flag it; the knowledge needs re-grounding.

## Completion Criteria

**Done when:** a corpus health/gap map exists (gaps, clusters, staleness, dedup candidates) and a receipt
records the counts — the next planning phase can query from a known map.

**Not done if:** a pattern was auto-promoted from a cluster; memory-mine deleted a drawer; gaps were
omitted when the corpus clearly under-covered the project's scope.

**Next step:** `research`/`explore` to fill the gaps; `forget` (provenance-gated) for confirmed
duplicates; a deliberate generalization pass to promote a cluster to a pattern drawer.

## Related Skills

- **memory-search**: A single query now. memory-mine is the corpus-wide offline analysis.
- **forget**: Provenance-gated deletion. memory-mine flags duplicates; forget removes them with a record.
- **graph-query**: Answers a specific architectural question. memory-mine maps what the corpus is missing.
