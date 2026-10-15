---
name: hostlink-me
version: 1.0.0
description: "HostLink Me: Show current logged-in user profile and leave balances."
metadata:
  openclaw:
    category: "hostlink"
    requires:
      bins: ["hostlink"]
    cliHelp: "hostlink me --help"
---

# me

> **PREREQUISITE:** Run `hostlink set-token <token>` to authenticate before using any command.

Show the current logged-in user's profile and staff leave information.

```bash
hostlink me [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `hostlink me` | Show profile and leave balances |
| `hostlink me --json` | Output as JSON |

## Output Fields

### Profile
| Field | Description |
|-------|-------------|
| `user_id` | User ID |
| `username` | Login username |
| `first_name` / `last_name` | Full name |
| `email` | Email address |
| `phone` | Phone number |
| `addr1~3` | Address |
| `status` | Account status |
| `language` | Preferred language |
| `join_date` | Account join date |
| `expiry_date` | Account expiry date |

### Staff & Leave
| Field | Description |
|-------|-------------|
| `staff_id` | Staff record ID |
| `join_date` | Employment start date |
| `resign_date` | Resignation date (if any) |
| `totalJoinDayDisplay` | Human-readable days in service |
| `total_leave_day_available` | **Total available leave balance (days). This ALREADY INCLUDES `total_compensatory_leave`. Do NOT add `total_compensatory_leave` to this value — that would double-count it.** |
| `total_leave_hour_available` | **OT compensatory leave balance (hours)** |
| `annual_leave_hour` | Annual leave in hours |
| `total_compensatory_leave` | Compensatory leave (days). **This is a breakdown component already included in `total_leave_day_available`. It is shown for reference only.** |
| `total_compensatory_leave_hour` | Compensatory leave (hours) |
| `total_ot_to_cleave` | OT converted to comp leave |
| `total_no_pay_leave` | No-pay leave taken (days) |
| `total_annual_leave_to_no_pay_leave` | Annual leave converted to no-pay |

> ⚠️ **IMPORTANT — Avoid Double-Counting:**
> `total_leave_day_available` is the **final total** of all available leave days, which **already includes** `total_compensatory_leave`.
> **Never** compute `total_leave_day_available + total_compensatory_leave` — this will double-count compensatory leave days.

## Examples

```bash
# Show my profile and leave balances
hostlink me

# Output as JSON for scripting
hostlink me --json
```
