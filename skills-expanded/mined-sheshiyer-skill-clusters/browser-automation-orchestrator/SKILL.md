---
name: browser-automation-orchestrator
description: "Route a browser / UI automation task to the right driver among the cluster's specialists — debug-first headless Chromium, local-webapp Playwright testing, native macOS UI capture and control, and the interactive-TTY harness that supervises them. USE WHEN a user wants to drive, screenshot, scrape, test, or verify a web page or desktop UI but hasn't named which engine or session model to use."
cluster: browser-automation
version: 1.0.0
---

# Browser Automation Orchestrator

The single entry skill for browser and UI automation work. It places the task on the
**surface × session-model** map — *what are you driving* (the web/DOM layer vs the native OS UI
layer) and *how long does the driver live* (one-shot vs persistent) — and delegates to one of
the specialist spokes. The cross-cutting model every spoke shares — the two automation surfaces,
the session lifecycle, the selector/targeting strategy, and the debug-first evidence rule — lives
in `browser-automation-core`; read it before choosing an engine or claiming a UI "works".

## Cluster map (spoke → role)

- **`browser`** — debug-first headless Chromium driver. Console logs, network requests, and page
  errors are captured by **default**; primary command navigates + screenshots + reports diagnostics
  in one shot. The go-to for "load this URL and tell me what's broken."
- **`webapp-testing`** — Playwright toolkit for **local** web apps. Manages dev-server lifecycle
  (`scripts/with_server.py`), then runs native Python Playwright scripts using a
  reconnaissance-then-action pattern (wait for `networkidle`, inspect DOM, act on discovered selectors).
- **`peekaboo`** — native **macOS UI** automation CLI (off the DOM, on the OS): capture/inspect
  screens, target accessibility elements, drive click/type/drag/scroll, manage apps/windows/menus.
  The `see → click → type` flow is the reliable path. (Requires Screen Recording + Accessibility.)
- **`tmux`** — interactive-TTY harness. Drives REPLs and TUI coding agents by sending keystrokes and
  scraping pane output over an isolated socket; the supervisor that runs the above drivers in
  parallel sessions and waits on prompts.

## Routing rules (intent → spoke)

**Web / DOM surface (Chromium)**
- "Open this URL, why is it broken?" / verify a deployment / capture console + network → `browser`
- Test or dogfood a **local** dev app, manage the dev server, write a Playwright flow → `webapp-testing`
- Quick screenshot or one-shot diagnostic of any reachable URL → `browser`
- Multi-step form / login / upload flow against a running app → `webapp-testing` (or `browser` for ad-hoc)

**Native OS / desktop surface (macOS)**
- Screenshot or read a **desktop app** (not a web page) → `peekaboo`
- Click/type/drag inside a native app, drive menus, windows, the Dock → `peekaboo`
- "What's on screen?" / annotate UI elements before acting → `peekaboo see --annotate`

**Harness / supervision**
- Drive an interactive REPL or a TUI agent (Claude Code, Codex) → `tmux`
- Run several automation sessions in parallel and poll for completion → `tmux`

## Standard flow

1. **Pick the surface first.** Web page / DOM → `browser` or `webapp-testing`. Native desktop UI →
   `peekaboo`. Interactive TTY → `tmux`. This is the dividing line of the whole cluster.
2. **Pick the session model.** One-shot diagnostic → `browser`. Server-backed local test loop →
   `webapp-testing`. Long-lived interactive supervision → `tmux`.
3. **Recon before you act.** Snapshot/inspect (`browser` diagnostics, `peekaboo see --annotate`,
   Playwright `networkidle` + DOM read) to discover real selectors/refs — never guess.
4. Delegate to the spoke(s). Compound asks fan out by surface (e.g. "test the web app *and* the
   menu-bar helper" → `webapp-testing` + `peekaboo`).
5. Return: chosen spoke(s), the surface + session model, the selectors/refs used, and the evidence
   captured (screenshot path, console/network state).

## Guardrails

See `browser-automation-core`. In short: **headless by default** — only open a visible browser when
the user says "show me." **Evidence before claims** — never assert a page or UI "works" without
having looked at the rendered screenshot AND its console/network diagnostics. **Recon before action** —
discover selectors/refs from a live snapshot, don't hardcode guesses. **Least surface** — drive the
narrowest target (one tab, one window, one element); close sessions / kill sockets when done.
Native control (`peekaboo`) needs explicit macOS permissions — confirm them before driving input.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills —
only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above,
**load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
