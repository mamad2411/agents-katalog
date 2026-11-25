---
name: reminders
description: Set, list, and manage timed reminders with optional voice call delivery.
tools: [reminders]
trigger: remind, reminder, alarm, wake, schedule, notify, alert, don't forget, remember to, at, tomorrow, tonight, later
---

# Reminders Skill

## Setting a Reminder
When the user asks you to remind them of something, output a tag in your response:

```
[SET_REMINDER: message text | ISO_datetime | delivery_method]
```

**delivery_method** options:
- `message` — send a Telegram message (default)
- `call` — make a voice call with TTS
- `both` — send message AND make a voice call

## Examples

User: "Remind me to call the dentist tomorrow at 3pm"
→ `[SET_REMINDER: Call the dentist | 2026-03-30T15:00 | message]`

User: "Wake me up at 7am with a call"
→ `[SET_REMINDER: Wake up! Good morning. | 2026-03-30T07:00 | call]`

User: "Remind me in 30 minutes to check the oven"
→ Calculate the time: now + 30 min = e.g. 2026-03-29T12:30
→ `[SET_REMINDER: Check the oven | 2026-03-29T12:30 | message]`

User: "Set an alarm for 6am tomorrow, call me and message me"
→ `[SET_REMINDER: Morning alarm - time to get up! | 2026-03-30T06:00 | both]`

## Timezone
IMPORTANT: Always use the user's configured timezone when computing reminder times.
The user's timezone is in USER.md or settings.yaml. Currently: Asia/Dubai (UTC+4).
When the user says "in 5 minutes" or "at 3pm", compute the datetime in their local timezone.
The ISO datetime in the SET_REMINDER tag must be in LOCAL time (not UTC).

## Important Rules
- ALWAYS use ISO format for datetime: YYYY-MM-DDTHH:MM
- Use the user's configured timezone (from USER.md or settings)
- For "in X minutes/hours", calculate the actual datetime
- For "tomorrow", use tomorrow's date
- Default to `message` delivery if the user doesn't specify
- Confirm what you set in your response text (the system will also confirm)

## Listing Reminders
When the user asks to see their reminders, tell them to use `/reminders`.

## Cancelling
Tell the user to use `/remind cancel <number>` to cancel a specific reminder.
