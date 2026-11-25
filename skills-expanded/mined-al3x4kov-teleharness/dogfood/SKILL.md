---
name: dogfood
description: Systematically explore and test a web application manually, like a meticulous first-time user, to find bugs, UX issues, and visual/interface problems. Use when asked to "dogfood", "QA", "manual testing", "exploratory test", "find issues", "bug hunt", "test this app/site/portal", "протестируй", "найди баги", or review the quality of a web application. Produces a structured report with full reproduction evidence -- step-by-step screenshots and detailed repro steps for every issue -- so findings can be handed directly to the responsible teams.
license: Apache-2.0
metadata:
  upstream: vercel-labs/agent-browser skill-data/dogfood
  upstream_commit: 5868f7c05020e047c00e68e4abf9253cce864f41
  local_adaptation: Browser is driven via the playwright MCP server instead of the agent-browser CLI (its win32 binary is blocked by Device Guard on this machine). Methodology unchanged.
---

# Dogfood

Systematically explore a web application, find issues, and produce a report with full reproduction evidence for every finding.

## Setup

Only the **Target URL** is required. Everything else has sensible defaults -- use them unless the user explicitly provides an override.

| Parameter | Default | Example override |
|-----------|---------|-----------------|
| **Target URL** | _(required)_ | `example.com`, `http://localhost:3000` |
| **Output directory** | `./dogfood-output/` | `Output directory: /tmp/qa` |
| **Scope** | Full app | `Focus on the billing page` |
| **Authentication** | None | `Sign in to user@example.com` |

If the user says something like "dogfood example.com", start immediately with defaults. Do not ask clarifying questions unless authentication is mentioned but credentials are missing.

**Browser tooling.** Drive the browser exclusively through the **playwright MCP** server tools (`browser_*`). Do not use the `agent-browser` CLI (blocked on this machine) and do not write Playwright scripts. Output artifacts (screenshots, report) go to the output directory; `browser_take_screenshot` `filename` accepts absolute or relative paths.

| agent-browser (upstream) | playwright MCP equivalent |
|---|---|
| `open {URL}` | `browser_navigate` `{url}` |
| `snapshot -i` (interactive refs) | `browser_snapshot` (returns `ref`s for clickable/fillable elements) |
| `click @eN` | `browser_click` `{element, ref}` |
| `fill @eN "text"` | `browser_fill_form` or `browser_type` `{element, ref, text}` |
| `type @eN "text"` (human-paced) | `browser_type` with slow typing enabled if available; otherwise type + brief `browser_wait_for` `{time: 0.5}` |
| `screenshot --annotate {path}` | `browser_take_screenshot` `{filename: {path}}` |
| `console` | `browser_console_messages` `{level: "warning"}` |
| `errors` | `browser_console_messages` `{level: "error"}` + `browser_network_requests` (failed requests) |
| `wait --text/--url` | `browser_wait_for` `{text}` / navigate + snapshot |
| `scroll down N` | `browser_press_key` `PageDown` (never `browser_evaluate` to scroll) |
| responsive checks | `browser_resize` `{width, height}` -- test 375x812 (phone) and 1280x800 (desktop) |
| `record start/stop` (video) | Usually unavailable: verify at session start whether any video/recording tool exists. If none, skip video and make the screenshot-per-step sequence mandatory (see below). |
| `state save` | Login persists in the MCP browser profile; if a later session loses it, just re-authenticate. |
| `close` | `browser_close` (optional, at wrap-up) |

## Workflow

```
1. Initialize    Set up output dirs, report file
2. Authenticate  Sign in if needed
3. Orient        Navigate to starting point, take initial snapshot
4. Explore       Systematically visit pages and test features
5. Document      Screenshot + record each issue as found
6. Wrap up       Update summary counts
```

### 1. Initialize

Create the output directories:

```
mkdir -p {OUTPUT_DIR}/screenshots {OUTPUT_DIR}/videos
```

Copy the report template into the output directory and fill in the header fields: copy `{SKILL_DIR}/templates/dogfood-report-template.md` (`{SKILL_DIR}` is the folder containing this SKILL.md) to `{OUTPUT_DIR}/report.md`.

Then open the target:

- `browser_navigate` `{url: TARGET_URL}` (it returns a snapshot on arrival)

### 2. Authenticate

If the app requires login:

1. `browser_snapshot` -- identify login form element refs
2. `browser_type` / `browser_fill_form` -- fill email and password
3. `browser_click` -- submit
4. `browser_wait_for` `{text: POST_LOGIN_TEXT}` or navigate to the post-login URL and snapshot to confirm

For OTP/email codes: ask the user, wait for their response, then enter the code.

### 3. Orient

Take an initial screenshot and snapshot to understand the app structure:

- `browser_take_screenshot` `{filename: {OUTPUT_DIR}/screenshots/initial.png}`
- `browser_snapshot`

Identify the main navigation elements and map out the sections to visit.

### 4. Explore

Read [references/issue-taxonomy.md](references/issue-taxonomy.md) for the full list of what to look for and the exploration checklist.

**Strategy -- work through the app systematically:**

- Start from the main navigation. Visit each top-level section.
- Within each section, test interactive elements: click buttons, fill forms, open dropdowns/modals.
- Check edge cases: empty states, error handling, boundary inputs.
- Try realistic end-to-end workflows (create, edit, delete flows).
- Check the browser console for errors periodically.
- Check responsiveness: `browser_resize` to 375x812 on key pages, screenshot, then restore.

