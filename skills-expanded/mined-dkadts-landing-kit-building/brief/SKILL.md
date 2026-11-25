---
name: brief
description: Interactive survey across the 9 brief files. Starts with desktop-first vs mobile-first (the most important question), then niche, then the rest. Fills brief/*.md instead of the user.
---

# /brief

Guides the user through the questionnaire. Fills `brief/00-priority.md` → `brief/08-content-pipeline.md`.

## When to use

- Start of a new project (before any `/build`).
- User prefers a dialog over filling .md files by hand.
- Revising an existing brief.

## Process

**Step 1. Read existing files**
Read every `brief/*.md`. Determine which fields are filled, which are `TBD`.

**Step 2. Ask the first — most important — question**

```
Desktop-first or mobile-first?

This decides:
- Assembly order (down or up)
- Block composition
- Reference viewport (1920px or 390px)

Help to choose: <brief decision table from 00-priority.md>
```

Wait for an explicit answer. Save to `brief/00-priority.md`.

**Step 3. Walk files 01-08 in order**

For each file:
- List `TBD` fields.
- Ask one question at a time (do not batch 10 questions at once — user tires).
- Use checklists where preset options exist.
- Save the answer (Edit tool).

**Step 4. Special attention — niche discovery**

`brief/01-business.md` — niche section — critical for `/copy-analyze`.
Do not accept "beauty" — narrow it to "men's Botox for CEOs 35-50 in Barcelona".
Do not accept "clients" — narrow maturity (cold/warm/hot).

**Step 5. After 07-interactive**

If the user checked interactive blocks — offer to run `/blocks` immediately to configure.

**Step 6. Final summary**

Show brief completeness: how many fields LOCKED, how many TBD.
If TBD remain — what to ask the client.

## Rules of behavior

- **One field — one question.** Do not batch.
- **Do not guess for the user.** If unclear — clarify.
- **Use examples.** "e.g. form submission → manager calls within 2 hours".
- **Save as you go.** Not at the end. Otherwise if the session drops — everything's lost.
- **Respect status.** If a field is already filled — do not re-ask, only clarify if needed.

## What NOT to do

- Do not start `/design-lock` until `01-business` + `02-audience` + `05-design` are filled.
- Do not suggest skipping `00-priority` — it's critical.
- Do not fill `brief/copy-analysis.md` — that's `/copy-analyze`.
- Do not touch `brief/blocks/*.md` — that's `/blocks`.

## Next

Once done:
- Suggest `/inbox` (if the client already has materials) or wait for materials.
- Or `/refs` (if references are already in `references/`).
