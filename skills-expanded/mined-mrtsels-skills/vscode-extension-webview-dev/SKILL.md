---
name: vscode-extension-webview-dev
description: Use when building or debugging VS Code extension webviews.
license: MIT
metadata:
  hermes:
    tags:
    - vscode
    - extension
    - webview
    - webviewview
    - csp
    - manifest
    related_skills:
    - vscode-extension-review
    - deepseek-harness
  source_frontmatter:
    version: 1.0.0
    author: Hermes Agent
  imported_from: hermes
---

# VS Code Extension Webview Development

Building activity-bar / sidebar webview views and debugging blank (white) screens. The pain points
below were all hit for real (2026-08) while embedding a vendored vite-built React UI into a
WebviewView — each one caused a white screen or a stuck loading state.

## Debug discipline (user expectation)

When a webview behavior is unexplained, **read the official docs and the installed VS Code's own
source before retrying** — not repeated trial-and-error restarts. Two fast sources:
- Extension guide: `code.visualstudio.com/api/extension-guides/webview`
- Installed VS Code's webview preload: `src/vs/workbench/contrib/webview/browser/pre/index.html`
  (via GitHub/jsdelivr, or `npx @electron/asar extract-file app.asar <path>`); the CSP check,
  nonce injection and html-rewrite logic all live there.
Also: go read the extension host logs yourself (`~/Library/Application Support/Code/logs/<latest>/window*/exthost/exthost.log`) instead of making the user collect them.

## Manifest declarations (package.json contributes)

- **A WebviewViewProvider view MUST declare `"type": "webview"`** in `contributes.views`,
  otherwise VS Code treats it as a tree view and reports
  `There is no data provider registered that can provide view data` even though you registered a
  `registerWebviewViewProvider`. Reference: claude-code extension declares
  `{"type": "webview", "id": "claudeVSCodeSidebar", ...}`. A plain TreeDataProvider view needs no type field.
- **ChatParticipant requires a `chatParticipants` contribution.** Newer VS Code throws
  `chatParticipant must be declared in package.json: <id>` from `createChatParticipant` if absent.
  The participant `name` must match `/^[\w-]+$/` — **no spaces** (`DeepSeek Harness` rejected).
  **Use LOWERCASE** (`deepseekharness`): the official docs say "lowercase name, title-case
  fullName", and a camelCase name (`DeepSeekHarness`) is the prime suspect for a participant that
  silently never responds — user types `@DeepSeekHarness`, gets no prompt, no output, no error.
  `fullName: "DeepSeek Harness"` is what the UI displays. A malformed contribution can fail the
  whole contributes block and take unrelated views down with it.
- **A throwing registration mid-activate aborts everything after it** (later registrations never
  run — classic cause of "view exists but no provider"). Wrap optional API registrations
  (chat participants, etc.) in try/catch with a log, so the core view provider still registers.
  BUT for core entry points (chat participant = a product feature, not an accessory): a silent
  `logger.warn` degrade means the user sees *nothing* and reports "没响应". Make the failure
  visible — `showWarningMessage` with the error, so the next reload surfaces the real cause
  instead of a mystery dead feature.

## Webview CSP (the white-screen trap)

- VS Code's webview preload checks for the CSP meta with
  `querySelector('meta[http-equiv="Content-Security-Policy"]')` — **exact uppercase, value-sensitive**.
- **Warning semantics (verified from 1.133 source): `handleNoCspFound` only fires the
  `created a webview without a content security policy` warning — it does NOT inject a fallback
  CSP and does NOT touch your script tags.** So a CSP warning alone does NOT blank the page; the
  blank screen has a different root cause (below). Don't burn hours on the warning — the meta
  exists, scripts run anyway (prove with a minimal test page).
- `script-src 'nonce-x'` only covers the entry `<script>` tag. **ESM module imports (vite chunks)
  are governed by script-src too** → also allow the webview's own origin:
  `script-src 'nonce-${nonce}' ${webview.cspSource}`.