**At each page:**

- `browser_snapshot` (read structure and element refs)
- `browser_take_screenshot` `{filename: {OUTPUT_DIR}/screenshots/{page-name}.png}`
- `browser_console_messages` `{level: "warning"}`
- `browser_network_requests` (scan for failed requests)

Use your judgment on how deep to go. Spend more time on core features and less on peripheral pages. If you find a cluster of issues in one area, investigate deeper.

### 5. Document Issues (Repro-First)

Steps 4 and 5 happen together -- explore and document in a single pass. When you find an issue, stop exploring and document it immediately before moving on. Do not explore the whole app first and document later.

Every issue must be reproducible. When you find something wrong, do not just note it -- prove it with evidence. The goal is that someone reading the report can see exactly what happened and replay it.

**Choose the right level of evidence for the issue:**

#### Interactive / behavioral issues (functional, ux, console errors on action)

These require user interaction to reproduce -- use a full step-by-step screenshot sequence:

1. **Verify reproducibility first**: reset to a clean state and reproduce once before collecting evidence.
2. **Walk through the steps at human pace.** Take a screenshot at every step; add a short pause (`browser_wait_for` `{time: 1}`) between actions so the sequence mirrors real usage:

```
browser_take_screenshot {filename: .../issue-{NNN}-step-1.png}
browser_wait_for {time: 1}
browser_click {element, ref}        # the action
browser_wait_for {time: 1}
browser_take_screenshot {filename: .../issue-{NNN}-step-2.png}
# ...continue until the issue manifests
```

3. **Capture the broken state.** Pause, then take the final screenshot:

```
browser_wait_for {time: 2}
browser_take_screenshot {filename: .../issue-{NNN}-result.png}
```

4. If a video/recording tool exists in the MCP toolset, record the repro instead of (or in addition to) the step sequence. If not, set **Repro Video** to `N/A` -- the screenshot sequence is the evidence.

5. Write numbered repro steps in the report, each referencing its screenshot.

#### Static / visible-on-load issues (typos, placeholder text, clipped text, misalignment, console errors on load)

These are visible without interaction -- a single screenshot is sufficient. No multi-step repro:

```
browser_take_screenshot {filename: .../issue-{NNN}.png}
```

Write a brief description and reference the screenshot in the report. Set **Repro Video** to `N/A`.

---

**For all issues:**

1. **Append to the report immediately.** Do not batch issues for later. Write each one as you find it so nothing is lost if the session is interrupted.

2. **Increment the issue counter** (ISSUE-001, ISSUE-002, ...).

### 6. Wrap Up

Aim to find **5-10 well-documented issues**, then wrap up. Depth of evidence matters more than total count -- 5 issues with full repro beats 20 with vague descriptions.

After exploring:

1. Re-read the report and update the summary severity counts so they match the actual issues. Every `### ISSUE-` block must be reflected in the totals.
2. Optionally `browser_close`.
3. Tell the user the report is ready and summarize findings: total issues, breakdown by severity, and the most critical items.

## Guidance

- **Repro is everything.** Every issue needs proof -- but match the evidence to the issue. Interactive bugs need the step-by-step screenshot sequence. Static bugs (typos, placeholder text, visual glitches visible on load) only need a single screenshot.
- **Verify reproducibility before collecting evidence.** If an issue can't be reproduced consistently, it's not a valid issue.
- **No video for static issues.** A typo or clipped text doesn't benefit from a recording. Save sequences for issues that involve user interaction, timing, or state changes.
- **For interactive issues, screenshot each step.** Capture the before, the action, and the after -- so someone can see the full sequence.
- **Write repro steps that map to screenshots.** Each numbered step in the report should reference its corresponding screenshot. A reader should be able to follow the steps visually without touching a browser.
- **Snapshot before acting.** `browser_snapshot` gives element `ref`s -- always act on refs from the latest snapshot, never on stale ones.
- **Be thorough but use judgment.** You are not following a test script -- you are exploring like a real user would. If something feels off, investigate.
- **Write findings incrementally.** Append each issue to the report as you discover it. If the session is interrupted, findings are preserved. Never batch all issues for the end.
- **Never delete output files.** Do not delete screenshots or the report mid-session. Do not restart the browser to "clean up". Work forward, not backward.
- **Never read the target app's source code.** You are testing as a user, not auditing code. Do not read HTML, JS, or config files of the app under test. All findings must come from what you observe in the browser.
- **Check the console.** Many issues are invisible in the UI but show up as JS errors or failed requests.
- **Test like a user, not a robot.** Try common workflows end-to-end. Click things a real user would click. Enter realistic data.
- **Type like a human.** When capturing repro evidence, type character-by-character (`browser_type` with slow typing, or type + short waits) -- not instant bulk fills.
- **Pace repro sequences for humans.** Add ~1s waits between actions and ~2s before the final result screenshot. A human reviewing the report needs to see what happened, not a blur of instant state changes.
- **Be efficient with calls.** Batch independent read-only calls (screenshot + console + network) in a single message. Never scroll with `browser_evaluate` -- use `browser_press_key` PageDown/End or click-through.

## References

| Reference | When to Read |
|-----------|--------------|
| [references/issue-taxonomy.md](references/issue-taxonomy.md) | Start of session -- calibrate what to look for, severity levels, exploration checklist |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/dogfood-report-template.md](templates/dogfood-report-template.md) | Copy into output directory as the report file |
