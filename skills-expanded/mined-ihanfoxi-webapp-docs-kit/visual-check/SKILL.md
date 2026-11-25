---
name: visual-check
description: Visually verifies UI changes in a web app. Takes Playwright screenshots of the affected screens, looks at them, and reports JavaScript errors, console errors, failed HTTP responses, blank pages and unexpected redirects. Use when asked for "/visual-check", after finishing a change to anything the user sees (views, styles, components, messages), or to see how a screen looks. Does not produce manuals or videos.
argument-hint: "[path or description of the change]"
---

# Visual check

A UI change is not done until someone **looks** at the screen. A successful
build, a deploy and an HTTP `200` prove nothing about what the user will see. A
collapsed panel, an icon that fails to load, a half-transparent dialog or
personal data left unblurred only show up in the screenshot.

`$V` is this skill's `scripts/` folder. The `user-manual` and `video-tutorial`
skills of webapp-docs-kit reuse these scripts.

## Before you start

1. If `$V/node_modules` does not exist, run `cd $V && npm install` and
   `node node_modules/playwright-core/cli.js install chromium`.
2. Look for `docs/webapp-docs.json` in the project. If it is missing, create it
   following `references/configuration.md`. Take the base URL from the
   project's `README.md`, `CLAUDE.md`/`AGENTS.md` or run scripts. Ask the user
   which environment to use if it is not obvious: local, dev or staging.
   **Never use production.**
3. The change must be running in that environment. If it is not, follow the
   project's own instructions to build and start or deploy it.

## Screens behind sign-in or other preconditions

This kit does not sign in, handle credentials or assume user roles. If a screen
you need is behind a login, a paywall, a feature flag, a specific role or any
other precondition (`check.js` reports a redirect, or the screenshot shows a
sign-in page), **stop and ask the user how they want to handle it**. It is
their decision. Never ask for, type or store passwords, tokens or cookies
yourself, and never work around access controls.

## Steps

1. **Pick what to check.** Take the views touched by the change (`git diff`).
   If the change depends on state (an open panel, an applied filter, a
   dialog), reproduce it with `--click` and `--type`.
2. **Screenshot** from the project root:
   ```bash
   node $V/check.js <path> [options]
   ```
   | Option | Purpose |
   |---|---|
   | `--click "SEL1\|SEL2"` | Open panels, tabs, dropdowns and dialogs, in order |
   | `--type "SEL\|text"` | Type into filters and search boxes |
   | `--wait MS\|SEL` | Slow screens or animated dialogs |
   | `--full` | Full page |
   | `--mobile` | Phone viewport (390×844), when the view must be responsive |
   | `--exists SEL` / `--text SEL` | Check an element without looking at the image. Useful to tune selectors |
   | `--html` | Save the rendered HTML to look for selectors |
   | `--redact SEL` | Blur more personal data on top of the config's `redact` list |
   | `--mock FILE` | Screens that need fake API data |

   The screenshot is saved in `~/.cache/webapp-docs-kit/screenshots/<app>/`, outside the repository.
3. **Open the image with your file-reading tool. Do not skip this step.** Check
   that the change looks as requested and that nothing around it broke:
   alignment, clipped text, overlaps, icons, colors and empty states.
4. **Read the `problems:` section of the output.** Report JavaScript errors,
   console errors, HTTP responses ≥ 400, blank pages and redirects. A new error
   on a screen that looks fine is still a defect.
5. If something is wrong, fix it, redeploy and take the screenshot again.
   Compare it with the previous one.

## Rules

- **Read-only.** `--click` and `--type` are for filtering, navigating and
  opening panels. `check.js` refuses to click Save, Delete, Submit, Send, Sign
  and similar buttons. Use `--allow-change` only when the user explicitly
  authorizes that specific case, and only in a test environment.
- `--text` prints unblurred data to the terminal. Do not copy it into documents or commits.
- Known pitfalls (prefixed ids, animated dialogs, charts that render late,
  JSF/PrimeFaces, SPAs) are in `references/capture-pitfalls.md`.

## Report

For each screen checked, give the path, whether it looks right or what is
wrong, the problems detected, and the screenshot path. Do not say "verified"
unless you opened the image.
