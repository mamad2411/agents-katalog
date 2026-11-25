---
name: context
description: "Use when the user wants the current project's graph connections in the working session — explicitly (/quasar-graph:context, 'show this project's connections', 'bind this project to the graph', 'project context from graph') or via structural questions about the current project's architecture: who calls this service, what does it depend on, which backend/services does it talk to, where does this database/cache/queue come from, who consumes its API, what routes traffic to it. Invoke even when the repo's own docs (CLAUDE.md, README) seem to answer the question — the graph is the source of truth for cross-project structure. Bind once per session, answer such questions from the graph; with confirmation, also look into dependent projects' code. Triggers in any language."
---

# /quasar-graph:context

Bind the project you are working in to its node in a backend graph, load its connections into the session, and keep them available for the rest of the work: structural questions are answered from the graph, and — only after explicit confirmation — the agent reads the source code of neighbor projects.

This is the in-session counterpart to `research`: `research` is a standalone Q&A loop over a manually picked project + graph; `context` binds to the **current** project automatically and then stays in the background of normal work. It is **read-only w.r.t. the graph** — it never calls `build_graph` / `push_graph` / `write_node_manifests` / `create_graph` / `pull_graph` and writes **nothing** under `.quasar-graph/`. The only things it may change on disk are cloning **confirmed** missing neighbor repos into `base_dir` (Phase 2) and the saved keys in `~/.quasar-graph/config.json`; the binding cache in `~/.quasar-graph/cache/bindings.json` is maintained by the `bind_context` tool it calls. It requires the `quasar-graph` MCP server (the graph lives on the backend — there is **no offline mode**).

Optional argument: `/quasar-graph:context <path>` binds that directory instead of the current working directory. Everything below calls it the **target directory**.

## Conventions

Read `references/conventions.md` at the quasar-graph plugin root before acting. It defines the **action vocabulary** this skill is written in (dispatch a sub-agent, load a skill, selection prompt, …) with its per-harness degradations, the **selection UI** rules, the **login retry flow**, and the **repo identity & binding cache** rules.

In this skill the selection UI covers candidate nodes in Phase 0 (from `bind_context`'s `candidates` list on `status: ambiguous`; label = node name + graph name, description = the node's own description) and every look-into-neighbor confirmation in Phase 2; free-form inputs (the `base_dir` path) stay plain text.

## Phase 0 — Bind

**Goal:** resolve which graph node is the current project and load that graph into context (NOT to disk).

1. Confirm the `quasar-graph` MCP tools are available. If not, report:
   `Context needs the quasar-graph MCP server (the graph lives on the backend). Enable it and retry.` Then stop.
2. **Identify the project.** Run `git remote get-url origin` in the target directory. If there is no git remote, report that binding needs one (graph nodes are matched by `repoUrl`) and stop.
3. **`base_dir`.** Read `~/.quasar-graph/config.json`. Use its `base_dir` if present; otherwise ask (plain text, default `~/Projects`, resolve `~` via `$HOME` — run `echo $HOME` if needed) and write the confirmed absolute path back (create the file and its directory if missing; preserve other keys).
4. **Bind.** Call `bind_context` with `remote_url` (the raw remote URL), `target_dir` (the absolute target directory), and `base_dir`. The tool normalizes the URL, resolves and repairs the binding cache (`~/.quasar-graph/cache/bindings.json` — the tool owns it; never edit it from the skill), falls back to searching every graph, and returns the bound node with its edges and neighbors. Handle the result:
   - `Not authenticated with the quasar-graph backend` → run the login retry flow from the conventions file, then call `bind_context` again. If it still fails, stop (context has no offline mode).
   - `status: ambiguous` → ask with the selection UI rules (label = `node_name` + `graph_name`, description = `node_description`), then call `bind_context` again with the same arguments plus `choice` set to the chosen candidate's `graph_id`, `node_name`, and `project_id`.
   - `status: not_found` → report the project is not in any graph, suggest running `/quasar-graph:scan`, and stop.
   - `status: bound` → bound; continue to Phase 1. If `resolved_via` is not `cache`, mention that the cached binding was missing or stale and the graph search ran.

