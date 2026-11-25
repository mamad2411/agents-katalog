---
name: chrome-session
description: "Playwright in the user's own logged-in Chrome (Playwright MCP Chrome extension). Use whenever the user says playwright, for auth-walled pages (Overleaf comments/threads JSON, Google Scholar, university portals), for public sites whose bot wall (Cloudflare 'Just a moment…', 403, CAPTCHA) blocks curl/read/headless browsers, and for user-requested form actions in their accounts (job alerts, settings, portal forms). One agent tab in its own tab group (background daemon, idle auto-close); never touches the user's tabs; no approval dialog once the token is saved."
---

# chrome-session: the user's logged-in Chrome, via Playwright extension

One helper, `scripts/chrome_session.py`. The first command starts a background
daemon that owns one `@playwright/mcp --extension` session and therefore ONE
tab in the agent's own tab group; every later command reuses that tab over a
Unix socket (`$XDG_RUNTIME_DIR/chrome-session-<uid>.sock`, log `….sock.log`).
The daemon closes the tab and exits after `CHROME_SESSION_IDLE` seconds idle
(default 600) or on `stop`. The user's tabs are invisible to it.

## Why this tool (checked 2026-09-28, Linux, Chrome 153)

| Option | Verdict |
|---|---|
| Playwright MCP `--extension` (this skill) | Uses the default profile's logins; agent sees only its tab group; token skips the approval dialog |
| Chrome DevTools MCP `--autoConnect` | Works, but Chrome shows an Allow dialog on every new server connection, and the agent sees every open window |
| `--remote-debugging-port` (Stagehand `connect`, browser-use, DevTools `--browser-url`) | Chrome ≥136 ignores it on the default profile: needs a separate profile and a second login |
| ego-lite | macOS only; Linux is roadmap |
| Copying the Cookies DB | Encrypted with the OS keyring key; sites re-challenge anyway. Do not |

## Prerequisites (check first)

1. Chrome has the **Playwright Extension** (Chrome Web Store id `mmlmfjhmonkocbjadbfplnigmagldckm`).
2. Token file `~/.config/playwright-mcp/token.env`, mode 600:

       PLAYWRIGHT_MCP_EXTENSION_TOKEN=<value shown in the extension's status page>

   Or export the variable. The token is per Chrome profile; never print it.
3. Node/`npx` on PATH (first run downloads `@playwright/mcp`, ~30 s).

If the helper says `playwright-mcp exited`, the extension is missing or the
token is stale: ask the user to open the extension and copy the current token.

## Usage

    S=<skill dir>/scripts/chrome_session.py
    python3 $S text     https://scholar.google.com/citations?user=XXXX
    python3 $S fetch    https://www.overleaf.com/project/<id> /project/<id>/threads /project/<id>/ranges
    python3 $S eval     https://example.com "async () => document.title"
    python3 $S snapshot https://example.com
    python3 $S nav      https://example.com/next     # navigate only
    python3 $S eval     - "() => location.href"      # `-` = stay on the current page
    python3 $S tool     - browser_click '{"element":"Next","target":"e12"}'  # raw MCP tool call
    python3 $S schema   browser_click                # current argument schema of a tool (`all` lists names)
    python3 $S status                                # alive? current URL
    python3 $S stop                                  # close the tab now

- `fetch` runs same-origin `fetch()` inside the logged-in page, so cookies and
  CSRF context apply. Prints `{path: {status, body}}` JSON. Best choice for sites
  with JSON APIs. `fetch -` reuses the current page's origin.
