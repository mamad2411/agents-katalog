---
name: refs
description: Parses references from references/ across all 9 design aspects. Finds conflicts (e.g. quiet-luxury mood vs bombastic motion). Produces a coherent proposal for DESIGN-LOCK.md AND an approved-manifest.md that /build and /audit enforce as required elements.
---

# /refs

Reads every folder under `references/*/`, extracts patterns per aspect, surfaces conflicts, and produces two artifacts:
- `references/proposal.md` — recommendations for `/design-lock`.
- `references/approved-manifest.md` — a flat list of required elements the user approved (see Step 5b).

## When to use

- After `brief/05-design.md` is filled.
- The user placed references in `references/`.
- Before `/design-lock`.

## Requirements

- At least 1 reference exists somewhere under `references/*/`.
- `brief/05-design.md` is filled (mood, associations).

If no references at all — offer to base the design on `brief/05-design.md` and skip this skill.

## Process

**Step 1. Walk every aspect folder.**

For each folder in `references/`:
- `animation/`, `structure/`, `typography/`, `color/`, `layout/`, `motion/`, `micro-interactions/`, `mood/`, `full-sites/`
- Read every subfolder: `source.txt`, `notes.md`, media files.
- If the user provided a URL but no screenshot, WebFetch the visual/structure (do not pull code).

**Step 2. Extract the common pattern per aspect.**

For each aspect, articulate what's shared across references:

```
## animation
From 3 references:
- Common pattern: subtle scale-up on hover (1.02×), fade + slight lift on scroll
- Common ease: cubic-bezier(0.22, 1, 0.36, 1)
- Common duration: ~300ms
- Outlier: <linear-refs uses longer 500ms>

## typography
- Serif heading + sans body (2 of 3)
- Ratio ~1.333 (Perfect Fourth)
- Weights: 400 body, 700 headings — only two
- Heading line-height: 1.1 (tight, editorial)
```

**Step 3. Detect conflicts.**

Run through the pairs:
- **Mood vs Motion:** "quiet luxury" + "bombastic scroll animations" → conflict.
- **Color vs Mood:** "warm beige" + "neon accent" → conflict (unless neon is a declared subversion).
- **Density vs Typography:** "compact" + "editorial serif big display" → conflict.
- **Density vs Structure:** "editorial density" + "5+ sections" → conflict (editorial = fewer sections, more air).

Each conflict is a question to the user:

```
⚠️ Conflict: mood/aesop = "quiet luxury" vs motion/apple-scroll = "bombastic sticky"
Which wins?
- A. Mood wins → pick a more subtle motion (e.g. Vercel scroll fade)
- B. Motion wins → revisit mood, pick something bolder
- C. Compromise: quiet mood + one bombastic hero scene
```

**Step 4. Build the proposal for DESIGN-LOCK.**

Assemble a single document — what will be proposed for `DESIGN-LOCK.md`. Every point (spacing, type, color, radius, motion, density, photography, sections) gets a proposal with a reason:

```markdown
## Proposal for DESIGN-LOCK

### 1. Spacing
Base: 8px
Rhythm: Fibonacci 8/16/24/40/64
Section padding: 96px top, 96px bottom
Page margin (left/right): 5% viewport (min 24px, max 120px)
Why: editorial density from mood + typical rhythm for serif-driven landings

### 2. Type
Ratio: 1.333 (Perfect Fourth)
Body: 17px, line-height 1.6
H1: 56px desktop / 32px mobile
Weights: 400 + 700 (two)
Font: Editorial New heading + Inter body
Why: all 3 typography refs use this ratio

### 3. Color
Mode: mono + accent
Background: #F5F1EA (warm beige)
Foreground: #1A1A1A (off-black)
Accent: #C69C6D (rare — only on CTA and underline)
Why: from color/aesop-mono-warm, matches quiet-luxury mood

...
```

**Step 5. Save the proposal.**

- Save `references/proposal.md` (temporary, feeds `/design-lock`).
- Show the user a summary.
- Ask: approved? Anything to change before `/design-lock`?

**Step 5b. Approved manifest — required elements.**

After proposal approval, extract every concrete element that the user explicitly approved and add it to `references/approved-manifest.md`. This file is the **contract** — `/build` refuses to save a section that omits a manifest item relevant to it, and `/audit` fails the whole build if any manifest item is unmet.

**Manifest format:**

```markdown
# Approved manifest

Every item here MUST appear in the final build. If an item is impossible for the current layout, it must be explicitly removed from this file by the user — not silently dropped.

## From /refs

### Motifs
[ ] motif: horizontal thin rule between sections    ← ref: mood/aesop
[ ] motif: serif accent on numbers                   ← ref: typography/nyt

### Patterns
[ ] pattern: 2-column asymmetric grid (60/40)        ← ref: layout/vercel-blog
[ ] pattern: sticky brand mark top-left              ← ref: full-sites/pentagram

### Elements
[ ] element: quote block with vertical rule          ← ref: typography/editorial
[ ] element: image caption overlay bottom-right      ← ref: mood/aesop

### Color usage
[ ] color: accent only on CTAs and inline underlines ← ref: color/aesop-mono
```

**What counts as a manifest item:**
- Visual motifs the user pointed to explicitly ("this thin line between sections is what I want").
- Structural patterns approved during conflict resolution.
- Approved elements from `/design-lock` §7 imagery discussion (added later by `/design-lock`).
- Approved section types from `/design-lock` §8 (added later by `/design-lock`).
- Approved animation behaviors from `/animation` (added by `/animation`).
- Approved icons from `/icons` (added by `/icons`).

**Every item includes the reference source** so the audit report can cite provenance when a check fails.

**Ask the user to review the manifest one item at a time.** Any item they cannot commit to → remove now, not later. Silently dropping approved elements is exactly the failure mode this file exists to prevent.

Save `references/approved-manifest.md`. This file is **appended to** by `/design-lock`, `/animation`, and `/icons` — do not overwrite in later passes.

## Rules of behavior

- **Reference aspects are inspiration, not verdict.** The user can reconsider.
- **Always cite the source.** Not "propose 8px" but "propose 8px because all three typography refs use this scale base".
- **Conflicts are questions, not decisions.** Do not decide for the user.
- **Full-sites count as a single reference weight.** If 1 full-site vs 5 aspect refs — aspects win.
- **Never drop an approved manifest item silently.** It's the whole point of this file.

## What NOT to do

- Do not "copy" the client's own site (copyright issue + worse result — original beats copy).
- Do not push the fashion of the moment ("everyone does glassmorphism right now") — go from brand and mood.
- Do not decide without the user — if uncertain, ask.
- Do not skip Step 5b even if there are no obvious manifest items. Create the file with a note saying "no items from /refs; awaiting /design-lock" so subsequent skills know to append.

## Next

- `/design-lock` — freezes decisions based on the proposal; appends more items to the approved manifest.
