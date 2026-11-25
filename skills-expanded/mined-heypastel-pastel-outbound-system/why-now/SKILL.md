---
name: why-now
description: Detective — builds a one-sentence reason to talk to a specific person now, from what they did (Pastel signal), what changed around them (company news), and what they care about (their posts). Use to research a lead or an account, after fit-check, before writing.
---

# Why now — Detective

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

The output is a single sentence that ties this person to this week. Everything else is working notes.

## Three sources, one sentence

For each lead marked _yes_:

1. **What they did** — the Pastel signal: `pastel_get_details`, and the post or comment itself.
2. **What changed around them** — company news from the last 90 days: a launch, a hire, a round, a new market. Company website, LinkedIn page, blog, press page. Dates matter more than adjectives.
3. **What they care about** — their own recent posts (`pastel_query_posts` with their name), and the words they use for their work.

Then write **why now** in their language: _"You asked your network last week how other teams handle X, two months after opening Y."_

## Quality bar

- **Specific:** it names something only this person did, said, or is going through.
- **Dated:** it points to something from the last 90 days. Without that, mark it `no-moment` — `priority-rank` scores it lower.
- **Ours to say:** the proof it leans on comes from `outbound-brief.md`, never from assumptions.

## Output per lead

```
lead_id:
did:         # the signal, dated
changed:     # company news, dated, or "nothing found"
cares_about: # from their posts, or "no posts"
why_now:     # one sentence
proof:       # from outbound-brief.md only
avoid:
quality: sharp | thin | no-moment
sources:
```
