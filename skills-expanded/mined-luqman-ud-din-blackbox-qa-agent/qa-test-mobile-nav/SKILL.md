---
name: qa-test-mobile-nav
section: interactive
description: "Tests hamburger menu / mobile nav drawer: ARIA label, opens, contains visible links, closes on Escape, focus does not leak to background content. Runs as ONE in-page async probe."
model: haiku
applyOn: [mobile, tablet]
needsSetup: false
viewportSensitive: false
interactive: true
executable: true
requires: [hasNavigation, hasHamburgerMenu]
---

## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate find/click/wait/recheck MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function finds the hamburger toggle, checks its a11y attributes, clicks it open in-page, verifies the drawer is visible with links, checks the background `<main>` is inert/aria-hidden (focus trap), attempts a swipe-to-close, then presses Escape (synthesized `keydown`), and re-checks visibility — returning `findings[]` in one round-trip. It does its own waits via in-page `setTimeout` promises, so there is **no AI reasoning between steps**. It **self-skips** (returns `[]`) when no hamburger toggle is found. The probe restores the drawer to its original open/closed state before returning. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

Run on **mobile/tablet only** (the orchestrator gates `applyOn: [mobile, tablet]`).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-mobile-nav' }, o));
  const qFirst = sels => { for (const s of sels) { let el; try { el = document.querySelector(s); } catch (_) { continue; } if (el) { const r = el.getBoundingClientRect(); if (r.width > 0 && r.height > 0) return { el, usedSel: s }; } } return null; };
  const selOf = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  const TOGGLE_SELS = [
    'button[aria-label*="menu" i]', 'button[aria-label*="navigation" i]',
    '.hamburger', '[data-testid*="menu-toggle"]', '[data-testid*="nav-toggle"]',
    'button[aria-controls*="menu" i]', 'button[aria-controls*="nav" i]',
    'button[aria-expanded][class*="menu"]', 'button[aria-expanded][class*="nav"]',
    'button[aria-label*="toggle" i]', 'button[aria-label*="sidenav" i]',
    '[class*="sidenav-toggle"]', '[class*="menu-toggle"]',
    'mat-icon[aria-label*="menu" i]', 'button mat-icon'
  ];
  const DRAWER_SELS = [
    '[role="dialog"][aria-modal="true"]',
    'nav[aria-hidden="false"]',
    '[class*="drawer"]:not([aria-hidden="true"])',
    '[class*="mobile-nav"]:not([aria-hidden="true"])',
    '[class*="nav-menu"][class*="open"]',
    '[data-state="open"][class*="nav"]',
    'mat-sidenav[opened]', 'mat-sidenav.mat-drawer-opened',
    'mat-sidenav:not([style*="visibility: hidden"])', '.mat-drawer-opened mat-sidenav'
  ];

  const findDrawer = () => {
    for (const s of DRAWER_SELS) { let el; try { el = document.querySelector(s); } catch (_) { continue; } if (!el) continue; const r = el.getBoundingClientRect(); const st = getComputedStyle(el); if (r.width > 50 && r.height > 50 && st.display !== 'none' && st.visibility !== 'hidden') return el; }
    return null;
  };

  // ── find toggle (self-skip) ──
  const toggle = qFirst(TOGGLE_SELS);
  if (!toggle) return [];
  const t = toggle.el;
  const wasOpen = t.getAttribute('aria-expanded') === 'true';

  // ── a11y of the toggle ──
  const hasAriaLabel = t.hasAttribute('aria-label') && (t.getAttribute('aria-label') || '').trim().length > 0;
  const hasVisibleText = (t.innerText || t.textContent || '').trim().length > 0;
  const hasAriaExpanded = t.hasAttribute('aria-expanded');
  if (!hasAriaLabel && !hasVisibleText)
    add({ issueType: 'hamburgerNoAriaLabel', severity: 'medium', selector: selOf(t), bbox: bb(t), description: 'Hamburger button has no aria-label and no visible text — screen readers can\'t identify it.', evidence: {} });
  if (!hasAriaExpanded)
    add({ issueType: 'hamburgerNoAriaExpanded', severity: 'medium', selector: selOf(t), bbox: bb(t), description: 'Hamburger button is missing aria-expanded — screen readers won\'t announce open/closed state.', evidence: {} });

  // ── open it (unless already open) ──
  if (!wasOpen) { t.click(); await sleep(500); }

  let drawer = findDrawer();
  if (!drawer) {
    add({ issueType: 'mobileNavDoesNotOpen', severity: 'high', selector: selOf(t), bbox: bb(t), description: 'Clicking hamburger toggle did not open a visible navigation drawer.', evidence: {} });
    return out;
  }

  // ── count links ──
  const links = [...drawer.querySelectorAll('a[href], button[role="link"]')].filter(a => { const r = a.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
  if (links.length < 1)
    add({ issueType: 'mobileNavEmpty', severity: 'high', selector: selOf(drawer), bbox: bb(drawer), description: 'Mobile nav drawer opened but contains no visible navigation links.', evidence: { linkCount: 0 } });

  // ── focus trap: background main inert/aria-hidden ──
  const main = document.querySelector('main, [role="main"], #main, #content, .main-content');
  if (main && !main.hasAttribute('inert') && main.getAttribute('aria-hidden') !== 'true') {
    const tabbable = [...main.querySelectorAll('a[href]:not([tabindex="-1"]), button:not([disabled]):not([tabindex="-1"]), input:not([disabled]):not([type="hidden"]):not([tabindex="-1"]), select:not([disabled]):not([tabindex="-1"]), textarea:not([disabled]):not([tabindex="-1"]), [tabindex]:not([tabindex="-1"])')].filter(el => !drawer.contains(el));
    if (tabbable.length > 0)
      add({ issueType: 'drawerNoFocusTrap', severity: 'high', selector: selOf(drawer), bbox: bb(drawer), description: `Mobile nav drawer is open but background <main> has no inert/aria-hidden — ${tabbable.length} tabbable elements leak outside drawer.`, evidence: { tabbableCount: tabbable.length } });
  }

  // ── swipe-to-close ──
  if (typeof window.TouchEvent !== 'undefined' && typeof window.Touch !== 'undefined') {
    const r = drawer.getBoundingClientRect();
    if (r.width > 0 && r.height > 0) {
      const startX = r.left + r.width * 0.7, startY = r.top + r.height * 0.5, endX = r.left - 30;
      try {
        const mk = (x, y) => new Touch({ identifier: Date.now(), target: drawer, clientX: x, clientY: y, radiusX: 10, radiusY: 10, force: 1 });
        drawer.dispatchEvent(new TouchEvent('touchstart', { bubbles: true, cancelable: true, touches: [mk(startX, startY)] }));
        drawer.dispatchEvent(new TouchEvent('touchmove', { bubbles: true, cancelable: true, touches: [mk((startX + endX) / 2, startY)] }));
        drawer.dispatchEvent(new TouchEvent('touchmove', { bubbles: true, cancelable: true, touches: [mk(endX, startY)] }));
        drawer.dispatchEvent(new TouchEvent('touchend', { bubbles: true, cancelable: true, touches: [], changedTouches: [mk(endX, startY)] }));
      } catch (_) {}
      await sleep(500);
      if (findDrawer())
        add({ issueType: 'mobileNavNoSwipeClose', severity: 'low', selector: selOf(drawer), bbox: bb(drawer), description: 'Mobile nav drawer did not close on left-swipe gesture — swipe-to-dismiss not implemented.', evidence: {} });
    }
  }

  // ── Escape to close ──
  const escTarget = findDrawer() || drawer;
  escTarget.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true }));
  document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true }));
  await sleep(400);
  if (findDrawer())
    add({ issueType: 'mobileNavWontClose', severity: 'medium', selector: selOf(drawer), bbox: bb(drawer), description: 'Mobile nav drawer did not close on Escape key — focus trap / dismiss risk.', evidence: {} });

  // ── restore original state ──
  if (!wasOpen && findDrawer()) { try { t.click(); await sleep(300); } catch (_) {} }
  else if (wasOpen && !findDrawer()) { try { t.click(); await sleep(300); } catch (_) {} }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| hamburgerNoAriaLabel | medium | "Hamburger button has no aria-label and no visible text — screen readers can't identify it" |
