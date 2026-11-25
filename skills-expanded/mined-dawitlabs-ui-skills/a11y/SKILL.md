---
name: a11y
description: Master accessibility audit skill that scans every screen with axe-core, tests keyboard navigation, checks focus visibility, audits ARIA and semantic structure, then fixes every violation from critical down to minor. Works screen by screen in priority order with visual and programmatic verification. Use when user wants to fix accessibility issues, meet WCAG 2.1 AA, improve keyboard nav, or invokes /a11y.
---

# /a11y — Master Accessibility Audit

Finds and fixes every accessibility violation across the entire app. Works programmatically (axe-core) and visually (keyboard screenshots), from critical to minor, screen by screen.

Full WCAG quick-reference and fix patterns: [WCAG.md](WCAG.md)

---

## Phase 0 — Environment Setup

### 0a. Check / start dev server
```bash
curl -s --max-time 2 -o /dev/null -w "%{http_code}" http://localhost:3000
```
If not `200`, find and start the dev command, then wait:
```bash
until curl -s --max-time 2 http://localhost:3000 > /dev/null 2>&1; do sleep 1; done && echo "ready"
```

### 0b. Find source root
```bash
find . -type d -name "src" \
  -not -path "*/node_modules/*" \
  -not -path "*/.next/*" \
  -not -path "*/dist/*" \
  -not -path "*/.turbo/*" \
  | head -1
```
If no `src/`: `find . -type d -name "app" -not -path "*/node_modules/*" -not -path "*/.next/*" | head -1`

Use the result as `<SRC>` throughout.

### 0c. Verify axe-core
```bash
find . -path "*/axe-core/package.json" -not -path "*/node_modules/.cache/*" 2>/dev/null | head -1
```
If not found: install it (dev dependency only):
```bash
pnpm add -D axe-core 2>/dev/null || npm install -D axe-core 2>/dev/null || yarn add -D axe-core
```

Resolve the axe bundle path for later injection:
```bash
find . -path "*/axe-core/axe.min.js" -not -path "*/node_modules/.cache/*" 2>/dev/null | head -1
```
Store this as `<AXE_PATH>`.

### 0d. Write the scan script
Write to the **project root** (needs node_modules). Deleted in Phase 4.

**`_a11y_scan.mjs`:**
```js
import { chromium } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'fs';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };

const url        = get('--url');
const name       = get('--name') ?? 'screen';
const width      = parseInt(get('--width')  ?? '1280');
const height     = parseInt(get('--height') ?? '900');
const auth       = get('--auth');
const screenshot = get('--screenshot') ?? `/tmp/a11y-${name}.png`;
const report     = get('--report')     ?? `/tmp/a11y-${name}.json`;

if (!url) { console.error('--url required'); process.exit(1); }

mkdirSync('/tmp/a11y', { recursive: true });

const axePath = (() => {
  try { return require.resolve('axe-core'); }
  catch { console.error('axe-core not found — run: pnpm add -D axe-core'); process.exit(1); }
})();

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width, height },
  ...(auth ? { storageState: auth } : {}),
});
const page = await context.newPage();

try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
} catch {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
}

// Inject axe-core from local node_modules
await page.addScriptTag({ path: axePath });

// Run axe scan
const results = await page.evaluate(async () => {
  const r = await window.axe.run(document, {
    runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'best-practice'] },
  });
  return {
    violations:  r.violations.map(v => ({
      id:          v.id,
      impact:      v.impact,
      description: v.description,
      help:        v.help,
      helpUrl:     v.helpUrl,
      nodes:       v.nodes.map(n => ({ html: n.html, target: n.target, failureSummary: n.failureSummary })),
    })),
    incomplete: r.incomplete.length,
    passes:     r.passes.length,
  };
});

await page.screenshot({ path: screenshot, fullPage: true });
await browser.close();

writeFileSync(report, JSON.stringify(results, null, 2));

const counts = { critical: 0, serious: 0, moderate: 0, minor: 0 };
for (const v of results.violations) counts[v.impact] = (counts[v.impact] ?? 0) + 1;

console.log(`saved: ${screenshot}`);
console.log(`report: ${report}`);
console.log(`violations: critical=${counts.critical} serious=${counts.serious} moderate=${counts.moderate} minor=${counts.minor}`);
console.log(`passes: ${results.passes} | incomplete: ${results.incomplete}`);
```

