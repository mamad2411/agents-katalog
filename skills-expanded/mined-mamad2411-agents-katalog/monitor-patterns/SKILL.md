---
name: monitor-patterns
description: "Monitor primitive decision matrix and helper signatures for streaming per-event output. Explicit-only, loaded on demand."
user-invocable: false
allowed-tools: Read, Glob, Grep, Bash
---

# Monitor Patterns

The Monitor primitive wraps a shell command and treats each stdout line as an event notification. Use it when the problem is **"tell me every time X happens"** — not "wait until X is done" (that's `run_in_background: true`).

Every Monitor invocation MUST use a selective filter (`grep --line-buffered`, `jq`, `awk`, or a helper function) so only discrete events reach the chat. Raw log tails auto-stop.

## Decision Matrix

| Need | Primitive | Why |
|------|-----------|-----|
| Run a Playwright suite, react to each PASS/FAIL/SKIP | **Monitor** + filter | Per-test events, no buffering, low context cost |
| Wait for one test run to finish (no streaming) | `Bash({ run_in_background: true })` | Single completion signal, no per-event work |
| Tail a Vercel deploy's state during CI/E2E setup | `Monitor` + `monitor_vercel_deploy` | Discrete READY/ERROR transitions |
| Watch CI for terminal state | `Monitor` + `monitor_gh_ci` | Final-state-only event stream |
| Watch a PR for bot review comments | `Monitor` + `monitor_gh_comments` | Per-comment events |
| Watch a cooperative signal directory | `Monitor` + `monitor_lock_files` | inotify + ls fallback |
| One-shot diagnostic command (`playwright test --list`, a status-check CLI) | Raw `Bash` | No streaming needed |
| Native blocking command with clean exit (`gh run watch --exit-status`) | Raw `Bash` | Already does the right thing |

## Canonical Helpers

Source a shared `monitor-helpers.sh` shell library in any script or agent that needs one of
these — never reinvent a poll loop inline:

```bash
source /path/to/monitor-helpers.sh
```

| Helper | Signature | Purpose |
|--------|-----------|---------|
| `monitor_turbo_stream` | `TEST_RUNNER_ARGS...` | Per-package / per-spec completion lines from a monorepo test run |
| `monitor_vercel_deploy` | `PROJECT BRANCH [POLL_SECONDS]` | READY / ERROR transitions on a deployment |
| `monitor_gh_ci` | `BRANCH [POLL_SECONDS]` | CI terminal state for a branch |
| `monitor_gh_comments` | `PR_NUMBER BOT_LOGIN [POLL_SECONDS]` | Stream bot review comments as they post |
| `monitor_lock_files` | `LOCK_DIR PATTERN_REGEX` | inotify-based file-watch with ls fallback |

Defaults and edge cases live inside the helper implementations — read the library file itself
for full signatures before wiring a new caller.

## Three Canonical Patterns

### 1. Filtered-stream — wrap a streaming tool, grep for terminal lines

The most common e2e/test pattern. Replaces a raw blocking test invocation.

**Before** (raw Bash — blocks, dumps all stdout):

```bash
cd packages/e2e && pnpm playwright test "$TEST_PATH" 2>&1
```

**After** (Monitor — per-spec completion events):

```bash
source /path/to/monitor-helpers.sh
monitor_turbo_stream pnpm --filter e2e playwright test "$TEST_PATH" --reporter=line
```

The agent sees `✓ tests/foo.spec.ts:42 (1.2s)` per pass and `✗ tests/bar.spec.ts:18` per fail — each line is one event, not a buffered dump.

### 2. Shell-poll — internal loop polling a remote API

Used for cloud state where there's no native streaming. Helpers like `monitor_vercel_deploy` and `monitor_gh_ci` implement this internally.

```bash
source /path/to/monitor-helpers.sh
monitor_vercel_deploy my-project dev 10  # poll every 10s, emit READY/ERROR
```

The wrapped helper polls the provider's API and emits one line per state transition. The agent reacts to the READY event by triggering downstream work, or to ERROR by surfacing the failure.

### 3. File-watch — `inotifywait -m` on a cooperative signal dir

Used when commands write completion markers to a shared directory.

```bash
source /path/to/monitor-helpers.sh
monitor_lock_files "/tmp/wave-locks" '^wave-[0-9]+\.done$'
```

Each new lock file matching the regex emits one event. Useful for fan-out gates where several parallel workers each drop a completion marker and an orchestrator waits on all of them.

## Poll-Loop Exit Anti-Pattern: never gate on a strict parser whose error is swallowed

A shell-poll helper (Pattern 2) breaks out of its `while` loop when a status field reaches a terminal value. If the variable that gates the `break`/`return` is extracted with a **strict parser** (`jq`) whose **error is swallowed** (`2>/dev/null`), the loop silently never exits — it runs to its iteration cap (tens of minutes) instead of stopping on completion.

**Root cause (observed against a CI provider's build API):** the build/timeline JSON embeds raw control chars (`U+0000`–`U+001F`) inside string fields — the triggering commit message, trigger-info, log URLs, and issue messages. `jq` is strict and **errors** on unescaped control chars. With `... | jq -r '.status' 2>/dev/null` the error is discarded, the gating variable becomes empty (`""`), the terminal-state comparison never matches, and the loop polls forever.

**Tell-tale signature:** every progress line renders the gated field as empty (e.g. `/ ::` where a status should be), and the stream ends with no terminal (`READY`/`succeeded`/`FAILED`) line — the Monitor invocation's lifetime expires instead.

**Fix — extract the gate scalar robustly.** Two idioms, in order of preference:

```bash
# A. grep-extract the one scalar the loop gates on (control-char-proof, no parser)
bstatus=$(printf '%s' "$body" | grep -o '"status":"[^"]*"' | head -1 | cut -d'"' -f4)

# B. python json.loads(strict=False) — when you need structured fields, not just one scalar
state=$(printf '%s' "$body" | python3 -c \
  'import sys,json; d=json.load(sys.stdin, strict=False); print(d.get("result") or d.get("status") or "")')
```

**Rules:**
- NEVER pipe raw control-char-bearing JSON through `jq` to produce the variable a loop's exit depends on.
- NEVER `2>/dev/null`-swallow the parser whose output gates the loop — a swallowed failure on the gate scalar is an infinite loop. (Swallowing is fine on a parser that only formats an *event* line; the loop's exit does not depend on it.)
- The robust-extract idiom belongs in the helper, not the caller — a helper that polls a pipeline API should gate its terminal-state `return` on a `python json.loads(strict=False)`-extracted field (idiom B) so it cannot hang on a `jq` parse error.

## When NOT to Use Monitor

- **One-shot lookups** (`playwright test --list`, `git log`, a status CLI call) — Monitor's per-line semantics add no value; raw Bash with stdout capture is correct
- **Native-blocking commands with clean exit codes** (`gh run watch --exit-status`) — already does the right thing; wrapping in Monitor adds latency without benefit
- **Parallel sub-agent dispatches** — Monitor cannot observe sub-agent completion; an orchestrator coordinates fan-in via task results, not stdout streaming
- **Non-streaming commands** — anything that produces output as one batch at the end (e.g. a curl response) — `run_in_background: true` is the right primitive

## Provider Recipes

Per-provider snapshot + stream recipes:

| Provider | Reference |
|---|---|
| Vercel deploy pipeline (snapshot + log tail) | `references/vercel.md` |
| Azure Pipelines (snapshot + App Insights tail) | `references/azure.md` |
| Better Stack (uptime + Logtail stream) | `references/better-stack.md` |
