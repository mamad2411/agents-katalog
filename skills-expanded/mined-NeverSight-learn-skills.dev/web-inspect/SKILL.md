---
name: web-inspect
description: Point-and-comment frontend review. User pins elements in their running dev app, types bug comments, and clicks "Send" — the skill receives the batch and fixes each bug sequentially. Use when the user says "review the frontend", "inspect the web app", "I annotated some bugs", "/web-inspect", or wants to test their UI and feed visual feedback back to a coding agent.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Web Inspect

Live point-and-comment QA for frontend apps. The user runs their dev server, opens the app in a browser, pins elements with bugs, types comments, and sends batches to the agent. The agent fixes each bug sequentially in the source.

## How it works

1. **Boot** — `node {{scripts_path}}/start.mjs` starts a small HTTP+SSE helper server, injects the overlay `<script>` into the project's HTML entries, prints a JSON blob with `{ port, token, devUrl, pageFiles }`.
2. **User tests** — User opens their dev URL in a browser. Overlay floats over the page. They click elements, leave comments, and click **Send to agent** when ready.
3. **Poll** — Agent runs `node {{scripts_path}}/poll.mjs` in a loop. The helper server holds the request open until the browser sends a batch (or 10 min timeout).
4. **Fix** — Each batch contains N annotations. Agent triages, then fixes one at a time in the main thread, proposing each change before applying (auto mode applies directly).
5. **Repeat** — After fixing, agent polls again. The user keeps testing and sends more batches.
6. **Exit** — User says stop, or the helper server is killed. Skill runs `node {{scripts_path}}/start.mjs stop` to restore the HTML files.

The helper runs on a random localhost port with token auth. The PID file lives inside the skill directory at `.runtime/state.json`, so nothing is written to the project root.

## Setup gates

Before any other action, pass these checks. The first failure stops the skill.

| Gate | Required check | If fail |
|---|---|---|
| Auto-detect | `start.mjs` scans for `pageFiles` (`index.html` or common locations) and `devUrl` (parsed from `package.json`). | If `start.mjs` returns `error: "needs_user_input"`, run **First-time setup** (below). |
| Page files | At least one HTML entry actually exists on disk. | Tell the user which paths were tried; ask for the correct one and re-run with `--page`. |

## Run

```bash
node {{scripts_path}}/start.mjs
```

Output JSON:
```json
{
  "ok": true,
  "port": 8401,
  "token": "...",
  "devUrl": "http://localhost:7776",
  "pageFiles": ["index.html"],
  "configDrift": { "orphans": [] }
}
```

If `{ ok: false, error: "needs_user_input", missing, detected }` — run First-time setup.
  - `missing` lists which fields couldn't be resolved (`pageFiles`, `devUrl`, or both).
  - `detected` shows what was found (use it to suggest defaults to the user).
If `{ ok: false, error: "no_page_files", tried }` — show the user which paths were tried; ask for the correct path and re-run with `--page`.
If `{ ok: true, devUrlGuessed: true }` — the dev URL was inferred from a framework default; confirm it with the user before telling them to open it.

After a successful start, **tell the user**:
> "Helper running on port `{port}`. Open `{devUrl}` in your browser, pin any bugs, and click **Send to agent** in the overlay when you're ready."

## Poll loop

```
LOOP:
  node {{scripts_path}}/poll.mjs    # default long timeout; no --timeout=
  Read JSON; dispatch on "type":

  "batch"   → Handle Batch; LOOP
  "timeout" → LOOP (no message to user)
  "exit"    → break → Cleanup
```

### Harness policy

- **Claude Code**: run the poll as a **background task**. The harness notifies you when it completes; the main conversation stays free.
- **Cursor**: run the poll in the **foreground** (blocking shell — not a background terminal, not a subagent). Cursor background terminals do not reliably resume the chat with poll stdout.
- **Codex**: run the poll in the **foreground** (blocking shell). Codex background exec does not reliably surface poll stdout back to the conversation.
- **OpenCode / Gemini / others**: foreground unless you've verified stdout reliably returns.