**Usage:**
```bash
node _a11y_scan.mjs --url http://localhost:3000 --name home
node _a11y_scan.mjs --url http://localhost:3000/dashboard --name dashboard --auth /tmp/uiux-auth-state.json
node _a11y_scan.mjs --url http://localhost:3000/settings --name settings --width 375 --height 812
```

**After every scan: read the JSON report and the screenshot.**

### 0e. Write the keyboard navigation script
Write to the **project root**. Deleted in Phase 4.

**`_a11y_keyboard.mjs`:**
```js
import { chromium } from '@playwright/test';
import { mkdirSync } from 'fs';

const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };

const url    = get('--url');
const name   = get('--name') ?? 'screen';
const width  = parseInt(get('--width')  ?? '1280');
const height = parseInt(get('--height') ?? '900');
const auth   = get('--auth');
const maxTabs = parseInt(get('--max-tabs') ?? '30');

if (!url) { console.error('--url required'); process.exit(1); }

mkdirSync('/tmp/a11y', { recursive: true });

const browser = await chromium.launch();
const context = await browser.newContext({
  viewport: { width, height },
  ...(auth ? { storageState: auth } : {}),
});
const page = await context.newPage();

try {
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
} catch {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
}

const issues = [];

// Check for skip link as first tab stop
await page.keyboard.press('Tab');
const skipLink = await page.evaluate(() => {
  const el = document.activeElement;
  if (!el || el === document.body) return null;
  return { tag: el.tagName, text: el.textContent?.trim(), href: el.getAttribute('href') };
});

const hasSkipLink = skipLink?.text?.toLowerCase().includes('skip') && skipLink?.href?.startsWith('#');
if (!hasSkipLink) issues.push({ type: 'missing-skip-link', detail: 'First Tab stop is not a "Skip to main content" link' });

// Tab through interactive elements
const focusLog = [];
for (let i = 0; i < maxTabs; i++) {
  await page.keyboard.press('Tab');
  const focusInfo = await page.evaluate(() => {
    const el = document.activeElement;
    if (!el || el === document.body) return null;
    const style   = getComputedStyle(el);
    const rect    = el.getBoundingClientRect();

    // Capture focused styles
    const focusedBorder     = style.borderColor;
    const focusedBackground = style.backgroundColor;

    // Briefly blur to capture unfocused styles, then refocus
    el.blur();
    const blurStyle       = getComputedStyle(el);
    const blurBorder      = blurStyle.borderColor;
    const blurBackground  = blurStyle.backgroundColor;
    el.focus();

    return {
      tag:                el.tagName,
      role:               el.getAttribute('role'),
      ariaLabel:          el.getAttribute('aria-label'),
      text:               el.textContent?.trim().slice(0, 60),
      outlineWidth:       style.outlineWidth,
      outlineStyle:       style.outlineStyle,
      boxShadow:          style.boxShadow,
      hasBorderChange:    focusedBorder     !== blurBorder,
      hasBackgroundChange:focusedBackground !== blurBackground,
      width:              Math.round(rect.width),
      height:             Math.round(rect.height),
    };
  });
  if (!focusInfo) break;

  // Detect focus visibility via outline, box-shadow, or meaningful border/background change.
  // Compare against a snapshot of the element's non-focused style by briefly blurring and refocusing.
  const hasVisibleFocus = (
    (focusInfo.outlineStyle !== 'none' && focusInfo.outlineWidth !== '0px')
    || (focusInfo.boxShadow && focusInfo.boxShadow !== 'none')
    || focusInfo.hasBorderChange
    || focusInfo.hasBackgroundChange
  );
  const hasName = !!(focusInfo.ariaLabel || focusInfo.text);
  const isTiny  = focusInfo.width < 44 || focusInfo.height < 44;

  if (!hasVisibleFocus) issues.push({ type: 'no-focus-visible', element: focusInfo.tag, text: focusInfo.text });
  if (!hasName)         issues.push({ type: 'missing-accessible-name', element: focusInfo.tag });
  if (isTiny)           issues.push({ type: 'small-tap-target', element: focusInfo.tag, text: focusInfo.text, size: `${focusInfo.width}×${focusInfo.height}` });

  focusLog.push({ ...focusInfo, hasVisibleFocus, hasName });
}

// Screenshot after keyboard traversal (last focused state)
await page.screenshot({ path: `/tmp/a11y/${name}-keyboard.png`, fullPage: false });
await browser.close();

console.log(`keyboard screenshot: /tmp/a11y/${name}-keyboard.png`);
console.log(`tab stops visited: ${focusLog.length}`);
if (issues.length) {
  console.log('issues found:');
  issues.forEach(i => console.log(' -', JSON.stringify(i)));
} else {
  console.log('no keyboard issues found');
}
```

