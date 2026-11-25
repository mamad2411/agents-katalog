---
name: verify-ui
description: Drive a real browser session through steps and assert expected outcomes — including console errors, network failures, and visual state. Save evidence under ./.rolepod-uiproof/artifacts/. Web only.
---

# /verify-ui

Single-backend skill. Calls **`verify_ui_flow`** on the rolepod-uiproof
MCP server and surfaces the structured result. No fallback (D-024) — if the
tool is unavailable, this skill fails with a clear diagnostic.

## When to use

- A diff changes user-visible behavior on a web target.
- A URL is reachable (dev server is running, or the target is deployed).
- You want to prove the UI works AND has no console errors / failed
  requests / regressed visuals — code-level tests can't do that.

## When NOT to use

- Backend-only diffs (no UI change).
- Doc, config, or build-tool changes with no behavior surface.
- No dev server / target available — ask the user to spin one up first.
- iOS / Android targets — mobile is partially supported (basic input);
  console / network / set_env / evaluate are web-only.

## Modes

- `mode: 'assert'` (default) — assertions describe what the **feature
  should do**; pass = feature works.
- `mode: 'reproduce'` — assertions describe what the **bug looks like**;
  pass = bug reproduces. When `minimize: true` (default) the tool then
  removes steps one-by-one to find the shortest still-reproducing sequence
  and writes `replay-minimized.json` next to `replay.json`.

## Inputs

### `open` — context setup

```json
{ "platform": "web", "url": "https://...", "browser": "chromium" }
```

Optional: `viewport`, `headless`, `user_agent`, `locale`. UA / locale /
timezone MUST be set here — they cannot change mid-session.

### `steps` — UI actions in order

Each step is one of:

- `{ "kind": "click", "query": "Submit" }`
- `{ "kind": "type", "query": "Email", "text": "x@y.com", "clear_first": true }`
- `{ "kind": "key", "key": "Enter" }`
- `{ "kind": "wait_for", "condition": { ... } }`
- `{ "kind": "navigate", "url": "https://..." }`
- `{ "kind": "hover", "query": "More" }`
- `{ "kind": "drag", "from_query": "Card A", "to_query": "Column 2" }`
- `{ "kind": "fill_form", "fields": [ { "query": "Name", "value": "Alice" }, { "query": "Subscribe", "value": true, "kind": "checkbox" } ] }`
- `{ "kind": "upload", "query": "Avatar", "file_path": "/abs/path/to/file.png" }`
- `{ "kind": "dialog", "action": "accept" }` — **place BEFORE the action that triggers the dialog**
- `{ "kind": "set_env", "viewport": { "width": 375, "height": 812 } }` — also accepts offline, geolocation, color_scheme, reduced_motion, extra_headers, network_throttle, cpu_throttle
- `{ "kind": "switch_page", "index": 1 }` — multi-page (popups, target=_blank)
- `{ "kind": "evaluate", "script": "return document.title" }` — runs arbitrary JS in the page; enabled by the shipped spawn configs via `ROLEPOD_ALLOW_EVAL=1` (a server launched without it, or with `ROLEPOD_ALLOW_EVAL=0`, rejects this step)
- `{ "kind": "scroll", "direction": "down", "amount": 1500 }` — scroll by a delta (`amount` defaults to 400px); use to fire scroll-reveal / IntersectionObserver content
- `{ "kind": "settle" }` — scroll the full page to trigger **all** reveals + lazy loads, network-idle, then return to top (web-only). Reach for this on reveal/animation-heavy pages so `text_visible` assertions see the settled state instead of an `opacity:0` placeholder.

### `expect` — assertions

- `{ "kind": "text_visible", "text": "..." }`
- `{ "kind": "text_absent", "text": "..." }`
- `{ "kind": "url_matches", "pattern": "regex" }`
- `{ "kind": "ref_in_state", "query": "Submit", "state": "enabled" }`
- `{ "kind": "no_console_errors", "exclude_patterns": ["3rd-party.com"] }`
- `{ "kind": "no_failed_requests", "exclude_patterns": ["/analytics"], "allow_4xx": false }`
- `{ "kind": "request_made", "url_pattern": "/api/checkout", "method": "POST", "min_count": 1 }`
- `{ "kind": "response_status", "url_pattern": "/api/me", "status": 200 }`

### `capture` — evidence

Default: `["screenshot"]`. Available:

