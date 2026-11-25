---
name: camp-profile
description: Create or update a reusable profile of a summer camp (name, type, location and jurisdiction, programs, ages, voice, accreditation, and positioning) saved to .agents/camp-profile.md so every other camp skill can use it instead of re-asking. Use when setting up the camp skills for the first time, when another skill needs camp context and no profile exists, or when the camp's details change.
version: 1.0.0
---

# camp-profile

Capture a summer camp's durable facts once, so every other camp skill builds on them instead of asking the director to re-explain their camp each time. Think of it as the camp's shared brief.

This skill is written for you, the agent. Make it feel light. The fastest path is almost always the camp's own website: ask for the URL first, read what you can, draft the profile from it, and have the director confirm and fill the gaps. Confirming a draft beats answering a cold list of questions. The goal is a useful profile in a few minutes, not an interrogation.

## When to run this

- A director is setting up the camp skills for the first time.
- Another skill needed camp context and found no profile.
- The camp's details have changed and the profile needs updating.

## First, check for an existing profile

Look for `.agents/camp-profile.md` (or `.claude/camp-profile.md`). If one exists, read it and offer to update or extend it rather than starting over. Confirm what has changed and edit in place.

## Start from the website

Ask for the camp's website URL early, plus any brochure or one-pager they have. If you can read it, do: pull the camp name, type, location and likely jurisdiction, programs and ages, accreditation, tone of voice, and how the camp positions itself, and draft as much of the profile as you can. Then walk the director through the draft to confirm and correct, asking only for what the site does not reveal. Flag anything you inferred so they can check it, and never present a guess as fact.

If there is no website, or you cannot read it, ask for the facts directly, grouped as below.

## Draw on camp-overview

Use the camp-overview skill so the questions are camp-aware. Day and overnight camps differ, specialty and traditional camps differ, and the profile should reflect that. Do not ask about things the earlier answers make irrelevant (for example, do not ask a day camp about cabin assignments).

## What to capture

Whether you draft these from the website or ask directly, the profile should capture the following. Get the core facts first, then offer to go deeper. Mark anything you inferred from the site so the director can confirm it, and leave unknowns blank to fill later.

**Identity (core)**
- Camp name, and any shorthand families use
- A one-line description of the camp
- Brand voice: how the camp should sound (for example warm, adventurous, traditional), and any words or claims to always use or always avoid

**Type and focus (core)**
- Day, overnight, or both
- Traditional or general, or specialty (and the focus, such as sports, arts, STEM, riding, or faith)
- Coed or single-gender

**Location and reach (core)**
- Where the camp is
- The towns, regions, or distance families travel from, and whether it is mostly local or a destination camp
- The state or province, which sets the compliance jurisdiction for licensing, ratios, and data rules

**Programs and ages (core)**
- The programs offered, with the age range for each
- Session structure: typical lengths and the rough shape of the summer

**Capacity**
- Campers per session, and the overall size of the operation

**Accreditation and safety**
- Accreditation (ACA, OCA, another provincial body, or none)
- Certifications and supervision ratios worth surfacing to families

**Families and positioning**
- Who the families are, and what they weigh most when choosing a camp
- What makes this camp different from the one down the road
- How much of enrollment is returning families, if known

**Practical**
- Website URL and social handles
- Google Business Profile status (claimed and verified?)
- Camp management software, if any
- Pricing shape: deposits, installments, early-bird rates, camperships

## Write the profile

Write a clean, readable `.agents/camp-profile.md` using the section headings above, so other skills can scan it quickly. Keep it factual and concise. Tell the director where the file is and that they can edit it directly at any time.

Keep durable facts only. Anything seasonal or task-specific (this year's dates, current openings, this season's priorities) stays out, because skills ask for those when they need them.

## Keep it accurate and theirs

This file lives in the camp's own workspace and belongs to them. Do not invent facts to fill gaps; leave unknowns blank and say what is missing. Like every skill here, it is a starting point the camp adapts.
