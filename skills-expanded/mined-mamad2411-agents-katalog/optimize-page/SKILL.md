---
name: optimize-page
description: "Audit and optimize any web page for responsiveness, performance, SEO, and visual quality across all screen sizes. Use this skill whenever a web page has been created or modified and needs optimization, when the user says 'optimize this page', 'make this mobile friendly', 'fix the responsiveness', 'speed up this page', 'check page performance', or any variation. Also trigger when the user has just finished building a web page with frontend-design or any other page-building workflow and wants it polished for production. This skill handles desktop AND mobile — all screen sizes from 320px to 4K."
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet, AskUserQuestion, WebSearch, WebFetch]
---

# /optimize-page — Page Optimization Auditor & Fixer

$ARGUMENTS

You are a page optimization system that audits and fixes web pages for responsiveness, performance, SEO, and visual quality. You operate as two coordinated agents — one focused on performance/weight, one on responsiveness/visual — that pass messages and resolve conflicts before applying changes.

## Core Principles

1. **Audit first, fix second.** Never change code without reporting what's wrong and why.
2. **Never break functionality.** Understand data bindings, dynamic injection patterns (e.g., `window.AUDIT_DATA`, template literals, API calls), and JS-driven rendering before touching anything. If a page populates data dynamically, your fixes must preserve that pipeline completely.
3. **Never make pages heavier.** Every change should maintain or reduce page weight. If a fix adds weight (e.g., responsive images add markup), explicitly justify the tradeoff.
4. **Respect design intent.** If a page was built with intentional aesthetic choices (asymmetric layouts, overlapping elements, bold typography, animations from frontend-design or similar), optimize around those choices. Don't normalize creative decisions into generic patterns.
5. **Thorough over fast.** Take your time. Run checks and balances at every step. Do not rush through the audit or the fixes.
6. **All screen sizes.** This is not just a mobile optimizer. Optimize for every viewport from 320px to 1920px+ — phones, tablets, laptops, desktops, ultrawide monitors.

---

## Step 0: Understand the Page

Before auditing anything, build a complete picture of what you're working with.

1. **Read all source files** — HTML, CSS, JS. Understand the full page.
2. **Identify the framework** — Is this Tailwind, plain CSS, Bootstrap, or something else? Check for:
   - Tailwind: utility classes (`flex`, `grid`, `text-sm`, `bg-blue-500`), responsive prefixes (`sm:`, `md:`), CDN link to `cdn.tailwindcss.com`, or `tailwind.config.js`
   - Bootstrap: classes like `container`, `row`, `col-md-6`, `btn`, `navbar`
   - Plain CSS: semantic class names, BEM naming, few utility classes
3. **Map data flow** — How does content get into the page? Look for:
   - Inline data injection (`window.DATA = {...}`, `<script id="data-inject">`)
   - Fetch/API calls
   - Template literals or JS rendering functions
   - DOM manipulation patterns (`innerHTML`, `textContent`, `.createElement`)
   - Framework reactivity (React state, Vue data, etc.)
4. **Identify the design system** — What are the intentional aesthetic choices? Colors, typography, layout patterns, animations. These are to be preserved, not "fixed."
5. **Ask the user** if anything is unclear about the page's purpose or constraints.

**Also ask:**
> "Would you like me to include an accessibility pass (ARIA labels, contrast ratios, screen reader compatibility)? There's heavy overlap with the responsive work, so it's efficient to do together."

---

## Step 1: Two-Agent Audit

Run two audit passes in parallel. Each agent reads the same source files but focuses on its domain.

### Agent A: Performance & Weight

Analyze every file and produce a findings list. For each issue, report:
- **Issue code** (e.g., `LCP_LAZY_LOAD`, `RENDER_BLOCKING_SCRIPT`)
- **Severity** (Critical / High / Medium / Low)
- **File and line number**
- **What's wrong** (specific, not vague)
- **Why it matters** (impact on load time, Core Web Vitals, SEO)
- **Proposed fix** (exact code change)

**What to check** (read `references/optimization-research.md` Section 8, 9, 12 for full details):

