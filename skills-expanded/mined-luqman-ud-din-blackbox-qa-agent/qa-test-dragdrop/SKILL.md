---
name: qa-test-dragdrop
section: interactive
description: "Tests drag-and-drop reordering. DETECTION (are there draggable items + drop zones, baseline order) runs as ONE in-page async probe; the actual drag uses the MCP browser_drag tool (native pointer events) with an HTML5 DragEvent fallback. Uses browser_console_messages to detect JS errors during drag."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
requires: [hasDragDrop]
---
# QA Test — Drag and Drop

## How the orchestrator runs this (probe + a drag MCP step)

🚨 This skill is **`executable: partial`**. Native HTML5 drag-and-drop requires real, trusted pointer events (press → move → release) that `browser_evaluate` cannot synthesize for most libraries, so the actual drag stays as an MCP `browser_drag` call. Everything else — finding draggable items, recording baseline order, and verifying whether a reorder occurred — is in-page.

1. ONE detection probe:
   ```
   dragState = browser_evaluate(<the async function in "## Interactive Probe" below>)
   ```
   It self-skips (returns `[]` with `_stateForMcp.found=false`) when there are fewer than 2 draggable items. Transcribe any findings verbatim.
2. If `dragState._stateForMcp.found`, run the **## MCP steps (drag)** below using the tagged selectors / coordinates, then re-call the probe in `verify` mode to assert the reorder.

## Self-skip
The probe returns `_stateForMcp.found=false` when there are no ≥2 visible draggable elements: `[draggable="true"], [class*="sortable"] > *, .drag-handle, [cdkDrag], [class*="cdk-drag"], [data-draggable], [class*="drag-item"]`.

## Interactive Probe (browser_evaluate, async)

```js
async (args) => {
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-dragdrop' }, o));
  args = args || {};

  // ── VERIFY mode: called after the MCP drag to check if the order changed ──
  if (args.mode === 'verify') {
    const container = document.querySelector('[class*="sortable"], [cdkDropList], [class*="drag-list"], [class*="drop-zone"]');
    let reordered = false, firstText = '';
    if (container) {
      const firstItem = [...container.children].find(el => el.getBoundingClientRect().height > 0);
      firstText = firstItem ? (firstItem.innerText || '').trim().slice(0, 60) : '';
      reordered = !!firstItem && firstText !== args.expectedFirstText;
    } else {
      const item0 = args.item0Selector ? document.querySelector(args.item0Selector) : null;
      if (!item0) reordered = true; // item moved out of its tagged DOM position
      else { const parent = item0.parentElement; const fc = parent && [...parent.children].find(c => c.getBoundingClientRect().width > 0); reordered = !!fc && fc !== item0; }
    }
    if (!reordered)
      add({ issueType: 'dragDropBroken', severity: 'high', selector: args.item0Selector || '[data-argus-drag="0"]', description: `Dragging '${args.expectedFirstText}' did not reorder the list (tried both MCP browser_drag and HTML5 DragEvent fallback).`, evidence: { text0: args.expectedFirstText, targetText: args.targetText, fallbackAttempted: !!args.fallbackAttempted, mcpDragAttempted: true } });
    return out;
  }

  // ── HTML5 FALLBACK mode: dispatch synthetic DragEvents (covers CDK/HTML5-only impls) ──
  if (args.mode === 'html5') {
    const source = document.querySelector(`[data-argus-drag="${args.sourceIdx}"]`);
    const target = document.querySelector(`[data-argus-drag="${args.targetIdx}"]`);
    if (!source || !target) return [{ skill: 'qa-test-dragdrop', _dispatched: false }];
    try {
      const dt = new DataTransfer(); dt.setData('text/plain', String(args.sourceIdx));
      source.dispatchEvent(new DragEvent('dragstart', { bubbles: true, cancelable: true, dataTransfer: dt }));
      target.dispatchEvent(new DragEvent('dragenter', { bubbles: true, cancelable: true, dataTransfer: dt }));
      target.dispatchEvent(new DragEvent('dragover',  { bubbles: true, cancelable: true, dataTransfer: dt }));
      target.dispatchEvent(new DragEvent('drop',      { bubbles: true, cancelable: true, dataTransfer: dt }));
      source.dispatchEvent(new DragEvent('dragend',   { bubbles: true, cancelable: true, dataTransfer: dt }));
    } catch (_) {}
    return [];
  }

  // ── CLEANUP mode ──
  if (args.mode === 'cleanup') {
    for (const el of document.querySelectorAll('[data-argus-drag]')) { try { el.removeAttribute('data-argus-drag'); } catch (_) {} }
    return [];
  }

  // ── DETECT mode (default): find ≥2 draggable items, tag them, return coords for the MCP drag ──
  const selectors = ['[draggable="true"]', '[class*="sortable"] > li', '[class*="sortable"] > [class*="item"]', '.drag-handle', '[cdkDrag]', '[class*="cdk-drag"]', '[data-draggable]', '[class*="drag-item"]'];
  let items = [];
  for (const s of selectors) {
    const found = [...document.querySelectorAll(s)].filter(el => { const r = el.getBoundingClientRect(); return r.width > 10 && r.height > 10; });
    if (found.length >= 2) { items = found; break; }
  }
  if (items.length < 2) { out._stateForMcp = { found: false }; return out; }

  const tagged = items.slice(0, 5).map((el, i) => {
    const r = el.getBoundingClientRect();
    el.setAttribute('data-argus-drag', String(i));
    return { idx: i, selector: `[data-argus-drag="${i}"]`, text: (el.innerText || el.getAttribute('aria-label') || `Item ${i+1}`).trim().slice(0, 60), cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2) };
  });
  out._stateForMcp = { found: true, items: tagged };
  return out;
}
```

