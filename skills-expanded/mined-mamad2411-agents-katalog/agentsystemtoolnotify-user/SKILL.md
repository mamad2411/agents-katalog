---
name: agentsystemtoolnotify_user
description: agent.system.tool.notify user
---

# agent.system.tool.notify user

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **agent.system.tool.notify user**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/agent-zero/prompts/agent.system.tool.notify_user.md`

## 🧠 Master Agent Prompt & Capabilities

### notify_user:
This tool can be used to notify the user of a message independent of the current task.

!!! This is a universal notification tool
!!! Supported notification types: info, success, warning, error, progress

#### Arguments:
 *  "message" (string) : The message to be displayed to the user.
 *  "title" (Optional, string) : The title of the notification.
 *  "detail" (Optional, string) : The detail of the notification. May contain html tags.
 *  "type" (Optional, string) : The type of the notification. Can be "info", "success", "warning", "error", "progress".

#### Usage examples:
##### 1: Success notification
```json
{
    "thoughts": [
        "...",
    ],
    "tool_name": "notify_user",
    "tool_args": {
        "message": "Important notification: task xyz is completed succesfully",
        "title": "Task Completed",
        "detail": "This is a test notification detail with <a href='https://www.google.com'>link</a>",
        "type": "success"
    }
}
```
##### 2: Error notification
```json
{
    "thoughts": [
        "...",
    ],
    "tool_name": "notify_user",
    "tool_args": {
        "message": "Important notification: task xyz is failed",
        "title": "Task Failed",
        "detail": "This is a test notification detail with <a href='https://www.google.com'>link</a> and <img src='https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png'>",
        "type": "error"
    }
}
```

