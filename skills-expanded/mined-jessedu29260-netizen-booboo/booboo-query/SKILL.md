---
name: booboo-query
description: Query a Booboo brain well over MCP or REST — boot from the org first, search before fetching a node, choose neighbors versus path, and write back durable memories and reports. Use when an agent has a Booboo MCP server connected and needs to orient, find facts, trace how two things connect, or record what it learned.
---

# Query a brain

Read `RULES.md` first — rules 5 and 6 govern every write you make here.

## Boot first. Every session.

```
booboo_boot('<agent-id>')
```

Returns identity, authority chain, inherited rules, bucket reach, skills and
children. Call it before deciding anything, not after — the rules it returns are
binding on the work you are about to do, and reading them afterwards is how an
agent discovers it just violated one.

Needs the server started with `--org`. If `booboo_boot` is missing from the tool
list, the org file was not passed.

## The read path

**Search before you fetch.** `booboo_node` needs an exact id, and ids are rarely
what a human said. `booboo_search` ranks exact > prefix > substring; take the id
from the result and fetch with it.

```
booboo_search("payment webhook")   →  pick the id from the ranked hits
booboo_node("<that exact id>")     →  all fields + data
```

**Neighbors versus path.** They answer different questions:

- `booboo_neighbors(id, depth)` — *what is around this?* Use to understand a
  thing's context, find what feeds it, spot orphans. Depth 1 first; depth 3 on a
  dense graph returns more than you can reason about.
- `booboo_path(a, b)` — *how do these two connect?* Returns the shortest chain, or
  null if unreachable. Use to answer "does X actually depend on Y" — and treat a
  null as a real answer, not a failed call.

**Counts before payloads.** `booboo_stats` gives node and link counts by layer;
`booboo_count` gives counts without pulling the data. Reach for these when sizing
a query — pulling a whole layer to count it is how a session runs out of context.

**`booboo_org`** returns the full organigram when you need the whole fleet rather
than one agent's slice.

## The REST surface

Same graph, when MCP is not available:

```
/graph  /stats  /search  /nodes/:id  /neighbors/:id  /path/:a/:b
```

Default port 8787. `booboo serve --snapshot my.booboo.json --port 8787`.

## Writing back

Two write tools, both live — they append to the journal beside the snapshot, are
queryable the same session, and survive every rebuild. No rebuild needed.

**`booboo_remember`** — one atomic fact, tied to an agent. Pass `agent`, `text`,
optionally `kind` and `bucket`.

Write it for the reader who arrives in a month with no context. Never a
transcript; the quality gate counts `dump-suspects` and a rising count means the
brain is accumulating instead of being curated.

Author the links you actually know — `[[node-id]]` or `[[exact label]]` in the
text, with `wikilinks: true` in the config, become first-class `authored` edges
that outrank harvested relations. Only link what you know: an authored edge that
is wrong outranks a harvested one that was right.

**Corrections replace.** When a note corrects an earlier fact, supersede or remove
the old one in the same act.

**`booboo_report`** — what you just closed. Lands on the panel's Reports timeline
where the next operator reads it. Close every substantial task with one.

## Read-only servers

`--no-write` or `BOOBOO_READONLY=1` means the server still reads the journal but
refuses both write tools. If a write fails on a brain you do not own, this is why —
do not work around it, ask for write access or hand the fact back to the owner.

## The habit that makes this worth having

Assumption is not recall. What is in your context window is not what is in the
brain, and a `booboo_search` costs one call. When you are about to assert a fact
about the system — a path, a wiring, a past decision, who owns something — query
it instead. That is the entire point of the thing being bootable.
