---
name: noui-record-workflow
description: Use this skill when the user wants to record a browser workflow and export it as a FastMCP server, a Claude Code Skill, or both. Triggers on "record a workflow", "export as MCP", "export as skill", "generate a FastMCP server", "generate a Claude Code skill", "noui workflow record", "workflow export", "capture a workflow", "turn a workflow into a tool", "create an MCP server from a website", or "I want to automate this workflow". Covers authenticated (session-cookie via Tabby), static API-key, and unauthenticated sub-paths. Covers both output formats.
---

# NoUI Record Workflow

Record a browser workflow and compile it into a runnable FastMCP server, a Claude Code Skill, or both. Works for session-cookie apps (full Tabby login flow), static API-key apps (just set an env var), and public unauthenticated APIs.

All commands run from the `noui/` directory using `.venv/bin/python cli/main.py`.

**Prerequisite:** `/noui-setup` must be complete. For Path A (session-cookie), `/noui-record-login` must also be complete and a live Tabby browser session must be running (`tabby session ensure`).

---

## Output Format Selection

Before exporting, decide what the user actually wants. Two orthogonal axes:

1. **Auth model** — Path A/B/C below (session-cookie vs static API key vs public).
2. **Output format** — `--as mcp` (always-on FastMCP server), `--as skill` (lazy-loaded Claude Code skill), or `--as both` (default).

When to pick which output:

| Output | Best for |
|---|---|
| `--as mcp` | Tools agents invoke constantly; need typed tool schemas always in context |
| `--as skill` | Long-tail / infrequent workflows; keeps Claude's context window clean until the intent matches |
| `--as both` | Unsure. No extra recording work; just a second compile pass. Ship both and let usage decide. |

The default is `--as both`. The rest of this skill focuses on the MCP output (auth verification, `mcp` lifecycle, etc.) because that is the longer-established path. For skill-side lifecycle (`skill list / show / install / uninstall`) invoke `/noui-generate-skill` after export.

---

## How Execution Works

Generated operations run **inside Tabby's authenticated browser** by default.
Each operation:

1. Opens a WebSocket to Tabby's CDP endpoint at `localhost:9222`.
2. Finds the tab whose URL matches the recorded domain (via `find_page`).
3. Calls `cdp_fetch(ws_url, url, method=..., headers=..., body=...)`, which
   runs `fetch(url, {credentials: 'include'})` via `Runtime.evaluate` — so the
   real browser's cookies, TLS fingerprint, and origin are used.

The two primitives live in the generated `noui_runtime/cdp.py` module:

```python
from noui_runtime.cdp import find_page, cdp_fetch
```

### Why this is the default

- **No credential extraction.** The Python MCP process never handles cookies
  or bearer tokens directly.
- **Matches what a real user does.** Real browser fingerprint and cookies
  eliminate the Akamai / Cloudflare / PerimeterX false positives that fire on
  Python HTTP clients.
- **Safer under session refresh.** Cookie rotation is handled by the browser;
  the MCP never sees a stale cookie.

### Runtime prerequisites

- Tabby must be running with a live session for the app.
- A page on the target domain must be open in that session. If not, the first
  call raises a clear error naming `tabby session ensure --profile <slug>`.

### Escape hatch — `--execution-mode http`

Switch to the legacy Python-side path when CDP cannot work:

```bash
.venv/bin/python cli/main.py workflow export <session_id> --execution-mode http
```

Use `http` mode when:

- The API is server-to-server and not reachable from the browser origin.
- CORS blocks `credentials: 'include'` cross-origin (no
  `Access-Control-Allow-Credentials: true`).
- You are running the MCP on a host without a live Tabby.

Under `--execution-mode http` the generator emits the classic
`httpx.AsyncClient()` + `resolve_auth()` template. The same flag is available
on `noui autopilot export`.

---

## Mode Selection

**Ask the user (or infer from context) before proceeding:**

| App auth type | Path |
|---|---|
| Session-cookie login — have `tabby_profile_id` from `/noui-record-login` | **Path A** — tabby_credentials |
| Static API key / Bearer token in every request, no login page | **Path B** — static_secret_header |
| Public API, no credentials needed | **Path C** — unauthenticated |

The compiler auto-detects the strategy from the HAR (Authorization header + no Set-Cookie → Path B). Pass `--profile-slug` for both Path A and B; omit it for Path C.

---

## Critical Rules (Never Violate)

- **ALWAYS** start the backend before asking the user to record
- **NEVER** skip `workflow export` — recording alone produces no server or skill
- Prefer the default `--as both` unless the user has a clear reason to pick one; it's a single extra compile pass and preserves the choice for later
- For Path A/B: **ALWAYS** pass `--profile-slug <slug>` — this is the runtime credential identifier; without it auth falls back to unauthenticated
- **NEVER** pass the DB UUID as `--profile-slug` — that is admin-only; use the human-readable slug (e.g. `example-bank`, not `8fdadf43-...`)
- **ALWAYS** note the `server_id` printed after export — it is required for all `mcp` commands
- **ALWAYS** create the workflow session with the CLI before the user records in Chrome — the session_id is needed for export

