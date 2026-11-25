---
name: repo-tour
description: Use after graphify has already built graphify-out/graph.json for a project, to generate a dependency-ordered guided tour, an onboarding doc for new team members, or a diff-impact analysis before a commit/PR — reading the existing graph instead of re-scanning the repo. Trigger on "onboarding guide", "เอกสารสำหรับทีมใหม่", "guided tour ของโค้ด", "diff impact", "อธิบาย repo ให้ทีมใหม่", "what does this change affect", when graphify-out/graph.json already exists. If graphify-out/graph.json does NOT exist yet, tell the user to run graphify first — this skill does not scan or build a graph itself.
---

# Repo Tour (reads an existing graphify graph)

## Overview

`graphify` already builds a persistent knowledge graph (`graphify-out/graph.json`) from a codebase — that's the expensive, token-hungry part, and it's already solved. What's missing is three specific consumption modes: a **dependency-ordered reading tour**, an **onboarding doc**, and a **diff-impact report**. This skill supplies those three by reading the existing graph, not by re-scanning the repo — cheap, fast, and doesn't duplicate graphify's own extraction pipeline.

**Fast-path rule (check this first, every time)**: if `graphify-out/graph.json` does not exist, **stop and tell the user to run `graphify` first** (`/graphify` or the graphify skill). Do not fall back to reading files manually — that's `project-discovery`'s job, not this skill's.

**Cost note before suggesting a graphify run**: `repo-tour` itself makes no LLM calls and costs nothing to run. Building the graph in the first place is not free, though — graphify's semantic extraction pass (anything that isn't code: `.md`, `.pdf`, images) dispatches an LLM subagent per ~20-25 files, and a real test run in this repo (10 small Markdown files) used **~116k output tokens** for that one pass. If no graph exists yet and the corpus is doc-heavy or large, say so explicitly and let the user decide whether to scope the graphify run narrower (a subdirectory, not the whole repo) rather than defaulting to a full-repo build. For a genuine one-off "explain this to me" question with no existing graph and no repeat use planned, `project-discovery` is usually cheaper — `repo-tour`'s value shows up when a graph already exists (regular graphify use) or the same graph gets reused across multiple onboarding/diff-impact checks, not on a single cold-start question.

## When to use

- สร้างเอกสาร onboarding สำหรับทีมใหม่ จากกราฟที่ graphify สร้างไว้แล้ว
- สร้างลำดับการอ่านโค้ดที่แนะนำ (จากโมดูลพื้นฐานไปหาโมดูลที่พึ่งพามัน)
- เช็คว่า diff/PR ปัจจุบันกระทบส่วนไหนของระบบบ้าง ก่อน commit
- Any request to "explain this repo to a new person" or "what breaks if I change X" when a graph already exists

## When NOT to use

- `graphify-out/graph.json` doesn't exist — run `graphify` first, this skill has nothing to read
- The user wants the graph itself explored interactively (queries, path-finding between concepts) — that's `graphify query`/`graphify path`/`graphify explain`, already built and more capable than anything here
- A one-shot, no-graph project overview for a small/unfamiliar repo — `project-discovery` is lighter-weight for that

## Core knowledge

**Three sub-workflows, one shared graph loader** (`graph_adapter.py`):

| Workflow | Script | Input | Output |
|---|---|---|---|
| Guided tour | `build_tour.py` | `graph.json` | Dependency-ordered node list (foundational modules first) |
| Onboarding doc | `build_onboarding.py` | `graph.json` + project name | Markdown doc: hub modules + reading order |
| Diff impact | `diff_impact.py` | `graph.json` + changed file paths | Per-file impact report, grouped by hop distance |

**Guided tour ordering**: topological sort over `imports`/`depends_on`/`requires` edges. An edge `source → target` means "source depends on target," so the tour visits `target` first. Real codebases have circular imports — nodes caught in a cycle are appended afterward and explicitly flagged `cycle_fallback`, never silently mixed in as if they were cleanly ordered.

**Onboarding doc**: ranks "hub" modules by total edge degree (most-connected = worth understanding early), computed directly from the edge list — does **not** depend on graphify's `god_nodes`/community analysis files, which graphify deletes as intermediate scratch after each run and are not guaranteed to exist.

**Diff impact**: for each changed file, walks the graph **backward** (finds what depends on the changed file, not what the changed file depends on) up to a hop limit, grouped by distance. Get the changed-file list with:
```bash
git diff --name-only              # unstaged changes
git diff --name-only --cached     # staged changes
git diff --name-only HEAD~1       # vs. the previous commit
```
Then run: `python3 diff_impact.py graphify-out/graph.json <file1> <file2> ...`

This is a **read-only report over the graph** — it does not run tests or execute anything. It narrows *where to look*, it does not replace actually running the test suite.

## Common mistakes

1. Running this skill without checking `graphify-out/graph.json` exists first — there's nothing to read, and re-scanning the repo manually here duplicates graphify's job.
2. Treating a `cycle_fallback` node in the tour output as if it were cleanly topologically ordered — it wasn't; the graph has a circular dependency there.
3. Assuming diff-impact's "no dependents found" means the change is definitely safe — it means the graph shows no dependents; a genuinely new/untracked relationship (or a stale graph) can hide real impact. Suggest re-running graphify if the graph is old relative to the diff.
4. Treating the impact report as a substitute for running tests — it's a "where to look" map, not a correctness guarantee.

