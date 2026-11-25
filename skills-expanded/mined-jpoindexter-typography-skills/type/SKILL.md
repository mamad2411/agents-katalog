---
name: type
description: Use when the user invokes /type, or when any task involves setting, choosing, scaling, spacing, loading, tokenizing, auditing, or critiquing type — a font choice, a type scale, body copy, headings, a data table, a UI label, responsive text, webfont performance, or non-Latin script. Also use when a screen "looks off" and the cause may be typographic. Dispatcher that routes to the focused typography-* skills.
---

# Type — typography router

Routes typographic work to the smallest sufficient set of focused skills. Do not
answer typography questions from memory when a skill below covers them: the skills
carry the decision procedures, the ranges, and the source conflicts that "looks
right" misses.

## Core principle

**Books teach judgment. Current standards teach implementation.**

Never emit a bare universal constant. Encode the decision and its inputs.

> ❌ "Body text should always be 16px."
> ✅ Determine body-text size from the typeface's apparent size, x-height, target
> device, reading distance, content density, user needs, and available line length.
> Treat 16px as a common browser-oriented starting point, not a universal optimum.
> Validate readability, zoom behavior, line length, and hierarchy in the rendered
> context.

## 1. When to invoke

- The user types `/type` (or `$type`).
- Any task that sets, chooses, scales, spaces, loads, tokenizes, audits, or
  critiques type.
- A screen "looks off", "feels cheap", or "looks AI-generated" and the cause may be
  typographic.
- You are about to answer a typography question from memory.

