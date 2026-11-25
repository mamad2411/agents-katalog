---
name: cc-htmlfeedback
description: Visualizing complex material (plans, designs, architectures, data models) as a self-contained HTML page is the preferred, best-practice way to collect the user's feedback - use this tool for EVERY HTML page meant to gather feedback. It serves your page(s) with a comment widget injected, then turns the comments you leave in the browser into fix-it tickets and applies each fix in place. Use when the user runs /cc-htmlfeedback, asks to "start the feedback loop", or whenever you generate an HTML page to collect the user's feedback.
---

# cc-htmlfeedback live loop (v2)

You (this Claude Code session) are the worker that drains the feedback queue. A companion
server (`server.js`) serves the user's pages with the widget injected. The user can open
**multiple pages** (one browser tab each) and comment on any of them; you fix them
**concurrently**. Everything flows through a **per-page** queue under `<servedRoot>/.cc-htmlfeedback/`:

```
.cc-htmlfeedback/
  index.json                         # { "<pagekey>": { page, file, firstSeen } }  (written by the server)
  pages/<pagekey>/
    feedback_inbox.jsonl             # append-only, written by the SERVER on each comment
    feedback_tasks.json              # the board for this page: { version, page, file, tickets:[] } — written ONLY by you
```

**Two-file ownership** (this is the lock): the server only ever *appends* to each page's
`feedback_inbox.jsonl`; **you (the loop) are the only writer of every `feedback_tasks.json`** —
the per-ticket subagents are pure workers that never touch any board. Because the loop is the
single board writer, tickets run concurrently (even on the same page) race-free: subagents fix +
verify, then return a result, and you serialize only the quick board write.

Statuses: `todo → in-progress → done` (or `error`). Refinement is a *new* comment, never an edit.

**The page updates itself.** When you set a ticket to `done` in its board, the widget applies
the verified change to the user's tab by **DOM morphing** (static mode) — in place, no reload,
preserving scroll/focus. In proxy mode the upstream dev server's HMR updates the page. You never
trigger a reload; you just edit the source and write the board.

## Install location (bundled plugin)

