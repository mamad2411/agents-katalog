---
name: relentless-validate
description: Pure QA agent. Runs live execution validation after TDD gates pass. Uses Chrome DevTools (frontend) and Databricks CLI (backend) to detect integration failures. Reports structured errors — never writes code fixes.
user-invocable: true
---

# Live Execution Validator (QA Agent)

Run live execution validation after TDD gate tests pass. This agent **detects and reports** errors — it never writes code fixes. The orchestrator dispatches a separate remediator agent for fixes.

**Announce at start:** "Running live execution validation."

## Pipeline Position

```
relentless-prd → prd_<slug>.md
    ↓
relentless-gates → failing gate tests + _gates.json
    ↓
relentless-implement → makes gate tests pass (Implementer Agent)
    ↓
relentless-validate → live execution + error capture (THIS SKILL — Validator Agent)
    ↓
relentless-orchestrate → dispatches remediator if errors found, re-validates
```

## Role Boundaries

| This agent DOES | This agent DOES NOT |
|----------------|-------------------|
| Start the app (local/deployed) | Write or edit source code |
| Hit API endpoints, check responses | Fix bugs or config issues |
| Open browser routes via Chrome DevTools | Apply patches or remediation |
| Capture console errors, network failures | Judge whether errors are "acceptable" |
| Read Databricks CLI logs | Re-run TDD gate tests |
| Categorize errors by type | Decide to stop the pipeline |
| Produce structured error report | Self-certify "PASS" without evidence |

**The validator is a pure observer.** It runs things, records what happens, and hands a structured report to the orchestrator. The orchestrator decides what to do next.

## Why This Exists

TDD gates catch logic errors. They do NOT catch:
- **Config errors**: Wrong env var, missing secret, bad connection string
- **Permission errors**: Service principal can't access catalog, CORS blocks request
- **Integration errors**: API returns different shape in prod, WebSocket handshake fails
- **Runtime errors**: Memory limits, timeout on real data volumes, race conditions
- **Frontend rendering**: Component crashes on mount, console errors, network failures

## Process

### Step 0: Pre-check

1. Confirm TDD gates passed: read `_gates.json` and verify all machine gates show `status: "passed"` (or run the gate command to check)

2. **Read `_relentless_config.json`** (if present) for resolved environment config:
   ```bash
   cat _relentless_config.json 2>/dev/null || echo "NO_CONFIG"
   ```
   If present, extract: `databricks.profile`, `backend.port`, `frontend.port`, `databricks.app_name`, `stack`. These values are authoritative — use them instead of inferring.

3. Read the PRD's Agent Handoff JSON to find `validation_surfaces` and `log_commands`
4. If no `validation_surfaces` in the handoff, tell the user: "PRD has no validation surfaces defined. I'll infer from the stack." Then determine surfaces from `stack` field (from config or PRD):
   - `backend` or `fullstack` → Databricks CLI + curl
   - `frontend` or `fullstack` → Chrome DevTools
   - `backend` only → skip browser validation
5. **Resolve the Databricks CLI profile** — priority order:
   - `_relentless_config.json` → `databricks.profile` (highest priority — pre-flight validated it)
   - Orchestrator passed a profile in the subagent prompt → use it
   - `_orchestration_state.md` → `## Environment` → `Databricks Profile`
   - `databricks.yml` / `bundle.yml` in the project for a profile reference
   - **If none found, ask the user:** "Which Databricks CLI profile should I use? (Run `grep '^\[' ~/.databrickscfg` to see available profiles)"
   - **NEVER default to `--profile default`** — using the wrong profile means validating against the wrong workspace
6. **Resolve ports** from `_relentless_config.json` → `backend.port` / `frontend.port`, or fall back to defaults (8000 / 5173)

### Step 1: Start the App (if needed)

Check if the app is already running:

```bash
# Local dev
curl -s http://localhost:8000/api/v1/debug/database 2>/dev/null | head -1
# Or check Databricks app (use the resolved profile from Step 0)
databricks apps get <app-name> --profile <RESOLVED_PROFILE> 2>/dev/null | grep -i status
```

If not running and `validation_surfaces` includes local URLs:

```bash
# Start backend
cd backend && uv run uvicorn app.main:app --reload --port 8000 &
# Start frontend (if fullstack)
cd frontend && npm run dev &
# Wait for startup
sleep 5
```

If validation targets a deployed Databricks app, ensure it's deployed:

```bash
make ship  # or whatever the deploy command is
make bundle-run
```

### Step 2: Backend Validation

For each backend validation surface defined in the PRD (or inferred):

#### 2a. Health & Smoke Tests

```bash
# Basic health
curl -sf http://localhost:8000/api/v1/debug/database | jq .status

# Smoke test from PRD
# (read verify.smoke_test from Agent Handoff)
```

