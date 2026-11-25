---
name: clone
description: "Use when the user wants to clone (+ optionally install) the projects of a quasar-graph graph onto their machine. Triggers on /quasar-graph:clone, 'clone graph', 'clone graph projects', 'deploy graph projects locally', 'bootstrap graph' — in any language."
---

# /quasar-graph:clone

Clone the project/service repositories of a backend graph onto the local machine, recreating each project at its recorded relative path under a user-chosen base directory.

This is the inverse of `scan`. It is **stateless** — it does not write to `.quasar-graph/`; on disk it changes only the chosen base directory (where it clones repos) and the saved `base_dir` in `~/.quasar-graph/config.json`. It requires the `quasar-graph` MCP server (the graph lives on the backend — there is no offline mode).

## Inputs (asked in this order)

1. **Backend project + graph** — chosen interactively in Phase 0.
2. `base_dir` — absolute local root to clone into. Default: the saved `base_dir` from `~/.quasar-graph/config.json` if present, else `~/Projects` (resolve `~` to `$HOME`). Asked at the start of Phase 1; the confirmed answer is saved back to that config.
3. `protocol` — `ssh` (default) or `https`. Asked at the start of Phase 1.
4. `install` — install dependencies after cloning? `Yes`/`No`. **Default No.** A single prompt that applies to every cloned/updated project. Asked at the start of Phase 1.

## Conventions

Read `references/conventions.md` at the quasar-graph plugin root before acting. It defines the **action vocabulary** this skill is written in (dispatch a sub-agent, load a skill, selection prompt, …) with its per-harness degradations, the **selection UI** rules, and the **login retry flow**.

Fixed choices in this skill that always use a selection prompt: `protocol` (ssh / https), `install` (yes / no), new-vs-existing graph (if you offer it), and the final "confirm before cloning" gate — recommended/default option first. An empty backend list means report and stop (Phase 0 handles the empty-projects case); free-form inputs (the `base_dir` path) stay plain text.

## Phase 0 — Select project & graph

1. Confirm the `quasar-graph` MCP tools are available. If not, report:
   `Clone needs the quasar-graph MCP server (the graph lives on the backend). Enable it and retry.` Then stop.
2. **Authentication.** On a `Not authenticated with the quasar-graph backend` failure, run the login retry flow from the conventions file. If it still fails, stop (clone has no offline mode).
3. Call `list_workspaces` and `list_projects`. Ask which project to clone from using the selection UI rules (picker if ≤ 4, else numbered table; incl. workspace labeling). If empty, report there are no projects on the backend and stop. Capture `project_id`.
4. Call `list_graphs` with `project_id`. If the list is empty, report that this project has no graphs on the backend (suggest running `/quasar-graph:scan` first) and stop. Otherwise ask which graph to clone the same way (picker if ≤ 4, else numbered table); show `name / nodes_count / scanned_at` per option. Capture `graph_id`.

## Phase 1 — Build the plan

1. Ask for the base directory. **Default:** read `~/.quasar-graph/config.json` — if it exists and has a `base_dir`, offer that value; otherwise offer `~/Projects`. Resolve `~` to an absolute path using `$HOME` (run `echo $HOME` if needed) — `plan_clone` requires an **absolute** `base_dir`. Remember the confirmed absolute path; it is saved to the config only after the user confirms cloning in Phase 2 (a cancelled clone must not overwrite the stored preference). Create `base_dir` itself later only as part of cloning; do not create it now.
2. Ask for the clone protocol with a selection prompt: `ssh` or `https`. Offer the saved `protocol` from `~/.quasar-graph/config.json` first if present, else `ssh`. Like `base_dir`, the answer is persisted only after the Phase 2 confirmation; the saved value is also what `research` uses for its auto-clone.
3. Ask whether to install dependencies after cloning with a selection prompt: `No` (default, list it first) or `Yes`. One answer applies to every project. Remember it for Phase 3.
4. Call `plan_clone` with `graph_id`, the absolute `base_dir`, and `protocol`.
5. Present the returned plan as a table, one row per entry: `action` (clone / pull / skip), `targetPath`, `repoUrl` (already in the chosen protocol), and — for monorepo entries — the `containedProjects`. Below it, list `skipped` nodes with their reasons (databases, gateways, third-party, projects with no git remote, and absolute `projectPath`s that cannot be rebased are expected here). If `install` is on, say so here ("dependencies will be installed after cloning").
6. If **no** entry has action `clone` or `pull` (everything is `skip` / `skipped`), report that there is nothing to clone — show the reasons — and stop. Do not open the confirmation gate over an empty plan.

