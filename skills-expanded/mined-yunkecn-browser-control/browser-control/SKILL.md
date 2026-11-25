---
name: browser-control
description: Control the user's real Chrome through a local Browser Control daemon and Chrome extension. Use when a task requires browser or webpage automation, screenshots, DOM snapshots, authenticated sessions, form interaction, network inspection, downloads, PDFs, or direct website interaction from an agent.
---

# Browser Control

Browser Control lets an agent operate the user's real Chrome profile through a localhost daemon and a Chrome Manifest V3 extension.

```text
agent -> scripts/browser-control.js -> localhost HTTP daemon -> WebSocket -> Chrome extension -> Chrome DOM
```

Use this skill for browser work that benefits from the user's installed Chrome, logged-in sessions, extension environment, or visible tabs.

## Quick start

Run commands from this skill directory unless `browser-control` is already on `PATH`:

```bash
node scripts/browser-control.js start --json
node scripts/browser-control.js doctor --json
bash scripts/health-check.sh
```

The daemon listens on `http://127.0.0.1:10087` by default and the extension connects to `ws://127.0.0.1:10087/ws`.

## Agent execution loop

1. Choose a unique `session` name for the task, such as `research-<topic>` or `checkout-review`.
2. Start or reuse the singleton daemon: `node scripts/browser-control.js start --json`.
3. Run `node scripts/browser-control.js doctor --json` and proceed only when the daemon is reachable and `extension_connected` is true.
4. Navigate with `navigate`, or find/attach an existing tab with `find_tab` (default attach; pass `attach:false` for lookup only).
5. Take a fresh `snapshot` before every element interaction. Snapshot is a compact structure/interaction view, not a full text dump; use `get_text` for reading page prose. On noisy pages, use filters such as `hasVisibleText`, `viewportOnly`, `roles`, and `maxElements`.
6. Use `@e` references (format `@e<structureId>_<revision>`) from the latest snapshot for `click`, `fill`, `press`, `select_option`, and `set_checked`; refresh the snapshot after navigation or significant DOM changes. Stale revisions fail closed with `STALE_ELEMENT_REFERENCE`. Use `scroll` for non-keyboard page or region scrolling; fall back to stable CSS only when needed.
7. Use default action strategies first (`click.strategy:"auto"`, `fill.strategy:"native_setter"`, `press.strategy:"auto"`). Inspect `warnings`, `hitTest`, and no-delta diagnostics before retrying with another strategy.
8. Use `force:true` only after confirming that a covering overlay or hit-test mismatch is intentional and safe to bypass. Prefer fixing the target locator or closing the overlay.
9. Verify important state-changing actions with `expectChange`, `observe_start` / `observe_diff`, `snapshot`, `wait_for`, or `scripts/screenshot.sh` when visual evidence matters.
10. Stop and ask before sensitive, destructive, account-changing, purchase/payment, upload, submit/send/post/publish, credential, MFA, or permission-grant actions.
11. Close task-specific tabs or sessions with `close_tab` / `close_session` when finished.

## Command API

Send typed command envelopes to `POST http://127.0.0.1:10087/command` or use the CLI helper:

```bash
node scripts/browser-control.js command snapshot --session demo --args '{}'
node scripts/browser-control.js command click --session demo --args '{"selector":"@e1jm0sbb_1"}'
node scripts/browser-control.js command click_probe --session demo --args '{"selector":"@e1jm0sbb_1"}'
node scripts/browser-control.js command click --session demo --args '{"selector":"@e1jm0sbb_1","expectChange":true}'
node scripts/browser-control.js command fill --session demo --args '{"selector":"@e0abc12_1","value":"draft text"}'
node scripts/browser-control.js command get_text --session demo --args '{"scope":"viewport","maxChars":4000}'
node scripts/browser-control.js command scroll --session demo --args '{"deltaY":800,"strategy":"dom"}'
node scripts/browser-control.js command scroll --session demo --args '{"strategy":"wheel","x":400,"y":500,"deltaY":800}'
node scripts/browser-control.js command snapshot --session demo --args '{"hasVisibleText":true,"viewportOnly":true,"maxElements":120}'
node scripts/browser-control.js command snapshot --session demo --args '{"roles":["button","link","textbox","combobox"],"viewportOnly":true}'
node scripts/browser-control.js command evaluate --session demo --code-file ./snippet.js
```

