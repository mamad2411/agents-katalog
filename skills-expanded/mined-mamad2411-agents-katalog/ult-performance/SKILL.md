---
name: ult-performance
description: Default router for the ult-performance plugin. Routes web performance, Core Web Vitals, loading, interaction, media, animation, Vite/bundle, accessibility, SEO, and quality-audit work to the matching specialist skill(s). Use when asked to optimize performance, speed up a site, audit a page, check web vitals, debug LCP/INP/CLS/TTFB/jank, run Lighthouse, or when the request spans more than one performance area. Also use for /ult-performance.
license: MIT
metadata:
  author: ult-performance
  version: "1.0.0"
  category: web-performance
---

# Ult Performance router

Load this skill first. Then load only the specialist skills the table names. Do not stay in the router after routing.

Read [execute-snippets.md](../../references/execute-snippets.md) before measuring anything in a browser.

## Route

Match the user request. Load every matching specialist. Ambiguous "make it fast" / "audit this page" uses the default row.

| Request | Load | Then |
|---------|------|------|
| Audit / Lighthouse / web quality / review this site | `audit` | Follow its category split |
| LCP, INP, CLS, Core Web Vitals, layout shift, slow hero | `core-web-vitals` | Measure, then fix from its references |
| TTFB, FCP, render-blocking, fonts, scripts, hints, bfcache, SSR hydration, save-data, slow 3g | `loading` | Run its workflow and decision tree |
| Jank, INP debug, long tasks, LoAF, scroll, 60fps, GSAP, will-change, GPU, layout thrash | `interaction` | Measure, then apply animation rules |
| Sticky / pinned sections, scrollytelling, parallax, scroll-linked animation build or repair, scroll jank from scroll-UI architecture | `scroll` + `interaction` for runtime measurement | Classify interaction, pick least-complex architecture, measure scroll with `interaction` snippets |
| Images, video, SVG, srcset, lazy-load, AVIF/WebP | `media` | Audit elements, then optimize |
| Speed up / bundle / Vite / cache / third-party / budgets / only source available | `performance` | Measure if a URL exists; otherwise hypothesis + verify steps |
| a11y, WCAG, keyboard, screen reader | `accessibility` | Live Lighthouse a11y + manual checks |
| SEO, meta, sitemap, schema, crawl | `seo` | Live Lighthouse SEO + crawl/index checks |
| Security headers, CSP, deprecated APIs, mixed content | `best-practices` | Live Lighthouse best-practices + headers |
| Default (broad or mixed) | `audit` + `core-web-vitals` | Add `loading` / `interaction` / `media` from the first failures |

If two specialists disagree, field p75 wins on impact; the trace/snippet wins on cause.

## Hard rules

1. **Measure before changing code** when a URL or running app exists.
2. **Label evidence:** field, lab, snippet, or hypothesis. Never mix them in one number.
3. **Fix the traced bottleneck**, not a generic checklist.
4. **Re-measure** the same lab path after a fix. Do not claim field CWV improved until new CrUX/RUM exists.
5. **Mobile lab by default** for public sites unless the product is desktop-only.

## Thresholds (field p75 = pass/fail)

| Metric | Good | Needs work | Poor |
|--------|------|------------|------|
| LCP | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |
| TTFB (lab diagnostic) | ≤ 800ms | ≤ 1800ms | > 1800ms |
| FCP (lab diagnostic) | ≤ 1.8s | ≤ 3.0s | > 3.0s |

Animation lab targets live in `interaction`: 60fps, JS/layout < 10ms/frame.

`interaction` owns runtime measurement (traces, snippets, LoAF, long tasks). `scroll` owns scroll-UI architecture and implementation (sticky, scrollytelling, parallax, observer vs CSS timelines vs Motion vs GSAP choice).

Starting transfer budgets (override with a project budget if one exists) live in `performance`.

## Output

```markdown
## Evidence
| Signal | Scope/conditions | Result | Source |
|--------|------------------|--------|--------|
| LCP | URL, phone, p75/28d | 3.1s needs improvement | CrUX |

## Findings
- **[skill]** Issue. File: `path:line`
  - Impact:
  - Evidence: field | lab | snippet | hypothesis
  - Fix:

## Next specialist
- skill-name — why
```

## Specialists

| Skill | Path |
|-------|------|
| audit | `../audit/SKILL.md` |
| core-web-vitals | `../core-web-vitals/SKILL.md` |
| loading | `../loading/SKILL.md` |
| interaction | `../interaction/SKILL.md` |
| scroll | `../scroll/SKILL.md` |
| media | `../media/SKILL.md` |
| performance | `../performance/SKILL.md` |
| accessibility | `../accessibility/SKILL.md` |
| seo | `../seo/SKILL.md` |
| best-practices | `../best-practices/SKILL.md` |
