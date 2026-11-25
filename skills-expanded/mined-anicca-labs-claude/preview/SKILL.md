---
name: preview
description: Take a browser screenshot of the running dev server, surface dev-server/console errors, and run tsc. Use after any UI change to verify the result visually before reporting done.
argument-hint: "[route]"
---

Capture and review the current state of the running dev server after the most recent code change.

## When to use

Call this after every UI change — new page, layout fix, Tailwind token update, component refactor. Do not report a UI task as done without running preview first.

## Steps

1. **Screenshot** — run the capture script with the route the change affects (defaults to `/`):

   ```bash
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/browser-screenshot.sh" "/dashboard/projects"
   ```

   The script prints the PNG path to stdout and emits diagnostics (HTTP status, hints) to stderr. It fails with a clear message if the dev server isn't running — start it with `yarn dev` (in the background) and retry.

2. **Read the image** — use the Read tool on the PNG path returned by the script. You will see the current page visually.

3. **Check for errors** — three places, in order:
   - The screenshot itself: Next.js renders a dev error overlay directly on the page — if the screenshot shows the red overlay, that error comes first
   - The terminal running `yarn dev` (check its background-task output): compile errors, server-component exceptions, hydration warnings
   - The HTTP status printed to stderr: a `500` means a server error even if the page painted something

4. **Type-check** — run `tsc --noEmit` and fix all errors.

5. **Evaluate against intent** — if `$ARGUMENTS` names a specific route, compare the screenshot to what the task asked for:
   - Spacing and alignment match the design
   - No overflow or clipped content
   - Loading states, empty states, and error states render correctly
   - Theme tokens resolve (no unstyled fallbacks or missing colors)
   - For layout-sensitive changes, capture a second shot at a narrow viewport (`--viewport-size` in the script, or pass a mobile-width base URL setup) when responsiveness is part of the task

6. **Iterate** — if the visual output doesn't match intent, fix the issue and re-run from step 1. Repeat until the screenshot confirms correctness.

7. **Report** — describe what you see in the screenshot and confirm it matches the task goal. If the dev server isn't running, tell the user to start it with `yarn dev` — do not fail silently.

## Rules

- Never skip this skill after a UI change and claim "it should look like X" — verify it
- If the screenshot shows the Next.js error overlay, fix that error before any other work
- If the route requires auth, the screenshot will show the login redirect — either preview a public route that exercises the same component, or note the limitation explicitly rather than pretending the page was verified
- `tsc --noEmit` must pass before the task is complete
