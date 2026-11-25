---
name: hermes-browser-internals
description: "Understand, troubleshoot, and modify Hermes Agent's browser subsystem — tab lifecycle, session management, agent-browser CLI, CDP supervisor, cloud providers, and Chrome DevTools MCP."
version: 2.0.0
author: Hermes Agent (via the operator)
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [hermes, browser, tabs, cdp, agent-browser, play-wright, session-management]
    triggers: [browser tab, browser session, browser cleanup, agent-browser, browser tool not closing tabs, browser tool opens too many tabs, CDP supervisor, browser_tool.py, tab reuse, browser_tab_reuse]
    related_skills: [hermes-agent, stealth-browser-setup, native-mcp, building-mcp-servers]
---

# Hermes Browser Internals

This skill covers the internal architecture of Hermes Agent's browser subsystem — how tabs and sessions are created, managed, and cleaned up. Use it when you need to understand, troubleshoot, or modify browser behavior.

## Architecture Overview

Hermes has two parallel browser systems:

### 1. Native Browser Tools (`browser_*`)
**Source**: `tools/browser_tool.py` (~3900 lines)

Backed by the `agent-browser` CLI (a Node.js/Playwright-based automation tool). Supports multiple backends:
- **Local mode**: Spawns a headless Chromium via Playwright
- **Cloud mode**: Browserbase / Browser Use / Firecrawl (via `browser.cloud_provider` in config)
- **Camofox mode**: Local anti-detection Firefox via REST API (`tools/browser_camofox.py`)
- **CDP mode**: Connect to an existing browser via `browser.cdp_url` or `/browser connect`

Key modules:

| File | Purpose |
|------|---------|
| `tools/browser_tool.py` | All `browser_navigate`, `browser_click`, `browser_snapshot`, etc. tool implementations. Session lifecycle, cleanup thread, agent-browser CLI orchestration. |
| `tools/browser_supervisor.py` | Persistent CDP WebSocket supervisor per task. Handles dialog interception, frame detection, runtime evaluation via live CDP connection. |
| `tools/browser_cdp_tool.py` | Raw CDP passthrough (`browser_cdp` tool method) — escape hatch for low-level browser control. |
| `tools/browser_camofox.py` | Camofox REST API adapter for the browser tools. |
| `tools/browser_dialog_tool.py` | Dialog response tool using supervisor state. |
| `agent/browser_provider.py` | ABC for cloud browser providers (Browserbase, Browser Use, Firecrawl). |
| `agent/browser_registry.py` | Provider registry lookup. |

### 2. Chrome DevTools MCP (`mcp_chrome_devtools_mcp_*`)
**Config**: `npx chrome-devtools-mcp@latest`

Connects to a live Chrome instance via CDP and exposes native tab management tools:
- `mcp_chrome_devtools_mcp_list_pages` — list all open tabs
- `mcp_chrome_devtools_mcp_close_page` — close a specific tab by ID
- `mcp_chrome_devtools_mcp_new_page` — open a new tab
- `mcp_chrome_devtools_mcp_select_page` — switch focus
- `mcp_chrome_devtools_mcp_take_snapshot` — get accessibility tree of current page

## The Tab Creation Problem

**Root cause**: Every `browser_navigate("url")` call runs `agent-browser open <url>` which creates a **new tab** in the Chromium instance. There is NO mechanism to reuse an existing tab or close individual tabs after use.

The `agent-browser` CLI has:
- `open <url>` — always opens a new tab
- `close [--all]` — closes the **entire browser** (all tabs)
- `eval <js>` — runs JavaScript in the current tab's context

There is **no `close-tab` command** in agent-browser. There is **no tab-reuse logic** in `browser_navigate`.

### Session Cleanup (current behavior)

- A background thread checks every 30s for sessions inactive > `browser.inactivity_timeout` (default 120s)
- When a session is cleaned up, it runs `agent-browser close` which kills the **whole browser process** and all its tabs
- The agent-browser daemon also self-terminates after the same idle timeout (`AGENT_BROWSER_IDLE_TIMEOUT_MS`)
- Session cleanup only fires on idle — during active use, tabs accumulate without bound

## Fix Implementation (committed June 2026)

The fix was implemented in commit `feat(browser): tab reuse to prevent tab proliferation` on branch `feature/tab-reuse` (pmb2 fork). Three parts:

### Part 1: Tab Reuse in browser_navigate

Modified `browser_navigate` to distinguish first navigation from subsequent navigations via a `_first_nav` flag stored in `_active_sessions[task_id]`.

**First navigation**: `agent-browser open <url>` (creates the tab -- unchanged)

**Subsequent navigations**: `_try_navigate_same_tab(task_id, url)` which uses a 3-strategy cascade:

1. **CDP `Page.navigate`** (preferred for cloud/CDP sessions) -- reuses the existing tab via the CDP supervisor's persistent WebSocket and its new `navigate(url)` method
2. **`agent-browser eval "window.location.href = '<url>'"`** (local sessions without CDP supervisor) -- navigates the current page in-place via JavaScript
3. **`agent-browser open <url>`** (fallback) -- opens a new tab only if strategies 1 and 2 both fail

