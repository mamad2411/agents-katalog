---
name: font-loading-and-performance
description: Use when shipping webfonts — choosing formats, subsetting, preloading, setting font-display, eliminating FOUT/FOIT, or fixing layout shift (CLS) caused by font swap. Also use when fonts are slow, text is invisible on load, the page jumps when fonts arrive, or Core Web Vitals flag font-related shift.
---

# Font loading and performance

Webfonts are render-blocking-adjacent resources that change text metrics when they
arrive. Two separate problems: **when text becomes visible**, and **whether the
page moves when the font swaps**.

⚠️ **Part of the corpus is obsolete here — but not all of it.** Rutter (2017)
calls `font-display` "a nascent CSS property under development," supported only
behind experimental flags at the time; that support status is obsolete —
`font-display` now has universal support and is the standard mechanism. His
five-value taxonomy and their descriptions (`auto`/`block`/`swap`/`fallback`/
`optional`), however, match the current spec closely and are still accurate —
don't discard the substance along with the outdated adoption note. What's
genuinely dead is the workaround the books reach for instead: the Font Loading
API + `wf-loading`/`wf-active`/`wf-inactive` classes (Rutter) and Web Font Loader
(both Rutter and Santa Maria) exist specifically to fake `font-display` behavior
in browsers that don't support it. No browser needs that workaround now.
Source-hierarchy rule 1 (browser behavior) outranks rules 4 and 8. Verify against
MDN before emitting code.

## 1. When to invoke

- Adding, replacing, or auditing webfonts.
- FOIT (invisible text) or FOUT (unstyled flash) reported.
- CLS regression traced to text.
- Font payload is large, or you're choosing between static and variable files.
- Self-hosting vs. a font CDN.

## 2. Required context

- Which **families, weights, styles, and scripts** are genuinely used. Most sites
  ship far more than they render.
- Whether the font is **self-hosted or third-party**.
- Whether the text is **above the fold**.
- The **fallback stack** and how far its metrics sit from the webfont.
- Current **CLS** and whether font swap contributes.
- Whether a **variable font** could replace multiple static files.

## 3. Invariant principles

- **Text must never be invisible indefinitely.** A font that fails to load must
  not take the content with it.
- **Only ship glyphs you render.** Unused weights, styles, and language ranges are
  pure cost.
- **WOFF2 is the format.** Universally supported and best-compressed. Additional
  formats are legacy weight.
- **Self-hosting is the default.** Third-party font CDNs add a connection to
  another origin and no longer benefit from cross-site cache sharing — browsers
  partition their HTTP cache by origin.
- **Preload only what's critical and certain.** Preloading everything competes
  with the resources that actually block render.
- **Swap-induced layout shift is preventable, not inevitable.**

## 4. Context-dependent heuristics

**`font-display`.**

| Value | Behavior | Use for |
|---|---|---|
| `swap` | Fallback immediately, swap when ready | Body text; safest default |
| `optional` | Very short block; may never swap | Perf-critical; eliminates swap CLS outright |
| `fallback` | Short block, short swap window | Compromise |
| `block` | Hides text up to ~3s | Almost never — this is FOIT |
| `auto` | Browser default (usually block-like) | Don't rely on it |

Default to `swap` for body text. Use `optional` when CLS matters more than seeing
the intended face on first visit — with `optional` the font is used on subsequent
visits from cache, so the cost is first-paint only.

A general target worth naming: Rutter frames the underlying goal as delivering a
*usable* page within about one second — fonts shouldn't be what blows that budget.
Note also that Rutter's own recommended default for body text is `fallback`, not
`swap`: it still gives the webfont a brief window to arrive before committing to
the fallback, at the cost of occasionally never swapping at all if the font is
slow. `swap`'s guarantee of an eventual (possibly disruptive) swap is why current
guidance treats it as the safer general default — but `fallback` is a legitimate,
deliberate choice where a mid-read swap is worse than staying on the fallback
face, and worth reaching for rather than treating `swap` as the only option.

**Killing swap CLS with metric-matched fallbacks.** This is the current technique
and the one the books predate. Declare a fallback `@font-face` over a local font
and override its metrics so the fallback occupies exactly the space the webfont
will:

```css
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107%;        /* match x-height / cap-height first */
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
body { font-family: "Inter", "Inter Fallback", sans-serif; }
```

`size-adjust` scales the glyphs proportionally and is the primary tool for matching
apparent size; the three override descriptors force identical vertical metrics so
the line box is unchanged across the swap. Tuned correctly the swap moves nothing
and font-related CLS goes to zero. (Target: CLS < 0.1 overall.)

**`font-size-adjust` — the other half of fallback matching.** Where `size-adjust` in
`@font-face` scales a fallback to match the webfont, `font-size-adjust` on the
element normalises apparent size by **aspect value** — the font's x-height divided by
its font size. Rutter's note on why it's useful: it "only affects the rendered size
of the text, not the reported or calculated size," so **line-height is unaffected**
and the surrounding code stays simple.

```css
body { font-family: "Altis", Arial, sans-serif; font-size-adjust: 0.545; }
/* modern syntax also allows a metric and from-font: */
body { font-size-adjust: ex-height from-font; }
```

The current grammar is `none | [ ex-height | cap-height | ch-width | ic-width |
ic-height ]? [ from-font | <number> ]`; `ex-height` is the default metric. Support is
narrower than `size-adjust`, so treat it as an enhancement and verify on MDN before
relying on it. Prefer `size-adjust` + the metric-override descriptors as the primary
technique; reach for `font-size-adjust` when you want apparent-size normalisation
without touching the line box.

**Choosing which system font to fall back to.** Metric-matched `size-adjust`
overrides fix the box a fallback occupies, but they don't fix a badly *chosen*
fallback — that's a separate, earlier decision (Rutter). Pick the candidate by
eye before tuning its metrics:

1. **Legibility and apparent size first** — a similar x-height so the fallback
   doesn't read as a different, worse-tuned typeface during its window on screen.
2. **Horizontal metrics next** — an economical webfont needs an economical
   fallback, or the reflow the metric overrides are trying to prevent shows up
   anyway in word-wrap differences.
3. **Stylistic match last** — compare the fallback and webfont's `G`, `W`, `a`,
   `y`, and `g`; those letters vary the most between faces and are where a
   mismatch is most visible mid-swap.

**Subsetting.** Cut to the scripts and characters you actually use — but never
subset away characters real content needs. User-generated content, names, and
currency symbols routinely break naive Latin-only subsets. `unicode-range` lets you
split by script so the browser downloads only the ranges it encounters.

**Variable vs. static.** One variable file replacing 4+ static weights is usually a
win. Replacing two is usually not — a variable font carries the whole design space.
Measure both, don't assume. See `variable-fonts`.

**Preload.** Preload the one or two files needed for above-the-fold text, and only
if you're certain they'll be used:

```html
<link rel="preload" href="/f/inter-var.woff2" as="font" type="font/woff2" crossorigin>
```

`crossorigin` is required even same-origin — fonts are fetched in CORS mode. Omit
it and you download the file twice.

## 5. Failure patterns

| Pattern | Cause | Fix |
|---|---|---|
| Text invisible for seconds | `font-display: block`/`auto` | `swap` or `optional` |
| Page jumps when font arrives | Metric mismatch with fallback | Metric-matched fallback `@font-face` |
| Fallback still looks visibly wrong even after metric-matching | Fallback face itself picked without comparison | Choose by x-height, horizontal metrics, then G/W/a/y/g before tuning metrics |
| Font downloaded twice | `preload` without `crossorigin` | Add it |
| Huge payload | Shipping unused weights/styles | Ship only what renders |
| Preloading many fonts, render still slow | Preload competing with critical resources | Preload ≤2 critical files |
| Fallback shows tofu for some names | Over-aggressive subset | Widen `unicode-range` |
| Variable font bigger than the statics it replaced | Replaced too few weights | Compare real bytes |
| Third-party CDN slow on first paint | Extra origin, partitioned cache | Self-host |
| Faux-bold appears | Weight declared but file not loaded | Load the weight or restrict usage |

## 6. Evaluation procedure

