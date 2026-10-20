---
name: ctf-windows-privesc
description: Use when pi needs the local Windows 提权 tool set for privilege-escalation enumeration or exploit helpers such as winPEAS and JuicyPotato on an authorized Windows target. Trigger on mentions of 提权, winPEAS, JuicyPotato, or Windows local privesc triage.
---

# Local Assets

- Tool root: N/A on this Linux host (these are Windows-target binaries).
- Files: `winPEAS.bat`, `winPEASx64.exe`, `JuicyPotato.exe`

# Workflow

- Confirm the target OS version, integrity level, and privilege context first.
- Prefer `winPEAS` for enumeration before choosing an exploit helper.
- Use JuicyPotato only when the host version and COM/DCOM prerequisites make sense.

# Common Commands

```bash
# These are Windows-target privilege-escalation helpers; they run ON a Windows target, not on this Linux host.
# Transfer the matching binary (winPEASx64.exe / JuicyPotato.exe) to the Windows target and execute there.
# On this Linux host, use linpeas / linpeas.sh for Linux privesc enumeration instead.
# winPEAS.bat / winPEASx64.exe / JuicyPotato.exe -h
```

# Notes

- This bundle is for authorized Windows privilege-escalation work only.
- Capture the enumeration output before taking exploit actions.
