---
name: check-errors
description: Drive a flow and fail if any console error or failed network request occurs. Thin wrapper over verify_ui_flow with strict error-only assertions. Use to gate merges on "no regressions during this flow".
---

# /check-errors

Thin wrapper over **`verify_ui_flow`** focused on the question:

> Does this flow run cleanly — no console errors, no failed requests?

Use after `/verify-ui` confirms the feature works, OR as a fast smoke
check before merging.

## When to use

- After feature work, to gate "did I introduce a regression somewhere?"
- During PR review, to confirm the happy path doesn't spew errors.
- After dependency upgrades, to catch a quiet console break.
- After CSP / CORS / API auth changes — common cause of silent 4xx/5xx.

## When NOT to use

- You want to assert specific UI text — use `/verify-ui` instead.
- You only care about visual regression — use `/visual-diff`.
- You want a11y compliance — use `/audit-a11y`.
- Backend-only diff with no UI surface.

## Inputs

- `url` — entry point.
- `steps` *(optional)* — drive the flow. Same shape as `/verify-ui` steps.
- `exclude_console_patterns` *(optional)* — substrings; matching console
  errors are ignored. Useful for third-party SDKs that always log
  noise (e.g. `["facebook.com", "googletagmanager"]`).
- `exclude_request_patterns` *(optional)* — same idea for URLs.
- `allow_4xx` *(optional, default false)* — if true, only 5xx counts as
  a failure. Useful when 4xx is part of the auth happy path.
- `phase` *(optional)* — Extension Protocol phase hint for the emitted
  `manifest.json`. Default `verify`.

## Process

Call `verify_ui_flow` with:

```json
{
  "mode": "assert",
  "open": { "platform": "web", "url": "<url>" },
  "steps": [ ...user-provided... ],
  "expect": [
    { "kind": "no_console_errors", "exclude_patterns": [...] },
    { "kind": "no_failed_requests", "exclude_patterns": [...], "allow_4xx": false }
  ],
  "capture": ["screenshot", "console", "har"]
}
```

When the run is **tracing a reported error** (debugging context — the user
is hunting a bug, not gating a merge), add `"phase": "debug"` so the
evidence lands with the parent's `debug-issue` skill instead of the verify
report. For the default merge-gate / smoke use, omit it (defaults to
`verify`).

Surface the result. On `passed: false`, point the user at `console.json`
and `network.har` in `evidence_paths` so they can drill in.

## Outputs

Same shape as `/verify-ui`:

- `passed: boolean`
- `failure_reason` — e.g. `Expectations failed: expect[0] no_console_errors`
- `evidence_paths.console` — JSON dump of console messages
- `evidence_paths.har` — full HAR file

## Examples

### Smoke check — landing page

User: "Open https://app.example.com and confirm no errors fire."

```json
{
  "open": { "platform": "web", "url": "https://app.example.com" },
  "steps": [],
  "expect": [
    { "kind": "no_console_errors" },
    { "kind": "no_failed_requests" }
  ],
  "capture": ["screenshot", "console", "har"]
}
```

### Drive a flow then assert clean

User: "Sign in then dashboard — make sure no console errors."

```json
{
  "open": { "platform": "web", "url": "https://app.example.com/login" },
  "steps": [
    { "kind": "fill_form", "fields": [
      { "query": "Email", "value": "test@example.com" },
      { "query": "Password", "value": "..." }
    ]},
    { "kind": "click", "query": "Sign in" },
    { "kind": "wait_for", "condition": { "kind": "url_matches", "pattern": "dashboard" } }
  ],
  "expect": [
    { "kind": "no_console_errors", "exclude_patterns": ["sentry.io"] },
    { "kind": "no_failed_requests", "exclude_patterns": ["/analytics"] }
  ],
  "capture": ["screenshot", "console", "har"]
}
```

## Evidence routing

Run artifacts are saved under:

- **Standalone:** `.rolepod-uiproof/artifacts/<prefix>_<ts>_<uuid>/`
- **With `rolepod` parent** (detected via the marker file `<git-root>/.rolepod/parent-active` written by the parent's SessionStart hook): `<git-root>/.rolepod/evidence/<ts>-rolepod-uiproof-<skill>/`

Either way the run directory contains a `manifest.json` per Extension Protocol v1. Because `/check-errors` wraps `verify_ui_flow`, the manifest is written by the underlying composite tool — same shape, same fields. When invoked with `"phase": "debug"` the manifest is tagged for the parent's `debug-issue` pickup instead of `check-work`'s verify report.

## If the tool is unavailable

> The `/check-errors` skill needs the **rolepod-uiproof** MCP server,
> which is not currently available. Confirm the plugin is installed and
> try again, or check that `npx -y @rolepod/uiproof` is reachable.
