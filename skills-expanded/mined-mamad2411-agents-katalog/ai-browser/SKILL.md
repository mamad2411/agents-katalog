---
name: ai-browser
description: Drive a real Chromium browser over the Chrome DevTools Protocol (CDP) for any web task — opening URLs, scraping rendered content, taking screenshots, evaluating JavaScript, and smoke-testing web apps. Use this skill whenever the user asks to open, browse, or visit a URL; scrape or extract a page's content; screenshot or render a site; check what a JS-heavy page actually displays; automate a browser; or test a local web server. Prefer it even when the user doesn't say "browser" and even when curl might seem enough, because a real browser executes JavaScript, handles cookies, and sees the rendered DOM. Uses $AI_BROWSER_CHROMIUM_CMD / $AI_BROWSER_PYTHON_CMD when set (the opencode-wrapped environment), otherwise falls back to any installed chromium/chrome and python3.
---

# ai-browser — drive Chromium over CDP

## Why a real browser

`curl` only sees static HTML. Most modern pages build their content with
JavaScript, so fetching the HTML often returns an empty shell. Launching a
real, headed Chromium and speaking CDP to it gives you the rendered DOM,
executed JS, screenshots, and cookies — the same view a user gets.

## Quick start

All paths below are relative to this skill's directory. Resolve the Python
interpreter first (it needs the `websockets` package):

```bash
PY="${AI_BROWSER_PYTHON_CMD:-python3}"
"$PY" -c 'import websockets' 2>/dev/null || {
  "$PY" -m venv /tmp/ai-browser-venv && /tmp/ai-browser-venv/bin/pip install -q websockets
  PY=/tmp/ai-browser-venv/bin/python
}
```

For each new independent browser session, check the preferred debugging port
(`$AI_BROWSER_CDP_PORT`, otherwise `9222`) before launching. If any process
occupies it, select a different free port instead of reusing that process:

```bash
set -euo pipefail
command -v flock >/dev/null || { echo "error: flock is required for safe ai-browser launch" >&2; exit 1; }

PORT="$(
  # All cooperating launches use this per-user lock through readiness.
  exec 9>"/tmp/ai-browser-launch-${UID}.lock" || exit $?
  flock -x 9 || exit $?
  selected="$("$PY" - <<'PY'
import os
import socket

def valid(value):
    try:
        port = int(value)
    except ValueError:
        raise SystemExit("error: AI_BROWSER_CDP_PORT must be an integer from 1 through 65535")
    if not 1 <= port <= 65535:
        raise SystemExit("error: AI_BROWSER_CDP_PORT must be from 1 through 65535")
    return port

def free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", port))
        return sock.getsockname()[1]

preferred = valid(os.environ.get("AI_BROWSER_CDP_PORT", "9222"))
try:
    print(free(preferred))
except OSError:
    try:
        print(free(0))
    except OSError as error:
        raise SystemExit(f"error: cannot select a free CDP port: {error}")
PY
)" || exit $?
  # Do not let detached Chromium inherit lock FD. Launcher output stays stderr.
  AI_BROWSER_CDP_PORT="$selected" bash scripts/launch-browser.sh 9>&- >&2 || exit $?
  printf '%s' "$selected"
)" || exit $?
export AI_BROWSER_CDP_PORT="$PORT"

"$PY" scripts/cdp.py --port "$PORT" open https://example.com  # -> {"url": "...", "title": "..."}
"$PY" scripts/cdp.py --port "$PORT" text                      # rendered body text of active tab
"$PY" scripts/cdp.py --port "$PORT" eval 'document.querySelectorAll("a").length'
"$PY" scripts/cdp.py --port "$PORT" screenshot page.png       # PNG of the viewport
"$PY" scripts/cdp.py --port "$PORT" tabs                      # list open tabs as JSON
"$PY" scripts/cdp.py --port "$PORT" close                     # shut this browser down when done
```

`open` waits for the page load event before returning, so follow-up commands
see the finished page.

Some shell-tool calls start with a fresh environment. Do not assume exported
`AI_BROWSER_CDP_PORT` persists. Record this session's numeric `PORT`, then set
it and pass it explicitly on every later command:

```bash
PORT=45123  # selected port for this existing session
"$PY" scripts/cdp.py --port "$PORT" text
```

Run selection only for a **new** session. Reuse your recorded port for this
session; never discover and adopt an arbitrary CDP endpoint. If your own
browser died, start a new session with selection rather than launching on a
stale port that another process may now occupy.

## Environment resolution

| What | Preferred | Fallback |
|------|-----------|----------|
| Browser binary | `$AI_BROWSER_CHROMIUM_CMD` | `chromium`, `chromium-browser`, `google-chrome-stable`, `google-chrome` on PATH |
| Python + websockets | `$AI_BROWSER_PYTHON_CMD` | `python3`; if `import websockets` fails, make a venv in `/tmp` and pip-install it |
| CDP port | `$AI_BROWSER_CDP_PORT` or `--port N` | `9222` |