- **`'unsafe-eval'` is REQUIRED for most vite/bundled production UIs.** Minified bundles keep an
  `eval`/`new Function` path; without it the module throws
  `Uncaught EvalError: Evaluating a string as JavaScript violates ... 'unsafe-eval' is not an
  allowed source of script` and the whole module aborts mid-execution → white screen, no error
  visible to the page's own `window.onerror` (the EvalError fires before your handler matters, or
  as an uncaught error). The browser version of the same UI "just works" because it serves no CSP.
  Full working CSP for a local bundle + local backend:
  `default-src 'none'; style-src ${csp} 'unsafe-inline'; script-src 'nonce-x' 'unsafe-eval' ${csp};
  img-src ${csp} data: blob:; font-src ${csp} data:;
  connect-src http://127.0.0.1:3080 ws://127.0.0.1:3080; worker-src ${csp} blob:;`
  Comment in the HTML why unsafe-eval is present (auditors will flag it).
- **Relative URLs in the bundle need `<base href="<webview-uri-of-bundle-root>/">`** in the html
  head. Manifest/plugin URLs like `./plugins/x/client.js` resolve against the webview origin, not
  your extension path — without the base tag they 404.
- **BASE HREF MALFORMATION (a multi-round white-screen root cause):** build the base from an
  explicit directory URI — `webview.asWebviewUri(Uri.joinPath(extensionUri, 'dist', 'web', 'bundle')) + '/'`.
  Do NOT build it via `asWebviewUri(asUri('.'))` where `asUri('.')` is
  `joinPath(extensionUri, ..., '.')` — that yields a malformed base (`…/bundle/.`) and every
  relative URL in the bundle 404s → white screen. **The trap is that Chrome-headless validation
  PASSES** because its test page uses a clean directory base (`http://127.0.0.1:8091/`), so you
  can burn many rounds "validated in Chrome but white in VS Code". Validate with the exact same
  base shape the webview will get, and when the real environment disagrees with Chrome, stop
  guessing and instrument the real page (banner + probes below) on the FIRST report.
- **`location.reload()` inside a webview loses the injected html.** The iframe reloads VS Code's
  preload shell, not your `webview.html` string → blank. To "reload" a webview, re-set
  `webview.html = buildHtml(webview)` from the extension side (round-trip a postMessage from the
  page to the extension to trigger it).
- No inline scripts (CSP forbids them): put boot/config data in a separate nonce'd .js file, or
  inline the file's contents into a nonce'd `<script>` (inline + nonce is allowed).

## Bundling vite / upstream UIs into a webview

- vite builds split **dynamic-import chunks** (e.g. shiki `./langs/*.js`). Fetching only the
  html-referenced entry assets (index/vendor js+css) is NOT enough — the chunk tree must be
  fetched recursively (scan each fetched JS/CSS for relative refs) or runtime dynamic imports 404
  and the UI never mounts (stuck loading screen).
- Webview origin is `vscode-webview://...` — any library deriving its API base from
  `location.origin` will hang trying to reach a fake authority. Patch the vendored bundle to point
  at the real backend, or inject config.
- `webview.options.localResourceRoots` must cover the bundle directory; reference files via
  `webview.asWebviewUri(uri)`; `enableScripts: true`.

## Debug channel (webview → extension log)

- **Page-visible error banner + render probes beat the console**: when the user reports a blank
  webview, instrument the INJECTED PAGE — fixed red strip at top appending capture-phase
  error/unhandledrejection/module-load-fail, plus T+2s/T+5s probes of `#root`
  (`children=` + `innerHTML.length` → mounted vs not), `document.styleSheets.length` (CSS 404?),
  `getComputedStyle(document.body).backgroundColor` (transparent survived the theme plugin?), root
  rect, first-child tag/class. One user reload then returns the exact failure — no DevTools, no
  extension-log digging. Info probes must not pollute the banner. Full recipe + timing trap
  (sync boot script runs BEFORE the module tag parses — `querySelector('script[type="module"]')`
  null at boot time is normal, not a bug): see `references/white-screen-debugging.md`.
