---
name: remote-hands-operator
description: Use when automating computer tasks via Remote Hands, controlling web browsers, interacting with native macOS applications, switching between windows and tabs, or executing cross-app desktop workflows.
---

# Remote Hands Operator

Unified system operator skill for controlling web browsers, native macOS desktop applications, terminal workspaces, and window environments at maximum speed through Remote Hands (`rh`).

## Overview

Remote Hands turns the host operating system into an ultra-low latency, deterministic automation canvas. This skill dictates how agents navigate between running browser profiles, manage application windows, execute coding instructions, and request user approvals without exploratory stalls or UI disruption.

## When to Use

- Operating web browsers on active, authenticated user profiles.
- Switching between browser tabs or finding specific open documents/pages without creating duplicates.
- Automating native macOS desktop software (VS Code, Xcode, Finder, Slack, Terminal, System Settings).
- Performing end-to-end tasks spanning both codebase files and GUI applications.
- Guiding the user visually using targeted UI arrows and highlight annotations.
- Requesting mobile human approval before publishing, financial, or destructive operations.

## When NOT to Use

- Plain HTTP requests for public static web data where `curl` or standard fetch suffices without browser sessions.
- Isolated filesystem edits where no GUI inspection, browser interaction, or desktop window management is required.

## Speed Mandate: Zero Discovery

Agents operating Remote Hands must begin execution immediately on the primary objective.
Exploratory diagnostic commands are strictly forbidden:
- Never run `which rh`, `rh --help`, `rh browser --help`, `rh desktop --help`, `rh profiles`, or test approval calls.
- All CLI utilities (`rh browser`, `rh desktop`, `rh guide`, `rh approve`) are pre-installed in `PATH` and available instantly.
- Jump directly to the relevant files, tabs, or application windows.

## MCP tools (preferred)

When the `rh-computer` MCP server is registered with your agent (`rh mcp install`), prefer its tools over shell commands. They run in one warm process, so each call is much faster than spawning `rh`, and each action returns the fresh compact UI state, so a separate snapshot after every step is not needed.

| Tool | Purpose |
|---|---|
| `desktop_snapshot` | List the controls and text of an app window as `[index] role "label"` with state, field values and scroll hints. Indexes stay the same while an element stays on screen. Optional `app`, `filter` (role/label substring) and `index` (read only that list or pane (up to 400 lines), from a `… N more in [id]` line; ids from outside it are unavailable until the next full snapshot). |
| `desktop_click` | Press an element by index from the latest `desktop_snapshot` through native Accessibility. Optional `action`: `open`, `menu`, `double`, `right`. |
| `desktop_type` | Type text into the focused element, or into the field at `index` (`replace` swaps its content, `submit` presses Return). |
| `desktop_scroll` | Scroll the list or area at `index` up/down/left/right when the snapshot says `… N more below`. |
| `desktop_read` | Read the full text of an element by `index` (never password fields). |
| `desktop_drag` | Drag one element onto another (`from`, `to`). |
| `desktop_key` | Press a key or shortcut such as `return` or `cmd+s`. |
| `desktop_open` | Launch or activate an app and return its UI state. |
| `desktop_menu` | Fuzzy-search an app menu bar and trigger the best match. |
| `desktop_windows` | List open windows as `App - Title`. |
| `browser_tabs` | List browser tabs. |
| `browser_focus` | Switch to an existing tab by index, URL substring or title; returns the page state. |
| `browser_open` | Open a URL (reuses a matching tab) and return the page state. |
| `browser_snapshot` | Re-read the interactive elements of the active tab as `[id] role "label"`. |
| `browser_click` | Click a page element by its stable id; returns the new page state. |
| `browser_type` | Type into a page element by its stable id (optional `submit` presses Enter); returns the new page state. |
| `browser_find` | Search a large page for elements matching a query (optional `limit` 1-20) and return only the best matches. |
| `browser_do` | Run 1-30 browser steps (`click`, `type`, `select`, `check`, `hover`, `press`, `scroll`, `wait`) in one call, naming elements by stable id or by visible `target` label, and return the final page state. |
| `browser_extract` | Read the visible page text (optional `max_chars` 200-20000) when you need to read content, not find controls. |
| `computer_batch` | Run up to 12 tool calls in one round trip. |

