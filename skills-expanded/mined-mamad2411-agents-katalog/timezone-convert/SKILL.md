---
name: timezone-convert
description: "Convert between timezones using command-line tools."
metadata:
  openclaw:
    emoji: "🕐"
---

# Timezone Convert

Convert between timezones.

## Convert

```bash
# Current time in different timezone
TZ="America/New_York" date
TZ="Europe/London" date
TZ="Asia/Tokyo" date

# Convert specific time
TZ="America/New_York" date -d "2024-01-15 14:30 UTC"

# List available timezones
timedatectl list-timezones 2>/dev/null || ls /usr/share/zoneinfo/
```

## Tips for AI Agents

- Use IANA timezone names (e.g., "America/New_York"), not abbreviations.
- UTC is the universal reference — convert to/from UTC for reliability.
