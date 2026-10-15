---
name: clock
description: >
  Reports current system date, time, timezone, and Unix epoch from the host
  machine. Use when user asks "what time is it?", "what's today's date?",
  "what timezone am I in?", or any query about the present moment.
---

## When to use

Trigger on any query about current real-world time/date:
- "What time is it?"
- "What's today's date?"
- "Is it a leap year?"
- "What's the current Unix timestamp?"

Do **not** use for: time-zone math, date arithmetic, parsing user-supplied dates. This skill only reports *now*.

## How to run

Execute one of these via the shell tool, depending on host OS:

**Linux / macOS / Git Bash:**
```bash
date '+Current Date: %Y-%m-%d
Current Time: %H:%M:%S
Timezone: %Z
Unix Epoch: %s'
```

**Windows PowerShell (no bash available):**
```powershell
$d = Get-Date
"Current Date: $($d.ToString('yyyy-MM-dd'))"
"Current Time: $($d.ToString('HH:mm:ss'))"
"Timezone: $([System.TimeZoneInfo]::Local.Id)"
"Unix Epoch: $([DateTimeOffset]::Now.ToUnixTimeSeconds())"
```

## Output format

Always present in this exact 4-line shape:

```
Current Date: YYYY-MM-DD
Current Time: HH:MM:SS
Timezone: <abbrev or IANA name>
Unix Epoch: <integer>
```

## Notes

- Timezone reporting depends on host. POSIX `date '+%Z'` returns abbreviation (`IST`, `PST`); PowerShell returns IANA-style id. Both acceptable.
- Always read directly from system. Never fabricate or estimate.
