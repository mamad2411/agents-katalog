---
name: ctf-dshield
description: Use when pi needs the local D盾 package for Windows webshell scanning, server hardening checks, or Web backdoor triage. Trigger on mentions of D盾, 网站后门查杀, 服务器安全检查, or Chinese Windows server defense tooling.
---

# Local Assets

- Tool root: N/A on this Linux host (D盾 is Windows-only).
- GUI executable: `D_Safe_Manage.exe` (Windows only; does NOT run here).

# Workflow

- Launch only when the user explicitly wants the GUI tool.
- Use it for scanning and review before making cleanup decisions.
- Prefer documenting findings or exportable evidence when used in incident response.

# Common Command

```bash
# D盾 (D_Safe_Manage.exe) is a Windows-only webshell scanner; it does NOT run on this Linux host.
# For webshell triage on Linux, prefer clamav (clamscan) or 河马 (hema-webshell) instead.
# If D盾 is required, ask the user to run it on a Windows host.
# D_Safe_Manage.exe
```

# Notes

- This is a GUI-first Windows tool.
- Opening it may require host permissions outside a sandboxed terminal session.
