---
name: qa-test-idempotency
section: interactive
description: "Tests that double-clicking submit does not allow duplicate form submissions. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasForms, hasActionButtons]
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_click` / `browser_wait_for` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function finds the first visible form, fills its required inputs with safe test values, clicks submit twice in quick succession, checks whether the button disabled itself after the first click, and counts success messages — all inside the page, in one round-trip. It does its own waits via in-page `setTimeout` promises. It **self-skips** (returns `[]`) when there is no visible form. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …).

**SAFETY:** This probe submits a form once (with a double-click) using throwaway test values. It does not create a marked record it can clean up, so it relies on the run config gating interactive submission. If the run does not allow live submission, do not invoke this skill.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-idempotency' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const setNative = (el, v) => { const p = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype; Object.getOwnPropertyDescriptor(p, 'value').set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };
  const isDisabled = btn => !!(btn.disabled || btn.getAttribute('aria-disabled') === 'true' || btn.classList.contains('disabled') || (btn.closest('[aria-disabled="true"], .disabled')) || /loading|spinner|submitting/i.test(btn.className) || btn.querySelector('[class*="spinner"], [class*="loading"]'));

  // ── self-skip if no visible form ──
  const form = [...document.querySelectorAll('form')].find(vis);
  if (!form) return [];

  const submitBtn = [...form.querySelectorAll('button[type="submit"], input[type="submit"], button:not([type="button"]):not([type="reset"])')].find(vis);
  if (!submitBtn) return [];

  // Fill up to 3 required inputs with safe test values.
  const required = [...form.querySelectorAll('input[required]:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="checkbox"]):not([type="radio"]), textarea[required]')].filter(vis).slice(0, 3);
  for (const el of required) {
    const tp = (el.type || '').toLowerCase();
    if (tp === 'email') setNative(el, 'test@example.com');
    else if (tp === 'password') setNative(el, 'TestPass123!');
    else if (tp === 'number') setNative(el, '99');
    else if (tp === 'tel') setNative(el, '+923001234567');
    else if (tp === 'url') setNative(el, 'https://example.com');
    else setNative(el, 'test');
  }
  // Required selects/checkboxes (best-effort).
  for (const s of [...form.querySelectorAll('select[required]')].filter(vis).slice(0, 2)) {
    const o = [...s.options].find(o => o.value && !o.disabled); if (o) { s.value = o.value; s.dispatchEvent(new Event('change', { bubbles: true })); }
  }
  for (const c of [...form.querySelectorAll('input[required][type="checkbox"]')].filter(vis).slice(0, 2)) {
    if (!c.checked) c.click();
  }

  await sleep(100);

  // First click.
  submitBtn.click();
  await sleep(250);
  const isDisabledAfterFirst = isDisabled(submitBtn);

  // Second (double) click.
  submitBtn.click();
  await sleep(600);

  if (!isDisabledAfterFirst) {
    const successEls = [...document.querySelectorAll('[role="alert"], .alert-success, [class*="success"], [data-testid*="success"], [class*="toast"], [class*="snackbar"]')].filter(vis);
    if (successEls.length > 1) {
      add({ issueType: 'doubleSubmitAllowed', severity: 'high', selector: sel(submitBtn), bbox: bb(submitBtn), description: 'Submit button is not disabled after first click — double-submission may create duplicate records.', evidence: { isDisabledAfterFirst, successMessageCount: successEls.length } });
    }
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| doubleSubmitAllowed | high | "Submit button is not disabled after first click — double-submission may create duplicate records" |

## Notes on this conversion
- Replaces the prose playbook with ONE in-page async probe. Same check, same issueType. The orchestrator makes a **single** `browser_evaluate` call instead of fill/click/wait/inspect round-trips.
- `isDisabled()` was broadened beyond the prose `btn.isDisabled()` to also treat `aria-disabled`, a `.disabled` class, and an in-button spinner/loading affordance as "disabled after first click" — these are the common ways apps guard against double-submit, and counting them avoids false positives.
- Required `select`/`checkbox` filling was added so the first submit is more likely to actually fire (otherwise validation blocks it and the test is inconclusive). No new issueTypes.