## Code

All four modules are pure stdlib (no dependencies) and independently self-testable:

- `graph_adapter.py` — schema-tolerant loader (`load_graph`, `normalize_node`, `normalize_edge`, `build_adjacency`), plus the shared `--out` flag helpers (`parse_out_flag`, `write_or_print`) all three CLIs below use
- `build_tour.py` — `topological_tour(nodes, edges)`; CLI: `python3 build_tour.py graphify-out/graph.json [--out tour.md]`
- `build_onboarding.py` — `render_onboarding_doc(project_name, nodes, edges)`; CLI: `python3 build_onboarding.py graphify-out/graph.json "Project Name" [--out onboarding.md]`
- `diff_impact.py` — `impact_of_changed_files(nodes, edges, changed_paths)`; CLI: `python3 diff_impact.py graphify-out/graph.json <changed files...> [--out impact.md]`

All three CLIs write UTF-8 correctly to stdout by default, and to a file with `--out <path>` (parent directories are created automatically) — equivalent to `> file.md` but without depending on the shell's own redirect encoding behavior (see the earlier em-dash/Windows finding above).

Run `python3 <file>.py` with no arguments for that module's self-test (uses synthetic in-memory graph data plus, for `graph_adapter.py`, a fixture in the real graphify shape — see below).

## Where to put each output — they don't all belong in the same place

The three outputs have different lifecycles; treat them differently, not identically:

| Output | Persist it? | Where | Why |
|---|---|---|---|
| Onboarding doc | Yes, commit it | `docs/ONBOARDING.md` or repo root | Meant to be read by multiple people, repeatedly, over time — a durable artifact |
| Guided tour | Optional | `docs/` alongside the onboarding doc | Nice to keep as a reference, less critical than the onboarding doc |
| Diff impact | No — don't commit as a standing file | Paste into the PR description or chat directly | It describes one specific uncommitted diff; the moment that diff changes or merges, a saved file describing it is stale and misleading to a later reader who doesn't know it's from an old snapshot |

Never write any of the three into `graphify-out/` itself — that directory is gitignored (it holds a machine-local absolute interpreter path and regenerable cache), so anything meant to be shared or kept must go somewhere your VCS actually tracks.

## Verified against a real graph (not just guessed)

The schema in `graph_adapter.py` was checked against graphify's actual installed source (`graphify/export.py`'s `to_json()`) and confirmed by running the full pipeline on `skills/trading/` end to end. Two real bugs were found and fixed this way — worth knowing since they show what "looks right but silently isn't" looks like for this kind of tool:

1. **The top-level edge list key is `"links"`, not `"edges"`** — graphify calls `networkx.readwrite.json_graph.node_link_data(G, edges="links")`, which renames the key. A naive `graph["edges"]` on a real `graph.json` silently returns nothing (no error, just an empty list) rather than failing loudly. `graph_adapter.py` now checks `"links"` first, falling back to `"edges"`.
2. **Node type lives in `"file_type"`** (`code`/`document`/`paper`/`image`/`rationale`/`concept`), not `"type"`. **Node file path lives in `"source_file"`**, not `"filePath"`/`"path"`. Both are now the first-checked key.
3. **The real AST edge type for a Python import is `"imports_from"`**, not `"imports"`. `build_tour.py`'s `DEPENDENCY_EDGE_TYPES` and `diff_impact.py`'s `IMPACT_EDGE_TYPES` both check for it now — omitting it silently produced correct-looking but incomplete output (no crash, just a tour/impact report missing real dependency edges).
4. **`find_node_by_path`'s tolerant suffix matching was too loose for short generic filenames.** graphify relativizes a root-level skill's own file to a bare `"SKILL.md"` with no directory — the original suffix check (`file_path.endswith(node_path)`) then matched *any* longer path ending in `/SKILL.md`, e.g. querying `"drawdown-circuit-breaker/SKILL.md"` wrongly matched the *router's* bare `"SKILL.md"` node instead of (or in addition to) the actual target. Fixed by requiring the shorter of the two paths to contain at least one `/` before suffix-matching is allowed — a bare filename now only matches by exact equality.

## Known limitations

- Onboarding "hub" ranking (edge degree) is a simple proxy for importance, not graphify's own god-node algorithm (which may use different centrality measures) — the numbers won't necessarily match `GRAPH_REPORT.md`'s own god-node list if that file is still around.
- Diff-impact only follows structural edge types (`imports`, `imports_from`, `depends_on`, `requires`, `calls`) — it will not surface a change's impact through doc-level relations (`references`, `cites`, `conceptually_related_to`) even though those exist in the same graph. A change to a `SKILL.md` that other skills only *reference* in prose, not import in code, will correctly report "no dependents" — that's accurate for code-impact, not a bug, but don't read it as "nothing in the project mentions this file."
- `imports_from` edges can point at a synthetic node for an external/stdlib symbol (e.g. `Decimal`), not just another project file — those show up in the guided tour as an ordering step with no further meaning; harmless, but don't be surprised to see a stdlib name in the reading order.
- This was verified against one real run (`skills/trading/`, a small, mostly-Python-with-docs corpus) on one graphify version — a different corpus shape (e.g. TypeScript, or a run with `--mode deep`) or a future graphify release could still surface a field this skill hasn't seen yet. `graph_adapter.py`'s defensive multi-key-variant lookups remain the safety net for that.
