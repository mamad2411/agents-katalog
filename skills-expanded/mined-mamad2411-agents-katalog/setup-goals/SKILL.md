---
name: setup-goals
description: Identity-aware goals setup — reads professional-identity.md, derives what it can, then asks only the fields it can't infer (comp, stage, geography, phase, thesis) and writes data/goals.md
argument-hint: (no arguments needed)
user-invocable: true
allowed-tools: Read(*), Write(data/goals.md)
---

# Setup Goals — Identity-Aware Goals File Builder

Bootstrap `data/goals.md` from your professional identity. Reads `data/professional-identity.md` first, derives industries, non-negotiables, and priority stack from it, then asks only for the 5–6 fields that identity doesn't cover.

## Instructions

### Step 1: Check Prerequisites

1. Check that `data/professional-identity.md` exists and contains real content (not just a stub).
   - If missing: "⚠️ `data/professional-identity.md` not found. Run `/extract-identity` first to build your professional identity file — it's the foundation this skill builds on."
   - If it exists but is mostly empty/placeholder: proceed with Step 2 anyway, but note you'll need to ask more questions.

2. Read `data/professional-identity.md` in full.

### Step 2: Derive What You Can

Scan the identity file for these sections and extract:

- **Target industries / sectors** — look for Career Direction, Target Industries, or similar headings
- **Hard filters / non-negotiables** — look for "Not pursuing", "Hard filters", "Non-negotiables", or a "Won't do" list
- **Priority stack** — look for Values Hierarchy, Priority Stack, or What Matters Most
- **Work style** — look for Work Style, Environment preferences, or culture fit signals
- **Role types / titles** — look for Target Roles, Career Direction, or title aspirations

### Step 3: Show Derived Snapshot

Display a confirmation block so the candidate can see what you found before asking questions:

```
From your professional-identity.md, I can see:

**Target industries:** [list — or "not specified"]
**Role types:** [list — or "not specified"]
**Priority stack:** [list — or "not specified"]
**Non-negotiables / won't-do:** [list — or "not specified"]
**Work style signals:** [list — or "not specified"]

I'll carry these into goals.md without asking you to repeat them.
Here's what I still need:
```

If any section above shows "not specified", note that the candidate may want to run `/extract-identity` to fill those gaps, but don't block — continue with the questions.

### Step 4: Ask for Missing Fields

Ask for only these fields — present them as a numbered list so the candidate can answer all at once:

```
1. **Search thesis** — one sentence: role + company type + your narrative hook.
   [If identity gave you enough to suggest one, offer a draft: "Suggested: '[draft thesis]' — edit or replace entirely."]

2. **Role types** (ranked 1–3, most to least preferred)
   [Skip this question if you already extracted clear role types from identity with enough specificity for a ranked list.]

3. **Company stage / size preference** — e.g., Series A–C, growth-stage, public, any
   [Identity rarely specifies this — almost always ask.]

4. **Geographic constraint** — SF in-office only / Bay Area / remote-first / open to relocate where?
   [Ask even if identity mentions SF — identity might say "prefer SF" without specifying flexibility.]

5. **Comp floor** — minimum base you'd accept, and total comp target (base + bonus + equity value)
   [Identity never has this — always ask.]

6. **Current phase + target offer date** — where are you in the search right now, and by when do you need an offer?
   (Exploring / Active / Interviewing / Negotiating + target date)
```

Wait for responses before proceeding.

### Step 5: Write data/goals.md

Using the template from `framework/templates/goals.md` as the structure, write `data/goals.md` with:

- **Search Thesis** — from the candidate's answer (or your suggested draft if accepted)
- **Role types** — from identity (derived) or candidate's answer
- **Company stage / size** — from candidate's answer
- **Geography** — from candidate's answer
- **Comp range** — from candidate's answer
- **Current Phase** — mark the correct checkbox; fill Phase notes with target date
- **This Week's Focus** — leave as TODO (populated by `/weekly-review`)
- **Week of** — leave as TODO
- **Success Metrics** — leave targets as TODO (candidate fills these in)
- **Notes** — add a line: `_Industries, priority stack, non-negotiables, and work style preferences are in data/professional-identity.md._`

For any field the candidate didn't answer, leave as TODO rather than guessing.

### Step 6: Confirm and Suggest Next Step

```
✅ data/goals.md written.

Profile guard check:
- data/profile.md: [exists ✅ / not found ⚠️]
- data/goals.md: ✅ just written

[If both exist:]
Profile guard will now pass — all generative skills are unblocked.

Suggested next step:
- Run `/standup` for a morning briefing now that goals are set
- Or `/weekly-review` to set This Week's Focus
- Fill in the Success Metrics targets in data/goals.md when you have a sense of your weekly pace
```

If `data/profile.md` is still missing, note: "⚠️ `data/profile.md` is still missing — run `/import-cv` to complete setup."

## Edge Cases

- **Identity file has good career direction but vague role titles:** Suggest 2–3 title options based on the direction and ask the candidate to rank them.
- **Candidate provides a thesis that's vague:** Accept it but add a gentle note: "Your thesis works — you may want to tighten it once you've applied to a few roles and know what's resonating."
- **data/goals.md already exists with real content:** Before writing, warn: "⚠️ `data/goals.md` already has content. Continuing will overwrite it. Proceed? (y/n)" — wait for confirmation.
- **No professional-identity.md:** Fall back to asking all fields including industries, priority stack, and non-negotiables. Note that running `/extract-identity` would make future updates much smoother.
