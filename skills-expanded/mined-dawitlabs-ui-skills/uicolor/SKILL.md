---
name: uicolor
description: Color master skill. Audits every color decision across the product — balance, hierarchy, harmony, temperature, saturation, shadow construction, hover states — and corrects them using HSB color theory. Extracts the actual rendered color palette from every screen, identifies what's wrong and why, then fixes it systematically. Use when colors feel off, the UI looks flat or garish or cold, brand color is everywhere or nowhere, or the user invokes /uicolor.
---

# /uicolor — Color Correction & Balance

The color master. Reads the rendered UI, extracts the real color distribution, diagnoses every imbalance, and corrects it with precision using HSB theory. Works screen by screen, always verifying visually.

Full color theory reference: [COLOR-THEORY.md](COLOR-THEORY.md)

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

### 0b. Find source root and token home
```bash
find . -type d -name "src" -not -path "*/node_modules/*" -not -path "*/.next/*" \
  -not -path "*/dist/*" -not -path "*/.turbo/*" | head -1

find . \( -name "globals.css" -o -name "variables.css" \) -not -path "*/node_modules/*" | head -3
find . -name "tailwind.config.*" -not -path "*/node_modules/*" | head -2
```

Read the token home file(s) — note every color value already defined. These are the values being corrected, not replaced from scratch.

### 0c. Read the DESIGN-BRIEF.md if present
```bash
cat DESIGN-BRIEF.md 2>/dev/null | head -60
```
The brief's **Color System** section tells you the intended direction (temperature, saturation, primary hex). Use it as the north star — you are correcting toward this intent, not away from it.

### 0d. Write the color analysis script
Write to the **project root** (needs node_modules). Deleted in Phase 4.

**`_uicolor_extract.mjs`** — extracts the rendered color palette with coverage percentages:
```js
import { chromium } from '@playwright/test';
import { mkdirSync, writeFileSync } from 'fs';

const get = (f) => { const i = process.argv.indexOf(f); return i !== -1 ? process.argv[i+1] : null; };
const url    = get('--url')    ?? 'http://localhost:3000';
const name   = get('--name')   ?? 'screen';
const width  = parseInt(get('--width')  ?? '1280');
const height = parseInt(get('--height') ?? '900');
const auth   = get('--auth');

mkdirSync('/tmp/uicolor', { recursive: true });

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

// Screenshot for visual reading
await page.screenshot({ path: `/tmp/uicolor/${name}.png`, fullPage: true });

// Extract color distribution from rendered elements
const palette = await page.evaluate(() => {
  const colorArea = new Map();
  const totalArea = document.documentElement.scrollHeight * window.innerWidth;

  document.querySelectorAll('*').forEach(el => {
    const rect   = el.getBoundingClientRect();
    const absTop = rect.top + window.scrollY;
    const area   = rect.width * (rect.height || 1);
    if (area < 100) return; // skip tiny elements

    const style = getComputedStyle(el);
    const props = ['backgroundColor', 'color', 'borderTopColor', 'outlineColor'];

    props.forEach(prop => {
      const val = style[prop];
      if (!val || val === 'rgba(0, 0, 0, 0)' || val === 'transparent') return;
      // Normalise to rgba string as key
      colorArea.set(val, (colorArea.get(val) ?? 0) + (prop === 'backgroundColor' ? area : area * 0.1));
    });
  });

  // Convert to sorted array with coverage %
  return [...colorArea.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 20)
    .map(([color, area]) => ({
      color,
      coverage: Math.round((area / totalArea) * 1000) / 10, // % of page area
    }));
});

// Parse rgb values to hex for readability
const toHex = (rgb) => {
  const m = rgb.match(/\d+/g);
  if (!m || m.length < 3) return rgb;
  return '#' + m.slice(0, 3).map(n => parseInt(n).toString(16).padStart(2, '0')).join('');
};

const result = {
  url,
  viewport: `${width}×${height}`,
  palette: palette.map(p => ({ ...p, hex: toHex(p.color) })),
};

writeFileSync(`/tmp/uicolor/${name}-palette.json`, JSON.stringify(result, null, 2));
await browser.close();

console.log(`screenshot: /tmp/uicolor/${name}.png`);
console.log(`palette:    /tmp/uicolor/${name}-palette.json`);
palette.slice(0, 10).forEach(p => console.log(`  ${toHex(p.color).padEnd(10)} ${p.coverage}%`));
```

**Usage:**
```bash
node _uicolor_extract.mjs --url http://localhost:3000 --name home
node _uicolor_extract.mjs --url http://localhost:3000/dashboard --name dashboard --auth /tmp/uiux-auth-state.json
node _uicolor_extract.mjs --url http://localhost:3000 --name home-mobile --width 375 --height 812
```

**After every run: read the screenshot AND the palette JSON.**

### 0e. Handle auth-protected screens
```bash
ls /tmp/uiux-auth-state.json /tmp/animate-auth-state.json /tmp/copy-auth-state.json 2>/dev/null | head -1
```
If found, pass `--auth <path>` to all script calls for protected routes.

