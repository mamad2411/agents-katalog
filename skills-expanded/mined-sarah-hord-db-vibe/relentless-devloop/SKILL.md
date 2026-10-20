---
name: relentless-devloop
description: Run the app and test it with Chrome DevTools MCP as a headless browser. Navigates routes, clicks elements, fills forms, captures screenshots, checks console/network errors. Returns structured pass/fail results. Usable standalone or delegated from validator/implementer.
user-invocable: true
---

# Dev Loop Tester

Start the app and test it using Chrome DevTools MCP as a programmatic headless browser. Navigate routes, interact with UI elements, capture evidence, and return structured results.

**Announce at start:** "Starting dev loop test."

## When to Use This

| Context | How it's used |
|---------|--------------|
| **Standalone** (`/relentless-devloop`) | User wants to smoke-test an app — "does this actually work?" |
| **From validator** | Validator delegates frontend testing here instead of inlining Chrome DevTools calls |
| **From implementer** | Quick smoke test during development — "did my change break the UI?" |
| **From orchestrator** | Ad-hoc check between phases |

## Role Boundaries

| This agent DOES | This agent DOES NOT |
|----------------|---------------------|
| Start the app (local or deployed) | Write or fix code |
| Navigate to routes | Judge whether errors are acceptable |
| Click buttons, fill forms, select options | Make decisions about what to fix |
| Take screenshots as evidence | Run unit/integration tests |
| Capture console errors and network failures | Modify config or environment |
| Return structured test results | Decide pipeline flow (orchestrator's job) |

## Inputs

The devloop tester accepts a **test plan** — either explicit (from the caller) or inferred (from the project).

### Explicit test plan (from caller)

When invoked by the validator or orchestrator, the caller provides specific routes and interactions:

```
Test plan:
- Navigate to /estimates/1/demand-plan → screenshot, check console
- Click "Add Row" button → verify new row appears
- Fill "Product Name" with "Test Product" → submit form → check for 200 response
- Navigate to /settings → screenshot, check for 403
```

### Inferred test plan (standalone invocation)

When invoked directly by the user with no plan, infer from:

1. **`_relentless_config.json`** → `backend.port`, `frontend.port`, `stack`
2. **PRD** → `validation_surfaces` from Agent Handoff
3. **Project structure** → scan for route definitions:
   ```bash
   # React routes
   grep -r "path=" frontend/src/ --include="*.tsx" --include="*.jsx" 2>/dev/null | head -20
   # FastAPI routes
   grep -r "@app\.\|@router\." backend/ --include="*.py" 2>/dev/null | head -20
   ```
4. **Fallback** → hit the root route (`/`) and any `/api/` health endpoints

## Process

### Step 0: Read config and resolve targets

```bash
cat _relentless_config.json 2>/dev/null || echo "NO_CONFIG"
```

Determine:
- **Backend URL**: from config `backend.port` or default `http://localhost:8000`
- **Frontend URL**: from config `frontend.port` or default `http://localhost:5173`
- **Stack**: `backend`, `frontend`, or `fullstack`
- **Deployed app URL**: from config `databricks.app_name` → resolve via `databricks apps get`

### Step 1: Ensure app is running

#### Local app

```bash
# Check backend
curl -sf http://localhost:${BACKEND_PORT}/docs 2>/dev/null | head -1
# Check frontend
curl -sf http://localhost:${FRONTEND_PORT}/ 2>/dev/null | head -1
```

If not running, start it:

```bash
# Backend
cd backend && uv run uvicorn app.main:app --reload --port ${BACKEND_PORT} &
BACKEND_PID=$!

# Frontend (if fullstack)
cd frontend && npm run dev -- --port ${FRONTEND_PORT} &
FRONTEND_PID=$!

# Wait for startup
sleep 5

# Verify
curl -sf http://localhost:${BACKEND_PORT}/docs > /dev/null && echo "Backend up" || echo "Backend FAILED"
curl -sf http://localhost:${FRONTEND_PORT}/ > /dev/null && echo "Frontend up" || echo "Frontend FAILED"
```

Record PIDs so we can clean up in Step 5.

#### Deployed Databricks app

```bash
databricks apps get ${APP_NAME} --profile ${PROFILE} 2>/dev/null | grep -i "url\|status"
```

Use the app URL directly — no need to start anything.

### Step 2: Backend smoke tests (if backend in stack)

Before touching the browser, hit API endpoints with curl to verify the backend is healthy:

```bash
# Health check
curl -sf http://localhost:${BACKEND_PORT}/api/v1/debug/database 2>&1 | jq .

# OpenAPI spec available
curl -sf http://localhost:${BACKEND_PORT}/openapi.json 2>&1 | jq '.paths | keys[]' | head -20

# Hit each endpoint from test plan (or discovered routes)
curl -sf http://localhost:${BACKEND_PORT}/api/v1/<endpoint> \
  -H "Content-Type: application/json" \
  -H "X-Forwarded-Email: test@example.com" \
  2>&1 | jq .
```

Record for each endpoint:
- URL, method
- HTTP status (expected vs actual)
- Response time
- Response shape (fields present?)
- Error in response body?

### Step 3: Frontend browser testing (if frontend in stack)

This is the core of the devloop — programmatic browser interaction via Chrome DevTools MCP.

#### 3a. Navigate and baseline

For each route in the test plan:

1. **Navigate:**
   ```
   navigate_page → url: "http://localhost:${FRONTEND_PORT}<route>"
   ```

2. **Wait for load:**
   ```
   wait_for → selector: "body", timeout: 10000
   ```

3. **Screenshot:**
   ```
   take_screenshot
   ```
   Save the screenshot path. This is evidence — visual proof the route rendered.

4. **Console check:**
   ```
   list_console_messages
   ```
   Filter for `level: "error"`. Record all errors.

5. **Network check:**
   ```
   list_network_requests
   ```
   Filter for `status >= 400`. Record failed requests with URL, status, response.

#### 3b. Interactive testing

For each interaction in the test plan:

**Click:**
```
click → selector: "button[data-testid='add-row']"
```
Then: `take_screenshot` + `list_console_messages` (check for new errors after interaction).

**Fill form:**
```
fill → selector: "input[name='product_name']", value: "Test Product"
```
Then: `take_screenshot`.

**Submit:**
```
click → selector: "button[type='submit']"
```
Then: `wait_for` network idle, `list_network_requests` (check for the POST/PUT), `take_screenshot`, `list_console_messages`.

**Select dropdown:**
```
fill → selector: "select[name='tier']", value: "Growth"
```
Then: `take_screenshot` + verify dependent UI updated.

#### 3c. Multi-step flows

For complex user flows (e.g., "create an estimate, add line items, submit"):

1. Execute each step sequentially
2. Screenshot after each step (evidence trail)
3. Check console after each step (catch errors early)
4. If any step fails (element not found, console error), record which step and continue remaining steps

#### 3d. Responsive check (optional)

If the test plan mentions responsive testing:

```
resize_page → width: 375, height: 812  # iPhone viewport
take_screenshot
resize_page → width: 1920, height: 1080  # Desktop
take_screenshot
```

### Step 4: Compile results

Collect all findings into a structured result:

```json
{
  "tested_at": "<ISO timestamp>",
  "app_url": "http://localhost:5173",
  "stack": "fullstack",
  "backend": {
    "healthy": true,
    "endpoints_tested": 5,
    "endpoints_failed": 1,
    "failures": [
      {
        "url": "/api/v1/estimates/1/demand",
        "method": "GET",
        "expected_status": 200,
        "actual_status": 500,
        "error": "Internal Server Error",
        "response_time_ms": 245
      }
    ]
  },
  "frontend": {
    "routes_tested": 3,
    "routes_with_errors": 1,
    "console_errors": [
      {
        "route": "/estimates/1/demand-plan",
        "level": "error",
        "message": "TypeError: Cannot read properties of undefined (reading 'map')",
        "source": "DemandPlanTable.tsx:47"
      }
    ],
    "network_failures": [
      {
        "route": "/estimates/1/demand-plan",
        "url": "/api/v1/estimates/1/demand",
        "method": "GET",
        "status": 500
      }
    ],
    "interactions": [
      {
        "action": "click 'Add Row'",
        "result": "pass",
        "screenshot": "/tmp/devloop_addrow.png"
      },
      {
        "action": "fill 'Product Name' → submit",
        "result": "fail",
        "error": "Network request POST /api/v1/line-items returned 422",
        "screenshot": "/tmp/devloop_submit_fail.png"
      }
    ]
  },
  "screenshots": [
    {"route": "/", "path": "/tmp/devloop_home.png"},
    {"route": "/estimates/1/demand-plan", "path": "/tmp/devloop_demand.png"},
    {"route": "/settings", "path": "/tmp/devloop_settings.png"}
  ],
  "summary": {
    "total_checks": 12,
    "passed": 9,
    "failed": 3,
    "clean": false
  }
}
```

### Step 5: Cleanup

If the devloop started the app processes:

```bash
# Kill backend/frontend if we started them
kill $BACKEND_PID 2>/dev/null
kill $FRONTEND_PID 2>/dev/null
```

If the app was already running before devloop, leave it running.

### Step 6: Report

Present human-readable results:

```
## Dev Loop Results

### Backend API
- [x] Health check: healthy
- [x] GET /api/v1/estimates: 200 OK (120ms)
- [x] GET /api/v1/estimates/1: 200 OK (85ms)
- [ ] GET /api/v1/estimates/1/demand: 500 Internal Server Error (245ms)
- [x] POST /api/v1/line-items: 201 Created (190ms)

### Frontend Routes
| Route | Rendered | Console Errors | Network Errors | Screenshot |
|-------|----------|---------------|----------------|------------|
| `/` | Yes | 0 | 0 | devloop_home.png |
| `/estimates/1/demand-plan` | Yes | 1 error | 1 failed request | devloop_demand.png |
| `/settings` | Yes | 0 | 0 | devloop_settings.png |

### Interactions
| Action | Result | Evidence |
|--------|--------|----------|
| Click "Add Row" | PASS | devloop_addrow.png |
| Fill "Product Name" → Submit | FAIL: 422 from API | devloop_submit_fail.png |

### Summary
9/12 checks passed. 3 failures detected.
```

If invoked by the validator, return the structured JSON (Step 4 output) — the validator will incorporate it into `_validation_report.json`.

If invoked standalone, present the human-readable report (Step 6).

## Selector Strategies

When the test plan doesn't specify exact selectors, use this priority:

1. **`data-testid`** — Most reliable: `[data-testid="add-row-btn"]`
2. **ARIA labels** — Accessible: `[aria-label="Add Row"]`
3. **Semantic HTML** — `button`, `a[href]`, `input[name]`, `select[name]`
4. **Text content** — Last resort: find element by visible text
5. **CSS class** — Fragile but sometimes necessary: `.btn-primary`

If an element can't be found:
- Take a screenshot to see current state
- Try alternative selectors
- Report as "element not found" with screenshot evidence — don't guess

## Integration with Other Skills

### Validator → Devloop

The validator invokes devloop for frontend testing instead of making Chrome DevTools calls directly:

```
Run /relentless-devloop with this test plan:
- Navigate to /estimates/1/demand-plan → check console, network
- Navigate to /settings → check for auth errors
- Click "Export CSV" → verify download initiates

Return structured JSON results.
```

The validator then maps devloop failures to its error report format (`_validation_report.json`).

### Implementer → Devloop

The implementer can invoke devloop for quick smoke tests during development:

```
Run /relentless-devloop — just hit the root route and check for console errors.
I just changed DemandPlanTable.tsx and want to see if it renders.
```

This is optional — the implementer doesn't need to validate (that's the validator's job), but a quick smoke test can catch obvious breakage early.

## Design Principles

### Screenshots are the ground truth

Every navigation and interaction produces a screenshot. These are evidence — they prove what the app actually looked like, not what we think it should look like. When in doubt, take another screenshot.

### Test the app like a user would

Navigate routes, click buttons, fill forms, submit data. Don't test internal state or component props. If a user would see an error, the devloop should catch it. If a user wouldn't notice, it's not a devloop concern.

### Fail loud, fail specific

"Console error on /demand-plan" is useful. "Something went wrong" is not. Every failure includes: where (route/endpoint), what (error message), and evidence (screenshot/response body).

### Cleanup after yourself

If the devloop started app processes, it kills them when done. Leave the environment as you found it.

### Chrome DevTools MCP is the browser

No Selenium, no Puppeteer, no Playwright installation needed. Chrome DevTools MCP provides all the primitives: navigate, click, fill, screenshot, console, network. It's already available in the Claude Code environment via MCP servers.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Chrome DevTools MCP not available | Check MCP server config in `mcp-servers.yaml`. Fall back to curl for backend-only testing |
| App won't start | Check port conflicts (`lsof -ti:8000`), missing deps, env vars |
| Element not found | Take screenshot to see actual DOM. Try alternative selectors. Check if route requires auth |
| Screenshot is blank | App may not have loaded. Add `wait_for` with longer timeout |
| Network requests show CORS errors | Backend CORS config doesn't include frontend origin. Report as config error |
| Form submission returns 422 | Check required fields. The test data may be missing required values |
| Route returns 404 | Check if route exists in app. May need auth token or different base path |
| Slow interactions | App may be loading data. Increase `wait_for` timeouts. Check network for pending requests |
