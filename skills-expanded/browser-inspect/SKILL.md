---
name: browser-inspect
description: Browser inspection and interaction for verifying rendered web UI during development.
usedBy: [coder]
relatedTo: [agent-browser, chrome-devtools-mcp]
version: 0.1.0
lastUpdated: 2026-09-12
---

## Purpose

An agent editing UI code cannot confirm that the result is correct by reading source files alone. CSS can be purged or overridden, client-side JS only runs in the browser, and server-rendered markup may differ from what the template suggests. Without looking at the live page, an agent is guessing. This skill codifies how to inspect, interact with, and verify rendered web UI using two complementary tools that serve different purposes.

## Procedure

### 1. Tool selection

Two tools exist for browser work. They are not interchangeable — the distinction is **which browser instance** you connect to.

- **agent-browser:** Spins up its own fresh session. Use for autonomous tasks: testing, form automation, screenshots, clean-state QA.
- **Chrome DevTools MCP:** Attaches to the user's live browser. Use for collaborative debugging: inspecting existing state, auth sessions, HMR.

**agent-browser** is a free CLI tool — harness-agnostic, works everywhere, no API key:

```bash
npm install -g agent-browser
agent-browser install   # downloads Chrome for Testing (first time only)
```

Verify it before use: run `command -v agent-browser`. If it is missing, show the user the two install commands above and stop. Installing a global npm package and downloading a browser are system changes — the user runs them or explicitly approves them first. Once installed, continue.

Always use `--engine chrome`. Lightpanda has no rendering engine and cannot display visual output.

**Chrome DevTools MCP** is an MCP server — requires registration in the harness's MCP config. If the MCP server is not available, ask the user to add it to `opencode.json` (project) or `~/.config/opencode/opencode.json` (global):

```json
{
  "mcp": {
    "chrome-devtools": {
      "type": "local",
      "command": ["npx", "-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

The harness must be restarted after adding the config. The MCP server starts Chrome automatically on first tool use.

**When to use which:**

- **agent-browser** for clean-state verification: "does this component render correctly from scratch?" Fresh context, no cookies, no auth, no prior state. Good for automated testing loops and screenshots.
- **Chrome DevTools MCP** for live-state debugging: "why does this look wrong in my browser right now?" Inherits the user's session — auth, localStorage, cookies, in-flight HMR state. The user and agent see the same tab simultaneously. Returns structured CDP responses directly, fewer round-trips for tight debugging loops.

Default to agent-browser for autonomous work. Switch to Chrome DevTools MCP when the user asks you to inspect something they're already looking at, or when reproducing the bug requires state that's hard to reconstruct.

### 2. The verification loop

After every UI change, run this cycle:

1. Edit the source file(s).
2. Rebuild / let the watcher handle it.
3. Server reloads and serves at `localhost:<port>`.
4. **Inspect** the rendered result (CSS, console, DOM state).
5. **Interact** with the component (click, fill, navigate).
6. **Read the screenshot** to visually confirm. Fix issues, repeat.

Never assume a component is correct without looking at it in the browser.

### 3. Inspection with agent-browser

**CSS.** Check whether classes are actually applied to rendered elements:

```bash
agent-browser get styles "h1"
agent-browser get styles "@e3"          # use refs from a prior snapshot
```

Diagnose: missing classes (purged or misspelled), specificity conflicts, responsive breakpoint issues, or dynamic classes that weren't generated.

**Console errors.** After any UI change, always check for runtime errors:

```bash
agent-browser console                   # view console logs
agent-browser errors                    # view page errors only
```

**Network traffic.** When the UI makes server requests, inspect them:

```bash
agent-browser network requests          # list captured requests
```

**DOM state.** Evaluate client-side state via JS when the framework exposes it:

```bash
agent-browser eval "document.title"
agent-browser eval "document.querySelectorAll('.my-class').length"
```

### 4. Interaction with agent-browser

**Core workflow: snapshot, ref, interact.** Always follow this sequence:

```bash
# 1. Navigate to the page
agent-browser open http://localhost:3000/page

# 2. Get the accessibility snapshot with interactive element refs
agent-browser snapshot -i

# 3. Interact using stable refs (@e1, @e2, etc.)
agent-browser click @e3

# 4. Re-snapshot after any state change
agent-browser snapshot -i

# 5. Capture an annotated screenshot
agent-browser screenshot --annotate /tmp/component-state.png
```

Refs are scoped to the current snapshot. After any navigation, client-side state change, or DOM update, take a new snapshot before using refs. Never reuse refs across page states.

**Forms.** Fill fields and trigger blur/validation:

```bash
agent-browser snapshot -i
agent-browser fill @e2 "test value"
agent-browser press Tab                  # trigger blur/validation events
agent-browser snapshot -i
agent-browser screenshot --annotate /tmp/input-filled.png
```

**Dropdowns and modals.** Hidden content (via `display: none`, `visibility: hidden`, or conditional rendering) won't appear until triggered. Click the trigger first, then re-snapshot to get refs for the now-visible elements:

```bash
agent-browser click @e4              # open dropdown/modal
agent-browser snapshot -i            # get refs for visible content
agent-browser click @e7              # select an option
agent-browser snapshot -i            # verify state updated
```

**Waiting for async operations.** After triggering a server request or animation, wait before re-snapshotting:

```bash
agent-browser click @e5              # trigger a request
agent-browser wait networkidle       # wait for network to settle
agent-browser snapshot -i
agent-browser screenshot --annotate /tmp/result.png
```

**Responsive testing.** Compare viewport sizes to verify responsive behavior:

```bash
agent-browser set viewport 375 812
agent-browser screenshot --annotate /tmp/mobile.png

agent-browser set viewport 1280 800
agent-browser screenshot --annotate /tmp/desktop.png
```

**Reading screenshots.** After taking an annotated screenshot, always read the file to close the loop. The annotation overlay shows element refs on top of the rendered page — both visual layout and interactive targets are visible together.

### 5. Inspection with Chrome DevTools MCP

When using Chrome DevTools MCP (attached to the user's live browser), the MCP tools provide direct access to CSS, console, network, and DOM state without navigation — you're already on the page the user is looking at.

Use it for: checking computed styles on an element the user is pointing out, reading console errors from a sequence they just triggered, evaluating Alpine/React/Vue state in the live session, or inspecting network responses from an interaction they just performed.

The MCP tools return structured CDP responses. There is no snapshot/ref workflow — you identify elements by CSS selector or coordinate, same as you would in DevTools.

## Guardrails

- Never assume a rendered component is correct from source code alone. Styling, client-side behavior, and server interactions can only be verified in the browser.
- Never reuse agent-browser refs across page states. Any navigation, state change, or DOM update invalidates existing refs — always re-snapshot first.
- Never use Lightpanda — it has no rendering engine and cannot display visual output.
- Never use Chrome DevTools MCP for autonomous testing workflows — it depends on the user's browser state which may not be reproducible. Use agent-browser for clean-state verification.
- Never use agent-browser to debug a live user session — it spins up a fresh browser and cannot access the user's cookies, auth state, or in-flight application state. Use Chrome DevTools MCP instead.
