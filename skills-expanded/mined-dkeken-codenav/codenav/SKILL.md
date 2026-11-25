---
name: codenav
description: >
  Unified code-navigation doctrine combining four persistent tools on four distinct axes —
  qdrant (memory/time), graphify (topology/macro), beacon (semantic retrieval), serena
  (precision/micro). Use at the start of ANY non-trivial code task in a repo wired with
  these MCPs: orient before editing, locate symbols by meaning, recall prior decisions, and
  feed findings back so each tool sharpens the others. Trigger phrases — "where is X",
  "how does Y work", "who calls Z", "trace the flow", "orient me", "find the code that...",
  "понять проект", "разберись в коде", "где это".
---

# codenav — the four-axis code navigation combine

Four tools. Four DIFFERENT questions. They are not redundant — each owns an axis the
others cannot see. Used together in order, they turn "I don't know this codebase" into a
precise edit with minimal token burn.

## The four axes (memorize this table)

| Tool | Axis | The question it answers | Authority |
|---|---|---|---|
| **qdrant** | time | "what did we decide / break / learn before?" | the diary |
| **graphify** | topology (macro) | "how does the whole thing connect, where are the hubs and bridges?" | the map |
| **beacon** | semantic retrieval | "find the code by meaning — I don't know the symbol name" | the front door |
| **serena** | precision (micro), live | "where EXACTLY is it defined, who references it?" | the scalpel |

Key insight: graphify and serena both assume you roughly KNOW a name. beacon is the entry
point when you have only a fuzzy description. qdrant is the only one that crosses sessions.
serena is the only one that reads live source (the other three read an index that can lag).

Derived from graphify's graph, two surfaces that close the gap with dedicated
graph-review and visual-onboarding tools:

| Surface | Axis | The question it answers | How |
|---|---|---|---|
| **blast radius** | change-impact | "if I touch these files, what breaks, and is it tested?" | `scripts/blast_radius.py --base <ref>` walks dependents N hops → impacted files/abstracts + per-seed test gaps + risk hint |
| **onboarding** | human-facing map | "teach me this unfamiliar repo / show the big picture" | `graphify-out/GRAPH_REPORT.md` + `*.html` (already emitted on build); `graphify explain` / `path` for walkthroughs |

## The mandatory pipeline

Run in this order. Each step narrows the search space for the next.

```
0. doctor.sh --fix                      → self-heal the environment (deps, graph freshness) — run once on a new repo / when a tool misbehaves
1. qdrant-find "<task keywords>"        → recall prior context for THIS repo (skip on trivial lookups)
2. graphify query "<question>"          → orient by topology; which abstracts/communities are involved
3. beacon semantic-search "<meaning>"   → fuzzy-locate candidate files when the symbol name is unknown
4. serena find_symbol / find_referencing_symbols  → pinpoint exact symbol + callers (the authority)
   (editing a hub or prepping a PR? → blast_radius.py FIRST: impacted files + test gaps + risk)
5. grep / Glob                          → last resort only
6. AFTER the change:
     graphify update .                  → keep the map fresh (AST-only, free)
     graphify_to_qdrant.py              → persist god-nodes/bridges as architectural-facts (self-improve)
     qdrant-store                        → persist any decision / gotcha / architectural fact
```

You do NOT always run all five. Decision rule:

- Know the exact symbol name? → skip beacon, go qdrant → graphify (orient) → serena (pinpoint).
- Only a vague description ("the thing that retries failed calls")? → beacon first to surface candidates, then serena to confirm.
- Pure "what is the architecture / where are the seams?" question? → graphify alone answers it; no serena needed.
- Touching code you've edited before? → always qdrant-find first; you may have left a gotcha.
- About to edit a hub, or prepping a PR/review? → run `blast_radius.py` FIRST: it tells you what the change touches and which impacted files have no test, so you size the edit before making it. Confirm the hot edges with serena before trusting them.
- Onboarding onto an unfamiliar repo (human or you)? → read `graphify-out/GRAPH_REPORT.md` and open the `*.html` map before grepping; orient on the whole before the part.

## How they complement each other (sync directions)

These are not four silos — outputs of one become inputs to another.

- **graphify → qdrant.** After a build/update, store the god-nodes and cross-community
  bridges as `kind: architectural-fact`. Future sessions recall the topology without a rebuild.
  (`${CLAUDE_PLUGIN_ROOT}/scripts/graphify_to_qdrant.py`)
- **beacon → graphify.** A beacon hit returns a file + snippet. Cross-reference it against
  the graph: which abstract does it live in, what does it bridge to? Turns a flat hit into a
  situated one. (`${CLAUDE_PLUGIN_ROOT}/scripts/beacon_enrich.py`)
