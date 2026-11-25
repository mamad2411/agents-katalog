---
name: icons
description: Hybrid icon system. First tries to source every needed icon from ONE library (Lucide / Phosphor / Heroicons) unified to the DESIGN-LOCK style spec. Falls back to AI-generated SVG only when the library lacks a themed concept, with strict geometry validation to prevent broken paths and hallucinated artifacts.
---

# /icons

Icons are a common failure point: mixed libraries, mismatched stroke weights, decorative-only icons, hallucinated SVG shapes. This skill enforces **one library, one style, verified geometry**.

## When to use

- After `/media` — media assets are in place, now icons are the last visual asset.
- Before `/build` — build references the icon set from `site/media/icons/`.
- Rerun anytime a new concept is added to the copy.

## Requirements

- `DESIGN-LOCK.md` LOCKED (need §2 type, §3 color, §5 motion, §7 imagery for style spec).
- `brief/copy-analysis.md` exists (concepts are extracted from here).
- `inbox/texts/` populated (backup source for concept extraction).

## Process

### Step 1. Extract concepts from context

Read:
- `brief/01-business.md` — niche, product, services.
- `brief/copy-analysis.md` — recommended section structure and key claims.
- `brief/03-goals.md` — CTA labels and offer names.
- `inbox/texts/*` — surface-level scan for repeating nouns.

Extract **5-15 icon concepts**. Each concept is a short label + intent:

```
- consulting            → conversation, expertise
- roadmap               → path, planning
- reporting             → chart, transparency
- fast-turnaround       → clock, speed
- privacy               → lock, safety
- multi-region          → globe, coverage
```

Present the extracted list to the user. Ask: "add, remove, or rename any concepts before we map to icons?"

### Step 2. Compute style spec from DESIGN-LOCK

Read DESIGN-LOCK and derive:

```
Style spec
  stroke-width:       <derived from type §2 body-weight and radius §4>
                      thin (1px) if radius = 0
                      regular (1.5px) if radius ≤ 8
                      bold (2px) if radius ≥ 12 or pill
  corner-style:       sharp if radius = 0 else rounded
  fill-style:         outline (default) | filled (only if brand uses heavy typography)
                                        | duotone (only if palette §3 is duotone/tritone)
  size-baseline:      24×24 viewBox
  color-strategy:     currentColor (inherit from text via CSS)
  geometric-complexity: minimal (≤ 2 paths) | detailed (up to 4 paths)
```

Show the derived spec. Ask user to confirm or override.

### Step 3. Library selection

Present three candidate libraries, ranked by fit against the style spec:

| Library | Best for | Stroke default | License |
|---------|----------|----------------|---------|
| **Lucide** | tech, SaaS, minimal | 2px | ISC |
| **Phosphor** | editorial, brand, versatile (6 weights) | 1.5px thin | MIT |
| **Heroicons** | minimal, product | 1.5px outline / 24px solid | MIT |

Auto-recommend one based on style spec match. User picks. This choice is written to DESIGN-LOCK §7 (Icons field) and becomes locked for the project — no mixing.

### Step 4. Concept-to-icon mapping

For each concept, find the closest library match. Present in a table:

```
concept              → library icon        confidence
consulting           → phosphor/chats-teardrop     high
roadmap              → phosphor/map-trifold        high
reporting            → phosphor/chart-line-up      high
fast-turnaround      → phosphor/clock              medium
privacy              → phosphor/lock-key           high
multi-region         → phosphor/globe-hemisphere-west  medium
custom-integration   → (none)                      MISSING → AI fallback
```

Confidence levels: **high** (exact match), **medium** (adjacent concept), **low** (loose semantic tie), **MISSING** (no plausible match — flag for AI fallback).

User reviews. For each row user can: accept, pick a different library icon (show 3 alternatives), or move to MISSING to force AI generation.

### Step 5. AI fallback for MISSING concepts only

**Never generate an icon if a library option exists.** AI is last resort.

For each MISSING concept:

1. **Build a strict prompt.** Include:
   - Concept meaning (one sentence).
   - Style spec (stroke-width, corner-style, fill-style).
   - Size: `viewBox="0 0 24 24"`.
   - Color: `stroke="currentColor" fill="none"` (or `fill="currentColor"` for solid).
   - Constraints: max 2 paths, no gradients, no filters, no text elements, all paths closed, symmetric where the concept implies it.
   - Reference: "match visual weight of Phosphor Regular icons" (or whichever library was picked).

