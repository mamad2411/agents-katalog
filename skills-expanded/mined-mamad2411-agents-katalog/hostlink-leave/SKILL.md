---
name: hostlink-leave
version: 1.0.0
description: "HostLink Leave: Submit and list staff leave requests interactively."
metadata:
  openclaw:
    category: "hostlink"
    requires:
      bins: ["hostlink"]
    cliHelp: "hostlink leave --help"
---

# leave

> **PREREQUISITE:** Run `hostlink set-token <token>` to authenticate before using any command.

Manage staff leave requests on the HostLink platform. Supports 4 leave types, each with different required fields.

```bash
hostlink leave <command> [flags]
```

## Commands

| Command | Description |
|---------|-------------|
| `hostlink leave add` | Submit a new leave request (interactive wizard) |
| `hostlink leave list` | List my leave requests |

---

## add

Interactive wizard that guides you through submitting a leave request. Before prompting, it displays your current leave balances.

```bash
hostlink leave add
```

### Leave Types

| Value | Type | Required Fields |
|-------|------|----------------|
| `0` | 年假 (Annual Leave) | from_date, from_time, to_date, to_time |
| `1` | 病假 (Sick Leave) | from_date, from_time, to_date, to_time |
| `3` | 時薪年假 (Hourly Annual Leave) | from_date, start_time, hour |
| `4` | 無薪假 (No Pay Leave) | from_date, from_time, to_date, to_time |

### from_time / to_time values

| Value | Meaning |
|-------|---------|
| `0` | 上午 (AM) |
| `1` | 下午 (PM) |

### Wizard flow

1. Displays annual leave balance and OT comp leave hours
2. Prompts: leave type → from_date → type-specific fields → remark → confirm
3. For types 0/1/4: shows **estimated leave days** before confirmation
4. For type 3: accepts `start_time` (HH:MM) and `hour` (0.5–8, multiples of 0.5)

```bash
# Example session
hostlink leave add

👤 John Smith
📊 Annual Leave Balance:     10 day(s)
⏱  OT Comp Leave (hours):    4 hr(s)

? 請假類型 (Leave Type): 年假 (Annual Leave)
? 開始日期 (From Date) [YYYY-MM-DD]: 2026-04-01
? 開始時間 (From Time): 上午 (AM)
? 結束日期 (To Date) [YYYY-MM-DD]: 2026-04-03
? 結束時間 (To Time): 下午 (PM)
? 備註 (Remark) [optional]: Family trip

📅 預估請假天數 (Estimated): 3 day(s)

? 確認提交請假申請? (Confirm submit?) Yes

✅ Leave request submitted successfully!
   ID:        42
   Type:      年假 (Annual Leave)
   From:      2026-04-01
   To:        2026-04-03
   Status:    pending
   Remark:    Family trip
```

```bash
# Hourly Annual Leave example
hostlink leave add

? 請假類型 (Leave Type): 時薪年假 (Hourly Annual Leave)
? 開始日期 (From Date) [YYYY-MM-DD]: 2026-04-01
? 開始時間 (Start Time) [HH:MM]: 14:00
? 小時數 (Hours) [0.5 - 8]: 2
? 備註 (Remark) [optional]:
? 確認提交請假申請? (Confirm submit?) Yes

✅ Leave request submitted successfully!
```

---

## list

List all of your own leave requests.

```bash
hostlink leave list [flags]
```

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON |

```bash
# List all leave requests
hostlink leave list

# JSON output
hostlink leave list --json
```

### Sample output

```
[42] 年假 (Annual Leave) | 2026-04-01 AM → 2026-04-03 PM | pending | Family trip
[43] 時薪年假 (Hourly Annual Leave) | 2026-03-15 14:00 (2h) | approved
```

---

## Leave balance

Use `hostlink me` to view your full leave balance summary:

```bash
hostlink me
```

Key fields:
- `Annual Leave Balance` — remaining annual leave days
- `OT Comp Leave (hours)` — available OT compensatory leave hours (convert to annual leave at `/my/convert-ot` before using)
