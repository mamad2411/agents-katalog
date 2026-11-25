---
name: uniffy-playwright
description: |
  Use the project MCP infrastructure to inspect the running app from a coding agent. Covers the Playwright MCP servers for headless-browser automation against the dev UI - navigate, snapshot, evaluate JS, capture console + network, and debug runtime state without leaving the conversation.

  TRIGGER when: the user asks you to "open the app", "click around", "check the browser", "use playwright", "drive the UI", "screenshot the page", "inspect runtime state in the browser", "check the console", "verify a fix in the running app", or log in as a named user; the user offers "do you want to connect to mcp"; a bug needs in-browser reproduction and the dev stack is running; you need to read live YDoc / Redux / window state to confirm a hypothesis.

  SKIP when: the user is asking about MCP / Playwright in general (not the project's setup); the task is pure backend, code-only, or covered by reading tests/logs; the dev stack is not running and the user hasn't asked you to start it.
---

# Uniffy MCP Infrastructure

The project ships Playwright MCP servers inside docker so supported coding agents can drive real Chrome sessions against the dev UI. This skill is the operating manual.

## What runs

Two identical Playwright MCP containers - the second exists purely to give multi-user tests a **separate browser** (isolated cookie jar + `localStorage`):

| Container | MCP server | Host port | Purpose |
|---|---|---|---|
| `uniffy-mcp-playwright` | `playwright` | `8931` | Primary browser. Default for single-user work. |
| `uniffy-mcp-playwright-b` | `playwright-b` | `8932` | Second, fully isolated browser. Use as the **second user** in cross-session tests. |

Both run the same baked image `uniffy-mcp-playwright` (`.docker/dev/mcp-playwright.Dockerfile`), with separate ports and persistent profile volumes. Claude Code uses the SSE endpoints from `.mcp.json`:

```json
{ "mcpServers": {
    "playwright":   { "type": "sse", "url": "http://localhost:8931/sse" },
    "playwright-b": { "type": "sse", "url": "http://localhost:8932/sse" }
} }
```

Codex uses the Streamable HTTP endpoints from `.codex/config.toml`:

```toml
[mcp_servers.playwright]
url = "http://localhost:8931/mcp"

[mcp_servers.playwright-b]
url = "http://localhost:8932/mcp"
```

Both start under the `dev` profile (`docker compose --profile dev up` / `./manage.py stack up`). Compose config: `.docker/compose/dev-tools.yaml`. The image bakes `@playwright/mcp` + `chrome-for-testing` + `chromium-headless-shell` so the first request after a cold start does not stall on a 100MB+ download. Separate `pw-profile-a` and `pw-profile-b` volumes keep the two browser identities isolated and persistent across container restarts.

After adding or starting a server, refresh MCP connections with `/mcp` when the host supports it, or restart the agent session. Tool namespace prefixes are host-generated; select tools from the `playwright` or `playwright-b` server by their `browser_*` names.

## Reaching the dev UI

The browser runs inside the docker network. Its localhost is **not** the development host's localhost. Use the docker-internal hostname:

- Frontend: `http://host.docker.internal:5173`
- Backend API: `http://host.docker.internal:8000`

The Vite dev server's `server.allowedHosts` includes `host.docker.internal` (see `src/ui/vite.config.ts`). Other hostnames produce `Blocked request. This host ... is not allowed.` - if you see that, the URL is wrong.

## Default credentials (dev only)

**Every seeded user shares one password** = `$INITIAL_ADMIN_PASSWORD` (default `admin`). All belong to the org **"Uniffy"** (the org card on `/welcome`).

| Email | Username | Name | Org role | Notes |
|---|---|---|---|---|
| `admin@uniffy.io` | admin | System Administrator | OWNER | also `is_system_admin` |
| `alice@uniffy.io` | alice | Alice Johnson | MEMBER | Engineering (member) |
| `bob@uniffy.io` | bob | Bob Smith | MEMBER | Engineering (admin) |
| `charlie@uniffy.io` | charlie | Charlie Brown | MEMBER | Engineering + Product (member of both) |
| `diana@uniffy.io` | diana | Diana Prince | MEMBER | Product (admin) |
| `eve@uniffy.io` | eve | Eve Martinez | MEMBER | Product (member) |

Groups (org "Uniffy"): **Engineering** {alice, bob(admin), charlie} and **Product** {charlie, diana(admin), eve}. `charlie` is intentionally in both, to exercise multi-group permission resolution.

Source of truth: `src/uniffy/db/seed.py` (admin + org) and `src/uniffy/db/seed_dev.py` (the 5 test users + 2 groups; only seeded when `ENVIRONMENT=development`).

The auth form has two `Sign in` buttons (mode switcher + submit). To submit, target `[data-testid="auth-submit-login"]` directly.

## Two-user (cross-session) testing

For anything that needs two users at once - sharing, permission grants, live cross-session updates, "create as A, confirm B sees it" - **use the two containers as two browsers.** They have separate cookie jars + `localStorage`, so the users never collide.

### Preferred: two containers (one user per browser)

- **User A -> `playwright` server** (port 8931). **User B -> `playwright-b` server** (port 8932).
- Log each user in once in its own browser via the login recipe below. No tab juggling, no identity-swap trap - you may `browser_navigate` / reload freely in either browser.
- Both browsers hit the same dev UI (`http://host.docker.internal:5173`) and each opens its own notification stream, so a server push fired by A's action arrives in B's browser independently.
- If the `playwright-b` tools are missing, the `-b` container is not up or MCP has not reconnected - see "Operating the containers".

### Browser isolation

Use separate browser contexts or the two containers for separate users. Auth rotation lives in
`uniffy:auth` storage and synchronizes across tabs. A login as another user retires the first tab's
session, so two tabs in one browser profile cannot represent independent users. Same-user multi-tab
tests remain supported. Never print tokens or cache-key seeds in tool output.

## Login recipe

The login `<input>` elements are typed-only via direct DOM events in newer React versions; the MCP `browser_type` selectors sometimes parse the textbox role oddly and throw. The reliable pattern is `browser_evaluate` to set values via the native `value` setter so React picks them up:

```js
const email = document.querySelector('input[type="email"], input[autocomplete="email"]');
const pwd = document.querySelector('input[type="password"]');
const setVal = (el, v) => {
  const set = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
  set.call(el, v);
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
};
setVal(email, 'admin@uniffy.io');
setVal(pwd, 'admin');
```

Then `browser_click` on `[data-testid="auth-submit-login"]`. A user with one organization lands on `/`; if the tab lands on `/welcome` instead, click the **Uniffy** card under Your organizations.

## Core MCP tools

| Tool | When to use |
|---|---|
| `browser_navigate` | Start of every session + page transitions. |
| `browser_snapshot` | Accessibility tree for the current page. Use this before clicking - it gives `ref=eXX` ids you can target. |
| `browser_click` / `browser_type` | Standard interactions. Use `target` = `ref=eXX` from the snapshot, OR a CSS / `data-testid` selector. |
| `browser_evaluate` | The escape hatch. Run arbitrary JS in the page context. Reach `window.__milkdownEditor`, `window.__milkdownEditorView`, Redux store (`window.store` if exposed), CSS-only queries, Y.Doc internals. |
| `browser_console_messages` | Pull console logs. Pass `level: "error"` + `all: true` to inspect everything since session start. |
| `browser_network_requests` | Inspect XHR/WebSocket traffic. Filter with the `filter` regex param. |
| `browser_take_screenshot` | Visual verification. Prefer `browser_snapshot` for action targeting (cheaper, structured). |
| `browser_press_key` / `browser_wait_for` | Keyboard shortcuts, async waits. `browser_wait_for` accepts `time` (seconds), `text`, or `textGone`. |

## Inspecting Yjs / Milkdown state

The notes editor exposes globals for debugging:

- `window.__milkdownEditor` - the Crepe-wrapped Milkdown editor
- `window.__milkdownEditorView` - the underlying ProseMirror `EditorView`

To read live YDoc state (e.g. confirm `Y.Text("markdown")` is being mirrored from PM transactions):

```js
const view = window.__milkdownEditorView;
for (const p of view.state.plugins) {
  const st = p.getState ? p.getState(view.state) : null;
  if (st?.binding?.doc) {
    const doc = st.binding.doc;
    const ytext = doc.share.get('markdown');
    const frag = doc.share.get('prosemirror');
    return {
      ytextLen: ytext?._length,
      ytextSample: ytext?.toString().slice(0, 200),
      fragmentLen: frag?.length,
    };
  }
}
```

The `y-sync$` plugin holds the binding; its `state.binding.doc` is the live `Y.Doc`.

## Operating the containers

Both services live in `.docker/compose/dev-tools.yaml`; add `mcp-playwright-b` to any command to act on the second browser (or omit the service name to act on both).

| Action | Command |
|---|---|
| Build / rebuild image | `docker compose build mcp-playwright` (one image, shared by both) |
| Start both | `docker compose --profile dev up -d mcp-playwright mcp-playwright-b` (or `./manage.py stack up -d`) |
| Start only the 2nd | `docker compose --profile dev up -d mcp-playwright-b` |
| Logs | `docker logs uniffy-mcp-playwright-b --tail 100 -f` |
| Restart (after image rebuild) | `docker compose restart mcp-playwright mcp-playwright-b` |
| Tear down | `docker compose --profile dev down mcp-playwright mcp-playwright-b` |

After editing the Dockerfile, rebuild and restart - running containers keep the old image until then. After starting or adding a server, reconnect MCP with `/mcp` or restart the agent session so the `playwright-b` tools become visible.

## Selector gotchas

- **`ref=eXX` snapshot refs are NOT accepted by `browser_click` in this build** - it throws `browserBackend.callTool: Unknown engine "ref"`. Click via `browser_evaluate` instead: find the element (by text / `data-testid` / `title`) and call `.click()` on it. Treat the snapshot refs as read-only locators for *finding* things, not as click targets.
- **`window.store` is NOT exposed** - reading Redux via `window.store.getState()` returns undefined. Read state from the **DOM** instead (e.g. tree section contents, header avatar initials), or from `localStorage.getItem('persist:root')` (note: that's the *persisted* snapshot, which can lag/diverge from a tab's live in-memory state - see two-user testing).
- `browser_type` with `target` as the snapshot's `textbox` role description sometimes throws `Unexpected token while parsing css selector`. Fall back to `browser_evaluate` with the native `value`-setter pattern (the login recipe) - it's the reliable way to fill any React-controlled input.
- Tree nodes in the notes sidebar are not always React-routable links - many fire via `onClick` on a `div[data-node-id="..."]`. Use `browser_evaluate` to click the chevron `<button>` child to expand a folder before clicking the leaf.
- `strict mode violation: resolved to N elements` means the selector is ambiguous. Prefer `data-testid` attributes, or filter to the visible one (`el.offsetParent !== null`).

## Workflow template

1. `browser_navigate` to `http://host.docker.internal:5173`.
2. `browser_snapshot` - confirm page state.
3. If unauthenticated, run the login recipe above.
4. Navigate to the failing surface (`/notes/<id>`, `/chat/...`, etc).
5. `browser_console_messages` with `level: "error", all: true` to capture any uncaught errors.
6. `browser_evaluate` for runtime state confirmation (YDoc, Redux, window globals).
7. `browser_take_screenshot` only when the user asks for visual evidence - the accessibility tree is faster and cheaper.
