---
name: wechat-push-message
description: Push a WeChat message proactively (not as a reply). Uses Hermes cronjob system to deliver messages independently to the user's WeChat.
tags: [wechat, push, message, cronjob]
---

# WeChat Push Message

Send a proactive push message to the user's WeChat, not as a reply in the current conversation.

## Mechanism

Hermes' cronjob system has a `deliver` parameter. When you're in a WeChat session:
- `deliver='origin'` (default or omitted) → delivers back to the current WeChat chat
- `deliver='weixin'` → delivers to the WeChat home channel
- This is already proven to work — existing cron jobs (DeepSeek cost report, email triage) push to WeChat successfully.

## Usage

### Immediate push (fires in ~1 minute)

```python
# Create a one-shot job
cronjob(
    action='create',
    name='微信推送: <简短标题>',
    schedule='1m',    # fires once in 1 minute
    repeat=1,         # run once
    prompt='消息内容'
)
```

### Push with a specific delivery target

```python
cronjob(
    action='create',
    name='微信推送: <简短标题>',
    schedule='1m',
    repeat=1,
    deliver='weixin',   # explicitly target WeChat home channel
    prompt='消息内容'
)
```

### Immediate execution (within the current turn)

```python
# Step 1: Create the job
result = cronjob(action='create', name='微信推送...', schedule='1m', repeat=1, prompt='消息内容')

# Step 2: Run immediately
cronjob(action='run', job_id=result['job_id'])
```

The cron agent will run the prompt and deliver the response to the user's WeChat as an independent push message.

## Notes

- Messages arrive as independent push notifications, not as replies
- There's a rate limit (cooldown ~30s) from WeChat iLink — avoid pushing too frequently
- For long-running or recurring tasks, use the regular schedule format (e.g., `'0 9 * * *'` for daily at 9am)
- Keep the prompt self-contained — the cron session has no conversation context

## Pitfalls

- Don't push too frequently; WeChat iLink has rate limiting (~30s cooldown)
- The cron job runs in a fresh session with no conversation history — include all necessary context in the prompt itself
- Use `'origin'` when in a WeChat session for auto-detection; use `'weixin'` when you know the destination is WeChat
