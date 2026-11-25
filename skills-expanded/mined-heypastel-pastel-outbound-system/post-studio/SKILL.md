---
name: post-studio
description: Storyteller — writes LinkedIn posts designed to make the user's buyers comment, using what the market is discussing in Pastel, then turns everyone who engages into leads. Use for "write a LinkedIn post", post ideas, a content calendar, lead-magnet posts, or growing inbound from LinkedIn.
---

# Post studio — Storyteller

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Outbound reaches people one by one; a good post brings them to you. Every person who comments or reacts becomes a lead with a signal attached.

## Steps

1. **Find what the market is talking about:** `pastel_aggregate_posts(group_by="intent_tag", range="30d")` and `pastel_recommend_best_posts` show the themes and questions buyers engage with right now. Add `competitor-watch` findings if available.
2. **Pick one idea per post**, from one of these angles:
   - **a number from the user's own work** ("we reviewed 200 onboarding calls…");
   - **a strong opinion** the audience half-agrees with;
   - **a teardown** of how something is done badly, and what works instead;
   - **a giveaway** — a template, checklist, or resource offered to people who comment. Only offer what the user can actually deliver.
3. **Write it:**
   - the first two lines must work on their own (that's all LinkedIn shows before "…see more");
   - short paragraphs, one idea;
   - end with a question or a clear call to comment;
   - 120–250 words; no hashtag wall (three at most).
4. **Run `human-voice`**, then give two opening lines to choose from.
5. **After publishing (2–5 days later):** find the post with `pastel_query_posts` and pull the engagers with `pastel_leads_for_post`. Hand them to `fit-check` with the signal "engaged with our post on [date]". For a giveaway post, list who asked for it so the user can send it.

The user publishes the post themselves; this skill never posts on their behalf.

## Output

```
# Post — [topic]

Opening A:
> …
Opening B:
> …

Post:
> …

Why this will get the right people talking: [one line]
After publishing: run post-studio again with "who engaged" in 2–5 days.
```
