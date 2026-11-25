---
name: postkit-review
description: Critique a draft post against the brand profile (memory/brand_*.md) and theme.css across three lenses — strategy (hook, angle, value arc), copy (CTA, word economy, tone), and design (layout, density, rhythm, typography). Returns HIGH/MEDIUM/LOW findings. Use when the user asks to review, critique, polish, or improve a draft before rendering.
---

# /postkit-review — three-lens critique

You review a post draft (one or more slides) against the user's brand and
design system, surfacing the changes that will materially improve performance.

Do not rewrite the post yourself. Your job is to **identify issues** and
**propose specific fixes** so the user (or the next run of `/postkit-new`) can
apply them.

## Inputs

1. The target post folder (default: most recently modified `posts/<slug>/`).
   If ambiguous, ask.
2. **The brand profile in `memory/`** — read every `memory/brand_*.md` file
   at the project root: `brand_identity.md`, `brand_audience.md`,
   `brand_goals.md`, `brand_voice.md`, `brand_visual.md`, `brand_hooks.md`.
   If any are missing, stop and send the user to `/postkit-setup`. Don't
   read brand state from Claude Code internal memory.
3. `theme.css` at the project root — palette, tokens, component classes.
4. Any review logs left by a previous `/postkit-review` run in
   `posts/<slug>/review.md` — don't repeat findings the user already addressed.

Read all slide files, `post.json`, and **every `caption*.md` file** in the
post folder before forming opinions. Each caption file targets a specific
platform (filename pattern `caption-<platform>.md`); critique each one
against that platform's length and formatting conventions, not just the
brand voice. Flag a caption that ignores its platform's norms (e.g. a
LinkedIn-length caption saved as `caption-x.md`, or hashtag spam on
LinkedIn) as HIGH.

**Alt text check.** Any post with slides must have an `## Alt text` section
in each caption file with one bullet per slide. Flag missing alt text as
HIGH (accessibility regression). Also flag alt copy that just repeats the
caption, exceeds ~125 chars, uses emojis/hashtags, or describes the
strategic purpose instead of what's visually on the slide — these as
MEDIUM.

## Three lenses, one pass

Do all three in the same response. Don't spawn sub-agents.

### 1. Strategy

- **Hook strength.** Does slide 1 stop a thumb in <1s? Is it specific, or
  generic enough to belong to any account?
- **Angle.** Is this the most compelling framing (myth-bust vs. listicle vs.
  story vs. hot take)?
- **Format fit.** Right slide count? Too much padding, or too rushed?
- **Value arc.** Does each slide build on the previous? Any filler?
- **Audience fit.** Will the segment in `brand_audience.md` actually care?
  Right level?
- **Goal alignment.** Does the CTA match the primary outcome in
  `brand_goals.md`?

### 2. Copy

- **CTA strength.** Specific, urgent, actionable? Does the reader know *why* to
  act?
- **Word economy.** Any sentence that can shrink without losing meaning?
- **Slide transitions.** Do slide endings push the reader to swipe?
- **Emotional triggers.** Does the copy hit a real feeling, or play it safe?
- **Tone consistency.** Does every slide match the voice in `brand_voice.md`? Flag
  anything that drifts corporate / cutesy / jargon-heavy.
- **AI-voice tells.** Flag every instance of the patterns below as HIGH
  (they break the illusion that a human wrote this):
  - Em dashes (`—`) used as a pause or aside. Propose a period, comma, or
    line break.
  - "Not X, it's Y" / "X, not Y" contrast rhetoric. Propose a direct
    positive claim.
  - Filler openers: "Here's the thing,", "Let me be clear,", "The truth
    is,", "Look,", "At the end of the day,".
  - Marketing superlatives: "game-changer", "seamless", "elegant",
    "beautifully", "transformative".
  - Rhythmic tricolons ("bigger, better, faster") and parallel 3-item
    structures when the user's brand voice doesn't call for them.
  - Rhetorical-question hooks unless `brand_voice.md` explicitly allows them.

### 3. Design

- **Layout balance.** Content distributed well? Breathing room?
- **Whitespace.** Padding/margin generous? Nothing crammed against edges?
- **Visual rhythm.** Do slides alternate colors/layouts enough to avoid
  monotony?
- **Typography hierarchy.** Headings vs. body vs. accents clearly differentiated?
- **Text density.** Any slide that reads as a wall of text for a 2-second scan?
- **Color usage.** Palette followed? Colors serve hierarchy/emphasis, not noise?
- **Brand consistency.** Radii, spacing, component classes match `theme.css`?

> You're reading HTML/CSS source, not rendered PNGs. Reason about visual
> weight from markup structure, class names, and inline styles. If you genuinely
> can't tell without seeing pixels, ask the user to run `/postkit-render` first
> and describe what they see, or check the `posts/<slug>/output/` folder if
> PNGs already exist there.

## Output

Return one structured report:

```markdown
## /postkit-review — posts/<slug>

### HIGH IMPACT (fix these)
- **[Strategy | Copy | Design] · slide-N:** What's wrong → Specific fix
  (include the exact replacement text or CSS change).

### MEDIUM (consider)
- [Observation]

### LOW (logged)
- [Observation]

### Verdict
[REVISE | APPROVED]  — one-line summary.
```

APPROVED = zero HIGH items. REVISE otherwise.

After the report, offer to save it to `posts/<slug>/review.md` so the next
review skips addressed items.

## Important

- Don't touch slide HTML. Suggest, don't edit.
- Don't re-critique decisions the user explicitly confirmed earlier in the
  conversation.
- Skip `/postkit-render` unless the user asks — this is a source-level review.