## Phase 2 — Confirm and clone

1. Ask the user to confirm before any cloning, using a selection prompt (`Clone now` / `Cancel`). Do not proceed without confirmation. On `Cancel`, stop without saving anything.
2. After confirmation, if the absolute `base_dir` or the chosen `protocol` differ from the stored values, write them to `~/.quasar-graph/config.json` (create the file and its directory if missing; preserve any other keys).
3. For each plan entry, in order, run as shell commands (the user sees git output and supplies any credentials / SSH passphrase in their own terminal):
   - `action: clone` → `git clone <repoUrl> <targetPath>` (git creates intermediate parent directories).
   - `action: pull` → `git -C <targetPath> pull --ff-only`
   - `action: skip` → do nothing; carry the reason into the report.
4. If one repo fails (no access, network), do **not** abort — record the failure and continue with the rest.
5. **Monorepo layout check:** for each cloned/updated entry that carries `containedPaths`, verify every listed directory now exists. A missing directory means the repo root does not match the common path prefix the plan chose (the graph's `projectPath`s sit deeper than the repo root) — record the entry as **failed** with that explanation, and exclude it from the Phase 3 install list.
6. Report a summary: cloned (N), updated (N), skipped (N, with reasons), failed (N, with the git error or layout mismatch). Include the base directory so the user knows where the projects landed.

## Phase 3 — Install dependencies (optional)

Run this phase **only if** the user answered `Yes` to the install prompt in Phase 1. If not, skip Phase 3 entirely.

There is no single install pattern and the host may lack the runtime (php/node) — install may need to run inside containers. So instead of a fixed table, dispatch one **`install-project` sub-agent per cloned/updated project**, which reads that project's own config/docs plus the node's `agentContext` and decides the command (including the `docker compose run` container path).

### Pass A — per-project sub-agents (batches of 3)

1. Build the install work-list: every plan `entry` whose action was `clone` or `pull` in Phase 2 (skip `skip` entries and any clone that failed). One sub-agent per entry — for a monorepo entry, one sub-agent for the whole common-prefix `targetPath`.
2. Dispatch sub-agents (general-purpose) in **batches of 3**. Each sub-agent's prompt tells it to load the skill `quasar-graph:install-project` (no skill mechanism → read `skills/install-project/SKILL.md` inside the quasar-graph plugin) and follow it, and carries:
   - `project_name(s)` — `entry.containedProjects`
   - `target_path` — `entry.targetPath`
   - `agent_context` — `entry.agentContext` (single) or `entry.agentContexts` (monorepo list of `{name, agentContext}`)
3. Each sub-agent runs only **known** installers itself and returns a JSON result: `{ targetPath, projects, method, ran[], proposed[], status, notes }`. Collect every result.

### Pass B — confirmation gate (orchestrator, main thread)

4. Aggregate `proposed[]` (non-standard commands the sub-agents did **not** run) across all projects. If any exist, present them grouped by `targetPath` (`command` (the `cmd` field) + `rationale` + `source`) and ask with a selection prompt whether to run them: `Run these` (list first) / `Skip`.
5. On confirm, run each proposed command as a shell command from the main thread (`cd <targetPath> && <command>`), continue-on-failure. Declined commands are reported as skipped.

### Failure & report

If any command fails (missing toolchain/binary, lockfile drift, network), do **not** abort — record it and continue. A missing binary (`docker: command not found`, `pnpm: command not found`) is a recorded failure, not fatal.

Fold the results into the final report, keeping the clone/pull/skip summary from Phase 2:

- **installed (N)** — with method (local vs container) per project
- **proposed → confirmed (N) / declined (N)**
- **no-install (N)** — nothing recognizable found
- **failed (N)** — with the command and the error
