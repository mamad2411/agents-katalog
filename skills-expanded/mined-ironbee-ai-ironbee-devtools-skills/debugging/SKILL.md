---
name: debugging
description: Debug web, Node.js, and Python applications using console inspection, network analysis, and non-blocking code debugging. Use when the user reports bugs, wants to debug JavaScript (browser or backend) or a running Python process, inspect network requests, troubleshoot page/API issues, trace function calls, monitor exceptions, or diagnose Python deadlocks/hung threads.
allowed-tools: Bash(ironbee-browser-devtools-cli:*), Bash(ironbee-node-devtools-cli:*), Bash(ironbee-python-devtools-cli:*)
---

# Debugging Skill

Debug web applications, Node.js backends, and running Python processes using console inspection, network analysis, and non-blocking code debugging with tracepoints, logpoints, and exception monitoring.

## When to Use

This skill activates when:
- User reports a bug or error on a web page or backend
- User asks to debug JavaScript (frontend or Node.js) or Python (a running process)
- User wants to inspect API calls or network requests
- User needs to troubleshoot page loading or API handler issues
- User mentions console errors or warnings
- User wants to debug without breakpoints
- User needs to trace function calls or monitor variables
- User needs to diagnose a Python deadlock, GIL contention, or hung threads

## Capabilities

### Console Inspection
```bash
ironbee-browser-devtools-cli o11y get-console-messages
ironbee-browser-devtools-cli o11y get-console-messages --type warning
ironbee-browser-devtools-cli --json o11y get-console-messages --type error
```

### Network Analysis
```bash
ironbee-browser-devtools-cli o11y get-http-requests
ironbee-browser-devtools-cli --json o11y get-http-requests --resource-type fetch
ironbee-browser-devtools-cli --json o11y get-http-requests --status '{"min":400}'
```

### Tracepoints (Non-Blocking)
```bash
ironbee-browser-devtools-cli debug put-tracepoint --url-pattern "app.js" --line-number 42
ironbee-browser-devtools-cli debug list-probes --types tracepoint
ironbee-browser-devtools-cli debug remove-probe --type tracepoint --id <probe-id>
ironbee-browser-devtools-cli debug clear-probes --types tracepoint
```

### Logpoints
```bash
ironbee-browser-devtools-cli debug put-logpoint --url-pattern "app.js" --line-number 50 --log-expression "user.id"
ironbee-browser-devtools-cli debug list-probes --types logpoint
ironbee-browser-devtools-cli debug remove-probe --type logpoint --id <probe-id>
ironbee-browser-devtools-cli debug clear-probes --types logpoint
```

### Exception Monitoring
```bash
ironbee-browser-devtools-cli debug put-exceptionpoint --state uncaught
ironbee-browser-devtools-cli debug put-exceptionpoint --state all
```

### Watch Expressions
```bash
ironbee-browser-devtools-cli debug add-watch --expression "this"
ironbee-browser-devtools-cli debug add-watch --expression "user.id"
ironbee-browser-devtools-cli debug list-probes --types watch
ironbee-browser-devtools-cli debug remove-probe --type watch --id <probe-id>
ironbee-browser-devtools-cli debug clear-probes --types watches
```

### Retrieve and Clear Snapshots (Unified)
```bash
ironbee-browser-devtools-cli --json debug get-probe-snapshots
ironbee-browser-devtools-cli --json debug get-probe-snapshots --types tracepoint,logpoint,exceptionpoint
ironbee-browser-devtools-cli --json debug get-probe-snapshots --probe-id "tp_abc" --from-sequence 0
ironbee-browser-devtools-cli debug clear-probe-snapshots
ironbee-browser-devtools-cli debug clear-probe-snapshots --types tracepoint --probe-id "tp_abc"
```

### Node.js Backend Debugging (ironbee-node-devtools-cli)

For debugging Node.js API servers, backends, or scripts:

```bash
# 1. Connect to process (by PID, name, or Docker)
ironbee-node-devtools-cli --session-id backend-debug debug connect --pid 12345
ironbee-node-devtools-cli --session-id backend-debug debug connect --process-name "server.js"

# 2. Tracepoint on route handler or service
ironbee-node-devtools-cli --session-id backend-debug debug put-tracepoint \
  --url-pattern "routes/api.ts" \
  --line-number 42

# 3. Exception monitoring
ironbee-node-devtools-cli --session-id backend-debug debug put-exceptionpoint --state uncaught

# 4. Console logs from Node process
ironbee-node-devtools-cli --session-id backend-debug --json debug get-logs
ironbee-node-devtools-cli --session-id backend-debug --json debug get-logs --search "error"

# 5. Retrieve snapshots (after triggering the code path)
ironbee-node-devtools-cli --session-id backend-debug --json debug get-probe-snapshots
ironbee-node-devtools-cli --session-id backend-debug --json debug get-probe-snapshots --types tracepoint,exceptionpoint

# 6. Status and cleanup
ironbee-node-devtools-cli --session-id backend-debug debug status
ironbee-node-devtools-cli debug disconnect
```

`urlPattern` in Node context matches **script file paths** (e.g., `server.js`, `routes/users.ts`). See [ironbee-node-devtools-cli](../ironbee-node-devtools-cli/SKILL.md) skill for full reference.

### Python Backend Debugging (ironbee-python-devtools-cli)

