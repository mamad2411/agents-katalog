---
name: brave-cdp
description: Drive the user's own logged-in Brave, Chrome or Edge over the Chrome DevTools Protocol with a single connection, so the browser's "Allow remote debugging?" prompt appears once instead of on every step. Use for browser tasks that need the user's real sessions (dashboards, uploads, downloads, sites that block scripted HTTP) when no browser MCP is available or wanted. Also for developing Chrome extensions: reload an unpacked extension after edits, read its errors, or auto-reload on every save.
---

# brave-cdp

`scripts/cdp.mjs` is a zero-dependency Node 22+ CDP client. Run it with `node <this-skill-dir>/scripts/cdp.mjs ...`.

## The one rule: one connection per task
Modern Chromium browsers (Brave, Chrome 144+, Edge) show an **"Allow remote debugging?"** prompt for EVERY new DevTools connection, with no "always allow". Many small probe scripts = many prompts = an annoyed user.
- Plan the whole browser task first, then run it as ONE job script (`run job.mjs`) with adaptive steps and full logging.
- For long sessions with many steps, ask the user once if they want the relay (`node cdp.mjs relay`, run in the background). It holds one approved connection and every later command reuses it automatically. Stop it when the work is done.
- The relay survives browser restarts: when the browser closes it waits, and when a new browser instance starts it reconnects by itself (one Allow click). It retries once per new browser instance and at most once a minute when a job needs the browser, so it never loops on the Allow prompt.

## Setup (user does this once)
- Brave: open `brave://inspect/#remote-debugging` and turn remote debugging on. Chrome/Edge: `chrome://inspect/#remote-debugging` / `edge://inspect/#remote-debugging`.
- Or start the browser with `--remote-debugging-port=9222`. Chrome 136+ ignores that flag for the default profile, so add `--user-data-dir=<separate dir>` in that case.
- The script finds the port from the browser's `DevToolsActivePort` file. Overrides: `CDP_BROWSER=brave|chrome|edge|chromium`, `CDP_PORT`, `CDP_URL=ws://...`, `CDP_RELAY_PORT` (default 9333). When `CDP_BROWSER`, `CDP_PORT` or `CDP_URL` is set, a running relay is used only if it is connected to that browser.

## Commands
```
node cdp.mjs tabs                              # list open tabs
node cdp.mjs eval "document.title" --match github.com
node cdp.mjs run job.mjs [args...]             # whole task, one connection
node cdp.mjs cleanup                           # close tabs left by jobs that were killed
node cdp.mjs relay                             # optional: keep one connection open
```

## Record mode
`node cdp.mjs record <url> --out job.mjs` (or `--match <url-part>` for an open tab) opens a visible tab with a red "Recording" badge. The user clicks through the task; pressing the badge (or closing the tab, or Ctrl+C) writes a job script that `run` replays in the background.
- Records clicks, typing, Enter/Escape, dropdown choices and URLs typed in the address bar. Clicks on plain page areas are skipped.
- Elements are found by id, test-id, name, aria-label or href first, then by visible text, then by position.
- Passwords, card numbers and one-time codes are never written to the file. The script reads them from `JOB_*` environment variables and its header lists which.
- File uploads are left as a commented line to fill in.
- **Safe reruns.** Clicks that change something (Submit, Send, Post, Pay, Delete, Save... and Enter) are wrapped in `once()`. Each one that runs is logged to `<job>.done.json`, and a finished run deletes the log. If a run dies part-way, the next run stops and says which step already went through, instead of submitting twice. Check the site, then `run job.mjs --again` to replay anyway. Wrap any other step in `once('label', () => ...)` by hand.

## MCP server (browser tools without job scripts)
`scripts/mcp.mjs` is a zero-dependency MCP server with 14 tools: `browser_open`, `browser_tabs`, `browser_navigate`, `browser_read`, `browser_click`, `browser_type`, `browser_key`, `browser_scroll`, `browser_wait`, `browser_screenshot`, `browser_eval`, `browser_show`, `browser_close`, `browser_extension`.
```
claude mcp add --scope user brave-cdp -e CDP_BROWSER=brave -- node /path/to/skills/brave-cdp/scripts/mcp.mjs
```
- It connects to the browser on the first tool call, not at start-up, and reuses a running relay, so it's one Allow per browser session.
- `browser_read` returns the page text plus numbered elements (`[12] button "Save"`); click and type take that number as `ref`. That costs a few hundred tokens where a screenshot costs well over a thousand, so screenshots are for layout questions only.
- Tabs open hidden (background mode below). `tab` takes any id from `browser_tabs`, including the user's own tabs; those are only detached, never closed.
- For long multi-step tasks a job script (`run job.mjs`) is still cheaper: one tool call instead of one per step.

