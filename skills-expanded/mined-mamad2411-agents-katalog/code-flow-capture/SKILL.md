---
name: code-flow-capture
description: >-
  Black-box browser recorder for troubleshooting a web app by capturing a whole
  flow instead of hand-reporting errors. Use when the user says /capture,
  /start-capture, /stop-capture, /fetch-session, "start a capture", "capture this
  flow", "investigate session <id>", "record
  the browser activity", hands you a code-flow-capture JSON, or wants to debug a
  web issue by testing it while everything (network requests + bodies, console,
  JS errors, navigation) is recorded to one file for you to analyse. The user
  tests; a start/stop recorder writes a timestamped JSON; you read + analyse it.
  Captures are private: gitignored and filed under systems/docs/captures/<app>/.
---

# Code Flow Capture

A "black-box recorder" for a web app. The user tests something; a start/stop
recorder captures the **whole flow** — every request/response (with bodies),
console line, JS error, and navigation — into ONE timestamped JSON. The capture
IS the bug report: no copy-pasting console logs, no screenshotting errors, no
"what did the request return?" round-trips.

**Model of use:** user starts capture → tests → stops capture → hands you the
JSON → you analyse. That's the whole loop.

## Commands

- **`/capture`** — show how to use it (load the recorder, start, stop, hand off).
- **`/start-capture`** — output the recorder + the exact start steps for the user.
- **`/stop-capture`** — the user stops + gives you the JSON; you file it and analyse.
- **`/fetch-session <id>`** — pull a stored capture from an on-site ingest service's
  admin API by id and analyse it (see `commands/fetch-session.md`).

## The recorder

The recorder `code-flow-capture.user.js` (in this skill directory —
`cli-skill/code-flow-capture.user.js`) is a self-contained script. Two ways to
load it — give the user whichever fits:

- **Console (one-off, zero install):** open the file, copy all, paste into DevTools
  → Console on the page under test, Enter. A red **● REC** pill appears top-right;
  capture auto-starts.
- **Tampermonkey (durable, survives reloads):** it's a `// ==UserScript==` — install
  once; a **Capture** pill appears that the user clicks to start/stop.

Stop = click the pill → `code-flow-capture-<timestamp>.json` downloads.

It captures, timestamped in order: **fetch + XHR** (method, url, status, request
body, response body ≤100 KB, duration), **console.\*** args, **window errors +
unhandled rejections** (message + stack), **SPA navigation**. Auth/cookie/CSRF
headers are never recorded.

## Where captures live — MANDATORY

Captures are the user's private runtime data. They are **gitignored — never pushed
to GitHub** — and filed under the systems docs tree, separated per app exactly like
reports:

```
systems/docs/captures/<app>/<year>/<month>/<capture-name>.json
```

- `<app>` = the app under test (ledger, admin, auth, docs, home, systems, …).
- Month is the lowercase full name (`july`).
- `systems/docs/` is already gitignored, so anything filed there stays local. If
  captures are ever kept elsewhere, add that path to `.gitignore` — a capture must
  never be committed (it holds real API payloads).
- When you write an **analysis** of a capture, save it beside the JSON as a
  markdown report (`<capture-name>-analysis.md`) in the same folder.

## Analysing a capture

The full, model-agnostic version of this playbook — copy-pasteable into any LLM —
is in `ANALYSIS.md` (same directory). Read the JSON and lead with what the user is
chasing. Prioritise:

1. **Failed / error requests** — any `fetch`/`xhr` with `ok:false` or `status>=400`.
   The `resBody` carries the server's exact error + code + details. Quote it.
2. **JS errors / unhandled rejections** — `kind:"error"` with stack.
3. **The flow** — walk the ordered events around the failure: what request fired,
   with what `reqBody`, what came back, what the console said, where it navigated.
4. **Anomalies** — duplicate requests, a call that never returned (`status:0`),
   unexpected payloads, wrong endpoints, retries.

Tie the finding to the code (file:line) and, if it's a bug, drive to root cause —
don't stop at the symptom. Then file the capture + your analysis per the storage
rule above.

## Filing steps (on `/stop-capture`)

1. Ask for the downloaded JSON's path (or its contents) if not given.
2. Determine `<app>` from the captured `meta.url` (or ask).
3. Move/copy the JSON to `systems/docs/captures/<app>/<year>/<month>/`.
4. Analyse; write `<name>-analysis.md` beside it.
5. Report the finding to the user; keep the capture out of git.
