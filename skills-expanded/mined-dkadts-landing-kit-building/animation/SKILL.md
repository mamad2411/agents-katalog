---
name: animation
description: Interactive motion brief. Six-section survey (page-load, scroll, text, blocks, micro-interactions, intensity) driven by the user's references from references/animation/ and references/motion/. Outputs brief/animation.md and appends motion tokens to DESIGN-LOCK §5. /build enforces the resulting animations as required elements.
---

# /animation

Motion is a first-class design system decision, not an afterthought. This skill runs a dedicated conversation about **what animates, how, and why**, grounded in the user's references. Output feeds `/tokens` and is enforced by `/build`.

## When to use

- After `/design-lock` (need ease + duration baseline from §5).
- Before `/blocks` if the interactive blocks depend on motion (e.g. a modal reveal style must match section reveals).
- Before `/tokens` — this skill adds motion tokens that `/tokens` writes to `tokens.css`.

## Requirements

- `DESIGN-LOCK.md` §5 (Motion) is `LOCKED` (has ease + duration).
- `brief/05-design.md` is filled (mood — affects motion intensity default).
- If `references/animation/` or `references/motion/` contain refs: `references/proposal.md` should mention motion patterns found there.

If no motion references exist, still run the skill — but every question defaults to `subtle` and explicitly asks the user to confirm rather than accept.

## Process

Six sections, in order. Each section: **show what refs suggest → offer 3-4 options → user picks → record.**

### Section 1. Page-load choreography

What appears first on initial page load, in what order, with what stagger?

Reference read: any first-frame screenshots or notes in `references/animation/*/notes.md`.

Options (present as A / B / C, first option always "match reference X" if a ref exists):
- **Instant** — everything visible at first paint, no entrance.
- **Hero-first** — hero content fades in over `--dur-slow`, everything else waits until fully loaded then reveals on scroll.
- **Staggered cascade** — top-to-bottom stagger with `--dur-base` per element, `stagger-base-ms` between.

Ask: `stagger-base-ms` value (30 / 60 / 120 ms). Default 60.

### Section 2. Scroll-driven

Behavior as user scrolls: reveal, parallax, pinning, sticky headers.

Reference read: `references/motion/` scroll captures, `references/animation/` scroll notes.

Ask 4 sub-questions:

1. **Reveal on scroll?** none / fade / fade+slide-up (16px) / fade+scale (0.98→1). Default: fade+slide-up if any ref shows reveal, else none.
2. **Parallax?** yes/no. Only allow yes if a ref explicitly shows parallax AND the mood is not "quiet luxury" (conflict from `/refs`). If enabled, ask depth: subtle (5%) / moderate (12%) / strong (25%).
3. **Sticky section headers?** yes/no. Default no (only enable if a ref shows it).
4. **Pinning (section stays while content animates over it)?** yes/no. Default no. If yes, warn: high complexity, mobile-safety flag.

### Section 3. Text animations

Reveal treatment for headlines, quotes, and body copy.

Reference read: `references/typography/` motion notes if any, `references/animation/` text captures.

Options:
- **None** — text appears with parent block, no separate animation.
- **Whole-block fade** — heading fades with its section.
- **Word-by-word stagger** — each word fades in with `stagger-base-ms/2` offset.
- **Line-by-line stagger** — each rendered line fades in (needs a split-lines JS helper).

Apply per element: `h1` / `h2` / `h3` / `p` / `blockquote` — user chooses which get animated.

**Constraint reminder:** text animations must respect the print-typography rules from `/typography`. Do not animate individual short words (`the`, `and`) separately — they animate with the word they are tied to via `&nbsp;`.

### Section 4. Block animations

Interactive states for cards, images, buttons.

Ask 5 sub-questions with defaults matching the mood:

1. **Card hover:** none / lift (translateY -4px) / scale (1.02) / border-glow / image-zoom. Duration: `--dur-fast`.
2. **Image hover:** none / zoom (scale 1.05) / caption-reveal / desaturate-to-color. Duration: `--dur-base`.
3. **Button press:** none / scale (0.98) / darken (background shift). Duration: `--dur-fast`.
4. **Button hover:** underline-grow / bg-fill / arrow-slide / none.
5. **Link hover:** underline / color-shift / both.

