---
name: scan
description: "Use when the user wants to scan a directory of their projects to build a quasar-graph index. Triggers on /quasar-graph:scan, 'index my projects', 'scan my projects directory'."
---

# /quasar-graph:scan

Orchestrate a scan of a directory containing the user's projects: catalog, deep analysis, resource aggregation, pre-upload review, and upload to the backend.

## Inputs

The scan asks for inputs **in this order**:

1. **Session** — new scan or resume of an existing one, chosen in the **Session** step below. Comes first because it determines `session_dir` and whether this is a resume. A `session_id` passed explicitly in the invocation skips the choice.
2. **Backend project + graph** — chosen interactively in **Phase 0** (project, then new/existing graph). This binds the scan before anything is cataloged.
3. `scan_dir` — absolute path to the directory to scan (containing the projects). Asked **only after** the backend binding, at the start of **Phase 1**. This is the scan **target**; nothing is written here.

The chosen `project_id` and `graph_id` are stored in `manifest.backend` and drive the upload in Phase 4. If the `quasar-graph` MCP server is unavailable, Phase 0 is skipped (offline mode): the scan still asks for `scan_dir`, writes all markdown to disk, and the upload is skipped.

**Graph model** (canonical statement — the phases below reference it, do not restate it). The scan produces the **logical + ingress overlay** model: logical dependency edges (who calls / needs whom — for illustration, `client → api`, `api → db`) plus the gateway/ingress routing path as a separate `routes` edge class (illustration: `traefik → nginx → api` — the gateways sit INSIDE the traffic path). The overlay is purely additive over the SAME logical dependency edges: it never removes or rewrites one (a direct `client → api` stays even when the routed path is also drawn), and if the scan finds no environment with a gateway it is simply a no-op. There is no toggle — the routing layer is always emitted. Operational rules live in Phase 3 (§ ingress overlay).

The scan **output** is always written under the current working directory (`cwd`) where the user launched the agent session — NOT inside `scan_dir`. `cwd` and `scan_dir` are often different directories. `session_dir` is derived from `cwd` + `session_id` and is therefore known before `scan_dir` is.

**Resume** (canonical rule — the per-phase checks below implement exactly this). Picking an existing session resumes it; each phase reuses what that `manifest.json` already records and redoes only what is missing. The Session step only decides `session_dir` — what gets skipped is decided by the manifest's contents:

| Present in `manifest.json` | What is skipped / reused |
|---|---|
| `backend` block | Phase 0 — binding reused, do not re-ask. (An offline session has no `backend` block, so Phase 0 re-runs and may bind it now.) |
| `scan_dir` | the `scan_dir` prompt in Phase 1 — reused, do not re-ask |
| `projects` array | Phase 1 discovery, **the working-copy refresh offer, and the deep-scan approval gate** — skipped; Phase 2 processes only `status: pending` entries (projects **and** environments). `skipped` entries stay skipped — to bring one back, edit its `status` to `pending` and resume |

## Conventions

Read `references/conventions.md` at the quasar-graph plugin root before acting. It defines the **action vocabulary** this skill is written in (dispatch a sub-agent, load a skill, selection prompt, …) with its per-harness degradations, the **selection UI** rules, and the **login retry flow**.

Fixed choices in this skill that always use a selection prompt: the session choice (Session step — `New session` plus the existing sessions, so it follows the bounded-list rule: options if the total is ≤ 4, numbered table otherwise), new-vs-existing graph (Phase 0), the Phase 1 working-copy refresh offer (`update all projects` / `scan as-is` — see Phase 1 step 10), the Phase 1 deep-scan approval gate (`start deep scan` / `adjust the list`; its adjust sub-prompt is multi-select over the cataloged entries when they fit, numbered-table fallback otherwise — see Phase 1 step 11), and the Phase 3.5 gate (`fix first` / `upload as-is`) — recommended/default option first. An empty backend list means report and stop (except the Phase 0 empty-projects case, which falls through to creating a project); free-form inputs (`scan_dir`, the new graph's name, a new project's name) stay plain text.

## Session

**Goal:** decide which session this run writes into — a new scan or one already on disk — and derive `session_dir` from it.

**Steps:**

1. **Determine `cwd` explicitly — do not guess.** Run `pwd` and use its output as the absolute launch directory.
2. If the invocation already carries a `session_id`, use it and skip to step 5 — no prompt.
3. Call the MCP tool `list_sessions` with `cwd`. It returns the scan sessions under `<cwd>/.quasar-graph/`, newest first, each with `session_id`, `created_at`, `scan_dir`, `graph_name` (`null` = the session ran offline) and `counts` (`done` / `pending` / `skipped` across projects **and** environments). It is local and read-only — no backend call, no authentication, so it works even when the backend is unreachable. `skipped_dirs` counts directories that are not scan sessions (an `/quasar-graph:edit` session, an aborted run) — they hold no `manifest.json`, cannot be resumed by a scan, and are never offered. If the tool is unavailable, list the directories under `<cwd>/.quasar-graph/` yourself and read each `manifest.json` to build the same summary.
4. If `sessions` is empty, generate a new `session_id` silently and move on — do not open a prompt with nothing to choose. Otherwise ask with a single selection, `New session (full scan)` first, then up to the 10 newest sessions, one line each:

   `<session_id> — graph: <graph_name or "offline"> · <done> done / <pending> pending / <skipped> skipped` with `scan_dir` beneath it.

   If more than 10 exist, say so and note that an older one can be resumed by passing its `session_id` directly. Picking `New session` generates a `session_id`; picking an existing one adopts it.
