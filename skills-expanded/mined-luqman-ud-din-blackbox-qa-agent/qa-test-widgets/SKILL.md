---
name: qa-test-widgets
section: interactive
description: "Tests modal open/close, dropdown selection, and row action menus. Runs as ONE in-page async probe (no AI hand-driving)."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasAccordion, hasCarousel, hasTabs, hasTreeView]
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it click-by-click with separate `browser_click` / `browser_press_key` / `browser_wait_for` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function detects every modal trigger / dropdown / action menu, opens it, asserts the result (open/close/select), and returns `findings[]` — all inside the page, in one round-trip. It does its own waits (animation/API) via in-page `setTimeout` promises, so there is **no AI reasoning between clicks** (this is what makes it cheap + fast + un-skippable). It **self-skips** (returns `[]`) when no widgets are present. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe closes everything it opened (Escape + close-button) before returning.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-widgets' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const txt = el => (el.innerText || el.textContent || el.value || el.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim();
  const esc = () => document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, bubbles: true }));
  const modalVisible = () => [...document.querySelectorAll('[role="dialog"], .modal.show, [aria-modal="true"], [class*="modal"][class*="open"]')].some(vis);
  const TRIGGER_TXT = /^(open|add|new|create|edit)\b/i;

  // ── self-skip ──
  const anyWidget = document.querySelector('[data-modal-trigger], [data-bs-toggle="modal"], button[aria-haspopup="dialog"], [aria-haspopup="listbox"], [role="combobox"], .dropdown-toggle, [data-testid*="dropdown"], [data-testid*="action-menu"], [data-testid*="row-action"], button[aria-label*="more" i], button[aria-label*="actions" i]');
  const anyTriggerBtn = [...document.querySelectorAll('button')].find(b => vis(b) && (TRIGGER_TXT.test(txt(b)) || txt(b) === '⋮'));
  if (!anyWidget && !anyTriggerBtn) return [];

  // ── MODALS (up to 3) ──
  const modalTriggers = [
    ...document.querySelectorAll('[data-modal-trigger], [data-bs-toggle="modal"], button[aria-haspopup="dialog"]'),
    ...[...document.querySelectorAll('button')].filter(b => TRIGGER_TXT.test(txt(b)))
  ].filter((el, i, a) => vis(el) && a.indexOf(el) === i).slice(0, 3);

  for (const trig of modalTriggers) {
    if (modalVisible()) esc(), await sleep(200);
    const label = txt(trig).slice(0, 30);
    trig.click(); await sleep(500);
    if (!modalVisible()) {
      add({ issueType: 'modalWontOpen', severity: 'high', selector: sel(trig), bbox: bb(trig), description: `Clicking "${label}" did not open a modal or dialog`, evidence: { label } });
      continue;
    }
    const dialog = [...document.querySelectorAll('[role="dialog"], .modal.show, [aria-modal="true"], [class*="modal"][class*="open"]')].find(vis);
    // close via close-button
    const closeBtn = dialog && [...dialog.querySelectorAll('button[aria-label*="close" i], .close, [data-dismiss], [data-bs-dismiss="modal"], button[class*="close"]')].find(vis);
    if (closeBtn) { closeBtn.click(); await sleep(300); }
    if (modalVisible()) {
      add({ issueType: 'modalWontClose', severity: 'high', selector: sel(dialog), bbox: bb(dialog), description: `Modal opened but could not be closed via close button`, evidence: { method: 'close-button', label } });
      esc(); await sleep(200);
    }
    // re-open then test Escape
    if (!modalVisible()) {
      trig.click(); await sleep(500);
      if (modalVisible()) {
        esc(); await sleep(300);
        if (modalVisible()) {
          const d2 = [...document.querySelectorAll('[role="dialog"], .modal.show, [aria-modal="true"]')].find(vis);
          add({ issueType: 'modalWontClose', severity: 'high', selector: sel(d2 || trig), bbox: bb(d2 || trig), description: `Modal opened but could not be closed via Escape key`, evidence: { method: 'Escape', label } });
          // best-effort close button
          const cb2 = d2 && [...d2.querySelectorAll('button[aria-label*="close" i], .close, [data-dismiss]')].find(vis);
          if (cb2) { cb2.click(); await sleep(200); }
        }
      }
    }
    esc(); await sleep(200);
  }

  // ── DROPDOWNS (up to 3) ──
  const dropdowns = [...document.querySelectorAll('[aria-haspopup="listbox"], [role="combobox"], .dropdown-toggle, [data-testid*="dropdown"]')].filter(vis).slice(0, 3);
  for (const dd of dropdowns) {
    const before = txt(dd).slice(0, 60);
    dd.click(); await sleep(300);
    const menu = [...document.querySelectorAll('[role="listbox"], .dropdown-menu.show, [class*="dropdown-menu"][class*="open"]')].find(vis);
    const options = [...document.querySelectorAll('[role="option"], .dropdown-item')].filter(vis);
    if (!menu && options.length === 0) {
      add({ issueType: 'dropdownBroken', severity: 'high', selector: sel(dd), bbox: bb(dd), description: 'Dropdown trigger clicked but no option list appeared', evidence: { before } });
      continue;
    }
    // pick second option (or first if only one)
    const pick = options[1] || options[0];
    if (pick) {
      pick.click(); await sleep(300);
      const after = txt(dd).slice(0, 60);
      if (after === before)
        add({ issueType: 'dropdownBroken', severity: 'high', selector: sel(dd), bbox: bb(dd), description: 'Dropdown option selected but the trigger value did not change', evidence: { before, picked: txt(pick).slice(0, 40) } });
    }
    esc(); await sleep(150);
  }

  // ── ACTION MENUS (up to 3) ──
  const actionMenus = [
    ...document.querySelectorAll('button[aria-label*="more" i], button[aria-label*="actions" i], [data-testid*="action-menu"], [data-testid*="row-action"]'),
    ...[...document.querySelectorAll('button')].filter(b => txt(b) === '⋮' || txt(b) === '⋯' || txt(b) === '…')
  ].filter((el, i, a) => vis(el) && a.indexOf(el) === i).slice(0, 3);
  for (const am of actionMenus) {
    am.click(); await sleep(300);
    const menu = [...document.querySelectorAll('[role="menu"], [role="menuitem"], .dropdown-menu.show')].find(vis);
    if (!menu)
      add({ issueType: 'actionMenuBroken', severity: 'high', selector: sel(am), bbox: bb(am), description: 'Row action menu button (⋮) clicked but no menu appeared', evidence: { label: txt(am).slice(0, 30) } });
    esc(); await sleep(150);
  }

  esc(); // final cleanup
  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| modalWontOpen | high | "Clicking \"{label}\" did not open a modal or dialog" |
| modalWontClose | high | "Modal opened but could not be closed via {method}" |
| dropdownBroken | high | "Dropdown trigger clicked but no option list appeared" |
| actionMenuBroken | high | "Row action menu button (⋮) clicked but no menu appeared" |

## Notes on this conversion
- Replaces the old multi-step prose playbook with ONE in-page async probe. Same checks, same 4 issueTypes — the orchestrator makes a **single** `browser_evaluate` call instead of driving 20+ MCP steps.
- The original `:has-text()` selectors (Playwright-only) were folded into in-page `innerText` matching (`TRIGGER_TXT` for Open/Add/New/Create/Edit, and `⋮` for action menus) so everything runs in DOM JS.
- `dropdownBroken` now also fires when the menu opens but selecting an option doesn't change the trigger value (the second half of the original dropdown test), preserving the original two-part check under the same issueType.
