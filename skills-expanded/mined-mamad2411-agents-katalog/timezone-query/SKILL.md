---
name: timezone-query
description: Get current time in any timezone and convert between timezones
---

# Time Zone Query

Get current time in any timezone and convert between timezones

## When to Use

- User wants to get time
- User wants to timezone convert
- User wants to current time
- Keywords: time, timezone, clock, convert

## Required Parameters

- **timezone** (string): IANA timezone like Asia/Shanghai or UTC

## Output

- **iso** (string): ISO 8601 timestamp
- **unix** (number): Unix timestamp
- **timezone** (string): Timezone used

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `get_time` -> 4 steps -> Exit: `ret_ok`, `ret_fail`