- In a nonce'd boot script add:
  `window.addEventListener('error', …)` + `unhandledrejection` → `acquireVsCodeApi().postMessage({type:'debug', kind, message})`,
  logged extension-side. Surfaces webview console errors without DevTools.
- Extension `console.log` does NOT appear in exthost.log — it goes to the Debug Console /
  Output → "Extension Host" channel. Don't grep exthost.log for it.
- `pnpm build` / failed `pnpm install` can wipe `dist/` — if the webview 404s, verify the
  bundle directory actually exists on disk before debugging further.

## Architecture-First Workflow (user correction, 2026-08-18)

When modifying code in a project with architecture documentation (like ARCH.md), **read the architecture doc first** to locate the relevant files and understand the module structure. Do NOT start by searching the codebase with grep/find — this wastes time on irrelevant files.

**Correct workflow:**
1. Read ARCH.md (or equivalent) → identify the module directory map and file→function lookup table
2. Locate the specific files that need changes
3. Read those files, then make targeted edits

**Wrong workflow (user corrected):**
1. Start grep-searching for keywords across the entire codebase
2. Read random files hoping to find the right one
3. Make changes after unnecessary traversal

This applies to any project with structured documentation (ARCH.md, CONTRIBUTING.md code organization section, etc.).

## Build Pipeline Knowledge (dsh-for-vs-code specific)

For projects with a build pipeline that generates shell/CSS/JS artifacts:

- **Source of truth** for CSS and injected JS is in the build script (e.g. `build-web-shell.mjs`), NOT in `dist/` artifacts
- The build script contains template strings for `shell.css` and `bridge.js` — edit the template, not the dist file
- After editing the build script, run the build script to regenerate dist files
- React components (e.g. `SessionView.tsx`) are built separately via esbuild → `dist/web/session-view.js`
- Copy the built session-view.js to `dist/web/dsh-shell/` for the webview to load

## dsh-for-vs-code: Plugin Exclusion Pitfall (EXCLUDE_PLUGINS)

When `build-web-shell.mjs` prunes plugins via `EXCLUDE_PLUGINS`, **check slot occupancy dependencies before excluding**. The `WorkspacePicker` component gates the "Add workspace..." menu item on `flowAvailable`, which depends on the `conversation.hero.workspace.directoryFlow` slot having an occupant. Excluding `ui-directory-picker-browse` removes the occupant → `flowAvailable = false` → menu item disappears.

**Debugging path for missing upstream UI elements:**
1. Is the element rendered by React? → Check source for render conditions (JSX ternaries, early returns)
2. Is a required slot/provider missing? → Trace slot occupancy chain
3. Only THEN check CSS clipping

**Do NOT assume CSS clipping when a UI element is missing.** The user was frustrated by repeated CSS edits when the real issue was plugin exclusion. Check DOM existence first (`document.body.innerText.includes("text")`), then React render conditions, then CSS.

## dsh-for-vs-code: VS Code Native Directory Picker Pattern

**Root cause of missing "Add workspace..."**: `EXCLUDE_PLUGINS` in `build-web-shell.mjs` removes `ui-directory-picker-browse`, which is the occupant of `conversation.hero.workspace.directoryFlow` slot. No occupant → `flowAvailable = false` → menu item not rendered.

**Correct approach** (not browse, not listDirectory):

上游有两个 directory-flow 实现：
- `ui-directory-picker-browse`：renderful in-app 浏览器，调 `host.listDirectory`（列出目录内容）
- `ui-directory-picker-native`：**renderless**，调 `host.pickDirectory`（选择一个目录）

Route A 应排除 browse、保留 native。native occupant 不渲染任何 UI，直接调 `host.pickDirectory` RPC。