- **serena ↔ graphify.** `serena find_symbol` gives the exact `source_location`; feed that
  back to `graphify explain "<symbol>"` for its neighbourhood, and vice-versa. Micro and macro
  views of the same node.
- **qdrant → everything.** A recalled decision often names a symbol or file — hand it straight
  to serena/graphify instead of re-discovering it.

## Unified entry point

For "I have a fuzzy concept, find and situate it" run the fan-out helper:

```
${CLAUDE_PLUGIN_ROOT}/scripts/locate.sh "<concept or description>"
```

`${CLAUDE_PLUGIN_ROOT}` is the plugin's install dir, expanded automatically when codenav runs
as a plugin. If you installed the skill manually (scripts not bundled alongside), substitute
the path where you placed `scripts/`.

It queries beacon (semantic) + graphify (topology) + serena (symbol guess) in parallel and
merges into one ranked answer: candidate files, the abstract each belongs to, and exact
symbol locations where serena resolved them. Use it as step 2-4 collapsed into one call when
you genuinely don't know where to start.

## Honesty rules

- serena is the authority on live code. If graphify/beacon disagree with serena, trust serena
  and flag the index as stale (`graphify update .`, beacon reindex).
- A graphify INFERRED edge is a hypothesis, not a fact — verify with serena before acting.
- Blast radius is graph-derived: every impacted node and test gap is a hypothesis. Confirm hot edges with `serena find_referencing_symbols`; if changed files show "not in graph", run `graphify update .` (the graph is stale) before believing a small radius.
- Never narrate memory ops. qdrant-find/store happen silently unless the result changes the answer.
- Re-cluster graphify by canonical project taxonomy when Louvain over-fragments (see README).

## Setup — agent does it for the downloader (one command)

Someone who just installed this skill has nothing configured. Do NOT make them wire
four tools by hand. On the FIRST codenav task in a repo, run the self-healing bootstrap:

```
${CLAUDE_PLUGIN_ROOT}/scripts/doctor.sh --fix
```

It installs graphify + python deps if missing, builds `graphify-out/graph.json` if
absent, refreshes it if stale vs HEAD, applies a `taxonomy.py` re-cluster if present,
checks every bundled script, and prints the three agent-side MCP checks (qdrant, beacon,
serena) it cannot run itself. Then make those three MCP calls to confirm the tools are
wired; a missing one degrades gracefully (the doctrine still runs on whatever is present).

`${CLAUDE_PLUGIN_ROOT}` is the plugin's install dir, expanded automatically when codenav
runs as a plugin. Installed manually? Substitute the path where you placed `scripts/`.
Full per-tool wiring + the re-cluster recipe live in `README.md`.

## Self-healing — never fail on a stale or missing index

The combine repairs itself instead of dead-ending:

- A script that needs the graph and finds none / a stale one tells you the exact fix
  (`graphify .` / `graphify update .`); run `doctor.sh --fix` to apply it in one shot.
- `blast_radius.py` reports changed files "not in graph" → the graph is stale; run
  `graphify update .` and re-run rather than trusting a falsely-small radius.
- serena says "no project activated" → `check_onboarding_performed` once, retry.
- `recluster.py` re-execs under the interpreter graphify recorded (`.graphify_python`)
  when graphify/networkx aren't importable under the current `python3`.
- Tool disagreement → serena (live source) wins; flag the index stale and refresh it.

Rule: when a tool errors, READ the error — every script's failure message names its own
remedy. Re-run the remedy, don't fall back to blind grep.

## Self-improving — each pass sharpens the next

The combine gets better at THIS repo every time it runs. After a change (pipeline step 6):

- `graphify update .` keeps the map fresh (AST-only, free) so the next blast-radius is accurate.
- `graphify_to_qdrant.py --project <p>` persists god-nodes / bridges / abstracts as
  `kind: architectural-fact` → a future session recalls the topology with one
  `qdrant-find`, skipping the rebuild.
- `qdrant-store` any decision / gotcha you hit (tag `metadata.project`) → the diary that
  only qdrant crosses sessions on.
- When Louvain over-fragments, write a `taxonomy.py` once and `recluster.py`; from then on
  blast-radius / enrich / qdrant facts all report named abstracts, compounding clarity.

The loop: orient (graphify) → locate (beacon) → pinpoint (serena) → recall/persist
(qdrant). Outputs feed back as inputs, so the fourth pass on a repo is far cheaper and
sharper than the first.
