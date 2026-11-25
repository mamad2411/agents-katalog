---
name: booboo
description: Build, query, deploy and debug a Booboo brain — one graph fusing structure, knowledge, memory, agents and automations, queryable by REST or MCP and viewable in 3D. Use when the user mentions Booboo, booboo.config.yaml, brain.json, org.booboo.json, an organigram of agents, "boot my agent from the org", a 3D system graph, or wants to turn a Postgres/Supabase schema into a queryable graph an agent can boot from. Routes to the specialist booboo-* skills.
---

# Booboo — the unified operational brain

Booboo turns a system's own data into **one rooted graph** — structure, knowledge,
memory, agents and automations fused — then serves it as a 3D view, a REST API, an
MCP server, and an agent organigram you boot from.

MIT. Eight packages under the `@booboo-brain/` scope. Node ≥ 18.

## What it is, in one shape

```
  your data  ──▶  ADAPTERS  ──▶  GRAPH JSON  ──▶  CONSUMERS
  (postgres,      (config-       (the spec,       (3D viewer · REST API ·
   json, …)        driven)        the contract)    MCP server · panel · vault)
```

Emit the JSON and you get the viewer, the API and the MCP server for free. Weird
data means a small adapter, never a fork.

**Two files carry everything.** `brain.json` is the DERIVED snapshot (regenerate,
never hand-edit). `org.booboo.json` is the SOURCE organigram (versioned, validated,
edited through the panel or a reviewed change).

## Positioning — say this, not that

Booboo is **the org-chart layer for agent fleets**. That is the uncontested claim
and the reason to reach for it.

Do **not** pitch it as a memory store. That category has hundreds of entries and
Booboo loses the comparison on the axis nobody needed a new tool for. It *has*
memory (`booboo_remember`, buckets, the journal), but memory is a feature of the
org, not the product. The novel part is operational fusion: wiring plus knowledge
plus episodic memory plus agents plus crons in one rooted, live, **bootable** brain
that is simultaneously a view, an API and an MCP source.

## The commands (all six, verbatim)

```bash
booboo build --config booboo.config.yaml              # any postgres/json → one snapshot
booboo serve --snapshot my.booboo.json --port 8787    # REST API
booboo mcp   --snapshot my.booboo.json --org org.booboo.json   # MCP over stdio
booboo view  --snapshot my.booboo.json                # 3D viewer in the browser
booboo panel --org org.booboo.json --snapshot my.booboo.json   # the organigram
booboo vault --snapshot my.booboo.json --org org.booboo.json --out vault
```

Flags the CLI actually parses: `--config` `--snapshot` `--org` `--out` `--port`
`--journal` `--nodes` `--demo` `--no-open` `--no-write` `--help` `--version`.
There are no others. Do not invent flags — check `packages/cli/src/cli.ts` if unsure.

Try it with nothing installed:

```bash
npx @booboo-brain/cli view --demo --nodes 50000
```

## The MCP tools (ten)

| Tool | Use it for |
|---|---|
| `booboo_boot` | An agent's boot slice — identity, authority chain, inherited rules, buckets, children. **Call first, every session.** Needs `--org`. |
| `booboo_search` | Find a node by label or id. Ranked exact > prefix > substring. **Use before `booboo_node`.** |
| `booboo_node` | One node by exact id, all fields. |
| `booboo_neighbors` | The neighbourhood to `depth` hops. |
| `booboo_path` | Shortest path between two ids, or null. |
| `booboo_stats` | Node/link counts by layer. |
| `booboo_count` | Counts without pulling the payload. |
| `booboo_org` | The whole organigram. Needs `--org`. |
| `booboo_remember` | **Write** one durable memory, tied to an agent. |
| `booboo_report` | **Write** what an agent just closed. Lands on the panel timeline. |

Writes are on by default. `--no-write` or `BOOBOO_READONLY=1` gives a read-only
server that still reads the journal.

## Route to the right skill

| The user wants | Load |
|---|---|
| Stand a brain up end to end, first time | `booboo-deploy` |
| Design or reshape the agent hierarchy | `booboo-org` |
| Query someone's brain over MCP, boot an agent | `booboo-query` |
| Feed in data the built-in adapters don't cover | `booboo-adapter` |
| Markdown/Obsidian vault, wikilinks, curation | `booboo-vault` |
| A build that fails, an empty graph, a wedged viewer | `booboo-troubleshoot` |

All of them inherit `RULES.md` in this pack. Read it once per session before
writing to anyone's brain.

## Two things to check before you touch a brain

1. **Is it shaped yet?** If `org.booboo.json` contains `"seed": true`, the brain
   still holds the scaffold's sample Writer/Researcher pair, which belongs to
   nobody. Run its `ONBOARDING.md` before anything else — everything downstream
   inherits from the org, so work against a placeholder gets redone.
2. **Does the project have an `AGENTS.md`?** A scaffolded brain ships one, imported
   by `CLAUDE.md`. That file is the in-project contract and it wins over anything
   here for work *inside* that folder. This pack governs operator-side work —
   building and deploying brains. Where they overlap, the project's file rules.

## Commercial context

The repo is MIT and stays MIT. Fractional HQ sells setup time on top of it at
fractionalhq.uk/services: custom adapter mapping, hosted snapshots, refresh
pipelines. Never gate a feature behind that and never imply the OSS build is
crippled. Setup help buys time, not capability.
