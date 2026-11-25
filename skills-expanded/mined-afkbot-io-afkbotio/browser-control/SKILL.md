---
name: browser-control
description: "Real browser automation via `browser.control`. Use when a task needs navigation, clicking, typing, screenshots, or page content from a live browser rather than plain HTTP."
---

# browser-control

Use this skill when a task requires real browser interaction rather than plain HTTP fetch.

Tool method:
- `browser.control`

Supported actions:
- `open`
- `navigate`
- `click`
- `fill`
- `press`
- `select`
- `check`
- `scroll`
- `wait`
- `content`
- `snapshot`
- `screenshot`
- `close`

Workflow:
1. Start with `action=open` (optional `url`).
2. Move page with `action=navigate`.
3. Interact with `action=click` / `action=fill` / `action=scroll`.
   Prefer semantic targets (`label`, `placeholder`, `field_name`, `role`, `target_text`) over brittle CSS selectors when possible.
4. If the page is still loading or reacts asynchronously, use `action=wait`.
5. For review or inspection tasks, prefer `action=snapshot` because it returns a structured page summary plus saved artifacts.
6. Use `action=content` when raw HTML/text is specifically needed.
7. Always finish with `action=close`.

Session lifecycle:
- Browser session is sticky for the current `profile_id + session_id`.
- If a browser is already open for this chat session, reuse it instead of opening a new one.
- Successful browser actions persist storage state for the same `profile_id + session_id`, so reopening the same chat session can restore cookies/local storage after process restarts.
- Use `action=close` when the browser is no longer needed.
- Use `action=close` with `clear_state=true` when the user wants to reset login state / cookies / local storage for that session.

Required fields by action:
- `navigate`: `url`
- `click`: one target (`selector`, `label`, `placeholder`, `field_name`, `role`, or `target_text`)
- `fill`: one target plus `text`
- `press`: `key`; optional target
- `select`: one target plus `value` or `target_text` (option label)
- `check`: one target
- `scroll`: optional target (`selector`, `label`, `placeholder`, `field_name`, `role`, `target_text`); without target scrolls page to bottom
- `wait`: optional target or `text` or `url`; without them waits for `timeout_ms`
- `snapshot`: optional `path` (workspace-local screenshot stem)
- `screenshot`: optional `path` (workspace-local)

Review guidance:
- For "изучи сайт", "посмотри блоки", "сделай ревью страницы" use `open` -> optional interactions -> `wait` -> `snapshot`.
- `snapshot` returns visible text, headings, buttons, links, forms, images, interactives, and saved files (`.png`, `.json`, `.html`, `.txt`).

Auth / multi-step guidance:
- Keep the same chat session while logging in, checking carts, placing orders, or moving through multi-page flows so the sticky browser session can be reused.
- If `open` reports `storage_state_loaded=true`, continue from the restored authenticated state instead of assuming a fresh login is required.
- Use `label` / `placeholder` / `field_name` for inputs, `role + target_text` for buttons and links, and `press key='Enter'` to submit when forms do not expose stable selectors.
- If a step waits on async UI or redirects, prefer `wait` with a concrete target before deciding that the flow is broken.

Failure handling:
- If Playwright/browser is unavailable, tool returns deterministic `browser_unavailable`.
- Prepare the local browser runtime with `afk browser install`.
- `afk browser install` now lets operators choose the browser backend interactively:
  - `playwright_chromium` for the default local Chromium path;
  - `lightpanda_cdp` for CDP browsers such as Lightpanda.
- For Lightpanda, set the CDP endpoint with `afk browser cdp-url http://127.0.0.1:9222` if it is not already stored.
- If Lightpanda uses a local endpoint, operators can also run `afk browser start` / `afk browser stop`
  to manage the bundled Lightpanda binary on supported platforms.
- Use `afk browser headless off` if you want visible browser windows.
- If a session is not opened first, tool returns `browser_session_not_open`.
- Runtime routes the correct skill automatically; do not send `skill_name`.