Never pass a short `--timeout=`. The poll script's default (600000 ms) is correct.

## Handle `batch`

Event shape:
```json
{
  "type": "batch",
  "id": "abc12345",
  "batchId": "...",
  "sessionDescription": "Optional overall repro context typed by the user",
  "annotations": [
    {
      "id": "1",
      "comment": "This button doesn't fire on tablet width",
      "url": "http://localhost:7776/p/abc",
      "viewport": { "w": 1280, "h": 800 },
      "element": {
        "selector": "button.save-btn",
        "outerHTML": "...",
        "textContent": "Save",
        "tagName": "button",
        "id": "",
        "classes": ["save-btn"],
        "boundingRect": { "x": 100, "y": 200, "w": 80, "h": 32 },
        "computedStyles": { "...": "..." },
        "componentName": "SaveButton",
        "sourceFile": "src/client/components/SaveButton.tsx",
        "sourceLine": 12,
        "cssSources": [
          { "source": "src/styles/buttons.scss", "line": 23, "column": 4, "selectorText": "button.save-btn" }
        ]
      },
      "screenshotPath": "/abs/path/.agents/skills/web-inspect/.runtime/sessions/<id>/ann-1.png",
      "consoleErrors": [
        {
          "level": "error",
          "message": "...",
          "ts": 1234567890,
          "stack": "Error: ...\n    at ...",
          "stackResolved": [
            { "source": "src/client/components/SaveButton.tsx", "line": 14, "column": 22, "name": "onClick", "raw": "at onClick (https://localhost:5173/...js:1234:5)" }
          ]
        }
      ],
      "networkErrors": [
        { "url": "...", "method": "POST", "status": 500, "duration": 230, "ts": 1234567890 }
      ]
    }
  ]
}
```

Process the batch in this order:

### 1. Triage

Print a numbered summary to the user. One line per annotation:

```
Got 3 bugs:
  1. SaveButton — "doesn't fire on tablet width" (src/client/components/SaveButton.tsx:12)
  2. <header> — "logo overlaps menu at <500px"
  3. /api/snippets request returning 500 — "save fails silently"
```

If `sessionDescription` is present, print it as a one-line preamble.

### 2. Locate source — fallback chain

For each annotation, find the source file in this order. The first match wins.

The first two steps use **source-map-resolved positions** captured by the overlay against the dev server's bundles. They're available whenever the dev server emits source maps (Vite/webpack/Next/etc. do by default). When absent, the chain falls through to the existing grep-based heuristics.

1. **`consoleErrors[*].stackResolved[0]`** — for any annotation whose comment names a runtime error, or whose `consoleErrors` are non-empty: walk `stackResolved` arrays and take the first frame whose `source` is a user file (not `node_modules`, not `vite/dist`). The frame's `source:line:column` is the failing call site. Confidence: highest for runtime-error bugs.
2. **`element.cssSources[0]`** — for visual / styling bugs ("padding wrong", "logo overlaps"), use the top entry. If `line` is non-null, jump straight to `source:line`; if null, open `source` and grep for `selectorText` within that single file. Confidence: highest when `line` present, high when file-only.
3. **`element.sourceFile` + `element.sourceLine`** — if present (React fiber `_debugSource` in dev builds), open that file. Confidence: highest for React component bugs.
4. **`element.componentName`** — grep for `function {name}`, `const {name} =`, `class {name}`, `<{name}` across the project. If a single source file is the obvious owner, use it. Confidence: high.
5. **Unique text content** — pick the longest unique substring of `element.textContent`, grep for it. If exactly one source file matches, use it. Confidence: medium.
6. **Class name + tag** — for stylesheet-only bugs (no `cssSources`), grep for `.{class}` in `.css`/`.scss`/`.module.css`/Tailwind utility patterns. Confidence: medium for visual bugs only.
7. **Fail open** — if none match, tell the user: "Couldn't locate the source for bug N. Annotation has selector `X`, text `Y`. Where should I look?" Don't guess.