---

## Step 1 — Start the Backend

```bash
.venv/bin/python cli/main.py start
```

Spawns a detached FastAPI server at `http://localhost:8002`. Verify with:

```bash
.venv/bin/python cli/main.py status
```

**If startup fails:** See the troubleshooting table in `/noui-setup`.

---

## Step 2 — Create a Workflow Recording Session

```bash
.venv/bin/python cli/main.py workflow record "<WorkflowName>" "<start-url>"
```

Examples:

```bash
# Path A — authenticated
.venv/bin/python cli/main.py workflow record "Create Contact" "https://app.hubspot.com/contacts"

# Path B — unauthenticated
.venv/bin/python cli/main.py workflow record "Fetch Posts" "https://jsonplaceholder.typicode.com"
```

The CLI creates a workflow session and prints the `session_id`. Note it — you need it for export.

The backend also creates an **App** (project) and **Process** that will appear in the Chrome extension. The App name is based on the URL hostname (e.g., `app.hubspot.com`). You do NOT need to create these manually in the extension.

---

## Step 3 — Record in Chrome

The CLI already created an App and Process in the backend. The extension should see them automatically.

Tell the user to perform these steps in the **NoUI Workflow Recorder** extension:

1. Click the extension icon in the Chrome toolbar
2. The App created by `workflow record` should appear in the extension's App list — **select it**
   - If you don't see it, click the refresh/reload button in the extension, or close and reopen the popup
   - The App name matches the URL hostname from the `workflow record` command
3. Select the **Process** under that App (there should be one matching your workflow name)
4. Click **Start Capture** to begin recording
5. Navigate to the start URL and perform the complete workflow you want to automate
6. Click **Stop** when done

> **Important:** Do NOT create a new App/Project in the extension. The CLI already created one. Creating a new one will disconnect the capture from the workflow session, and export will fail.

After stopping, get the **capture session ID** from the CLI:

```bash
.venv/bin/python cli/main.py workflow captures
```

Lists all capture sessions with their IDs, statuses, and project IDs. Note the `id` of the most recent `stopped` session whose project matches the workflow's project — that is your `capture_session_id`.

> **Tip:** If `workflow captures` shows many sessions, run `workflow list` to find your workflow session and match by `project_id`.

> If no capture sessions appear linked to your workflow's project, the capture was likely recorded under a different App in the extension. Re-record, making sure to select the correct App (the one created by `workflow record`).

> For Path A (authenticated apps): navigate to the authenticated starting point manually before starting capture — credentials are managed separately via Tabby.

---

## Step 4 — Export as FastMCP Server

Pass both the `session_id` (from Step 2) and the `capture_session_id` (from Step 3):

### Path A — Session-cookie (tabby_credentials)

```bash
.venv/bin/python cli/main.py workflow export --as mcp <session_id> \
  --capture-session <capture_session_id> \
  --profile-slug <app-slug> \
  --profile-db-id <tabby_profile_db_uuid> \
  --verify
```

### Path B — Static API key (static_secret_header)

```bash
.venv/bin/python cli/main.py workflow export --as mcp <session_id> \
  --capture-session <capture_session_id> \
  --profile-slug <app-slug> \
  --verify
```

The compiler detects the Bearer token in the HAR and automatically generates the `static_secret_header` strategy. `--verify` will report `NEEDS_SECRET <APP_SLUG>_API_KEY` — set that env var in `noui/.env` then re-run to confirm `PASS`.

### Path C — Unauthenticated

```bash
.venv/bin/python cli/main.py workflow export --as mcp <session_id> --capture-session <capture_session_id>
```

The CLI compiles the captured HAR and click events into a FastMCP server and writes it to:

```
workbench/mcp_servers/<app_slug>/<server_id>/
├── server.py            # FastMCP entrypoint
├── tools.json           # Tool inventory (source of truth for tool shapes)
├── manifest.json        # Server manifest (schema v2: strategy, profile_slug, auth_plan_file)
├── API.md               # Human-readable API reference (auto-generated)
├── auth_plan.json       # Auth strategy + fallback recipes (Path A/B only; never stores secrets)
├── noui_runtime/
│   └── auth.py          # Runtime auth adapter (2-step Tabby flow or static env var)
└── operations/
    └── <tool_name>.py   # One file per generated tool
```

On success:

```
MCP server generated:
  Server ID  : <server_id>
  Tools      : <n>
  Output     : workbench/mcp_servers/<app_slug>/<server_id>/
```

