---
name: competitor-watch
description: Radar — reads what the competitors Pastel tracks are posting, who engages with it, and what those people complain about, then turns it into leads and angles. Use for "who's engaging with [competitor]", competitor intelligence, a weekly competitor digest, or ideas for displacement messages and posts.
---

# Competitor watch — Radar

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

People who engage with a competitor are already shopping. Their comments also tell you, in their own words, what the competitor doesn't solve.

## Steps

1. **List the competitors** from `pastel_get_workspace_context` and `outbound-brief.md`. The user can add names.
2. **Their recent posts:** `pastel_query_posts` with each competitor's name as `search`, status `ALL`. Open the most engaged ones with `pastel_get_details`.
3. **Who engaged:** `pastel_leads_for_post` on each of those posts. Keep people who fit `outbound-brief.md`; note how many engaged with more than one competitor.
4. **What they're saying:** from the comments, collect complaints, missing features, pricing reactions, and questions that went unanswered. Quote exactly; a paraphrase is not evidence.
5. **Turn it into moves:**
   - leads → lead cards with signal "engaged with [competitor] on [date]", handed to `fit-check`;
   - recurring complaints → angles for `message-writer` (only ones our product actually answers);
   - open questions → post ideas for `post-studio`.

Messages talk about the problem the comments reveal, not about the competitor: naming a rival in a first message tends to start a debate instead of a conversation.

## Output

```
# Competitor watch — [period]

| Competitor | Posts read | People engaged | Fit our brief |

What people say (quoted):
- "…" — [role], on [competitor]'s post, [date]

Leads handed to fit-check: n
Angles for message-writer:
Post ideas for post-studio:
Open questions:
```
