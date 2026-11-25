---
name: plan-content
description: |
  Use when user wants to think strategically about LinkedIn content
  rather than post-by-post: starting a LinkedIn presence from scratch,
  posting feels scattered or unfocused, or before committing to a
  consistent posting routine. Trigger phrases include "help me plan my
  LinkedIn content," "what should I be posting about regularly," "define
  my content pillars," "build a content calendar," "I post randomly and
  it's not working."
license: MIT
---

# Plan content

A LinkedIn presence with no plan tends to drift. The user posts whatever they thought of that day, the topics vary widely, the audience does not learn what to expect from them, and the algorithm does not learn what to surface them for. A content plan is not about scheduling tweets; it is about deciding what the user wants to be known for and then producing content that reinforces that consistently.

## Why this skill exists

LinkedIn's 2026 algorithm and audience both reward consistency in topic and angle. The algorithm builds an interest-graph profile of what the user posts about and surfaces it to people interested in those topics; the audience builds an expectation of what to come to the user for. Random posting forfeits both.

But "consistency" is also where most content strategy advice goes off the rails into rigid editorial calendars that the user abandons in two weeks. This skill is meant to produce something light enough to actually use: a few content pillars, a clear audience, and a sustainable cadence.

## When to use this skill

Trigger when:
- The user wants to think strategically about content rather than post-by-post
- The user is starting a LinkedIn presence (or restarting after dormancy)
- Their posting feels scattered, and engagement is inconsistent
- Before committing to a regular posting routine
- The user is positioning for a new audience and needs to align content

Do NOT trigger when:
- The user wants to write one specific post. Send to write-post (with find-ideas first if needed).
- The user wants to schedule and publish. This skill produces the plan; scheduling is a separate concern.

## What you need from the user

A short conversation, not a survey. Aim for 4-6 questions, batched at most two at a time.

1. **Who are you trying to reach on LinkedIn?** Not "professionals" or "decision-makers." Specific. ("Engineering managers at Series A-C startups, hiring backend engineers" / "Founders of bootstrapped SaaS companies under 50 employees" / "Engineering leaders in regulated industries.")

2. **What do you want to be known for?** One sentence. The thing the user wants to come to mind when their name does.

3. **What are you actually doing that is content-worthy?** Their day job, their side project, their reading and thinking, their experiments. Content pillars come from work, not from imagination.

4. **What are you willing to commit to?** Per week, how many pieces of content can they realistically produce. Honest numbers.

5. **What are the no-go zones?** Anything they cannot post about: NDAs, employer restrictions, topics they refuse to touch.

If voice-profile.md and rewrite-profile output exist, read them. Both inform the plan.

## How content pillars work

A pillar is a recurring topic-and-angle pair. Not just a topic.

Bad pillar: "Engineering management"
Good pillar: "What I am changing about how I run engineering at this company size"

Bad pillar: "Product strategy"
Good pillar: "The decisions I am making this quarter that I am unsure about"

The structure of a strong pillar:

```
[topic the user knows about] + [angle the user can own]
```

The angle is what differentiates the user from every other person posting about the topic. It should:

- Be specific enough that the user has unique material for it
- Be sustainable: the user can produce 2-3 posts a month on this for a year
- Be defensible: the user can argue with someone who disagrees

3-5 pillars is the sweet spot. Fewer than 3, and the audience gets bored. More than 5, and the user is not focused enough for the algorithm or the audience.

## How cadence works

Cadence depends on the user's actual capacity, not on aspirational numbers. The right cadence is the one the user will sustain.

Rough framework:

- **Minimum viable presence:** 1 post/week, with weekly engagement (5-10 substantive comments). Below this, the algorithm does not learn the user.
- **Growth mode:** 3-4 posts/week, plus daily commenting (5-10 comments/day). This is what creators on a serious push commit to.
- **Founder mode:** 1-2 posts/week, with focused commenting in the user's domain. Founders are not full-time creators; their audience values quality over volume.

The mix matters too. Within a week:
- 1 carousel (highest-effort, highest-reward format)
- 1-2 text posts (the workhorse format)
- 1 video if the user films (otherwise skip)
- 1 long-form article every 2-4 weeks
- Daily comments on others' posts (the multiplier)

But none of this is prescriptive. The plan should match what the user will actually do.

## What to write into the content plan

Save to `content-plan.md` in the workspace.

```markdown
# Content plan for [user's name or role]

Generated [date]. Revisit every 3 months.

## Audience
[2-3 sentences on the specific audience]

## What I want to be known for
[one sentence]

## Content pillars

### Pillar 1: [name]
Topic: [what the topic is]
Angle: [the unique angle the user owns]
Why this works for me: [the user's specific access to material here]
Example post ideas: [3 concrete ideas, not topics]

### Pillar 2: [name]
[same structure]

### Pillar 3: [name]
[same structure]

[3-5 pillars total]

## Cadence
- [N] posts per week, in this mix: [breakdown by format]
- Commenting: [N] comments per day/week on others' posts
- Long-form: [cadence for articles or newsletter]

## What I will NOT post about
[the no-go zones]

## Review checkpoints
- After 4 weeks: review which pillars are getting traction
- After 12 weeks: re-run plan-content if needed
```

## How downstream skills use this file

- find-ideas can read the pillars to suggest ideas in the user's defined territory
- write-post can check whether a post fits an established pillar or starts a new one
- analyze-performance can group posts by pillar to see what is working
- review-post can ask "did this post serve a pillar, and how did it perform?"

## A note on rigidity

The plan is a guide, not a contract. If the user writes a post that does not fit a pillar, that is fine; the question is whether it is the start of a new pillar or a one-off. After 4-8 weeks of posting, the actual pattern of what the user produces should inform whether to revise the pillars.

Some users want a more rigid calendar (Monday: pillar 1, Wednesday: pillar 2, Friday: carousel). Others want only the pillars and resist the calendar. Match the user.

## What this skill does not do

- Produce a rigid editorial calendar with specific dates. If the user wants scheduling support, that is a different concern (and an external tool like Buffer or Postiv handles it).
- Define pillars from no input. The pillars come from what the user actually knows and is doing. If the user has no material to draw from, the answer is to keep working and revisit content planning later.
- Promise specific follower growth, view counts, or engagement metrics from following the plan.
- Tell the user to "post 5x daily" or any other generic frequency advice. Cadence comes from the user's capacity.
- Force the user into one of 5 archetypal content-creator personas. The plan should fit the specific user, not a category.
