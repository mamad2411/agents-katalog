---
name: booboo-troubleshoot
description: Diagnose a Booboo brain that is not working — an empty or tiny graph, a flat starburst view, missing MCP tools, a client that cannot find the snapshot, climbing orphan counts, or a build that exits clean but produces nothing. Use when a booboo build, serve, mcp, view, panel or vault command misbehaves.
---

# Troubleshooting

Read `RULES.md` first — rule 4 is the method: verify against the running thing,
because most of these failures exit 0.

Full reference: `docs/TROUBLESHOOTING.md` in the repo. This skill is the ordered
diagnostic path.

## Start by finding out what is actually true

Before theorising, get three facts:

```bash
booboo build --config booboo.config.yaml   # read the quality line AND the node count
curl localhost:8787/stats                  # what the server thinks it has
```

Plus: does `org.booboo.json` say `"seed": true`? That single flag explains a
surprising share of "my agents behave strangely" reports — the fleet is booting
from the scaffold's sample pair.

## The build exits 0 but the graph is empty or tiny

The most common failure, because nothing errors.

- **A `where` clause matching nothing.** Run the same predicate as `SELECT count(*)`
  against the source. A filter that excludes everything is silent.
- **A wrong table or column name** in a `nodes:` entry. The adapter reads what you
  named; if `label: name` points at a column that does not exist, you get nodes
  with no labels or no nodes at all depending on the source.
- **The wall is wider than you think.** A `walls:` entry matching a cluster name
  you also use for real data filters it out entirely — correctly, silently, in the
  builder.
- **`${VAR}` did not resolve.** An unresolved connection string usually fails
  loudly, but an unresolved *path* can silently read nothing.

Compare the built node count to a `count(*)` on the source. That one comparison
finds most of these.

## The 3D view is a flat starburst

Everything is parented to the root, so there is no spine. Set `parent:` on your
node entries deliberately — see `booboo-adapter`. This renders perfectly and tells
you nothing, so it is easy to miss unless you look at the picture.

## Spines converge somewhere that is not the root

A parent-mapping bug: some node is acting as a hub because a `parent:` column
contains a constant, a null coerced to a shared value, or a foreign key pointing
at the wrong table. Search for the hub node and read its neighbors.

## MCP tools are missing

- **`booboo_boot` and `booboo_org` absent** → the server was started without
  `--org`. They are the two org-dependent tools.
- **`booboo_remember` and `booboo_report` refuse** → the server is read-only, via
  `--no-write` or `BOOBOO_READONLY=1`. It still reads the journal. Do not work
  around it on a brain you do not own.
- **No tools at all** → the client is not launching the server. Check the client's
  MCP log, not Booboo's.

## The client cannot find the snapshot

Almost always a relative path. The MCP client's working directory is usually not
your project directory, so `--snapshot my.booboo.json` resolves somewhere
unexpected.

**Use absolute paths** for `--snapshot` and `--org` in any client config. If it
works in your shell and fails in Claude Desktop or Cursor, this is the reason.

## Orphans or dump-suspects climbing

Not a cosmetic metric. See `booboo-vault` for what each number means.

- **Orphans climbing** → links are not resolving. Nearly always an id mismatch
  between the node emitter and the link emitter — the `links:` entry's `source`
  and `target` must contain the same id values the `nodes:` entries produced.
  Unstable ids that change between builds cause this too.
- **Dump-suspects climbing** → notes are being written as transcripts rather than
  atomic facts. Fix the writing habit, not the gate.

## A rebuild wiped my edit

Working as designed. `brain.json` and `vault/` are DERIVED — regenerate, never
hand-edit. Put the change in the source or the config. `org.booboo.json` is the
one file that is source rather than output.

## An agent hangs on boot with no error

Suspect a cycle in the org. The panel validates before every write specifically so
this cannot land, which means a cycle usually arrives via a hand-edit or a script.
Reshape through `booboo panel` and let the validator catch it.

## The viewer struggles

Drop `--nodes` on demo runs; on a real snapshot, check the count in `/stats`
first. A million nodes at 60fps is the proven ceiling on capable hardware — see
`SCALE.md` — but a modest laptop wants 50k. If the count is far higher than the
source justifies, you have duplicate nodes from unstable ids, which is a build bug
rather than a rendering one.

## Escalate honestly

If you cannot reproduce or explain it, say so plainly and report what you did
observe — the quality line, the node counts, the exact command, the real error
text. `docs/TROUBLESHOOTING.md` for the long form, and issues on the repo for
genuine defects. A guessed root cause filed as fact is worse than an open question.
