---
name: mobile
description: Mobile adaptation with hardened rules from real production iterations. Uniform scale factor, preserve composition, no JS→scroll-snap swap, iOS ?v=N cache-bust, text nowrap in collapsed cards. Ends with a headless-browser safety check (text overflow, safe paddings, no horizontal scroll, tap-target sizes) across 320/375/390/414/480/768. Runs only when priority=desktop-first.
---

# /mobile

Skill hardened by real iterations. All rules below come from projects where mobile ate weeks and hundreds of fixes.

## When to use

- `brief/00-priority.md` = `desktop-first`.
- After `/build` (desktop version ready).
- Edits to an existing mobile version.

**If mobile-first** — this skill does not apply. Mobile is built directly in `/build`, desktop is extended via `expansion.css`.

## Requirements

- Desktop version exists and works.
- All sections assembled, `/audit` shows desktop = pass.
- `site/css/responsive.css` exists (empty template).

## Rules (must-follow)

### 1. Breakpoints
- `≤ 768px` = mobile (hamburger active, layout adapted).
- `≤ 480px` = small-phone (targeted fixes where general mobile rules are insufficient).

### 2. Preserve desktop composition
**Do NOT restructure blocks.** Do not change element order inside a section. Do not swap layouts (grid → stack without reason).
Scale proportionally in the same positioning.

Exception: if an element physically does not fit (e.g. a horizontal-timeline of 6 steps does not work at 390px) — make an explicit decision to restructure and log it in `DESIGN.md`.

### 3. Uniform scale factor per block
Within one block — one multiplier for all sizes (card:phone ratio, gap, margin, height). Otherwise proportions break.

Example: if desktop `.card { width: 20vw; }` → mobile `.card { width: 45vw; }` (×2.25). Then gap, phone-mockup, and everything inside — also ×2.25.

### 4. Preserve JS-driven carousels
**Never** turn a JS carousel into CSS `scroll-snap` on mobile. Never set `transform: none !important` on `.track` — it will kill the JS.

If a different visual is needed — change sizes/gap, but not the behavior type.

### 5. Text in collapsed cards — nowrap + ellipsis
When a card is scaled down, inner text must:
```css
white-space: nowrap;
overflow: hidden;
text-overflow: ellipsis;
```

Otherwise lines spill sideways or wrap to new lines.

### 6. Font-size via clamp()
`font-size: clamp(min_px, Nvw, max_px)` instead of raw `Nvw`. Guarantees text does not collapse to invisibility at 320px.

Example: `clamp(10px, 1.2vw, 16px)`.

### 7. Min sizes
- Text: ≥ 12px.
- Tap targets (buttons, links, checkboxes): ≥ 44×44px (Apple HIG standard).
- Feature objects (large phone mockups, feature cards): ≥ 25vw to remain recognizable.

### 8. Kill inline-transform JS parallax on touch
If `main.js` writes `transform` per scroll frame — on touch it jitters. In `responsive.css` for mobile:
```css
.parallax-target {
  transform: none !important;
}
```
Or `scale(1.08)` — a static enlarged variant.

Apply to: `.hero__img`, `.about__portrait img`, `.card__img img`, any `--parallax` elements.

### 9. iOS Safari CSS cache-bust
After CSS edits Safari on iOS often ignores changes even on force-reload.

**Rule:** after every significant CSS/JS change in prod — increment `?v=N` on every `<link rel="stylesheet">` and `<script>` in HTML.

Automation — by hand or via a script:
```powershell
# PowerShell example
(Get-Content site/index.html) -replace '\?v=(\d+)', '?v=$($matches[1] + 1)' | Set-Content site/index.html
```

## Process

**Step 1. Read every section**
Walk `site/index.html` — enumerate sections. All need adaptation.

**Step 2. Per section — determine the scale factor**
Take base font-size on mobile ÷ base on desktop = multiplier.
Usually ×2 – ×2.5 for vw-based sizes.

**Step 3. Edits in responsive.css**
All mobile edits — in `site/css/responsive.css`. NOT in the base section CSS.

Structure:
```css
@media (max-width: 768px) {
  /* HEADER */
  .site-header__nav { display: none; }
  .site-header__burger { display: block; }

  /* HERO */
  .sec-hero { ... }

  /* ... per section ... */

  /* CARDS with shrink — nowrap + ellipsis */
  .card__title, .card__caption {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Kill parallax */
  .hero__img, .about__portrait img {
    transform: none !important;
  }
}
```

