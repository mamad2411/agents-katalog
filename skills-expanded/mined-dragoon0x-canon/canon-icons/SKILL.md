---
name: canon-icons
description: Use when designing, auditing, or refactoring iconography, icon libraries, emoji usage, or icon-only buttons. Covers icon sizing, stroke weight, grid alignment, meaning ambiguity, accessibility, when to pair icons with labels, and the rules for using SVG vs font vs emoji. Trigger when the user mentions icon, glyph, emoji, SVG, pictogram, or icon button.
---

# CANON · Icons

An icon that needs explanation is a failed icon. Most of them fail.

## The "nobody knows what that means" test

Before any icon enters your UI, answer: **would a first-time user of this product understand what clicking it does, without a tooltip?**

Icons that pass (almost universal): ✕ (close), ⌕ (search), ← (back), ⬇ (download), ▶ (play), 🖨️ (print, desktop only), 🗑️ (delete).

Icons that fail more than they succeed: ≡ (hamburger on desktop), ⚙️ (settings is fine; customize/config/admin are not), ∅ (empty? no? disabled?), 🔁 (refresh? loop? sync?), custom brand icons for custom features.

If the icon fails the test, **pair it with a label.** Always.

## Sizing

Pick a pixel size, not a visual size. Icon grids are designed at specific sizes; scaling them creates sub-pixel blur.

| Size | Context |
|---|---|
| 12–14px | Inline with caption text, inside chips |
| **16px** | Inline with body text, input adornments, menu items |
| **20px** | Buttons (default), nav items |
| 24px | Primary buttons, toolbars |
| 32–40px | Tab bars (mobile), large actions |
| 48–64px | Empty state illustrations, onboarding |

**Mobile tap targets require 44×44px total hit area**, even if the icon glyph is 20px. Pad around the icon.

## Stroke weight

Icons in a set should share one stroke weight. Mixing looks amateur.

| Style | Stroke | Use |
|---|---|---|
| Outline / linear | 1.5–2px | Modern, airy |
| Duotone | 1.5–2px + filled accent | Playful |
| Solid / filled | No stroke | Dense UIs, small sizes (< 16px read better filled) |
| Glyph (mono) | Custom per icon | Brand iconography |

Don't mix outline and filled in the same toolbar. If you want filled-active and outline-inactive, pick a library that supports both.

## Pairing icons with text

Research shows icon + label outperforms icon-only for comprehension in almost every tested case. Icon-alone is acceptable only when:

1. The meaning is truly universal (✕, search, back arrow).
2. Space is genuinely exhausted (mobile tab bar, dense toolbar).
3. The action is secondary and a tooltip on hover/focus is available.

Even then, provide a tooltip + aria-label.

## Accessibility

### Icon is decorative (paired with text)

```html
<button>
  <svg aria-hidden="true" focusable="false">...</svg>
  Save changes
</button>
```

- `aria-hidden="true"` and `focusable="false"` on SVG.
- Screen reader reads the text label only.

### Icon is the only signal (icon-only button)

```html
<button aria-label="Delete item">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>
```

- `aria-label` on the button, not the SVG.
- Still `aria-hidden="true"` on the SVG.

### Meaningful decorative icons (inline with content)

```html
<p>
  <svg aria-hidden="true" focusable="false">...</svg>
  5 items saved
</p>
```

- If the text already conveys the meaning, icon is decorative.

## Format choice — SVG wins

| Format | Use? |
|---|---|
| **SVG (inline)** | **Default.** Recolorable via CSS, sharp at any size, small file size |
| SVG sprite | Good for libraries with many icons in use |
| Icon font | Avoid. Screen reader confusion, no pixel-perfect control, blocks render |
| PNG / raster | Only for complex illustrations where SVG isn't feasible |
| Emoji | For user-facing casual UI only (chat messages, reactions). Not for interface chrome. |

### Why not icon fonts

- Screen readers sometimes read the private-use-area codepoint.
- Font loading delays icon rendering.
- Can't style parts of the icon.
- Rasterized at non-integer sizes.

Use SVG.

## Color

- Icons inherit `color` via `currentColor` in SVG. Set `stroke="currentColor"` or `fill="currentColor"` in the SVG source.
- Icons follow text color in most contexts. Separate tokens only for special uses (success checkmark green, destructive red trash).
- Contrast: 3:1 minimum for interactive icons against the background. WCAG 1.4.11 Non-Text Contrast.

## Emoji in UI

Emoji render differently across platforms. An emoji in one button on iOS looks different on Android looks different on Windows.

| Use emoji for | Don't use emoji for |
|---|---|
| User-generated content (chat, reactions) | Interface chrome (nav, buttons, labels) |
| Marketing / casual comms | Status indicators (red circle could be anything) |
| Empty state flavor text | Primary UI signals |

If you must use emoji in the UI, test across iOS, Android, Windows, macOS — they render very differently.

## Icon + text alignment

When inline with text, icons should visually center, not baseline-align.

```css
.icon-text {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
```

Gap between icon and label: 6–8px at 14–16px text size.

## Brand icons (logos)

- Preserve aspect ratio.
- Keep minimum size constraints (brand guidelines usually specify).
- Don't recolor locked brand marks.
- Pair with `aria-label` naming the brand for screen readers.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Mixing outline and filled icons in one set | Visual chaos |
| Different stroke weights across the same toolbar | Amateur appearance |
| Icon fonts in production | Screen reader + rendering issues |
| Icon-only buttons without `aria-label` | Inaccessible |
| Hamburger menu on desktop | 30–50% lower discoverability (Luke W. research) |
| Emoji for critical status | Renders inconsistently across platforms |
| Icon size < 16px for tap targets | Not even close to the 44px floor |
| Custom icons for universal actions (back, close) | Users have to relearn |
| Animated icons without reduced-motion fallback | Triggers motion sensitivity |
| Lottie animations for simple loaders | 500KB for 3 seconds of spinning |

## Decision tree

```
Does the icon's meaning pass the "first-time user" test?
  ├─ No → Pair with a text label
  └─ Yes → Icon-only OK (with aria-label + tooltip)

Inline with text or standalone?
  ├─ Inline → Size matches x-height (16px for 14–16px text)
  └─ Standalone → Size from the button scale (20–24px)

SVG or emoji?
  ├─ Interface chrome → SVG, always
  └─ User-generated / casual → Emoji acceptable

Animated?
  └─ Only if it communicates state change. Always with prefers-reduced-motion fallback.
```

## Audit checklist

- [ ] All icons in a set share one stroke weight
- [ ] All icons in a set share one visual style (outline OR filled, not mixed)
- [ ] Icons use SVG, not icon fonts
- [ ] SVGs have `aria-hidden="true"` and `focusable="false"` when decorative
- [ ] Icon-only buttons have `aria-label` on the button
- [ ] Icon + text uses `currentColor` or shares color tokens
- [ ] Icon contrast ≥ 3:1 against background
- [ ] Mobile tap targets ≥ 44×44px
- [ ] Icons inline with text are visually centered
- [ ] Gap between icon and label is 6–8px
- [ ] No emoji in critical UI status
- [ ] No animated icons without reduced-motion fallback

## Sources

- WCAG 2.2 · 1.1.1 Non-text Content, 1.4.11 Non-Text Contrast, 2.5.5 Target Size
- Material Design 3 · Iconography
- Apple HIG · SF Symbols (sizing, semantic scale)
- Phosphor / Lucide / Heroicons · stroke-weight reference
- Nielsen Norman · "Icon Usability" (icon + label research)