**Note the `server_id`** — pass it to `/noui-generate-mcp` to start and connect the server.

> **Optional Step 5 — Generalize:** If the generated tools have unreadable raw API parameter names (`f_sid`, `bl`, `reqid`, `soc_app`), run `/noui-generalize`. Claude will read the tools, ask you questions about what you recorded, and rewrite the operations with natural-language parameters (`origin`, `destination`, `departure_date`) so they're usable by Claude Code.

---

## Decision Flow

```
Start
  │
  ├─ App auth type?
  │     ├─ Session-cookie login → Path A (need tabby_profile_id from /record-login)
  │     ├─ Static API key/Bearer → Path B (just need the slug; set env var after export)
  │     └─ No auth → Path C
  │
  ├─ Backend running?
  │     ├─ No  → Step 1: start
  │     └─ Yes → continue
  │
  Step 2: workflow record "<Name>" "<url>" → note session_id
  │
  Step 3: Chrome (select the App created by CLI → Start Capture → perform workflow → Stop)
    └─ get capture_session_id: workflow captures (match by project_id)
  │
  Step 4:
    Path A: workflow export --as mcp <session_id> --capture-session <cap_id> --profile-slug <slug> --profile-db-id <uuid> --verify
    Path B: workflow export --as mcp <session_id> --capture-session <cap_id> --profile-slug <slug> --verify
              └─ NEEDS_SECRET? → add <APP>_API_KEY to noui/.env → re-run --verify → PASS
    Path C: workflow export --as mcp <session_id> --capture-session <cap_id>
    └─ note server_id
  │
  Done → pass server_id to /mcp
```

---

## CLI Command Reference

| Command | Purpose |
|---|---|
| `.venv/bin/python cli/main.py start` | Start the NoUI backend |
| `.venv/bin/python cli/main.py status` | Check backend reachability and session counts |
| `.venv/bin/python cli/main.py workflow record "<Name>" "<url>"` | Create a workflow recording session |
| `.venv/bin/python cli/main.py workflow list` | List existing workflow sessions |
| `.venv/bin/python cli/main.py workflow captures` | List capture sessions recorded via the extension (use this to get `capture_session_id`) |
| `.venv/bin/python cli/main.py workflow export --as mcp <session_id> --capture-session <cap_id>` | Compile session → FastMCP server (unauthenticated) |
| `.venv/bin/python cli/main.py workflow export --as mcp <session_id> --capture-session <cap_id> --profile-slug <slug>` | Compile session → FastMCP server (authenticated, auto-detects strategy) |
| `.venv/bin/python cli/main.py workflow export --as mcp <session_id> --capture-session <cap_id> --profile-slug <slug> --profile-db-id <uuid>` | As above, also records DB UUID for admin operations |
| `.venv/bin/python cli/main.py workflow export --as mcp ... --verify` | Run AuthVerifier immediately after export; reports PASS / NEEDS_SECRET |

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Backend not running | `.venv/bin/python cli/main.py start` |
| `session_id` not found | Run `workflow list` to confirm the session was created |
| Export fails: "No HAR file found for this session" | Extension did not capture HAR — confirm Capture was active during the workflow |
| Export fails: "Workflow session not found" | The `session_id` doesn't match any workflow session — run `workflow list` |
| Generated server has 0 tools | Workflow had no capturable HTTP calls — re-record navigating through the full flow |
| Export reports `NEEDS_SECRET <VAR>` | Set `<VAR>=<value>` in `noui/.env`, then re-run `--verify` or `mcp verify <server_id>` |
| Path A/B: auth errors at runtime | Run `mcp diagnose-auth <server_id>` — shows strategy, missing env vars, and repair steps |
| Path A: Tabby returns empty credentials | Profile not HEALTHY — run `login validate` and `tabby session ensure` |
| `workbench/mcp_servers/` empty after export | Check `.noui-backend.log` in the repo root for compiler errors |
| Tools have unreadable raw API param names (`f_sid`, `bl`, `reqid`) | Run `/noui-generalize` |
| `API.md` missing from the generated folder | Run `.venv/bin/python cli/main.py mcp docs <server_id>` to generate it |
| `API.md` is stale after editing `tools.json` | Run `.venv/bin/python cli/main.py mcp docs <server_id>` to refresh |
| Capture session not linked to workflow (different project_id) | User created a new App in the extension instead of selecting the one created by `workflow record`. Re-record using the correct App. |
| Extension doesn't show the App created by CLI | Click refresh in the extension popup, or close and reopen it. The backend creates the App immediately on `workflow record`. |
| `workflow captures` returns empty after recording | The extension may not have been connected to `localhost:8002`. Check that the extension shows "Connected" status and the backend is running. |
