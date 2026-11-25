---
name: generating-status-report
description: Generates executive project status reports from Astravue data including task progress, budget consumption, and project health. Use when asked for a status update, project summary, executive report, or "how is the project going?".
---

# Generating Status Report

## Workflow

1. **Identify scope**

   Clarify which project and audience (executive vs team). Use `astravue_list_projects` to help select.

2. **Collect data**

   - `astravue_get_project` — status, health, priority, dates, budget fields
   - `astravue_internal_get_project_stats` — task completion metrics
   - `astravue_list_overdue_tasks` — overdue count and details
   - `astravue_get_project_time_summary` — billable vs non-billable hours

3. **Write the report in narrative paragraphs**

   Cover four sections:

   **Project Overview** — status, health, completion %, whether on schedule.

   **Task Progress** — total, completed, pending, overdue. Use plain language.

   **Budget** — allocated vs spent, billable vs non-billable, remaining. Compare budget consumption % to completion %.

   **Risks** — overdue tasks, budget concerns, schedule slippage.

4. **Present to user**

   Ask if they want adjustments or more detail on any section.

## Important

- Write in narrative form, not raw data dumps
- Always include context with numbers: "64% budget consumed at 68% completion — on track"
- Tailor depth to audience
