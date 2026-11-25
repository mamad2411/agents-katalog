---
name: booboo-adapter
description: Feed data into a Booboo brain that the built-in postgres and json adapters do not cover — write a small config-driven adapter against the spec instead of forking the builder. Use when a source is Neo4j, an API, a CSV export, a proprietary store, or any shape the standard config cannot express.
---

# Adapters — a small file, never a fork

Read `RULES.md` first. Rule 3 is the whole skill in one line: **ship the shortest
adapter, never a fork.**

## Why this stays cheap

Booboo is a small JSON spec at the centre with adapters feeding it and consumers
rendering it. Emit conformant JSON and you inherit the 3D viewer, the REST API,
the MCP server, the panel and the vault for free — none of them know or care where
the nodes came from.

That is deliberate. The spec is roughly a kilobyte of contract precisely so that
supporting a weird source costs a small file rather than a maintained fork. Read
`SPEC.md` before writing anything; if the job appears to need a fork, you have
almost certainly misread it.

## Try the escape hatch first

The `json` adapter is passthrough and it is the universal answer:

```yaml
sources:
  - adapter: json
    path: ./data/extra.booboo.json
```

For a one-off import, an export script that writes conformant JSON plus this
adapter beats a custom adapter, because there is nothing left to maintain. Reach
for a real adapter when the source needs to be re-read on **every** build.

## What an adapter owes the spec

Whatever the source, the output is nodes and links:

- **nodes** — a stable `id`, a human `label`, a `layer`, optionally `parent`
  (the spine), `cluster`, `weight`, `icon`, and a `data` payload
- **links** — `source`, `target`, `type`

Two things decide whether the graph is readable rather than a hairball:

**Stable ids.** An id that changes between builds turns one node into two and
silently orphans every authored `[[link]]` pointing at the old one. Derive ids
from something the source guarantees — a primary key, a slug — never from a
mutable label or an array index.

**Parent, deliberately.** `parent` builds the spine that makes the 3D view legible
and the hierarchy meaningful. Everything defaulting to the root produces a flat
starburst that renders fine and tells you nothing. If the source has no natural
parent, group in the adapter and say so in a comment.

## Weight and cluster

`weight` drives visual prominence. Set it from something real — `weight_from: degree`
against a numeric column beats a constant. A graph where everything weighs the
same is a graph with no signal.

`cluster` groups nodes within a layer and, importantly, is what `walls:` filters
on. Cluster with the walls in mind.

## Walls are enforced in the builder, not in your adapter

Your adapter may read walled data; the builder filters it before the snapshot
exists. Do not implement your own wall logic — that duplicates a guarantee and
duplicated guarantees drift.

What you **must not** do is add a second source that reads the same table under a
different cluster name to route around a wall. That is rule 2, and it is a leak
with a commit attached.

## Verify a new adapter

1. Build and read the quality line: `quality · authored:N · orphans:N ·
   dump-suspects:N`. A flood of new orphans means your links are not resolving —
   usually an id mismatch between the node emitter and the link emitter.
2. Check the node count against the source. `SELECT count(*)` and compare. A `where`
   clause that silently matches nothing exits 0 and emits an empty layer.
3. Open `booboo view`. Spines converging on a single point that is not the root, or
   a flat starburst, are parent-mapping bugs no status code reveals.
4. Search the served graph for a term you know exists only behind a wall. It must
   return nothing.

## Contributing it back

If the source is one other people have, the adapter belongs upstream rather than in
a private fork — see `CONTRIBUTING.md` and `docs/SUBMISSIONS.md`. A config-driven
adapter that fits the spec is a small, reviewable PR. That is the design working.
