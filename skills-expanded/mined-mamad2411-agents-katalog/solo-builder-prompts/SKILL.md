---
name: solo-builder-prompts
description: Use when the user wants a ready-made prompt for a solo/indie product-marketing task — a landing page headline, App Store title/subtitle/keywords, a behavioral onboarding email sequence, launch-day comment replies, a reply to a first user's message, rewriting rough notes into an email, making an email sound human, or building a 30-day content calendar from 5 content pillars. Trigger phrases include "write my landing page headline", "help with App Store metadata", "onboarding emails", "launch day comments/replies", "reply to this user", "content calendar", "content pillars", "30-day content plan", or "/solo-builder-prompts". Also use when the user just wants the raw prompt text to paste elsewhere themselves.
---

# Solo Builder Prompts

Five copy-paste prompt templates for the marketing tasks a solo or indie
product builder repeats most often. Originally shared as a TikTok carousel by
`@luc1r6` ("Five prompts I use for everything that is not code"); kept here
as a reusable local skill.

Each prompt below is a template with a `[paste]` placeholder. When invoked:

1. If the user names a specific task (headline, App Store, onboarding email,
   launch comments, first user reply), fill in that one template using
   whatever context the user has already given in this conversation, asking
   only for what's still missing (e.g. the product description, the
   activation action, the message to reply to). Then run the filled prompt
   as an actual request — produce the output, don't just hand back the
   template.
2. If the user doesn't name a task, or asks to see them all, list all five
   with their placeholders intact so they can be copied elsewhere.
3. Never invent the bracketed input yourself — always ask, or use what the
   user already supplied verbatim.

## 1. Landing page headline

> Most solo dev landing pages open with a feature list. Strangers decide in
> seconds and leave before scrolling.

```
Here is my product description: [paste]. Write 10 headlines under 10 words, each naming who it is for and the outcome. Ban the words powerful, seamless, effortless. Then pick the 3 a stranger understands with zero context.
```

Mistake avoided: describing what you built instead of what changes for the user.

## 2. App Store metadata

> Apple indexes title, subtitle and keyword field. Title is 30 characters,
> keywords are comma separated with no spaces.

```
My app does [paste]. Give 5 titles under 30 characters, 5 subtitles under 30 characters, and a keyword field. Split terms so they combine, like photo in the title and editor in the subtitle. No word repeated across fields.
```

Mistake avoided: burning the keyword field on words already in your title.

## 3. Behavioral onboarding email

> 61% of SaaS companies still run one welcome email and nothing else.

```
My product is [paste] and activation happens when a user [paste action]. Write 4 emails triggered by behavior, not by day count: after signup, after 48 hours without activation, right after activation, before trial end. Under 120 words, plain text, one link.
```

Mistake avoided: a time-based drip that ignores what the user actually did.

## 4. Launch day comment replies

> Product Hunt cut the weight of top hunters in 2025 and the featured rate
> dropped to around 10 percent.

```
I launch [paste] today. Write 8 reply templates: generic congrats, feature request, skeptical pricing question, competitor mention, someone asking for a mobile app I do not have. Under 40 words each, answer the real question first, no exclamation marks.
```

Mistake avoided: going quiet during the first four hours the algorithm is watching.

## 5. First user reply

> Median B2B trial-to-paid sits at 15 to 17 percent, top quartile products
> reach 25 to 30 percent.

```
Here is a message from one of my first users: [paste]. Reply in under 80 words, answer them, then ask one question that tells me why they signed up and what they tried first. No survey link, no feature promises.
```

Mistake avoided: thanking them politely and learning nothing about your activation gap.

## 6. Rewrite rough notes into an email

> For any email, not just marketing ones — follow-ups, difficult
> conversations, proposals, introductions, customer replies.

```
Rewrite my rough notes into an email.

Recipient: [WHO]
Relationship: [CLIENT / MANAGER / SUPPLIER]
Goal: [WHAT I WANT TO HAPPEN]
Tone: [WARM / DIRECT / DIPLOMATIC]
Constraints: [DEADLINE / BUDGET / POLICY]

ROUGH NOTES:
[PASTE]
```

Mistake avoided: asking AI to "make this professional" instead of giving it the context it actually needs.

## 7. Make an email sound human

> Run as a second pass on the output of prompt 6, or on any AI-drafted email.

```
Give me 3 versions: concise, warm and firm.

Keep only claims supported by my notes. Remove filler and corporate clichés.

Then highlight any sentence where the wording could be misunderstood or sounds more certain than the evidence allows.
```

Mistake avoided: sending the first draft instead of catching overconfident or ambiguous wording.

## 8. 30-day content calendar (two-step)

> From @earchoe's "AI Playbook" carousel. The point isn't "use AI" — it's
> removing the "what do I post today?" bottleneck by giving every post a job
> instead of generating 30 random captions.

Step 1 — build the strategy (5 content pillars):

```
My niche: [NICHE]
Audience: [AUDIENCE]
Offer: [OFFER]
Goal for the next 30 days: [GOAL]
Topics I already know well: [TOPICS]

Build 5 content pillars: Teach, Demonstrate, Prove, Opinion/Story, Convert. Explain the job of each pillar.
```

Step 2 — build the calendar from those pillars:

```
Create a 30-day calendar using those pillars. For every day include:
- Hook
- Format
- One useful takeaway
- CTA
- What I need to create it

Avoid repeating the same idea with different wording. Prioritise practical posts people would save or send to someone.
```

Run Step 1 first, let the user review the 5 pillars, then run Step 2 in the
same conversation so it can reference them. Attach any existing best-performing
posts to Step 1 if the user has them — it visibly improves the pillars.

Mistake avoided: treating a content calendar as 30 generated captions instead
of a repeatable system where every post has a job.

Monetization note (from the same source): this becomes a monthly
content-planning service for professionals/small businesses when you add a
review call and human editing on top — sell "a specific result for a specific
customer with human quality control," not "I know how to prompt AI."

## Applying any output (companion checklist)

Whichever prompt is used, run the result through this before it ships:

1. **Input** — give the real context, audience and constraints, not a vague ask.
2. **Prompt** — ask for a concrete output, not "help me with this."
3. **Improve** — ask AI to find assumptions, gaps and weak spots in its own draft.
4. **Verify** — check anything important before publishing, sending or selling.
5. **Apply** — the value is what you do with the output, not the output itself.
