---
name: hierarchy-and-scale
description: Use when building or fixing a type scale, choosing heading sizes, or when a screen's importance ordering is unclear — everything looks the same weight, users miss the primary action, or headings compete. Also use when a design has drifted into a dozen ad-hoc font sizes.
---

# Hierarchy and scale

Hierarchy is the reader's answer to "what do I look at, and in what order." Scale
is the finite set of sizes you allow yourself so that answer stays consistent.

## 1. When to invoke

- Defining a type scale for a product, site, or design system.
- Headings compete, or everything reads at the same importance.
- A codebase has accumulated arbitrary sizes (13px, 15px, 17px, 22px…).
- Content structure exists but is not visible.

**Do not** invoke for body-copy tuning alone (`body-text-and-reading`) or for
spacing detail (`microtypography`).

## 2. Required context

- The **content's real structure** — how many genuine levels exist? Most
  interfaces need 3–4, not 8.
- Whether a **design system or token set** already constrains sizes.
- The **densest** screen the scale must serve, and the **most editorial** one.
- Whether headings must survive translation (German/Finnish run long).
- Body size, since the scale should be anchored to it.

## 3. Invariant principles

- **Hierarchy is relative, not absolute.** A 20px heading is only a heading
  because the body is 16px. Define relationships, not values.
- **Size is the weakest hierarchy tool available, and the most overused.** Weight,
  spacing, colour, position, and case all carry hierarchy. Reach for space and
  weight before size.
- **A scale is a constraint, not a menu.** Its value is in what it forbids. If
  every size is available, there is no scale.
- **Fewer levels read faster.** If two levels are hard to tell apart, you have one
  level with a spacing problem.
- **Proximity outranks size.** A label sitting close to its value is bound to it
  more strongly than any size difference can express.

## 4. Context-dependent heuristics

**Anchor to body size, then step outward.** The body size is determined by
`body-text-and-reading`. The scale extends from it in both directions.

**Ratio selection.** A modular scale multiplies each step by a fixed ratio. Brown
describes it as "like a ruler… a system of measurement you can refer to as you
decide on sizes and spaces."

| Ratio | Character | Fits |
|---|---|---|
| 1.125 (major second) | Very tight | Dense product UI, data tools |
| 1.200 (minor third) | Tight | App interfaces, dashboards |
| 1.250 (major third) | Balanced | General product + marketing |
| 1.333 (perfect fourth) | Open | Content sites, docs |
| 1.414–1.500 | Dramatic | Editorial, landing pages |
| 1.618 (golden) | Very dramatic | Display-led pages; too coarse for UI |

Larger ratios give obvious hierarchy and too few usable mid sizes. Smaller ratios
give many usable sizes and weak distinction. **Dense UI wants a small ratio;
editorial wants a large one.** A product with both often needs a small ratio plus a
few deliberate display sizes outside it.

**The classic scale is a legitimate alternative.** 6, 7, 8, 9, 10, 11, 12, 14, 16,
18, 21, 24, 36, 48, 60, 72 — not a constant ratio, but centuries of use, with a
recurring 2:1 (6/12/24/48). Rutter notes the musical analogy. Its irregularity is a
feature: it's denser where you need choices and coarser where you don't.

**Don't ship raw ratio output.** A 1.25 scale from 16 gives 31.25, 39.0625… Round
to whole or half pixels and keep the rounded value as the token.

**Baseline grid.** A horizontal rhythm every *n* pixels that every text element
aligns to, so unrelated columns share a common baseline. Stocks' concrete version:
a 24px baseline grid — "literally, a line every 24 vertical pixels" — suits body
type with a 24px line-height. Smaller text at 12px line-height can use a 12px
sub-grid, with body type aligning every two lines.

Worth it for editorial, print, and multi-column layouts where cross-column
alignment is visible. Usually **not** worth it for dense product UI, where forcing
every component onto a baseline fights the component's own padding and produces
worse spacing than a simple 4/8px spacing scale. Decide deliberately rather than
adopting one by default — and note that a baseline grid constrains your line-height
choices, which `body-text-and-reading` may have already fixed for readability. If
they conflict, readability wins (rule 2 over convention).

