---
name: research
description: "Use when the user wants to research/answer a question across their projects' code using a quasar-graph graph as the map. Triggers on /quasar-graph:research, 'research graph', 'query graph', 'find in graph', 'search the graph' — in any language."
---

# /quasar-graph:research

Answer a natural-language question — or trace a pasted error — by reading the **real source code** of the relevant projects, using a backend graph as the **router**: the graph supplies the connections (edges) and the paths (`projectPath`, `repoUrl`) needed to scope and locate the code.

This is the read-side counterpart to `scan`: `scan` builds the map, `research` navigates it into the code. It is **read-only w.r.t. the graph** — it never calls `build_graph` / `push_graph` / `write_node_manifests` / `create_graph` / `pull_graph` and writes **nothing** under `.quasar-graph/`. The only things it may change on disk are syncing **relevant** repos under `base_dir` — cloning the missing ones and fast-forward-pulling the already-present ones (Phase 1, after one confirmation) — and the saved `base_dir` in `~/.quasar-graph/config.json`. It requires the `quasar-graph` MCP server (the graph lives on the backend — there is **no offline mode**).

## Conventions

Read `references/conventions.md` at the quasar-graph plugin root before acting. It defines the **action vocabulary** this skill is written in (dispatch a sub-agent, load a skill, selection prompt, …) with its per-harness degradations, the **selection UI** rules, the **login retry flow**, and the **repo identity & binding cache** rules.

In this skill every gate (`Research the current project's graph`, `Search all <N>`, `Sync & research`) is a fixed-choice selection prompt; an empty backend list means report and stop; free-form inputs (the `base_dir` path, the research query) stay plain text.

## Phase 0 — Bind graph

**Goal:** choose the backend project + graph, load the graph into context (NOT to disk), and resolve a local `base_dir` for rebasing project paths.

This runs in the main thread via the bundled `quasar-graph` MCP server.

1. Confirm the `quasar-graph` MCP tools are available. If not, report:
   `Research needs the quasar-graph MCP server (the graph lives on the backend). Enable it and retry.` Then stop.
2. **Authentication.** On a `Not authenticated with the quasar-graph backend` failure, run the login retry flow from the conventions file. If it still fails, stop (research has no offline mode).
3. **Working-directory shortcut.** Before asking anything, try to resolve the directory research was invoked from to a graph it is already bound to:
   1. Run `git remote get-url origin` there; no git remote → skip to step 4. Normalize the URL with the graph's own rules ("Repo identity & binding cache" in the conventions file).
   2. Read the binding cache `~/.quasar-graph/cache/bindings.json` (shape and ownership in the conventions file — research only reads it, never writes). Missing file or no entry under the normalized URL → skip to step 4.
   3. Dedupe the matched entries by `graph_id`. **One graph** → ask with a selection prompt whether to research it (`Research the current project's graph`, listed first, naming the bound `node_name` / `Pick another project`). **Several graphs** → offer one option per graph the same way (label = `node_name` + a graph identifier, following the selection UI rules) plus a final `Pick another project` option.
   4. On accept, capture that entry's `project_id` and `graph_id` and continue at step 6 — steps 4–5 are skipped. If step 6's `get_graph` then fails (stale cache — the graph is gone), fall back to step 4 and leave the cache untouched. On `Pick another project`, continue with step 4.
