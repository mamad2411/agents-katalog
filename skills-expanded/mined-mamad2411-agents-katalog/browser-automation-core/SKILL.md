---
name: browser-automation-core
description: "Shared reference for the browser-automation cluster: the surface model (web/DOM vs native macOS UI), the session lifecycle (one-shot vs persistent vs supervised-TTY), the recon-then-act selector strategy, and the debug-first evidence rule every spoke shares. USE WHEN choosing an automation engine, targeting elements, or deciding what counts as proof a UI works."
cluster: browser-automation
version: 1.0.0
---

# Browser Automation Core

Shared model for the `browser-automation` cluster. The drivers all differ in *what they touch* and
*how long they live* — keep these concepts consistent here so no spoke contradicts another.

## 1. The decision the cluster turns on: which surface?

Everything starts with one question — **what are you actually driving?** There are two surfaces,
and they do not overlap:

```
                 ┌─ Web / DOM surface ─────────────┐      ┌─ Native OS surface ────────────┐
your target ──→  │ a page in a Chromium browser    │  OR  │ a desktop app's real UI         │
                 │ → selectors, accessibility tree │      │ → OS accessibility elements     │
                 │ → browser / webapp-testing      │      │ → peekaboo                      │
                 └─────────────────────────────────┘      └─────────────────────────────────┘
```

- **Web/DOM** — anything rendered in a browser. You target **CSS selectors / ARIA refs** inside the
  page. Drivers: `browser` (headless Chromium, debug-first) and `webapp-testing` (Playwright against
  a local dev server).
- **Native OS UI** — a real macOS application *outside* any browser (menus, windows, the Dock, a
  native dialog). You target **OS accessibility elements** by ID/query/coords. Driver: `peekaboo`.

**Rule:** decide the surface before anything else. A web page is never a `peekaboo` job; a native
menu bar is never a Playwright job. Picking the wrong surface is the #1 way these tasks fail.

## 2. Session lifecycle (the second axis)

| Model | Lives for | Use it for | Spoke |
|---|---|---|---|
| **One-shot diagnostic** | a single command | "load URL → screenshot → report errors" | `browser` |
| **Persistent browser** | until 30-min idle | many queries against one loaded page; cookies carry over | `browser` (auto-session) |
| **Server-backed test** | a scripted run | local dev app + Playwright flow, dev-server managed for you | `webapp-testing` |
| **Persistent native** | snapshot cache | drive a desktop app across many steps | `peekaboo` (snapshot IDs) |
| **Supervised TTY** | until killed | REPLs, TUI agents, parallel sessions over a socket | `tmux` |

Sessions auto-start on first use (`browser`) and auto-clean on idle; `tmux` sockets and `peekaboo`
caches you manage explicitly. **Close what you open** — stop servers, kill sockets, quit apps.

## 3. Recon-then-act: never guess a selector

Every spoke follows the same loop: **observe the live state, then act on what you found.**

- **`browser`** — the primary command already returns a screenshot + console + network in one shot;
  query `console` / `network` / `failed` to dig.
- **`webapp-testing`** — `goto` → **wait for `networkidle`** → screenshot / read DOM → act on
  discovered selectors. Inspecting before `networkidle` on a dynamic app is the classic pitfall.
- **`peekaboo`** — `see --annotate` produces an annotated UI map with element refs (B1, T2, …);
  target those refs, not raw coordinates, whenever possible.

Refs/snapshots are invalidated by navigation — **re-snapshot after every `goto` or window change.**

## 4. Targeting matrix

| Surface | Discover with | Target by | Driver |
|---|---|---|---|
| Web (any URL) | `browser` diagnostics / screenshot | CSS selector | `browser` |
| Web (local dev) | Playwright `networkidle` + DOM read | `text=` / `role=` / CSS / id | `webapp-testing` |
| Native macOS | `peekaboo see --annotate` | element ref / `--app` + query / coords | `peekaboo` |
| Interactive TTY | `capture-pane` scrape | `send-keys` to `session:window.pane` | `tmux` |

## 5. The debug-first evidence rule (cluster's defining stance)

Debugging visibility is **on by default**, not opt-in. Console logs, network requests, and errors
should already exist when a problem appears — you don't enable logging *after* the failure.

**Therefore: you cannot claim a page or UI "works" until you have looked at the rendered evidence.**
A change is verified only when you have (a) the screenshot of the actual rendered state, AND (b) a
clean console + network read (no uncaught errors, no failed requests). Screenshots taken by any spoke
must be surfaced (Read the PNG) so they're actually seen — an unseen screenshot proves nothing.

## 6. Conventions

- **Headless by default.** Run headless; only open a visible browser when the user says "show me",
  honoring `$BROWSER` (fall back to the system default).
- **macOS permissions.** `peekaboo` needs **Screen Recording + Accessibility** — confirm with
  `peekaboo permissions` before driving native input.
- **TTY input safety.** When sending to TUI agents over `tmux`, send the text and `Enter` as
  **separate** `send-keys` calls with a small delay; a fast text+Enter can be swallowed as paste.
- **Least surface.** One tab / one window / one element at a time; widen only when needed.

## 7. Shared guardrails

- Decide the **surface** (web/DOM vs native OS) before choosing a tool.
- **Recon before action**: discover selectors/refs from a live snapshot; never hardcode guesses.
- **Evidence before claims**: no "it works" without a seen screenshot + clean console/network.
- Headless by default; visible only on explicit request.
- Confirm macOS permissions before native control; treat any new permission as a stated change.
- Close sessions, stop servers, kill sockets, quit apps when the task ends.
