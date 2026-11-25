---
name: powershell-ui-workflows
description: Help design, review, and maintain PowerShell user interfaces, including WinForms dialogs, WPF/XAML tools, terminal UI flows, interactive admin utilities, progress displays, input validation, event handling, background work, UI-thread marshaling, cleanup, and packaging considerations.
---

# PowerShell UI Workflows

Use this skill when a PowerShell task needs a graphical or terminal interface. Keep the automation logic separate from the UI so the core behavior remains testable.

## Choose the Interface

- Use simple console prompts only for short, low-risk interactive scripts.
- Use WinForms for small Windows desktop tools and straightforward dialogs.
- Use WPF with XAML for richer Windows layouts, stronger binding, or more complex visual structure.
- Use terminal UI patterns for cross-platform or remote-friendly tools.
- Use a web UI or non-PowerShell frontend when the tool needs broad distribution, accessibility, or multi-user access.

## Design Workflow

1. Clarify target users, host environment, and whether the tool must run on Windows only.
2. Separate business logic into functions or modules before building the UI.
3. Choose the simplest UI framework that satisfies the workflow.
4. Validate input before invoking privileged or destructive actions.
5. Provide progress and cancellation for long-running work.
6. Keep state transitions explicit: initialize, load, run, complete, error, cleanup.
7. Manually test UI flows on the target host; UI behavior is easy to get subtly wrong.

## Implementation Guidance

- Keep event handlers thin; call testable functions from handlers.
- Avoid blocking the UI thread with long-running PowerShell commands.
- Use runspaces, jobs, or another background pattern for work that may take noticeable time.
- Marshal updates back to the UI thread: WinForms uses `Invoke()`/`BeginInvoke()`, and WPF uses the dispatcher.
- Dispose forms, controls, timers, runspaces, and other resources for tools that stay open.
- Use anchoring, docking, layout panels, or adaptive sizing instead of hard-coded coordinates for complex forms.
- Show friendly errors to users while logging enough technical detail for maintainers.

## Anti-Patterns

- Mixing all business logic directly into button click handlers.
- Creating a GUI for automation that would be safer and clearer as a CLI.
- Freezing the interface while commands run.
- Updating controls directly from a background thread.
- Storing secrets in form fields longer than necessary.
- Assuming a desktop session exists when the script may run in CI, remoting, or scheduled task contexts.
