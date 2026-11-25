---
name: runtime-debug
description: Agent-agnostic runtime debugging workflow with local NDJSON log collection. Use when the user explicitly invokes runtime-debug, debug mode, or when a hard-to-diagnose reproducible bug needs runtime evidence, temporary probes, manual reproduction, log analysis, a minimal fix, user verification, and instrumentation cleanup. For simple build, type, lint, or obvious test failures, fix normally and only mention that runtime-debug is available. Triggers include runtime-debug, debug mode, runtime logs, log-based diagnosis, reproduce before fixing, insert probes, frontend/UI state bugs, or investigate a hard bug without guessing.
---

# Debug Mode

Use this skill to run a disciplined runtime debugging loop. Do not jump directly to a fix. The value of this skill is the stop-and-reproduce checkpoint after targeted instrumentation.

Use normal debugging instead for straightforward build errors, type errors, lint failures, obvious failing unit tests, or bugs already explained by existing logs. In those cases, mention `runtime-debug` only if runtime instrumentation would materially help.

## Workflow

1. Read the relevant code and repro details.
2. List 2-5 ranked, falsifiable hypotheses with IDs such as `H1`, `H2`, and `H3`. Each hypothesis must predict what a runtime probe will show.
3. Start the local log collector:

   ```bash
   node <skill-dir>/scripts/log-server.mjs --dir .runtime-debug/logs --session <session_id> --port 0
   ```

   Keep the default loopback binding unless there is a very specific local-only reason to use `localhost` or `::1`.

4. Clear the session log before each repro if the file exists. Prefer a fresh session when the investigation changes.
5. Insert minimal temporary probes that POST JSON to `DEBUG_URL + "/log"`.
6. Wrap every temporary helper or probe in paired `RUNTIME_DEBUG_PROBE <session_id>` region comments.
7. Stop and ask the user to reproduce manually. Do not analyze or fix until the user replies.
8. When the user replies `A`, inspect the session log at `.runtime-debug/logs/<session_id>.ndjson`.
9. Classify each hypothesis as `CONFIRMED`, `REJECTED`, or `INCONCLUSIVE` using specific log evidence.
10. Make the smallest fix only after logs confirm a root cause.
11. Keep instrumentation active for one post-fix verification run, tagged with `runId: "post-fix"`.
12. Ask the user to verify with the same A/B/C checkpoint.
13. When the user replies `B` after a fix, remove all `RUNTIME_DEBUG_PROBE <session_id>` instrumentation and run relevant checks.

## Manual Checkpoint

After adding probes, always stop and send exactly this interaction shape, adapted with the real session details:

If the host client provides a structured choice or user-input UI, request the same three choices through that UI. Otherwise, send the plain-text fallback below.

```text
I added runtime debug probes and the collector is writing:

- Session: <session_id>
- Log file: .runtime-debug/logs/<session_id>.ndjson
- Debug endpoint: <DEBUG_URL>/log

Please reproduce the bug manually, then reply:

A - Reproduced
B - Fixed
C - Other; describe what happened
```

Handle replies as a state machine:

- `A`: The bug reproduced. Read the NDJSON log for this session, compare actual runtime state to the hypotheses, then either fix the confirmed cause or add more targeted probes.
- `B`: The bug is fixed. This is only valid after a fix was applied. Remove all temporary probes for this session and run final checks.
- `C`: Treat the user's text as new evidence. Adjust the repro, hypotheses, or probes. If no useful logs were written, verify the app is calling the right endpoint and session.

## Probe Rules

- Add only probes that distinguish between hypotheses.
- Use 3-8 instrumentation points by default. Cover function entry/exit, before/after critical operations, and branch paths.
- Log both intent and result when that distinction matters, for example "about to persist settings" and "persist returned status".
- Do not use `console.log`, `print`, stdout, or stderr for debug probes. All probe output must go to the collector and NDJSON log.
- For high-frequency events such as mousemove, scroll, resize, polling, or render loops, log only on state changes or sample aggressively.
- Add `runId: "pre-fix"` before the fix and `runId: "post-fix"` during verification when comparing before/after behavior.
- Wrap every temporary helper or probe with paired region markers so cleanup is mechanical. Prefer editor-foldable markers when the language supports them:

  ```ts
  // #region RUNTIME_DEBUG_PROBE <session_id> <probe-or-purpose>
  runtimeDebugLog({
    probe: "save.beforePersist",
    hypothesis: "settings-state-lost-before-api",
    file: "src/settings/save.ts",
    fn: "saveSettings",
    vars: { enabled, userId: "redacted" }
  });
  // #endregion RUNTIME_DEBUG_PROBE <session_id>
  ```

  ```python
  # #region RUNTIME_DEBUG_PROBE <session_id> <probe-or-purpose>
  runtime_debug_log({
      "probe": "save.before_persist",
      "hypothesis": "settings-state-lost-before-api",
      "file": "settings/save.py",
      "fn": "save_settings",
      "vars": {"enabled": enabled, "user_id": "redacted"},
  })
  # #endregion RUNTIME_DEBUG_PROBE <session_id>
  ```

  Use the matching comment syntax for the target language:

  ```text
  // #region RUNTIME_DEBUG_PROBE <session_id> ...    JavaScript, TypeScript, Java, C#, Go, Rust, C, C++
  # #region RUNTIME_DEBUG_PROBE <session_id> ...     Python, Ruby, Shell, YAML
  <!-- #region RUNTIME_DEBUG_PROBE <session_id> -->  HTML, Vue, Svelte
  /* #region RUNTIME_DEBUG_PROBE <session_id> */     CSS and C-style block contexts
  -- #region RUNTIME_DEBUG_PROBE <session_id> ...    SQL, Lua
  ```
