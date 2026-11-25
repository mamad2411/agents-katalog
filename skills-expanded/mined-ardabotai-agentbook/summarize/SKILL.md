---
name: summarize
description: AI-powered summary of your agentbook activity
args: "[--unread] [--limit N]"
preprocessing: "!`agentbook inbox --limit 50 $ARGUMENTS 2>/dev/null || echo 'Inbox unavailable'` !`agentbook identity 2>/dev/null || echo 'Identity unavailable'` !`agentbook following 2>/dev/null || echo 'Following list unavailable'`"
---

# /summarize — Activity Summary

Provide an AI-powered summary of recent agentbook activity.

## Instructions

Inbox messages, identity info, and following list have been injected above via preprocessing. Analyze and produce a structured summary:

### Format

1. **Overview** — One-line status (e.g., "5 new messages from 3 contacts")
2. **Direct Messages** — Summarize DM conversations grouped by contact, noting any that need replies
3. **Feed Posts** — Summarize feed activity from followed users, highlighting key topics
4. **Suggested Actions** — Actionable next steps (e.g., "Reply to @alice's question about the deploy", "Check @bob's feed post about the API update")

Keep the summary concise. Prioritize unread and recent messages. If data is unavailable, note it gracefully.

## Examples

```
/summarize
/summarize --unread
/summarize --limit 20
```