4. Call `list_workspaces` and `list_projects`. Ask which project to research using the selection UI rules (incl. workspace labeling). If empty, report there are no projects on the backend and stop. Capture `project_id`.
5. Call `list_graphs` with `project_id`. If the list is empty, report that this project has no graphs on the backend (suggest running `/quasar-graph:scan` first) and stop. Otherwise ask which graph the same way; show `name / nodes_count / scanned_at` per option. Capture `graph_id`.
6. Call `get_graph` with `graph_id`. Keep the returned graph (`nodes[]`, `edges[]`) **in context only** — do **NOT** write it to disk (that is `pull_graph`'s job, and research does not use it).
7. Ask for the local `base_dir` (plain text). **Default:** the saved `base_dir` from `~/.quasar-graph/config.json` if present, else `~/Projects`; resolve `~` to an absolute path via `$HOME` (run `echo $HOME` if needed). After the user confirms, if the absolute path differs from the stored value, write it back to that config (create the file and its directory if missing; preserve any other keys). Do not create `base_dir` now. This rebases each node's relative `projectPath` (`abs = join(base_dir, projectPath)`).

Each node carries: `name`, `type`, `description`, `data` (`technologies` / `engine` / `port` / `hostname`), `repoUrl`, `projectPath` (relative to the graph's `scanPath`), `links`, and graph-owned `agentContext`. Each edge carries `type` (`routes` overlay vs logical dependency), `sourceNodeId`, `targetNodeId`.

## Phase 1 — Research loop

The graph is now in context. If the user passed a query as the skill argument (`/quasar-graph:research <question>`), handle it immediately; otherwise ask the user for their first question (plain text). After answering, ask for the next question and repeat **without re-fetching the graph**, until the user says they are done.

A query is either a **question** ("how does auth work?", "which project uses Redis?") or a **pasted error / stack trace** (`ECONNREFUSED mongodb:27017`, a traceback). For each query, run the ladder:

### 1. Scope via graph

Compute the **minimal** set of relevant project/service nodes from the graph:

- **Error input:** extract entities from the message — hostname, port, service name, resource type, error string. Match them to node `name` / `data.hostname` / `data.port` / `data.engine` / `type`. Include the matched node's **graph neighbors** (follow `edges` where it is `sourceNodeId` or `targetNodeId`) — the caller is often where the fix lives.
- **Question input:** match by `type` / `data.technologies` / `name` / `description`, then expand along `edges` as the question implies (e.g. "how does auth work" → start at the client/api node, follow edges to an `auth_provider` node). Use `edge.type` to tell runtime traffic (`routes` overlay) from logical dependency.
- **Topological short-circuit:** if the question is purely about structure ("what connects to X?", "what depends on Y?"), it is answerable from `edges` alone — answer directly from the graph and **skip steps 2–5** (no code descent).

Only `project` / `service` nodes have code to read. Resource/database/gateway/third-party nodes have no repo — use their graph metadata (`hostname`, `port`, `links`) directly, never send them to a sub-agent.

- **Empty scope:** if no node matches the query, do NOT silently dispatch across all projects. Tell the user nothing in the graph matched, show the candidate `project`/`service` nodes (name + description), and ask where to look.
- **Wide scope:** if more than **5** code nodes are relevant, show the list and confirm with a selection prompt (`Search all <N>`, listed first / `Narrow down`) before dispatching anything. On `Narrow down`, ask which projects to include.

### 2. Locate

For each relevant **code** node, rebase its `projectPath`: `local_path = join(base_dir, projectPath)`.

### 3. Ensure present & fresh (auto-clone missing, auto-update present)

Every relevant code node must be researched against a **present and up-to-date** working copy. Keep an in-session `synced` set of repo paths (target paths of executed or dirty-skipped entries): a repo is synced **at most once per session**, no matter how many questions touch it.

For each `local_path`, check whether the directory exists on disk (e.g. `test -d <local_path>`). Split the relevant nodes:

- **`missing[]`** — path absent AND the node carries a non-empty `repoUrl`. (A relevant node missing locally but with **no** `repoUrl` cannot be cloned — note it and fall back to its graph metadata.)
- **`stale[]`** — path present, but the node's repo is not yet in the `synced` set.

If both lists are empty, go straight to step 4. Otherwise:

1. Call the `plan_clone` MCP tool with `graph_id`, the absolute Phase-0 `base_dir`, and the saved `protocol` from `~/.quasar-graph/config.json` (fall back to `ssh`) — this is **planning only**, no git runs yet, and it needs no extra questions. It returns the deterministic plan for the whole graph: correct clone URLs (same normalization the graph was written with), monorepo-deduped `targetPath`s, and per-entry `action` (clone / pull / skip).
2. From the returned `entries`, keep **only** those whose `containedProjects` include a `missing[]` or `stale[]` node's name — entries for projects the query does not touch must NOT be executed. Drop kept entries whose `targetPath` is already in the `synced` set. A kept entry with `action: skip`, and any missing node absent from every entry (see the plan's `skipped[]`), cannot be materialized — report the reason and fall back to that node's graph metadata; these need no confirmation.
3. If no executable entry remains, skip the gate and research what is present. Otherwise ask for **one** confirmation with a selection prompt (`Sync & research`, listed first / `Skip sync`), spelling out exactly what will run: which repos will be **cloned** and where, and which **already-present repos will be pulled** (`git -C … pull --ff-only`) — the user must see when an existing working copy is about to be touched.
4. On confirm, execute each kept entry:
   - `action: clone` → `git clone <repoUrl> <targetPath>` (git creates intermediate parent directories).
   - `action: pull` → first run `git -C <targetPath> status --porcelain`. Non-empty output means uncommitted local changes: do NOT pull, record the repo as researched from a **dirty local copy**, and continue. Clean → `git -C <targetPath> pull --ff-only`.
   - Add the entry's `targetPath` to the `synced` set regardless of outcome — one attempt per repo per session.
5. If a clone/pull fails (no access, network, diverged history blocking `--ff-only`), record the failure and continue with the working copy as it is — do not abort.
6. **Re-check after cloning:** for every node in `missing[]`, re-run the existence check on its `local_path`. A path still missing after a successful clone/pull means the repo layout does not match the graph's `projectPath` (e.g. the monorepo common prefix sat deeper than the repo root) — do NOT dispatch a sub-agent at that path; record the node as unavailable and fall back to its graph metadata.
7. Research never installs dependencies — reading code does not need them. If the user asks for the cloned projects to be installed, point them to `/quasar-graph:clone` (its install pass carries the confirmation gate for non-standard commands).
8. On `Skip sync`, research the working copies as they are (present ones stay stale, missing ones stay unavailable) and tell the user which clones and updates were skipped.

### 4. Research the code (sub-agents)

Announce the scope in one line before dispatching ("Searching in: A, B, C"). Then dispatch **one `research-project` sub-agent (general-purpose) per relevant present project**, in **batches of 3**. Each sub-agent's prompt tells it to load the skill `quasar-graph:research-project` (no skill mechanism → read `skills/research-project/SKILL.md` inside the quasar-graph plugin) and follow it, and carries:

- `query` — the user's exact question / error.
- `project_name` — the node `name`.
- `project_path` — the node's `local_path`.
- `agent_context` — the node's `agentContext` (may be empty).
- `graph_context` — this node's edges/connections (its `sourceNodeId`/`targetNodeId` edges and the connected node names/types), so the sub-agent understands cross-project boundaries.

Each sub-agent reads the project's **source code** and returns the JSON object defined by `research-project` (`{ project, found, confidence, summary, findings[], notes? }`). Collect every result.

### 5. Synthesize

Merge the sub-agent results into a single **prose answer**, written in the language the user asked in:

- Lead with the direct answer to the user's query.
- Cite the concrete evidence as `file:line` (prefix each with the project name, since files come from different projects), drawn from the sub-agents' `findings[]`. When results conflict, weigh them by their `confidence`.
- Mention the relevant graph nodes and surface their `links` (`admin_url`, `repoUrl`) when useful.
- If every sub-agent returned `found: false`, say plainly that the answer was not located in the code (and give whatever partial answer the graph metadata supports). Do **not** fabricate.
- If a sub-agent's `notes` reports a trail into monorepo shared code outside its scope, surface it: the answer may live in that shared path, which no graph node covers.
- State which projects were searched, and note any that were skipped, unavailable, failed to clone, or were researched from a stale or dirty working copy (update skipped or failed) — the answer's coverage must be honest.

Then ask the user for their next question (loop back to the top of Phase 1).
