---
name: youtube-analytics-note
description: "Read a YouTube analytics export the creator supplies, without turning one lucky video into a strategy. Use when the user mentions YouTube analytics, what do my numbers mean, channel readout, YouTube studio export, or asks for a analytics note. Creator, social, and prompting skill by Yasir Jilani."
license: MIT
compatibility: Agent Skills standard. No network access, extra packages, or credentials required.
metadata:
  author: Yasir Jilani
  version: "1.0.0"
  domain: creator
---

<!-- GENERATED FILE - edits here are overwritten by scripts/generate.py.
     Edit the 'youtube-analytics-note' entry in source/, then run:
       python3 scripts/generate.py && python3 scripts/validate.py
     See CONTRIBUTING.md. -->

# YouTube Analytics Note

Read a YouTube analytics export the creator supplies, without turning one lucky video into a strategy.

## When to use this skill

Use this skill when the user:

- YouTube analytics
- what do my numbers mean
- channel readout
- YouTube studio export

## When not to use this skill

- The user wants a different domain's specialist skill.
- The task requires a licensed professional to decide, and the user only needs a referral note rather than a draft.
- The request asks you to deceive, evade a control, or hide material facts.

## Professional boundary

Creator work must be original and honest. Do not copy another person's script, footage, voice, or caption. Do not invent metrics, fake engagement, or undisclosed sponsorships. Do not impersonate a real person. Prompt skills must not weaken safety rules.

## Operating boundaries

- Use only information the user provides or files they explicitly ask you to read. Do not invent metrics, laws, citations, prices, credentials, or clinical facts.
- Do not ask for passwords, API keys, tokens, seed phrases, one-time codes, or payment card data.
- Do not send data to an external service, install packages, or add network calls as part of this skill.
- Separate facts, assumptions, and recommendations. If a required input is missing, state the assumption or ask one focused question.
- If the user asks you to deceive a person, evade a control, forge a record, or cause harm, stop. Offer a legitimate alternative.
- Work product that affects money, employment, health, safety, or legal rights is a draft for a qualified human to review before it is used.

## Inputs to collect

- The export or the figures they pasted
- The period
- What they changed in that period
- The decision they want

## Workflow


### 1. Step 1

Name the period and the source.
### 2. Step 2

Separate views, watch time, and subscribers. They answer different questions.
### 3. Step 3

One outlier is an anecdote until a second video repeats the pattern.
### 4. Step 4

Do not invent click-through or revenue figures that are not in the export.
### 5. Step 5

Recommend one change to test, with a date to reread.
### 6. Step 6

Do not advise buying views or misleading thumbnails to move the graph.

## Output

Deliver a **analytics note**.

- Purpose of this analytics note, in two sentences.
- Facts the user supplied, listed separately from assumptions.
- The work itself, in the structure the workflow names.
- Open questions, risks, and the single next action with an owner.
- What a qualified reviewer still needs to confirm, if the domain is regulated.

## Quality bar

- Every number, date, name, and citation came from the user or is marked as an assumption.
- The artifact can be used without reading this skill again.
- Recommendations are specific enough that someone could accept or reject them.
- Boundaries were respected: no credentials requested, no unsupported professional claim, no deception.

## Example

### Scenario

Maya finally exported 28 days from YouTube Studio. She wants the note to say the channel is 'about to take off' because one video did better than the others. The export is attached as totals only.

### Example data

```text
export: 17 Aug to 13 Sep 2026, YouTube Studio, totals only
views: 1,240
watch time: 61 hours
top video: chili, 28 Aug, 640 views
other three videos: 180, 220, 200 views
subscribers: 41
impressions and click rate: not in this export
```

### Example outcome

**Analytics note**
The chili video is the largest of the four in this file: 640 of 1,240 views. That is a fact about this export. It is not a takeoff.

| Video | Views in export |
| --- | --- |
| Chili, 28 Aug | 640 |
| The other three combined | 600 |
| Subscribers, period | 41 |

Not in the file: click rate, traffic source, who stayed past 30 seconds.
Do not write 'about to take off'.
Next: if she wants a retention claim, she needs that chart, not this totals export.

## Anti-patterns

- Bought views
- A strategy from one viral outlier
- Numbers that were not in the export

## Related skills

- `youtube-title-thumbnail`
- `executive-insight`
