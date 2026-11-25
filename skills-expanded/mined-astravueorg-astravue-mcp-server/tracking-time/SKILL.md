---
name: tracking-time
description: Tracks time on tasks using timers or manual entries and generates timesheet reports in Astravue. Use when logging work hours, starting or stopping a timer, reviewing time entries, generating timesheets, or asking "how much time was spent on this?".
---

# Tracking Time

## Workflow

1. **Identify the task**

   Confirm which task to track time for. Use `astravue_list_project_tasks` or `astravue_find_tasks` to locate the task ID.

2. **Check for active timers**

   Always call `astravue_get_active_timers` before starting a new timer — only one timer can run at a time per user.

3. **Log time**

   Choose the method that fits:
   - `astravue_start_timer` / `astravue_stop_timer` — real-time tracking
   - `astravue_log_manual_time` — log a duration with a start time
   - `astravue_log_time_range` — log a start-to-end time range

4. **Review entries**

   - `astravue_get_task_time_entries` — entries for a specific task
   - `astravue_get_project_time_summary` — billable vs non-billable totals
   - `astravue_get_project_time_entries` — detailed entries grouped by member
   - `astravue_get_timesheet_report` — global report grouped by member or project

5. **Delete entries**

   Use `astravue_delete_time_entry` only after confirming with the user. This cannot be undone.

## Important

- Time values from the API are in milliseconds — convert to hours and minutes for display
- Only set billable or notes when the user explicitly provides them
- Present reports with billable ratio and per-member breakdown