Rules:
- Same-app rule: `desktop_click`, `desktop_type` with an index, `desktop_scroll`, `desktop_read` and `desktop_drag` must target the same app as the latest `desktop_snapshot`. Omit `app` on both calls or pass the same app to both, otherwise the call fails.
- Browser ids (the numbers in brackets) are stable: they stay valid while the element stays on the page. Every browser action result already contains the updated state, so never call `browser_snapshot` again after an action.
- Use `browser_do` to fill and submit a whole form or run any multi-step browser sequence in one call, with ids from the last state you saw. Use `target` (the visible label) when you have not seen the page yet; ambiguous labels fail with candidates. Open shadow DOM and same-origin iframes are included; large frames that cannot be read (other websites, sandboxed) are reported in a note. Labels are matched among the controls visible on screen, using a fresh look at the page at the start of the call, and fail, asking for an `index`, when the page has more controls than could be listed or the label is not unique. Use `browser_find` before dumping a big page and `browser_extract` to read long text. `browser_focus` and `browser_open` reuse existing tabs.
- If a browser result begins with `note: fast browser path unavailable`, do not mention it to the user and continue with the fallback. If a `browser_*` tool fails because the browser is not Chrome, drive that browser with `desktop_snapshot`, `desktop_click` and `desktop_type` using its app name. Never run `rh browser setup` yourself: it is interactive.
- Desktop indexes are only valid until the next snapshot or action. If an error says `no longer present` or `not in last snapshot`, call `desktop_snapshot` again and use the fresh indexes.
- When the user names a Mac app (Music, Messages, Notes, Finder…), do the task inside that app with the `desktop_*` tools: open it, click its Search, type with `submit`, open the result. Never open the app's website or an https link instead, and do not use curl or osascript to search or play.
- `desktop_click` presses by Accessibility with no mouse movement. If the element does not support `AXPress`, it may fall back to a physical click at the element center. The result then includes a `note:` line saying so. This is expected; do not retry.
- `computer_batch` validates every step first and stops at the first failure. Index-based steps (`desktop_click`, `browser_click`, `browser_type`) refer to the UI state after the previous step, which you have not seen, so batch only steps that need no index, with at most one index-based step first or last. For browser sequences use `browser_do` instead.
- The zero-discovery and zero-screenshot mandates apply unchanged to the MCP tools.

The `rh browser` and `rh desktop` shell commands below remain available as a fallback when the MCP tools are not registered or a tool does not cover the action.

## Browser Automation & In-Place Tab Continuity

Chrome is pre-launched and authenticated with the user's primary personal profile (logged into Google, GitHub, X, etc.).

### Tab Continuity Rules
- Never query or read local SQLite cookie files or Keychain passwords.
- Always inspect existing open tabs before navigating to avoid opening duplicate windows or tabs.
- If the required service or URL is already open in any window or tab, focus that existing tab directly in-place.
- Never steal window focus unnecessarily; keep user workflows uninterrupted.
- ZERO MOUSE MOVEMENT: `rh browser click <index>` and `rh browser type <index>` interact directly via CDP or native Accessibility without moving the physical mouse pointer. Never write ad-hoc Swift or Python scripts (such as `CGEvent`, `screencapture`, `pyautogui`, `Quartz`).
- ZERO SCREENSHOTS: All web automation runs on structured DOM accessibility trees. Never take screenshots or write image recognition scripts.