**Usage:**
```bash
node _a11y_keyboard.mjs --url http://localhost:3000 --name home
node _a11y_keyboard.mjs --url http://localhost:3000/dashboard --name dashboard --auth /tmp/uiux-auth-state.json --max-tabs 50
```

### 0f. Handle auth-protected screens
```bash
ls /tmp/uiux-auth-state.json /tmp/animate-auth-state.json /tmp/copy-auth-state.json 2>/dev/null | head -1
```
If found, pass `--auth <path>` to all script calls for protected routes.

If not found and protected screens exist, write `_a11y_auth.mjs` to the project root:
```js
import { chromium } from '@playwright/test';
const { TEST_EMAIL, TEST_PASSWORD, LOGIN_URL, SUCCESS_URL } = process.env;
if (!TEST_EMAIL || !TEST_PASSWORD) { console.error('Set TEST_EMAIL and TEST_PASSWORD'); process.exit(1); }
const browser = await chromium.launch();
const page    = await browser.newPage();
await page.goto(LOGIN_URL ?? 'http://localhost:3000/sign-in');
await page.fill('input[type="email"]',    TEST_EMAIL);
await page.fill('input[type="password"]', TEST_PASSWORD);
await page.click('button[type="submit"]');
await page.waitForURL(SUCCESS_URL ?? '**/dashboard**', { timeout: 15000 });
await page.context().storageState({ path: '/tmp/a11y-auth-state.json' });
await browser.close();
console.log('saved → /tmp/a11y-auth-state.json');
```

---

## Phase 1 — Accessibility Audit

### 1a. Find all screens
Every `page.tsx` in App Router, every page in Pages Router, modals, drawers, auth flows, settings, onboarding. List each with its route.

### 1b. Run axe scan on every screen
For each screen, run at **both** desktop and mobile viewports. Tap target failures only appear at mobile.

```bash
node _a11y_scan.mjs --url http://localhost:3000<ROUTE> --name <name>-desktop
node _a11y_scan.mjs --url http://localhost:3000<ROUTE> --name <name>-mobile --width 375 --height 812
```

Read both JSON reports and both screenshots. Group violations by impact:
- **Critical** — `impact: "critical"` — content inaccessible to assistive tech
- **Serious** — `impact: "serious"` — major barrier, usually WCAG AA failure
- **Moderate** — `impact: "moderate"` — degrades the experience
- **Minor** — `impact: "minor"` — best-practice violation

### 1c. Run keyboard nav test on every screen
For each screen, run `_a11y_keyboard.mjs`. Read stdout for issues. Read the keyboard screenshot.

```bash
node _a11y_keyboard.mjs --url http://localhost:3000<ROUTE> --name <name>
```

Check manually from the output:
- Is the first Tab stop a skip link?
- Do all interactive elements have a visible focus ring?
- Do all buttons and links have accessible names?
- Are all tap targets ≥44×44px?

### 1d. Code-level scan for structural issues
```bash
SRC=<your source root>

# Images without alt
grep -rn "<img" "$SRC" --include="*.tsx" --include="*.jsx" | grep -v "alt="

# Buttons with no accessible name
grep -rn "<button" "$SRC" --include="*.tsx" | grep -v "aria-label\|aria-labelledby"

# onClick on non-interactive elements
grep -rn "onClick" "$SRC" --include="*.tsx" | grep -v "button\|a\|input\|select\|textarea\|role="

# Missing form labels
grep -rn "<input" "$SRC" --include="*.tsx" | grep -v "aria-label\|aria-labelledby\|id=" | grep -v "type=\"hidden\""

# Heading hierarchy — look for h3 without an h2 parent context
grep -rn "<h[1-6]" "$SRC" --include="*.tsx"

# lang attribute on html element
grep -rn "<html" "$SRC" --include="*.tsx" --include="*.html"

# color-only state signals (errors shown only with a red class, no icon/text)
grep -rn "text-red\|text-error\|border-red" "$SRC" --include="*.tsx" | head -20

# Dynamic content missing aria-live
# Find containers that update dynamically but have no live region announcement
grep -rn "useState\|useEffect\|isLoading\|isError\|toast\|notification\|alert" "$SRC" --include="*.tsx" -l | \
  xargs grep -L "aria-live\|aria-atomic\|role=\"alert\"\|role=\"status\""
```

