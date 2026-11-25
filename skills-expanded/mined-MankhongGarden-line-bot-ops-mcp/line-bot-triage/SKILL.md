---
name: line-bot-triage
description: Diagnose a LINE bot that stopped replying, replies late, or replies twice, using the line-bot-ops tools. Use when the user says the bot is silent, slow, duplicating messages, or asks why a message was never answered.
---

# LINE bot triage

Work from the queue outward. Most silent bots are a stuck or failing worker, not a LINE outage.

1. `line_queue_health`. Read three numbers:
   - Oldest pending job older than a minute or two: the worker isn't being triggered or is crashing before it claims jobs.
   - Jobs stuck in `processing`: the worker started and died mid-job (timeout, out of memory).
   - Many `failed`: go to step 2.
2. `line_failed_jobs`. Group the errors. One repeated error is a code or config bug; show the user the error text and the message that caused it before suggesting a fix.
3. Only after the cause is fixed, offer `line_retry_job` for the affected jobs. Tell the user first that a retried job which replies may fail again because reply tokens expire soon after the event, and that a push is the fallback.
4. If the queue is healthy, check LINE's side: `line_bot_info` (token valid, chat mode is bot) and `line_message_quota` (push quota exhausted means pushes fail while replies still work).
5. Duplicate replies with a healthy queue usually mean the webhook handler does slow work before answering, so LINE redelivers. Point the user at the fast-ack pattern in the bot's webhook route.

Never call `line_push_text`, `line_link_richmenu` or `line_broadcast` during triage without the user's explicit OK for that specific message or user.