| hamburgerNoAriaExpanded | medium | "Hamburger button is missing aria-expanded — screen readers won't announce open/closed state" |
| mobileNavDoesNotOpen | high | "Clicking hamburger toggle did not open a visible navigation drawer" |
| mobileNavEmpty | high | "Mobile nav drawer opened but contains no visible navigation links" |
| drawerNoFocusTrap | high | "Mobile nav drawer is open but background <main> has no inert/aria-hidden — {N} tabbable elements leak outside drawer" |
| mobileNavNoSwipeClose | low | "Mobile nav drawer did not close on left-swipe gesture — swipe-to-dismiss not implemented" |
| mobileNavWontClose | medium | "Mobile nav drawer did not close on Escape key — focus trap risk" |

## Notes on this conversion
- This replaces the old 12-step orchestrator flow (find → a11y → click → wait → check-visible → count-links → focus-trap → swipe → wait → Escape → wait → recheck) with ONE async `browser_evaluate`. All waits are in-page `setTimeout` promises, so there is **no AI reasoning between steps**.
- All 7 issueTypes preserved.
- The Escape press is synthesized in-page as a `keydown` event (instead of a `browser_press_key` MCP call); the swipe uses a synthetic `TouchEvent` sequence, guarded by a `TouchEvent` feature check.
- The probe restores the drawer's original open/closed state before returning, so the next skill sees a clean page.
