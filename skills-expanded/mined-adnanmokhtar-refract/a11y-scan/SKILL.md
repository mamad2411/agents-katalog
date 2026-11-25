---
name: a11y-scan
description: "Rendered WCAG 2.2 AA detector: one axe recipe per route × state × theme, plus keyboard, focus, reflow and target-size probes."
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash, Write]
---

# Skill: a11y-scan

## Premise

This is the rendered half of WCAG 2.2 AA. `a11y-code-scan` (this pack) finds defects in source. This skill renders the routes of a production build and proves what only a browser shows: the axe floor at every route × state × theme × viewport, the menus and dialogs opened, contrast in both themes, focus visible and not obscured along a real Tab walk, target size, reflow, text spacing, and whether the project's own a11y gate can fail at all.

**Every finding cites the axe rule id or the probe + the node selector + the source `<file:line>` that renders it + the route-state + the WCAG 2.2 SC and level + the fix in the project's own components.** "No issues" is never printed. The output is a class-coverage block and the automated-floor line: automation finds part of the problem, 57 % of issues by volume in Deque's study and 41 % of 143 barriers for the best single tool in the GDS test (`ui § 58`).

**Three render states, never collapsed** (the `visual-check` contract): `SKIPPED (no harness)` when nothing can render; `RENDER BLOCKED` when a harness exists but the cell landed on a login wall, the wrong theme or the wrong language, which halts that lane; and a rendered cell. A § whose oracle got no render is `blocked (no harness)`, never `checked`.

Below, `ui § n` is [`precedents/ui.md`](../../../../snippets/precedents/ui.md) § n, V-numbers are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states, and a bare `§n` is a class in this skill.

## The rule

A rendered result is a finding when all four hold:

1. **The cell is real.** The route rendered its surface-unique marker, and the theme and `lang` the page drew match the cell (read back, not assumed). A login wall, a 403 or an un-applied theme is `RENDER BLOCKED`, never a clean cell.
2. **A user reaches the state.** The route is in the route table, and the opened surface or UI state is one a user can reach.
3. **The oracle fired at that cell.** An axe rule id has a violation node there, or a probe failed (Tab walk, focus delta, obscured rect, geometry, reflow, spacing, injected violation).
4. **No precedent excuses it, and the node traces to source.** `ui § 11–34` exceptions are checked, and the selector is mapped to the component `<file:line>` that renders it (one finding per component or wrapper, `ui § 9`).

## Boundaries

- **Static classes** belong to `a11y-code-scan`: non-semantic controls, names in source, focus styles in CSS, dialog focus code, route-change wiring, error association, ARIA in templates. Its §1, §4, §5 and §9 candidates are settled here: the §4 Tab walk is their bulk oracle. Its old riders (zoom lock, `<html>` without `lang`, orientation lock) are this skill's: grep 6 reports them as static facts, and §1 and §6 confirm them at a cell.
- **UI states** — `ui-state-scan` (ui-ux pack, when installed) owns which states exist. Its state handlers (MSW or `page.route` fulfilling `[]`, 500, 403, offline) are how §1 and §3 reach the error, empty and forbidden cells. Without ui-ux, cells are loaded + opened only, and state cells print `N/A (owner pack ui-ux not installed)`.
- **Motion** (2.2.2, reduced motion) → `motion-audit` (ui-ux pack, when installed). The axe rules `blink`, `marquee` and `no-autoplay-audio` stay in §1.
- **Contrast token pairs** → `design-token-audit`; the visual fixes are `ui-design-sweep` verbs 12 (lift-contrast), 13 (align-focus-ring), 16 (expand-tap-target) and 18 (clarify-affordance), both ui-ux, when installed. Without ui-ux the fix is written here in the project's own tokens.
- **Native mobile trees** → `mobile-a11y-scan` (mobile pack, when installed). Without it they print `N/A (native UI — not a DOM)`; DOM tooling on a native tree proves nothing.
- **The judge** is `@ux-reviewer` (ui-ux pack) when installed, else `@accessibility-auditor` (this pack). This skill is the rendered detector both consume.
- **Not this skill:** a Lighthouse accessibility score (`ui § 51`; `@lhci/cli` 0.15.1 still bundles Lighthouse 12.6.1); UI test quality beyond the a11y gate (testing pack).

## Harness — what this skill needs and what it writes

