---
name: vs-ui-explore
description: Autonomously explore the UI of a Visual Studio debuggee via vs-mcp UIA tools (ui_snapshot, ui_find_elements, ui_wait_*) and produce a structured bug/coverage report. Use when the user asks to "test all screens", "crawl the UI", "find UI bugs autonomously", or similar.
---

# vs-ui-explore

Drive a running, debugged desktop application from Visual Studio through its UI
using the `vs-mcp` UI Automation tools. The goal is to visit every reachable
screen/dialog, exercise interactive elements, and collect a structured report
of crashes, unhandled dialogs, UIA binding errors, disabled-but-expected
states, and unreachable features.

This skill is the Windows/VS analogue of iOS `ios-simulator-skill`. It expects
the target application to already be running under the VS debugger before the
crawl starts.

## When to use this skill

Trigger when the user says things like:
- "Test all the screens of this app"
- "Crawl the UI and tell me what's broken"
- "Run through every dialog and report issues"
- "Find UI bugs autonomously"

Do not trigger for single, targeted UI actions ("click Save", "open the
Settings dialog") — use the individual `ui_*` tools directly for those.

## Prerequisites

Before starting a crawl, confirm via `get_status`:

1. A solution is open in Visual Studio.
2. `debugMode` is `Run` (the target is being debugged). If it is
   `Design`, ask the user whether to start debugging first via
   `debug_start` or `debug_start_without_debugging`; do not start it
   silently because the user may want to target a specific configuration.
3. The debuggee has a visible main window (`ui_capture_window` must not
   error with "no debugged process").

If any of the above fails, stop and ask the user how to proceed instead of
guessing.

## Crawl loop

For each iteration the agent should:

1. **Observe.** Call `ui_snapshot` with `depth: 8`, `includeScreenshot: true`.
   The compact tree returned already prunes offscreen/boring containers and
   annotates each node with its `role`, `id`, `name`, `actions`, and `state`.
2. **Fingerprint the screen.** Build a signature from
   `window.title + focused.role + focused.automationId + top-level child roles`.
   Skip screens you have already explored (track signatures in memory for the
   duration of the crawl).
3. **Catalogue interactive targets.** From the tree, collect every node whose
   `actions` array contains `invoke`, `toggle`, `select`, or `expand`. Prefer
   elements with meaningful `name` or `id`; de-prioritize anonymous `Custom`
   controls unless nothing else is available.
4. **Decide the next action.** Pick one interactive target that has not been
   exercised yet on this screen. Prefer:
   - Buttons whose name suggests navigation ("Next", "Open", menu items,
     tabs) over destructive verbs ("Delete", "Remove", "Uninstall").
   - Toggles and selects *last*, since they rarely reveal new screens.
5. **Act.** Use `ui_invoke` (preferred when an AutomationId exists) or
   `ui_click` (by name if no id). Never fall back to raw coordinates.
6. **Settle.** Immediately call `ui_wait_idle` with `quietMs: 600`,
   `timeoutMs: 4000` so any async UI updates finish before the next
   observation.
7. **Verify.** Call `ui_snapshot` again. If the focused window title changed
   or a new dialog appeared, treat it as a new screen and recurse. If nothing
   changed after a non-trivial action, record that as a suspicious result.
8. **Escape dialogs.** If a modal dialog appears that you did not intend
   (error, confirmation, progress), record it, close it via the most benign
   option (`Cancel`, `Close`, `No`), and continue. Never click `Delete`,
   `Uninstall`, `Reset`, or similar destructive defaults. If the only option
   is destructive, stop and ask the user.

Cap the crawl at a reasonable iteration count (default 40 steps or 10
distinct screens) and stop early if nothing new is discovered for 5
consecutive iterations.

## Dangerous actions — hard stops

Never invoke a control whose name matches any of the following without first
asking the user:

- `Delete`, `Remove`, `Uninstall`, `Reset`, `Restore Defaults`, `Format`
- `Sign out`, `Log out`, `Clear history`, `Clear cache`
- `Overwrite`, `Discard changes`, `Revert`
- Anything that looks like a payment/purchase button
- `OK` on a dialog whose message text you have not read

If a confirmation dialog ships with a pre-selected destructive default, cancel
it and move on; do not "just try it".

## Bug signals to record

While crawling, flag any of the following in the report:

- **Error dialogs** — window titles containing `Error`, `Exception`,
  `Failed`, `Unhandled`. Capture the message text via `ui_find_elements`
  with `controlType: ControlType.Text` scoped to the dialog's
  `ancestorAutomationId`.
- **Unhandled exceptions in the debugger** — check with `debug_get_mode`
  after each action. If it returns `Break` unexpectedly, call
  `debug_get_callstack` and include the top frame in the report.
- **UIA binding errors** — run `diagnostics_binding_errors` once before the
  crawl and once after; diff the results.
- **Disabled controls where enabled was expected** — e.g. a Save button
  that is always `disabled` even after editing content.
- **Dead screens** — a screen where no interactive control changes any
  observable state.
- **Focus traps** — a dialog that cannot be closed via any of its own
  buttons.
- **Output pane errors** — after the crawl, pull the last N lines via
  `output_read` and grep for `error`/`exception`/`failed`.

## Report format

Produce a Markdown report with the following sections:

```markdown
# UI Crawl Report — <app name> — <ISO date>

## Summary
- Screens visited: N
- Interactive elements exercised: N
- Issues found: N (critical: X, warning: Y, info: Z)
- Crawl duration: Xs

## Screens Visited
1. `<window title>` — <N elements> — <link to first screenshot>
   ...

## Issues
### Critical
- **Unhandled exception at <callstack frame>**
  - Reproduction: Main → <Button A> → <Button B>
  - Evidence: screenshot hash / debug mode / top frame

### Warning
- **"Save" button remains disabled after editing document**
  - Screen: Document Editor
  - Expected: enabled once text changes
  - Observed: `state: disabled` across 4 snapshots

### Info
- **Unreachable feature: "Export as PDF" menu item never fires a dialog**

## Coverage Gaps
- Screens the crawler suspects exist but could not reach, with the reason.

## Recommended Next Steps
- Concrete actions the user should take based on findings.
```

Always include at least one screenshot per unique screen (from
`ui_snapshot`'s image content block) and cite element ids/names so the user
can reproduce each finding.

## Integration notes

- Prefer `ui_snapshot` over `ui_get_tree` + `ui_capture_window` — it returns
  both in one round-trip with an already-pruned tree.
- Prefer `ui_find_elements` with `nameMatch: "contains"` or `"regex"` when
  looking for fuzzy matches like "any button whose name contains 'Save'".
- Scope searches with `ancestorAutomationId` when you know which dialog is
  active — it dramatically reduces noise.
- Never call `ui_wait_idle` with a `timeoutMs` greater than ~10s; if the app
  is hung longer than that, record it as an issue and move on.
- Respect the user's CLAUDE.md rules: do not start debugging, close VS, or
  modify code without an explicit ask.