1. Inventory every `@font-face` and every weight/style **actually rendered**.
   Delete the difference.
2. Confirm WOFF2 and that legacy formats are gone.
3. Confirm `font-display` is set explicitly on every face.
4. Throttle to slow 3G and reload. Is text readable immediately? Does it swap?
5. Measure CLS with and without the webfont. Attribute the delta.
6. If swap CLS > 0, build a metric-matched fallback and re-measure.
7. Verify `preload` has `crossorigin` and covers only critical files.
8. Test with fonts **blocked entirely** — the page must remain usable.
9. Test the fallback stack renders acceptably on its own.

## 7. Output format

```
Families/weights shipped: <n> — rendered: <n> — removed: <list>
Format: WOFF2 <yes/no> · legacy removed: <yes/no>
font-display: <value> — because <reason>
Preload: <files> — crossorigin: <yes/no>
Fallback: <stack> — metric-matched: <yes/no>
CLS: before <n> → after <n> (font-attributed: <n>)
Subset: <ranges> — verified against real content: <yes/no>
Tested: slow-3G <pass/fail> · fonts-blocked <pass/fail>
```

## 8. Examples

**Marketing site, Inter at 4 weights, CLS 0.18 mostly from text.**

> Replaced the four static files with one variable Inter (smaller in total), set
> `font-display: swap`, preloaded the single variable file with `crossorigin`, and
> added an Arial-based fallback face with `size-adjust: 107%` plus ascent/descent
> overrides tuned to Inter's metrics. CLS dropped to 0.02, with the font-attributed
> component at 0.00. Verified with fonts blocked: the page reads correctly in the
> fallback.

**Docs site where CLS matters more than first-visit branding.**

> `font-display: optional`. First visit renders in the fallback and never swaps, so
> swap CLS is structurally impossible; the webfont is cached and used from the
> second visit on. Acceptable because the docs' value is the text, not the face.

## 9. Counterexamples

- ❌ "Use Web Font Loader to manage loading." — Obsolete. `font-display` and the
  CSS Font Loading API cover this natively.
- ❌ "Google Fonts is faster because of shared caching." — Cross-site font cache
  sharing ended when browsers partitioned the HTTP cache by origin.
- ❌ "`font-display: block` so users only ever see the real font." — That's FOIT;
  it hides content for a font.
- ❌ "Preload every font file for speed." — Preloads compete; over-preloading
  delays render.
- ❌ `<link rel="preload" as="font">` without `crossorigin` — downloads twice.
- ❌ "CLS is 0.05, fonts are fine." — Measure the font-attributed component; a
  small total can still hide a full-width text shift.
- ❌ "Subset to Latin-basic to save bytes." — Breaks on real names and currency.

## 10. Source citations

- **Current standards take precedence here.**
  MDN — [`font-display`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display),
  [`size-adjust`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust),
  [`ascent-override`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/ascent-override),
  [`unicode-range`](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range).
  [web.dev — optimize web fonts](https://web.dev/learn/performance/optimize-web-fonts).
  [Chrome for Developers — improved font fallbacks](https://developer.chrome.com/blog/font-fallbacks).
- Rutter, *Web Typography* — FOIT and FOUT defined and named; the tradeoff between
  them; font loading strategy; the general one-second usable-page target; the
  five `font-display` values and their behavior (**still accurate**, only the
  "nascent/experimental support" framing is obsolete); recommending `fallback`
  over `swap` for body text specifically; choosing a fallback system font by
  x-height, horizontal metrics, then G/W/a/y/g letterform comparison, before
  applying metric overrides. **Its Font Loading API / `wf-active` class
  workaround is obsolete** now that `font-display` has universal support.
- Santa Maria, *On Web Typography* — FOUT; severity scales with how far the webfont
  diverges from the fallback (still true, and the basis for metric matching).
  **Its Web Font Loader recommendation is obsolete.**
- Latin, *Better Web Typography* — FOUT/FOIT tradeoff; why hiding text is dangerous
  when the font never arrives.
- Brown, *Flexible Typesetting* — managing fallback font transitions as a design
  concern, not only a performance one.