### Jev Ultrafast Decision Policy
- **One operation per cycle:** Advance the user's goal from the CURRENT page with the single best operation.
- **Page text context:** Read the page text returned by `rh browser snapshot` for state and questions; do not re-read or guess.
- **Autonomous survey & form filling:** When asked to complete a survey, form, questionnaire, or multi-step web workflow, drive it autonomously to 100% completion. Inspect each step (`rh browser snapshot`), pick the best answer matching user instructions with `rh browser click <index>`, fill text inputs with `rh browser type <index> "<text>"`, and click Next/Submit until the survey is completely done.
- **Do not repeat satisfied steps:** If a radio button or checkbox is already `[checked]`, do NOT click it again.
- **Fill required fields before submitting:** Type values into required inputs before clicking Next or Submit.
- **Fast submission:** When Next, Continue, Search, or Submit is visible and inputs are ready, click it immediately.

### Browser Workflow

1. Inspect open tabs:
```bash
rh browser tabs
```

2. Focus an existing tab by index, title, or URL substring:
```bash
rh browser focus "github.com"
```

3. Open a URL only if not already open (reuses matching tabs automatically):
```bash
rh browser open "https://github.com/pulls"
```

4. Inspect the interactive DOM elements:
```bash
rh browser snapshot
```

5. Click interactive elements by numeric index:
```bash
rh browser click 14
```

6. Type into inputs by numeric index:
```bash
rh browser type 3 "Antigravity Remote Hands"
```

### Browser Automation Principles

- Strictly use `rh browser snapshot`, `rh browser click <index>`, and `rh browser type <index> "<text>"`.
- NEVER run external debugger scripts or CDP WebSocket attach tools (such as browser-harness).
- Native accessibility and direct CDP events are triggered seamlessly with zero mouse movements and zero debug popups.

## Native Desktop & Window Management

Control native macOS software using accessibility-driven inspection, native accessibility actions, and menu bar search.

### Zero Screenshots & Instant Accessibility Mandate

Never capture screenshots or run vision loops for desktop automation. Screen capture is strictly prohibited during autonomous execution. Never write ad-hoc Swift or Python automation scripts (`CGEvent`, `screencapture`, `pyautogui`, `Quartz`) and never move the physical mouse cursor. Speak directly to the application layer using Accessibility APIs and native menu commands:
- `rh desktop menu-search <app> "<item>"`: Trigger any application menu item instantly (<5ms)
- `rh desktop menu-list <app>`: Inspect available native application menus
- `rh desktop ax-action <app> <index> [action]`: Execute accessibility action directly on a control (e.g. `AXPress`) with zero mouse movement
- `rh desktop key <combo>`: Send native keyboard shortcuts
- `rh desktop snapshot [--no-ocr]`: Fast semantic inspection of the UI element hierarchy (use `--no-ocr` for pure native AX)

### Window Operations

1. List all active application windows:
```bash
rh desktop window list
```

2. Focus a native window:
```bash
rh desktop window focus "Visual Studio Code"
```

3. Open or launch an application:
```bash
rh desktop open "Slack"
```

### UI Interaction

1. Snapshot the native UI hierarchy:
```bash
rh desktop snapshot --no-ocr
```

2. Execute direct accessibility action on control (instant <5ms, no mouse movement):
```bash
rh desktop ax-action "Bambu Studio" 5 AXPress
```

3. Fuzzy search and execute application menu bar items instantly:
```bash
rh desktop menu-search "Bambu Studio" "Import 3D Model"
```

4. List application menu hierarchy:
```bash
rh desktop menu-list "Bambu Studio"
```

5. Click a native control by numeric index:
```bash
rh desktop click 5
```

6. Type into the focused control:
```bash
rh desktop type "New Project"
```

7. Execute keyboard shortcuts:
```bash
rh desktop key "cmd+s"
rh desktop key "enter"
```

8. Select application menu bar items:
```bash
rh desktop menu "Code" "File" "Save All"
```

9. High-level goal automation:
```bash
rh desktop act "create a new file named test.py"
```

## Interactive Guidance Overlays

When the user asks "how do I...", "where do I click...", "point to...", or "show me where to...":
Do NOT click the button autonomously. Project an interactive arrow overlay over the target UI element.

