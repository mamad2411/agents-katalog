---
name: international-typography
description: Use whenever type will render in a non-Latin script or a language other than English — Arabic, Hebrew, CJK, Indic, Cyrillic, Greek, Thai. Also use for bidirectional text, vertical writing, localisation-driven layout breakage, font stacks for multiple scripts, and any assumption that Latin typographic rules generalise.
---

# International typography

The default assumption in every other skill is Latin script. That assumption is
wrong for most of the world's readers, and it fails in ways that are invisible to
a monolingual reviewer.

## 1. When to invoke

- Any product supporting a non-Latin script, now or planned.
- Bidirectional text (Arabic, Hebrew) mixed with Latin.
- CJK, Indic, Thai, or vertical writing.
- Layout breaking after localisation.
- Building a font stack that must cover several scripts.

**Always co-load for any non-English or multi-script product.**

## 2. Required context

- **Every script** in scope, and any planned.
- Whether text mixes scripts **within a line** (numerals, brand names, code).
- Whether content is **user-generated** (you cannot predict the script).
- Whether the font covers each script, or a **per-script stack** is needed.
- Locale-specific conventions: numerals, quotation marks, date formats.

## 3. Invariant principles

- **Latin typographic rules do not generalise.** The Latin axes are cap height,
  x-height, and baseline. Other writing systems have different points of focus:
  many **Indic scripts hang from a headline**; **Chinese characters gravitate to the
  heart** (a centred square); **Japanese characters occupy a square**; **Indic and
  Arabic emphasize horizontal flow.** (Lupton)
- **"x-height" and "cap height" are meaningless in scripts without those features.**
  So is any rule derived from them, including much size- and leading-matching advice.
- **Measure in characters does not transfer.** A CJK line of 40 characters carries
  far more content than 40 Latin characters; Arabic and Devanagari have different
  densities again. Use per-script guidance, not a translated CPL number.
- **Line-height needs are script-specific and usually larger than Latin.** Devanagari
  and Thai have tall stacked marks above and below; CJK needs space to avoid
  crowding. Latin-tuned leading clips or crowds them.
- **Never hardcode direction.** Use logical CSS properties so RTL works without a
  parallel stylesheet.
- **Never synthesize.** Faux bold and faux italic are wrong in Latin and actively
  destructive in Arabic (which is cursive and connected) and CJK.
- **Italic is not universal.** Many scripts have no italic tradition; emphasis is
  carried differently.

## 4. Context-dependent heuristics

**Use logical properties everywhere.**

| Physical (avoid) | Logical (use) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |
| `width` / `height` | `inline-size` / `block-size` |
| `top` / `bottom` | `inset-block-start` / `inset-block-end` |

This makes a single stylesheet work in both LTR and RTL.

**Mark up language and direction.** `<html lang="ar" dir="rtl">`. Set `lang` on any
inline span in a different language — it drives font selection, hyphenation,
line-breaking, and screen-reader pronunciation.

**Bidi.** Mixed RTL/LTR text (an Arabic sentence containing a Latin brand name or a
number) is resolved by the Unicode bidirectional algorithm. Use `dir="auto"` on
user-generated content, and isolate embedded runs with `<bdi>` or
`unicode-bidi: isolate`. Do not attempt to reorder characters manually.

**Per-script font stacks.** One font rarely covers several scripts well. Use
`unicode-range` to serve a different file per script, which also prevents
downloading a CJK font for a Latin-only page:

```css
@font-face { font-family: App; src: url(latin.woff2);
             unicode-range: U+0000-00FF, U+0131, U+2000-206F; }
@font-face { font-family: App; src: url(arabic.woff2);
             unicode-range: U+0600-06FF, U+FB50-FDFF; }
```

**CJK specifics.** Fonts are very large — subsetting and `unicode-range` matter far
more. Characters are monospaced-square, so justification behaves differently and
works well. Line-breaking can occur between most characters, but `line-break` and
`word-break` control kinsoku rules (characters forbidden at line start/end).
Vertical writing via `writing-mode: vertical-rl` needs `text-orientation` handled
for embedded Latin.

**Arabic specifics.** Cursive and connected; letters change shape by position
(initial/medial/final/isolated). Never letterspace Arabic — it breaks the
connections. Never synthesize bold. Arabic needs more line-height than Latin;
justification uses kashida elongation, not word-space stretching.

**Indic specifics.** Complex shaping with conjuncts, reordered vowel signs, and
marks above and below the headline. Requires proper shaping support; needs
generous line-height. Never assume character order equals visual order.

**Localisation length.** German and Finnish run ~30–40% longer than English;
Japanese and Chinese often much shorter. Design containers to grow. See
`ui-component-typography`.

**Quotation marks are not universal glyphs.** English "…" is one convention among
several: German uses „…" (low-9 opening, high-6 closing), French uses «…» (with a
non-breaking space against the enclosed text), and other locales vary again
(Rutter). Hardcoding English curly quotes into a smart-quote transform is a
Latin-English assumption exactly like the ones this skill exists to catch. Drive
quote glyphs from the `lang` attribute — either the CSS `quotes` property keyed to
`:lang()`, or a locale-aware content pipeline — rather than one fixed substitution
rule for every language.

