---
name: visionaire-feedback
description: Collect and log feedback from [your name] after delivering significant work. Use after completing any meaningful deliverable — strategy docs, content drafts, brand work, code specs, research, creative briefs. Triggers when work is delivered and a response is received. Ask for a rating and optional comment, then log it. This feeds the self-study feedback-analysis loop.
---

# Visionaire Feedback Collection

After delivering significant work and receiving a response from [your name], collect feedback.

## When to collect
After delivering: strategy docs, content, brand work, code/specs, research, creative briefs, or any task [your name] asked for explicitly. Skip for quick factual answers, casual chat, or heartbeats.

## How to ask
Keep it light — one line at the end of the reply or as a follow-up:

> "How'd that land? Rate it 1–5 (and drop a note if something missed)."

or shorter:

> "Rate it 1–5?"

## Logging feedback
Once [Your name] responds with a rating, run:

```
node /data/.openclaw/workspace/scripts/log-feedback.mjs <rating> \
  --task "<short task description>" \
  --comment "<their comment if any>" \
  --tags "<relevant tags e.g. strategy,solana,content>"
```

## Notes
- Never ask for feedback twice on the same deliverable
- If [Your name] rates without a comment, log with empty comment — that's fine
- Feedback feeds directly into the self-study `feedback-analysis` loop (fires once 1+ entries exist)
- Cap is 100 entries — oldest drop off automatically