### Section 5. Micro-interactions

Form focus, error states, cursor.

Ask:

1. **Input focus:** border-color shift / border-thickness / label-float / underline-grow. Default: border-color shift.
2. **Input error:** border-red-flash (200ms) / shake (2 iterations, `--dur-fast`) / border-red-static.
3. **Form success:** button-morphs-into-checkmark / thank-you-slide-in / redirect-to-page.
4. **Custom cursor?** yes/no. Default no unless the mood is editorial+experimental. If yes, ask: dot / circle / cross / crosshair, and: mixed-blend-mode difference or plain.
5. **Cookie banner / toast entrance:** slide-up (bottom) / slide-down (top) / fade / none.

### Section 6. Motion intensity

Global multiplier that adjusts durations everywhere.

- **subtle** (multiplier 0.75) — high-end brand, quiet luxury moods.
- **balanced** (multiplier 1.0) — default.
- **lively** (multiplier 1.25) — consumer product, playful moods.
- **dramatic** (multiplier 1.5) — editorial, cinematic moods.

Default based on `brief/05-design.md` mood. Show the calculated final `--dur-base`, `--dur-fast`, `--dur-slow` values after the pick.

## Output

**Write `brief/animation.md`** with all decisions, structured for `/build` consumption:

```markdown
# Animation spec
STATUS: LOCKED
Generated: <date>

## 1. Page-load
choreography: <instant|hero-first|staggered-cascade>
stagger-base-ms: <value>

## 2. Scroll
reveal: <none|fade|fade-slide|fade-scale>
parallax: <off|subtle|moderate|strong>
sticky-headers: <yes|no>
pinning: <yes|no>

## 3. Text
h1: <animation>
h2: <animation>
p: <animation>
blockquote: <animation>

## 4. Blocks
card-hover: <value>
image-hover: <value>
button-press: <value>
button-hover: <value>
link-hover: <value>

## 5. Micro
input-focus: <value>
input-error: <value>
form-success: <value>
custom-cursor: <spec|off>
toast-entrance: <value>

## 6. Intensity
level: <subtle|balanced|lively|dramatic>
multiplier: <numeric>
final-dur-base-ms: <computed>
final-dur-fast-ms: <computed>
final-dur-slow-ms: <computed>
```

**Append to `DESIGN-LOCK.md` §5:** three new lines under Motion:

```
Scroll-behavior:      <reveal type>
Text-animation:       <text style>
Stagger-base-ms:      <value>
Motion-intensity:     <level (multiplier)>
```

Update `DESIGN-LOCK.md` §5 STATUS to LOCKED if not already, and log a decision entry in `DESIGN.md`.

**Append to `references/approved-manifest.md`** (see /refs for manifest format): every non-`none` / non-`off` decision becomes a required element:

```
[ ] animation:card-hover:lift
[ ] animation:text:h1:word-stagger
[ ] animation:scroll:fade-slide
```

`/build` will confirm each required animation is present in the generated CSS/JS.

## Reference priority

**Rule:** if the user has references, present "match reference X" as option A of every question. Only offer generic alternatives as B/C/D. The user's brand is the anchor.

If a reference conflicts with `/refs` proposal or DESIGN-LOCK values, flag it and ask the user which side wins.

## Rules of behavior

- **One question, one screen.** Do not batch six pickers.
- **Show trade-offs.** For each option, one sentence on cost (bundle size, mobile-safety, complexity).
- **Never accept "whatever".** Push for a specific choice — even if it's `none`.
- **Respect `/mobile` constraints.** Parallax and pinning have known mobile issues; surface those warnings when the user picks them.

## What NOT to do

- Do not invent motion tokens outside DESIGN-LOCK §5. Duration and ease come from there.
- Do not enable heavy scroll effects on mobile-first projects unless explicitly overridden.
- Do not skip sections silently. Every section produces a value.
- Do not touch the copy — animations are added around text, not replacing it.

## Next

- `/tokens` — will write motion tokens (`--stagger-base-ms`, `--motion-multiplier`, computed durations) into `tokens.css`.
- `/build` — reads `brief/animation.md` and generates matching CSS classes per section; checks each item in the approved-manifest.
- `/audit` — verifies every manifest item was applied.
