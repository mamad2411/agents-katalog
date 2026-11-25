---
name: leave-tracker
description: >
  Check open leaves for deadline alerts and required decisions. Surfaces only
  the leaves that require an action and explains why — not a status board.
  Use weekly, or whenever the attorney needs to know which leaves have
  upcoming designation, certification, or exhaustion deadlines.
argument-hint: "[no arguments — works from HRIS or leave-register.yaml]"
---

# /leave-tracker (HK)

Checks all open leave entries under the Employment Ordinance (Cap 57) and surfaces only the ones
requiring a decision or action. Not a status board — tells you what you need
to do and why.

**HK statutory leave types to track:**
- Statutory holidays (12+ per year under Cap 57 s. 39)
- Statutory annual leave (7–14 days depending on length of service, Cap 57 Part IX)
- Paid sickness days (accumulating up to 120 days, Cap 57 Part VIII)
- Maternity leave (14 weeks, Cap 57 Part III)
- Paternity leave (5 days, Cap 57 Part IIIA)
- Bereavement leave (no HK statutory requirement — governed by contract)
- Examination leave (Cap 279 Apprenticeship Ordinance — apprentices only)
- Court attendance / jury service (but HK has no jury in civil cases)

## Instructions

1. Load the `leave-tracker` agent and run the full workflow.

2. If no HRIS is connected and no `~/.claude/plugins/config/claude-for-hk-law/employment-legal/leave-register.yaml` exists, prompt
   the attorney to upload a leave spreadsheet or use
   `/employment-legal:log-leave` to add entries.

3. Alerts only for leaves requiring action. Clean leaves summarized one line each.

## Examples

```
/employment-legal:leave-tracker
```

Run this weekly — set a Monday-morning reminder to invoke
`/employment-legal:leave-tracker`. Automated scheduling requires a separate
integration (calendar reminder, cron job, etc.); Claude Code agents do not
self-schedule.
