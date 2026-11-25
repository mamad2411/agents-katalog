---
name: remindme
description: ⏰ simple Telegram reminders for OpenClaw. 
tags: [telegram, cron, reminders, productivity, schedule]
metadata:
  {
    "openclaw":
      {
        "summary": "⏰ **Remind Me:** Schedule Telegram reminders using plain natural language. Just type what and when — like \"in 5 minutes\" or \"tomorrow at 9am\" — and it works. Fast, reliable, no setup.",
        "emoji": "⏰"
      }
  }
user-invocable: true
command-dispatch: tool
command_tool: exec
command_template: "node --import tsx skills/remindme/src/index.ts --chat-id {chatId} {args}"
---

# ⏰ Remind Me

Set reminders in Telegram using normal human language.

## 🚀 How to Use

Just type what you want and when:

- `/remindme drink water in 10m`
- `/remindme tomorrow 9am standup`
- `/remindme next monday call mom`
- `/remindme in 2 hours turn off oven`

No menus. No setup. No thinking.

## ✨ Why It’s Good

- **Natural language:** say it like a human
- **Fast:** reminder is scheduled instantly
- **Accurate:** runs on OpenClaw cron
- **Safe in groups:** reminders don’t get lost

## 🛠️ How It Works

Runs a background process that schedules reminders reliably through OpenClaw.