- Include `session`, `probe`, `hypothesis`, `file`, and either `fn` or a short location label. The server will add `session` if omitted, but explicit fields make logs easier to search.
- Keep `vars` small and structured. Prefer booleans, ids already safe to expose, counts, enum states, timestamps, and branch names.
- Use a unique, stable `probe` name such as `settings.before-persist` or `checkout.after-discount`.
- Never log secrets, tokens, cookies, authorization headers, API keys, raw request bodies, raw responses that may contain private data, or unnecessary personal data.
- Never "log everything and grep." Logs should be few enough that the causal path is readable.

## Copyable Helpers

Use small local helpers instead of repeating raw `fetch` or HTTP code everywhere.

JavaScript or TypeScript in a browser:

```js
// #region RUNTIME_DEBUG_PROBE <session_id> debug-log-helper
const RUNTIME_DEBUG_SESSION = "<session_id>";
const RUNTIME_DEBUG_URL = "<DEBUG_URL>/log";

const runtimeDebugLog = (event) => {
  const payload = JSON.stringify({
    session: RUNTIME_DEBUG_SESSION,
    ...event,
    loc: new Error().stack?.split("\n")[2]?.trim(),
  });
  if (navigator.sendBeacon?.(RUNTIME_DEBUG_URL, payload)) return;
  fetch(RUNTIME_DEBUG_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: payload,
  }).catch(() => {});
};
// #endregion RUNTIME_DEBUG_PROBE <session_id>
```

Node.js or server-side JavaScript:

```js
// #region RUNTIME_DEBUG_PROBE <session_id> debug-log-helper
const RUNTIME_DEBUG_SESSION = "<session_id>";
const RUNTIME_DEBUG_URL = "<DEBUG_URL>/log";
const runtimeDebugLog = (event) =>
  fetch(RUNTIME_DEBUG_URL, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ session: RUNTIME_DEBUG_SESSION, ...event }),
  }).catch(() => {});
// #endregion RUNTIME_DEBUG_PROBE <session_id>
```

Python without third-party dependencies:

```python
# #region RUNTIME_DEBUG_PROBE <session_id> debug-log-helper
import json
import urllib.request

RUNTIME_DEBUG_URL = "<DEBUG_URL>/log"

def runtime_debug_log(event):
    try:
        payload = {"session": "<session_id>", **event}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            RUNTIME_DEBUG_URL,
            data=data,
            headers={"content-type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=0.5).close()
    except Exception:
        pass
# #endregion RUNTIME_DEBUG_PROBE <session_id>
```

Example event body:

```json
{
  "probe": "save.beforePersist",
  "hypothesis": "settings-state-lost-before-api",
  "file": "src/settings/save.ts",
  "fn": "saveSettings",
  "vars": {
    "enabled": true,
    "userId": "redacted"
  }
}
```

## Collector Contract

The bundled collector is intentionally small. It only accepts `POST /log` with a JSON object and appends one NDJSON line per event.

The collector is loopback-only. It refuses non-loopback hosts such as `0.0.0.0` because debug probes may contain local runtime state.

The log file is `.runtime-debug/logs/<session_id>.ndjson`. The server also prints the absolute `LOG_FILE` path on startup. Do not add a read wrapper script just for this skill; the agent can inspect NDJSON directly.

## Analyze Logs

After an `A` reply, summarize evidence in this shape before editing code:

Read the session log directly. For large logs, inspect only the relevant session, hypothesis, probe, or `runId` events instead of loading the whole file into context.

```text
H1 settings state is lost before API call
Status: CONFIRMED
Evidence: save.beforePersist logged enabled=false while UI event logged enabled=true.

H2 API rejects the value
Status: REJECTED
Evidence: no API call happened in this repro.

Next action: fix the local state handoff between onToggle and saveSettings.
```

If every hypothesis is `REJECTED` or `INCONCLUSIVE`, generate new hypotheses from a different subsystem and add narrower probes. Do not patch from vibes.

## Troubleshooting

- Logs empty: confirm the app executed the instrumented path, the session id matches, and the endpoint includes `/log`.
- Browser blocked the request: check mixed content, CSP `connect-src`, or extension/content-script isolation.
- CORS/preflight issue: the collector handles `OPTIONS`; if the browser still blocks, try `navigator.sendBeacon`, a same-origin dev-server proxy, or server-side instrumentation.
- Host rejected: use the default `127.0.0.1`, `localhost`, or `::1`; do not bind the collector to LAN or public interfaces.
- Too many logs: replace noisy probes with narrower state-change probes in the next run.
- Cannot reproduce: ask for exact steps, environment, input data, or a screen recording; do not invent a fix.

## Cleanup

Before declaring the task done:

- Re-run the original repro or the closest available automated check.
- Remove every paired region marked `RUNTIME_DEBUG_PROBE <session_id>`.
- Search the workspace for the session id, `RUNTIME_DEBUG_PROBE`, `#region RUNTIME_DEBUG_PROBE`, and `#endregion RUNTIME_DEBUG_PROBE`.
- Remove the session NDJSON log or confirm it is ignored and should be kept for local evidence. Never commit debug logs.
- Keep only the minimal product fix and any useful regression test.

## Hard Rules

- Never skip the reproduce checkpoint after adding probes.
- Never fix without runtime evidence when this skill is active.
- Never remove instrumentation before the user confirms the fix.
- Always clear the session log before a new reproduction run.
- Always keep probe output out of stdout/stderr.
