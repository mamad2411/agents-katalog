# Mobile-Responsive Web Design

## Summary

**One-sentence:** Produces mobile-first CSS (320px baseline up to 1920px) with viewport meta, fluid type via clamp(), CSS Grid layout, >=44x44px tap targets, no fixed pixel widths above 1px borders, and a multi-viewport Playwright verification step.

**One-paragraph:** Mobile-first CSS design: start at 320px and enhance for larger viewports via `min-width` media queries. Use relative units (rem, %, clamp()), CSS Grid/Flexbox for layout, viewport meta tag, and tap targets >= 44x44px (WCAG 2.5.5). On iOS use `100dvh`/`svh`/`lvh` instead of `100vh`. No hover-only interactions; provide touch equivalents. Verification: Playwright screenshots at 360/768/1280/1920, Lighthouse mobile perf > 85, axe-core a11y > 95.

**Ефективно для:** any public-facing web UI, audits after redesigns, Tailwind/Storybook component libraries, email/embed snippets, replacing desktop-first stylesheets that accumulated mobile override debt.

## Applies If (ALL must hold)

- Web UI (HTML/CSS), not native mobile or print.
- Audience uses mobile devices (most public products).
- Build pipeline can run Playwright + Lighthouse in CI.
- Designs available or describable in mobile-first form.

## Skip If (ANY kills it)

- Internal admin tool on fixed-resolution kiosk.
- Embedded WebView pinned to one viewport (Telegram WebApp).
- Print stylesheet / PDF generator.
- Native mobile (React Native / Flutter / SwiftUI) — different layout primitives.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Design tokens / Figma | URL / png | designer |
| Breakpoint targets | list (360/768/1280/1920) | product brief |
| Touch-target audit list | bullet list | a11y review |
| Lighthouse thresholds | int (perf=85, a11y=95) | infra/SRE ADR |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `[[javascript]]` | TS conventions for the React component layer. |
| `[[e2e-testing]]` | Playwright drives the viewport verification step. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 rules: mobile-first, viewport meta, clamp() typography, no fixed px, tap targets, dvh on iOS, no hover-only | ~700 |
| `content/02-output-contract.xml` | essential | Required CSS invariants + Playwright assertions | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: fixed pixel widths, desktop-first, hover-only, 100vh on iOS | ~600 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~700 |
| `content/06-decision-tree.xml` | essential | Root: "Is this a public-facing web UI?" | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Generate component CSS | sonnet | Pattern-driven. |
| Audit existing CSS | sonnet | Grep + lint. |
| Visual-diff triage | opus | Multimodal reasoning. |

## Templates

| File | Purpose |
|------|---------|
| `templates/responsive-check.ts` | Playwright script — screenshot at 360/768/1280/1920, assert no horizontal scroll, tap targets >=44px. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mobile-responsive.py` | Greps CSS for fixed pixel widths > 1px, 100vh on iOS-targeted blocks, hover-only handlers. | Pre-commit gate. |

## Related

- parent skill: `free/dev/software-developer/`
- `[[e2e-testing]]` — Playwright verification harness
- `[[javascript]]` — React + Tailwind conventions

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters: web UI yes/no, public/multi-device yes/no, build can run Playwright yes/no.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/responsive-check.ts`

```typescript
/**
 * responsive-check.ts — Playwright script for multi-viewport screenshot and overflow detection.
 * Usage: npx ts-node scripts/responsive-check.ts http://localhost:3000
 * Output: screenshots in out/<viewport-name>.png, console errors on horizontal overflow.
 */
import { chromium, devices } from "@playwright/test";
import * as fs from "fs";

const viewports = [
  { name: "iphone-se", ...devices["iPhone SE"] },
  { name: "ipad", ...devices["iPad Pro 11"] },
  { name: "desktop", viewport: { width: 1280, height: 800 } },
];

const url = process.argv[2] ?? "http://localhost:3000";

(async () => {
  if (!fs.existsSync("out")) fs.mkdirSync("out");
  const browser = await chromium.launch();

  for (const v of viewports) {
    const ctx = await browser.newContext(v as Parameters<typeof browser.newContext>[0]);
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready);

    await page.screenshot({ path: `out/${v.name}.png`, fullPage: true });

    const overflow = await page.evaluate(
      () => document.body.scrollWidth > window.innerWidth,
    );
    if (overflow) {
      console.error(`FAIL: horizontal scroll detected at ${v.name}`);
    } else {
      console.log(`OK: ${v.name}`);
    }
    await ctx.close();
  }

  await browser.close();
})();
```