This skill ships inside the `cc-htmlfeedback` Claude Code plugin; the runtime tooling
(`server.js`, `lib/`, the injected widget) is bundled alongside it. Resolve paths from the plugin
root — Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}` with the installed plugin directory on any
machine:
- `TOOLING = ${CLAUDE_PLUGIN_ROOT}` (bundled `server.js` + `lib/` + `feedback-widget.js`)
- `SKILL = ${CLAUDE_PLUGIN_ROOT}/skills/cc-htmlfeedback` (this folder — `SKILL.md`, `task-workflow.md`, `judge-prompt.md`)

`server.js` resolves its own `./lib/*` and the co-located widget relative to its file, so it runs
correctly from the plugin cache. The served app is chosen via `--root`/`--proxy`.

## Arguments

`/cc-htmlfeedback [target] [--port N]`
- no target / a directory → **static mode**: `node $TOOLING/server.js --root <dir> --port <port>` (default `.`, `4317`).
- a URL (e.g. `http://localhost:5173`) → **proxy mode**: `node $TOOLING/server.js --proxy <url> --port <port>`.
- `/cc-htmlfeedback stop` → stop the loop and kill the server.

## Start

1. Resolve `QUEUE = <servedRoot>/.cc-htmlfeedback`.
2. Start the server **in the background**: `node $TOOLING/server.js --root <dir> --port <port>` (or `--proxy`). Note the base URL `http://127.0.0.1:<port>/`.
   - **If the port is busy** the server exits non-zero with a clear message instead of crashing. If the
     occupant is our own (possibly orphaned) server it prints its **pid** — free the port with
     `kill <pid>` or `curl -X POST http://127.0.0.1:<port>/__ccfb/shutdown`, then retry; if it's a
     foreign process, pick another `--port`. You can probe first with
     `curl -s http://127.0.0.1:<port>/__ccfb/health` — a cc-htmlfeedback server replies with its
     `sessionId`, `pid`, `mode`, `target`, and `tooling` dir (anything else / no reply = not ours).
3. **Startup outstanding-feedback check.** Scan `QUEUE/pages/*/feedback_tasks.json` (and seed any
   `feedback_inbox.jsonl` lines whose `id` isn't yet in that page's board as `todo`). If any
   **non-`done`** tickets exist, summarize them to the user grouped by **page** then **status**
   (counts + one line each), and ask how to proceed:
   - **Resume** the `todo`/`in-progress` items (default),
   - **Explain/retry** each `error` (show its `result` reason),
   - **Clean** — clear a page's `done` history, or wipe a page's board for a fresh start.
   If there is no outstanding work, say so and continue.
4. Open the page(s) the user wants in Chrome with `mcp__claude-in-chrome__*` — **one tab per page**
   (the widget auto-injects and connects). Track which tabId maps to which page.
5. Tell the user the loop is listening, then enter the drain loop.

## Drain loop (one agent per ticket, concurrent — up to 5 in flight)

Repeat until stopped. **You (the loop) are the sole writer of every `feedback_tasks.json`;**
subagents are pure workers that never touch a board.

1. **Collect** all `todo` tickets across every page board. If there are none:
   - Run `node $TOOLING/lib/watch-inbox.js <QUEUE> 1800000` as a **background task**
     (`Bash` with `run_in_background: true`). It exits the moment any page's `feedback_inbox.jsonl`
     changes (a new comment arrived) — the harness then re-invokes you. Between comments you are
     idle: no polling, no token cost. The 30-min timeout is just a liveness heartbeat;
     `/cc-htmlfeedback stop` reaches you as a normal message, so no short poll is needed.
   - On wake: re-scan all pages, merge new inbox lines into the right per-page board as `todo`,
     re-arm a fresh background watcher next time, and continue. If the user asked to stop → **Stop**.
2. **Claim + dispatch, keeping ≤ 5 tickets in flight.** Fill the 5 concurrent slots from the pending
   `todo` tickets (any page — page no longer constrains concurrency):
   - **Claim:** set the batch you're about to dispatch to `in-progress` (one batched read-modify-write
     per affected page board). This instantly pulses the "working" animation on those exact texts.
     Claim at dispatch time so `in-progress` means *actually being worked*, not merely queued.
   - **Dispatch one fresh subagent per ticket, in a single message** (parallel `Agent` calls,
     `subagent_type: "general-purpose"`). Each gets a clean context and does exactly one ticket.
     Its prompt MUST tell it to **first read `$SKILL/task-workflow.md`** and follow it step-by-step.
     Pass it: the `TICKET` JSON, `ROOT` = served root, `TABID` = the user's tab for that page, and
     `TOOLING`/`SKILL`. **Do NOT pass a `BOARD` path or any board-writing duty** — the subagent only
     fixes, verifies, and returns its result.
   - **Concurrency:** up to **5 tickets at once, regardless of page.** Same-page tickets now run in
     parallel safely because only you write the board. (If two tickets edit the same source span, the
     loser's `Edit` fails and it returns `error` — resurface it; the file is never corrupted.)
3. **Resolve as each returns.** Each subagent returns `{ id, status: "done"|"error", result, files }`.
   Write it into that ticket's board entry (read-modify-write the whole file — you own it): `done` →
   the widget morphs the user's tab in place (no reload); `error` → keep the `result` reason. Free the
   slot, dispatch the next pending `todo`, and keep going until all are resolved, then loop to Step 1.

## Verification rubric (judge-prompt.md)

There is no separate judge agent anymore — **verification is Step 3 of each task subagent's own
workflow** (`task-workflow.md`), using the rubric in `$SKILL/judge-prompt.md` (intent satisfied +
no regressions). **Tab isolation is mandatory:** the subagent opens a **new, dedicated tab** via
`mcp__claude-in-chrome__tabs_create_mcp` and inspects only that tab — it NEVER reuses or navigates
the user's tab. If it can't drive Chrome, it falls back to capturing evidence (screenshot +
DOM/console text) from its own fresh tab and evaluating that against the rubric.

## Stop

`/cc-htmlfeedback stop` (or the user says stop): kill the background `server.js` process and end the
loop. If you no longer hold the process handle (e.g. an orphan from a prior session), confirm it's
ours via `curl -s http://127.0.0.1:<port>/__ccfb/health` then stop it PID-independently with
`curl -X POST http://127.0.0.1:<port>/__ccfb/shutdown`. The per-page boards remain as the persistent
record; restarting resumes from them (the startup check surfaces anything still outstanding).

## Notes

- One session, many pages; up to 5 tickets fixed concurrently regardless of page; one browser tab per page.
- You never edit any `feedback_inbox.jsonl`; you (the loop) fully own each `feedback_tasks.json` —
  subagents never write a board.
- Keep `result` to one glance-able line; put touched paths in `files`.
- No reloads: the widget reflects a `done` change by morphing in place (static) or via the
  upstream HMR (proxy). Just edit source + write the board.
- Each task runs in its own fresh subagent that reads `$SKILL/task-workflow.md`, fixes + verifies the
  ticket, and **returns a result**; the loop claims `in-progress` at dispatch (the user-facing signal)
  and writes the returned `done`/`error` back to the board.
- **Maintenance:** this skill lives in the repo at `plugins/cc-htmlfeedback/skills/cc-htmlfeedback/`
  (the single source of truth). Edit `SKILL.md` / `task-workflow.md` / `judge-prompt.md` **there**.
  The bundled `server.js`, `lib/`, and `feedback-widget.js` are assembled into the plugin by
  `node build.js` from the repo-root sources — run it after changing the server, lib, or widget
  (e.g. `watch-inbox.js` takes `<queueDir> [timeoutMs]`; the queue is per-page under `pages/<pagekey>/`).