`cdp.py` accepts both forms. `launch-browser.sh` accepts its first positional
port or `$AI_BROWSER_CDP_PORT`; it does not select a port for you.

## Launching the browser — why each piece matters

`scripts/launch-browser.sh` is deliberately picky about process handling:

- **Full detachment (`setsid ... </dev/null >>log 2>&1 &`).** Shell tools may
  kill the whole process group when a command times out. A browser launched
  without detaching dies silently mid-session and every later CDP call fails.
  This exact failure happened in practice; don't simplify the flags away.
- **Headed, not headless.** Always launch with a visible window — never add
  `--headless`. Headed windows make failures visible to the user and keep the
  browser's behavior identical to a real session. This requires a display:
  the script errors out clearly when neither `DISPLAY` nor `WAYLAND_DISPLAY`
  is set.
- **Port-local idempotency, not ownership.** If `/json/version` already answers
  on its requested port, the script reuses it, even when another session owns
  that browser. It neither verifies ownership nor selects a different port.
  Use locked quick-start selection only for new sessions, then retain and use
  that session's numeric port.
- **Fresh temp profile (`mktemp -d`).** A profile directory locked by another
  Chromium instance prevents startup entirely.
- **Readiness polling.** The debug port takes a moment to appear; poll
  `http://127.0.0.1:$PORT/json/version` until it responds instead of sleeping
  a fixed time.

## cdp.py reference

| Command | Effect |
|---------|--------|
| `ping` | Print browser version; exit code 1 if not running |
| `open <url>` | Navigate active tab, wait for load, print final URL + title |
| `eval <js>` | Evaluate JS in the page, print result (JSON for non-strings) |
| `text` | Print `document.body.innerText` — the rendered text, not source |
| `screenshot [path]` | Write a viewport PNG (default `./screenshot.png`) |
| `tabs` | List page targets as JSON |
| `close` | Graceful `Browser.close` |

Behavior worth knowing:

- The "active tab" is the most recently listed tab with a real URL — stale
  `about:blank` tabs are skipped so you don't screenshot emptiness.
- Screenshots arrive base64-encoded over one websocket frame; the script sets
  `max_size=64 MiB` because the default 1 MiB limit truncates them.
- If a page never fires `load` (rare), `open` returns after ~15 s anyway.

## Going beyond the bundled script

For flows cdp.py doesn't cover (clicking, typing, network interception,
multiple tabs), read `scripts/cdp.py` as the template — it already solves the
boring parts: request/response ID correlation against a background reader
task, per-session event filtering, and target attachment via
`Target.attachToTarget {flatten: true}`. Typical additions are a few lines:
send `Input.dispatchMouseEvent` for clicks, `Page.captureSnapshot` for MHTML,
or attach to several targets at once.

## Session patterns

**The browser is live state.** A correctly selected port isolates independent
ai-browser sessions, but user actions can still move this session's active tab.
Before acting on "the current page", read where you actually are:

```bash
"$PY" scripts/cdp.py --port "$PORT" eval 'location.href'
```

Derive context (repo name, issue number, ...) from that URL rather than from
local assumptions like `git remote` — they can disagree, and the user almost
always means what's on screen.

**Extract structured links, then navigate.** Pull hrefs plus labels as JSON,
pick the entry you want, and `open` it:

```bash
"$PY" scripts/cdp.py --port "$PORT" eval 'JSON.stringify(
  [...document.querySelectorAll("a[href*=\"/actions/runs/\"]")]
    .slice(0, 5).map(a => ({href: a.getAttribute("href"),
                            text: a.innerText.trim().split("\n")[0]})))'
```

Worked example — latest GitHub Actions run for the repo on screen: open
`https://github.com/<owner>/<repo>/actions`. If it redirects to
`/actions/new`, the repo has zero workflow runs (this also happens when no
`.github/workflows/` exists) — stop and say so instead of guessing. Otherwise
the first `/actions/runs/<id>` link from the query above is the newest run;
open it and scrape the outcome from the page text (`Success`, `Failure`, ...)
and job names from `a[href*="/job/"]`.

## Gotchas checklist

- Browser died? `"$PY" scripts/cdp.py --port "$PORT" ping` first. If it fails,
  perform new-session selection; do not launch on stale port or adopt an
  arbitrary CDP endpoint.
- Multiple agents/tasks sharing a machine: each new session selects a port.
  Selection tries `$AI_BROWSER_CDP_PORT` (or `9222`) with `socket.bind`, then a
  kernel-picked port. `flock` is required and protects cooperating launches
  only, not arbitrary external processes.
- Empty `text`/blank screenshot usually means you attached to a blank tab —
  run `tabs` to see what's actually open.
- Headless is intentionally never used; if launch fails on a display-less
  machine, surface the error instead of silently switching to `--headless`.
- `close` when finished with long-lived browsing sessions, but leave it
  running if more requests will come soon; startup costs ~1 s.
- Don't assume the tab is still where you left it — check `location.href`
  before reasoning about "the current page"; users and other agents move it.