**Weight and space do the work size can't.** Once you have 3–4 sizes, express
further distinction with weight (400/600/700), space above (a heading belongs to
what follows it, so space above > space below), and case.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Eight heading levels, six indistinguishable | Scale generated, not designed | Cut to the levels content actually has |
| Everything looks equally important | Only size varies, and barely | Add weight and spacing contrast |
| Heading looks attached to the paragraph above it | Symmetric margins | More space above than below |
| Scale looks fine in English, breaks in German | Tested on short strings | Test with longest supported locale |
| Marketing hero and dashboard can't share a scale | One ratio forced on both | Small ratio for UI + explicit display steps |
| 22px appears once, off-scale | No enforcement | Tokenize; make off-scale values impossible |
| h1 chosen for size, not structure | Visual level conflated with semantic level | Keep heading *level* semantic; style separately |

## 6. Evaluation procedure

1. List the **real** content levels. Name them by role, not by number.
2. Confirm each level has a distinct job. Merge any that don't.
3. Squint at the rendered screen. Does the intended reading order emerge?
4. Grayscale it. Hierarchy that depends on colour alone fails here — and fails
   for colour-blind users.
5. Grep the codebase for font-size declarations. Every one must be on-scale.
6. Render the longest real string at each level, in the longest locale.
7. Zoom to 200%. Confirm levels remain distinguishable.
8. Verify heading *semantics* (h1…h6) are sequential and independent of visual size.

## 7. Output format

```
Body anchor: <size>
Ratio: <n> (<name>) — chosen because <density/editorial reasoning>
Scale:  <role>  <size>/<line-height>  <weight>  <space-above>
        ...
Levels: <n> semantic, <n> visual
Non-size hierarchy: <weight | space | case | colour>
Checks: squint <pass/fail> · grayscale <pass/fail> · 200% <pass/fail> · longest-locale <pass/fail>
Off-scale values found: <list or none>
```

## 8. Examples

**Analytics dashboard, dense, body 14px.**

> Dense data UI, so a small ratio: 1.2 (minor third). From a 14px body: 14 → 16.8
> → 20 → 24, rounded to 14/17/20/24. Only three levels above body, because the
> content has exactly three (page title, section, card title). Distinction between
> card title and section comes mostly from weight (600 vs 400) and space above,
> not size — at 1.2 the size step alone is too subtle to carry it.

**Marketing site sharing a design system with that dashboard.**

> Don't re-ratio the system. Keep the 1.2 UI scale for all interface chrome and
> add two explicit display steps (48, 64) outside it for hero use only, tokenized
> as `display-1`/`display-2` so they can't leak into UI. This keeps one system
> while letting the editorial surfaces breathe.

## 9. Counterexamples

- ❌ "Use the golden ratio, it's the most harmonious." — 1.618 from a 16px body
  gives 16 → 25.9 → 41.9 → 67.8. There is no usable size between body and a large
  heading. Fine for a poster, unusable for an interface.
- ❌ "Generate the scale and use every step." — A scale's value is exclusion.
- ❌ "Make it an h1 because it should be big." — Heading level is document
  structure and is read by assistive technology. Style is separate.
- ❌ "Add a size between 16 and 20 for this one label." — That's how a scale dies.
  Solve it with weight or space.
- ❌ "The hierarchy works — the primary action is blue." — Fails in grayscale and
  for colour-blind users. Colour may reinforce hierarchy, never carry it alone.

## 10. Source citations

- Lupton, *Thinking with Type* 3e — modular scales; "a type scale is a selection
  of type sizes based on history or mathematics"; preset sizes reflect historical
  type sizes.
- Rutter, *Web Typography* — the classic scale (6…72), the recurring 2:1 ratio,
  and the musical analogy.
- Brown, *Flexible Typesetting* — the modular scale as a ruler, a system of
  measurement tailored to the composition.
- Latin, *Better Web Typography* — modular scale and meaningful typography; heading
  relationships.
- Santa Maria, *On Web Typography* — typographic scales and rhythm; eyeballers vs.
  system-builders.
- Stocks, *Universal Principles of Typography* — a typographic scale is already a
  design system; size, weight, and spacing imply order.
