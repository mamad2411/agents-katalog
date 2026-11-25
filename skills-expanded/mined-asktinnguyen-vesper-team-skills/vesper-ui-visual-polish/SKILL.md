---
name: vesper-ui-visual-polish
description: Use this skill when improving or polishing Vesper Electron UI/UX and you want to work from real screenshots of the dev instance instead of code alone. It routes the debuggable dev window to the target view, captures before/after screenshots with CDP, and iterates visually between edits.
---

# Vesper UI Visual Polish

Use this skill for Vesper desktop UI refinement when visual truth matters: layout polish, spacing, hierarchy, readability, empty states, modal cleanup, docs surfaces, settings pages, sidebars, or renderer regressions that need screenshot-driven iteration.

## First Principles

- Use the dev instance, not the installed production app.
- Prefer CDP screenshots from the Electron renderer over macOS OS-level screenshots.
- Capture first, edit second.
- Re-capture after each meaningful UI pass.
- Keep changes scoped to the mapped renderer component and any shared CSS actually responsible for the issue.

## Pairing Skills

- Use `frontend-design` for design direction and anti-patterns.
- Use `polish` for final-pass spacing, hierarchy, and interaction-state checks.
- Use `vesper-electron-testing` when the change also needs durable automated coverage.
- For other UI/UX moves, see [references/related-uiux-skills.md](references/related-uiux-skills.md) and load only the relevant section.

## Companion Skills

This skill is the visual orchestration layer. It should own the screenshot-driven loop:

1. capture the real dev-instance UI
2. inspect what is visually wrong
3. choose the right UI/UX sub-skill
4. patch the code
5. re-capture and compare

Do not load every related skill by default. Use soft progressive disclosure:

- If the issue is primarily final-fit-and-finish, load `polish`.
- If the UI is too busy or overbuilt, load `distill`.
- If the screen works but lacks warmth or memorable touches, load `delight`.
- If the issue is resilience, overflow, empty/error states, or production reality, load `harden`.
- If the bottleneck is runtime speed, loading, animation smoothness, or bundle weight, load `optimize`.
- If the design is visually aggressive, loud, or overstimulating, load `quieter`.
- If you need diagnosis before changing anything substantial, load `audit`.
- If motion and interaction feedback are the missing ingredient, load `animate`.

The visual screenshot loop stays the same regardless of which companion skill is loaded.

## Primary Workflow

1. Find the target component from UI inspector context or by tracing the route.
2. Ensure a Vesper dev instance is running.
3. Capture a before screenshot from the debuggable dev window.
4. View the screenshot and identify concrete visual issues.
5. Patch the mapped source and the narrowest styling layer that can fix the issue.
6. Wait for hot reload, then capture an after screenshot.
7. Compare before/after and keep iterating until the page feels intentional.
8. Report the visual outcome, screenshot artifact path, and any unrelated verification failures separately.

## Dev Instance Rules

- Default target is the running Vite/Electron dev app on `http://localhost:5174`.
- If you need isolation, launch a dedicated dev instance with `VESPER_DEV_MODE=1` and a unique config/workspace dir.
- If launching Electron directly, put the app path before the remote debugging flag:

```bash
VESPER_DEV_MODE=1 \
VESPER_INSTANCE_ID=polish01 \
VESPER_DEV_WORKTREE=/Users/tinnguyen/vesper \
VESPER_DEV_BRANCH=main \
VITE_DEV_SERVER_URL=http://localhost:5174 \
VESPER_APP_NAME='Vesper Dev (polish01)' \
VESPER_CONFIG_DIR=/tmp/vesper-polish-config \
VESPER_WORKSPACES_DIR=/tmp/vesper-polish-config/workspaces \
VESPER_DEEPLINK_SCHEME=vesper-dev-polish01 \
./node_modules/.bin/electron apps/electron --remote-debugging-port=9222
```

Why: Vesper’s dev protocol bootstrap expects `process.argv[1]` to be the app path, and `VESPER_DEV_MODE=1` avoids colliding with the already-running instance lock.

## Screenshot Loop

Use the bundled CDP capture helper:

```bash
/Users/tinnguyen/vesper-team-skills/vesper-app-skills/vesper-ui-visual-polish/scripts/cdp-screenshot.js \
  --route 'docs/page/getting-started/index' \
  --workspace-id 'ws_123' \
  --wait-for 'Getting Started with Vesper' \
  --out /tmp/vesper-ui-before.png
```

Then inspect it locally:

```bash
open /tmp/vesper-ui-before.png
```

After edits:

```bash
/Users/tinnguyen/vesper-team-skills/vesper-app-skills/vesper-ui-visual-polish/scripts/cdp-screenshot.js \
  --route 'docs/page/getting-started/index' \
  --workspace-id 'ws_123' \
  --wait-for 'Getting Started with Vesper' \
  --out /tmp/vesper-ui-after.png
```

## When Capturing

- Route directly to the target screen instead of navigating manually where possible.
- If a modal blocks the surface, dismiss it first and capture again.
- Favor exact UI issues:
  - oversized type
  - weak hierarchy
  - wasted right-edge space
  - awkward top spacing
  - table density problems
  - breadcrumb invisibility
  - low-contrast helper copy

## Editing Heuristics

- Fix shell issues in the page container first: width, padding, top rhythm, sticky headers, breadcrumbs.
- Fix readability in a docs-scoped class before touching shared markdown globally.
- Prefer widening the reading measure a little before shrinking everything dramatically.
- Reduce type in small steps and re-capture.
- Avoid styling changes that would affect chat markdown unless the user asked for a broader system update.
- If multiple issues are present, use this order by default:
  1. `audit` when diagnosis is unclear
  2. `distill` or `quieter` to fix structural overload
  3. `harden` or `optimize` for robustness/perf constraints
  4. `animate` or `delight` for experience uplift
  5. `polish` as the final pass

## Verification

- Re-capture the exact same route after edits.
- Compare the two screenshots, not just the code diff.
- If typecheck/test fails in unrelated files, call that out explicitly instead of blocking the polish work.

## Good Outcomes

- The screenshot looks clearly more readable before you explain why.
- The content uses the available panel width intelligently.
- Hierarchy is visible at a glance.
- The UI feels designed, not merely rendered.