Envelope shape:

```json
{
  "id": "req-1",
  "version": "2026-05-19",
  "session": "demo",
  "command": "snapshot",
  "args": {},
  "timeoutMs": 30000
}
```

Common commands: `navigate`, `find_tab`, `snapshot`, `click`, `click_probe`, `fill`, `press`, `scroll`, `select_option`, `set_checked`, `wait_for`, `evaluate`, `get_text`, `screenshot`, `save_as_pdf`, `observe_start`, `observe_diff`, `network_start`, `network_list`, `network_detail`, `network_stop`, `upload`, `download`, `list_tabs`, `close_tab`, and `close_session`.

Load `references/api.md` for the full command and CLI reference.

Action commands return diagnostics when available: `strategyUsed`, `target`, `hitTest`, `focusBefore`, `focusAfter`, `newTab` / `newTabs` for actions that open another tab, `warnings`, and optional `actionObservation`. If a click reports no observable change, take a fresh `snapshot`, inspect whether another element covered the target, and retry only with a deliberate strategy choice. `element_click` is an explicit escape hatch that calls `el.click()` directly; it is not the default fallback because it can bypass pointer/mouse semantics.

Snapshot redacts likely sensitive field values by default (`password`, token/secret/session/cookie/API-key-like fields). If you need page text rather than targets, prefer `get_text` so the agent does not spend context on layout containers. For below-fold or scrollable-region text, use `scroll` plus `get_text` instead of using `evaluate` as a scrolling workaround.

## Common recipes

Load `references/recipes.md` for task playbooks:

- read a page
- operate UI safely
- fill a form without submitting
- submit after confirmation
- capture screenshots or PDFs
- inspect network calls
- download files
- clean up sessions

For quick single-action verification, `click`, `fill`, and `press` can use `expectChange` / `observe` and return an inline `actionObservation`. For multi-step debugging or broader before/after checks, call `observe_start`, perform normal reversible actions, then call `observe_diff` to get capped added/removed visible text and network requests since the baseline marker. This does not prove request causation and may include sensitive visible text; keep summaries compact.

## Screenshots and artifacts

Do not paste raw screenshot or PDF base64 into context. Use bundled artifact helpers:

```bash
bash scripts/screenshot.sh -s demo -f png
```

Artifact-producing commands return file references and metadata. Default artifact storage is `~/.browser-control/artifacts`; override it with `BROWSER_CONTROL_ARTIFACT_DIR` when needed.

`screenshot` and `save_as_pdf` responses intentionally omit raw base64 after the daemon persists the file. Read the returned artifact path from `data.artifact.path` or `artifacts[0].path`; the `scripts/screenshot.sh` helper does this and prints only the saved file path.

## Confirmation boundaries

Must ask the user before:

- clicking Submit, Send, Post, Publish, Confirm, Buy, Pay, Delete, Cancel, or similar final-action controls
- placing orders, payments, subscriptions, bookings, or irreversible changes
- changing account, security, privacy, OAuth, permission, or organization settings
- uploading local files or entering/sending personal, sensitive, private, or credential-like data
- handling login, MFA, CAPTCHA, browser permission prompts, or native file pickers

Usually no confirmation is needed for navigation, reading visible content, opening non-submitting menus, taking screenshots for task evidence, or filling reversible draft fields with non-sensitive content.

If risk is ambiguous, stop and ask.

## Readiness and troubleshooting

Start with:

```bash
node scripts/browser-control.js status --json
node scripts/browser-control.js doctor --json
node scripts/browser-control.js logs -n 100
```

If `extension_connected` is false, browser automation is blocked except for diagnostics; ask the user to load or reload the bundled Chrome extension from this skill's `extension/` directory when you cannot safely do it. If commands fail with `Element not found`, take a fresh `snapshot` and rebuild the locator. Validation errors include stable `error.details`; for example `fill` requires `args.value` (not `args.text`).

If `extension_connected` is false after `doctor --json`, guide the user to load the Chrome extension with `references/chrome-extension-setup.md`; it covers both the installed skill's `extension/` directory and the release extension zip.

Load `references/decision-guide.md` for readiness/failure decisions and `references/troubleshooting.md` for detailed recovery steps and known limitations.