The `_try_navigate_same_tab` function in `tools/browser_tool.py`:
```python
def _try_navigate_same_tab(task_id, url):
    # Strategy 1: CDP supervisor navigate() -- uses Page.navigate
    # Strategy 2: agent-browser eval -- window.location.href via JS
    # Strategy 3: agent-browser open -- new tab (last resort)
    # Returns same shape as _run_browser_command
```

### Part 2: CDP Supervisor Tab Management Methods

New methods added to `CDPSupervisor` in `tools/browser_supervisor.py`:

| Method | CDP Command | Purpose |
|--------|-------------|---------|
| `navigate(url, timeout)` | `Page.navigate` | Navigate current tab in-place (no new tab) |
| `close_current_tab(timeout)` | `Target.closeTarget` | Close the active page tab |
| `close_tab(target_id, timeout)` | `Target.closeTarget` | Close any tab by CDP target ID |
| `get_open_tabs()` | `Target.getTargets` | List all open page targets with URLs/titles |

Also tracks `_page_target_id` (set during `_attach_initial_page`) so the supervisor knows which tab is the active one.

### Part 3: Tab Garbage Collection

`_cleanup_extra_tabs()` runs every 30 seconds in the background cleanup thread:
- Lists all open tabs via the CDP supervisor's `get_open_tabs()`
- Uses `close_tab()` to close any tab that isn't the current one (`_page_target_id`)
- Only fires for sessions with active CDP supervisors (cloud/CDP mode)
- Logs closed count at INFO level for observability

Wired into `_browser_cleanup_thread_worker()` right after `_cleanup_inactive_browser_sessions()`.

## Session Lifecycle Details

### Session Creation (`_get_session_info`)
1. Check if session exists in `_active_sessions` dict
2. If CDP override set → `_create_cdp_session()`
3. If local sidecar → `_create_local_session()`
4. If cloud provider configured → `provider.create_session()`
5. If all else fails → `_create_local_session()`
6. Store in `_active_sessions[task_id]`
7. Start CDP supervisor via `_ensure_cdp_supervisor()`

### Hybrid Routing
- Public URLs route to the cloud session
- Private/LAN URLs auto-route to a local sidecar when `browser.auto_local_for_private_urls: true`
- Sidecar key: `{task_id}::local`
- `_last_active_session_key` maps bare task IDs to the correct session for non-nav tools

### Cleanup (`cleanup_browser`)
1. Stop CDP supervisor
2. Stop recording
3. Run `agent-browser close`
4. Remove from `_active_sessions`
5. Close cloud provider session (if `bb_session_id` set)
6. Kill daemon process, clean socket dir

## Config Knobs (in `config.yaml`)

```yaml
browser:
  inactivity_timeout: 120     # Seconds before idle session is killed (floor: 30s)
  command_timeout: 30          # Seconds before each browser command times out
  record_sessions: false       # Record browser sessions to video
  allow_private_urls: false    # Allow navigating to LAN/private IPs
  tab_reuse: true               # When True, navigations reuse existing tabs instead of opening new ones
  engine: auto                 # Browser engine (auto, chromium, firefox, lightpanda, webkit)
  auto_local_for_private_urls: true  # Route private URLs to local Chromium
  cdp_url: ''                  # CDP WebSocket URL to connect to an existing browser
  dialog_policy: must_respond  # How JS dialogs are handled
  dialog_timeout_s: 300        # Dialog auto-dismiss timeout
  camofox:
    managed_persistence: false  # Keep Camofox profile across sessions
    user_id: ''
    session_key: ''
    adopt_existing_tab: false   # Use existing browser tab instead of creating new
    rewrite_loopback_urls: false
    loopback_host_alias: host.docker.internal
```

## Chrome DevTools MCP Integration

The Chrome DevTools MCP server (`npx chrome-devtools-mcp@latest`) provides direct tab management that the native browser tools lack. Use it when you need to:

- List all open tabs: `mcp_chrome_devtools_mcp_list_pages`
- Close a specific tab: `mcp_chrome_devtools_mcp_close_page(pageId=N)`
- Navigate to a URL: `mcp_chrome_devtools_mcp_navigate_page(url="...")`
- Take a snapshot: `mcp_chrome_devtools_mcp_take_snapshot()`
- Take a screenshot: `mcp_chrome_devtools_mcp_take_screenshot()`

This MCP connects to a real Chrome instance (not headless by default). Configure via `--headless` flag if you don't want a visible window.

## Adding Tab Management to agent-browser

If you want to add a `close-tab` command to agent-browser itself (the repo is at `tools/agent-browser/` in the Hermes source):
1. Add a `close_tab` or `open --reuse` command in agent-browser's CLI handler
2. Map it to Playwright's `page.close()` for the current page
3. The Hermes `browser_tool.py` would then call `agent-browser close-tab` after each navigation

## Related Skills

- `hermes-agent` — general Hermes configuration (bundled)
- `stealth-browser-setup` — Camofox/CloakBrowser setup
- `native-mcp` — MCP server configuration
- `building-mcp-servers` — building custom MCP servers
- `firefox-cdp-bridge` — Firefox CDP routing