Dynamic content that needs `aria-live`:
- Toast / notification messages
- Form validation errors (after submit)
- Search result counts ("3 results found")
- Loading completion messages
- Real-time data updates

If a component updates content without a page reload and has no `aria-live`, screen readers miss it — flag for manual review.

### 1e. Check prefers-reduced-motion
```bash
grep -rn "prefers-reduced-motion" "$SRC" --include="*.css" --include="*.tsx" --include="*.ts"
```
If missing entirely: flag as critical — every animation must be suppressible.

Present the full audit grouped by screen before continuing.

---

## Phase 2 — Priority Ranking

Score each screen:

| Factor | Points |
|--------|--------|
| Has critical violations (content inaccessible) | +4 |
| Has serious violations (WCAG AA failure) | +3 |
| Entry point / high traffic (landing, auth, dashboard) | +3 |
| Revenue critical (checkout, pricing, sign-up) | +3 |
| Keyboard navigation broken or trapped | +3 |
| Has moderate violations | +2 |
| Has minor violations | +1 |
| Admin / power-user only | −1 |

Rank highest to lowest. Ask user to confirm before starting Phase 3.

---

## Phase 3 — Recursive Fix Loop

Work through screens in ranked order. Maximum **3 iterations per screen**.

### 3a. Read the violations report
Read the JSON from Phase 1 for this screen. Group by impact: critical → serious → moderate → minor. Read the axe screenshot and keyboard screenshot again.

### 3b. Analyse
For each violation, read the source file to understand the context. Cross-reference with [WCAG.md](WCAG.md) for the correct fix pattern. Categorise:

- **Critical** — screen reader can't access content, keyboard trap, missing lang attribute
- **Major** — color contrast failure, missing form label, image without alt, button without name, non-semantic interactive element
- **Minor** — ARIA misuse, heading skip, missing skip link, small tap target, missing prefers-reduced-motion

### 3c. Fix — structural fixes first, then visual

**Priority order:**
1. Semantic structure (lang, headings, landmarks, lists)
2. Interactive elements (button roles, keyboard access, no onClick on divs)
3. Names and labels (aria-label, alt text, form labels)
4. ARIA correctness (roles, states, properties)
5. Contrast (use HSB adjustments from ui-design-principles)
6. Focus visibility (add `focus-visible:outline` or `focus-visible:ring`)
7. Motion (add `prefers-reduced-motion` if missing)
8. Tap targets (increase padding, not width/height directly)

**Apply fixes automatically — no permission needed:**

```
Semantic HTML:
  <div onClick> → <button>
  <div role="button"> → <button> (unless ARIA role is truly needed)
  <img> missing alt → alt="" for decorative, descriptive alt for informative
  heading skip (h1→h3) → add missing h2

Labels:
  <input> no label → add aria-label or associate <label htmlFor>
  <button> no text → add aria-label describing the action
  icon-only button → add aria-label, add <span className="sr-only">

ARIA:
  aria-label on non-interactive div → move to the interactive child
  role="button" on <a> → remove role, keep <a> with href
  aria-hidden on focusable element → remove aria-hidden or tabIndex={-1}

Contrast:
  Use HSB adjustments: darker = increase S + decrease B
  Prefer token changes over component-level overrides

Focus:
  Add to global CSS or Tailwind config:
    focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand
  Never suppress with: outline: none (unless replacing with custom focus style)

Skip link:
  Add as first child of <body>:
    <a href="#main-content" className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-white focus:text-black">
      Skip to main content
    </a>
  Add id="main-content" to the <main> element.

aria-live regions:
  // Non-urgent announcements (search results, save confirmations)
  <div aria-live="polite" aria-atomic="true" className="sr-only">{statusMessage ?? ''}</div>

  // Urgent interruptions (form errors, session expiry)
  <p role="alert">{errorMessage}</p>

  // CRITICAL: container must be in the DOM BEFORE content changes.
  // Wrong:  {message && <div aria-live="polite">{message}</div>}
  // Right:  <div aria-live="polite" className="sr-only">{message ?? ''}</div>

prefers-reduced-motion:
  In globals.css — verify this rule exists, add if missing:
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
      }
    }
```

