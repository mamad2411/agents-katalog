---
name: proactive-check
description: Run on scheduler ticks to evaluate due reminders, approaching deadlines, and upcoming schedule events.
---

# Proactive Check Skill

## Purpose
Evaluate active tasks, reminders, and schedule events on periodic cron ticks. Dispatches proactive notifications when action or preparation is required.

## Core Rules
- **Fast & Silent**: When nothing is due or approaching, produce no output.
- **Zero Emojis**: Do not use emojis in proactive messages. Use bold `*text*` for titles and times.
- **Deduplication**: Never send duplicate alerts for the same threshold.

## Evaluation Thresholds
1. **Due Reminders**: If the reminder time has arrived, dispatch the alert to the target recipient and mark as fired.
2. **Task Lead-Time & Deadlines**:
   - *Lead-Time Buffer*: If current time enters the task's lead-time window, send a preparation heads-up.
   - *Due Alert*: When deadline arrives, alert the assignee.
   - *Overdue Escalation*: If an urgent task passes its deadline without completion, send periodic nudges.
3. **Calendar Events**:
   - Send an upcoming event notice within 1 hour before scheduled start time.

## Delivery Routing
- Individual tasks/reminders are dispatched directly to the person's DM.
- Shared couple tasks (`assignee="Both"`) or important couple dates are dispatched to the Trio group chat.
