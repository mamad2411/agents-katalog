---
name: edit
description: "Use when the user wants to edit an existing quasar-graph graph without re-scanning — move nodes, update descriptions or per-node agent context, add or remove nodes and edges. Triggers on /quasar-graph:edit, 'edit graph', 'move a node', 'update node description', 'add an edge' — in any language."
---

# /quasar-graph:edit

Edit an existing backend graph directly: pull its full snapshot, change it in conversation, push it back. No scanning, no source-code reads. Requires the `quasar-graph` MCP server (the graph lives on the backend — there is no offline mode).

The unit of work is the snapshot file `<session_dir>/graph/graph.json`: nodes (`id`, `name`, `type`, `description`, `repoUrl`, `projectPath`, `agentContext`, `position`, `data`, `links`) and edges (`sourceNodeId`, `targetNodeId`, `type`). `push_graph` recomputes deterministic ids from `(graphId, type, name)` and rewires edges, so in-file ids only need to be internally consistent.

Node `type` is a backend enum — the only valid values are `project`, `service`, `database`, `external_api`, `admin_panel`, `gateway`, `cache`, `queue`, `storage`, `monitoring`, `auth_provider`, `cdn`, `library`, `search`, `realtime`, `other`; pushing any other value is rejected with 422. Node `data` is one flat schema shared by all types — exactly five nullable fields (`engine`, `port`, `hostname`, `technologies`, `packageName`); any field is valid on any type, and keys outside the five are not persisted by the backend.

## Conventions

Read `references/conventions.md` at the quasar-graph plugin root before acting. It defines the **action vocabulary** this skill is written in (selection prompt, edit the file, …) with its per-harness degradations, the **selection UI** rules, the **login retry flow**, and the **repo identity & binding cache** rules.

Fixed choices in this skill that always use a selection prompt: the bound-graph default offer (use bound graph / pick another), and the pre-push confirmation gate (push / keep editing / discard) — recommended/default option first.

## Phase 0 — Bind a graph

1. Confirm the `quasar-graph` MCP tools are available. If not, report:
   `Edit needs the quasar-graph MCP server (the graph lives on the backend). Enable it and retry.` Then stop.
2. **Authentication.** On a `Not authenticated with the quasar-graph backend` failure, run the login retry flow from the conventions file. If it still fails, stop (edit has no offline mode).
3. **Default from the binding cache.** Run `git remote get-url origin` in the invocation directory and normalize the URL per the conventions file. If `~/.quasar-graph/cache/bindings.json` has an entry for it, offer that graph first as the default (selection prompt: use it / pick another) — an entry naming several graphs gets one option per graph, labeled the same way. The cache lookup is read-only; ownership stays with the `bind_context` MCP tool. If pulling a cache-default graph then fails because it no longer exists on the backend, report it, leave the cache untouched, and fall back to step 4 for manual selection.
4. Otherwise (or if the user picks another): call `list_workspaces` and `list_projects`, ask which project (selection UI rules, incl. workspace labeling), then `list_graphs` with `project_id` and ask which graph — show `name / nodes_count / scanned_at` per option. If either list is empty, report it (for an empty graph list suggest `/quasar-graph:scan`) and stop. Capture `graph_id`.

## Phase 1 — Pull

1. Create a session directory `<cwd>/.quasar-graph/<session_id>/` with a fresh `session_id` (`YYYYMMDD-HHMM-<6-hex>`).
2. Call `pull_graph` with `session_dir` and `graph_id`. The snapshot lands at `<session_dir>/graph/graph.json`.
3. Present a short overview: node count, edge count, and a compact list of nodes (`name`, `type`) so the user can refer to them by name.

## Phase 2 — Edit in conversation

The user states changes in natural language ("move redis left of the api", "update the api description", "add an edge from api to redis", "remove the legacy node"). For each request, edit `<session_dir>/graph/graph.json` yourself, from the main thread — no sub-agents, no source-code reads. Keep a running list of the changes made this session.

Editing rules:

- **Positions** are `{ x, y }` numbers; when the user speaks in relative terms, derive coordinates from the neighbors they mention.
- **Adding a node:** invent any unique placeholder `id`, set `name` and `type` (required), a `position`, and any of the optional fields; reference the placeholder from new edges. `push_graph` replaces placeholders with canonical ids.
- **Removing a node:** also remove every edge that references its id.
- **Renaming a node (or changing its type)** is safe here: its `position`, `agentContext`, and `links` travel with the JSON object onto the new deterministic id.
- Never introduce two nodes with the same `(type, name)` — they would collapse into one id; `push_graph` rejects the file.
- **Scan-owned fields** (`description`, `projectPath`, `repoUrl`, graph-level `scanPath`) are legal to edit but the next scan of this graph will refresh them. **Graph-owned fields** (`position`, `agentContext`) persist across re-scans. **`links` sit in between** — the next scan merges them by URL: a link added here survives, but an edit to a link whose URL the scan produces itself (e.g. the `Admin Panel` link from a resource's `admin_url`) is overwritten by the fresh value. Mention this once when the user first edits a scan-owned field.

## Phase 3 — Confirm and push

1. When the user says they are done (or asks to push), present a change summary from your running list: nodes added / removed / renamed, fields changed per node, edges added / removed. Include the warning: the push **fully replaces** the graph on the backend — any edits made in the web UI since the pull will be overwritten (last write wins).
2. Ask with a selection prompt: push now (default) / keep editing / discard the session.
3. On push: call `push_graph` with `session_dir`. On success report the returned counts. On a validation failure, show the tool's error list verbatim, fix the file with the user, and offer the gate again.
4. The session stays live: the user can keep editing and push again. On discard, leave the session directory on disk and report its path.
