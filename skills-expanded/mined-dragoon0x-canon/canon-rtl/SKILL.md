---
name: canon-rtl
description: Use when designing or implementing right-to-left (RTL) layout support for Arabic, Hebrew, Farsi, Urdu, and other RTL scripts. Covers logical properties, mirroring rules, bidirectional text, icon direction, and what should NOT flip. Trigger when the user mentions RTL, right-to-left, Arabic, Hebrew, bidi, or dir="rtl".
---

# CANON · RTL

RTL is not "flip everything." It's about reading direction. Text, layout flow, and directional icons mirror. Decorative elements, media controls, and universal icons do not.

## Set the direction

```html
<html lang="ar" dir="rtl">
```

`dir="rtl"` on `<html>` flips the entire document flow. Browser handles most text and flexbox/grid automatically.

## Use CSS logical properties

Physical properties break in RTL. Logical properties work in both directions automatically.

| Physical (avoid) | Logical (use) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `text-align: left` | `text-align: start` |
| `float: left` | `float: inline-start` |
| `left: 0` | `inset-inline-start: 0` |
| `border-left` | `border-inline-start` |

```css
.sidebar { margin-inline-start: 24px; padding-inline-end: 16px; }
```

## What mirrors (flips in RTL)

- Text alignment and flow
- Flex and grid direction (row → row-reverse)
- Navigation order (left-to-right becomes right-to-left)
- Breadcrumbs (Home > Products becomes Products < Home)
- Directional icons: back arrow, forward arrow, chevrons pointing "forward/backward"
- Progress bars, sliders, timeline direction
- Lists with indentation
- Form layout: labels relative to inputs

## What does NOT mirror

- Media playback controls (play/pause/seek are universal)
- Phone number fields (always LTR, digits are universal)
- Clocks (clockwise is universal)
- Logos and brand marks
- Checkmarks, plus/minus, close X
- Up/down arrows (vertical is directionless)
- Images and photos (don't flip)
- Charts with mathematical axes (0 at origin)
- Slash direction in paths (/Users/path)

## Bidirectional text (bidi)

Mixed LTR and RTL content in the same string (e.g., Arabic text with an English brand name):

```html
<p>مرحباً بك في <bdi>CANON</bdi> للتصميم</p>
```

- `<bdi>` isolates the embedded text direction.
- Never rely on Unicode control characters manually. Use HTML elements.

## Numbers

Arabic-Indic numerals (٠١٢٣٤٥٦٧٨٩) are used in some Arabic locales. Western Arabic numerals (0123456789) are acceptable and more common in UI contexts. Check locale conventions.

Phone numbers, dates, and currency amounts follow locale formatting regardless of direction.

## Testing

Test at minimum: Arabic (RTL, connected script), Hebrew (RTL, disconnected), English (LTR baseline).

Visual checklist:
- Text reads naturally right-to-left
- Navigation items right-to-left
- Back arrow points right, forward points left
- Sidebar is on the right
- Form labels align correctly relative to inputs
- No overlapping elements from position: absolute with physical offsets

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Flipping images/photos | Content becomes wrong (text in images reads backward) |
| Using physical CSS properties | Breaks RTL layout |
| Flipping media controls | Universal direction |
| Manual `transform: scaleX(-1)` on entire containers | Hacky, breaks text rendering |
| Not testing with real RTL content | Latin text in RTL doesn't expose connected-script issues |
| Hardcoded `left: 20px` for positioned elements | Wrong side in RTL |
| Breadcrumb separators not flipping | Reading direction confused |

## Audit checklist

- [ ] `dir="rtl"` on `<html>` for RTL locales
- [ ] `lang` attribute matches the content language
- [ ] CSS uses logical properties (inline-start/end, block-start/end)
- [ ] Directional icons (arrows, chevrons) mirror correctly
- [ ] Non-directional icons (close, check, play) do NOT mirror
- [ ] `<bdi>` used for embedded opposite-direction text
- [ ] Phone/number inputs use `dir="ltr"` explicitly
- [ ] Tested with real Arabic or Hebrew content
- [ ] Flexbox/grid flow works without manual reversal
- [ ] No physical `left`/`right` in CSS

## Sources

- W3C · CSS Logical Properties (spec)
- Material Design 3 · Bidirectionality
- Apple HIG · Right-to-Left
- MDN · `<bdi>`, CSS Logical Properties
