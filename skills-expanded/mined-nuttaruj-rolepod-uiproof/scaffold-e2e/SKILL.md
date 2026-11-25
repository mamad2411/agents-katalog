---
name: scaffold-e2e
description: Generate a runnable e2e test file (playwright-test, vitest+playwright, pytest+selenium, or a Maestro YAML flow for mobile) from a scenario description plus an optional replay bundle from a prior /verify-ui run.
---

# /scaffold-e2e

Single-backend skill. Calls **`scaffold_e2e`** on the rolepod-uiproof
MCP server. No fallback (D-024).

## When to use

- The user asks to generate an e2e test for a flow they just verified
  interactively.
- A replay bundle from `/verify-ui` exists and should be transcribed into
  a real test file.
- A mobile target (iOS / Android / React Native / Flutter) needs a test
  scaffold — use `framework: "maestro"` to emit a Maestro YAML flow.

## When NOT to use

- A unit or integration test is sufficient — pick a closer framework
  manually.
- The scenario is too vague to scaffold — ask the user to clarify before
  calling.

## Coverage

The codegen handles every step kind and expect kind supported by
`/verify-ui` (click, type, key, navigate, wait_for, hover, drag,
fill_form, upload, dialog, set_env, switch_page, evaluate; text_visible,
text_absent, url_matches, ref_in_state, no_console_errors,
no_failed_requests, request_made, response_status).

Playwright-test gets first-class translation for everything that has a
direct Playwright API. Pytest+selenium covers the basics; expect kinds
that need network introspection (no_failed_requests, request_made,
response_status) emit a TODO referencing `selenium-wire` or BiDi, since
upstream Selenium has no network-capture primitive.

**Maestro** (mobile) emits a YAML flow (`launchApp` / `tapOn` /
`inputText` / `assertVisible` / `extendedWaitUntil` / `scroll`), following
Maestro's own conventions rather than a translation of the Playwright
template. Web-only kinds (hover, switch_page, evaluate, network expects)
degrade to comments instead of failing. TC-ID traceability: a `TC<n>` id
and `P1`/`P2` priority found in `scenario_nl` are carried into the
filename (`TC2_<slug>.yaml`), the header comment, and Maestro `tags` —
greppable exactly like the web frameworks' test names. The Maestro CLI is
NOT required to scaffold (only to run); the scaffold hands off — it never
auto-runs.

## Inputs

- `framework` — `playwright-test` | `vitest+playwright` | `pytest+selenium` | `maestro`.
- `scenario_nl` — natural-language description of the scenario. For
  `maestro`, lead with the TC id and priority (e.g. `"TC2 [P1] …"`) to
  preserve traceability.
- `url` — entry URL. Required for the web frameworks; for `maestro` it
  marks a web flow instead of `app_id`.
- `app_id` *(maestro only)* — application id of the mobile app under test
  (e.g. `com.example.app`).
- `recorded_bundle` *(optional)* — path to a replay bundle from a prior
  `/verify-ui` run; when present, steps and expectations are transcribed.
- `filename` *(optional)* — override the generated file name.

## Outputs

- `run_id` — folder under `./.rolepod-uiproof/artifacts/`.
- `test_file_path` — path to the generated test file.
- `language` — `typescript` | `python` | `yaml`.
- `dependencies` — packages the user needs to install (empty for
  `maestro` — the CLI is an external binary, pointed to in
  `setup_notes`).
- `setup_notes` — what to run after install (for `maestro`:
  `maestro test <flow.yaml>`, run by the caller, never by the tool).
- `from_replay_bundle` — boolean indicating whether the file was
  transcribed from a recorded run.

## Process

1. Build `scaffold_e2e` input.
2. Call the tool.
3. Print the generated file path and the setup steps. Surface
   `dependencies` as an install command.

## Evidence routing

Run artifacts (the generated test file) are saved under:

- **Standalone:** `.rolepod-uiproof/artifacts/<prefix>_<ts>_<uuid>/`
- **With `rolepod` parent** (detected via the marker file `<git-root>/.rolepod/parent-active` written by the parent's SessionStart hook): `<git-root>/.rolepod/evidence/<ts>-rolepod-uiproof-<skill>/`

Either way the run directory contains a `manifest.json` per Extension Protocol v1 (with `phase: "build"` for this skill).

## If the tool is unavailable

Surface plainly:

> The `/scaffold-e2e` skill needs the **rolepod-uiproof** MCP server, which
> is not currently available. Confirm the plugin is installed and try
> again.

Do not attempt another backend (D-024).

## Examples

### Transcribe a replay bundle to a Playwright Test file

```json
{
  "framework": "playwright-test",
  "scenario_nl": "user opens example.com and clicks Learn more",
  "url": "https://example.com",
  "recorded_bundle": ".rolepod-uiproof/artifacts/verify_…/replay.json"
}
```

Returns:

```json
{
  "run_id": "scaffold_…",
  "test_file_path": ".rolepod-uiproof/artifacts/scaffold_…/user-opens-example-com-and-clicks-learn-more.spec.ts",
  "language": "typescript",
  "dependencies": ["@playwright/test"],
  "setup_notes": "Install: npm i -D @playwright/test && npx playwright install. Run: npx playwright test.",
  "from_replay_bundle": true
}
```

### Scaffold a Maestro flow for a mobile test case

```json
{
  "framework": "maestro",
  "scenario_nl": "TC2 [P1] user logs in with minimum boundary password",
  "app_id": "com.example.app"
}
```

Returns `test_file_path` ending in `TC2_user-logs-in-with-minimum-boundary-password.yaml` with the TC id in the header comment and `tags`, `language: "yaml"`, empty `dependencies`, and `setup_notes` pointing at `maestro test <flow.yaml>` (hand-off — the caller runs it).