> The probe attaches a non-ticketed `_stateForMcp` field (tagged items + center coords). Only objects with an `issueType` become tickets.

## MCP steps (drag)

Using `dragState._stateForMcp.items`: let `item0 = items[0]` (source), `item2 = items[min(2, items.length-1)]` (target), `text0 = item0.text`.

1. `browser_take_screenshot()` — baseline.
2. **Primary — MCP native drag:** `browser_drag(startX=item0.cx, startY=item0.cy, endX=item2.cx, endY=item2.cy)` then `browser_wait_for(time=700)`.
3. **Verify:** `browser_evaluate(probe, {mode:'verify', expectedFirstText:text0, item0Selector:item0.selector, targetText:item2.text})`.
   - If it returns no finding → reorder succeeded; skip to step 5.
4. **HTML5 fallback** (if reorder did not occur): `browser_evaluate(probe, {mode:'html5', sourceIdx:item0.idx, targetIdx:item2.idx})`, `browser_wait_for(time=700)`, then `browser_evaluate(probe, {mode:'verify', expectedFirstText:text0, item0Selector:item0.selector, targetText:item2.text, fallbackAttempted:true})`. A returned **dragDropBroken (high)** finding here is the real failure.
5. **JS errors during drag:** `consoleMsgs = browser_console_messages()`; `jsErrors = consoleMsgs.filter(m => m.type === 'error')`. If `jsErrors.length > 0` → emit **dragDropJsError (high)** with `evidence:{firstError: jsErrors[0].text.slice(0,200)}`.
6. **Cleanup:** `browser_evaluate(probe, {mode:'cleanup'})` — removes all `data-argus-drag` attributes.

## Issues
| issueType | severity | description |
|---|---|---|
| dragDropBroken | high | "Dragging '{text0}' to position 3 did not reorder the list (tried both MCP browser_drag and HTML5 DragEvent fallback)" |
| dragDropJsError | high | "Drag-and-drop produced a JavaScript console error: {firstError}" |

## Hard rules

1. **NEVER use** raw Playwright mouse API (`page.mouse.down()`, `page.mouse.move()`, `page.on()`) — unavailable in MCP.
2. **Primary method:** MCP `browser_drag(startX, startY, endX, endY)` handles the real press/move/release.
3. **Fallback method:** HTML5 `DragEvent` dispatch via the probe's `html5` mode — covers CDK / HTML5-only implementations.
4. **JS error detection:** use `browser_console_messages()` — not `page.on('pageerror', ...)`.
5. **Mandatory cleanup** — run the probe's `cleanup` mode to remove all `data-argus-drag` attributes.

## Notes on this conversion
- `executable: partial`. Detection, baseline-order capture, the HTML5 fallback dispatch, reorder verification, and cleanup are all folded into ONE multi-mode `browser_evaluate` probe (`detect` / `verify` / `html5` / `cleanup`). The only step that genuinely needs MCP is the native `browser_drag` pointer drag, which `browser_evaluate` cannot reproduce as trusted events for most drag libraries.