```css
:lang(de) { quotes: "„" "\201C" "‚" "\2018"; }
:lang(fr) { quotes: "«" "»" "‹" "›"; }
```

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| RTL layout mirrored wrong or not at all | Physical properties | Logical properties + `dir` |
| Arabic looks like disconnected letters | Letterspacing applied, or wrong font | Remove tracking; use a real Arabic face |
| Devanagari/Thai marks clipped | Latin-tuned line-height | Increase; test with real strings |
| Tofu (□) for some characters | Font lacks coverage | Per-script `unicode-range` stack |
| CJK font downloaded on an English page | No `unicode-range` | Split by range |
| Arabic bold looks smeared | Faux bold synthesis | Ship a real bold; `font-synthesis: none` |
| Brand name inside Arabic text appears in the wrong place | Bidi not isolated | `<bdi>` / `unicode-bidi: isolate` |
| Measure guidance applied to CJK | Latin CPL assumed universal | Per-script guidance |
| Screen reader reads Japanese with English phonetics | Missing `lang` | Set `lang` on the element |

## 6. Evaluation procedure

1. List every script in scope. For each, confirm the font actually covers it.
2. Render **real text in each script** — never lorem ipsum, never transliteration.
3. Switch `dir="rtl"` and inspect the whole layout. Anything not mirrored is using
   a physical property.
4. Check marks and extenders aren't clipped — Devanagari, Thai, Vietnamese,
   Arabic diacritics.
5. Test mixed-direction strings: Arabic sentence + Latin brand + digits.
6. Confirm `lang` and `dir` are set correctly, including on inline runs.
7. Confirm `font-synthesis: none` where synthesis would be wrong.
8. Check the longest localisation of every UI string.
9. Verify network: does a Latin-only page avoid downloading CJK/Arabic files?

## 7. Output format

```
Scripts in scope: <list>
Coverage: <script> → <font file> via unicode-range <range> | GAP
Direction: <ltr|rtl|both> — logical properties used: <yes/no>
lang/dir set: <where>
Bidi isolation: <yes/n-a>
Line-height per script: <script>: <value> — <verified with real text?>
Synthesis disabled: <yes/no>
Payload: <script>: <n>KB — conditionally loaded: <yes/no>
Not tested: <scripts not rendered with real content>
```

## 8. Examples

**Product adding Arabic to an existing English interface.**

> This isn't a translation task, it's a layout task. Three things must change
> before any copy lands. First, every physical CSS property becomes logical —
> otherwise the RTL layout won't mirror. Second, a real Arabic face loaded by
> `unicode-range` (U+0600–06FF, U+FB50–FDFF), with `font-synthesis: none`, because
> faux bold on connected cursive script smears the joins. Third, line-height rises
> for Arabic runs; the Latin-tuned value clips diacritics. Then test with a real
> Arabic sentence containing the Latin brand name, isolated with `<bdi>` so bidi
> doesn't reorder it.

## 9. Counterexamples

- ❌ "We'll use the same font for all scripts." — Very few faces cover Latin,
  Arabic, CJK, and Indic well.
- ❌ "Measure is 45–75 characters, so keep CJK lines to 60." — CPL doesn't transfer
  across scripts.
- ❌ "Letterspace the Arabic heading to match the Latin one." — Breaks cursive
  connections.
- ❌ `text-align: left` in a stylesheet that must serve RTL.
- ❌ "Bold it — the browser will synthesize if the weight is missing." — Wrong in
  Latin, destructive in Arabic and CJK.
- ❌ Testing RTL with reversed English placeholder text.
- ❌ "Indic is fine, the characters render." — Rendering ≠ correct shaping;
  conjuncts and reordered vowel signs must be verified by a reader of the script.

## 10. Source citations

- Lupton, *Thinking with Type* 3e — **primary book source.** "The main axes of
  alignment in Latin typography are the cap height, x-height, and baseline. Other
  writing systems have different points of focus. Many Indic scripts hang from a
  headline. Chinese characters gravitate to the heart. Japanese characters occupy a
  square, while Indic and Arabic scripts emphasize horizontal flow."
- **W3C Internationalization** — [w3.org/International](https://www.w3.org/International/)
  — authoritative for script behavior, bidi, and vertical text. **Outranks the books
  here** (source-hierarchy rule 1).
- MDN — [logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values),
  [`unicode-range`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range),
  [`writing-mode`](https://developer.mozilla.org/en-US/docs/Web/CSS/writing-mode),
  [`font-synthesis`](https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis).
- Latin, *Better Web Typography* — language ranges and why the Latin range isn't
  always sufficient.
- Rutter, *Web Typography* — `unicode-range` and subsetting by script; quotation
  marks varying by locale (German „…", French «…» with non-breaking spaces) and
  driving them from `lang` via the CSS `quotes` property rather than one hardcoded
  transform.

**Note on Elam's *Typographic Systems of Design*:** the only text available for this
corpus is the German edition (the English scan has no text layer). Elam's subject —
compositional/grid systems — doesn't cover scripts, bidi, or localisation, so it
contributes nothing specific to this skill; its content is fully used in
`typography-layout-systems` instead. No claims here are attributed to Elam.
