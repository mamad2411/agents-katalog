---
name: ironbee-browser-devtools-cli
description: Automates browser interactions using Playwright for web testing, debugging, and automation. Use when the user needs to navigate websites, take screenshots, fill forms, click elements, extract page content (HTML/text), audit accessibility (ARIA/AX tree), measure Web Vitals performance, monitor console logs and HTTP requests, mock API responses, execute JavaScript in browser, inspect React components, compare UI with Figma designs, manage reusable scenarios, or perform non-blocking debugging with tracepoints, logpoints, and exception monitoring. Also covers the creds-gated Jira and Linear issue-tracker domains: fetch/search issues, download attachments, attach evidence, comment, transition/set state, and report verification results back to the tracker.
allowed-tools: Bash(ironbee-browser-devtools-cli:*), Bash(ironbee-devtools-cli:*)
---

# IronBee Browser DevTools CLI

Command-line interface for browser automation, debugging, and testing using Playwright. Part of [IronBee DevTools](https://github.com/ironbee-ai/ironbee-devtools). This CLI targets the **browser platform**; for Node.js backend debugging see `ironbee-node-devtools-cli`, and for HTTP/gRPC/GraphQL/WS + log + database verification see `ironbee-backend-devtools-cli`.

`ironbee-browser-devtools-cli` and `ironbee-devtools-cli` are aliases — both ship with the same package and target the browser platform by default. Examples in this doc use `ironbee-browser-devtools-cli`; substitute `ironbee-devtools-cli` if you prefer the shorter name.

## Installation

```bash
# Install this skill (skills.sh)
npx skills add ironbee-ai/ironbee-devtools-skills

# Install the CLI binary
npm install -g @ironbee-ai/devtools
```

Requires **Node.js >= 22.16.0** (`engines.node` in the package): the backend `db` domain's SQLite engine and the `FTS5` scenario-search strategy run on Node's built-in `node:sqlite`, which replaced the last native dependency.


## Quick Start

```bash
# Navigate to a URL
ironbee-browser-devtools-cli navigation go-to --url "https://example.com"

# Take a screenshot
ironbee-browser-devtools-cli content take-screenshot --name "homepage"

# Get page content as text
ironbee-browser-devtools-cli content get-as-text
```

**Ref-based workflow** (recommended for AI agents): Call `a11y take-aria-snapshot` first to get refs (e1, e2, ...), then use refs in `interaction click --selector "e1"` or `content take-screenshot --annotate` for numbered element labels.

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port <number>` | Daemon server port | `2020` |
| `--session-id <string>` | Session ID for browser state persistence | auto |
| `--json` | Output results as JSON (recommended for AI) | `false` |
| `--quiet` | Suppress log messages | `false` |
| `--verbose` | Enable debug output | `false` |
| `--timeout <ms>` | Operation timeout | `30000` |
| `--headless` | Run browser in headless mode | `true` |
| `--no-headless` | Run browser with visible window | - |
| `--persistent` | Preserve cookies/localStorage | `false` |
| `--no-persistent` | Clear state on session end | - |
| `--user-data-dir <path>` | Browser user data directory | OS temp |
| `--use-system-browser` | Use system Chrome | `false` |
| `--browser-path <path>` | Custom browser path | auto |

**AI Agent Recommended Options:**

```bash
# JSON output for parsing, quiet mode for clean output, session for state persistence
ironbee-browser-devtools-cli --json --quiet --session-id "my-session" <command>
```

## Tool Domains

The CLI provides tools organized by domain:

| Domain | Description | Reference |
|--------|-------------|-----------|
| navigation | Page navigation (go-to, back, forward, reload) | [navigation](./references/navigation.md) |
| content | Content extraction (screenshot, PDF, HTML, text, video recording) | [content](./references/content.md) |
| interaction | User interactions (click, fill, hover, scroll) | [interaction](./references/interaction.md) |
| a11y | Accessibility snapshots (ARIA, AX tree) | [a11y](./references/a11y.md) |
| o11y | Observability (Web Vitals, console, HTTP, trace pin + reading traces back from the IronBee platform) | [o11y](./references/o11y.md) |
| debug | Non-blocking debugging (tracepoints, logpoints, exceptions) | [debug](./references/debug.md) |
| stub | HTTP mocking (intercept, mock, clear) | [stub](./references/stub.md) |
| sync | Synchronization (wait for network idle) | [sync](./references/sync.md) |
| react | React DevTools integration | [react](./references/react.md) |
| figma | Figma design comparison | [figma](./references/figma.md) |
| scenario | Reusable step-based (or legacy single-script) flows — add, update, delete, list, search, recorded-actions, run; `scenario-run` is a direct subcommand with pause/resume for `llm-action` steps | [scenario](./references/scenario.md) |
| execute | Batch JavaScript execution (run execute; CLI and MCP) | [execute](./references/execute.md) |
| jira | Jira issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [jira](./references/jira.md) |
| linear | Linear issue tracker: intake, evidence, outcome, verification report (creds-gated shared domain; writes opt-in) | [linear](./references/linear.md) |

**Jira / Linear** are platform-agnostic shared issue-tracker domains (like scenario/execute) — registered on every platform CLI, but **only when credentials are configured**: jira needs `JIRA_BASE_URL` plus `JIRA_EMAIL` + `JIRA_API_TOKEN` (Cloud) or `JIRA_PAT` (Server/DC); linear needs `LINEAR_API_KEY`. Without creds the `jira` / `linear` subcommand group does not exist. Write tools (add-comment, attach-file, create/update-issue, transition-issue / set-state, link-issue, report-verification) additionally require `JIRA_WRITE_ENABLED=true` / `LINEAR_WRITE_ENABLED=true` (default off ⇒ read-only intake tools only). Close the loop after a verification run: `ironbee-browser-devtools-cli jira report-verification --key PROJ-123 --result pass --report "..." --artifacts ./artifacts/evidence.png` (linear: same shape with `--state` instead of `--transition`). See [jira](./references/jira.md) / [linear](./references/linear.md).

**Execute** is available in both **CLI** and **MCP**. Use it to run JavaScript and batch tool calls: CLI `run execute --code "<js>"` (or `--file <path>`, optionally `--timeout-ms`); MCP tool `execute` with the same params. Inside the VM: **`page`** (browser only) — Playwright Page; use `await page.title()`, `await page.evaluate(...)`, etc. **`callTool(name, input, returnOutput?)`** — invoke any tool; **always `await`**; `name` is underscore form (e.g. `'navigation_go-to'`); `input` is an object (camelCase keys); `returnOutput: true` adds the result to the response `toolOutputs`. See [execute reference](./references/execute.md) for full bindings and args.

**Scenarios** are stored as per-scenario `<name>.json` files (plus a sibling `<name>.cache.json`) under `${WORKING_DIR}/.ironbee-devtools/scenarios/` (project) or `~/.ironbee-devtools/scenarios/` (global). A scenario is either an ordered `body.steps` list (`script` / `tool-call` / `command` / `llm-action` / `include` / `group`, optionally bracketed by `setup` / `teardown`) or a legacy single script; script steps run inside the same VM as `execute` (same `callTool` and `page` bindings, plus scenario-only `ctx` and `assert`). An `llm-action` step **pauses** the run for the agent to resolve, then caches its realization for deterministic replay. See [scenario reference](./references/scenario.md).

## CLI Management Commands

### Daemon Management

```bash
ironbee-browser-devtools-cli daemon status      # Check daemon status
ironbee-browser-devtools-cli daemon info        # Show daemon info (version, uptime, sessions)
ironbee-browser-devtools-cli daemon start       # Start daemon
ironbee-browser-devtools-cli daemon stop        # Stop daemon
ironbee-browser-devtools-cli daemon restart     # Restart daemon
```

### Session Management

```bash
ironbee-browser-devtools-cli session list                  # List active sessions
ironbee-browser-devtools-cli session info <session-id>     # Show session details
ironbee-browser-devtools-cli session delete <session-id>   # Delete a session
```

### Tool Discovery

```bash
ironbee-browser-devtools-cli tools list              # List all available tools
ironbee-browser-devtools-cli tools search <query>    # Search tools by name or description
ironbee-browser-devtools-cli tools info <tool-name>  # Show tool details and parameters
```

### Configuration

```bash
ironbee-browser-devtools-cli config    # Show current configuration
```

### Updates

```bash
ironbee-browser-devtools-cli update --check   # Check for updates
ironbee-browser-devtools-cli update           # Check and install updates
```

## Examples

### Basic Navigation and Screenshot

```bash
# Navigate to URL
ironbee-browser-devtools-cli navigation go-to --url "https://example.com"

# Take screenshot
ironbee-browser-devtools-cli content take-screenshot --name "homepage"

# Get page text
ironbee-browser-devtools-cli content get-as-text
```

### Form Automation

```bash
# Use same session for state persistence
SESSION="--session-id login-test"

# Navigate to login page
ironbee-browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com/login"

# Fill form fields
ironbee-browser-devtools-cli $SESSION interaction fill --selector "#email" --value "user@example.com"
ironbee-browser-devtools-cli $SESSION interaction fill --selector "#password" --value "password123"

# Submit form
ironbee-browser-devtools-cli $SESSION interaction click --selector "button[type=submit]"

# Wait for navigation
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle

# Capture result
ironbee-browser-devtools-cli $SESSION content take-screenshot --name "dashboard"
```

### Performance Analysis

```bash
# Navigate
ironbee-browser-devtools-cli navigation go-to --url "https://example.com"

# Get Web Vitals metrics
ironbee-browser-devtools-cli --json o11y get-web-vitals

# Check console for errors
ironbee-browser-devtools-cli --json o11y get-console-messages --type warning

# Analyze HTTP requests
ironbee-browser-devtools-cli --json o11y get-http-requests
```

### Accessibility Audit

```bash
# Navigate
ironbee-browser-devtools-cli navigation go-to --url "https://example.com"

# Get ARIA snapshot
ironbee-browser-devtools-cli a11y take-aria-snapshot

# Get detailed AX tree
ironbee-browser-devtools-cli --json a11y take-ax-tree-snapshot --roles button,link,textbox
```

### Batch Execution (execute)

```bash
# Run JavaScript in session VM (page + callTool available)
ironbee-browser-devtools-cli run execute --code "return await page.title();"

# Batch multiple tools in one call (fewer round-trips)
ironbee-browser-devtools-cli run execute --code "await callTool('a11y_take-aria-snapshot', {}, true); await callTool('content_take-screenshot', {}, true);"

# Run script body from a file (mutually exclusive with --code)
ironbee-browser-devtools-cli run execute --file ./scripts/login-flow.js
```

### Scenarios (reusable JS)

The scenario tools are platform-agnostic shared tools — their CLI commands live under the auto-generated `default` group (they have no domain prefix in their tool id). The full set (the six CRUD tools + `scenario-run`) is registered on **all six platform CLIs** (browser, node, python, backend, android, terminal). A scenario is either a legacy single `--script` or an ordered `--body` of steps; it can declare an optional typed `params` contract (defaults + shallow validation applied by `scenario-run`) — see the [scenario reference](./references/scenario.md#declared-params).

```bash
# Register a scenario at the project scope
ironbee-browser-devtools-cli default scenario-add \
  --name "login-flow" \
  --description "Logs in and verifies dashboard" \
  --script "await callTool('navigation_go-to', { url: 'https://app.example.com/login' });"

# Discover available scenarios
ironbee-browser-devtools-cli default scenario-list
ironbee-browser-devtools-cli default scenario-search --query "login"

# Run a scenario directly (scenario-run is a CLI subcommand on every platform)
ironbee-browser-devtools-cli default scenario-run --name login-flow

# Parameterize: --args JSON, or repeatable --param key=value (coerced to declared param types)
ironbee-browser-devtools-cli default scenario-run --name login-flow --param email=user@example.com

# Step-based: steps go in one --body JSON flag (setup/teardown are their own JSON flags)
ironbee-browser-devtools-cli default scenario-add \
  --name "checkout-smoke" \
  --description "Open the cart, check out, verify the confirmation" \
  --body '{"steps":[{"type":"tool-call","tool":"navigation_go-to","input":{"url":"{{args.baseUrl}}/cart"}},{"type":"llm-action","name":"complete-checkout","intent":"Fill the checkout form with the test card and submit it"}]}'

# An llm-action pauses the run: resolve it, see what you called, then resume + freeze the realization
ironbee-browser-devtools-cli default scenario-recorded-actions --name checkout-smoke
ironbee-browser-devtools-cli default scenario-run --name checkout-smoke --resume --cache '{"script":"await callTool(\"interaction_click\", { selector: \"#submit\" });"}'
```

Equivalent MCP tool names (all seven are MCP-registered): `scenario-add`, `scenario-update`, `scenario-delete`, `scenario-list`, `scenario-search`, `scenario-recorded-actions`, `scenario-run` (flat, no domain prefix).

### API Mocking

```bash
# Mock API response
ironbee-browser-devtools-cli stub mock-http-response \
  --pattern "**/api/users" \
  --body '[{"id": 1, "name": "Test User"}]'

# Navigate and test
ironbee-browser-devtools-cli navigation go-to --url "https://app.example.com"

# Clear mocks
ironbee-browser-devtools-cli stub clear
```

### Non-Blocking Debugging

```bash
SESSION="--session-id debug-session"

# Navigate to app
ironbee-browser-devtools-cli $SESSION navigation go-to --url "http://localhost:3000"

# Set tracepoint on a function
ironbee-browser-devtools-cli $SESSION debug put-tracepoint \
  --url-pattern "app.js" \
  --line-number 42

# Add watch expression
ironbee-browser-devtools-cli $SESSION debug add-watch --expression "this"

# Enable exception catching
ironbee-browser-devtools-cli $SESSION debug put-exceptionpoint --state uncaught

# Interact with app (triggers probes)
ironbee-browser-devtools-cli $SESSION interaction click --selector "#submit-btn"

# Get captured snapshots
ironbee-browser-devtools-cli $SESSION --json debug get-probe-snapshots
ironbee-browser-devtools-cli $SESSION --json debug get-probe-snapshots --types tracepoint,exceptionpoint
```

### Shell Script for CI/CD

```bash
#!/bin/bash
set -e

CLI="ironbee-browser-devtools-cli --json --quiet --session-id ci-test-$$"

# Navigate
$CLI navigation go-to --url "https://example.com"

# Wait for load
$CLI sync wait-for-network-idle

# Take screenshot
$CLI content take-screenshot --name "ci-test"

# Get Web Vitals
VITALS=$($CLI o11y get-web-vitals)
echo "Web Vitals: $VITALS"

# Check for console errors
ERRORS=$($CLI o11y get-console-messages --type error)
if [ "$ERRORS" != "[]" ]; then
  echo "Console errors found: $ERRORS"
  exit 1
fi

# Cleanup
$CLI session delete "ci-test-$$"
```

## Interactive Mode (Human Users)

For manual exploration, an interactive REPL mode is available:

```bash
ironbee-browser-devtools-cli interactive
ironbee-browser-devtools-cli --no-headless interactive   # With visible browser
```

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `exit`, `quit` | Exit interactive mode |
| `<domain> <tool>` | Execute a tool |

## Shell Completions

```bash
# Bash
ironbee-browser-devtools-cli completion bash
echo 'eval "$(ironbee-browser-devtools-cli completion bash)"' >> ~/.bashrc

# Zsh
ironbee-browser-devtools-cli completion zsh
echo 'eval "$(ironbee-browser-devtools-cli completion zsh)"' >> ~/.zshrc
```