**Step 4. Test**
Run local server + Chrome DevTools mobile emulator + real iOS if available.
Walk through key breakpoints: 320, 375, 390, 414, 480, 768.

**Step 5. Verify cache-bust**
After edits — increment `?v=N` in `index.html`.

**Step 6. Report**
What was adapted, where problems may remain, what was tested on real devices.

**Step 7. Safety check (automated)**

Run the site through a headless browser at each key breakpoint and verify:

**Test matrix:** viewports 320, 375, 390, 414, 480, 768. iPhone Safari + Android Chrome user-agent.

**For each breakpoint:**

1. **Serve the built site.** Launch a local static server (e.g. `python -m http.server 8000`) if not already running.
2. **Navigate the headless browser** to the site (use the browser skill available in this environment).
3. **Set the viewport width** to the breakpoint value.
4. **Capture a screenshot** to `site/_mobile-check/screens/<breakpoint>.png`.

**Checks per breakpoint:**

- **No horizontal scroll.** Assert `document.documentElement.scrollWidth === window.innerWidth`. Fail on mismatch (means something overflows).
- **Text overflow.** For every text element (`h1`-`h6`, `p`, `li`, `blockquote`, `.card__title`, etc.), get its bounding rect and the client size. If the element has `overflow: hidden` AND `scrollHeight > clientHeight` AND does not have `text-overflow: ellipsis` — fail (means text is silently clipped).
- **Safe paddings.** Every `.sec` element must have effective `padding-left` and `padding-right` ≥ 16px on ≤ 480px viewports, ≥ 24px on 481–768px. Fail on shortage.
- **Section spacing.** Vertical gap between adjacent sections ≥ 24px on mobile. Fail on shortage.
- **Tap-target size.** Every button, link, input, `[role="button"]`, checkbox, radio — bounding rect min(width, height) ≥ 44px. Fail per instance.
- **Absent elements.** Every element that has a desktop counterpart but is `display: none` on mobile — verify user intentionally hid it (cross-check `references/approved-manifest.md`; if the item is an approved manifest entry that got hidden, fail).

**Output:** `site/_mobile-check-report.md`

```markdown
# Mobile safety check — 2026-08-08 17:00

## Verdict: ❌ FAIL

## Screenshots
- 320px: screens/320.png
- 375px: screens/375.png
- 390px: screens/390.png
- 414px: screens/414.png
- 480px: screens/480.png
- 768px: screens/768.png

## Failures
1. **Horizontal scroll @ 375px**
   `.sec-hero` scrollWidth=390, viewport=375. Overflowing element: `.hero__badge` (right: -12px).
2. **Text clipped @ 375px**
   `.card__caption:nth-child(3)`: scrollHeight=42, clientHeight=24, overflow:hidden, no ellipsis. Copy: "Delivered in under two weeks, from…"
3. **Unsafe padding @ 320px**
   `.sec-form`: padding-left=8px, min required=16px.
4. **Tap target too small @ 375px**
   `.footer__social a`: 32×32, min required=44×44.

## Warnings
1. **Hidden manifest item @ 375px**
   `[x] motif: horizontal thin rule between sections` — display: none in mobile media query. If intentional, remove from manifest with decision-log entry.

## Passes
- 320, 480, 768 breakpoints: passed all checks (screenshots attached).
```

**If verdict = FAIL**, `/audit` will refuse to progress (verifies this file in category H).

**Warnings do not block**, but user should review before shipping.

## Rules of behavior

- **Do not edit desktop CSS.** Only `responsive.css` + careful `.mobile-*` classes if truly needed.
- **Every scale factor is justified.** No "tried ×2".
- **Test on a real device.** Emulator ≠ Safari iOS. Especially for `position: sticky` and touch behavior.
- **Never hide an approved manifest item silently on mobile.** If mobile can't accommodate it, log a decision and remove it from the manifest.

## What NOT to do

- Do not carry desktop parallax onto mobile (rule 8).
- Do not turn a JS carousel into scroll-snap (rule 4).
- Do not change font/color/spacing tokens — they are desktop-independent.
- Do not "improve" desktop under the pretext of mobile.
- Do not skip Step 7 — the safety check is what catches "text is cut off, we shipped it anyway".

## Next

- `/audit` — pre-ship check (also includes mobile emulation check).
