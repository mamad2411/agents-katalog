---
name: date-time-cli
description: Date, time, timezone, and epoch timestamp manipulation from the command line. Use when user mentions "date command", "timestamp", "epoch", "unix timestamp", "timezone conversion", "date math", "date formatting", "ISO 8601", "convert timestamp", "time ago", or any date/time manipulation in shell.
---

# Date & Time CLI

## Current Date and Time

```bash
date                        # system default format
date +%s                    # epoch seconds (Unix timestamp)
date +%Y-%m-%d              # 2026-04-13
date +"%Y-%m-%d %H:%M:%S"  # 2026-04-13 14:30:00
date +%T                    # 14:30:00 (shorthand for %H:%M:%S)
date -u                     # UTC time
```

## Format Strings

| Token | Meaning            | Example    |
|-------|--------------------|------------|
| `%Y`  | 4-digit year       | 2026       |
| `%m`  | Month (01-12)      | 04         |
| `%d`  | Day (01-31)        | 13         |
| `%H`  | Hour 24h (00-23)   | 14         |
| `%M`  | Minute (00-59)     | 30         |
| `%S`  | Second (00-59)     | 45         |
| `%s`  | Epoch seconds      | 1681400000 |
| `%N`  | Nanoseconds (GNU)  | 123456789  |
| `%Z`  | Timezone name      | EDT        |
| `%z`  | Timezone offset    | -0400      |
| `%A`  | Day of week name   | Monday     |
| `%a`  | Day abbrev         | Mon        |
| `%B`  | Month name         | April      |
| `%j`  | Day of year        | 103        |
| `%u`  | Day of week (1=Mon)| 1          |
| `%F`  | Shorthand %Y-%m-%d | 2026-04-13 |

## macOS vs GNU date -- Critical Differences

macOS ships BSD `date`. Linux ships GNU `date`. They are not compatible.

### Parse a date string

```bash
# GNU (Linux)
date -d "2026-04-13 14:30:00" +%s

# macOS (BSD)
date -j -f "%Y-%m-%d %H:%M:%S" "2026-04-13 14:30:00" +%s
```

### Date math

```bash
# GNU (Linux) -- use -d with relative strings
date -d "now + 3 days"
date -d "2026-04-13 + 2 hours"
date -d "yesterday"
date -d "last monday"

# macOS (BSD) -- use -v with adjustment flags
date -v+3d                  # 3 days from now
date -v-2H                  # 2 hours ago
date -v+1m                  # 1 month from now (lowercase m = month)
date -v+30M                 # 30 minutes from now (uppercase M = minute)
date -v-1y                  # 1 year ago
date -v+1w                  # 1 week from now
```

macOS `-v` flags: `y` year, `m` month, `w` week, `d` day, `H` hour, `M` minute, `S` second.

## Epoch Conversions

Epoch **seconds**: 10 digits (e.g., `1681400000`). Epoch **milliseconds**: 13 digits (e.g., `1681400000000`). If 13 digits, divide by 1000 first.

```bash
# Seconds to human-readable
# GNU
date -d @1681400000
# macOS
date -r 1681400000

# Milliseconds to human-readable
# GNU
date -d @$((1681400000000 / 1000))
# macOS
date -r $((1681400000000 / 1000))

# Human-readable to epoch seconds
# GNU
date -d "2026-04-13T14:30:00" +%s
# macOS
date -j -f "%Y-%m-%dT%H:%M:%S" "2026-04-13T14:30:00" +%s

# Current epoch
date +%s
```

## ISO 8601

```bash
# GNU
date --iso-8601=seconds          # 2026-04-13T14:30:00-04:00

# macOS (no --iso-8601 flag, construct manually)
date -u +"%Y-%m-%dT%H:%M:%SZ"   # 2026-04-13T18:30:00Z
date +"%Y-%m-%dT%H:%M:%S%z"     # 2026-04-13T14:30:00-0400
```

Note: ISO 8601 wants `-04:00` not `-0400`. GNU handles this; on macOS insert the colon yourself.

## Timezone Conversion

```bash
# Show time in a specific timezone (works on both GNU and macOS)
TZ="America/New_York" date
TZ="Europe/London" date
TZ="Asia/Tokyo" date
TZ="UTC" date

# Convert a specific timestamp to another timezone
# GNU
TZ="Asia/Tokyo" date -d "2026-04-13 14:30:00 EDT"
# macOS
epoch=$(date -j -f "%Y-%m-%d %H:%M:%S" "2026-04-13 14:30:00" +%s)
TZ="Asia/Tokyo" date -r "$epoch"

# List available timezones
ls /usr/share/zoneinfo/America/
```