- The final URL goes to stderr as `# landed on:` (extension token redacted:
  a fresh tab sits on the extension's `connect.html?…&token=` page); a login
  URL there means the user is not signed in to that site.
- Single tab, serial: commands queue on the daemon; do not run helpers in
  parallel. Page state (JS globals, open modals) persists between commands.
- Run `stop` when finished so the tab does not linger until the idle timeout.
- SPA pages: `text` right after navigation can be empty; use `nav`, then
  `eval - "async () => { await new Promise(r=>setTimeout(r,6000)); return document.body.innerText }"`.
- Clicks that navigate inside `eval` raise "Execution context was destroyed";
  the navigation still happened. Read the new page with a second `eval -`.
- Links that open new tabs: install `window.open=(u)=>{location.href=String(u);return window;}`
  before clicking, or better, find the target URL from
  `performance.getEntriesByType('resource')` / the site's JSON API and `nav` to it.

## Acting in pages (forms, buttons, dropdowns)

Use this only for the exact action the user asked for. Pattern that worked
(AcademicPositions job alert, 2026-10-24, `@playwright/mcp` 1.64):

1. `schema <tool>` before the first `tool` call of a session. Argument names
   change between releases: element arguments are now `target`, not `ref`
   (`ref` fails with `expected string, received undefined → at target`).
2. `target` takes a snapshot ref (`e12`, `f1e40`) or a Playwright selector.
   Prefer selectors (`button:has-text("Create a job alert")`, `select[name=type]`):
   refs go stale after every action, and `tool` output now links the snapshot
   as a `.playwright-mcp/*.yml` file instead of printing it.
3. Read the form state with `eval` instead of reading the whole snapshot:

       python3 $S eval - "() => [...document.querySelectorAll('input,select,textarea,button')].filter(e=>e.offsetParent!==null).map(e=>[e.tagName,e.type,e.name,e.placeholder,(e.type==='checkbox'||e.type==='radio')?e.checked:e.value,(e.innerText||'').slice(0,40)].join('|')).join('\n')"

   Prefilled values usually come from the page URL filters; report them.
4. Custom dropdowns often hide a native `<select>`: list its options with
   `eval` (`[...document.querySelector('select[name=type]').options].map(o=>o.value+':'+o.text)`),
   set it with `browser_select_option {"target":"select[name=type]","values":["weekly"]}`,
   then confirm both the `select` value and the visible button label changed.
5. After submit, check `Page URL` in the tool output and read the page. A
   redirect to a login/sign-up page means the action did NOT happen: stop, ask
   the user to sign in (or sign up) in the agent's tab-group tab. Never type
   passwords or create accounts for the user. After sign-in, check the account's
   own list (e.g. profile → Job-Alerts) BEFORE redoing the form: AcademicPositions
   saved the pending alert itself on the `?r=` return ("Ihre Job-Benachrichtigung
   wurde erstellt"), so a redo would have made a duplicate. If the agent tab
   still looks signed out, open the auth URL once; it redirects back with the session.
6. Bot-walled public sites (Cloudflare 403 for curl, `read` and headless
   Chromium) load normally here because this is the user's real browser. That
   does not override a site's terms: do the user's requested actions, not bulk
   collection.

## Recipe: Overleaf review comments

    python3 $S fetch https://www.overleaf.com/project/<id> \
        /project/<id>/threads /project/<id>/ranges /Project/<id>/doc/<docid>/download

- `threads`: `{threadId: {messages: [{content, timestamp, user: {first_name, last_name}}], resolved}}`.
- `ranges`: `[{id: docid, ranges: {comments: [{op: {p, c, t}}]}}]`; `p` is a
  character offset, `c` the anchored text, `t` the thread id.
- Doc download returns raw text; line number = count of `\n` before `p`. Check
  `text[p:p+len(c)] == c` before trusting the mapping.

## Rules

- Read-only by default. Never click, type, or submit in the user's accounts
  unless the user asked for that exact action; `tool` exists for those cases
  (see "Acting in pages").
- Do not navigate to URLs that trigger actions (logout, delete, confirm links).
- The helper deletes the `.playwright-mcp/` output directory it runs in; if you
  drive the MCP server another way, delete that directory yourself.
- OMP note: OMP silently drops MCP servers whose args contain `@playwright/mcp`
  while `browser.enabled` is true, so use the helper instead of registering it.
