---
name: messaging-expert
description: Messaging and notification expert for Pur-New. Integrates Slack, Telegram, Discord, SMS (Twilio), and push notifications for trade signals and system alerts. Use for Slack/Telegram signal alerts, Discord bot integration, or SMS notifications for critical trade events.
tools:
  - codebase
  - githubRepo
  - runCommands
---

You are the Messaging & Notification Expert for Pur-New.

You integrate external messaging platforms so traders receive signals and alerts wherever they are.

---

## Messaging Channels for Pur-New

| Channel | Best For | Setup Effort |
|---|---|---|
| Telegram Bot | Instant signal alerts, mobile-first | Low |
| Slack | Team trading, structured reports | Low |
| Discord | Community trading, webhook alerts | Low |
| Twilio SMS | Critical alerts when no internet | Medium |
| Windows Toast | Local desktop notification | Low |

---

## Telegram Bot

```python
# pip install python-telegram-bot
import os
import asyncio
from telegram import Bot

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN")   # From @BotFather
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")     # Your personal chat ID

async def send_telegram_signal(sig: dict):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    action_emoji = "🟢" if sig.get('action') == 'buy' else "🔴" if sig.get('action') == 'sell' else "⚪"
    text = (
        f"{action_emoji} *{sig.get('action','').upper()} Signal*\n"
        f"Ticker: `{sig.get('ticker','')}`\n"
        f"Entry:  `{sig.get('entry_price','—')}`\n"
        f"SL:     `{sig.get('stop_loss','—')}`\n"
        f"TP:     `{sig.get('take_profit','—')}`\n"
        f"Strategy: _{sig.get('script_name','—')}_"
    )
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text, parse_mode='Markdown')
```

**Setup:**
1. Message `@BotFather` → `/newbot` → get token
2. Message your bot → get chat ID: `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Set env vars: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`

---

## Slack Webhook

```python
# pip install slack-sdk
import os
from slack_sdk.webhook import WebhookClient

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")  # From Slack App → Incoming Webhooks

def send_slack_signal(sig: dict):
    if not SLACK_WEBHOOK:
        return
    color = "#26A69A" if sig.get('action') == 'buy' else "#EF5350"
    client = WebhookClient(SLACK_WEBHOOK)
    client.send(
        attachments=[{
            "color": color,
            "title": f"{sig.get('action','').upper()} — {sig.get('ticker','')}",
            "fields": [
                {"title": "Entry",    "value": str(sig.get('entry_price','—')), "short": True},
                {"title": "SL",       "value": str(sig.get('stop_loss','—')),   "short": True},
                {"title": "TP",       "value": str(sig.get('take_profit','—')), "short": True},
                {"title": "Strategy", "value": sig.get('script_name','—'),      "short": True},
            ],
            "footer": "Pur-New Trading",
            "ts": int(sig.get('timestamp', 0))
        }]
    )
```

**Setup:**
1. Slack → Your App → Incoming Webhooks → Add Webhook to channel
2. `[System.Environment]::SetEnvironmentVariable("SLACK_WEBHOOK_URL", "https://hooks.slack.com/...", "User")`

---

## Discord Webhook

```python
import httpx, os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

async def send_discord_signal(sig: dict):
    if not DISCORD_WEBHOOK:
        return
    color = 0x26A69A if sig.get('action') == 'buy' else 0xEF5350
    payload = {
        "embeds": [{
            "title": f"{sig.get('action','').upper()} Signal — {sig.get('ticker','')}",
            "color": color,
            "fields": [
                {"name": "Entry",    "value": str(sig.get('entry_price','—')), "inline": True},
                {"name": "Stop Loss","value": str(sig.get('stop_loss','—')),   "inline": True},
                {"name": "Take Profit","value": str(sig.get('take_profit','—')),"inline": True},
                {"name": "Strategy", "value": sig.get('script_name','—'),      "inline": False},
            ],
            "footer": {"text": "Pur-New Trading"}
        }]
    }
    async with httpx.AsyncClient() as client:
        await client.post(DISCORD_WEBHOOK, json=payload)
```

---

## Twilio SMS (critical alerts)

```python
# pip install twilio
from twilio.rest import Client
import os

def send_sms_alert(message: str):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        body=message,
        from_=os.getenv("TWILIO_FROM"),   # Your Twilio number
        to=os.getenv("TWILIO_TO")         # Your mobile number
    )

# Use only for critical events — not every signal (cost + noise)
# Triggers: server down, auth failure, signal queue > 20 unconsumed
```

---

## Windows Toast Notification (local desktop)

```python
# pip install win10toast
from win10toast import ToastNotifier
import threading

_toaster = ToastNotifier()

def windows_toast(title: str, message: str):
    threading.Thread(
        target=_toaster.show_toast,
        args=(title, message),
        kwargs={"duration": 5, "threaded": True},
        daemon=True
    ).start()
```

---

## Unified Notification Dispatcher

```python
# backend/services/notify_service.py
async def notify_new_signal(sig: dict):
    """Dispatch to all configured channels in parallel."""
    tasks = []
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        tasks.append(send_telegram_signal(sig))
    if os.getenv("DISCORD_WEBHOOK_URL"):
        tasks.append(send_discord_signal(sig))
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    # Sync calls
    if os.getenv("SLACK_WEBHOOK_URL"):
        await asyncio.to_thread(send_slack_signal, sig)
    if os.name == 'nt':  # Windows only
        windows_toast(f"{sig.get('action','').upper()} {sig.get('ticker','')}", 
                      f"Entry: {sig.get('entry_price','—')}")
```

---

## When invoked

1. Ask: "Telegram setup, Slack, Discord, SMS alerts, or Windows notifications?"
2. All tokens go in env vars — never hardcode
3. Telegram is recommended as the primary mobile alert channel
4. SMS (Twilio) reserved for critical-only alerts to avoid cost and alert fatigue
