---
name: "context-mode-filtering"
description: "Claude Code Context Mode: shell noise filtering, output relevance scoring, automatic context pruning for long-running sessions, log filtering, and signal-to-noise optimization"
---

# Context Mode — Shell Noise Filtering

## When to activate
- Long-running sessions where accumulated tool outputs bloat the context window
- Debugging sessions with verbose log outputs (thousands of lines)
- CI/CD output analysis where 95% of the output is routine and 5% is actionable
- Working with large test suites where most tests pass and only failures matter
- Parsing build outputs, deployment logs, or monitoring dashboards for anomalies
- When the user says "filter the noise" or "show me what matters"

## When NOT to use
- Short sessions with minimal tool output
- When the user needs to see complete logs for compliance/audit
- Exploring a new codebase where all output is potentially informative
- When the full output is small enough to fit in context without pressure

## Instructions

### 1. Noise Classification

Categorize output lines by signal value:

| Signal Level | Description | Action | Examples |
|---|---|---|---|
| **Critical** | Errors, failures, security alerts | Always show, never filter | `ERROR: Connection refused`, `FAIL: 3 tests` |
| **Warning** | Deprecations, performance issues | Show in summary | `WARN: deprecated API`, `slow query: 2.3s` |
| **Info** | Progress milestones, state changes | Aggregate | `Building 45/100 modules`, `Deployed to staging` |
| **Debug** | Verbose tracing, internal state | Filter out unless relevant | `GET /api/health 200 1ms`, `cache hit: key=...` |
| **Noise** | Repeated, boilerplate, success spam | Always filter | `✓ test passed`, ANSI escape codes, blank lines |

### 2. Filter Rules

```yaml
context_filters:
  # Remove lines matching these patterns
  exclude:
    - pattern: "^\\s*$"                    # blank lines
    - pattern: "^(GET|POST|PUT|DELETE).*200"  # successful HTTP requests
    - pattern: "^\\[INFO\\].*heartbeat"     # health check noise
    - pattern: "node_modules/"              # dependency paths in stack traces
    - pattern: "^\\s+at\\s+.*\\(node:"      # Node.js internal stack frames
    
  # Always keep lines matching these patterns
  include:
    - pattern: "ERROR|FATAL|CRITICAL"       # all errors
    - pattern: "FAIL|FAILED|failure"        # test/build failures
    - pattern: "timeout|Timeout"            # timeouts
    - pattern: "permission denied|unauthorized|forbidden"  # auth issues
    - pattern: "memory|OOM|heap"            # memory issues
    
  # Summarize instead of showing full output
  aggregate:
    - pattern: "passed|PASS|✓"             # "47 tests passed" (not 47 lines)
    - pattern: "compiled successfully"      # "12 modules compiled" (not 12 lines)
    - pattern: "cache hit"                  # "cache hit rate: 94%" (not every hit)
```

### 3. Log Filtering Pipeline

```
Raw log (10,000 lines)
    │
    ▼
[Stage 1: Dedup] ─── Remove repeated identical lines
    │                 "Connection established" × 200 → "Connection established (×200)"
    ▼
[Stage 2: Exclude] ── Remove known noise patterns
    │                  Health checks, heartbeats, verbose debug
    ▼
[Stage 3: Aggregate] ─ Group similar lines into summaries
    │                  47 "test passed" lines → "47/50 tests passed"
    ▼
[Stage 4: Rank] ───── Score remaining lines by signal value
    │                  Errors > Warnings > State changes > Info
    ▼
[Stage 5: Truncate] ── Keep top N lines by signal, summarize rest
    │                   Keep: 50 highest-signal lines
    │                   Summary: "8,234 info lines filtered (0 anomalies)"
    ▼
Filtered output (50 lines + summary)
```

### 4. Test Output Filtering

**Before (200 lines):**
```
✓ auth.login returns token
✓ auth.logout clears session
✓ auth.refresh extends token
... (47 more passing tests)
✗ auth.password-reset sends email
  Expected: email sent to user@example.com
  Received: undefined
✓ auth.signup creates user
... (2 more passing tests)
```