```
WorkspacePicker → "Add workspace..."
  → NativeDirectoryFlow (renderless, no in-app browser)
  → ctx.workspaces.pickDirectory()
  → host.pickDirectory RPC
  → proxy 拦截 → vscode.window.showOpenDialog()
  → user picks folder → return path
  → onPicked(path) → workspace 创建
```

Implementation:
1. In `build-web-shell.mjs` EXCLUDE_PLUGINS: remove `dsh-client-ui-directory-picker-native`, keep `dsh-client-ui-directory-picker-browse` excluded
2. Add `pickDirectory` callback to `HttpProxy`: `async (): Promise<string | null>`
3. In `handleHttp`, intercept POST to `/api/host.pickDirectory` (NOT `/api/host.listDirectory`)
4. Parse `rpcId` from request body, return proper envelope

**Wire envelope for `host.pickDirectory`** (Zod-validated):
```json
{
  "type": "server-response",
  "rpcId": "<from request body>",
  "result": { "ok": true, "value": { "path": "/selected/path" } }
}
```
Cancel: `{ "path": null }`. Missing `type`/`rpcId` or wrong `value` shape causes Zod validation error.

**Pitfall: intercepting `host.listDirectory` instead of `host.pickDirectory`**
- `listDirectory` = "give me children of a directory" (returns `{ path, home, crumbs, entries, truncated }`)
- `pickDirectory` = "let me choose a directory" (returns `{ path: string | null }`)
- Intercepting listDirectory with showOpenDialog is semantically wrong AND causes the in-app browser to render (because browse plugin is still loaded). The user sees a broken UI, not a native picker.

**Debugging path for missing upstream UI elements:**
1. Is the element rendered by React? → Check source for render conditions (JSX ternaries, early returns)
2. Is a required slot/provider missing? → Trace slot occupancy chain
3. Only THEN check CSS clipping

**Do NOT assume CSS clipping when a UI element is missing.**

## Smoke Test Interpretation

When comparing before/after smoke test results:
- Count failures before changes, then after — a decrease means you fixed something
- Pre-existing failures (especially Phase 10 attachment tests in headless mode) are NOT regressions
- Focus on whether YOUR specific changes introduced new failures, not the absolute failure count

## Smoke Test Screenshot Capture

For capturing real webview screenshots (not SVG mockups) using the smoke test infrastructure:

**Prerequisites**: dsh web instance running on port 3080, Playwright available in vendor/deepseek-harness.

**Setup**: Create a static server for the shell dist + a relay proxy to bypass Origin restrictions. Use the same pattern as `smoke-shell.mjs`.

**Key environment variables for the webview**:
- `__DSH_WEB_URL__` — relay proxy URL (e.g. `http://127.0.0.1:8958`)
- `__DSH_HOST__` — set to `'sidebar'`
- `__DSH_BOOT_SESSION__` — `{ sessionId: '<real-session-id>' }` from `session.list` RPC

**Capturing different views**:
- Chat panel: just wait 10-12 seconds after navigation
- Session management: `await page.evaluate(() => window.__dshBridge?.setView('sessions'))` then wait 5 seconds

**Pitfall**: Do NOT manually toggle DOM elements to simulate view changes — this bypasses React rendering and produces incorrect screenshots. Always use `bridge.setView()` for session management.

**See also**: `vscode-extension-publishing` skill for the full publishing workflow including README image requirements.

## Launching the extension host

- F5 debug: if `Extension host did not start in 10 seconds`, drop `preLaunchTask` from launch.json
  (build manually) to shrink the failure surface; verify activation in exthost.log
  (`ExtensionService#_doActivateExtension <id>`).
- `code` may be missing from PATH — use the full path
  `/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code`.
- Aggressive `pkill` of VS Code can leave LaunchServices wedged: `open -a` / `code` start a main
  process but no window ever appears. The user's own F5 debug window is often the stable path;
  check `~/Library/Application Support/Code/logs/<latest>/` for `window*/` dirs to confirm a window exists.
