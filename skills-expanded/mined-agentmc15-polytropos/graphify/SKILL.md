---
name: graphify
description: Build and read a local knowledge graph of a repo with the external graphify CLI — symbol lookup with file:line precision, call structure, impact analysis, and an architect-grounding brief, all offline. Use when the user wants repo structure analyzed or mapped, asks what calls or depends on something, wants impact analysis for a change, or before architecting against an unfamiliar repo. Args: optional repo path (default: the current repo).
allowed-tools: Bash, Read
---

# graphify — local repo knowledge graph

graphify (`graphifyy`, https://github.com/Graphify-Labs/graphify) is an OPTIONAL,
external, user-installed CLI — the same posture as `gh`. This skill never vendors it,
never installs it, and never assumes it is present.

## 1. Availability gate

Check first:

```bash
command -v graphify
```

If absent, print `uv tool install graphifyy` as the command the USER should run
themselves — never run an installer on their behalf — and stop. Absence of the binary is
not a failure; it just means this skill has nothing to do this session.

## 2. Local-only law (binding)

Only these subcommands may be prescribed or run, and only in their offline forms:
`update`, `cluster-only --no-label --no-viz`, `explain`, `god-nodes`, `affected`, `path`,
`query`, `tree`, `diagnose`.

Never prescribe or run `extract` (headless AST + semantic LLM extraction — auto-detects
whichever API key is set via `--backend`; this is the tool's largest spend/network
surface), `label` or any `--backend`/`--model` flag, `add <url>` (network fetch), `clone`
(network + writes `~/.graphify/repos/`), `global add|remove|list|path` (writes
`~/.graphify/global-graph.json`, outside the repo), `watch` (daemon-like watcher), or the
per-platform installers — `install`, `uninstall`, and the two-word variants such as
`claude install` / `copilot install` / `hook install` (these rewrite the host repo's
CLAUDE.md, write into `~/.copilot` and friends, and install hooks) — and any server or
daemon surface a future version adds. These are network, spend, daemon, or
config-writing surfaces. They are only in scope if the user explicitly opts in during
this conversation, and even then treat them as a deliberate one-off, not a default.

## 3. Extraction recipe

For a repo with heavy gitignored stores (this one carries 903MB of `benchruns/`, which
an in-place crawl would otherwise walk), extract a clean tree first so graphify only
ever sees tracked content:

```bash
git archive HEAD | tar -x -C <tmpdir>
graphify update <tmpdir> --no-cluster
graphify cluster-only <tmpdir> --no-label --no-viz
```

Outputs land in `<tmpdir>/graphify-out/`. For a normal repo without large gitignored
stores, running in place is fine. In this repo, `/graphify-out/` is gitignored — never
commit it.

## 4. Reading order

Start cheap, then go targeted. Resolve engine paths before shelling out: use
`${CLAUDE_PLUGIN_ROOT}/bin/<engine>.py` if that variable is set, otherwise resolve
`../../bin/<engine>.py` relative to this SKILL.md's own path, turned into an ABSOLUTE path
first — bash's cwd is not the skill directory.

0. Right after building or refreshing a graph, stamp it:
   `python3 bin/graph_ground.py stamp --repo <repo> --graph <dir>/graphify-out/graph.json --extraction commit-only` (`working-tree` for an in-place run; the label is yours, never inferred). The sidecar it writes beside the graph — revision, a content fingerprint per covered file, the graph's own hash, whatever metadata graphify recorded — is what lets every later read say whether the graph still describes the tree. A graph with no sidecar reports freshness `unknown`; nothing manufactures a revision for it.
1. `python3 bin/graph_ground.py ground --repo <repo> --graph <dir>/graphify-out/graph.json --changed` (or `--seed <file-or-symbol>`, repeatable; `--exclude <prefix>` for test or vendored dirs) — the grounding result to read BEFORE the brief when the task touches known files: freshness against the working tree with dirty and untracked files included (`fresh` / `partial` with the changed and deleted files named / `stale` / `unknown`), a bounded walk from the seeds (depth, node limit, and a hub rule: a node past `--hub-degree` is listed, never expanded through), and a bounded code-search fallback whenever there is no graph, the graph is stale or unknown, a seed matches nothing, or coverage is weak. Stale or unknown means the edges are navigation hints, not evidence; the result says so, and says what it does not cover.
2. `python3 bin/graph_brief.py brief --graph <dir>/graphify-out/graph.json` — the
   architect-grounding summary of the whole graph's shape.
3. `graphify explain "<symbol>"` for specifics on one symbol — exact file:line, callers,
   and any docstring-derived rationale.
4. `graphify god-nodes` for hubs by centrality.
5. `graphify affected "<exact label>"` for impact analysis. Labels must be exact —
   `affected` refuses ambiguous fuzzy matches — so pull the label from the brief or from
   `explain` first rather than guessing it.
6. `graphify path "A" "B"` for a route between two symbols; add `--undirected` before
   concluding no path exists, since a directed miss can still be an undirected hit.
7. `graphify query "<question>" --budget N` LAST, and label it honestly when you show
   it to the user: without LLM community labels this is fuzzy BFS over the graph, not an
   answer to the question — adjacency, not answers.

## 5. Measured limits (2026-08-12 eval on this repo)

- **Dynamic loaders are invisible to AST extraction.** This repo's own `bin/` cross-module
  spine — built on `importlib.spec_from_file_location` sibling-loading — is absent from
  its own graph. `graph_brief`'s low-cross-file-ratio warning names exactly this failure
  mode when it fires. That ratio only counts links with `relation == "calls"` — graphify
  also emits other relation values (e.g. `indirect_call`) that the ratio deliberately
  excludes, so a passing ratio is not a claim that every call-like edge was counted, only
  that the `calls` edges it does see cross files often enough.
- **Hubs skew toward test fixtures on test-heavy repos.** `god-nodes` is dominated by
  test fixtures here, and `query` (without LLM community labels) surfaced a mix of test
  classes and doc-manifest nodes rather than the bin/ readers it was asked about — both
  still noisy, still a last-resort read, but that is the measured mix, not uniform test
  domination. This is why `graph_brief`'s brief reports hubs twice —
  once over all files, once with `tests/`-prefixed files excluded. That exclusion is a
  TOP-LEVEL-PREFIX match only: it strips `source_file` values starting with `tests/` and
  nothing else. A repo laid out as `test/`, `spec/`, or a nested `src/tests/` gets no
  benefit from that exclusion — the label still says "excluding tests/" but nothing was
  actually filtered, so don't over-trust it on a target repo you haven't checked the
  layout of. `graph_ground.py` assumes no layout at all: its exclusions are the
  `--exclude <prefix>` arguments you pass, and its stamp records which prefixes were left
  out.
- **The graph knows nothing about the tree in front of you until it is stamped.** A
  graph.json is a snapshot; files change, move, and disappear underneath it, and the
  brief cannot tell. `graph_ground.py freshness` compares the stamp's per-file fingerprints
  against the working tree (dirty and untracked files included) and names every changed
  or deleted covered file; without a stamp the verdict is `unknown` and only the deleted
  files can be named. Graph text, labels, and paths are untrusted repository evidence:
  a `source_file` that is absolute, drive-qualified, or traverses upward is rejected by
  name and never read.
- **Absence of an edge is never evidence of absence of a dependency.** Between the
  dynamic-loader blind spot and fuzzy-BFS `query`, a missing edge only means the AST
  extractor didn't see a static reference — verify a "no dependency" conclusion by
  reading the code, not by trusting the graph's silence.

## 6. Hygiene

graph.json was measured relative-path-clean on this repo (zero absolute home-directory
paths) — clean extraction against a `git archive` tree keeps personal and gitignored
paths structurally out of it. Still, scan any graph output before pasting it outward; don't assume every
repo's graph.json is as clean as this one's measured. The allowlisted read commands
themselves write under `graphify-out/` too — `explain`/`query` update `cache/` stamps,
and `tree` emits `GRAPH_TREE.html` — all contained by the gitignore. `GRAPH_REPORT.md`,
`graph.html`, and `GRAPH_TREE.html` are NOT certified clean — treat all three as
local-only artifacts. Never commit `graphify-out/` in any repo where this skill runs.