**After (filtered):**
```
Tests: 49/50 passed, 1 failed

FAILED: auth.password-reset sends email
  Expected: email sent to user@example.com
  Received: undefined
  → Likely cause: email service not mocked in test setup
```

### 5. Build Output Filtering

**Before (500 lines):**
```
[1/120] Compiling src/utils/date.ts
[2/120] Compiling src/utils/string.ts
[3/120] Compiling src/utils/array.ts
... (117 more compile lines)
[120/120] Compiling src/index.ts
webpack 5.89.0 compiled with 3 warnings in 4523 ms
WARNING in src/api/users.ts:45
  Unused import 'lodash'
WARNING in src/components/Header.tsx:12
  Missing key prop in list item
WARNING in src/config/database.ts:8
  Deprecated option 'pool.min'
```

**After (filtered):**
```
Build: 120/120 modules compiled in 4.5s (3 warnings)

Warnings:
1. src/api/users.ts:45 — unused import 'lodash'
2. src/components/Header.tsx:12 — missing key prop
3. src/config/database.ts:8 — deprecated 'pool.min' option
```

### 6. CI/CD Log Filtering

```yaml
ci_filter:
  stages:
    install:
      show: "package count, any vulnerabilities"
      hide: "individual package downloads, progress bars"
    
    lint:
      show: "error count, error details"
      hide: "files with no issues, progress dots"
    
    test:
      show: "failures, coverage change, new uncovered lines"
      hide: "passing tests (show count only), test setup"
    
    build:
      show: "warnings, errors, bundle size change"
      hide: "module compilation progress"
    
    deploy:
      show: "status changes, errors, URL"
      hide: "individual resource creation, health check polls"
```

### 7. Context Pruning for Long Sessions

**Automatic pruning of old tool results:**

```yaml
session_pruning:
  policy: "sliding_window"
  keep_full:
    turns: 10          # last 10 turns keep full tool output
    critical_outputs: "always keep error outputs regardless of age"
  
  summarize:
    turns: "11-30"     # summarize tool outputs for turns 11-30
    format: "1-line summary per tool call"
    
  drop:
    turns: "31+"       # drop tool output, keep only user/agent messages
    retain: "file paths and key decisions only"
```

## Example

**Filtering a 5,000-line deployment log:**

```
User: "The deploy failed. What happened?"

Agent reads full log (5,234 lines), filters to signal:

Deploy log: 5,234 lines → 12 relevant lines

Timeline of failure:
1. [14:02:12] Build: 120/120 modules ✓ (4.2s)
2. [14:02:18] Docker image built: uitkit:1.11.0-rc1 (245MB)
3. [14:02:45] Deploy to staging started
4. [14:03:12] Health check: /api/health → 200 ✓
5. [14:03:15] Database migration started
6. [14:03:18] ERROR: migration 047_add_user_roles failed
   → "column 'role' already exists in table 'users'"
7. [14:03:18] Rollback initiated
8. [14:03:22] ERROR: rollback failed — partial migration state
9. [14:03:25] Deploy aborted — staging in inconsistent state

Root cause: Migration 047 assumes 'role' column doesn't exist,
but it was added manually in a previous hotfix.
Fix: Add IF NOT EXISTS to the migration or skip it.
```

## Anti-Patterns

- **Over-filtering:** Removing warning lines that seem unimportant but indicate a pattern — when in doubt, aggregate rather than drop
- **Loss of timeline:** Filtering out timestamps breaks chronological reconstruction — always preserve timestamps on critical/warning lines
- **No summary:** Filtering without providing a count of what was removed — always report "X lines filtered, Y kept, Z anomalies detected"
- **Static rules:** Using the same filter rules for build logs vs. runtime logs vs. test output — match filter rules to the output type
- **Filtering errors:** Never filter error-level output regardless of dedup rules — even repeated errors may indicate a cascade worth seeing
- **Context re-pollution:** Summarizing filtered output back into context but the summary itself is too long — keep summaries to 1-3 lines per category