2. **Generate.** Produce a candidate SVG.

3. **Validate.** Run the SVG through these gates:
   - **Parseable.** Valid XML, no unclosed tags. If fail → retry (max 3).
   - **viewBox.** Exactly `0 0 24 24`. If fail → rewrite.
   - **Path count.** `<= 2` `<path>` elements (or up to 4 if `geometric-complexity=detailed`). If fail → retry with tighter prompt.
   - **Paths closed.** Every `<path d="…">` either ends with `Z`/`z` or returns to its `M` start within 0.5 units. If fail → retry.
   - **Stroke width match.** All `stroke-width` attributes equal library baseline. If mismatch → normalize.
   - **No prohibited elements.** No `<text>`, `<image>`, `<filter>`, `<mask>`, `<foreignObject>`, `<defs>` with gradients. If fail → retry.
   - **No dangling points.** Detect degenerate `M x,y M x,y` sequences with no intervening geometry. If fail → retry.
   - **Symmetry (conditional).** If concept implies symmetry (heart, star, target, shield, cross) — measure axis symmetry within 2% tolerance. If fail → retry.

4. **Retry policy.** Up to 3 attempts. If all fail, escalate to user:
   ```
   ⚠️ Could not generate a clean icon for "custom-integration" after 3 attempts.
   Options:
   A. Pick a library alternative (show 3 loose matches from Phosphor)
   B. Refine the concept ("integration" → "handshake"? "puzzle"?)
   C. Skip — this concept ships without an icon
   ```

### Step 6. Unification pass

All icons — library-sourced and AI-generated — go through the same normalization:

1. **SVGO** with a locked config:
   ```json
   {
     "plugins": [
       "preset-default",
       { "name": "removeViewBox", "active": false },
       { "name": "removeDimensions", "active": true }
     ]
   }
   ```
2. **Inject `stroke="currentColor"` and `fill="none"`** (or the fill counterpart for solid) — remove hardcoded colors.
3. **Enforce `stroke-width`** to the library baseline.
4. **Add `class="icon icon-<concept>"`** to the root `<svg>` for CSS targeting.
5. **Add `aria-hidden="true"`** by default. If the icon is standalone (no accompanying text), it must instead have `role="img"` and `<title>` — flag for the user to decide.

### Step 7. Output

Write to `site/media/icons/`:

```
site/media/icons/
  consulting.svg
  roadmap.svg
  reporting.svg
  fast-turnaround.svg
  privacy.svg
  multi-region.svg
  custom-integration.svg     ← AI-generated, marked in README
  README.md                  ← concept → file map + source (library or AI)
  _snippets.html             ← ready-to-paste <svg> inline snippets for /build
```

**`site/media/icons/README.md`** structure:

```markdown
# Icons

Library: **Phosphor Regular** (locked in DESIGN-LOCK §7).
Total: 7 icons (6 library, 1 AI-generated).

| concept | file | source | notes |
|---------|------|--------|-------|
| consulting | consulting.svg | phosphor/chats-teardrop | — |
| ... |
| custom-integration | custom-integration.svg | AI-generated | validated: 2 paths, symmetric |
```

**Append to `references/approved-manifest.md`** — every icon that ships is a required element in the corresponding section:

```
[ ] icon:consulting → services section
[ ] icon:privacy → footer/trust
```

`/build` confirms each icon appears in the generated HTML.

## Rules of behavior

- **One library, no mixing.** Once picked in Step 3, no other library icons enter the project.
- **AI only when necessary.** Library-first, always. AI fallback is the last resort, gated by validation.
- **No decorative icons.** Every icon must earn its place tied to a concept from the copy. Decoration = anti-slop rule violation.
- **`currentColor` only.** Never hardcode fill/stroke in SVG — inherit from CSS so tokens.css controls color.
- **Validate before shipping.** An AI SVG without geometry validation is a broken-icon bug waiting to happen.

## What NOT to do

- Do not generate icons before locking the library.
- Do not accept AI output that failed a validation gate — retry or fall back to library.
- Do not embed inline `<style>` in SVGs — all styling via CSS classes.
- Do not use icon fonts (FontAwesome, Material Icons) — SVG only, unified pipeline.
- Do not add icons for concepts the user did not confirm in Step 1.

## Next

- `/build` — reads `site/media/icons/_snippets.html` and drops inline SVG into sections. Checks approved-manifest coverage.
- `/audit` — confirms only one icon library was used, all icons have `aria-hidden` or `role="img"`, no icon fonts loaded.