- `screenshot` — `final.png`
- `console` — `console.json` (filtered errors+warnings, ring buffer up to 1000)
- `har` — `network.har` (full HAR)
- `video` — `videos/*.webm`
- `trace` — `trace.zip` (Playwright trace; view with `npx playwright show-trace`)
- `a11y_tree` — `a11y_tree.json` (final snapshot)

### Defaults

- `close_on_finish: true`
- `minimize: true` (only consulted when `mode: 'reproduce'`)

## Outputs

- `run_id`, `passed`, `failed_at_step`, `failure_reason`,
  `final_url_or_screen`
- `evidence_paths: { screenshots, replay_bundle, console?, a11y_tree?, har?, trace?, video? }`
- `minimized` (only on `mode: 'reproduce'` + `passed: true` + `minimize: true`)

## Process

1. Build the `verify_ui_flow` input.
2. Call the tool.
3. Report the structured result. On failure include `failed_at_step` +
   `failure_reason` + relevant evidence paths (screenshot, console.json
   if console errors caused the failure).

## Default suggestion

For ANY user-visible flow, default-include `no_console_errors` and
`no_failed_requests` in `expect`. Real UI bugs surface as console errors
or 5xx responses far more often than as wrong text.

## Evidence routing

Run artifacts are saved under:

- **Standalone:** `.rolepod-uiproof/artifacts/<prefix>_<ts>_<uuid>/`
- **With `rolepod` parent** (detected via the marker file `<git-root>/.rolepod/parent-active` written by the parent's SessionStart hook): `<git-root>/.rolepod/evidence/<ts>-rolepod-uiproof-<skill>/`

Either way the run directory contains a `manifest.json` per Extension Protocol v1, so the parent's `check-work` skill can aggregate results into the verify phase report. Standalone users can read the manifest themselves — same shape.

## If the tool is unavailable

> The `/verify-ui` skill needs the **rolepod-uiproof** MCP server, which is
> not currently available. Confirm the plugin is installed and try again,
> or check that `npx -y @rolepod/uiproof` is reachable.

Do **not** attempt this work via Playwright MCP, Chrome DevTools MCP, or
any other backend from inside this skill. Multi-backend routing is the
job of the parent `rolepod` plugin's `check-work` / `debug-issue` skills.

## Examples

### Success — verify checkout flow with no errors

User: "Verify https://shop.example.com/checkout works — fill the form,
submit, expect a success page and no errors."

```json
{
  "mode": "assert",
  "open": { "platform": "web", "url": "https://shop.example.com/checkout" },
  "steps": [
    { "kind": "fill_form", "fields": [
      { "query": "Name", "value": "Alice" },
      { "query": "Email", "value": "alice@example.com" },
      { "query": "Card", "value": "4242 4242 4242 4242" }
    ]},
    { "kind": "click", "query": "Pay" },
    { "kind": "wait_for", "condition": { "kind": "text_visible", "text": "Thank you" } }
  ],
  "expect": [
    { "kind": "text_visible", "text": "Thank you" },
    { "kind": "no_console_errors" },
    { "kind": "no_failed_requests", "exclude_patterns": ["/analytics"] },
    { "kind": "response_status", "url_pattern": "/api/checkout", "status": 200 }
  ],
  "capture": ["screenshot", "console", "har"]
}
```

### Failure with evidence

When `no_console_errors` fails, the result surfaces:

```json
{
  "passed": false,
  "failure_reason": "Expectations failed: expect[1] no_console_errors",
  "evidence_paths": {
    "screenshots": ["…/final.png"],
    "console": "…/console.json"
  }
}
```

Open `console.json` to inspect the errors.

### Dialog handling

User: "When the user clicks Delete, a confirm dialog appears. Verify
that accepting it deletes the row."

```json
{
  "steps": [
    { "kind": "dialog", "action": "accept" },
    { "kind": "click", "query": "Delete" },
    { "kind": "wait_for", "condition": { "kind": "text_absent", "text": "Row A" } }
  ],
  "expect": [ { "kind": "text_absent", "text": "Row A" } ]
}
```

The `dialog` step arms a one-shot handler; the *next* trigger (the click)
fires it. Un-armed dialogs are auto-dismissed.

### Responsive + dark mode

User: "Verify mobile dark-mode layout."

```json
{
  "steps": [
    { "kind": "set_env", "viewport": { "width": 375, "height": 812 }, "color_scheme": "dark" }
  ],
  "expect": [ { "kind": "text_visible", "text": "Menu" } ],
  "capture": ["screenshot"]
}
```