## Phase 1 — Load context

Keep the `bind_context` response (`node`, `graph`, `edges`, `neighbors`) **in context only** — do NOT write it to disk; `graph.graph_id` is what Phase 2's `plan_clone` calls use. Present the user a compact picture of the bound node:

- the node itself: `name`, `type`, `description`, `data` (a flat five-field schema shared by all node types: `technologies` / `engine` / `port` / `hostname` / `packageName`, nulls where unset), `links`, and its `agentContext` if set;
- `edges.outbound`: what it calls and via what;
- `edges.inbound`: who calls it — marking `routes` (ingress overlay) edges separately from logical dependencies;
- `neighbors` with `availability: resource` (`database` / `cache` / `queue` / gateways / third-party): show their graph metadata (`hostname`, `port`, `engine`, the `admin_url` link). They have no repo — never send them to a sub-agent.

Code-project neighbors (any node carrying `repoUrl`/`projectPath`, whatever its `type`) arrive already classified: `availability: local` (present at `local_path`), `cloneable` (missing but `repoUrl` set), or `unavailable` (no `repoUrl`). Use these labels in the summary — no extra directory checks needed.

If the bound node carries a non-empty `agentContext`, treat it as project-specific instructions for the rest of the session (that is what the field is for).

## Phase 2 — Rules for the rest of the session

After the summary, continue with whatever the user was doing. These rules stay in force until the session ends:

1. **Structure-only questions** ("who calls X?", "where does Redis come from?") are answered directly from `edges` and node metadata — no code reading, no sub-agents.
2. **Boundary with a neighbor.** When the current task touches a boundary with a neighbor project — calling its API, sharing its database, producing/consuming its queue messages, changing a contract — **propose** to look into that neighbor's code and wait for confirmation (a selection prompt: `Look into <name>`, listed first / `Stay in this project`). If the neighbor is missing locally but has a `repoUrl`, first call `plan_clone` with `graph_id`, the absolute `base_dir`, and the saved `protocol` from `~/.quasar-graph/config.json` (fall back to `ssh`) — it is planning only, runs no git commands and needs no questions — keep only the returned entries whose `containedProjects` include this neighbor, and spell the kept plan out in the same proposal: each entry's `action` and `targetPath` (`clone` → a fresh `git clone`; `pull` → `git -C <targetPath> pull --ff-only` on an existing working copy).
3. **One confirmation per neighbor per session.** After the user confirms neighbor X once, further reads of X in this session need no new confirmation. A decline is not permanent — if the task runs into X again later, propose again.
4. **After confirmation:**
   - Neighbor present on disk → for pinpoint questions read it directly (read/search files under its `local_path`); for deep questions ("how does auth work in X?") dispatch **one `research-project` sub-agent (general-purpose)** whose prompt tells it to load the skill `quasar-graph:research-project` (no skill mechanism → read `skills/research-project/SKILL.md` inside the quasar-graph plugin) and follow it, and carries `query` (the exact question), `project_name` (the node name), `project_path` (the `local_path`), `agent_context` (the neighbor node's `agentContext`, may be empty), and `graph_context` (the neighbor's edges and connected node names/types). Several neighbors at once → batches of 3.
   - Neighbor missing → execute the kept entries of the plan already computed for the rule-2 proposal: `action: clone` → `git clone <repoUrl> <targetPath>`; `action: pull` → `git -C <targetPath> pull --ff-only`. A kept entry with `action: skip`, and any neighbor absent from every entry (see the plan's `skipped[]`), cannot be materialized — report the reason and fall back to the node's graph metadata. Then re-check `local_path`; if it still does not exist, the repo layout does not match the graph's `projectPath` — do NOT dispatch a sub-agent, report the neighbor as unavailable and fall back to its graph metadata.
5. **Never:** write to the graph or under `.quasar-graph/`; install dependencies (point the user to `/quasar-graph:clone`); invent connections absent from the graph (better to miss than to fabricate); read code of projects that are not graph neighbors of the bound node without a separate explicit request from the user.