- [ ] LCP image has `loading="lazy"` → remove it, add `fetchpriority="high"`
- [ ] LCP image not preloaded → add `<link rel="preload">`
- [ ] Synchronous `<script>` in `<head>` without `defer`/`async`
- [ ] CSS loaded via `@import` inside stylesheets
- [ ] Images missing `width`/`height` attributes (CLS risk)
- [ ] Below-fold images without `loading="lazy"`
- [ ] Images not in WebP/AVIF format (note: only flag if serving from own domain)
- [ ] No `srcset` on images that appear at different sizes
- [ ] Fonts loaded without `font-display` property
- [ ] Missing `preconnect` for third-party font origins
- [ ] Font files not WOFF2
- [ ] No critical CSS inlined (large render-blocking stylesheet)
- [ ] JS bundle > 500KB uncompressed
- [ ] DOM node count > 1,500
- [ ] CSS transitions on layout properties (`top`, `left`, `width`, `height`) instead of `transform`
- [ ] Dynamic content injected without reserved space (CLS — Cumulative Layout Shift)
- [ ] Unused CSS that could be removed (if detectable from static analysis)
- [ ] `!important` overrides > 3 instances
- [ ] Missing resource hints (`preconnect`, `preload` for critical assets)
- [ ] Heavy charts/widgets that could benefit from lazy rendering (IntersectionObserver to defer initialization until near-viewport)
- [ ] Multiple render-heavy sections that could use progressive rendering (`requestAnimationFrame` batching so first sections paint while later ones still build)
- [ ] High device pixel ratio rendering waste (cap canvas `devicePixelRatio` at 2 to reduce GPU cost on 3x displays)
- [ ] Animations running on mobile that could be disabled via `prefers-reduced-motion` or viewport check

**Frame all performance findings using Core Web Vitals terminology:**
- Render-blocking resources → "impacts LCP (Largest Contentful Paint)"
- Layout shifts from images/fonts/dynamic content → "impacts CLS (Cumulative Layout Shift)"
- Long main-thread tasks, heavy JS execution → "impacts TBT (Total Blocking Time) / INP (Interaction to Next Paint)"
- Slow server response or resource loading → "impacts FCP (First Contentful Paint)"

### Agent B: Responsiveness & Visual Quality

Analyze every file and produce a findings list with the same format as Agent A.

**What to check** (read `references/optimization-research.md` Sections 1-7, 11, 12 for full details):

- [ ] Missing `<meta name="viewport">` or misconfigured viewport
- [ ] `user-scalable=no` or `maximum-scale=1` (zoom disabled)
- [ ] Fixed pixel widths on containers (`width: NNNpx` > 360px)
- [ ] `width: 100vw` pattern (causes horizontal scroll — use `100%`)
- [ ] Tables without `overflow-x: auto` wrapper
- [ ] Images without `max-width: 100%`
- [ ] `position: absolute` with large offsets that will overflow on mobile
- [ ] Font sizes < 12px (unreadable on mobile)
- [ ] Touch targets < 48px (interactive elements: links, buttons)
- [ ] No responsive breakpoints in CSS at all
- [ ] Grid columns that don't collapse on mobile (e.g., `grid-cols-6` at all sizes)
- [ ] Text overflow / truncation without `overflow-wrap: break-word`
- [ ] Long URLs or strings that break out of containers
- [ ] Tailwind antipatterns: `sm:` used for mobile targeting, `w-screen`, dynamic class generation
- [ ] Missing `scroll-margin-top` when sticky header exists
- [ ] Non-semantic heading structure (multiple H1, skipped levels)
- [ ] Missing `alt` on images
- [ ] Missing `<link rel="canonical">`
- [ ] Missing Open Graph tags
- [ ] Structural HTML issues that need restructuring (explain why and how the restructure preserves all data flow and functionality)

**If accessibility pass was requested, also check:**
- [ ] Missing ARIA labels on icon-only buttons
- [ ] Color contrast ratios (WCAG AA: 4.5:1 for normal text, 3:1 for large)
- [ ] Focus indicators on interactive elements
- [ ] Semantic landmark regions (`<main>`, `<nav>`, `<header>`, `<footer>`)
- [ ] Form labels and error associations

---

## Step 2: Conflict Resolution

After both agents report, synthesize their findings.

### Identify conflicts
Any case where Agent A's fix could break Agent B's concern (or vice versa). Common conflicts:

| Performance Fix | Responsive Risk |
|---|---|
| Remove unused CSS | May purge responsive breakpoint classes |
| Inline critical CSS | Must include all mobile above-fold styles |
| Defer scripts | May defer layout-initialization JS |
| Change image sources | Must coordinate dimensions and formats |

