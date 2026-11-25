---
name: ctf-antsword
description: Use when pi needs the AntSword client for connecting to and managing an already-authorized WebShell session. Trigger on mentions of AntSword, 蚁剑, WebShell client management, or interactive shell management.
---

# Local Assets

- Tool root: wherever AntSword is installed.
- GUI executable: `AntSword` (Linux build) / `AntSword.exe` (Windows). The win32 loader does NOT run on this Linux host.

# Workflow

- Launch only when the user explicitly wants the GUI workflow.
- Use it only for authorized shells or lab environments.
- Prefer non-GUI tooling when the task can be completed in-shell.

# Common Command

```bash
# AntSword is a Windows/macOS/Linux GUI client; the win32 loader above does NOT run on this Linux host.
# Install the Linux build of AntSword, or use an alternative webshell manager (e.g. a custom Python handler).
# If only the Windows build is available, ask the user to run it on a Windows host.
antsword        # if the Linux build is installed
```

# Notes

- This is an interactive GUI client, not a command-line scanner.
- Opening the GUI may require host permissions outside a sandboxed shell.