5. `session_id` format: `YYYYMMDD-HHMM-<6-hex>` (e.g. `20260519-1430-a3f2c1`). Set `session_dir = <cwd>/.quasar-graph/<session_id>` as an **absolute** path (e.g. `/Users/me/work/.quasar-graph/20260519-1430-a3f2c1`).
   - ALWAYS write output using this absolute `session_dir`. Never use a path relative to `scan_dir`, and never `cd` into `scan_dir` — `scan_dir` is read-only input. The `.quasar-graph` folder must land under `cwd`, even when `scan_dir` is elsewhere.

## Phase 0 — Backend binding

**Goal:** choose the backend project and graph this scan targets, record them in `manifest.backend`, and (for an existing graph) download it into the session so graph-owned per-node fields (`position`, `agentContext`) survive the re-scan.

This runs in the main thread via the bundled `quasar-graph` MCP server.

**Steps:**

1. `session_dir` is already resolved by the Session step. If `<session_dir>/manifest.json` already exists AND has a `backend` block, this is a resume — skip Phase 0 and reuse that binding.
2. Confirm the `quasar-graph` MCP tools are available. If not, report:
   `Skipping backend binding: quasar-graph MCP server unavailable. The scan will run offline and write to <session_dir>; upload is skipped.`
   Then proceed to Phase 1 in **offline mode** (no `backend` block; Phase 4 will be skipped).
3. **Authentication.** If any backend tool call in this phase fails with `Not authenticated with the quasar-graph backend`, this is NOT the offline case — do not fall back to offline mode. Run the login retry flow from the conventions file; if the retry still fails with the same error, report it and offer offline mode explicitly.
4. Call `list_workspaces` and `list_projects`. Ask which project to scan into using the selection UI rules (picker if ≤ 4, else numbered table; incl. workspace labeling), adding a final `Create new project` option. If the list is empty, skip straight to creation — there is nothing to choose. To create: ask for the project name (plain text), then call `create_project` with `name` and — when the user has more than one workspace — the `workspace_id` chosen with the selection UI from the `list_workspaces` result already in hand (single workspace → omit `workspace_id`, the tool resolves it). Capture `project_id` + `project_name` from the chosen or created project.
5. Ask the user with the picker: **new graph or existing graph?**
   - **existing:** call `list_graphs` with `project_id` to list only that project's graphs. Ask which to use the same way (picker if ≤ 4, else numbered table); show `name / nodes_count / scanned_at` per option. If the list is empty, say so and fall back to creating a new graph. Capture `graph_id` + `graph_name`. Then call `pull_graph` with `session_dir` + `graph_id` — it writes only `graph/graph.json` (the full snapshot). Set `mode: existing`.
   - **new:** ask the user for a graph name, offering the chosen `project_name` as the default (`scan_dir` is not known yet, so a directory-derived name cannot be offered). Call `create_graph` with `project_id` + `name`. Capture the returned `graph_id`. Set `mode: new` (no seed files).
6. Write the binding into the manifest as a top-level `backend` block (Phase 1 will add `projects`):

   ```json
   "backend": {
     "project_id": "<uuid>",
     "project_name": "<name>",
     "graph_id": "<uuid>",
     "graph_name": "<name>",
     "mode": "new"
   }
   ```

   If `manifest.json` does not exist yet, create it now with `session_id`, `scan_dir`, `created_at`, and this `backend` block (Phase 1 appends `projects`).

## Phase 1 — Catalog

**Goal:** produce `<cwd>/.quasar-graph/<session-id>/manifest.json` listing all projects with status `pending`.

**Steps:**