If the bug is from `networkErrors`, also search by API path — it often points straight at the failing call site.

### 3. Read the screenshot

`annotation.screenshotPath` is an absolute PNG path. **Read it before proposing a fix.** The screenshot encodes layout context not recoverable from `outerHTML` alone (parent elements, sibling overlap, viewport-specific rendering).

### 4. Propose, then fix (sequential)

For each annotation, in order:

a. **Propose** — one or two sentences: what's wrong, what file:line you're going to change, what the change is. In auto mode, skip the explicit confirmation step but still print the proposal so the user sees it.

b. **Fix** — apply the edit. Keep the change minimal and targeted to the reported symptom. Don't refactor surrounding code, don't rename variables, don't "improve while you're here." If the bug needs a deeper change than expected, surface that as a separate proposal before doing it.

c. **Move on** — print `Fixed {N}. {file:line}` and proceed to the next annotation.

After the batch:
- Print `Batch done — {N} fixes across {M} files. Reload the page to verify.`
- Run `node {{scripts_path}}/poll.mjs` again. Stay in the loop.

### 5. Hard rules during processing

- **Never** modify the overlay's HTML markers in user files. The overlay markers are a server-side concern.
- **Never** disable user-agent-stylesheet defaults or `data-web-inspect-*` attributes — those are overlay state.
- **Don't write tests** for these fixes unless the user asks. Frontend annotation fixes are usually visual; tests come from the user's existing flow.
- If two annotations target the same component, fix them in a single edit when possible. Two edits to the same file in one batch is fine; ten is a smell — pause and consider grouping.

## First-time setup

If `start.mjs` returns `{ ok: false, error: "needs_user_input", missing, detected }`:

1. Look at `missing` and `detected` to know what to ask.
   - If `devUrl` is missing, ask: "What URL does your dev server run on? (e.g. `http://localhost:5173`)"
   - If `pageFiles` is missing, ask: "Which HTML file is your app's entry point? (e.g. `index.html`, `public/index.html`)"
2. Re-run with the provided values:
   ```
   node {{scripts_path}}/start.mjs --page <html> --dev-url <url>
   ```
3. The skill writes `web-inspect.config.json` next to `SKILL.md` so subsequent runs are silent.
   No files are written to the project root.

For non-Vite, non-Node frameworks (Laravel, Rails, plain HTML on a remote dev server), `start.mjs` cannot inject the script tag itself if the entry is server-rendered. In that case, it prints a `<script>` tag the user must paste once into their dev layout (gated by `APP_ENV=local` / `Rails.env.development?` / similar). The skill should print that tag verbatim and tell the user to add it to their dev-only template, then continue.

## Cleanup

When the user says "stop", "exit", or you receive an `exit` event:

```bash
node {{scripts_path}}/start.mjs stop
```

This:
- Sends an exit signal to the helper server (it shuts down)
- Removes the injected `<script>` tag from every file in `pageFiles`
- Deletes the PID file

If the helper is already gone (crashed, user killed it), `stop` still cleans up injected tags by scanning HTML files for the marker comments — no config needed.

## Output discipline

The user is watching a live dev session — chat is overhead. Spend tokens on tools and edits, not on prose.

- One short sentence after the boot output: "Open the dev URL and start pinning bugs."
- Numbered triage list when a batch arrives.
- One line per fix: proposal sentence, then `Fixed {N}. {file:line}`.
- One line at the end of each batch: `Batch done. Reload to verify.`
- No recap, no tutorial output, no praise, no summary of what just happened.

## Anti-patterns

- **Don't ask the user to describe the bug in chat.** The annotation comment IS the description — re-asking defeats the entire purpose of this tool.
- **Don't fix a bug that wasn't annotated** even if you notice one nearby. The user's attention is on what they pinned. Anything else is scope creep.
- **Don't open issues, write PRs, or commit during the session.** Just edit. Commits are the user's call after they verify.
- **Don't auto-reload the user's browser.** They may want to compare before/after themselves.
