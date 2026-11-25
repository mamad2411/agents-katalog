---
name: dooray-hook
description: Send automated notifications to Dooray! messenger channels via webhooks.
homepage: https://dooray.com
metadata:
  openclaw:
    emoji: "📨"
    requires:
      bins: ["python3"]
---

# Dooray! Webhook Skill

A seamless integration to send text notifications and status updates to **Dooray!** chat rooms using Incoming Webhooks.

## Overview

This skill allows OpenClaw to communicate with your team on Dooray!. It supports multiple chat rooms and customizable bot profiles.

## Configuration

To use this skill, you must define your Dooray! webhook URLs in the OpenClaw global config (`~/.openclaw/openclaw.json`):

```json
{
  "skills": {
    "entries": {
      "dooray-hook": {
        "enabled": true,
        "config": {
          "botName": "YOUR BOT NAME",
          "botIconImage": "[https://static.dooray.com/static_images/dooray-bot.png](https://static.dooray.com/static_images/dooray-bot.png)",
          "rooms": {
            "General": "[https://hook.dooray.com/services/YOUR_TOKEN_1](https://hook.dooray.com/services/YOUR_TOKEN_1)",
            "Alerts": "[https://hook.dooray.com/services/YOUR_TOKEN_2](https://hook.dooray.com/services/YOUR_TOKEN_2)"
          }
        }
      }
    }
  }
}

```

### Setup Instructions

1. Navigate to your Dooray! Project/Mail → **Settings** → **Incoming Webhook**.
2. Create a new webhook and copy the URL.
3. Add the URL to the `rooms` dictionary in your config as shown above.

## Usage

### 💬 Natural Language

You can ask OpenClaw to send messages directly:

* *"Send 'Server deployment successful' to the Alerts room on Dooray."*
* *"Tell the General channel that I'll be late for the meeting."*

### 💻 CLI Execution

```bash
python scripts/send_dooray.py "RoomName" "Your message content"

```

## Technical Details

* **Zero Dependencies**: Uses Python's built-in `urllib.request` and `json` modules. No `pip install` or `venv` required.
* **Payload Structure**:
* `botName`: Customizable via config.
* `botIconImage`: Optional avatar URL.
* `text`: Plain text message.



## Troubleshooting

* **Room Not Found**: Ensure the room name matches the key in your `openclaw.json` exactly (case-sensitive).
* **Invalid URL**: Verify the webhook URL starts with `https://hook.dooray.com/services/`.
* **Permission Denied**: Check if the script `scripts/send_dooray.py` has execution permissions.

