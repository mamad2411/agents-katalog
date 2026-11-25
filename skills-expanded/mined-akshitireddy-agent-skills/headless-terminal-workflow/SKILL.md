---
name: headless-terminal-workflow
description: Keep Windows commands and helper processes hidden during local execution and application testing.
---

# Headless Terminal Workflow

Honor the user's quiet-workspace preference.

- Launch task-owned command work through noninteractive execution, hidden/background processes, redirected logs, or headless automation.
- Prefer browser automation, file/log inspection, and process-level diagnostics over opening a terminal window.
- Do not deliberately surface, focus, move, maximize, or reuse a visible terminal on the user's desktop.
- A visible terminal is allowed only when it is genuinely necessary for a task and no headless route can provide the needed capability. State that limitation before opening it.
- Preserve user-owned terminals and other windows. Stopping a task-owned headless process is fine when it is no longer needed.
- This preference is independent of monitor placement: if a GUI is necessary, apply the secondary-display policy separately.
