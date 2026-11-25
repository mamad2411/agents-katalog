---
name: what-works
description: Coach — measures which segments, signals, Pastel agents, and message angles start real conversations, using Pastel stats, runs, and inbox data, and says how much to trust each finding. Use for "what's working", a weekly or monthly review, or before changing targeting or volume.
---

# What works — Coach

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Every comparison uses the same yardstick: hot replies per person reached.

## Steps

1. **Gather:** `pastel_get_workspace_stats` and `pastel_get_performance` for the period; `pastel_aggregate_leads` by `action` (signal type), `job_title`, and `industry`; `pastel_list_agents(include_stats=true)`; `pastel_list_sequence_runs`; `pastel_list_conversations` for outcomes.
2. **Funnel, as far as the data goes:** caught → scheduled → accepted → replied → hot → call. Pastel doesn't know about booked calls: stop at _hot_ unless the user shares their calendar or CRM numbers, and say so.
3. **Compare** by signal strength (🔥 / 🟠 / 🟡), by Pastel agent, by segment, and — where the drafts are readable — by message angle.
4. **Rank by hot replies ÷ people scheduled.**
5. **Confidence, stated for each finding:**
   - **strong** — at least 50 people scheduled in each group compared;
   - **early** — 15 to 49; worth a test, not a decision;
   - **anecdote** — under 15; mention, don't act on it.
6. **Recommend three moves at most**, each backed by the numbers above: pause an agent, test an angle, shift a segment. Changes to targeting go through `market-map`.

## Output

```
# What works — [period]
In one line:

Funnel:
Working (confidence):
Busy but not working:
Try next:
Open questions:
```
