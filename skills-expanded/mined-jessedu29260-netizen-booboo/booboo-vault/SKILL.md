---
name: booboo-vault
description: Emit a Booboo brain as a wiki-linked markdown vault for Obsidian, author authored edges with double-bracket links, and read the ingestion quality gate. Use when someone wants their system as plain files, an Obsidian second brain generated from real data, a portable insurance copy, or wants to know why their orphan count is climbing.
---

# The vault — the brain as plain markdown

Read `RULES.md` first. Rule 1 (derived files are never hand-edited) and rule 5
(one atomic fact, author your links) both apply directly.

```bash
booboo vault --snapshot my.booboo.json --org org.booboo.json --out vault
```

Emits one page per node with frontmatter and its links, index pages per layer and
per cluster, and an agent dossier per org member — chain of command, inherited
rules, buckets, machines, contract. Open the folder in Obsidian and the graph view
works, because the wikilinks are real.

## Why bother when the 3D view exists

Three reasons, in order of how often they matter:

1. **Portability.** Plain files outlive every tool in the chain. Any human can
   read them, any agent from any provider can too — no MCP client, no server, no
   Node.
2. **Insurance.** Emit it nightly and the vault is a complete, readable copy of
   the brain that survives the database going away.
3. **The second-brain pattern, without hand-feeding.** The usual Obsidian
   knowledge vault is manually curated notes. This one is generated from the real
   system, so it cannot drift from what is actually deployed.

## The vault is DERIVED

Regenerate it; never hand-edit it. Edits to `vault/` are erased by the next
`booboo vault` run without warning.

If you want text in the vault, put it in the **source** — the note, the row, the
table the adapter reads. That is the only edit that survives, and it is the edit
that also reaches the API, the MCP server and the 3D view.

## Authoring links — the part that actually improves the brain

Put refs inside a note's text:

```
The dispatcher writes to [[content-ledger-live]] after [[zernio-api]] confirms.
```

With `wikilinks: true` in the config, the builder turns those into first-class
`authored` edges that **outrank harvested relations** everywhere — the graph, the
API, the 3D view and the vault.

Both forms work: `[[node-id]]` and `[[exact label]]`. Prefer the id when you know
it — labels change, ids should not.

The discipline: **only link what you know.** An authored edge is a claim that
outranks whatever the harvester inferred, so a guessed link actively displaces a
correct one. Unsure means leave it to the harvester.

## The quality gate — a number, not a vibe

Every build prints:

```
quality · authored:N · orphans:N · dump-suspects:N
```

Read it every time.

- **authored** should grow. It is the count of edges a human or agent asserted
  deliberately, and it is the measure of curation.
- **orphans** should not grow. An orphan is a node nothing links to — usually an
  id mismatch, sometimes a genuinely stranded record. A climbing count means new
  data is arriving unconnected.
- **dump-suspects** should not grow. These are notes that look like transcripts or
  pastes rather than atomic facts. They are the leading indicator of a brain that
  is accumulating rather than being curated.

Rising orphans or dumps are a **defect to fix before adding more data**, not a
statistic to note and move past. Curation debt compounds: every dump makes the
next search worse, which makes the next agent trust the brain less, which is how
these systems quietly die.

## Nightly emission

Wire `booboo vault` next to `booboo build` in whatever runs the refresh. The vault
costs one pass over an existing snapshot, so the marginal cost of always having a
current portable copy is close to nothing.

Commit it or do not, deliberately: committing gives you a readable diff of how the
system changed, at the cost of noise in the history. For a brain with walls, check
what the vault contains before committing it anywhere shared — the walls are
enforced in the builder, so a correctly configured vault is already clean, but
verify rather than assume.