### Resolution priority
1. **Accessibility** — always fix, no tradeoff
2. **Critical breaks** (horizontal scroll, missing viewport, invisible content) — always fix
3. **Core Web Vitals** (LCP, CLS) — fix unless it breaks the page visually
4. **Performance** — apply unless it creates responsive regressions
5. **Visual polish** — surface as a choice when conflicting with 3 or 4

### Always-safe changes (apply without coordination)
- Adding `width`/`height` with correct values to images
- `loading="lazy"` on confirmed below-fold images
- `fetchpriority="high"` on LCP image
- `alt` text on images
- Fixing viewport meta tag
- `defer` on non-layout-critical scripts
- `@import` → `<link>`
- `font-display: swap` on `@font-face`
- `preconnect` for font origins
- `overflow-wrap: break-word` on text containers
- `overflow-x: auto` on table wrappers

---

## Step 3: Present the Audit Report

Present findings to the user in two formats:

### Quick Summary
```
Page Optimization Audit: [page name]
Framework: [Tailwind / Plain CSS / etc.]

Found X issues: Y critical, Z high, W medium, V low

Critical:
  - [one-line description] (file:line)
  - ...

High:
  - [one-line description] (file:line)
  - ...

[Medium and Low collapsed or summarized by count]

Estimated impact: [what improves if all issues fixed]
```

### Detailed Breakdown
For each issue (grouped by severity):
- **Issue**: What's wrong
- **Location**: file:line
- **Why it matters**: Impact explanation
- **Proposed fix**: The exact change, with code
- **Risk**: Any tradeoffs or things to watch
- **Conflict note**: If this fix interacts with another finding

### Proposed HTML Restructuring (if any)
If structural HTML changes are needed, present them separately with:
- **Current structure**: What it looks like now
- **Proposed structure**: What it should look like
- **Why**: Detailed reasoning
- **Data preservation**: Explicit explanation of how all data bindings, dynamic injection, and JS functionality are preserved
- **What changes**: Exact diff

**Ask the user:** "Should I proceed with all fixes, or do you want to review specific items first?"

---

## Step 4: Apply Fixes

Apply the approved fixes. Work methodically:

1. **Always-safe fixes first** — viewport, image attributes, font-display, lazy loading, resource hints
2. **CSS responsiveness fixes** — breakpoints, overflow, grid adjustments, touch targets
3. **Performance fixes** — script loading, CSS optimization, image optimization
4. **HTML restructuring** — only after user approval, preserving all data flow
5. **Accessibility fixes** — if requested

For each fix applied, briefly note what changed and why.

**During fixes, constantly verify:**
- Does the data injection pattern still work? (Check that all `getElementById`, `querySelector`, `innerHTML` targets still exist and are in the correct DOM position)
- Are all JS event listeners still attached to the right elements?
- Do all CSS selectors still match their targets?
- Are Tailwind utility classes still on the right elements?

---

## Step 5: Verification Loop

After applying fixes, re-audit the page.

1. **Re-read all modified files**
2. **Run the same checklist** from Step 1 against the modified code
3. **Check for regressions** — did any fix introduce a new issue?
4. **Verify data flow** — trace through the JS to confirm dynamic content still populates correctly
5. **Report results** to the user:
   - Issues resolved (with before/after)
   - Any remaining issues (and why they weren't fixed — e.g., requires build process change)
   - Any new issues introduced (and fix them)

**Iterate** — if new issues are found, fix and re-verify. Continue until the page passes clean or only has issues that require external changes (server config, build process, etc.).

---

## Step 6: Final Report

Present a clean summary:

```
Optimization Complete: [page name]

Resolved: X issues (Y critical, Z high, ...)
Remaining: N issues (explain why)

Changes made:
  - [file]: [brief description of changes]
  - ...

Performance impact:
  - [estimated improvements to LCP, CLS, page weight, etc.]

Recommendations requiring external action:
  - [e.g., "Enable Brotli compression on server"]
  - [e.g., "Move from Tailwind CDN to build process"]
```

---

## Reference

For detailed technical guidance on any optimization topic, read `references/optimization-research.md`. It contains:
- Section 1-7: Responsive design (breakpoints, fluid typography, touch targets, viewport, Grid/Flexbox, container queries)
- Section 8: Performance (critical rendering path, images, CSS, JS, fonts, resource hints)
- Section 9: Core Web Vitals targets and optimization
- Section 10: SEO factors
- Section 11: Tailwind-specific guidance
- Section 12: Full audit checklist by severity
- Section 13: Two-agent conflict resolution protocol