For debugging a running Python process (API server, worker, script) via debugpy — the target's Python env must have `debugpy` installed:

```bash
# 1. Connect (already-listening debugpy, PID injection, or process name)
ironbee-python-devtools-cli --session-id py-debug debug connect --host 127.0.0.1 --debugpy-port 5678
ironbee-python-devtools-cli --session-id py-debug debug connect --pid 12345
ironbee-python-devtools-cli --session-id py-debug debug connect --process-name "app.py"

# 2. Tracepoint on a handler (python probes use --file/--line, not --url-pattern/--line-number)
ironbee-python-devtools-cli --session-id py-debug debug put-tracepoint --file "routes/users.py" --line 25

# 3. Exception monitoring
ironbee-python-devtools-cli --session-id py-debug debug put-exceptionpoint --state uncaught

# 4. Process stdout/stderr logs
ironbee-python-devtools-cli --session-id py-debug --json debug get-logs --type error

# 5. Deadlock / hung-thread diagnosis: snapshot EVERY thread's stack at once
ironbee-python-devtools-cli --session-id py-debug --json debug dump-threads --include-locals

# 6. Retrieve snapshots, then clean up
ironbee-python-devtools-cli --session-id py-debug --json debug get-probe-snapshots
ironbee-python-devtools-cli --session-id py-debug debug disconnect
```

See [ironbee-python-devtools-cli](../ironbee-python-devtools-cli/SKILL.md) skill for full reference.

### Error Investigation
```bash
ironbee-browser-devtools-cli content take-screenshot --name "error-state"
ironbee-browser-devtools-cli content get-as-html --selector ".error-container"
```

## Basic Debugging Workflow

1. **Reproduce**: Navigate to the problematic page
2. **Capture**: Take screenshot of current state
3. **Inspect Console**: Check for JavaScript errors
4. **Analyze Network**: Look for failed requests
5. **Investigate**: Run diagnostic JavaScript
6. **Document**: Summarize findings with evidence

```bash
# Quick debug workflow
ironbee-browser-devtools-cli navigation go-to --url "https://example.com"
ironbee-browser-devtools-cli content take-screenshot --name "initial"
ironbee-browser-devtools-cli --json o11y get-console-messages --type warning
ironbee-browser-devtools-cli --json o11y get-http-requests --status '{"min":400}'
```

## Advanced Debugging Workflow (Non-Blocking)

### 1. Set Up Probes

```bash
SESSION="--session-id debug-session"

# Navigate to app
ironbee-browser-devtools-cli $SESSION navigation go-to --url "http://localhost:3000"

# Tracepoint on a function
ironbee-browser-devtools-cli $SESSION debug put-tracepoint \
  --url-pattern "app.js" \
  --line-number 42

# Exception monitoring
ironbee-browser-devtools-cli $SESSION debug put-exceptionpoint --state uncaught
```

### 2. Add Watch Expressions

```bash
ironbee-browser-devtools-cli $SESSION debug add-watch --expression "this"
ironbee-browser-devtools-cli $SESSION debug add-watch --expression "user.id"
```

### 3. Interact with Application

```bash
ironbee-browser-devtools-cli $SESSION interaction click --selector "#submit-btn"
ironbee-browser-devtools-cli $SESSION sync wait-for-network-idle
```

### 4. Retrieve Snapshots

```bash
ironbee-browser-devtools-cli $SESSION --json debug get-probe-snapshots
ironbee-browser-devtools-cli $SESSION --json debug get-probe-snapshots --types tracepoint,exceptionpoint
ironbee-browser-devtools-cli $SESSION --json debug get-probe-snapshots --from-sequence 0
```

### 5. Clean Up

```bash
ironbee-browser-devtools-cli $SESSION debug clear-probes
ironbee-browser-devtools-cli $SESSION debug clear-probe-snapshots
ironbee-browser-devtools-cli session delete debug-session
```

## Probe Types Summary

| Probe | Purpose | Output | CLI |
|-------|---------|--------|-----|
| Tracepoint | Function calls | Stack, locals, watches | ironbee-browser-devtools-cli, ironbee-node-devtools-cli, ironbee-python-devtools-cli |
| Logpoint | Expression values | Evaluated result | all three |
| Exceptionpoint | Error catching | Error, stack trace | all three |
| Watch | Per-tracepoint expressions | watchResults in snapshot | list/remove via list-probes, remove-probe, clear-probes |
| Thread dump | Deadlock / GIL / hung-thread diagnosis | Every thread's stack | ironbee-python-devtools-cli only (`debug dump-threads`) |

## Best Practices

1. **Choose the right CLI**: Use `ironbee-browser-devtools-cli` for frontend/page debugging; use `ironbee-node-devtools-cli` for Node.js backend/API debugging; use `ironbee-python-devtools-cli` for running Python processes (probes take `--file`/`--line` there, and the target needs `debugpy` installed)
2. **Always check console for errors first**
3. **Filter network requests** to relevant endpoints
4. **Take screenshots** before and after actions (browser)
5. **Use source maps** for minified/bundled code
6. **Start with exceptions** to catch errors first
7. **Use logpoints** for lightweight monitoring
8. **Poll snapshots** with `--from-sequence` for efficiency
9. **Clear probes** when done to avoid overhead
10. **Document reproduction steps** clearly
