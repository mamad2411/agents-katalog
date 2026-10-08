---
name: pinchtab-dev
description: Develop and contribute to the PinchTab project. Use when working on PinchTab source code, adding features, fixing bugs, running tests, or preparing PRs. Triggers on "work on pinchtab", "pinchtab development", "contribute to pinchtab", "fix pinchtab bug", "add pinchtab feature".
---

# PinchTab Development

PinchTab is a browser control server for AI agents — Small Go binary with HTTP API.

## Project Location

Run everything from the repository root (a clone of `github.com/pinchtab/pinchtab`).

## Dev Commands

All development commands run via `./dev`:

| Command | Description |
|---------|-------------|
| `./dev build` | Build the application |
| `./dev dev` | Build & run |
| `./dev dashboard` | Hot-reload dashboard development (Vite + Go) |
| `./dev run` | Run the application |
| `./dev check` | All checks (Go + Dashboard + Plugin) |
| `./dev check go` | Go checks only |
| `./dev check dashboard` | Dashboard checks only |
| `./dev test unit` | Go unit tests |
| `./dev test dashboard` | Dashboard unit tests |
| `./dev e2e basic` | Basic suite (api + cli + infra) |
| `./dev e2e extended` | Extended suite (all extended) |
| `./dev e2e smoke` | Smoke suite |
| `./dev smoke` | Host Docker smoke checks (`--browser=chrome\|cloak\|all`) |
| `./dev e2e test "<name>"` | Run a single E2E test by `start_test` name |
| `./dev all` | check + test + e2e extended (pre-push gate) |
| `./dev binaries` | Build the full release binary matrix into dist/ |
| `./dev doctor` | Setup dev environment |

## Architecture

```
cmd/pinchtab/     CLI entry point
internal/
  bridge/         Chrome CDP communication
  handlers/       HTTP API handlers
  server/         HTTP server
  dashboard/      Embedded React dashboard
  config/         Configuration
  routes/         API route catalogue
  assets/         Embedded assets (stealth.js)
dashboard/        React dashboard source (Vite + TypeScript)
tests/e2e/        E2E runner, fixtures, scenarios/{api,cli,infra,plugin}/
```

## Workflow: New Feature or Bug Fix

1. **Create branch** from `main`:
   ```bash
   git checkout main && git pull
   git checkout -b feat/my-feature  # or fix/my-bug
   ```

2. **Make changes** — follow code patterns in existing files

3. **Run checks locally**:
   ```bash
   ./dev all          # check + test + e2e (one-shot pre-push gate)
   # …or individually:
   ./dev check        # Lint + format + typecheck
   ./dev test unit    # Go unit tests
   ./dev e2e basic    # E2E tests (Docker required)
   ```

4. **Commit** with conventional commits, usually scoped — `fix(extract): … (PIN-394)`:
   - `feat:` new feature
   - `fix:` bug fix
   - `refactor:` code change without behavior change
   - `test:` adding tests
   - `docs:` documentation
   - `chore:` maintenance

5. **Push and create PR**

## Definition of Done (PR Checklist)

### Required — Code Quality
- Error handling explicit — all errors wrapped with `%w`, no silent failures
- No regressions — verify stealth, token efficiency, session persistence
- SOLID principles — functions do one thing, testable
- No redundant comments — explain *why*, not *what*

### Required — Testing
- New/changed functionality has tests
- Docker E2E tests pass locally: `./dev e2e basic` (or `./dev all` for the full chain)
- If npm wrapper touched: `npm pack` and `npm install` work

### Required — Documentation
- README.md updated if user-facing changes
- /docs/ updated if API/architecture changed

### Required — Review
- PR description explains what + why
- Commits are atomic with good messages

## Key Files

| File | Purpose |
|------|---------|
| `internal/assets/stealth.js` | Bot detection evasion (light/medium/full levels) |
| `internal/bridge/bridge.go` | Chrome CDP bridge |
| `internal/handlers/*.go` | HTTP API endpoints |
| `dashboard/src/` | React dashboard source |
| `internal/routes/routes.go` | API route catalogue |
| `tests/e2e/scenarios/api/` | API E2E tests |
| `tests/e2e/scenarios/cli/` | CLI E2E tests |

## Testing

### Unit Tests
```bash
./dev test unit              # All Go tests
go test ./internal/handlers  # Specific package
```

### E2E Tests (requires Docker)
```bash
./dev e2e basic                 # Basic suite (api + cli + infra)
./dev e2e api                   # API basic tests
./dev e2e cli                   # CLI basic tests
./dev e2e infra                 # Infra basic tests
./dev e2e api-extended          # API extended tests (multi-instance)
./dev e2e cli-extended          # CLI extended tests
./dev e2e infra-extended        # Infra extended tests (multi-instance)
./dev e2e extended              # Full extended suite (all extended tests)
./dev smoke                     # Host Docker smoke checks (not an e2e suite)

# Run specific test file(s) with filter (second argument)
./dev e2e api clipboard                # Run only clipboard-basic.sh
./dev e2e api-extended tabs            # Run tabs-extended.sh
./dev e2e cli browser                  # Run browser-basic.sh in CLI suite

# Run a single test by its start_test name (fastest debug loop)
./dev e2e test "click with humanize: click input by ref"
./dev e2e test "scroll (down)"
./dev e2e test "low-level mouse"
```

The scenario filter is one plain substring (no regex, no `|`) matched against scenario file names, groups, tiers, helpers and tags. Requires Docker daemon running.

