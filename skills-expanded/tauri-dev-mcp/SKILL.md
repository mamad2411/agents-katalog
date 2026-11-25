---
name: tauri-dev-mcp
description: Use when you need to visually verify or drive this Tauri app's running UI — taking screenshots, reading the live DOM, clicking real buttons, or calling real backend commands against real data. Covers launching the dev build with the MCP bridge compiled in, connecting the driver session, and shutting down cleanly. Not suitable for unit-test-only changes, or when the user only wants the code read.
---

# Verifying this app's UI through the Tauri MCP bridge

This app ships an optional MCP bridge that lets an agent screenshot the window,
read/execute JS in the webview, and invoke real Tauri commands. It is the only
way to check "does this actually render / actually work" without asking the user.

**The single most common failure: launching with the wrong command.** The bridge
is behind a non-default Cargo feature. `npm run tauri dev` compiles **without**
it and every `mcp___hypothesi_tauri-mcp-server__*` tool will then fail to connect,
with nothing in the log explaining why.

## 1. Launch

```bash
# Correct — bridge compiled in, listening on 127.0.0.1:9223
nohup npx tauri dev --features dev-mcp > /tmp/tauri-dev.log 2>&1 &

# Wait for the window instead of guessing a sleep duration
until pgrep -f "target/debug/cc-sessions-viewer" >/dev/null 2>&1; do sleep 2; done
sleep 5   # let the webview finish loading
```

First build takes minutes; incremental rebuilds are seconds. Do not run this in
the foreground — it never exits.

### Port 1420 is already in use

Vite is locked to port 1420 (`strictPort`, hardcoded in `tauri.conf.json`). A
stale Vite from a previous run **survives `pkill -f "tauri dev"`**, and the next
launch dies with `Error: Port 1420 is already in use` followed by
`The "beforeDevCommand" terminated with a non-zero status code`.

```bash
lsof -ti :1420 | xargs kill    # then relaunch
```

## 2. Connect

```
driver_session { action: "start" }
```

Required before any `webview_*` / `ipc_*` tool. A warning about the plugin not
reporting its version is expected and harmless — this repo pins
`tauri-plugin-mcp-bridge` 0.2, and tools needing ≥0.13 (such as
`manage_window { action: "focus" }`) will refuse; see §4 for the workaround.

Re-run `driver_session start` after any `location.reload()` — the reload drops
the injected bridge globals.

## 3. Drive the UI

Prefer `webview_execute_js` over coordinate clicking: it is deterministic, and it
returns data you can assert on in the same call.

```js
// Open Settings → a specific tab, then read back what rendered
(async () => {
  const wait = (ms) => new Promise(r => setTimeout(r, ms))
  const btn = [...document.querySelectorAll('button')]
    .find(b => /Settings|设置/.test(b.textContent || ''))
  btn && btn.click()
  await wait(300)
  const tab = [...document.querySelectorAll('.set-nav-item')]
    .find(n => /Storage|存储/.test(n.textContent || ''))
  tab && tab.click()
  await wait(500)
  return { rows: [...document.querySelectorAll('.set-store-name')].map(e => e.textContent.trim()) }
})()
```

### Calling real backend commands

Go through the webview's own bridge — `ipc_execute_command` has an allowlist and
will reject most commands:

```js
(async () => {
  const invoke = window.__TAURI__.core.invoke
  return await invoke('storage_usage')
})()
```

This runs the real command against real data. For anything destructive, seed
disposable fixtures first and restore afterwards (see §5).

## 4. Screenshots: focus the window first

If the window is not frontmost, `document.visibilityState === 'hidden'` and
**`requestAnimationFrame` never fires**. Vue `<Transition>` then freezes at
`*-leave-from` — a dialog you just closed stays in the DOM forever, and
screenshots come back faded, stale, or showing a modal that is logically gone.
This looks exactly like a product bug and is not one.

```bash
osascript -e 'tell application "System Events" to set frontmost of \
  (first process whose unix id is (do shell script \
  "pgrep -f \"target/debug/cc-sessions-viewer\" | head -1") as integer) to true'
```

Confirm before trusting a screenshot:

```js
({ hidden: document.hidden, visibility: document.visibilityState })
```

`manage_window { action: "focus" }` would be the clean way, but it needs plugin
≥0.13 and this app is on 0.2 — use the osascript above.

## 5. Hazards worth planning around

- **HMR reloads the webview.** Editing locale files or several files at once
  remounts the app: open modals close and your carefully staged state is gone.
  Re-open and re-assert rather than trusting a stale handle.
- **Disabled buttons swallow clicks silently.** A clear/delete button gated on
  `:disabled="!bytes"` does nothing when the target is empty, and the absence of
  a dialog reads as "my code is broken". Check `button.disabled` before
  concluding anything.
- **Two copies of the app may be running.** The user's installed build
  (`/Applications/Sessions Viewer.app`) shares on-disk state with the dev build.
  Never kill it, and remember it can be the one holding a file you are watching.
- **Seed, then restore.** When verifying deletion/retention paths, write throwaway
  fixtures (a `TEST-` name prefix makes cleanup greppable), back up any real
  config you perturb, and put it back when finished.

## 6. Shut down

Kill the wrapper, the app, **and** Vite — the first two leave Vite holding 1420:

```bash
pkill -f "tauri dev"
pkill -f "target/debug/cc-sessions-viewer"
pkill -f "node_modules/.bin/vite"
lsof -ti :1420          # must print nothing
pgrep -fl "Applications/Sessions Viewer.app"   # the user's app — must survive
```

Then `driver_session { action: "stop" }`.

Leave the machine as you found it: dev processes stopped, port free, fixtures
deleted, backed-up config restored.