---

## Phase 1 — Color Audit

### 1a. Run color extraction on every screen
```bash
node _uicolor_extract.mjs --url http://localhost:3000 --name home
node _uicolor_extract.mjs --url http://localhost:3000 --name home-mobile --width 375 --height 812
```
Repeat for every distinct screen. **Read every screenshot and every palette JSON.**

For each screen, record:
- The top 3 colors by coverage % — these are the dominant, secondary, accent (should match 60-30-10)
- The full palette — look for colors that appear at <1% coverage (decorative noise) or unexpected colors
- Whether any single hue dominates at >40% coverage (saturation fatigue)

### 1b. Check color roles
For each color in the palette, determine its role:

| Role | Should be | % coverage |
|------|-----------|------------|
| Background / dominant | Neutral surface | 50–65% |
| Secondary | Slightly elevated surface, sidebar | 20–30% |
| Text | Dark neutral | 10–20% (applied to text elements) |
| Primary / accent | Brand color | ≤10% |
| Semantic colors | Success, error, warning | ≤5% total |

**Flag immediately:**
- Primary/brand color > 15% coverage → brand dilution (everything screams, nothing does)
- More than 3 distinct background shades → surface chaos
- Pure black (#000000) used for shadows → flat and harsh
- Pure gray neutrals with no hue whisper → dead, lifeless surfaces
- All hover states are the same color as their base → no feedback

### 1c. Read the token definitions
Cross-reference every color in the palette with the token file. For each:
- Does it have a token name? (Good)
- Is it hardcoded? (Flag for /tokens)
- Is the token name semantic? (`--color-primary` vs `--blue`) — flag non-semantic names

### 1d. Squint test — color hierarchy
Take the screenshot of the most complex screen. Squint until blurry. Ask:
1. What is the first color your eye goes to?
2. Is that the most important element on the screen?
3. Do any background elements compete with foreground elements in color weight?

If the answers are wrong → color hierarchy is broken.

### 1e. Temperature audit
For every neutral surface and text color: is the temperature consistent?

```bash
# Extract all CSS color values from token file
grep -E "color:|background:|border:" globals.css tailwind.config.* 2>/dev/null | grep -v "var(--" | head -30
```

Convert each to HSB. Check:
- All neutrals should have the same hue whisper (warm: H 20–50°, cool: H 200–240°)
- Mixing warm grays and cool grays on the same screen = temperature clash
- Brand color temperature should match neutral temperature direction

Present the full audit grouped by screen before continuing.

---

## Phase 2 — Priority Ranking

Score each issue:

| Issue | Points |
|-------|--------|
| Brand/primary color > 15% coverage (dilution) | +4 |
| Temperature clash (warm + cool neutrals mixed) | +4 |
| Color hierarchy wrong (accent on background, not foreground) | +4 |
| Shadow is pure black (no hue tint) | +3 |
| More than 3 distinct background shades | +3 |
| Hover state = base state (no color feedback) | +3 |
| Neutral grays are pure (no hue whisper) | +2 |
| Semantic colors used decoratively (green used for non-success) | +2 |
| Saturation inconsistency across same-role elements | +2 |
| Text colors don't follow a clear scale | +2 |
| On high-traffic / first-impression screen | +2 |
| Color blindness risk (red/green only distinction) | +2 |

Rank by score. Highest = fix first. Ask user to confirm before Phase 3.

---

## Phase 3 — Recursive Color Fix Loop

Work through issues in ranked order. Maximum **3 iterations per screen**.

### 3a. Screenshot before
Run `_uicolor_extract.mjs` for this screen. **Read the screenshot and palette JSON.**
State in one sentence: what does the color feel like right now? (Cold and flat? Garish? Muddy? Lifeless?)

### 3b. Diagnose the root cause
Every color problem has one of five root causes:

1. **Wrong value** — the hex is simply wrong (too saturated, wrong temperature)
2. **Wrong role** — a color is being used for the wrong purpose (primary used decoratively)
3. **Missing variation** — only one shade of a color exists, so states can't be distinguished
4. **Missing hue whisper** — neutrals are pure gray, creating a lifeless palette
5. **Missing shadow tint** — shadows are pure black instead of hue-tinted

Identify the root cause before writing any fix.

### 3c. Fix — apply HSB adjustments precisely

**Rules from [COLOR-THEORY.md](COLOR-THEORY.md) applied automatically:**

```
Brand dilution (primary used everywhere):
  → Keep primary on: CTAs, links, focus rings, active nav items, badges
  → Replace on: decorative icons, background fills, section dividers
  → Replace with: neutral-600 for icons, surface colors for backgrounds

Temperature correction:
  → Convert current neutral hex to HSB
  → Adjust hue: toward 30° for warm, toward 220° for cool
  → Keep S ≤ 8% (barely perceptible — a whisper, not a tint)
  → Recheck against brand primary temperature — they should agree

Shadow construction:
  → Bad:  box-shadow: 0 4px 6px rgba(0,0,0,0.1)
  → Good: take surface color HSB → increase S by 30% → decrease B by 60% → use at 0.12–0.20 opacity
  → Example: white surface (#ffffff) → shadow: 0 4px 6px rgba(0, 0, 40, 0.12)
  → Example: blue-50 surface (#eff6ff) → shadow: 0 4px 6px rgba(30, 60, 120, 0.12)

Hover state construction:
  → Hover (darker): S+10, B-15, hue toward 0°/120°/240°
  → Active/pressed: S+15, B-25 (more dramatic than hover)
  → Disabled: S-30, B+10, opacity 0.5
  → Focus ring: brand primary at full S+B, 2px offset

Neutral hue whisper:
  → Pure gray: hsl(0, 0%, 97%) → add whisper: hsl(220, 8%, 97%)
  → The hue should match the brand primary's temperature direction
  → S between 3–8% — visible in isolation, invisible when focused on content

Text color scale:
  → Primary text: brand-neutral-900 (or equivalent)
  → Secondary text: brand-neutral-500 (not pure gray — use hue-tinted neutral)
  → Disabled text: brand-neutral-400
  → Never more than 4 levels of text gray

60-30-10 correction:
  → Measure coverage from palette JSON
  → If primary > 10%: audit every use, keep only interactive elements
  → If no element < 5% coverage: the accent has no room to breathe — reduce secondary color
```

**Fix in the token file first, then verify component usage.** A single token change fixes 50 components.

### 3d. Screenshot after
```bash
sleep 3  # hot reload
node _uicolor_extract.mjs --url http://localhost:3000<ROUTE> --name <name>-after
```
**Read the screenshot and the new palette JSON.**

Compare palette JSONs before and after:
- Did the primary color coverage drop to ≤10%?
- Did the neutral hue shift in the right direction?
- Is the temperature consistent across all neutrals?

Apply the squint test again. Ask:
1. Does the screen feel warmer/cooler/more balanced than before?
2. Does the primary color now pop against the background?
3. Do shadows have depth, or do they still look painted on?

If any answer is wrong: go back to 3c (increment iteration, max 3).

### 3e. Color checklist
Before advancing to the next screen:

- [ ] Primary/brand color ≤10% coverage on any screen (from palette JSON)
- [ ] All neutrals have a consistent hue whisper — same temperature direction
- [ ] No pure-gray neutrals (HSB S = 0%) on any surface
- [ ] All shadows are hue-tinted, not pure black
- [ ] Hover states are visually distinct from base (S+10 B-15 minimum)
- [ ] Active/pressed states are visually distinct from hover
- [ ] Text follows a ≤4-level gray scale, all hue-consistent
- [ ] No semantic color (success green, error red) used decoratively
- [ ] No red/green combination used as the only distinction between two states
- [ ] Squint test: eye goes to the highest-priority element first
- [ ] Temperature is consistent — no warm/cool clash within a single screen
- [ ] Before/after palette JSON shows coverage shift in the right direction

Any fail → go back to 3c. After iteration 3: flag and advance.

---

## Phase 4 — Cleanup & Report

Delete temp scripts:
```bash
rm -f _uicolor_extract.mjs
```

After each screen:
```
✓ Screen name (rank N, iteration K) — primary coverage: 23% → 8%, shadows tinted, neutrals warmed
```

Final summary:

| Screen | Primary Coverage Before | After | Temperature | Shadow | Iterations | State |
|--------|------------------------|-------|-------------|--------|------------|-------|
| Home   | 28%                    | 7%    | ✓ warm      | ✓ tinted | 2        | ✓ |

**Palette before/after** — list every token that changed, old value and new value.

List all flagged issues at the bottom.

---

## Rules

1. **Read the screenshot first. Always.** Color problems are felt before they're measured. Look at the image, then look at the numbers.
2. **Fix the token, not the component.** A color that's wrong in 40 places has one wrong token definition.
3. **HSB is the tool.** Never adjust colors by guessing hex values. Convert to HSB, apply the rule, convert back.
4. **60-30-10 is a visual law, not a suggestion.** If primary coverage is 25%, everything else fights it. Reduce it.
5. **Neutrals are never truly neutral.** A pure gray looks cold on a warm brand and warm on a cool brand — always add a hue whisper.
6. **Shadows have color.** Pure black shadows flatten the UI. Tinted shadows add depth.
7. **Temperature is a system decision.** Never mix warm and cool neutrals. Pick a direction and commit.
8. **Semantic colors are sacred.** Green = success. Red = error. Using green for branding and error states destroys the signal.
9. **Max 3 iterations per screen.** Flag and move on.
10. **Never change logic, layout, or component structure.** Only color values.

---

See [COLOR-THEORY.md](COLOR-THEORY.md) for HSB reference, hue temperature charts, shadow construction formulas, and the complete 60-30-10 guide.
