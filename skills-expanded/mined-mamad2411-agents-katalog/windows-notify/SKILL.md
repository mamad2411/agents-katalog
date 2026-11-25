---
name: windows-notify
description: >-
  Send Windows 11 toast notifications with custom app icons (-AppLogo), real-time progress percentages (%),
  start/completion alerts, and sound feedback using PowerShell BurntToast.
  Use whenever a background task, backup, build, server restart, or long process requires visual notification feedback.
---

# XYZ Windows Notify — Universal AI Agent Skill

This skill enables any AI agent (Antigravity, Claude, GPT, Cursor, etc.) to trigger native **Windows 11 Toast Notifications** using PowerShell `BurntToast`.

## Installation via Skills CLI

```bash
npx skills add xyz-rainbow/xyz-windows-notify
```

## Key Capabilities

- 🎨 **Custom App Icons**: Pass `-AppLogo "U:\Pictures\Icons\unicorn.jpg"` or custom image paths.
- 📊 **Percentage Progress Updates (%)**: Send notifications at milestones (every 10%, 25%, etc.).
- 🚀 **Lifecycle Alerts**: Start, In-Progress, Success (100%), and Error notifications.
- 🔊 **Sound Feedback**: Play Windows native notification sounds (`-Sound 'Default'`).

---

## Quick Start (PowerShell)

```powershell
Import-Module BurntToast

# Simple Toast Notification with Custom Icon
New-BurntToastNotification `
    -Text "🦄 Task Started", "Backup process is now running in background..." `
    -AppLogo "U:\Pictures\Icons\unicorn.jpg" `
    -Sound 'Default'
```

---

## Python Integration Pattern

```python
import subprocess
import os

def send_toast(title, message, icon_path="U:\\Pictures\\Icons\\unicorn.jpg"):
    try:
        if os.path.exists(icon_path):
            ps_cmd = f"Import-Module BurntToast; New-BurntToastNotification -Text '{title}', '{message}' -AppLogo '{icon_path}' -Sound 'Default'"
        else:
            ps_cmd = f"Import-Module BurntToast; New-BurntToastNotification -Text '{title}', '{message}' -Sound 'Default'"
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd], capture_output=True)
    except Exception:
        pass

# Example Usage
send_toast("🚀 Backup Iniciado", "Analizando archivos en L:\\ y U:\\...")
send_toast("📊 Progreso: 50%", "Copiados 1,024 MB de 2,048 MB")
send_toast("✅ Backup COMPLETADO (100%)", "2,100 archivos copiados exitosamente a D:\\")
```

---

## Global Agent Skill Setup

To install this skill globally for any AI agent on Windows:

```bash
npx skills add xyz-rainbow/xyz-windows-notify
```

Or manually copy `SKILL.md` to your global skill directory (e.g. `C:\Users\<user>\.gemini\config\skills\windows-notify\SKILL.md`).