#### Single-test mode (`dev e2e test "<name>"`)

Use this when iterating on one specific E2E failure. The runner:

1. Greps `tests/e2e/scenarios/**/*.sh` for `start_test "...<name substring>..."`.
2. Auto-picks the suite (`api`/`cli`/`infra`/`plugin`) and `-extended` variant (or `smoke` for `*-smoke.sh`) from the matching scenario file's path.
3. Builds the images (`compose build`, then `up`) and runs, inside that scenario file, **only the `start_test`...`end_test` blocks whose name contains the substring** — the scenario preamble (helper sourcing, `FIXTURES_URL`, etc.) is preserved, every other test in the file is skipped.

Notes:
- The substring is literal (fgrep), so colons/parens/quotes in test names work without escaping.
- If several tests match, the scenario file of the first match is used and the others are printed — pass a longer/more-specific substring to disambiguate. It is not a way to run a group of tests; for a whole scenario use `go run ./tests/tools/runner e2e --suite <suite> --filter <stem>`.
- Logs stream to the terminal by default (unlike full suites which hide logs); helpful for debugging.
- Implemented by `scripts/dev-e2e.sh` → `go run ./tests/tools/runner e2e --suite … --filter <stem> --test "<name>"`, which passes `E2E_TEST_FILTER` to `tests/e2e/run.sh`.

### Dashboard Tests
```bash
./dev test dashboard  # Vitest
cd dashboard && npm test
```

## Dashboard Development

### Setup

Start hot-reload development:
```bash
./dev dashboard
```

This runs:
- Backend on `:9867`
- Vite dev server on `:5173` with hot-reload
- Dashboard at `http://localhost:5173/dashboard/`

### Development Workflow (Use PinchTab to Develop PinchTab)

**Do not assume changes worked.** Use pinchtab itself to verify changes visually:

1. **Start dev mode**:
   ```bash
   ./dev dashboard
   ```

2. **Make changes** to files in `dashboard/src/`

3. **Verify with pinchtab** — use the pinchtab skill to inspect the dashboard:
   ```bash
   # ./dev dashboard runs the backend with token "dev"
   # Navigate to the page under development
   curl -X POST http://localhost:9867/navigate -H "Authorization: Bearer dev" \
     -d '{"url":"http://localhost:5173/dashboard/settings"}'
   
   # Take a screenshot (written under the state dir; response carries "path")
   curl -H "Authorization: Bearer dev" "http://localhost:9867/screenshot?output=file"
   
   # Or get a snapshot to inspect elements
   curl -s -H "Authorization: Bearer dev" http://localhost:9867/snapshot | jq .
   ```

4. **Provide evidence** — when reporting changes, include:
   - Link to the page: `http://localhost:5173/dashboard/{page}`
   - Screenshot of the result
   - Relevant snapshot data if inspecting specific elements

### Example: Verifying a Settings Page Change

```bash
# Navigate to settings
curl -X POST http://localhost:9867/navigate -H "Authorization: Bearer dev" \
  -d '{"url":"http://localhost:5173/dashboard/settings"}'

# Screenshot the result (beyondViewport=true captures the full page)
curl -H "Authorization: Bearer dev" \
  "http://localhost:9867/screenshot?output=file&beyondViewport=true"

# Find an element by description (semantic match, not a CSS selector)
curl -X POST http://localhost:9867/find -H "Authorization: Bearer dev" \
  -d '{"query":"stealth level setting"}'
```

### Key Dashboard Pages

| Page | URL | Purpose |
|------|-----|---------|
| Monitoring | `/dashboard/monitoring` | Instance overview (`/dashboard/` redirects here) |
| Activity | `/dashboard/activity` | Activity log |
| Profiles | `/dashboard/profiles` | Browser profiles |
| Agents | `/dashboard/agents` | Agents |
| Settings | `/dashboard/settings` | Configuration |

### Dashboard Tech Stack

- React 19 + TypeScript
- Vite (build/dev)
- Tailwind CSS
- Zustand (state)
- Vitest (tests)

## Stealth Module

The stealth module (`internal/assets/stealth.js`) has three levels:

| Level | Features | Trade-offs |
|-------|----------|------------|
| `light` | webdriver, CDP markers, plugins, hardware | None — safe |
| `medium` | + userAgentData, chrome.runtime.connect, puppeteer/playwright marker cleanup | May affect error monitoring, extension messaging |
| `full` | + screen/window realism, headless-only WebGL vendor/renderer spoofing (canvas/audio/WebRTC stay native) | May break graphics-dependent sites in headless mode |

Configure in `~/.pinchtab/config.json`:
```json
{
  "instanceDefaults": {
    "stealthLevel": "medium"
  }
}
```

## Common Tasks

### Add new API endpoint
1. Create handler in `internal/handlers/`
2. Add the endpoint to `internal/routes/routes.go` and bind it in the `routeBinding` table in `internal/handlers/handlers.go`
3. Add tests in same package
4. Add E2E test in `tests/e2e/scenarios/api/`

### Modify stealth behavior
1. Edit `internal/assets/stealth.js`
2. Run `./dev build` (embeds via go:embed)
3. Test with `./dev e2e infra stealth` (infra scenarios matching `stealth`; `infra-extended stealth` for the extended ones)

### Update dashboard
1. Run `./dev dashboard` for hot-reload
2. Edit files in `dashboard/src/`
3. Run `./dev check dashboard` before commit
