---
description: Regenerate wiki/index.md, per-type shards, and tag shards from the filesystem.
when_to_use: Run when the index looks stale or after manual file moves/renames. Lighter than lint — only recomputes source_count / inbound_refs / inbound_refs_primary and rebuilds the shard tree. Never modifies page bodies. Also triggered by phrases like "rebuild the index", "recompile the wiki catalog".
allowed-tools: Read, Write, Bash, Glob
---

# Wiki Compile

Read `CLAUDE.md` for conventions. Follow the COMPILE operation exactly as specified there.

## Steps

1. Rebuild the sidecar cache (and embeddings, if semantic is on):

   ```bash
   python3 scripts/build_meta.py --embed-if-enabled
   ```

   This writes `wiki/.meta/backlinks.json`, `wiki/.meta/sources.json`,
   `wiki/.meta/search-index.tsv` from the filesystem, and refreshes
   embeddings for pages whose text changed when
   `/wiki-enable-semantic` has been run (silent no-op otherwise).
   Fast — O(N) in
   page count, runs in under a second on a 5K-page vault.

2. Rebuild the shard tree:

   ```bash
   python3 scripts/shard_index.py
   ```

   Writes `wiki/index.md` (thin, ~1K tokens), per-type
   `wiki/<type>/_index.md` (auto-sharded if >10K tokens), and
   `wiki/indexes/by-tag/*.md` for every tag with ≥3 members.

3. Reconcile frontmatter `source_count` / `inbound_refs` /
   `inbound_refs_primary` with the fresh sidecar. For every
   concept/entity page whose frontmatter disagrees with
   `wiki/.meta/backlinks.json`, rewrite those frontmatter fields in
   place. This is the **only** body-adjacent change COMPILE is allowed
   to make.

4. Append one `compile` entry to `wiki/log.md` with per-type counts
   and the number of frontmatter reconciliations.

Do not touch any page body.

## Reporting

- Counts per type
- Frontmatter drifts fixed (with list of affected slugs)
- Shard files written (total count and whether any per-type index
  crossed into alphabetical shards)
- Tag shards emitted
- Files that lacked a usable `title` or `summary` (these are lint
  targets — COMPILE does not fix them)