### Browser Guidance
```bash
rh guide show --browser --index=12 --text="Click to create repository"
```

### Desktop Guidance
```bash
rh guide show --desktop --app="Slack" --target="Channels" --text="Find project channel"
```

### Guidance Navigation
```bash
rh guide next
rh guide dismiss
```

## Human-in-the-Loop Approval Protocol

Before performing sensitive, irreversible, financial, or public actions:
- Publishing or posting content to social media (X, LinkedIn).
- Deleting files, branches, or repositories.
- Sending emails or direct messages.
- Submitting payments or subscriptions.
- Deploying to production environments.

You MUST request approval on the user's paired mobile device:
```bash
rh approve "Post announcement tweet to @account: Launching Remote Hands 2.0" --risk=high --action=publish
```

### Protocol Handling
- Exit status `0`: Human approval granted. Execute the action immediately without asking again.
- Exit status `1`: Approval rejected. Read stderr for the user's rejection reason (`Approval rejected by user: <reason>`). Modify the proposed content or action according to the feedback and re-request approval, or terminate if instructed.
- When resuming with `[HUMAN APPROVAL GRANTED]`, proceed directly to execution.

## Quick Reference

| Action | Command |
|---|---|
| List browser tabs | `rh browser tabs` |
| Focus browser tab | `rh browser focus <index\|url\|title>` |
| Open URL (with auto-reuse) | `rh browser open "<url>"` |
| Snapshot browser DOM | `rh browser snapshot` |
| Click browser element | `rh browser click <index>` |
| Type into browser field | `rh browser type <index> "<text>"` |
| List desktop windows | `rh desktop window list` |
| Focus desktop window | `rh desktop window focus "<app>"` |
| Snapshot desktop UI | `rh desktop snapshot [--no-ocr]` |
| Execute accessibility action | `rh desktop ax-action <app> <index> [action]` |
| Search and trigger menu | `rh desktop menu-search <app> "<item>"` |
| List app menu bar items | `rh desktop menu-list <app>` |
| Click desktop element | `rh desktop click <index>` |
| Type desktop text | `rh desktop type "<text>"` |
| Send keyboard shortcut | `rh desktop key "<combo>"` |
| Select menu item | `rh desktop menu "<app>" "<menu>" "<item>"` |
| Show browser guidance arrow | `rh guide show --browser --index=<idx> --text="<msg>"` |
| Show desktop guidance arrow | `rh guide show --desktop --app="<app>" --target="<btn>" --text="<msg>"` |
| Request phone approval | `rh approve "<summary>" [--risk=high] [--action=publish\|delete\|push\|pay\|send]` |

## Common Mistakes & Rationalization Table

| Rationalization / Mistake | Reality & Correct Behavior |
|---|---|
| "I should run `rh --help` to inspect arguments." | Never run discovery commands. All commands match the syntax in this guide. |
| "I should capture screenshots or use vision to find buttons." | Never take screenshots. Use `rh desktop snapshot --no-ocr`, `rh desktop ax-action`, or `rh desktop menu-search` directly. |
| "I need to open a new tab for each site." | Always check `rh browser tabs` first. Switch to existing tabs in-place with `rh browser focus`. |
| "I should scrape SQLite cookie databases to authenticate." | Chrome is already authenticated with the user's active session. Use the browser directly. |
| "I will click the button for the user when they asked 'where is'." | When asked 'where is' or 'how do I', use `rh guide show` to project an interactive arrow. |
| "I can post or delete without approval if the prompt said 'do it'." | Irreversible or public actions strictly require `rh approve` before execution. |
| "The user rejected my approval so I should retry the exact same request." | Read the rejection reason from stderr, revise the content or approach, and re-request approval. |
| "I should write a Swift or Python script with CGEvent or pyautogui to click." | Strictly prohibited. Never move the physical mouse pointer. Use `rh browser click` for web elements and `rh desktop ax-action` for desktop controls. |

