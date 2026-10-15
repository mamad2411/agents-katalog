---
name: noui-setup
description: Use this skill when the user wants to set up the NoUI project for the first time, install dependencies, configure the environment, load the Chrome extension, or prepare to run any NoUI skill. Triggers on "set up NoUI", "install NoUI", "configure noui", "load the Chrome extension", "first time setup", "get NoUI running", or "I want to start using NoUI".
---

# NoUI Setup

One-time environment setup for the NoUI project. Run this before any other NoUI skill.

All commands run from the `noui/` directory (the repo root).

---

## Critical Rules (Never Violate)

- **ALWAYS** use `.venv/bin/python cli/main.py` for all CLI invocations — never the system `python` or `python3`
- **NEVER** run `pip install` individual packages — all deps are managed by `poetry install --no-root`
- **NEVER** run `pip install -e .` — the project uses `package-mode = false` in `pyproject.toml` and does not support editable installs
- **ALWAYS** copy `.env.example` to `.env` and set `ANTHROPIC_API_KEY` before running the backend
- **ALWAYS** load the extension from `noui/extension/` in Developer mode — the packed install path does not work

---

## Step 1 — Create the Virtual Environment

```bash
python3 -m venv .venv
```

Creates `.venv/` in the repo root. All subsequent commands use `.venv/bin/python`.

If `python3 --version` returns something older than 3.11, use `python3.11 -m venv .venv` or `python3.12 -m venv .venv` explicitly (both are supported; the project requires >=3.11).

---

## Step 2 — Install Dependencies

```bash
.venv/bin/python -m pip install poetry
.venv/bin/python -m poetry install --no-root
```

`--no-root` is required because `pyproject.toml` sets `package-mode = false`. All runtime deps (FastAPI, FastMCP, Anthropic SDK, SQLAlchemy, httpx, etc.) are installed into `.venv`.

**Common errors:**

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'poetry'` | Re-run the `pip install poetry` step above |
| `python3: command not found` or version < 3.11 | Install Python 3.11 or 3.12 via your OS package manager, then re-create the venv with that interpreter |
| `This build backend cannot be used in 'editable' mode` | You ran `pip install -e .` — use `poetry install --no-root` instead |

---

## Step 3 — Configure Environment Variables

```bash
cp .env.example .env
```

Open `.env` and fill in:

| Variable | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Powers the MCP compiler's LLM calls |
| `TABBY_API_HOST` | Auth flows only | Tabby endpoint (default: `http://localhost:8080`) |
| `TABBY_ADMIN_TOKEN` | Auth flows only | Admin token for provisioning Tabby profiles |
| `NOUI_PORT` | No | Backend port (default: `8002`) |

If you only need unauthenticated app support, `ANTHROPIC_API_KEY` is the only required field.

---

## Step 4 — Load the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable **Developer mode** (toggle, top-right corner)
3. Click **Load unpacked**
4. Select the `noui/extension/` directory
5. The **NoUI Workflow Recorder** icon appears in the Chrome toolbar

> If the icon does not appear, click the puzzle-piece Extensions menu and pin it.

**Verify:** Click the icon — you should see the NoUI popup with recording mode options.

---

## Step 5 — Verify the Installation

```bash
.venv/bin/python cli/main.py status
```

Expected output when the backend has not yet been started:

```
NoUI backend:
  Not reachable at http://localhost:8002
```

This confirms Python, the venv, and all imports are working. The backend not running at this point is expected.

---

## Decision Flow

```
Start
  │
  ├─ Does .venv/ exist?
  │     ├─ No  → Step 1: python3 -m venv .venv
  │     └─ Yes → skip
  │
  ├─ Are deps installed?
  │     ├─ No  → Step 2: pip install poetry + poetry install --no-root
  │     └─ Yes → skip
  │
  ├─ Does .env exist?
  │     ├─ No  → Step 3: cp .env.example .env + fill in ANTHROPIC_API_KEY
  │     └─ Yes → verify ANTHROPIC_API_KEY is set
  │
  ├─ Is Chrome extension loaded?
  │     ├─ No  → Step 4: Load unpacked from noui/extension/
  │     └─ Yes → skip
  │
  └─ Step 5: .venv/bin/python cli/main.py status
       └─ Ready → proceed to /record-login or /record-workflow
```

---

## CLI Command Reference

| Command | Purpose |
|---|---|
| `.venv/bin/python cli/main.py status` | Verify backend reachability and session counts |
| `.venv/bin/python cli/main.py start` | Start the FastAPI backend on port 8002 |
| `.venv/bin/python cli/main.py stop` | Stop the backend |
| `.venv/bin/python cli/main.py tabby status` | Check Docker Compose services and Tabby API liveness |
| `.venv/bin/python cli/main.py tabby start` | Start Docker Compose infra and Tabby API |
| `.venv/bin/python cli/main.py tabby stop [--infra]` | Stop the Tabby API (and optionally Docker Compose) |
| `.venv/bin/python cli/main.py tabby setup` | Full Tabby provisioning: agent client + ServiceProfiles + write TABBY_* to `.env` |
| `.venv/bin/python cli/main.py tabby session status` | Show browser session state for configured profiles |
| `.venv/bin/python cli/main.py tabby session ensure` | Ensure a HEALTHY browser session exists |
| `.venv/bin/python cli/main.py tabby session stop` | Stop the locally-running worker |

> **Tabby setup** — for authenticated app workflows, run `tabby start` then `tabby setup` (interactive) to provision agent credentials and ServiceProfiles. This writes `TABBY_CLIENT_ID`, `TABBY_CLIENT_SECRET`, and `TABBY_API_URL` to `.env`. You still need `TABBY_ADMIN_TOKEN` (or `ADMIN_BOOTSTRAP_EMAIL`/`ADMIN_BOOTSTRAP_PASSWORD` in `tabby/.env.local`) for the provisioning step.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ImportError` or `ModuleNotFoundError` on `cli/main.py` | Deps not installed — re-run `poetry install --no-root` |
| `.env not found` error from backend | Run `cp .env.example .env` from the `noui/` directory |
| Extension shows "Manifest file is missing" | Confirm you selected `noui/extension/` (the dir containing `manifest.json`) |
| Extension loads but popup is blank | Check `chrome://extensions/` for errors; remove and re-load unpacked |
| Port 8002 already in use on start | `lsof -i :8002` to find conflicting process; set `NOUI_PORT=8003` in `.env` to use another port |
| Generated tool raises "No Tabby page matching ..." | Open the target site in the Tabby browser, or `tabby session ensure --profile <slug>` |
| Generated tool raises `Connection refused` on port 9222 | Tabby's CDP endpoint is down — `tabby session ensure --profile <slug>` |
