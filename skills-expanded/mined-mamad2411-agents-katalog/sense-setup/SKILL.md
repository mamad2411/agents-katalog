---
name: sense-setup
description: Set up the sense CLI on a markdown tree and make the tree-design decisions that shape it — sense init, enabling features (links, sections, rank, embed), and the trade-offs of frontmatter conventions, summaries, folder layout, and note size. Use when creating or restructuring a markdown knowledge base, running sense init, editing sense.config.json, enabling semantic search, or deciding how notes should be written for an agent to query later.
---

# sense: setup and tree design

Querying an existing tree is the `sense` skill. This one covers making a tree:
installing, configuring features, and the design decisions a tree owner faces.

## Setup

- `npm install -g sensemaking`, then `sense init` at the tree root writes
  `sense.config.json` (all opt-out features on, `embed` off). Config discovery
  walks up from cwd; `--config <path>` overrides.
- `scan.include` globs resolve relative to the config file, never the cwd.
- `sense map` and `sense status` report feature state
  (`features: links, sections, rank · off: embed (features.embed)`), so the
  current config is always discoverable from output.

## Features

| feature | powers | cost when on | config key |
|---|---|---|---|
| `links` | backlinks, dead-link queries, `find`'s link expansion, `peek`'s link lists | link re-resolution at reconcile | `features.links` (default on) |
| `sections` | `peek`'s outline, line-range reads, per-section token estimates | heading extraction at parse | `features.sections` (default on) |
| `rank` | `map`'s hubs, `_rank` in any ORDER BY | PageRank pass at reconcile; requires `links` | `features.rank` (default on) |
| `embed` | `find --semantic` (meaning-based expansion) | vectors computed at reconcile; model download to `~/.cache/sensemaking` on first use; ~40 ms model load per semantic invocation | `features.embed` (default off) |

- `embed` accepts `true` (built-in static model) or an object: `model` (Hugging
  Face id or local path), `type` (`static` pure-JS built-in, or `api` for any
  OpenAI-compatible `/v1/embeddings` endpoint — Ollama, LM Studio, llama.cpp,
  hosted), `url`, `key` (env var name). A local `model` path is fully offline.
- Enabling `embed` changes no default `find` result — expansion runs only when
  a query passes `--semantic`. Invoking `--semantic` on a tree without `embed`
  is an error naming the config key.
- Toggling any feature rebuilds the cache on the next query (safe, automatic).
- Disabled features degrade output, visibly: `peek` prints
  `sections: off (features.sections)` rather than an empty outline.

## Tree design decisions

These belong to the tree's owner. sense works with any of them and reads no
instruction files of its own; each choice below only changes what queries can
do, and every consequence is listed so the choice can be made deliberately.

- **Frontmatter fields.** Columns are discovered per tree — whatever keys notes
  declare become queryable. Consistent fields across notes make SQL filters
  and named queries possible (`WHERE status = 'active'`); inconsistent fields
  still work but produce sparse columns that filter less of the tree. Reserved
  keys (dropped with a warning): `path`, `_mtime`, `_size`, `_rank`, `content`,
  `links`, `sections`.
- **Dates.** `datetime()` comparisons work for dates written as ISO 8601 —
  the only format it parses. A tree that mixes date formats can store them,
  but can't compare them in SQL.
- **Summaries.** A one-line `summary:` is optional and pays twice: it shows in
  every result row (often answering a question with no file read) and is a
  weighted search field ranked above body text. The cost is writing and
  maintaining the line as notes change.
- **Folder shape.** sense is structure-indifferent: globs find the files,
  paths are queryable text, links resolve by basename at any depth. Folders
  are for the humans and agents navigating the tree, not for the index —
  flat and nested trees query identically.
- **Note size.** Many small notes: precise `find` hits, whole-file reads stay
  cheap, more links to maintain. Fewer large notes: `sections` and `peek`
  carry the cost down to line-range reads. Both work; per-section token
  estimates exist either way.
- **Where decisions live.** Choices that should outlive one conversation can
  be recorded in the agent's own instruction or skill files, or in a note in
  the tree itself; a one-off search over an existing corpus needs none of
  that. Whether to settle a choice with the user or proceed on the corpus as
  found depends on whether the agent is only querying or also authoring —
  an authoring agent's choices compound; a querying agent's don't.
