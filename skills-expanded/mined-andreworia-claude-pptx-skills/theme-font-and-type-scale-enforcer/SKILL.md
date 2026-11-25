---
name: theme-font-and-type-scale-enforcer
description: Replaces rogue fonts and random sizes with the brand heading and body fonts on a consistent type scale.
---

# Theme Font and Type-Scale Enforcer

## When to use

Use this skill when rogue fonts or random sizes break the type system. Symptoms include a deck with Calibri, Arial, and the brand font mixed across slides, titles that are 32pt on one slide and 28pt on the next, and body copy ranging from 11pt to 16pt for no reason. Run this in Stage 2 alongside the color work, so type and color are both wired to the theme.

## What it does

It binds the deck to the brand's two theme fonts (a heading font and a body font) and enforces a single type scale: a fixed set of sizes for title, subtitle, section header, body, sub-body, and caption. After this skill, every slide uses the brand fonts at the right sizes, and a font swap in the theme would carry through.

## Method

A PowerPoint theme defines a font pair: the major (heading) font and the minor (body) font. A type scale is the small set of sizes the brand uses. The job is to make the deck use the theme fonts at the scale sizes everywhere.

1. **Read the theme fonts and scale.** From the template, record the major font, the minor font, and the size for each level: title, subtitle, section header, body level one, body level two, caption, and footer. If the brand has no documented scale, derive it from the template's placeholders.

2. **Find non-theme fonts.** Scan for any font that is not the major or minor theme font. Use Home then Replace then Replace Fonts to list and swap fonts deck-wide: replace each stray font with the appropriate theme font (headings to the major font, body to the minor font).

3. **Bind to theme fonts, not the named font.** Where possible set text to "+Headings" and "+Body" (the theme font slots) rather than the literal font name, so a theme font change carries through. In placeholders this is automatic once direct formatting is cleared.

4. **Normalize sizes to the scale.** Map every text size to the nearest scale level by role. A title at 30pt or 34pt snaps to the scale's title size. Body at 13pt snaps to the body size. Do not invent in-between sizes. If a slide is overset and needs smaller text, reduce content or move detail to backup rather than shrinking below the scale.

5. **Fix weights and styles.** Use the brand's weights (for example a semibold heading, a regular body). Remove ad hoc bold, italics, all-caps, and letter-spacing that are not part of the system, keeping only the emphasis the brand sanctions.

6. **Repair line spacing and case.** Set line spacing to the brand value rather than per-slide guesses. Apply the brand's title case rule (sentence case or title case) consistently across titles.

7. **Re-clear direct formatting.** After replacing fonts, clear direct formatting on placeholder text so it inherits the theme font and the placeholder's scale size, then re-apply only sanctioned emphasis.

## Inputs

- The deck to fix.
- The brand's major and minor fonts and the type scale (sizes per level). If undocumented, ask, or derive from the template placeholders.

## Output format

A type enforcement report:

- The theme fonts and the scale, restated.
- A font replacement list: each stray font and its theme replacement.
- A size normalization list: out-of-scale sizes found and the scale size they snap to.
- Notes on case, weight, and line spacing fixes.

Close with a confirmation that the deck uses only the two theme fonts at scale sizes.

## Example

Input: titles in Arial at mixed sizes, body in Calibri, one slide in Georgia.

Output:

- Theme fonts: major font for headings, minor font for body. Scale: title 28pt, body 14pt, caption 11pt.
- Replace Fonts: Arial and Georgia to the major font for headings, Calibri to the minor font for body.
- Sizes: titles at 30pt and 34pt snap to 28pt; body at 13pt and 16pt snap to 14pt.
- Result: two theme fonts, fixed scale, deck-wide.