**Do not** invoke for non-typographic layout — that belongs to the general design
skills. Two topics are split rather than excluded: *type* that moves is
`motion-typography` (general interface motion is not this pack's), and *type* that
carries colour or is made of glyphs is `color-and-icon-fonts` (general colour systems
and iconography are not). If the request is
really about information architecture or copy *content* rather than its setting, say
so and route elsewhere.

## 2. Required context

Before routing, establish:

- **What is actually changing** — a value, a system, a file, or a judgment.
- **Medium and platform** — web, native, print, or cross-platform.
- **Whether an artifact exists** to inspect, or this is greenfield.
- **Whether accessibility or i18n is in scope** (they usually are, whether stated or
  not).

If the request is one line and ambiguous, route on the most likely reading and
state the assumption — don't stall.

## 3. Invariant principles

- **Load 2–4 skills maximum per pass.** More is context waste and dilutes attention.
- **Route by what changes, not by vocabulary used.** Someone saying "kerning" often
  means tracking, and someone saying "font" usually means typeface.
- **Always resolve conflicts with the hierarchy below**, and say which rule won.
- **Never claim typography is accessible after a contrast check alone** — 1.4.3,
  1.4.4, and 1.4.12 fail independently.
- **State what was not verified in a rendered context.**

## 4. Context-dependent heuristics — conflict resolution and routing

### Conflict hierarchy — read before deciding anything

Full list in `references/source-hierarchy.md`. Highest first:

1. Accessibility standards and browser behavior
2. User and product context
3. *Thinking with Type* → 4. *Web Typography* → 5. *Flexible Typesetting* →
   6. *Detail in Typography* → 7. *Typographic Systems*
8. The supporting books
9. Style trends and subjective convention

This exists so the agent never applies a print-era rule to a responsive
application, and never lets a trend override an accessibility floor.

### Routing table

| Signal in the request | Load |
|---|---|
| "what is leading / em / baseline", vocabulary, first principles | `type-foundations` |
| naming letterform parts, reading a specimen, apertures/terminals/counters | `typeface-anatomy` |
| "which font should I use", evaluating or replacing a typeface | `typeface-selection` |
| combining two or more typefaces | `typeface-pairing` |
| type scale, heading levels, size ramp, "hierarchy is unclear" | `hierarchy-and-scale` |
| body copy, long-form reading, measure, line-height, paragraphs | `body-text-and-reading` |
| fluid type, clamp(), breakpoints, "text breaks on mobile" | `responsive-typography` |
| buttons, labels, inputs, tables, nav, dense product UI | `ui-component-typography` |
| articles, marketing pages, art-directed layouts, drop caps, pull quotes | `editorial-web-typography` |
| composition, grid, spatial arrangement, "layout feels arbitrary" | `typography-layout-systems` |
| kerning, tracking, word spacing, hyphenation, punctuation, orphans/widows | `microtypography` |
| variable fonts, weight/width/optical-size axes, `font-variation-settings` | `variable-fonts` |
| animated or kinetic type, text transitions, scroll effects, streaming text | `motion-typography` |
| colour fonts, layer fonts, `font-palette`, icon fonts vs SVG, emoji | `color-and-icon-fonts` |
| webfont performance, FOUT/FOIT, CLS, subsetting, `font-display` | `font-loading-and-performance` |
| contrast, zoom, Dynamic Type, dyslexia, screen readers, WCAG | `typography-accessibility` |
| Arabic, Hebrew, CJK, Indic, bidi, vertical text, localization | `international-typography` |
| exporting type as design tokens, Style Dictionary, theme config | `design-token-generation` |
| "check this", systematic review against criteria, pass/fail | `typography-audit` |
| "is this good", taste, expressive judgment, art direction | `typography-critique` |

### Reference tables (load directly, no skill needed)

| Question | File |
|---|---|
| "which OpenType tag / CSS property does X?" | `references/opentype-features.md` |
| "is there a principle covering X?" | `references/universal-principles-index.md` (all 100, routed) |
| "the books disagree — which wins?" | `references/source-hierarchy.md` |
| "what do the books actually disagree about?" | `references/corpus-conflicts.md` |

### Always co-load

- Anything rendering **body text** → also `typography-accessibility`.
- Anything shipping **webfonts** → also `font-loading-and-performance`.
- Anything for a **non-English or multi-script** product → also
  `international-typography`.

### Shortcuts

- "Make this look better", no specifics → `typography-critique` +
  `hierarchy-and-scale` + `microtypography`.
- "Build a type system" → `hierarchy-and-scale` + `responsive-typography` +
  `design-token-generation`.
- "Why does this feel cheap / generic / AI-generated" → `typography-critique` +
  `microtypography`. The tell is almost always spacing detail, not font choice.
- "Audit our typography" → `typography-audit`, which pulls others as needed.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Answered from memory; emitted a constant | Router skipped | Load the skill; encode the procedure |
| Loaded all twenty-one skills | Routing by topic, not by change | 2–4 max |
| Routed "kerning" to letterform spacing | Took the word literally | Usually tracking → `microtypography` |
| Font swap recommended for a spacing problem | Skipped `typography-critique` §4 | Diagnose before prescribing |
| Body text set with no accessibility check | Co-load rule ignored | Always add `typography-accessibility` |
| Emitted 2017 font-loading advice | Corpus treated as current | Rule 1 outranks the books |
| Gave taste feedback when criteria existed | Critique/audit conflated | Criteria → audit |
| Claimed "accessible" after contrast only | Criteria treated as one | Check 1.4.4 and 1.4.12 too |

## 6. Evaluation procedure

1. Identify what the task actually changes.
2. Pick 2–4 skills from the table. Apply co-load rules.
3. Read them before answering — not after drafting.
4. If two skills conflict, resolve with the hierarchy and name the winning rule.
5. Before answering, check: did I emit any bare constant? Replace it with its
   decision procedure.
6. Check whether the claim needs a rendered artifact. If you didn't render it, say so.
7. If the answer touches CSS, browser support, or font loading, verify against MDN —
   the corpus is 2007–2024.

## 7. Output format

```
Routed to: <skill>, <skill> [+ <co-loaded skill> because <rule>]
Assumption: <if the request was ambiguous>
<the answer, in the loaded skill's own output format>
Conflicts resolved: <which rule won>
Unverified: <what was not checked in a rendered context>
```

## 8. Examples

**"Our dashboard numbers look wobbly."**

> Routes to `ui-component-typography` (tabular figures own this) plus
> `typeface-anatomy` (to confirm the face actually ships a `tnum` set). Two skills,
> not five. The word "wobbly" is a rendering symptom, so the answer requires looking
> at the rendered table — flag that if you can't.

**"Set up typography for our new marketing site."**

> Greenfield and broad, so route in sequence rather than loading everything at once:
> `typeface-selection` → `hierarchy-and-scale` → `responsive-typography`, co-loading
> `typography-accessibility` (body text) and `font-loading-and-performance`
> (webfonts). Answer each stage before moving on; don't try to produce a whole
> system in one pass.

## 9. Counterexamples

- ❌ Answering "what line-height should I use?" directly. — That's
  `body-text-and-reading`, and the answer depends on measure, size, and face.
- ❌ Loading all twenty-one skills for "pick a font."
- ❌ Routing "the text looks bad on mobile" to `typeface-selection`. — Almost always
  `responsive-typography` + `body-text-and-reading`.
- ❌ Treating `typography-audit` and `typography-critique` as interchangeable. —
  Criteria exist → audit. Taste → critique.
- ❌ Skipping `international-typography` because "we're English-only for now." — If
  the product will localise, the layout decisions are being made now.
- ❌ Quoting a book on `font-display` behavior. — Rule 1 outranks rule 4.

## 10. Source citations

Corpus: Lupton *Thinking with Type* 3e (2024); Rutter *Web Typography* (2017);
Brown *Flexible Typesetting* (2018); Elam *Typographic Systems* (2007); Hochuli
*Detail in Typography* (2008); Coles *The Anatomy of Type* (2012); Lupton (ed.)
*Type on Screen* (2014); Latin *Better Web Typography* (2017); Santa Maria *On Web
Typography* (2014); Stocks *Universal Principles of Typography* (2024).

Living sources, which outrank the books on implementation:
[MDN CSS Fonts](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_fonts) ·
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) ·
[web.dev fonts](https://web.dev/learn/performance/optimize-web-fonts) ·
[W3C Internationalization](https://www.w3.org/International/)

See also `references/source-hierarchy.md` and `references/corpus-conflicts.md`.