#### 2b. API Endpoint Validation

For each API endpoint changed by the implementation:

```bash
# Hit the endpoint with realistic data
curl -sf http://localhost:8000/api/v1/<endpoint> \
  -H "X-Forwarded-Email: test@example.com" \
  | jq .
```

Check and record:
- HTTP status code (expected vs actual)
- Response shape (expected fields present?)
- Error fields in response body
- Response time

#### 2c. Databricks CLI Validation (deployed apps)

If the app is deployed to Databricks:

```bash
# Check app status
databricks apps get <app-name> --profile <profile>

# Tail recent logs for errors
databricks apps logs <app-name> --profile <profile> 2>&1 | tail -50

# Check for startup errors
databricks apps logs <app-name> --profile <profile> 2>&1 | grep -i "error\|exception\|traceback"

# Validate bundle config
databricks bundle validate --profile <profile>
```

Parse logs for error patterns:
- `ImportError` / `ModuleNotFoundError` → category: `runtime`
- `PermissionDenied` / `403` → category: `permission`
- `ConnectionRefused` / `timeout` → category: `config`
- `sqlalchemy.exc.*` → category: `runtime`

#### 2d. Database Validation

If the feature touches database schema:

```bash
# Check migrations ran
curl -sf http://localhost:8000/api/v1/debug/database | jq .

# Verify new tables/columns exist (via app endpoint or direct query)
```

### Step 3: Frontend Validation (via devloop)

If `validation_surfaces` includes frontend or stack is `fullstack`, delegate to `/relentless-devloop`:

#### 3a. Build the test plan

From the PRD's `validation_surfaces` and any specific user flows, build a test plan for the devloop:

```
Run /relentless-devloop with this test plan:
- Navigate to <each frontend route from validation_surfaces> → check console, network
- <any interactive flows from PRD ACs — clicks, form fills, submissions>
Return structured JSON results.
```

Include the frontend port from `_relentless_config.json` (or default 5173).

#### 3b. Parse devloop results

The devloop returns structured JSON with:
- `frontend.console_errors` — map to error entries with `surface: "frontend_console"`
- `frontend.network_failures` — map to error entries with `surface: "frontend_network"`
- `frontend.interactions` — check for `result: "fail"` entries
- `screenshots` — include paths in the validation report

#### 3c. Categorize frontend errors

Map devloop findings to validation error categories:

| Devloop finding | Validation category |
|----------------|-------------------|
| Console: "Cannot read property", "Uncaught TypeError" | `runtime` |
| Console: "Failed to fetch", "ERR_CONNECTION_REFUSED" | `config` |
| Console: "Loading chunk X failed" | `runtime` |
| Console: "Access-Control-Allow-Origin" | `config` |
| Network: 401 | `auth` |
| Network: 403 | `permission` |
| Network: 404 | `config` |
| Network: 500 | `runtime` |
| Interaction failed: element not found | `runtime` |
| Interaction failed: network error after submit | `integration` |

#### 3d. If devloop is unavailable

Fall back to direct Chrome DevTools MCP calls:

1. `navigate_page` to each route
2. `take_screenshot` — visual sanity check
3. `list_console_messages` — filter for `level: "error"`
4. `list_network_requests` — filter for `status >= 400`
5. `click` / `fill` for interactive flows

### Step 4: Error Triage

Collect ALL errors from Steps 2-3 into a structured error report. For each error, assign:

| Field | Description |
|-------|-------------|
| `id` | Sequential error number (E-1, E-2, ...) |
| `category` | `config` \| `runtime` \| `permission` \| `auth` \| `integration` \| `timeout` \| `infrastructure` |
| `surface` | Where it was detected: `backend_api`, `frontend_console`, `frontend_network`, `databricks_logs`, `database` |
| `message` | The actual error message |
| `source_file` | Best guess at which file caused it (from stack trace if available) |
| `auto_fixable` | `true` for config/runtime, `false` for permission/auth/infrastructure, `maybe` for integration/timeout |
| `suggested_fix` | What the remediator should try (specific, actionable) |

**Error triage table:**

| Category | Auto-fixable | Typical Fix |
|----------|-------------|-------------|
| **config** | Yes | Fix env var, connection string, config file, CORS origin |
| **runtime** | Yes | Null check, type error, missing import, schema mismatch |
| **permission** | No | Needs SP config, IAM change, catalog grant |
| **auth** | No | Needs credential setup, token refresh |
| **integration** | Maybe | API contract change (code-side fix) or external dependency (escalate) |
| **timeout** | Maybe | Query optimization (code-side) or resource limit (escalate) |
| **infrastructure** | No | Needs deployment config, compute scaling, network setup |

### Step 5: Write Validation Report

