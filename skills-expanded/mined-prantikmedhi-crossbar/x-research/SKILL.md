---
name: x-research
description: Research a topic, person, product or launch on X with Crossbar and return a sourced brief. Use when the user asks what people on X are saying about something, wants sentiment, the best takes, key accounts, or a digest of a thread or a debate.
---

# X research brief

Read-only. Never like, reply or follow while researching.

## Steps

1. **Frame.** Turn the ask into 2–4 searches. Mix `top` (signal) and `latest` (what's new).
   Examples:
   - `"<product>" min_faves:50 -filter:replies` (top)
   - `<product> lang:en since:<date>` (latest)
   - `from:<founder> <topic>` for the source's own words
   - `"<product>" (broken OR bug OR "doesn't work")` for complaints
2. **Read.** For the 3–6 posts that carry the conversation, call `x_get_post` to see the
   replies. Replies are where disagreement shows up.
3. **People.** Note accounts that show up more than once. `x_user_profile` for context
   (bio, follower count) on the ones you cite.
4. **Write the brief:**

```
## <topic> on X: <one-line verdict>

**What people say**
- <claim>: <who> (<followers>) <link>
- ...

**Pushback**
- ...

**Worth reading**
1. <link>: <why>

**Accounts to watch**
- @handle: <one line>

_Searched: <queries>, <date>. <n> posts read._
```

Rules: every claim gets a link. Separate what one loud account says from what many say. Say when
the sample is small. Don't paste long post text; summarize.