## Compare Two Dates

Convert both to epoch, then compare.

```bash
# GNU
d1=$(date -d "2026-04-13" +%s)
d2=$(date -d "2026-05-01" +%s)

# macOS
d1=$(date -j -f "%Y-%m-%d" "2026-04-13" +%s)
d2=$(date -j -f "%Y-%m-%d" "2026-05-01" +%s)

# Compare
if [ "$d1" -lt "$d2" ]; then
  echo "d1 is earlier"
fi

# Difference in days
diff_days=$(( (d2 - d1) / 86400 ))
echo "$diff_days days apart"
```

## Parse Dates from Strings

```bash
# GNU date is very flexible
date -d "April 13, 2026" +%F
date -d "13 Apr 2026" +%F
date -d "next friday" +%F
date -d "2 weeks ago" +%F

# macOS requires exact format specification
date -j -f "%B %d, %Y" "April 13, 2026" +%F
date -j -f "%d %b %Y" "13 Apr 2026" +%F
```

## Useful One-Liners

### How long ago was this timestamp

```bash
# Given an epoch timestamp
ts=1681400000
now=$(date +%s)
diff=$((now - ts))
echo "$((diff / 86400)) days, $(( (diff % 86400) / 3600 )) hours ago"
```

### What day of the week was a date

```bash
# GNU
date -d "2026-04-13" +%A        # Monday

# macOS
date -j -f "%Y-%m-%d" "2026-04-13" +%A
```

### Seconds between two timestamps

```bash
# GNU
echo $(( $(date -d "2026-05-01" +%s) - $(date -d "2026-04-13" +%s) ))

# macOS
echo $(( $(date -j -f "%Y-%m-%d" "2026-05-01" +%s) - $(date -j -f "%Y-%m-%d" "2026-04-13" +%s) ))
```

### Relative time description

```bash
relative_time() {
  local diff=$(( $(date +%s) - $1 ))
  if   [ $diff -lt 60 ];    then echo "${diff}s ago"
  elif [ $diff -lt 3600 ];  then echo "$((diff/60))m ago"
  elif [ $diff -lt 86400 ]; then echo "$((diff/3600))h ago"
  else echo "$((diff/86400))d ago"
  fi
}
relative_time 1681400000
```

## Date in Scripts

### Generate timestamped filenames

```bash
backup_file="db-backup-$(date +%Y%m%d-%H%M%S).sql.gz"
log_file="deploy-$(date +%F).log"
```

### Log timestamps

```bash
log() { echo "[$(date +"%Y-%m-%d %H:%M:%S")] $*"; }
log "Deployment started"
# [2026-04-13 14:30:00] Deployment started
```

### Measure elapsed time

```bash
start=$(date +%s)
# ... do work ...
echo "Took $(( $(date +%s) - start ))s"
```

## When `date` Is Not Enough

### Python

```bash
python3 -c "from dateutil.parser import parse; print(parse('April 13, 2026 2:30 PM').isoformat())"
python3 -c "from datetime import datetime; print(datetime.fromtimestamp(1681400000000/1000))"
python3 -c "from datetime import datetime,timezone; print((datetime.now(timezone.utc)-datetime(2026,4,13,tzinfo=timezone.utc)).total_seconds())"
python3 -c "from datetime import datetime; from zoneinfo import ZoneInfo; print(datetime.now(ZoneInfo('Asia/Tokyo')))"
```

### Node

```bash
node -e "console.log(new Date(1681400000000).toISOString())"
node -e "console.log(new Date('April 13, 2026').toISOString())"
node -e "console.log(Date.now())"                              # current epoch ms
node -e "console.log((Date.now() - new Date('2026-04-13').getTime()) / 3600000, 'hours')"
```

## Quick Reference

| Task                         | GNU (Linux)                          | macOS (BSD)                                    |
|------------------------------|--------------------------------------|------------------------------------------------|
| Current epoch                | `date +%s`                           | `date +%s`                                     |
| Epoch to date                | `date -d @EPOCH`                     | `date -r EPOCH`                                |
| Parse date string            | `date -d "STRING"`                   | `date -j -f "FMT" "STRING"`                    |
| Add 3 days                   | `date -d "now + 3 days"`            | `date -v+3d`                                   |
| Subtract 2 hours             | `date -d "now - 2 hours"`           | `date -v-2H`                                   |
| ISO 8601                     | `date --iso-8601=seconds`           | `date -u +"%Y-%m-%dT%H:%M:%SZ"`               |
| Specific TZ                  | `TZ="Zone" date`                     | `TZ="Zone" date`                               |