Write the report to `_validation_report.json` in the project root:

```json
{
  "prd_file": "prd_<slug>.md",
  "validated_at": "<ISO timestamp>",
  "tdd_gates_status": "all_passed",
  "surfaces_tested": {
    "backend_api": {"tested": true, "endpoints": 5, "errors": 1},
    "frontend_browser": {"tested": true, "routes": 3, "errors": 0},
    "databricks_cli": {"tested": false, "reason": "not deployed"},
    "database": {"tested": true, "errors": 0}
  },
  "errors": [
    {
      "id": "E-1",
      "category": "runtime",
      "surface": "frontend_console",
      "message": "TypeError: Cannot read properties of undefined (reading 'map')",
      "source_file": "frontend/src/components/DemandPlanTable.tsx",
      "auto_fixable": true,
      "suggested_fix": "Add null check for monthly_data before .map() call"
    },
    {
      "id": "E-2",
      "category": "permission",
      "surface": "databricks_logs",
      "message": "PermissionDenied: SP cannot access lakemeter_catalog",
      "source_file": null,
      "auto_fixable": false,
      "suggested_fix": "Grant SP lakemeter-sp USE CATALOG on lakemeter_catalog"
    }
  ],
  "screenshots": [
    {"route": "/estimates/1/demand-plan", "path": "/tmp/screenshot_demand_plan.png"}
  ],
  "summary": {
    "total_errors": 2,
    "auto_fixable": 1,
    "needs_escalation": 1,
    "clean": false
  }
}
```

### Step 6: Report to User/Orchestrator

Present the human-readable summary:

```
## Validation Report: prd_<slug>.md

### Surfaces Tested
- [x] Backend API (localhost:8000): 5 endpoints, 1 error
- [x] Frontend (localhost:5173): 3 routes, 0 errors
- [ ] Databricks App: not deployed (skipped)
- [x] Database: migrations verified

### Errors Found
| # | Category | Surface | Error | Auto-fixable |
|---|----------|---------|-------|-------------|
| E-1 | runtime | Frontend console | TypeError: Cannot read 'map' of undefined | Yes |
| E-2 | permission | Databricks logs | SP cannot access catalog | No — escalate |

### Verdict
- 1 auto-fixable error → remediator can patch
- 1 permission error → requires human action
- Report written to: _validation_report.json

### Next Steps (for orchestrator)
- Dispatch remediator for E-1
- Escalate E-2 to user
- Re-validate after remediation
```

If zero errors:

```
## Validation Report: prd_<slug>.md

All surfaces clean. Zero errors detected.
- Backend API: 5/5 endpoints healthy
- Frontend: 0 console errors, 0 failed requests
- Database: migrations verified

Verdict: PASS — ready for production.
```

## Design Principles

### Fresh context, complete observation

The validator runs in a fresh subagent context (dispatched by the orchestrator). It receives: the PRD's validation surfaces, the progress summary, and nothing else. No accumulated state from the implementer or prior validation runs. This ensures each validation is independent and unbiased.

### Validator never writes code

This is the core separation of concerns. The implementer builds, the validator tests, the remediator patches. If the validator also fixed code, it would be judging its own fixes — the same self-reinforcing error pattern that TDD gates were designed to prevent.

### Structured output enables the loop

`_validation_report.json` is the validator's `finish()` artifact — the durable handoff to the next phase. The orchestrator reads this file (not the validator's conversation) to decide: dispatch remediator, escalate to human, or mark complete. This follows the RelentlessAgent principle: artifacts on disk are the only thing that survives between phases.

### Error categories drive decisions

The triage table is deterministic. `config` and `runtime` → auto-fix. `permission` and `auth` → always escalate. This prevents the agent from wasting loops on unfixable problems.

### Screenshots are evidence

Every frontend validation captures screenshots. They serve as:
- Proof of rendering (visual QA for manual ACs)
- Debug context for errors (what was on screen when it broke)
- Before/after evidence for remediation fixes

### Validation is idempotent

Running the validator twice produces the same report (assuming no code changes between runs). This makes it safe for the orchestrator to re-run after remediation without side effects. Same input → same output — no hidden state.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| App not running | Start with `make dev-backend` / `make dev-frontend` or `make bundle-run` |
| Chrome DevTools MCP not available | Check MCP server config; fall back to curl + manual browser check |
| Databricks CLI not configured | Run `databricks configure`; check `~/.databrickscfg` for profile |
| No `validation_surfaces` in PRD | Infer from `stack` field; validate basic health + smoke test only |
| Frontend route requires auth | Use `X-Forwarded-Email` header or `LOCAL_DEV_EMAIL` env var |
| Validator reports error that isn't real | Check if error is transient (race condition on startup); re-run once to confirm |