1. `session_id` and `session_dir` are already resolved by the Session step — reuse them, do not recompute.
2. If `<session_dir>/manifest.json` already exists and already has a `projects` array, this is a resume — load it (including its stored `scan_dir`) and skip Phase 1 entirely. (Phase 0 may have created the manifest with only a `backend` block; in that case continue cataloging and **merge** the discovered projects into that file rather than overwriting it.)
3. **Ask the user for `scan_dir` now** — it is deferred until after the backend binding so the user picks the target project/graph first. If the manifest already records a `scan_dir` (resume or re-entry), reuse it without asking. **Default:** the saved `base_dir` from `~/.quasar-graph/config.json` if present, else no default. Validate it is an absolute path that exists. After validation, if the confirmed path differs from the stored `base_dir`, write it back to `~/.quasar-graph/config.json` (create the file and its directory if missing; preserve any other keys).
4. Otherwise, discover projects in **two complementary passes** at depth 1–3 below `scan_dir`. Pass 1 globs marker files; Pass 2 finds marker-less git repos. Union the results, then deduplicate by project directory (step 5).

   **Pass 1 — marker files** (a project that uses a package manager, build tool, container, CI, or is a plain static site). Marker names:

   ```
   - package.json
   - pyproject.toml
   - requirements.txt
   - go.mod
   - Cargo.toml
   - composer.json
   - pom.xml
   - build.gradle
   - build.gradle.kts
   - pubspec.yaml
   - Gemfile
   - docker-compose.yml
   - index.html            # static site with no package manager (e.g. a marketing/docs site)
   - .gitlab-ci.yml         # CI config = a deployable project even without a build marker
   - .github/workflows/     # same signal, GitHub
   - Dockerfile             # containerized project with no other marker
   ```

   Search for each marker at **every** depth 1–3 below `scan_dir`: glob `*/<marker>`, `*/*/<marker>`, AND `*/*/*/<marker>` (or one pattern `{*,*/*,*/*/*}/<marker>`). A depth-1-only glob (`*/package.json`) misses grouped layouts (`frontend/acme-site/package.json`) — such a project would then be found only if it has its own `.git` (Pass 2), and a nested project without one would be silently lost.

   **Pass 2 — git repos.** A directory that contains a `.git/` folder is a project even when it has none of the markers above (this is what catches a plain static site, a docs repo, or an infra repo). The project directory is the **directory that owns the `.git/`** — not the first path segment under `scan_dir`. This is the reliable boundary, since `repo_url` already comes from `git -C <path>`. Find these with a `.git`-presence search at depth 1–3 (do NOT descend into a repo's own `.git/` or into blacklisted dirs).

   > **Note on `index.html`:** the blacklist in step 6 (`node_modules`, `dist`, `build`, `.next`, …) keeps built/vendored `index.html` files from creating phantom projects. Only a root-level `index.html` of a real top-level directory should count.

5. For each match, the **project directory** is the directory that owns the discovery signal: for a git repo (Pass 2) it is the directory holding `.git/`; for a marker file (Pass 1) it is the **top-level directory under `scan_dir`** that contains the marker — NOT the marker file's immediate parent (e.g. `quasar-graph-mcp/mcp/package.json` → project `quasar-graph-mcp`, not `mcp`). **Monorepo / grouped layouts:** when `scan_dir`'s immediate children are grouping folders (e.g. `backend/`, `frontend/`, `devops/`) rather than projects, the project is the git-repo/marker-owning directory **nested inside** the group, not the group folder itself (e.g. `frontend/acme-site` is the project, not `frontend`). Prefer the git-repo boundary (Pass 2) to resolve the project directory when both passes match the same tree. Deduplicate: many nested markers (and the repo's own `.git`) under the same project directory collapse to one project.

6. **Skip** directories whose name is in this blacklist anywhere in their path:
   `node_modules`, `.venv`, `venv`, `.git`, `dist`, `build`, `out`, `.next`, `.nuxt`, `target`, `vendor`, `__pycache__`, `.quasar-graph` (our own output).

7. For each discovered project, derive:
   - `name` — basename of the **project directory resolved in step 5** (e.g. `acme-site` for `frontend/acme-site`) — not the marker's immediate parent (`mcp`), and not the grouping folder (`frontend`).
   - `path` — absolute path to that project directory. This becomes the node's `projectPath` (the on-disk location of the project) at upload.
   - `repo_url` — the git remote, captured by running `git -C <path> config --get remote.origin.url` (trim the trailing newline). If the directory is not a git repo or has no `origin` remote, **omit the field** (do not write an empty string). This becomes the node's `repoUrl` at upload.
   - `lang` — primary language (from the marker file present). For a marker-less project (Pass 2 git repo, e.g. a static site), infer from the dominant top-level files (e.g. `index.html` + `style.css` → `html`); the analyzer will refine.
   - `framework` — quick guess from top-level deps or files (best effort; analyzer will refine). A plain static site may have no framework — omit it.
   - `status` — `pending`.

8. **Classify each discovered directory as a `project` or an `environment`.** An **environment** is a deployment/infrastructure descriptor — it describes *how the other projects run* rather than being an app itself. It is **NOT a graph node**; it is a source of self-hosted resources and deployment topology. Signals (any is sufficient):
   - its only marker is `docker-compose*.yml` plus infra config (`traefik/`, `nginx*/`, monitoring config, k8s/helm manifests, `Makefile`) and it has **no application package manifest of its own** (no root `package.json` / `composer.json` / `pyproject.toml` / `go.mod` / … describing an app);
   - it lives under a grouping path named `devops` / `infra` / `deploy` / `deployment` / `environment` / `ops`;
   - the user explicitly designated it as a deployment/config directory.

   When genuinely unsure, prefer `project` (better a node than a silent miss). Put `project`-classified entries in `projects[]` and `environment`-classified entries in `environments[]` (same derived fields). Environments are analyzed in Phase 2 but produce **no project/service node and no edges from themselves** — only resources (Phase 3) and graph context.

9. Write the catalog into `<session_dir>/manifest.json`. **Preserve any existing `backend` block** written by Phase 0 — add/replace only the `projects` and `environments` arrays:

   ```json
   {
     "session_id": "<session_id>",
     "scan_dir": "<scan_dir>",
     "created_at": "<ISO-8601>",
     "backend": { "project_id": "<uuid>", "project_name": "<name>", "graph_id": "<uuid>", "graph_name": "<name>", "mode": "existing" },
     "projects": [
       {
         "name": "acme-backend",
         "path": "/abs/.../acme-backend",
         "repo_url": "https://github.com/acme/acme-backend.git",
         "lang": "typescript",
         "framework": "nestjs",
         "status": "pending"
       }
     ],
     "environments": [
       {
         "name": "acme-devops",
         "path": "/abs/.../devops/environment/acme/prod",
         "repo_url": "git@gitlab.com:.../environment.git",
         "lang": "yaml",
         "framework": "docker-compose",
         "status": "pending"
       }
     ]
   }
   ```

   (The `backend` block is omitted entirely in offline mode. Omit `environments` if none were found.)

10. **Offer to refresh the working copies.** A scan reads whatever is checked out, so a stale feature branch or an old checkout silently skews the graph. After the catalog is written and **before** the approval gate, ask with a selection prompt whether to update all cataloged entries first: **update all projects** (default) or **scan as-is**. Skip the prompt when no cataloged entry is a git repo.

    On **update all projects**, for each entry with a `repo_url`, run shell commands (orchestrator, main thread) in this order and never interactively:

    1. Check whether the working copy is dirty. **A dirty repo is skipped entirely** — do not switch its branch, do not pull, never stash, reset, or discard anything. Uncommitted work is the user's; losing it is not recoverable from the scan.
    2. Fetch from `origin` (with prune).
    3. Resolve the repo's **default branch** from `origin/HEAD` (`master`, `main`, `dev` — whatever the remote points at), falling back to `master` then `main` when the symbolic ref is absent. Do NOT hardcode `master`/`main`: many repos default to something else, and forcing a branch that is not the default gives a checkout that never runs in production.
    4. Check out that branch and pull **fast-forward only** — a merge or rebase can leave the working copy in a conflicted state mid-scan.

    Report a per-entry summary (`updated <branch>` / `skipped — uncommitted changes` / `failed — <reason>`) and name the skipped ones explicitly, so the user knows which entries are being scanned from an unrefreshed checkout. Failures never abort the scan — the scan continues with whatever is on disk. Then continue to the approval gate.

11. **Deep-scan approval gate.** Not every cataloged entry deserves deep analysis — the user drops the irrelevant ones (archived repos, throwaway experiments, forks) here, before any sub-agent is dispatched. Phase 2 MUST NOT start without an explicit approval: the gate is a loop the user exits only by approving the list.

    1. Present the current list of discovered **projects and environments** (name, path, lang/framework), marking any entry already excluded.
    2. Ask with a selection prompt: **start deep scan** (approve the list as shown — the default, first option) or **adjust the list**.
    3. On **adjust the list**: ask which entries to toggle — exclude kept ones or bring excluded ones back (**≤ 4 entries** → a multi-select selection prompt, label = name, description = path + lang/framework, currently-kept entries selected; **> 4 entries** → a numbered markdown table, the user types the numbers to toggle). Apply the changes by editing `manifest.json` (orchestrator, main thread): excluded → `status: "skipped"`, re-included → `status: "pending"`. Then return to step 11.1 with the updated list — the user adjusts over as many rounds as needed.
    4. Only on **start deep scan** proceed to step 12.

    `status` values: `pending | done | skipped`; after the gate, `skipped` is terminal for resume purposes (only a manual edit back to `pending` revives the entry), and a skipped entry never produces a node, an `.md` file, or a `scan/` folder. The entry stays in the manifest as a record of the decision, so a resume does not re-ask and Phase 3.5 knows the exclusion was deliberate.

12. Report to user: `Catalog done: <N> projects + <E> environments (<K> skipped) at <session_dir>/manifest.json.` Then proceed to Phase 2.

## Phase 2 — Deep analysis

**Goal:** for each `pending` entry, dispatch a sub-agent that analyzes it via the `analyze-project` skill. Projects write to `<session_dir>/scan/projects/<name>/<name>.md`; **environments** write to `<session_dir>/scan/environments/<name>/<name>.md`. Update manifest status to `done` after each success.

**Concurrency:** dispatch sub-agents in batches of 3 to keep rate limits under control. Wait for the batch to complete before dispatching the next.

**Steps:**

1. Read `<session_dir>/manifest.json`.
2. Filter `projects` **and** `environments` where `status == "pending"` — call this `queue` (each item tagged with its kind so step 5 knows where its file should land). Entries with `status: "skipped"` (excluded at the Phase 1 approval gate) are never analyzed — the `pending` filter excludes them.
3. If `queue` is empty, report `Nothing to analyze — all entries already done.` and proceed to Phase 3 (a resumed session may have finished Phase 2 earlier but never reached aggregation).
4. Take up to 3 items from `queue`. For each, dispatch a sub-agent (general-purpose) — dispatch the whole batch in parallel. **Substitute the absolute `session_dir`** (the one resolved in the Session step, e.g. `/Users/me/work/.quasar-graph/<session_id>`) into the prompt — never a relative `.quasar-graph/...` path, or the sub-agent will write to the wrong directory.

   For a **project** entry, dispatch a sub-agent described as `Analyze <project_name>` with this prompt:

   ```
   Load the skill quasar-graph:analyze-project (no skill mechanism → read
   skills/analyze-project/SKILL.md inside the quasar-graph plugin) and follow it
   with these inputs:

   project_name: <project.name>
   project_path: <project.path>
   session_dir: <absolute session_dir, e.g. /Users/me/work/.quasar-graph/20260615-1233-bbdd76>
   manifest: <stringified manifest.json content>
   ```

   For an **environment** entry, pass `role: environment` and the environment output path so the analyzer captures **only** resources + deployment topology (no node, no `connections`) — dispatch a sub-agent described as `Analyze environment <name>` with this prompt:

   ```
   Load the skill quasar-graph:analyze-project (no skill mechanism → read
   skills/analyze-project/SKILL.md inside the quasar-graph plugin) and follow it
   with these inputs:

       project_name: <env.name>
       project_path: <env.path>
       session_dir: <absolute session_dir>
       role: environment
       output_md: <absolute session_dir>/scan/environments/<env.name>/<env.name>.md
       manifest: <stringified manifest.json content>

       This is a deployment/infrastructure environment, NOT an app. Read its docker-compose*.yml and
       infra config (traefik, nginx, monitoring, centrifugo, etc.) and capture every backing service it
       operates as a `resources[]` entry — including the edge layer (`kind: gateway` for Traefik/nginx).
       Do NOT emit `connections`. Write to the `output_md` path above (under scan/environments/, NOT scan/projects/).

       Additionally, for each `kind: gateway` resource, capture a `routes:` list of the downstream
       targets it forwards traffic to (by node name — a peer project/service `name` from the manifest,
       or another gateway/resource `name`). Read these from Traefik `Host(...)` routers / service
       labels and nginx `upstream`/`proxy_pass`. Example: Traefik routes `api.* → nginx-acme-api`,
       `ws.* → centrifugo`, `acme.com → acme-site`, `app.* → acme-client`; nginx-acme-api
       routes `→ acme-api`. `routes` is the ingress/routing LAYER (a separate edge class) — it is NOT
       a `connection` and does not violate the outbound-only rule. Always record it when visible; the
       orchestrator decides at Phase 3 whether to surface it.
   ```

5. After the batch returns, validate each result before touching the manifest:
   - **Success** = the expected file exists (`scan/projects/<name>/<name>.md` for projects, `scan/environments/<name>/<name>.md` for environments) AND its YAML frontmatter parses AND contains a `name` field. Read the head of the file to check — file existence alone is not enough: a malformed frontmatter marked `done` breaks Phase 3 parsing and the upload transform, which trusts these files.
   - For each validated success: edit `manifest.json` and set that entry's `status` to `done`.
   - For each failure (no file, malformed frontmatter, or sub-agent errored): leave `status: pending` — the retry rule below or a later resume picks it up.
6. Repeat from step 2. **No-progress guard:** if a full pass over the queue completes and every remaining entry failed again (the set of `pending` entries did not shrink), do NOT keep re-dispatching — report which entries are stuck and why, leave them `pending` (a resume can retry after the user fixes the cause), and proceed to Phase 3 with the entries that succeeded. When the queue is empty, proceed to Phase 3.

## Phase 3 — Aggregate resources

**Goal:** extract resources from all `scan/projects/*/<name>.md` files, deduplicate by host, classify self-hosted vs SaaS, and write one file per unique resource into `<session_dir>/scan/resources/<slug>/<slug>.md` or `<session_dir>/scan/third-party/<slug>/<slug>.md`.

The orchestrator does this in the main thread (reading and writing the files itself), not via sub-agents. Connections between projects (`connections:` block) are NOT resources — skip them.

**Steps:**

1. For each **project** with `status: done`, Read `<session_dir>/scan/projects/<name>/<name>.md`; for each **environment** with `status: done`, Read `<session_dir>/scan/environments/<name>/<name>.md`. Parse the `resources:` YAML block of each.

   **Environments are a resource source, not a consumer.** Fold an environment's resources into the same host-keyed dedup (step 3) as projects, but do **NOT** add the environment as a `consumer` of any resource — it hosts/operates them, it does not consume them as a graph node. Record its role via `hosted_in` (e.g. `hosted_in: acme-devops (docker-compose, prod)`) instead. A resource that *only* an environment surfaced (e.g. Traefik, the monitoring stack) is a legitimate **consumer-less** self-hosted resource node — that is expected for the edge/infra layer, not an error.

2. For each resource entry, compute a `host_key` for dedup. **The key identifies the actual backing host/service — never the project that references it.** Derive it from the connection target:
   - The bare host from the `env` value or `admin_url`, stripped of scheme/port/path/credentials and (for DB URLs) of the database name. Examples: `http://centrifugo:8000/api` → `centrifugo`; `mongodb://mongo:27017/acme` → `mongo`; `centrifugo.acme.local`; `ws.acme.com`.
   - If there is no host but `type` + an identifier clearly name one logical thing (e.g. `firebase` + project id `acme-dev`), use `<type>:<id>` (e.g. `firebase:acme-dev`).
   - **Do NOT put the project name into the key**, and do NOT use a per-project DB/database name as the key when the server host is the same.
   - When genuinely uncertain whether two entries are the same thing, do NOT merge — better two near-duplicates than wrongly merged unrelated resources.

3. Group resources by `host_key` **globally, across all projects** — the same `host_key` is ONE resource even when several projects reference it. For each group, build a single merged record:
   - `consumers` — the union of `{project, env, role?}` from **every** project that references this host (one entry per project+env binding). Two projects sharing the same Centrifugo → one resource with two consumers. Preserve multiple env vars from the same project (e.g. `MONGODB_URL` and `LOCK_DSN` both bind the same mongo).
   - `name` — short slug derived from the **host**, not a project: `<type>-<short-host>` (e.g. `centrifugo`, `mongodb`, or `centrifugo-tg` if you must disambiguate two genuinely different hosts). When a single host is shared by all projects, prefer the plain `<type>` (e.g. `centrifugo`, `mongodb`). Keep slugs distinct only when the hosts are actually distinct.
   - `kind`, `type` — normalize if entries disagree; use the most specific kind (e.g. `realtime` over `external_service` for Centrifugo).
   - `description` — synthesize from the per-consumer descriptions; if multiple databases live on one server, name them here (1–2 sentences total).
   - `admin_url`, `hosted_in` — carry over if present.

   **Same server, different databases:** one MongoDB/Postgres host serving several named databases is still ONE resource (the server) — merge by host and list the database names in `consumers`/`description`. Split into separate resources only when the underlying hosts differ.

   **Worked example:** `acme-api` and `quasar-graph-api` both set `CENTRIFUGO_API_URL=http://centrifugo:8000/api` → host_key `centrifugo` → a single `centrifugo` resource whose `consumers` are both projects. Do NOT emit `centrifugo-acme` + `centrifugo-quasar-graph`. Same for mongo at host `mongo`. Two different Firebase projects (`acme-dev` vs `demo-quasar_graph`) DO stay separate — different host_keys.

4. Classify each group as **self-hosted** or **third-party**:
   - **self-hosted** if any host signal looks internal: ends in `.local`, is `localhost`, has no TLD (e.g., `mongo`, `redis`, bare hostname), is a private IP (`10.*`, `192.168.*`, `172.16-31.*`), OR matches a service name found in any scanned project's `docker-compose.yml`.
   - Otherwise **third-party** (SaaS / external API).
   - If ambiguous (no host info), default to `third-party`.

5. Write each resource to its target folder under `scan/` using this schema:

   ```yaml
   ---
   name: <slug>
   kind: <kind>
   type: <type>
   hosted_in: <where-hosted>             # self-hosted only, optional (e.g. compose env)
   admin_url: <url>                       # optional
   consumers:                             # one entry per project+env that uses this host
     - project: <project-a>
       env: <ENV_VAR>
       role: <publisher|consumer|admin>   # optional
     - project: <project-b>
       env: <ENV_VAR>
   ---

   # <slug>

   1–2 sentences describing the resource.

   ## Consumers
   - **<project-a>** — one-line note (`ENV_VAR`).
   - **<project-b>** — one-line note (`ENV_VAR`).
   ```

   **Gateway routes (ingress overlay).** When merging a `kind: gateway` resource, carry over the `routes:` list captured by the environment analyzer (downstream target names) and write it into the frontmatter — see the routing-layer note below.

6. Report final summary to user:
   `Scan complete. Session: <session_id>. Analyzed: <N> projects. Resources: <R> self-hosted, <T> third-party. Pending (retry to resume): <M>.`
   With path: `<session_dir>/scan/`.

### Phase 3 → ingress overlay (routing layer)

The logical dependency edges are ALWAYS written (every project's `connections`, every resource's `consumers`) — this step only **adds** the routing layer and never touches logical edges.

For each `kind: gateway` resource file, write its `routes:` block into the frontmatter — a list of `{ to: <node-name>, type: routes }` (or the bare-string shorthand `- <node-name>`), one per downstream target the gateway forwards to. The MCP transform (`mcp/src/transform/edges.js`) turns each into a `gateway → target` edge of type `routes`, resolving `to` against a project/service name first, then a resource slug. This puts the gateway IN the traffic path instead of leaving it a consumer-less node. Example for this repo's prod env: `traefik` → `routes: [nginx-acme-api, centrifugo, acme-site, acme-client]`, `nginx-acme-api` → `routes: [acme-api]`.

The routing layer is intentionally **gateway-downstream only** (`gateway → backend`), typed `routes`. Do NOT synthesize a `client → gateway` entry edge: the initiator's relationship is already carried by its logical edge (`client → api`), and a parallel `client → gateway` edge would duplicate it in the same plane until a UI can filter by edge type. Keep the two layers cleanly separable by `type`.

### Phase 3 → graph-level context from environments

If the scan found any `environments`, fold their deployment topology into the **graph-level `agentContext`** so the assembled graph records *where prod/infra is configured* even though the environment is not a node. Write (or update) `<session_dir>/graph/graph.json` with a top-level `agentContext` string and an empty (or existing) `nodes` array — `build_graph` reads it from this exact location and carries it into the assembled snapshot's top-level `agentContext`, which `push_graph` sends to the backend. Summarize: which repo/dir holds the configs (with its on-disk path), what the environment runs (compose stacks, proxy, monitoring), and which self-hosted resources originate there. In existing-graph mode the snapshot already provides `graph.json`; preserve any prior `agentContext` unless this scan supersedes it.

### Phase 3 → materialize graph overlay (MCP tool)

After all `scan/projects/*`, `scan/resources/*`, `scan/third-party/*` are written, call the MCP tool `write_node_manifests` with `session_dir`. It reads `graph/graph.json` + the scan folders and writes a per-node `manifest.json` (`{ id, position, agentContext }`) beside each `.md`. Existing/edited positions and `agentContext` are preserved (idempotent — an on-disk edit wins over the snapshot). In offline mode (no `graph/graph.json`) it still runs and writes `{ id }` only. Run this **before Phase 3.5** so positions and `agentContext` are visible in the review.

Then call the MCP tool `build_graph` with `session_dir`. It reads the session (manifest + `scan/` markdown), transforms it into nodes/edges with deterministic UUIDv5 ids, overlays the graph-owned per-node fields (`position`, `agentContext` — a per-folder `manifest.json` wins over the previous snapshot), and **overwrites** `<session_dir>/graph/graph.json` with the assembled snapshot (`id`, `agentContext`, `scanPath`, `nodes`, `edges`). It also backfills scan-owned node fields the fresh scan could not produce (`description`, `repoUrl`, `projectPath`, `data` keys, `links` merged by URL) from the previous `graph/graph.json` snapshot — a value the fresh scan produced always wins, previous values only patch holes. The result reports `backfilled`; if it is greater than zero, tell the user how many values were preserved from the previous graph. From this point `graph/graph.json` IS the graph this scan uploads: the Phase 3.5 review reads it and Phase 4 pushes it. During a scan the snapshot is derived — fix mistakes in the `.md` files / per-node `manifest.json` and rebuild, do not hand-edit `graph.json` (that is the `/quasar-graph:edit` flow). In offline mode (no `backend` block) skip this call — there is no `graph_id` to build against; the markdown output on disk is still complete.

## Phase 3.5 — Pre-upload review

**Goal:** before pushing anything to the backend, run one holistic review of the assembled session and surface likely mistakes to the user. This catches errors that no single per-project analyzer can see — they only emerge once the whole graph is assembled (e.g. two projects declaring the same relationship in opposite directions).

The orchestrator dispatches **one** review sub-agent in the main thread, then presents its findings and **waits for the user to confirm** before Phase 4. The review is **advisory** — it never blocks and never edits files; the user decides whether to fix first or upload as-is.

**Steps:**

1. Dispatch a single read-only review sub-agent (general-purpose), described as `Review scan session before upload`, with this prompt:

   ```
       Read-only review of an assembled quasar-graph scan session. Do NOT edit, write, or move any files — only read and report.

       Read every file under:
         <absolute session_dir>/manifest.json
         <absolute session_dir>/scan/projects/*/*.md
         <absolute session_dir>/scan/environments/*/*.md   (deployment/infra sources — NOT graph nodes)
         <absolute session_dir>/scan/resources/*/*.md
         <absolute session_dir>/scan/third-party/*/*.md
         <absolute session_dir>/graph/graph.json   (if it exists — the assembled snapshot this scan uploads, written by build_graph; absent in offline mode)

       You MAY also read (read-only) the directory listing of `manifest.scan_dir` and the deployment/compose files of any devops project, to cross-check coverage (see the "Missing project" check). Never write or move anything.

       Build the full picture (projects, resources, connections) and report likely mistakes. Check for:
       - **Reciprocal connections** — projects A and B both declaring a directional link (`rest_api` / `grpc` / `webhook` / `client_of`) to each other for the same relationship. A directional call should be declared by exactly ONE side (the caller). Flag the inbound/wrong-direction one.
       - **Dangling connections** — a `connections[].project` that does not match any `name` in manifest.json.
       - **Self-loops** — a connection whose target is the project itself.
       - **Resource-as-connection** — a resource whose `type` is the name of another scanned project (an `external_service` pointing at a peer should be a `connections[]` edge, not a resource).
       - **Resources without consumers** — a resource file with an empty/missing `consumers` list. NOTE: `kind: gateway` (reverse proxy / web server) and `kind: monitoring` (observability stack — Prometheus/Grafana/Loki/exporters) resources are LEGITIMATELY consumer-less infra/edge nodes — do not flag them as orphans. A gateway instead carries a `routes:` list (downstream targets); that is expected, not a defect.
       - **Dangling / wrong routes** — if a gateway has a `routes:` block, each `to:` target must resolve to a scanned project/service `name` or a resource slug; flag a route to a non-existent node. Also flag an obviously wrong direction (a backend "routing to" its front proxy) or a route that should have been a logical `connection` instead. The `routes` layer must remain additive — it must NOT have replaced a logical `connections` edge (e.g. a `client → api` rest_api edge going missing because someone moved it into the gateway path is a regression; logical edges stay).
       - **Likely duplicate resources** — separate resource files that appear to be the same backing host/service (same hostname, or one internal + one public route to the same thing) and should have been merged; OR a single resource that merged two genuinely different hosts.
       - **Misclassification** — a self-hosted-looking host (`.local`, bare hostname, private IP, compose service) filed under `third-party/`, or a clear SaaS filed under `resources/`.
       - **Orphans** — a project node with no connections and no resources (informational, not necessarily wrong).
       - **Missing project (catalog gap)** — a project that exists but was never cataloged, so it has no node. Two strong signals: (a) a **deployment reference** — a compose `services:` entry, a deployed `image:` name, a Traefik `Host(...)` router, or an nginx upstream (typically inside a devops project) that names an app (e.g. `acme-site`, `*-web`, `*-site`) for which **no project node exists**; and (b) a **directory under `manifest.scan_dir`** (at depth 1–3, skipping the step-6 blacklist) that looks like a project — it contains `.git/`, or a `package.json` / `index.html` / `Dockerfile` — but whose name is **absent from `manifest.projects`**. Marker-less static sites are the classic miss. Report these as `warning` with the concrete directory path and the suggested project name; the fix is to re-run the scan after adding the project (Phase 1 Pass 2 should now catch git repos), or catalog it manually. EXCEPTION: a manifest entry with `status: "skipped"` was deliberately excluded by the user at the Phase 1 approval gate — do NOT flag its directory as a missing project; at most list skipped entries once as `info`.
       - **Diff vs. current backend graph** — if `manifest.json` has a `backend` block, call the MCP tool `get_graph` with its `graph_id` and compare the result against the assembled `graph/graph.json`: summarize project/resource nodes that are newly added, and nodes present on the backend but absent from the assembled snapshot — those will be REMOVED by the full-replace upload, so name them explicitly. If the `get_graph` tool is unavailable in your environment, skip this check and say so. This is informational context for the user, not necessarily a mistake.

       Return a markdown report grouped by severity: `error` (almost certainly wrong), `warning` (likely wrong, review), `info` (worth a glance). For each finding give: the file(s) involved, what's wrong, and the concrete fix. If nothing is found, say so explicitly. Do not fabricate findings — only report what the files actually show.
   ```

2. Present the sub-agent's report to the user verbatim (or lightly summarized), then ask with a selection prompt whether to:
   - **fix first** — apply the suggested edits to the `project.md` / resource files, then re-run this review, or
   - **upload as-is** — proceed to Phase 4.

   Do NOT proceed to Phase 4 until the user confirms. If the user asks for fixes, edit the affected files (orchestrator, main thread — edit/write the files directly), then **re-run `write_node_manifests` and `build_graph`** (both with `session_dir`) before uploading — fixes can add or rename node folders (and a `role` change alters the node's deterministic id), so the per-node `manifest.json` files must be re-materialized and the `graph/graph.json` snapshot re-assembled; both tools are idempotent, existing positions and `agentContext` survive. Then optionally re-dispatch the review.

## Phase 4 — Upload to backend

**Goal:** push the assembled `<session_dir>/graph/graph.json` to the backend graph chosen in Phase 0. `push_graph` validates the snapshot, recomputes deterministic node/edge ids and anchors, and the backend's `/scan` endpoint **fully replaces** that graph's contents.

The orchestrator does this in the main thread after the user confirms the Phase 3.5 review.

**Steps:**

1. If the scan ran in **offline mode** (no `backend` block in the manifest), report:
   `Skipping upload: scan ran offline (no backend binding). Output is saved at <session_dir>. Re-run the scan with the MCP server enabled to bind and upload.`
   Then stop — the markdown output on disk is complete.

2. Call the MCP tool `push_graph` with:
   - `session_dir` — the absolute `<session_dir>` used throughout.
   It reads `<session_dir>/graph/graph.json` — the snapshot assembled by `build_graph` at the Phase 3 tail. If it fails because `graph/graph.json` is missing, re-run the Phase 3 materialize steps (`write_node_manifests`, then `build_graph`) and retry.

3. On success report:
   `Uploaded to backend. Graph: <graphId>. Nodes: <nodesPushed>. Edges: <edgesPushed>.`

4. On error (network, backend unreachable, validation 422), report the returned error message and remind the user the scan output is preserved at `<session_dir>` and the upload can be retried by re-running Phase 4.

> **Note:** node/edge identity is stable (deterministic UUIDv5), so re-scanning reuses the same ids. Graph-owned fields preserved across re-scans: `position` and `agentContext`, materialized into per-folder `manifest.json` files and applied into the snapshot by `build_graph` in Phase 3. Scan-owned fields (`description`, `repoUrl`, `projectPath`, `data`) are refreshed on every node, but a value the fresh scan could not produce is backfilled from the previous snapshot (fill-missing; stale values are removed via `/quasar-graph:edit`); `links` are merged by URL — the fresh link wins per URL, previous links with other URLs are inherited. A reclassified node gets a new id, so nothing carries over to it.
