---
name: community-ops-expression
description: Use when writing, rewriting, reviewing, or polishing community-operations language, including announcements, activity posts, reminders, result posts, daily/weekly reports, public articles, skill descriptions, resume bullets, interview stories, stakeholder updates, and natural-language edits. Trigger when the user asks for writing that sounds human, concrete, less templated, less AI-like, or free of repetitive contrast patterns.
---

# Community Ops Expression

## Overview

Use this skill to make community-ops writing sound like a real operator wrote it: clear, grounded, and easy to act on.

The default process is:

```text
audience -> facts -> action needed -> boundary -> concise wording -> self-check
```

## Project Inputs

Get the source facts, audience, publishing surface, desired reader action, language or voice constraints, and confirmation status of timing, rewards, benefits, metrics, permissions, or official claims from the user or an approved project source.

The skill supplies writing judgment and output patterns. It does not supply project facts, brand voice, activity rules, numbers, approvals, or publication status. Low-risk tone details may be inferred from the request; material facts and sensitive claims may not. Do not reuse example values or present placeholders as finished copy.

## First Questions To Resolve Silently

Before writing, infer:

- who will read it: users, creators, paid members, owners, team, recruiters, or public readers;
- what action the reader should take next;
- which facts are confirmed and which are only drafts or ideas;
- whether there is any reward, paid benefit, permission, privacy, safety, or official-claim boundary.

Ask the user only if missing context changes a risky public or official statement.

## Writing Rules

### Be Concrete

Name the surface, action, and next step:

- where it appears;
- who it is for;
- what the reader should do;
- what proof or response is needed;
- what happens next.

Avoid empty phrases such as "boost engagement", "build an ecosystem", or "increase stickiness" unless paired with a concrete mechanism and measurement.

### Keep Operator Voice

Use direct sentences. Prefer practical verbs:

- collect;
- check;
- route;
- remind;
- prepare publication draft;
- review;
- archive;
- follow up;
- compare;
- confirm.

For Chinese outputs, write naturally and avoid over-structured template tone.

For short outputs, preserve the conclusion, supporting evidence, material caveat, and next action. Remove introductions, repetition, generic reassurance, and optional background first. Define tone through observable writing choices instead of broad labels such as "friendly" or "professional".

### Reduce AI Flavor

Remove or limit:

- repeated binary contrasts such as `not X, but Y` and `not only X, but also Y`;
- long abstract openings;
- inflated adjectives;
- three-part slogans;
- vague "empower / enable / ecosystem" style claims;
- unsupported results.

Use contrast only when it clarifies a real boundary.

### Keep Claims Honest

Separate:

- completed public actions;
- drafts;
- analysis;
- assumptions;
- data gaps;
- next actions;
- owner decisions needed.

Do not write that something was sent, rewarded, approved, or completed if it is only prepared.

Keep public posts, DMs, mentions, rewards, discounts, winner lists, paid-benefit promises, role/channel/permission changes, webhooks, and official claims in draft status until the owner explicitly approves the exact action and target.

## Common Output Shapes

### Announcement Or Activity Copy

```text
Title:
Who it is for:
What to do:
How to submit / respond:
Deadline:
Reward or feedback:
Notes / boundary:
```

### Report Or Recap

```text
Today / This week:
Confirmed actions:
Signals found:
Risks or gaps:
Decisions needed:
Next actions:
```

### Skill Or Career Expression

```text
Capability:
What I actually did:
How I judged it:
What system or artifact came out:
What changed because of it:
Evidence or boundary:
```

## Self-Check

Before finalizing, check:

- can a normal reader understand the next action in one pass;
- are facts and drafts separated;
- does the text avoid repetitive contrast phrasing;
- is the tone practical instead of performative;
- are sensitive claims, rewards, permissions, or paid benefits approval-gated.
