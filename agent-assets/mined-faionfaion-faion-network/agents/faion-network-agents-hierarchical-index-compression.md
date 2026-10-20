# Hierarchical Index Compression

## Summary

**One-sentence:** Produces an Index Budget Record that bounds what a tiered retrieval index costs to walk — a read ceiling per level, a fan-out that reaches the corpus, entries that discriminate rather than describe, and a numeric shard trigger.

**One-paragraph:** When the graph gate says "no graph, use a hierarchy with compact indexes", this is that hierarchy. The failure it prevents is specific and quiet: index tiers grow with the corpus, each entry acquires a prose summary that restates the leaf it points at, and a lookup ends up paying more for the map than for the destination. Nothing breaks — the answers stay correct — so it is discovered as unexplained context pressure years later. The fix is arithmetic, not machinery. Declare the maximum tokens any single index read may cost; declare the fan-out and depth and check they reach the corpus; cap entries to a discriminator that answers "when would I open this" and nothing else; shard on a number rather than on judgement. Where a corpus already nests, all of that is free restructuring. Where it does not, a recursive summary tree must be built and its build cost budgeted like any other index.

**Ефективно для:**

- A retrieval tree whose index reads now cost more than the bodies they deliver.
- A corpus that already nests — by domain, module, product area — where the hierarchy is free and only the entries need compressing.
- The `warrant: none` exit of a graph decision, which prescribes this structure and stops.
- Deciding between sharding what exists and building a RAPTOR-style summary tree over what does not.

## Applies If (ALL must hold)

- Retrieval routes through one or more index or table-of-contents tiers before reaching content.
- A cost ledger exists showing index reads are a material share of the lookup — this methodology is a remedy, and applying it without the measurement optimises the wrong tier.
- The corpus is too large to enumerate into the context window, and growing.

## Skip If (ANY kills it)

- Index reads are under 20% of lookup cost. The bill is candidates or bodies; compressing the index moves nothing.
- Retrieval is flat vector search with no index the model ever reads — there is no tier to compress.
- The corpus is static, small and fully enumerable in one read that fits the budget; one flat list beats any hierarchy at that size.

## Content

| File | What's inside |
|------|---------------|
| `content/01-core-rules.xml` | Six testable rules. R2 is the one that recovers the most tokens for the least work. |
| `content/02-output-contract.xml` | The Index Budget Record: levels, ceilings, fan-out arithmetic, shard trigger, and what the leaf owns. |
| `content/03-failure-modes.xml` | Six ways a tiered index quietly becomes the bill. |
| `content/06-decision-tree.xml` | Routing from measured index share and corpus shape to shard / build / leave alone. |
| `scripts/validate-hierarchical-index-compression.py` | Validates a record: ceilings, reachability, entry caps, build-cost amortisation. `--self-test` included. |

## Templates

| File | Purpose |
|------|---------|
| `templates/index-budget-record.yaml` | Fill-in record; ships valid against the contract. |
| `templates/index-entry-format.md.j2` | The entry shape, with a before/after showing what a discriminator removes. |
| `templates/index-entry-format.md` | The entry shape, with a before/after showing what a discriminator removes. Generated from `templates/index-entry-format.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- `retrieval-cost-per-answer-audit` — the required upstream. It measures the index share; this methodology acts on it. Re-run it afterwards to confirm the cut.
- `context-graph-engineering` — its `warrant: none` exit routes here. This is the structure it declines to replace with a graph.
- `chunking-document-structure` — how a leaf is split. Orthogonal: that governs the body, this governs the map to it.
- `llamaindex-indexes-queries` — one framework's implementation of tiered indexes; the budget arithmetic here is framework-independent and applies to it too.