### 3d. Re-scan after fixes
```bash
sleep 3  # hot reload
node _a11y_scan.mjs --url http://localhost:3000<ROUTE> --name <name>-after-desktop
node _a11y_scan.mjs --url http://localhost:3000<ROUTE> --name <name>-after-mobile --width 375 --height 812
node _a11y_keyboard.mjs --url http://localhost:3000<ROUTE> --name <name>-after
```

Read the new JSON report. Compare violation counts before and after. Read the screenshots.

Verify:
1. Critical and serious violations cleared?
2. Keyboard focus visible on all interactive elements?
3. Skip link present and functional?
4. All buttons and inputs have accessible names?
5. Contrast ratios pass 4.5:1 (body) and 3:1 (large text, UI components)?

If any critical or serious violations remain: go back to 3c (increment iteration, max 3).

### 3e. Accessibility checklist
Before advancing to the next screen:

- [ ] Zero critical violations in axe report
- [ ] Zero serious violations in axe report
- [ ] `lang` attribute on `<html>` element
- [ ] One `<main>` landmark, one `<h1>` per page
- [ ] Heading hierarchy is sequential (no h1→h3 skip)
- [ ] Skip link is first focusable element, targets `#main-content`
- [ ] Every interactive element reachable by Tab in logical order
- [ ] Every focused element has a visible focus ring (not browser default removed)
- [ ] No keyboard traps (can Tab away from every element, including modals via Escape)
- [ ] Every `<img>` has alt — empty `""` for decorative, descriptive for informative
- [ ] Every `<input>` has an associated `<label>` or `aria-label`
- [ ] Every icon-only button has `aria-label`
- [ ] No `onClick` on non-interactive elements (`<div>`, `<span>`, `<p>`)
- [ ] Color is not the only signal (errors have icon + text, not just color)
- [ ] Body text contrast ≥4.5:1, large text ≥3:1, UI components ≥3:1
- [ ] `prefers-reduced-motion` rule exists in global CSS
- [ ] Touch targets ≥44×44px (verified in keyboard script output)
- [ ] Modal/drawer traps focus while open, returns focus to trigger on close
- [ ] Dynamic content (toasts, errors, search counts, loading completion) wrapped in `aria-live="polite"` or `role="alert"` for urgent messages
- [ ] `aria-live` containers are in the DOM before content changes (not mounted and unmounted with the content)

Any critical/serious fail → go back to 3c. After iteration 3: flag and advance.

---

## Phase 4 — Cleanup & Report

Delete temp scripts:
```bash
rm -f _a11y_scan.mjs _a11y_keyboard.mjs _a11y_auth.mjs
```

After each screen:
```
✓ Screen name (rank N, iteration K) — A critical + B serious + C moderate + D minor fixed
```

Final summary table:

| Rank | Screen | Route | Critical | Serious | Moderate | Minor | Iterations | State |
|------|--------|-------|----------|---------|----------|-------|------------|-------|
| 1    | ...    | ...   | 0        | 0       | ...      | ...   | ...        | ✓ / ⚠ |

List all flagged violations at the bottom with the specific issue that couldn't be resolved.

---

## Rules

1. **Axe-core is the floor, not the ceiling.** It catches ~30–40% of real accessibility issues. The keyboard test and code scan catch the rest.
2. **Read the JSON, not just the count.** Understand what each violation means before fixing.
3. **Semantic HTML beats ARIA.** A real `<button>` is better than `<div role="button">` every time.
4. **Never remove focus styles without replacing them.** `outline: none` is a violation unless a custom focus style replaces it.
5. **Color is never the only signal.** Every state change visible only by color must also use an icon, text, or pattern.
6. **Fix structural issues before visual ones.** Landmarks, headings, and keyboard access first — contrast last.
7. **Max 3 iterations per screen.** Flag remaining issues and move on.
8. **Never change logic or functionality.** Only accessibility attributes, semantic elements, and styles.
9. **Test at 375px too.** Tap targets that pass at desktop may fail at mobile.
10. **Modal focus trapping is non-negotiable.** An open modal that lets focus escape to the background is a critical failure.

---

See [WCAG.md](WCAG.md) for the full WCAG 2.1 AA quick reference and fix patterns.
