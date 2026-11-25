---
name: design-plan
description: Generate a DESIGN-PLAN.md for a new brand or branding project — the strategic intent layer (visual direction, voice, audience, hard NOs, mood references) that PRECEDES design tokens. Use BEFORE design-system. Triggers include "design plan for [brand]", "brand brief", "let's plan a brand", "create a DESIGN-PLAN.md", "/design-plan".
---

# Skill: design-plan

Produces `./design/<brand-slug>/DESIGN-PLAN.md` — a brand-agnostic strategic plan that the `design-system` skill consumes to derive concrete tokens. Think of it as the design equivalent of a PRD: it captures intent, constraints, and direction without committing to specific hex codes or fonts yet.

## When to use

- Starting a new branding project (Shane's own brand, a client brand, or an experiment)
- Before `/design-system` — the system skill needs strategic input to make non-arbitrary token decisions
- When revisiting a brand and the existing plan no longer matches the work

Do NOT use this for one-off artifacts where the brand is already defined and a `DESIGN.md` exists. Skip straight to a platform skill.

## Inputs

A brand slug (kebab-case, e.g. `shane-personal`, `acme-launch`) and answers to 3 short questions (default) or 8 deeper questions (with `--deep` flag).

## Output

`./design/<brand-slug>/DESIGN-PLAN.md` — created in the current working directory. The skill creates the parent dirs if needed. Never write to any other location.

## Steps

### 1. Determine brand slug

If the user said "design plan for X", derive the slug from X (kebab-case, lowercase, no special chars). If they didn't, ask:

> What brand slug should I use? (kebab-case, e.g. `shane-personal`, `acme-launch`)

### 2. Run the interview

**Default (3 questions, ~2 min):**

```
1. One sentence: who is this brand for, and what do they do? (e.g. "tooling for senior engineers building AI products")

2. Pick a visual direction + give me 3 voice/tone adjectives:
   - editorial (type-led, print-inspired, restrained)
   - technical (dev aesthetic, mono-led, dense)
   - bold (high-contrast, expressive, attention-grabbing)
   - minimal (whitespace-led, calm, neutral)
   - mixed (specify which two and how)
   Voice adjectives: e.g. "direct, dry, confident" or "warm, curious, generous"

3. Hard NOs and mood references:
   - Aesthetic constraints to never violate (e.g. "no emojis ever", "no gradients", "no stock photography")
   - 2–3 reference brands or sites whose vibe you want to channel (URLs or names)
```

The five directions above (editorial / technical / bold / minimal / mixed) are the common shorthands. The full named-aesthetic roster — Swiss, brutalist, warm minimal, bold geometric, code/terminal, solarpunk, distinctive display, archival, and more, each defined in concrete type/color/radius/density/layout terms — lives in `../../design-variation-sop.md`. If the user's answer points at one of those, name it explicitly in the plan's Visual Direction section. **Do not let the plan default to "minimal" / "clean" / "modern"** — that is the absence of a direction, not a direction (variation-sop Rule 1). Pick deliberately, biased away from whatever recent brands chose.

**Deep dive (8 questions, ~10 min) — only if user passes `--deep` or asks for it:**

Add to the above:
```
4. Competitors / peers — name 2–3 brands in the same space you want to feel DIFFERENT from. Why?

5. Color associations — any colors that mean something for the brand (positive or banned)? E.g. "must include warm cream, never use medical blue."

6. Type personality — preference for serif (literary, established), sans (modern, neutral), mono (technical, precise), or mixed? Any specific font families you want considered?

7. Density preference — spacious (lots of whitespace, breathing room) or compact (information-dense, efficient)? Affects line-height and spacing scale.

8. Platform constraints — anything platform-specific to honor? E.g. "LinkedIn artifacts must always include the company mark" or "YouTube thumbnails must work for a developer audience that hates clickbait"
```

Ask all questions in a single message. Do not ask one at a time.

### 3. Generate the plan

Write to `./design/<brand-slug>/DESIGN-PLAN.md` using this exact structure:

```markdown
# DESIGN-PLAN: <Brand Name>

**Slug:** `<brand-slug>`
**Date:** YYYY-MM-DD
**Status:** Draft

## Audience

<1–2 sentences from Q1. Be specific about who, not generic "developers" — e.g. "senior engineers (10+ yrs) at AI infrastructure companies who write production code daily and choose their own tools.">

## Visual Direction

**Primary direction:** <editorial | technical | bold | minimal | mixed>

<2–3 sentences interpreting what this means in execution terms. E.g. for "editorial": "Typography carries the visual weight. Display serif for headlines, generous letter-spacing on small uppercase labels, hairline rules over heavy borders. Whitespace is a design element, not leftover space.">

## Voice & Tone

**Adjectives:** <adj1>, <adj2>, <adj3>

**In practice:**
- <One concrete writing example showing the voice in action>
- <One example of what the voice is NOT>

## Brand Archetype (optional)

<If clear from interview, name one: Sage, Creator, Maverick, Magician, Hero, Explorer, Caregiver, Lover, Jester, Everyman, Innocent, Ruler. If unclear, omit this section entirely.>

## Mood References

<List the references from Q3, with one-line interpretation each. E.g.>
- **Are.na** — quiet authority, no ornamentation, content-first
- **Linear changelog** — technical precision with editorial restraint
- **Fraunces specimen** — display type as the entire visual event

## Hard NOs

<Bulleted list of aesthetic constraints from Q3. Be ruthless — these become enforcement rules in every downstream skill.>

- No purple-to-cyan or blue-to-pink gradients
- No floating orbs, glowing nodes, brain meshes, robot iconography
- No center-aligned hero with template "[Big Word] [Subheading] [Button]"
- <user-supplied NOs>

## Platform Priorities

**Phase 1:** <which 5 platforms this brand will use first — from LinkedIn, X, YouTube thumbnails, stream overlays, Instagram, etc.>

## Token Direction Hints (for design-system to interpret)

**Color stance:** <e.g. "warm neutrals + single accent" | "high-contrast monochrome with one signal color" | "tonal gradient on a single hue">

**Type stance:** <e.g. "display serif + sans body + mono labels" | "single sans family across 3 weights" | "mono-dominant with serif accents">

**Density:** <spacious | compact | balanced>

**Surface:** <flat | layered | textured>

---

## Handoff

Run: `/design-system <brand-slug>` — the design-system skill will read this plan and generate concrete `DESIGN.md` tokens, `tokens.css`, and `showcase.html`.
```

### 4. Confirm and hand off

After writing the file, tell the user:

> Plan saved to `./design/<brand-slug>/DESIGN-PLAN.md`.
>
> Next: run `/design-system <brand-slug>` to derive concrete tokens and a visual showcase. Or revise the plan first — anything you want me to push back on or expand?

## Rules

- The plan is **strategic only** — no hex codes, no font sizes, no spacing values. Those live in `DESIGN.md`.
- Never hardcode Shane's personal brand into this skill. The plan is brand-agnostic input.
- 1 page max. If the file exceeds ~80 lines, cut.
- If the user can't answer a question, write `TBD — needs decision before tokens` rather than guessing.
- If `./design/<brand-slug>/DESIGN-PLAN.md` already exists, ask before overwriting.
- **Universal anti-patterns** (purple-cyan gradients, indigo/violet default, orbs, italics-emphasis, Inter/Roboto/system primary, etc.) live in `../../design-anti-patterns.md` and apply to every brand. The positive craft floor (`../../design-principles.md`) and the direction roster + offer-3 procedure (`../../design-variation-sop.md`) are the other two shared canonical references. The Hard NOs section of the plan is for brand-SPECIFIC bans on top of those universals — don't restate the universals here.