- **A production build**, served the way the lane table says, started or reused through `dev-server-start`. A dev server adds dev-only overlays and markup, which pollute §4.
- **The session** follows `visual-check`: `tests/.auth/user.json`, written by an auth setup project. `storageState` sits under the project's `use:`, not at the project's top level, where Playwright does not apply it. **Auth-success gate first:** load a known authenticated route and assert the final URL is not the login path (`/login` or the project's own) and a post-auth marker is visible. Otherwise `RENDER BLOCKED`.
- **Write mode** (Setup, a fix command, a user asking for the gate): it writes the probe module and the cell spec into the project's Playwright `testDir`, **named to its `testMatch`** (grep 0b). Measured on a real repo: its Playwright suite matches only `*.flow.ts`, because Vitest claims every `*.spec.ts` and would run it in jsdom. An `a11y.spec.ts` there never runs in a browser. It also writes per-cell evidence JSON through `testInfo.attach` into `test-results/` (gitignored), and a baseline file only when asked to record one. It never edits product code, and it prints any Playwright config change as a diff before writing it.
- **Judge mode** (dispatched by `@ux-reviewer` or any caller without Write): nothing is written in the repo. The same module and spec go in a scratch dir under `$TMPDIR` (the scratch-dir rule for judges in [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10, gate 6), with `@playwright/test` pinned to the project's version, `@axe-core/playwright@4.13.0` and a config whose `use.baseURL` and `use.storageState` point at the served app and the session file. Run it with `npx --no playwright test -c <scratch>`. The report is returned, not saved.

## Adapt to the codebase — lane table

Read every version from the lockfile and print the lanes in the output header.

| Lane | Serve the production build | Built-in that changes a row | Existing a11y harness to reuse and audit (§7) |
|---|---|---|---|
| **React + Vite / React Router 7** | `vite build && vite preview` | no route announcer (`ui § 27`) | Storybook `@storybook/addon-a11y` 10.6 (`a11y.test: 'error'` is the only value that fails CI) |
| **Next.js** | `next build && next start` | App Router route announcer (`ui § 27`) | same; `@axe-core/playwright` specs |
| **Vue 3 / Nuxt 4** | `vite build && vite preview` · `nuxi build && nuxi preview` | `<NuxtRouteAnnouncer>` only when placed in `app.vue` | `cypress-axe` 1.7.0: an `includedImpacts` filter hides issues |
| **SvelteKit** | `vite build && vite preview` | announcer + focus reset to `body` | — |
| **Angular 20–22** | `ng build`, then a static server over `dist/<app>/browser` | CDK `cdkTrapFocus`, Material dialog | — |
| **Solid / Qwik / Lit / plain HTML / SSG** | a static server over the build output | — | `jest-axe` 11 / `vitest-axe` 0.1 run in jsdom: no layout, so contrast, target size and reflow can never run there |
| **Other runners** | `@axe-core/cli` 4.13 (flags [K]), `pa11y` 10 (`--runner axe`; HTML_CodeSniffer disagrees with axe, so pick one engine per baseline) | — | Lighthouse 13.5 is a subset, not axe (`ui § 51`) |

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds **§N**; grep 0 is context. Every `rg` names its path. Test, story, config, script and CI files are **in** scope for 0c and 7, and hidden dirs (`.storybook/`, `.github/`) need `--hidden`. An rg exit 2 is a failed grep, never zero hits. Never use `rg -L` (it means `--follow`).

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|@builder\.io/qwik|lit)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.angular,coverage,storybook-static}/**' -g '!**/docs/**' -g '!/ai/**' -g '!**/*.min.*')
S=(-g '*.{jsx,tsx,vue,svelte,astro,html,css,scss,sass,less,pcss,ts,js,mjs}' -g '!**/*.{test,spec,stories,story,e2e,flow,d}.*' -g '!**/{test,tests,__tests__,__mocks__,mocks,e2e,fixtures,playwright,cypress,scripts}/**' -g '!**/{locales,locale,i18n,translations}/**')
T=(--hidden -g '*.{ts,tsx,js,jsx,mjs,cjs,vue,svelte,json,yml,yaml}' -g '!.git/**' -g '!**/package.json' -g '!*.lock' -g '!**/{locales,locale,i18n,translations}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--|#(?!\{))')   # drops comment-only lines
# 0a tool versions; 0b the Playwright harness (testDir/testMatch name the file §1 writes); 0c every place axe already runs;
# 0d how a cell sets dark and RTL, and how to read back what the page drew.
rg -n --no-heading --pcre2 '"(?:axe-core|@axe-core/(?:playwright|cli|react|puppeteer|webdriverjs)|@playwright/test|playwright|@storybook/addon-a11y|@storybook/addon-vitest|@storybook/test-runner|cypress-axe|jest-axe|vitest-axe|axe-playwright|pa11y(?:-ci)?|lighthouse|@lhci/cli|@guidepup/[\w-]+)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --pcre2 '\b(?:testDir|testMatch|storageState|webServer|baseURL)\b' -g '**/playwright.config.*' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'new AxeBuilder\b|\baxe\.run\(|\bcheckA11y\(|\binjectAxe\(|toHaveNoViolations|configureAxe\(|axe-core/[\d.]+/axe|addon-a11y|\ba11y\s*:\s*\{|categories:accessibility' "${T[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'prefers-color-scheme|\bdata-theme\b|classList\.(?:add|toggle|remove)\(\s*["\x27]dark\b|darkMode\s*:|@custom-variant\s+dark|documentElement\.(?:dir|lang)\s*=|\bdir\s*=\s*["\x27]rtl' "${S[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. Interactive-surface triggers in source (union with the DOM pass in §2). Add the project's own menu/dialog wrapper names.
rg -n --pcre2 'aria-haspopup|aria-expanded|aria-controls|role=["\x27]tab["\x27]|<details\b|<dialog\b|popovertarget' "${S[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. 2.4.11 context: pinned layers (full-cover scrims and off-screen print helpers dropped), and whether scroll padding is reserved.
rg -n --pcre2 'position\s*:\s*["\x27]?(?:fixed|sticky)\b|(?<![\w:-])(?:fixed|sticky)\b(?=[^"\x27`\n]*\b(?:top|bottom|inset|inset-x)-0\b)' "${S[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | rg -v --pcre2 '\binset-0\b|visibility:\s*hidden|opacity:\s*0\b|:\s*-\d{4,}px'
rg -n --pcre2 'scroll-padding|scroll-margin|(?<![\w-])scroll-(?:p|m)[tb]?-' "${S[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6. Static riders (formerly a11y-code-scan grep 0d): zoom lock, <html> without lang, orientation lock.
rg -n --pcre2 'user-scalable\s*=\s*(?:no|0)\b|maximum-scale\s*=\s*(?:1(?:\.0*)?|0?\.\d+)\b|userScalable\s*:\s*false|maximumScale\s*:\s*(?:1(?:\.0+)?|0?\.\d+)\b|<html\b(?![^>]*\blang=)[^>]*>|screen\.orientation\.lock\(|"orientation"\s*:\s*"(?:portrait|landscape)' -g '*.{html,webmanifest}' -g '**/*manifest*.json' -g '**/{layout,root,_document,app,index}.{tsx,jsx,vue,svelte,ts,js}' -g '**/app.html' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7. Gate integrity: 7a neutering shapes; 7b tag lists with no wcag22aa; 7c stories raised to a11y.test 'error' (-U: the
#    object spans lines in preview files); 7d axe runners that never read `incomplete` (7a's `resultTypes` effect, written
#    as `const { violations } = await new AxeBuilder(…).analyze()`).
rg -n --pcre2 '\.disableRules\(|\.exclude\(\s*["\x27](?:main|body|html|#root|#app|#__next)["\x27]|includedImpacts|resultTypes\s*:\s*\[\s*["\x27]violations["\x27]\s*\]|\btest\s*:\s*["\x27](?:todo|off)["\x27]|["\x27]color-contrast["\x27]\s*:\s*\{\s*enabled\s*:\s*false|page\.accessibility\b|\.withTags\([^)]*\)\s*\.options\(' "${T[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\[(?![^\]]*wcag22aa)[^\]]*["\x27]wcag2a["\x27]|--tags[\s=](?!\S*wcag22aa)\S*wcag2' -g '*.{md,sh}' "${T[@]}" "${X[@]}" "${ROOTS[@]}"
rg -c -U --pcre2 '\ba11y\s*:\s*\{[^}]*\btest\s*:\s*["\x27]error["\x27]' -g '*.{stories,story}.*' -g '**/.storybook/preview.*' --hidden "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 'new AxeBuilder\b|\baxe\.run\(' "${T[@]}" "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match '\bincomplete\b'
```

**Measured** (2026-10-05, about 0.4 s per tree). On all 12 `benchmarks/fixtures` trees the script parses, and every grep returns 0 except: 4 = 2 on `web-dashboard` (two overlays with inline `position: 'fixed'`; a CSS-only first version missed both), 2 = 1 on `vuln-fullstack`, and 0a = 1 on `brittle-suite` (no a11y harness in any fixture). On a read-only real React 19 + Vite + Radix app (2026-10-05): **7a: 2, both true** (`.storybook/preview.tsx` `a11y: { test: 'todo' }`; a sweep's `resultTypes: ['violations']`). Without `--hidden`, 7a missed the Storybook hit. **Re-measured 2026-10-15** on the same app, now inside a real NestJS + React monorepo, after the owner fixed both: 0a 4 · 0b 6 · 0c 3 · 0d 27 · 2: 72 · 4a: 17 · 4b: 9 · **6: 5, all true** (five PWA `manifest-*.json` files lock `"orientation": "portrait"`; 0 before `**/*manifest*.json` joined the glob) · 7a: 0 (preview now says `'error'`; no `resultTypes` left) · 7b: 0 · **7c: 1** (`preview.tsx` spreads the `a11y` object over two lines; 0, a false "no story at error", before `-U`) · **7d: 1, true** (`e2e/flows/support/axe.ts` keeps `const { violations } = …analyze()`, so `incomplete` never surfaces: 7a's effect with no 7a shape). On the fixtures, grep 6 and 7c are unchanged and 7d adds the two `a11y-states` Playwright specs, which drop `incomplete` too.

## The axe recipe and the probes — one module

This is the **one** axe recipe in the repo. `ui-crawl`, `a11y-quick-check` and the fix commands cite it rather than carry their own. It is `@playwright/test` 1.63 and `@axe-core/playwright` 4.13.0. In write mode it is saved as `<testDir>/a11y/a11y-probes.ts`; in judge mode it goes in the scratch dir. It typechecks under `tsc --strict`, and every probe was run on 2026-10-05 against a page seeded with each defect (results under each §).

```ts
import { expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

export const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];   // wcag22aa is what runs target-size
// ONE .options() object. Never chain .withTags() / .options() / .disableRules(): a later call drops the earlier one.
export function axeAt(page: Page, o: { experimental?: boolean; include?: string; off?: Record<string, string> } = {}) {
  let b = new AxeBuilder({ page }).options({
    runOnly: { type: 'tag', values: o.experimental ? [...TAGS, 'experimental'] : TAGS },
    rules: Object.fromEntries(Object.keys(o.off ?? {}).map((id) => [id, { enabled: false }])),   // id → reason, printed in the report
  });
  if (o.include) b = b.include(o.include);
  return b.analyze();
}
export const rows = (r: Awaited<ReturnType<AxeBuilder['analyze']>>) => ({
  axe: r.testEngine.version,
  violations: r.violations.flatMap((v) => v.nodes.map((n) => ({ id: v.id, impact: v.impact, target: n.target.join(' ') }))),
  review: r.incomplete.flatMap((v) => v.nodes.map((n) => ({ id: v.id, target: n.target.join(' '), why: n.any[0]?.data?.messageKey ?? '' }))),
});

// Reach the cell, then PROVE it: the surface marker (never networkidle), and the theme and lang the page actually drew.
export type Cell = { route: string; marker: string; theme: 'light' | 'dark'; width: number; locale?: string };
export async function reach(page: Page, c: Cell, prepare?: (page: Page, c: Cell) => Promise<void>) {
  await page.setViewportSize({ width: c.width, height: 900 });
  await page.emulateMedia({ colorScheme: c.theme });
  await prepare?.(page, c);   // the app's own switches from grep 0d: a storage key via addInitScript, a class, a cookie
  await page.goto(c.route);
  if (/\/(login|sign-?in)\b/.test(new URL(page.url()).pathname)) throw new Error(`RENDER BLOCKED — ${c.route} landed on ${page.url()}`);
  await expect(page.locator(c.marker).first()).toBeVisible();
  const drawn = await page.evaluate(() => { const h = document.documentElement;   // replace with the project's own marker (0d)
    const dark = /\bdark\b/.test(h.className) || h.dataset.theme === 'dark' || (!/\b(dark|light)\b/.test(h.className) && !h.dataset.theme && matchMedia('(prefers-color-scheme: dark)').matches);
    return { theme: dark ? 'dark' : 'light', lang: h.lang }; });
  if (drawn.theme !== c.theme) throw new Error(`THEME NOT APPLIED — asked ${c.theme}, the page drew ${drawn.theme}`);
  if (c.locale && !drawn.lang.startsWith(c.locale)) throw new Error(`LANG NOT APPLIED — asked ${c.locale}, <html lang="${drawn.lang}">`);
}

// §4 — one Tab walk: reachability, focus-visible delta, focus obscured (2.4.11).
export async function tabWalk(page: Page) {
  const n = 2 * (await page.locator('a[href],button,input,select,textarea,[tabindex]:not([tabindex="-1"])').count()) + 5;
  const stops: { id: string; delta: boolean; covered: boolean }[] = [];
  for (let i = 0; i < n; i++) {
    await page.keyboard.press('Tab');
    const s = await page.evaluate(() => {
      const e = document.activeElement as HTMLElement | null;
      if (!e || e === document.body) return null;
      const look = () => ['', '::before', '::after'].map((p) => { const c = getComputedStyle(e, p || null);   // only what is drawn
        const ol = c.outlineStyle === 'none' || parseFloat(c.outlineWidth) === 0 ? 'none' : `${c.outlineStyle} ${c.outlineWidth} ${c.outlineColor} ${c.outlineOffset}`;
        return [ol, c.boxShadow, c.borderTopColor, c.borderTopWidth, c.backgroundColor, c.color, c.textDecorationLine, c.opacity].join('|'); }).join('/');
      const on = look(); e.blur(); const off = look(); e.focus({ preventScroll: true });
      const r = e.getBoundingClientRect();
      const pinned = (x: Element | null) => { for (let p = x; p; p = p.parentElement) if (/fixed|sticky/.test(getComputedStyle(p).position)) return p; return null; };
      const covered = [[0.5, 0.5], [0.1, 0.1], [0.9, 0.1], [0.1, 0.9], [0.9, 0.9]].every(([fx, fy]) => {
        const top = document.elementFromPoint(r.left + r.width * fx, r.top + r.height * fy);
        if (!top || e.contains(top) || top.contains(e)) return false;
        const pin = pinned(top); return !!pin && !pin.contains(e);
      });
      return { id: e.dataset.testid || e.id || `${e.tagName}:${(e.getAttribute('aria-label') ?? e.textContent ?? '').trim().slice(0, 30)}`, delta: on !== off, covered };
    });
    if (s) stops.push(s);
  }
  return stops;   // reachability: expect(stops.map(s => s.id)).toContain(…); a trap: the last 2k ids cycle outside an open modal
}

// §3 non-text contrast. Colours go through a canvas, so oklch() and color-mix() resolve to sRGB.
export const contrastOf = (page: Page, sel: string) => page.evaluate((sel) => {
  const ctx = document.createElement('canvas').getContext('2d', { willReadFrequently: true })!;
  const rgba = (c: string) => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = c; ctx.fillRect(0, 0, 1, 1); return [...ctx.getImageData(0, 0, 1, 1).data]; };
  const lum = ([r, g, b]: number[]) => [r, g, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }).reduce((a, v, i) => a + v * [0.2126, 0.7152, 0.0722][i], 0);
  const bg = (e: Element | null): number[] => { for (let p = e; p; p = p.parentElement) { const c = rgba(getComputedStyle(p).backgroundColor); if (c[3] > 0) return c; } return [255, 255, 255, 255]; };
  return [...document.querySelectorAll(sel)].map((e) => {
    const s = getComputedStyle(e); const fg = rgba(s.borderTopWidth !== '0px' && s.borderTopStyle !== 'none' ? s.borderTopColor : s.outlineColor);
    const [a, b] = [lum(fg), lum(bg(e.parentElement))]; return { el: (e as HTMLElement).id || e.tagName, ratio: +((Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05)).toFixed(2) };
  });
}, sel);

// §5 house target (AA is axe's target-size) and §6 reflow and text spacing.
export const smallTargets = (page: Page, min: number) => page.evaluate((min) =>
  [...document.querySelectorAll('a[href],button,input:not([type=hidden]),select,[role=button],[role=link],[role=checkbox],[role=radio],[role=switch],[role=tab]')]
    .filter((e) => !(e.tagName === 'A' && getComputedStyle(e).display === 'inline'))   // inline text links are excepted
    .map((e) => { const r = e.getBoundingClientRect(); return { el: (e as HTMLElement).id || e.tagName, w: Math.round(r.width), h: Math.round(r.height) }; })
    .filter((x) => x.w > 0 && (x.w < min || x.h < min)), min);
export async function reflow(page: Page) {
  await page.setViewportSize({ width: 320, height: 256 });
  return page.evaluate(() => {
    const allowed = (e: Element) => !!e.closest('table,pre,code,canvas,iframe,[role=grid],[role=table],[data-a11y-2d]') ||
      (() => { for (let p = e.parentElement; p && p !== document.body; p = p.parentElement) { const o = getComputedStyle(p).overflowX; if (/auto|scroll|hidden|clip/.test(o) && p.getBoundingClientRect().right <= 321) return true; } return false; })();
    const over = [...document.querySelectorAll('body *')].filter((e) => e.getBoundingClientRect().right > 321 && (e as HTMLElement).innerText?.trim() && !allowed(e));
    return { scrollWidth: document.documentElement.scrollWidth, over: over.filter((e) => !over.includes(e.parentElement!)).map((e) => (e as HTMLElement).id || e.tagName) };
  });
}
export async function textSpacing(page: Page) {
  const clipped = () => page.evaluate(() => [...document.querySelectorAll('body *')].filter((e) => { const s = getComputedStyle(e);
    return /hidden|clip/.test(s.overflow + s.overflowX + s.overflowY) && (e as HTMLElement).innerText?.trim() && (e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1); }).map((e) => (e as HTMLElement).id || e.tagName));
  const before = await clipped();
  await page.addStyleTag({ content: '* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important } p { margin-bottom: 2em !important }' });
  return (await clipped()).filter((x) => !before.includes(x));   // clipped only because of the 1.4.12 spacing
}
```

**The builder traps, measured** (2026-10-05, axe-core 4.13.0, `@axe-core/playwright` 4.13.0, Chromium 153, a page with two adjacent 14 px buttons and a portrait-only rotate): plain `analyze()` never ran `target-size` · `.withTags(TAGS)` ran it · `.withTags(TAGS).options({…})` did **not** (the later `.options()` replaced `runOnly`) · `.options({ rules: { 'target-size': { enabled: true } } }).disableRules(['region'])` did **not** (the disable wiped the enable) · `css-orientation-lock` (1.3.4) **and** `label-content-name-mismatch` (2.5.3) ran only with `'experimental'` in the tags · the one-object `.options({ runOnly, rules })` above ran all of them. `AxeBuilder` also throws on a page from `browser.newPage()`; it needs one from `browser.newContext()` (`@playwright/test`'s `page` fixture is fine). `ui § 49–50` hold the general rules.

**The cell spec.** One test per cell, named to `testMatch`; the gate is G9: **no new serious or critical violation (rule id × target) against the stored baseline**, per cell.

```ts
import { test, expect } from '@playwright/test';
import { existsSync, readFileSync } from 'node:fs';
import { axeAt, rows, reach } from './a11y-probes';
const ROUTES: [string, string][] = [['/orders', 'h1:has-text("Orders")']];   // THIS project's route table, a surface-unique marker each
const B = 'e2e/a11y/a11y-baseline.json'; const BASELINE = new Set<string>(existsSync(B) ? JSON.parse(readFileSync(B, 'utf8')) : []);
for (const theme of ['light', 'dark'] as const) for (const width of [1280, 375]) for (const [route, marker] of ROUTES)
  test(`a11y ${route} ${theme} ${width}`, async ({ page }, info) => {
    await reach(page, { route, marker, theme, width });
    const r = rows(await axeAt(page));
    await info.attach('axe.json', { body: JSON.stringify({ route, theme, width, ...r }), contentType: 'application/json' });
    const fresh = r.violations.filter((v) => /serious|critical/.test(v.impact ?? '') && !BASELINE.has(`${route}|${theme}|${width}|${v.id}|${v.target}`));
    expect(fresh, 'new serious/critical vs baseline').toEqual([]);
  });
```

Add a locale axis when the product ships a second script or direction, and the ui-state-scan states as `prepare` hooks. Run `axeAt(page, { experimental: true })` once per route as a **separate, non-gating** pass. Its rows are candidates for the 2.5.3 and 1.3.4 oracles, never gate failures.

## Scans for

Severity follows axe impact at a reachable cell: critical or serious → **high**; moderate → **medium**; minor → **low**. Raise to **critical** when the node is the sole path to a primary or destructive action, or blocks sign-in or checkout. Drop one step when an equivalent accessible path exists on the same page.

| § | Class | WCAG 2.2 SC (level) | Oracle | Variant |
|---|---|---|---|---|
| 1 | Axe floor per cell: names, labels, structure, `lang`, ARIA, zoom meta, autocomplete values, captions | 1.1.1, 1.3.1, 2.4.1, 2.4.2, 2.4.4, 3.1.1, 3.1.2, 3.3.2, 4.1.2 (A); 1.3.5, 1.4.4 (AA) | axe at route-state | V88, V94, V97 |
| 2 | Interactive surfaces: what only the opened state shows | 4.1.2, 2.1.1, 2.1.2, 2.4.3 (A) | axe scoped to the surface + keyboard path | V90 |
| 3 | Contrast per theme; non-text contrast | 1.4.3, 1.4.11 (AA) | axe `color-contrast` per theme + `contrastOf` | V101 |
| 4 | Keyboard path: reachability, trap, focus visible, focus obscured | 2.1.1, 2.1.2, 2.4.3 (A); 2.4.7, 2.4.11 (AA) | `tabWalk`, normal and forced colours | V87, V89, V91 |
| 5 | Target size | 2.5.8 (AA); house target separately | axe `target-size` + `smallTargets` | V102 |
| 6 | Reflow, zoom, text spacing, orientation | 1.4.10, 1.4.4, 1.4.12, 1.3.4 (AA) | `reflow`, `textSpacing`, axe `meta-viewport`, experimental `css-orientation-lock` | V103 |
| 7 | The a11y gate neutered | — (it certifies every SC above) | injected violation | V104 |

### 1. Axe floor per cell

```
BAD:   /orders dark 375 — button-name on 12 row-action buttons; html-has-lang after switching to en; label on the search box
GOOD:  every cell's violations are in the baseline or fixed; every incomplete node is a named review row
```

Cells are **route × state × theme × viewport** (× locale when a second script or direction ships). States: loaded, each surface from §2, and the ui-state-scan states when ui-ux is installed. **Read the result:** every `incomplete` node is a review row with its `messageKey` reason. `bypass`, `video-caption` and `no-autoplay-audio` are needs-review only: never auto-fail them, never drop them. **Read the code:** which component renders the selector (one finding per wrapper)? Does a design-system primitive own the role or name (`ui § 12–14`)? Does a spread prop or a translation key supply the name? After a locale switch, does `<html lang>` follow (`reach` reads it back) and does `dir` match the script? **Finding when** a violation node sits at a reached cell, traces to source, and no `ui § 11–34` exception applies. **Proof:** axe at route-state (V88, V94, V97), asserting the **one** rule id the finding names.

### 2. Interactive surfaces — what only the opened state shows

```
BAD:   "Edit address" dialog opens with focus left on <body>, no accessible name, Escape returns focus to <body>
GOOD:  focus moves in, the dialog is named, Tab wraps inside, Escape closes and focus is back on the trigger
```

In an admin app the defects live in the modal, the menu, the combobox, the date picker and the tab panel, all unmounted at load. A route with no opened surfaces is half a scan.

```ts
const triggers = await page.locator('[aria-haspopup], [aria-expanded], [aria-controls], [role="tab"], summary, [popovertarget]').all();
const SURFACES = 'dialog[open], [role="dialog"], [role="alertdialog"], [role="menu"], [role="listbox"], [role="tabpanel"], [popover]:popover-open';
const unreachable: Locator[] = [], opened: object[] = [];
for (const t of triggers) {                          // union with grep 2 and the project's wrapper names
  await t.click();                                   // then hover(), then focus() + Enter, before calling it unreachable
  const surface = page.locator(SURFACES).filter({ visible: true }).last();   // the newest open surface, not a hidden one
  if (!(await surface.waitFor({ timeout: 2000 }).then(() => true, () => false))) { unreachable.push(t); await page.keyboard.press('Escape'); continue; }
  const id = await surface.getAttribute('id');      // .include() takes a selector, never an element handle
  const r = rows(await axeAt(page, id ? { include: `#${id}` } : {}));
  const focusIn = await surface.evaluate((s) => s.contains(document.activeElement));
  const expanded = await t.getAttribute('aria-expanded');
  await page.keyboard.press('Escape');
  opened.push({ r, focusIn, expanded, focusBack: await t.evaluate((e) => e === document.activeElement) });
}
```

Assert four things beyond axe: the surface's accessible name (`aria-dialog-name` fires only once open); focus moved in on open and returned to the trigger on close; Tab past the last focusable wraps inside a modal and leaves a menu; the trigger's `aria-expanded` flipped. **Mandatory row** on every route: `interactive surfaces: N found / M opened / K unreachable [/ J deferred: <names>]`. `K > 0` is itself a candidate: a trigger that opens nothing on click, hover or Enter is broken or mouse-only. Measured on a seeded page: a native `<dialog>` opened with `showModal()` → focus in and back on Escape; a `role="dialog"` `div` unhidden by a click → focus never moved in and `aria-expanded` stayed `"false"`. A first version that took `.first()` of the surface selector picked a hidden dialog, left the modal open and timed out on the next trigger; hence `filter({ visible: true })` and the Escape on every branch. **Read the code:** is the surface a headless primitive whose consumer overrides it (`asChild` onto a `div`, `ui § 12`)? Is it native `<dialog>` opened with `show()` rather than `showModal()` (`ui § 13`)? Does it open only for a role the test user lacks? **Finding when** one of the four fails at a reached surface. **Severity:** critical when focus is trapped with no way out; high otherwise. **Proof:** keyboard path (V90).

### 3. Contrast per theme; non-text contrast

```
BAD:   dark theme muted text #6b6b6b on #1e1e1e (3.1:1)  · input border #e5e5e5 on #fff (1.26:1, measured on the seeded page)
GOOD:  ≥ 4.5:1 text (3:1 large) in every theme  · borders, focus rings, toggle states ≥ 3:1 against what they sit on
```

**Read the result:** axe `color-contrast` is text-only. Its `incomplete` reasons (`bgImage`, `bgGradient`, `bgOverlap`, `fgAlpha`, `shortTextContent`, `pseudoContent`, …) are manual rows. `contrastOf(page, 'input, select, textarea, [role=checkbox], [role=switch]')` and the focus ring colour cover 1.4.11, which no axe rule checks. Exempt: disabled controls, decoration, logos (`ui § 19`); placeholder text is **not** exempt. **Per locale:** a real RTL app's own audit note records `color-contrast` returning nothing for Arabic-only text under axe 4.10.2. A minimal page did not reproduce it under 4.10.2 or 4.13.0 (2026-10-05), so compare the node count `color-contrast` evaluated (violations + passes + incomplete) between locales. A locale whose count collapses is `blocked`, not clean. **Read the code:** which token pair produces the colours in this theme (`design-token-audit` when ui-ux is installed), and does every consumer use it? Is the element disabled or decorative? **Finding when** a pair in a reached theme falls below its ratio. **Severity:** high for body text and primary controls; medium for secondary text and borders. **Proof:** V101 in light and dark.

### 4. Keyboard path — reachability, trap, focus visible, focus obscured

```
BAD:   .btn:focus { outline: none }  → delta: false  · a "Save" link scrolled under a fixed cookie banner → covered: true
GOOD:  a :focus-visible ring drawn in normal and forced-colours modes · scroll-padding-block-end equal to the banner height
```

One `tabWalk` per cell gives four results. **Reachability:** every `a11y-code-scan` §1 / §9 candidate on the route is in (or absent from) the stop list. **Trap:** the last 2k ids cycle inside a subtree that is not an open modal (`ui § 15`: modal containment is required). **Focus visible:** `delta: false` is a 2.4.7 candidate; repeat under `page.emulateMedia({ forcedColors: 'active' })`, where a `box-shadow`-only ring vanishes (`ui § 18`: Low, not a 2.4.7 failure). **Obscured:** `covered: true` is 2.4.11 (all five sample points under a fixed/sticky layer; partial cover is AAA 2.4.12). Walk with the cookie banner and chat bubble **shown**, at 375 px too. Measured on the seeded page: `outline: none` with no replacement → `delta: false`; a `:focus-visible` ring → `true`; the box-shadow ring → `true`, then `false` under forced colours; a link scrolled under a fixed 140 px banner → `covered: true`. The computed delta is the bulk lane. The per-finding proof is the screenshot delta (V89): a clip 4 px larger than the box, focused vs blurred, must differ. **Read the code:** which rule removes the ring (`a11y-code-scan` §3 hit) and which wrapper class should add it? Which layer covers the stop (grep 4a), and is scroll padding reserved for it (grep 4b)? Can the user dismiss the layer, and did the walk start with it shown? **Finding when** a reached stop shows no delta, is covered, is unreachable, or traps. **Severity:** critical for a trap or an unreachable sole path; high for a missing ring on a primary control; medium for obscured focus. **Proof:** V87, V89, V91.

### 5. Target size

```
BAD:   20×20 row-action icon buttons 4 px apart (24 px circles overlap)
GOOD:  ≥ 24×24 CSS px, or spaced so the 24 px circles touch no other target; inline text links are exempt
```

**Read the code:** which wrapper sets the size (one finding per wrapper)? Is an equivalent larger control on the page (`ui § 20`)? axe `target-size` decides AA 24×24 with the spacing exception: an isolated 16 px button passed on the seeded page, and two adjacent 14 px buttons failed. Its `incomplete` reasons (`partiallyObscured`, `tooManyRects`, a `tabindex=-1` target) are review rows. A **house target** (44 px, or the platform minimum in `THR-A11Y`) is checked with `smallTargets(page, 44)` at 360 px **only when the project declares one**, and reported as the house rule, never as AA (`ui § 4`, `ui § 20`). **Finding when** axe fails the node at a reached cell and no exception applies. **Severity:** medium; high on a primary action at the mobile width. **Proof:** V102.

### 6. Reflow, zoom, text spacing, orientation

```
BAD:   <meta name="viewport" content="width=device-width, maximum-scale=1">  · a 600 px form at 320 px  · height: 48px; overflow: hidden on text
GOOD:  zoom allowed · single-column reflow at 320 px · min-height instead of height on text boxes
```

**Reflow:** `reflow(page)` at 320×256. `over` lists text boxes past 320 px that sit outside a 2-D or scrolling container (tables, code, maps and `[data-a11y-2d]` are allowed, `ui § 21`). **Text spacing:** `textSpacing(page)` reports only boxes that clip **because of** the 1.4.12 spacing, not boxes that clipped before. **Zoom:** axe `meta-viewport`; grep 6 `user-scalable=no` / `maximum-scale≤1` is a static fact (`ui § 57`: iOS ignores it, other platforms do not). **Orientation:** the experimental `css-orientation-lock` pass plus a portrait and a landscape viewport; a web app manifest's `"orientation"` (grep 6 reads `*.webmanifest` and `*manifest*.json`) locks every installed PWA, a static fact. **`lang`:** grep 6 `<html>` with no `lang` is a static fact; axe `html-has-lang` confirms it. Measured on the seeded page: a 600 px block → `over: ['wide']`, `scrollWidth: 600`; the table in an `overflow-x: auto` wrapper was allowed; a 48 px `overflow: hidden` box holding two lines → clipped only after the injection. **Read the code:** which fixed width or height causes it, and is the content two-dimensional by nature? Is the orientation lock essential (a game, a check deposit)? **Finding when** a reached cell scrolls horizontally outside an allowed container, clips under the spacing, blocks zoom, or locks orientation. **Severity:** high for a zoom lock or a transactional form that does not reflow; medium otherwise. **Proof:** V103.

### 7. The a11y gate neutered

```
BAD:   parameters: { a11y: { test: 'todo' } } with no story at 'error'  · new AxeBuilder({ page }).withTags(T).options({ rules })  · .exclude('main')
GOOD:  a11y.test: 'error' (per-story 'todo' with a reason)  · one .options({ runOnly, rules }) object  · scoped excludes with a ticket
```

**Classes:** a broad `.disableRules([...])`; `.exclude('main' | 'body' | '#root')`; an `includedImpacts` filter (cypress-axe); `resultTypes: ['violations']`, which drops every `incomplete`, and its destructured twin `const { violations } = await …analyze()` with `incomplete` read nowhere (grep 7d); Storybook `a11y.test` of `'todo'` or `'off'` with no story raised to `'error'`; contrast only in jsdom (jest-axe, vitest-axe); a tag list without `wcag22aa`; `.options()` after `.withTags()`; `page.accessibility` (removed in Playwright 1.63, `ui § 56`); a Lighthouse score used as the gate; an axe older than 4.13 pinned by URL (re-baseline on upgrade: 4.13 changed issue counts). **Read the code:** is the disabled rule checked by another job (a real-browser contrast job beside a jsdom suite is fine)? Does a comment give a reason and an owner? **Finding when** an injected violation leaves the gate green. **Severity:** high, because a neutered gate certifies every later regression. **Proof:** V104: add one unnamed icon button on a test-only route (or one story at `a11y.test: 'error'` with a missing label), run the project's gate command unchanged, and it must exit non-zero.

## Proof

Each § names its oracle from [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states. The test runs on a production build at the cell, asserts the **one** rule or probe the finding names, and **fails before the fix**. A test that passes on unfixed code proves nothing: rebuild it until it fails. A fix is accepted only when that oracle goes green, the class variants pass (the opened dialog, dark theme, 320 px, RTL, forced colours), the cell's violation count strictly drops, and no new rule id appears. Never accepted as fixes: adding to `disableRules` or `.exclude()`, `aria-hidden` on the offender, an `outline: none` swapped for another invisible style, a raised `maxDiffPixelRatio`, `a11y.test: 'todo'`, or deleting the test.

## Output

```
a11y-scan — @axe-core/playwright 4.13.0 · axe-core 4.13.0 · @playwright/test 1.63.0 · react 19.2 + vite (vite preview)
Harness: tests/.auth/user.json (auth gate passed) · cells: 14 routes × light/dark × 1280/375 = 56 · locale ar + en · judge mode (scratch)

Findings: 2 · Unconfirmed: 1 · Review rows (axe incomplete): 9

1. src/shared/ui/icon-button.tsx:41              [report-with-fix]   high
   §5 target-size (2.5.8 AA) — 20×20 row actions 4 px apart; /orders light 375, 12 nodes from one wrapper.
   Proof: axe target-size at /orders (375) fails; 0 nodes after size="md" spacing. Fix: the wrapper's min size, one change.
2. .storybook/preview.tsx:116                    [report-with-fix]   high
   §7 gate neutered — a11y.test 'todo' for 88 stories, 0 raised to 'error'. Proof: injected unnamed button story; the
   storybook vitest project stays green. Fix: 'error' globally; per-story 'todo' with a reason where debt is accepted.
3. src/features/orders/components/OrderPanel.tsx:88    [report-flagged]   medium
   §4 focus obscured (2.4.11 AA) — "Save" covered by the sticky save bar at 375. Unproven link: whether the bar can be
   dismissed. Settling test: obscured rect (V91) with the bar shown.

interactive surfaces: /orders 9 found / 9 opened / 0 unreachable · /settings 14 / 13 / 1 ("Row actions": click, hover, Enter opened nothing)
Verification: 23 candidates → 2 findings · 1 unconfirmed · 4 hardening · 0 pre-existing · 16 refuted
Automated floor only: the manual pass (screen reader, zoom 200 %, content judgement) is not part of this run.

Class coverage (WCAG 2.2 AA, rendered):
  §1 axe floor               checked (56 cells → 0 findings; 9 incomplete listed as review rows)
  §2 interactive surfaces    checked (31 found / 30 opened / 1 unreachable → 1 unconfirmed)
  §3 contrast + non-text     checked (light + dark; ar color-contrast node count within 5 % of en; 0 findings)
  §4 keyboard path           checked (56 walks → 1 unconfirmed; forced colours: 3 box-shadow rings, Low)
  §5 target size             checked (1 finding, 12 nodes, 1 wrapper; house target not declared → not checked)
  §6 reflow / spacing / zoom checked (0 findings; 2 tables scroll inside their container)
  §7 gate integrity          checked (2 hits → 1 finding; the sweep's resultTypes is Hardening: a second job reads incomplete)
  riders                     zoom lock, <html lang>, orientation: 0 static hits
```

`[report-with-fix]`: the cell, the node, the source line and a failing oracle are present, and the fix is a local change in the project's own components. `[report-flagged]`: one link is unproven, and the row names it with the settling test. The coverage block lists **all seven** classes on every run: `checked (k → m findings)` only when the cells rendered; `N/A (<reason>)` when the surface is absent; `blocked (no harness)` / `blocked (RENDER BLOCKED: <cell>)` otherwise. A partial run reads `Live, unreviewed (k groups / n nodes)`, never `checked`.

## The 3,000-hit path

Volume here is **nodes × cells**: 12 nodes of one wrapper across 56 cells is 672 rows and one finding.

1. **Intersect** with the route table and the reached cells. A node on a `RENDER BLOCKED` cell is not a result.
2. **Group** by (rule id or probe, the component that renders the selector). A wrapper with the defect is one group; fixing the wrapper closes every call site.
3. **Rank** by route traffic (RUM or analytics when present; else landing, auth, checkout-class, list and form routes) and by axe impact.
4. **Read the top 30 groups** fully, tracing each to source.
5. **Prefer the bulk oracle.** One run of the cell spec across the matrix confirms or refutes whole groups. The `a11y-code-scan` §1 / §9 groups are settled by the stop lists from one walk per route.
6. **Ledger the rest** `Live, unreviewed (k groups / n nodes)` with the command that continues them.

## False positives / precedents

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (accessibility § 11–34, versions § 49–57, § 58) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10 (the accessibility column). The ones this skill meets most: decorative `alt=""` (§ 11); headless and native primitives (§ 12–13); modal focus containment (§ 15); box-shadow rings (§ 18); contrast exemptions (§ 19); target-size exceptions, inline links (§ 20); 2-D scrolling at 320 px (§ 21); built-in route announcers (§ 27); a Lighthouse 100 is not conformance (§ 51).

## When to run

- On every PR that touches UI, as G9 on the touched routes' cells (no new serious or critical vs the baseline).
- After a theme, token or locale change: contrast and RTL failures are cell-specific.
- After any change to a modal, menu, tab, combobox or disclosure: only §2 sees it.
- On every whole-repo `/a11y-audit`, after `a11y-code-scan`, across the full route matrix. The two are complements, never substitutes.
- When `@ux-reviewer` or `@accessibility-auditor` needs a static candidate proven on the real DOM.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under an audit command that happens in its verification phase. Run standalone, apply the protocol as a separate second pass and tag those rows `self-verified`. List the rest as Unconfirmed, Hardening, Pre-existing or Refuted; never drop them.
- Halt on `RENDER BLOCKED`: the auth gate failed, a cell landed on the login path, or the theme or `lang` read back differs. Never score that cell.
- Halt on a finding without the rule id or probe, the node, the source `<file:line>`, the cell, the WCAG 2.2 SC and level, and the fix.
- Halt if a route row carries no `interactive surfaces: N found / M opened / K unreachable` line, or if a surface was opened and only axe ran on it.
- Halt if `incomplete` was not read, if the report claims WCAG 2.2 AA without `wcag22aa` in the tags, or if the builder chains `.withTags()` / `.options()` / `.disableRules()`.
- Halt if the scan returns zero violations on a page with no `<h1>`, no landmark and no labelled input: it did not scan the page.
- Do not report an AAA criterion or a house target as an AA failure. Do not print "accessible", "compliant" or "no issues found".
- Do not propose `disableRules`, `.exclude()`, `aria-hidden`, a suppression or a lowered threshold as a fix.

## Related

- `a11y-code-scan` (this pack) — the static half; run it first. Its candidates are settled by §1, §2 and §4 here.
- `dev-server-start` and `visual-check` (this pack) — the served build and the session / blocked-render contract this skill uses verbatim.
- `@ux-reviewer` (ui-ux pack, when installed) — the WCAG judge and owner of the SC-coverage block; `@accessibility-auditor` (this pack) judges without ui-ux and keeps the manual lanes.
- `ui-state-scan` (ui-ux pack, when installed) — the state handlers that put a cell in error, empty or forbidden.
- `ui-crawl` (ui-ux pack) — the cross-route crawler; its axe call uses this recipe's tag list.
- `/a11y-audit` (this pack) — dispatches both detectors and folds their coverage blocks into the ledger.
