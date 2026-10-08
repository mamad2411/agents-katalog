---
name: tt-sidebar
description: Open a live Token Tracker sidebar for only the current Codex session in a right-side terminal split at one-third width. Use when the user explicitly invokes $tt-sidebar or asks to monitor the current Codex session beside its terminal pane.
---

# TT Sidebar

<!-- token-tracker-managed -->

Run the installed launcher exactly once:

```bash
__TT_SIDEBAR_COMMAND__
```

Choose execution permissions from the current terminal environment before running it:

- On iTerm2 (`ITERM_SESSION_ID` set, with no `TMUX_PANE`), run the launcher outside the Codex sandbox by setting `sandbox_permissions` to `require_escalated`. Set `justification` to ask whether Token Tracker may control iTerm2 to create the sidebar pane. If reusable approval is supported, set `prefix_rule` to the complete launcher argv above; never approve Python generally. Do not first try the iTerm2 launcher inside the sandbox: macOS may hide iTerm2's AppleScript dictionary and misreport error `-2741`.
- On Ghostty (`TERM_PROGRAM=ghostty`, macOS, Ghostty ≥ 1.3.0), apply the same escalated execution as iTerm2: the launcher drives Ghostty's AppleScript `split` and the sandbox may hide Ghostty's scripting dictionary and misreport error `-2741`.
- On tmux (`TMUX_PANE` set), run the launcher with normal sandbox permissions.

Return the launcher's output directly. Do not run regular `tt sidebar`, inject a command into a transient shell, or open another sidebar in the current pane. If the launcher fails, report only its concise stage error.

The launcher must keep the source pane focused and open a right-side pane at one-third width. The split view is current-session-only and is intentionally independent from the regular all-session `tt sidebar` layout.
