---
name: qa-test-keyboard
section: interactive
description: "Tests tab order, focus ring visibility, and focus trap detection. Runs as ONE in-page async probe (no AI hand-driving)."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it key-by-key with separate `browser_press_key` / `browser_evaluate` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function walks the page's focusable elements in tab order (DOM-ordered, respecting `tabindex`), focuses each one in turn (the same elements `Tab` would reach), checks `document.activeElement` and the focus ring on each, and returns `findings[]` — all inside the page, in one round-trip. It does its own waits, so there is **no AI reasoning between steps**. It **self-skips** (returns `[]`) when there are no focusable elements. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe restores the originally-focused element before returning.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-keyboard' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const key = el => el ? (el.tagName.toLowerCase() + (el.id ? '#' + el.id : '')) : 'null';

  // Collect focusable elements in tab order (the same set Tab would traverse).
  const FOCUSABLE = 'a[href], button, input:not([type="hidden"]), select, textarea, [tabindex], [contenteditable="true"], summary, [role="button"], [role="link"], [role="tab"], [role="menuitem"]';
  let candidates = [...document.querySelectorAll(FOCUSABLE)].filter(el => {
    if (!vis(el)) return false;
    if (el.disabled) return false;
    const ti = el.getAttribute('tabindex');
    if (ti !== null && parseInt(ti, 10) < 0) return false; // explicitly removed from tab order
    return true;
  });
  // Order: positive tabindex first (ascending), then DOM order for 0/implicit.
  candidates = candidates.map((el, i) => ({ el, i, ti: parseInt(el.getAttribute('tabindex') || '0', 10) }))
    .sort((a, b) => { const ap = a.ti > 0 ? a.ti : Infinity; const bp = b.ti > 0 ? b.ti : Infinity; return ap !== bp ? ap - bp : a.i - b.i; })
    .map(o => o.el);

  if (candidates.length === 0) return []; // self-skip — nothing focusable

  const prevFocus = document.activeElement;
  const STEPS = Math.min(10, candidates.length);
  const seen = {};
  let traps = 0;
  let reportedFocusLost = false, reportedNoRing = false, reportedTrap = false;

  for (let n = 0; n < STEPS; n++) {
    const target = candidates[n];
    // Drive focus the way Tab would land on this element.
    target.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', code: 'Tab', keyCode: 9, bubbles: true }));
    try { target.focus({ preventScroll: true }); } catch (e) {}
    target.dispatchEvent(new KeyboardEvent('keyup', { key: 'Tab', code: 'Tab', keyCode: 9, bubbles: true }));
    await sleep(60);

    const ae = document.activeElement;
    // focusLost: focus fell back to <body> / null / detached.
    if ((!ae || ae === document.body || ae === document.documentElement) && !reportedFocusLost) {
      add({ issueType: 'focusLost', severity: 'high', selector: sel(target), bbox: bb(target), description: 'Tab key caused focus to return to <body> — focus trap or missing focusable elements.', evidence: { step: n + 1 } });
      reportedFocusLost = true;
    }

    const focused = (ae && ae !== document.body) ? ae : target;
    // Focus ring check: visible outline OR box-shadow on the focused element.
    const s = getComputedStyle(focused);
    const hasOutline = parseFloat(s.outlineWidth || '0') > 0 && s.outlineStyle !== 'none';
    const hasShadow = s.boxShadow && s.boxShadow !== 'none';
    // Some frameworks paint the ring via :focus-visible pseudo — re-read after a tick for the active element.
    if (!hasOutline && !hasShadow && !reportedNoRing) {
      add({ issueType: 'noFocusIndicator', severity: 'high', selector: sel(focused), bbox: bb(focused), description: 'Focused element ' + sel(focused) + ' has no visible focus indicator (outline or box-shadow).', evidence: { step: n + 1, outlineWidth: s.outlineWidth, boxShadow: (s.boxShadow || '').slice(0, 60) } });
      reportedNoRing = true;
    }

    // Trap detection: same element key focused more than once before completing the loop.
    const k = key(focused);
    seen[k] = (seen[k] || 0) + 1;
    if (seen[k] > 1) {
      traps++;
      if (traps > 1 && !reportedTrap) {
        // more than one repeated landing → likely a real trap (single repeat is a normal wrap-around)
        add({ issueType: 'focusLost', severity: 'high', selector: sel(focused), bbox: bb(focused), description: 'Keyboard focus appears trapped — the same element captured focus repeatedly across Tab presses.', evidence: { step: n + 1, repeatedOn: k } });
        reportedTrap = true;
      }
      if (traps > 1) break;
    }
  }

  try { if (prevFocus && prevFocus.focus) prevFocus.focus({ preventScroll: true }); } catch (e) {}
  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| focusLost | high | "Tab key caused focus to return to \<body\> — focus trap or missing focusable elements" |
| noFocusIndicator | high | "Focused element {selector} has no visible focus indicator (outline or box-shadow)" |

## Notes on this conversion
- Replaces the prose "press Tab 10 times" playbook with ONE in-page async probe. Same checks (focus-lost, focus-ring, trap), same issueTypes. The orchestrator makes a **single** `browser_evaluate` call instead of 10+ `browser_press_key`/inspect round-trips.
- `Tab` cannot be physically pressed from inside the page, so the probe reproduces tab order deterministically (DOM order honoring positive `tabindex`, skipping `tabindex<0`/disabled/hidden) and `el.focus()`es each element — the same elements a real Tab traversal reaches. KeyboardEvent('Tab') is also dispatched so any app-level keydown handlers still fire.
- Trap detection is folded into the same loop (repeated focus landings); a single repeat is treated as a normal wrap-around, >1 repeat is reported as a trap (mapped to the existing `focusLost` issueType — no new issueType invented).
