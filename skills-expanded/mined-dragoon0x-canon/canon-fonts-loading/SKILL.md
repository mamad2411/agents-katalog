---
name: canon-fonts-loading
description: Use when selecting, loading, or optimizing web fonts — font-display strategy, preloading, subsetting, variable fonts, FOUT/FOIT handling, and limiting font file count. Trigger when the user mentions web fonts, font loading, font-display, @font-face, Google Fonts, preload fonts, FOUT, or FOIT.
---

# CANON · Font Loading

Fonts block rendering by default. Control the loading strategy or the browser controls it for you, badly.

## font-display — always declare it

```css
@font-face {
  font-family: 'Geist';
  src: url('geist.woff2') format('woff2');
  font-display: swap;
}
```

| Value | Behavior | Use |
|---|---|---|
| `swap` | Show fallback immediately, swap when loaded | **Default for body text** |
| `optional` | Show fallback; use custom font only if already cached | Performance-critical pages |
| `block` | Invisible text for up to 3s | Never for body; acceptable for icon fonts |
| `fallback` | 100ms invisible, then fallback, swap if loaded within 3s | Good middle ground |

`font-display: swap` is the CANON default. `optional` for ultra-fast pages.

## Preload critical fonts

```html
<link rel="preload" href="/fonts/geist-regular.woff2" as="font" type="font/woff2" crossorigin>
```

Preload only the critical weight (regular body text). Don't preload every weight — that defeats the purpose.

## Limit font families and weights

| Budget | Reason |
|---|---|
| 1–2 font families | Visual consistency, reduced HTTP requests |
| 2–3 weights per family | Most UIs need regular + medium + bold at most |
| Total font files ≤ 4–6 | Each file is a blocking or swap-flashing resource |

Variable fonts reduce file count: one file covers all weights.

## WOFF2 only

WOFF2 is supported by every modern browser and is 30% smaller than WOFF. Don't serve TTF, OTF, or WOFF to browsers — WOFF2 only (with WOFF fallback if you must support very old browsers).

## Subsetting

If you only use Latin characters, subset the font to remove CJK, Cyrillic, etc. Tools: `pyftsubset`, Google Fonts `&subset=latin`, `glyphhanger`.

A full Noto Sans is 20MB. Latin-subset is 20KB. Subsetting matters.

## Reducing FOUT (Flash of Unstyled Text)

- Match the fallback font's metrics to the custom font: `size-adjust`, `ascent-override`, `descent-override`.
- Tool: `fontaine` generates these values automatically.

```css
@font-face {
  font-family: 'Geist Fallback';
  src: local('Arial');
  size-adjust: 100.5%;
  ascent-override: 96%;
  descent-override: 24%;
}
```

## Self-host vs CDN

Self-hosting is faster (same origin, no DNS lookup, no cross-origin overhead). Google Fonts is convenient but adds a DNS lookup + connection to `fonts.gstatic.com`.

Self-host when performance matters. Use Google Fonts for prototyping.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| No `font-display` (defaults to `auto` → invisible text) | FOIT for up to 3 seconds |
| Preloading 6 font files | Wastes bandwidth on non-critical weights |
| Serving TTF/OTF to browsers | Larger files, WOFF2 is smaller and universal |
| 4 font families on one page | 12+ files, inconsistent visual identity |
| No subsetting for Latin-only site | Shipping CJK glyphs nobody uses |
| Google Fonts in production without self-hosting option | Extra DNS + connection latency |

## Audit checklist

- [ ] `font-display: swap` or `optional` on all @font-face
- [ ] Critical font weight preloaded
- [ ] ≤ 2 font families
- [ ] ≤ 3 weights per family
- [ ] WOFF2 format only
- [ ] Subset to character ranges actually used
- [ ] Fallback font metrics matched to reduce FOUT
- [ ] Total font payload ≤ 100KB

## Sources

- web.dev · "Best practices for fonts"
- `canon-typography` for font selection rules
- `canon-performance` for Core Web Vitals targets
- Zach Leatherman · "A Comprehensive Guide to Font Loading Strategies"
