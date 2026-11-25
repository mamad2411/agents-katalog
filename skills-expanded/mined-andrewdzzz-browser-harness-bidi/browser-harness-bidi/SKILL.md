---
name: browser-harness-bidi
description: bidi-first browser control for agents. Use when the user wants WebDriver bidi, Firefox or Chrome automation, or cross-browser standard browser control.
allowed-tools: Bash, Edit, Write, Read
---

# browser-harness-bidi

Use `bidi-harness` or the managed `bidi-firefox` / `bidi-ruyi-firefox` / `bidi-chrome` launchers for WebDriver bidi browser control.

Compatibility note: `browser-harness` is also available in this fork and routes to the same bidi implementation, so original Browser Harness muscle memory still works while the transport is WebDriver bidi.

bidi is the preferred default for Firefox and the future-facing protocol for cross-browser browser agents. It is the standard automation surface this project builds around.

## Fast path

```bash
bidi-firefox <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY
```

`bidi-firefox` starts geckodriver, requests a WebDriver bidi WebSocket, runs the harness script, and cleans up the managed browser session.

For ruyiPage's Firefox runtime or a Firefox-compatible fingerprint browser:

```bash
bidi-ruyi-firefox --browser-path /path/to/firefox --fpfile /path/to/fpfile.txt <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY
```

`bidi-ruyi-firefox` starts Firefox directly with `--remote-debugging-port` and connects to the direct Firefox BiDi socket. It can also attach to an already-open endpoint with `--existing-address 127.0.0.1:12000`, as long as that endpoint can create a new BiDi session.

For Chrome through ChromeDriver:

```bash
bidi-chrome <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY
```

`bidi-chrome` starts chromedriver, requests a Chrome WebDriver bidi WebSocket, runs the harness script, and cleans up the managed browser session.

## Manual harness path

```bash
bidi-harness <<'PY'
new_tab("https://example.com")
wait_for_load()
print(page_info())
PY
```

Set one of these before using `bidi-harness` directly:

- `BIDI_WS=ws://127.0.0.1:9222/session` for a direct bidi WebSocket, commonly Firefox remote debugging.
- `BIDI_WEBDRIVER_URL=http://127.0.0.1:9516` for a WebDriver broker such as geckodriver.
- `BIDI_BROWSER_NAME=firefox` or `BIDI_BROWSER_NAME=chrome`.
- `BIDI_CAPABILITIES='{"moz:firefoxOptions":{"args":["-headless"]}}'` for broker-managed Firefox options.
- `BIDI_CAPABILITIES='{"goog:chromeOptions":{"args":["--headless=new"]}}'` for broker-managed Chrome options.

For every supported environment variable, read `docs/env-vars.md`.

## Interaction skills

If a browser task involves a known mechanic, read the matching file in `interaction-skills/` before inventing a new approach.

Available skills:

- `browser-basics.md` - page state, tabs, screenshots, selectors, viewport, and PDF capture.
- `forms-and-input.md` - forms, text input, file uploads, and dialog handling.
- `network-and-storage.md` - network events, network idle waits, localStorage, sessionStorage, and cookies.

## Domain skills

Domain skills live under `agent-workspace/domain-skills/` and are disabled unless `BH_DOMAIN_SKILLS=1`. When enabled, `goto_url(url)` and `new_tab(url)` may return `domain_skills`; read those files before inventing a site-specific flow.

Good domain skills store durable selectors, URL patterns, loaded states, and auth-wall clues. Never store credentials, private data, or anti-detection guidance.

## Helpers

Prefer visible, user-like actions first:

```python
capture_screenshot()
click_at_xy(x, y)
type_text("text")
press_key("Enter")
scroll(500, 500, dy=600)
```

Use DOM and raw bidi when coordinates are the wrong tool:

```python
print(js("document.title"))
print(bidi("browsingContext.getTree"))
```

Common functions:

- `new_tab(url="about:blank")`
- `goto_url(url, wait="none")`
- `wait_for_load(timeout=15)`
- `wait_for_element(selector, timeout=10, visible=False)`
- `wait_for_network_idle(timeout=10, idle_ms=500)`
- `page_info()`
- `list_contexts()`
- `switch_context(context_or_dict)`
- `close_context(context=None)`
- `capture_screenshot(path=None, full=False, max_dim=None)`
- `upload_file(selector, path)`
- `http_get(url)`

## bidi-first design rules

- Think in `browsingContext`, `script`, `input`, `network`, and `log` modules.
- Use raw `bidi("module.command", ...)` for anything helpers do not cover.
- Put task-specific additions in `agent-workspace/agent_helpers.py`.
- Use bidi browsing context ids and script realms deliberately.
- Do not treat bidi as stealth. Standard WebDriver automation may expose `navigator.webdriver`.

## Why this matters

For agents that should survive across Firefox, Chrome, WebDriver Grid, and future browser automation infrastructure, bidi is the protocol to build around.
