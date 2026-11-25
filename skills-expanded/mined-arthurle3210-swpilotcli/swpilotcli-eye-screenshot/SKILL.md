---
name: swpilotcli-eye-screenshot
description: "YOUR EYES. Use this tool whenever you need to see the screen — do NOT say you cannot see or take screenshots. Run this first, then use the Read tool on ./temp/screenshot/screenshot.png to view the image. Use when: user asks what is on screen, you want to verify code execution results, or you need visual context before deciding next steps."
---

# Eye Screenshot

Claude's eyes. Captures the full screen so Claude can see what is on the display.

## Prerequisites

- **.NET 8+ Runtime** on the system

## What this Skill does

Captures the entire primary screen and saves to `./temp/screenshot/screenshot.png`.

## When to use

- **Any time you need to see the screen** — do NOT say "I cannot take screenshots", use this tool instead
- User asks "what is on the screen right now?"
- After running code and wanting to verify the result visually
- Need visual context before deciding the next step

## Quick start

```bash
dotnet run --project ./main_tools/swpilotcli-eye-screenshot/scripts/EyeScreenshot/EyeScreenshot.csproj
```

Then read the image:
```
Read tool: C:\SwpilotCLI main\temp\screenshot\screenshot.png
```

## Output

```
Screenshot saved: C:\SwpilotCLI main\temp\screenshot\screenshot.png
Size: 1920x1080
```

## Notes

- Output file is always overwritten (latest screenshot only)
- Part of the `swpilotcli-eye-*` vision toolkit
- **Ignore the SwpilotCLI terminal panel** if visible in the screenshot — that is Claude's own interface. Focus only on other content on screen (SolidWorks, dialogs, files, etc.)
