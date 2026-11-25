---
name: make-playbook
description: An indie maker playbook inspired by Pieter Levels' (@levelsio) book "MAKE: The Indie Maker Blueprint" — idea validation, fast/DIY building, launching, organic growth, monetization, automation, and exits for bootstrapped apps. Use when the user is starting a new app idea, deciding what to build or build next, prepping a launch, stuck on growth or monetization, deciding whether/how to automate operations, or considering selling a product.
user-invocable: true
references: references/ethos.md, references/idea.md, references/build.md, references/launch.md, references/grow.md, references/monetize.md, references/automate.md, references/exit.md
templates: templates/make-tracker.md
---

# MAKE Playbook

A working reference system for bootstrapped app builders, inspired by Pieter Levels' *MAKE: The Indie Maker Blueprint* — meant to be consulted repeatedly across many apps and stages, not read once. This is an original set of checklists and diagnostics built around the book's core ideas, not a copy of the book itself. Read the full book at [readmake.com](https://readmake.com) for the deep-dive chapters, war stories, and numbers behind this framework.

## The 7-stage model

Idea → Build → Launch → Grow → Monetize → Automate → Exit

Every reference file corresponds to one stage. `references/ethos.md` is the constant background frame (bootstrapping-first stance, ethics constraints, realistic expectations about persistence) that applies no matter which stage you're in — read it once per session if it hasn't come up yet, and let its ethics constraints override any tactic from the stage-specific files that would violate them (fake engagement, dishonest growth hacks, user-hostile monetization).

## Workflow

1. **Identify the app and the stage.** If the user hasn't said which app or what stage it's at, ask — don't guess. If there's a `MAKE.md` tracker file in the current project (see below), read it first; it may already answer this.

2. **Load the relevant reference file(s).** Usually just the current stage's file, but load the adjacent one too when the question sits on a boundary (e.g. "should I charge yet" spans build/launch/monetize; "should I hire someone" spans build/automate).

3. **Apply the framework to the user's specific app — don't just restate it.** Each reference file ends with a short set of diagnostic questions for that stage; use them to get the specific facts you need (their niche size, their stack, their traffic, their pricing) rather than giving generic advice. Turn the relevant checklist into a concrete, numbered action list for *this* app, this week.

4. **Push toward shipping, not deliberating.** The strongest repeated theme across every stage is bias toward action over analysis — perfectionism and endless planning are the most common failure mode. If the user is stuck theorizing, hand them the smallest next concrete step, not more framework.

5. **Offer to create or update a per-app tracker.** For a new app, offer to copy `templates/make-tracker.md` into the project as `MAKE.md` and fill in what's known. For an app that already has a `MAKE.md`, update the relevant stage section as decisions get made in conversation, so the next invocation of this skill (on this app or a different one) has real state to pick up from.

6. **Flag ethics violations even when a tactic would "work."** Per `references/ethos.md`: no fake followers/upvotes/reviews, no dishonest growth-hacking, no selling user data, no dark-pattern monetization. If the user proposes something in this territory, say so plainly and suggest the honest alternative from the relevant reference file.

## Quick stage diagnostic

Use this if the user is unsure which stage they're actually in (common when an app has stalled):

| Symptom | Likely stage to revisit | Reference |
|---|---|---|
| "I don't know what to build" / idea feels unoriginal or too big | Idea | references/idea.md |
| Stuck deciding tools/stack, or outsourcing before shipping anything | Build | references/build.md |
| Built but nobody knows it exists / one soft launch, no follow-through | Launch | references/launch.md |
| Traffic exists but plateaued, or growth only exists while ads run | Grow | references/grow.md |
| Users but no revenue, or revenue but priced/modeled wrong | Monetize | references/monetize.md |
| Revenue but the founder is the bottleneck on every task | Automate | references/automate.md |
| Considering an acquisition offer or thinking about selling | Exit | references/exit.md |

## Principles worth keeping in working memory

- Size a niche before committing: does the price your audience will actually pay, times a realistic customer count, add up to a business worth building?
- Assume only a small fraction of free users convert to paid when sizing an audience against a revenue goal.
- A recurring subscription usually compounds to more revenue than an equivalent one-time price, even accounting for churn — model both before choosing.
- Match your launch-day infrastructure to the platform: a general startup community can send a real, sudden traffic spike.
- Only automate when the time saved clearly exceeds the time spent building the automation.
- Paid acquisition works best after there's already real organic pull — not as a substitute for it.

## Ending on an action, not just advice

Every reference file's diagnostic section is meant to end in a concrete, time-boxed next step (e.g. "spend the next 7 days logging 3 problem-ideas a day" for Idea, or "pick a launch date this week" for Launch) rather than just a list of considerations. Carry that pattern into every conversation this skill is used in.
