---
name: browser-testing
description: Browser automation for testing web applications. Covers tab management, element interaction, console log filtering, screenshot capture, and failure escalation. Use when testing web UI, verifying frontend changes, automating browser interactions, or when asked to check a web page.
user-invocable: true
---

# Browser Testing

CRITICAL: Always snapshot browser state before interacting. Never assume tabs or elements from a previous session still exist.

## Before Any Interaction

1. **Check for browser tools**: Verify that browser automation MCP tools are available. If not, tell the user and stop — don't attempt workarounds.
2. **Get tab context**: Call the tabs/context tool to see what's currently open. Never assume a tab exists from a prior session.
3. **Snapshot the page**: Capture the page structure and element references before clicking, typing, or hovering. Element refs are ephemeral — re-snapshot after any navigation or significant DOM change.

## Core Interaction Patterns

### Navigation
- Open new pages in new tabs within the user's existing browser session.
- After navigation, wait for the page to load before snapshotting. Use short incremental waits (1-2 seconds) with snapshot checks, not a single long wait.
- Track tab IDs during the session. Never reuse tab IDs from a previous session — they're invalid after the browser restarts.

### Element Interaction
- Always snapshot before clicking, typing, or selecting. Use the element ref from the most recent snapshot.
- For elements inside scroll containers, scroll the element into view before clicking.
- Use `fill` to replace input contents (clears first), `type` to append text.
- For contenteditable elements, use `fill` as well.

### Forms
- Use `fill_form` for multi-field forms — it's more reliable than filling fields one at a time.
- After submitting a form, wait for the response and snapshot to verify the result.

### Screenshots
- Take screenshots to verify visual state, capture bugs, or document behavior.
- Use element-scoped screenshots for focused verification (e.g., a specific component).
- Use full-page screenshots sparingly — they're large and often not necessary.

## Console Log Monitoring

- Check console messages after page loads and interactions to catch JavaScript errors.
- Filter console output for relevant patterns — don't dump the entire console.
- Common patterns to watch for:
  - `Error`, `TypeError`, `ReferenceError` — runtime JS failures
  - `Failed to load resource` — missing assets, broken API calls
  - `CORS` — cross-origin issues
  - `Warning` — React/framework warnings that may indicate bugs

## Modal and Dialog Handling

- Native browser dialogs (alert, confirm, prompt) are non-blocking in automation — they return immediately.
- Configure dialog handling BEFORE triggering the action that shows the dialog.
- Default: `confirm()` returns true, `prompt()` returns the default value.
- To test different responses, call the dialog handler with your desired values before clicking the trigger.

## Failure Escalation

- **2-3 failures on the same action**: Stop retrying. Report what's failing and ask the user for guidance.
- **Element not found**: Re-snapshot the page. If still not found, the DOM may have changed — search for the element by text or role instead of stale refs.
- **Navigation timeout**: Check if the server is running. Report the URL and timeout to the user.
- **Never retry infinitely.** If something doesn't work after 2-3 attempts, investigate why rather than retrying the same action.

## Verification Workflow

When verifying frontend changes:

1. Start the dev server if not already running (check first).
2. Navigate to the relevant page.
3. Snapshot and verify the expected UI elements are present.
4. Interact with the feature: click buttons, fill forms, navigate.
5. Check console for errors after each interaction.
6. Take screenshots of key states for evidence.
7. Test edge cases: empty inputs, boundary values, rapid clicks.
8. Report findings with screenshots as evidence.

## Network Request Monitoring

- Check network requests to verify API calls are being made correctly.
- Look for failed requests (4xx, 5xx status codes).
- Verify request payloads and response shapes match expectations.
- Monitor for unnecessary duplicate requests.

CRITICAL REMINDER: Snapshot before every interaction. Track tab IDs per session only. Stop after 2-3 failures and ask the user — don't retry infinitely.

## Related Skills

- Use `code-verification` patterns for the structured PASS/FAIL verdict after browser testing.
- After finding UI bugs, apply `systematic-debugging` patterns to trace the root cause.
- Use `effective-tool-use` patterns when starting dev servers and running build commands.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Dev server URL and start command
- Authentication steps required before testing
- Browser-specific test patterns for the project's framework
- Common UI components and their expected behavior
