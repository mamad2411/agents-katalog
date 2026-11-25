---
name: morning-brief
description: Morning plan — what Pastel caught overnight, who replied, what's stuck, and the five moves worth making today, each with its draft ready to approve. Use for "morning brief", "what should I do today", "daily plan", or a scheduled daily run.
---

# Morning brief

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Fifteen minutes of outbound, decided in advance. The brief reads and drafts; each move waits for a "go".

## Steps

1. **Can we send today?** `pastel_list_connected_accounts`.
2. **Replies:** `pastel_list_conversations(unread_only=true)`, tagged the `reply-desk` way. Hot ones lead the brief.
3. **Stuck:** `pastel_list_sequence_runs(status="needs_attention")`.
4. **New signals:** `pastel_recommend_best_leads(created_since=<yesterday>, limit=10)`, quickly checked against `outbound-brief.md`. Nothing new → the empty-result check; during a first run, the brief says so and lists the set-up moves to do meanwhile. (`pastel_get_crawl_status` only shows crawls running right now; the newest lead's date tells you whether agents are producing.)
5. **Posts worth a comment:** `pastel_recommend_best_posts(limit=5)`.
6. **Choose five moves**, in this order of value: answer hot replies → unblock stuck runs → comment on a strong post → first message to a new 🔥 lead → a scheduled nudge. Draft each with its skill, then `human-voice`.

## Output

```
# Today — [weekday]
Sending: ok | blocked · New signals: n · Unread: n · Stuck: n · Posts: n

1. [Move] — [Person, role] — [why, in one line]
   > draft
   Reply "go 1" to approve
…

Waiting on you:
Open questions:
```

"go N" runs that move through `campaign-launch`, `nudge`, or `social-warmup`.