## Background mode (default)
New tabs from `page({ url })` open **hidden**: in a browser window parked off-screen, without taking the user's focus, with focus emulated so sites behave as if watched (animations run, videos play, clicks and screenshots work). The user keeps using the browser and other apps while a job runs. It costs no extra tokens.
- Each hidden tab is its own off-screen **popup** window. Links from other apps (gh auth, email, chat) always open in the user's normal window, never in a popup. Each popup is closed when its page is closed, so nothing is left behind after a job. Creating a window can take focus once on Windows; set `CDP_KEEP_WINDOW=1` to keep up to two idle popups for reuse instead (the relay then makes one at start-up).
- With `CDP_KEEP_WINDOW=1`, idle popups show in Alt+Tab as "Claude is working here (hidden)". `cleanup --all` closes them.
- `await p.show()` moves the window on screen, e.g. to hand a login or CAPTCHA to the user. It goes back off-screen when the page closes.
- `page({ url, visible: true })` (or `CDP_VISIBLE=1`) opens a normal tab in the user's window instead.
- Sound plays from hidden tabs. Pause or mute media in the job if that matters.
- Only the active tab of a window renders at full speed, so with two hidden pages at once the first one is throttled. Run them one after another.
- Brave reports fake `screenX`/`screenY` to pages; check the window position with `Browser.getWindowBounds` instead.

## Extensions you are developing
Uses the browser's own extensions page, so no extra flags or setup. `<ext>` is the extension's id, its folder, or part of its name (an ambiguous name stops and lists the ids).
```
node cdp.mjs ext list                      # every extension: id, on/off, unpacked/store, folder, error count
node cdp.mjs ext reload <ext> [--tabs]     # reload and print only errors raised since the reload
node cdp.mjs ext errors <ext> [--clear]    # what the extensions page's Errors button shows
node cdp.mjs ext watch <ext> [--tabs]      # reload on every save in the folder (Ctrl+C stops)
```
- After editing an unpacked extension, run `ext reload <folder> --tabs` instead of asking the user to click reload. `--tabs` also reloads the open pages its content scripts match, because Chrome doesn't re-inject content scripts into tabs that were already open.
- Exit code 2 means the reload produced errors or the manifest didn't load; the message shows the file and line.
- The extension must have been loaded once with "Load unpacked". Chrome has no way to do that first load over DevTools without restarting the browser with special flags.
- In jobs: `const x = await ext(); const r = await x.reload(dir, { reloadTabs: true }); await x.close();`. `x.list()`, `x.find(q)`, `x.info(id)` and `x.clearErrors(id)` are there too.

## Writing a job
```js
export default async function ({ page, tabs, ext, waitEvent, downloadsTo, cdp, log, args }) {
  const p = await page({ url: 'https://example.com' });  // NEW tab (default) — never hijack the user's tabs
  // or: await page({ match: 'mail.google.com' })        // reuse an existing tab only when the task needs it
  await p.click('button.save');        // real mouse events at the element centre
  await p.type('hello'); await p.key('Enter');           // modifiers: 1 Alt, 2 Ctrl, 4 Meta, 8 Shift
  await p.waitFor(`!!document.querySelector('.done')`);
  const data = await p.eval(`[...document.querySelectorAll('h2')].map(h => h.textContent)`);
  await p.upload('input[type=file]', ['photo.jpg']);    // no OS file dialog
  await p.screenshot('step.png'); log('done', data);
  await p.close();
}
```
- `p.send(method, params)` sends any raw CDP command to that tab; `cdp.send(...)` sends browser-level ones.
- Events: `await p.send('Page.enable')`, then `await waitEvent('Page.loadEventFired', { sessionId: p.sessionId })`. Events also work through the relay.
- Downloads: `await downloadsTo('out')`. Files arrive named by GUID with no extension. Wait for `Browser.downloadProgress` with `state: 'completed'`, then rename.

## Tab cleanup
- `run` closes every tab the job opened when it finishes, throws, or gets Ctrl+C.
- Tabs a job opens are also recorded in `~/.cdp-opened.json` with the job's PID. If the job is killed outright (timeout, closed terminal), the next `tabs`/`eval`/`run`/`cleanup` closes those tabs. Tabs of jobs still running, and the user's own tabs, are never touched.

## Gotchas
- Synthetic `el.click()` doesn't open file choosers, menus, or some React handlers. Use `p.click()` (real mouse events) or `p.upload()`.
- Some pages (e.g. Google Photos) render nothing while their tab is in the background. Hidden tabs already avoid this; for `visible: true` tabs call `await p.front()` first.
- If `p.click()` times out, the element is probably hidden or zero-size. Take a screenshot and inspect it before retrying.
- A stale `DevToolsActivePort` file stays behind after the browser closes. A connect error after that usually means the browser isn't running.

## Safety
- The connection has full control of the user's logged-in browser. Only do what the user asked.
- Never read, print or export cookies, passwords, tokens or localStorage secrets.
- Ask before anything outward-facing or hard to undo: sending messages, posting, submitting forms, purchases, deleting.
- The relay listens on 127.0.0.1 only and requires the random token in `~/.cdp-relay-token` (`~/.cdp-relay-token-<port>` for another `CDP_RELAY_PORT`), which is deleted on exit. Any process running as the user can still read that file, so don't leave the relay running unattended.
