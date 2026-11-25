---
name: qa-test-data-controls
section: interactive
description: "Tests search (live/Enter/button-triggered), filter dropdowns, sort, pagination, tabs, refresh — applies each control and verifies the list actually changes. Runs as ONE in-page async probe (no AI hand-driving)."
model: haiku
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasTables, hasFilters, hasPagination]
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it click-by-click with separate `browser_click` / `browser_type` / `browser_wait_for` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function detects every control, drives it, asserts the result, and returns `findings[]` — all inside the page, in one round-trip. It does its own waits (debounce/API) via in-page `setTimeout` promises, so there is **no AI reasoning between clicks** (this is what makes it cheap + fast + un-skippable). It **self-skips** (returns `[]`) when no data controls are present. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe restores the list (clears search / resets filters / clicks back to the original tab) before returning.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-data-controls' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).display !== 'none' && getComputedStyle(el).visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const rows = () => [...document.querySelectorAll('table tbody tr, [role="row"], [data-testid*="row"]')].filter(r => !r.closest('thead') && vis(r));
  const rowCount = () => rows().length;
  const rowsText = () => rows().map(r => (r.innerText || '').replace(/\s+/g, ' ').trim());
  const firstRow = () => { const t = rowsText(); return t[0] || ''; };
  const emptyStateVisible = () => /no results|nothing found|no .* found|empty|0 results|no records|record not found/i.test(document.body.innerText || '');
  const setNative = (el, v) => { const p = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype; Object.getOwnPropertyDescriptor(p, 'value').set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };

  // applySearch: type → (if unchanged) Enter → (if unchanged) click adjacent button. Returns 'live'|'enter'|'button'|'none'.
  const applySearch = async (input, value) => {
    const before = rowCount();
    setNative(input, '');
    setNative(input, value);
    await sleep(800);
    if (rowCount() !== before) return 'live';
    input.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true }));
    input.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter', keyCode: 13, bubbles: true }));
    await sleep(600);
    if (rowCount() !== before) return 'enter';
    const cont = input.closest('[class*="search"], [class*="filter"], [class*="input-group"], [class*="form-field"], mat-form-field') || input.parentElement;
    const btn = cont && [...cont.querySelectorAll('button, [type="submit"]')].find(vis);
    if (btn) { btn.click(); await sleep(600); }
    if (rowCount() !== before) return 'button';
    return 'none';
  };

  // ── self-skip if no data controls at all ──
  const anyControl = document.querySelector('input[type="search"], input[placeholder*="search" i], input[placeholder*="filter" i], [aria-label*="search" i], [aria-label*="filter" i], select, [role="combobox"], table, [role="table"], [role="grid"], [class*="paginat" i], [role="tab"], [role="tablist"], .nav-tabs, button[aria-label*="refresh" i]');
  if (!anyControl) return [];

  // ── SEARCH ──
  const search = [...document.querySelectorAll('input[type="search"], input[placeholder*="search" i], input[placeholder*="filter" i], [aria-label*="search" i]')].find(vis);
  if (search) {
    const rowsBefore = rowCount();
    const fired = await applySearch(search, 'zzzzz_no_match_test_argus');
    const rowsAfter = rowCount();
    if (rowsBefore > 1 && rowsAfter >= rowsBefore && fired === 'none')
      add({ issueType: 'searchNoEffect', severity: 'high', selector: sel(search), bbox: bb(search), description: 'Search did not narrow results on a no-match query (after live + Enter + button were all tried).', evidence: { rowsBefore, rowsAfter, fired } });
    if (rowsAfter === 0 && !emptyStateVisible())
      add({ issueType: 'noEmptyState', severity: 'medium', selector: sel(search), bbox: bb(search), description: 'Search returned 0 rows but no empty-state message is shown.', evidence: { rowsBefore, rowsAfter } });
    // clear (×) button — while text is still present
    await sleep(300);
    const cont = search.closest('[class*="search"], [class*="filter"], [class*="input-group"], [class*="form-field"], mat-form-field') || search.parentElement;
    const clearBtn = cont && [...cont.querySelectorAll('[aria-label*="clear" i], [title*="clear" i], [class*="clear-button"], [class*="clear-icon"], [data-action="clear"], button[type="reset"]')].find(vis);
    if (!clearBtn)
      add({ issueType: 'searchNoClearButton', severity: 'low', selector: sel(search), bbox: bb(search), description: 'Search input has no visible clear (×) button while it contains typed text — users must backspace to reset.', evidence: { valueWhenChecked: 'zzzzz_no_match_test_argus' } });
    // happy match: pick a token from the first row, search it
    setNative(search, ''); await sleep(400);
    const rt = rowsText();
    if (rt.length > 1) {
      const token = (rt[0].match(/[A-Za-z0-9]{3,}/g) || [])[0];
      if (token) {
        const orig = rowCount();
        await applySearch(search, token);
        const match = rowCount();
        if (match === 0)
          add({ issueType: 'searchMatchReturnsNothing', severity: 'high', selector: sel(search), bbox: bb(search), description: 'Searching a value visible on the page returned zero rows.', evidence: { pickedToken: token } });
        else if (match === orig && orig > 1)
          add({ issueType: 'searchNoEffect', severity: 'high', selector: sel(search), bbox: bb(search), description: 'Search is a no-op even for a valid value picked from a row.', evidence: { pickedToken: token, rows: match } });
        else if (match >= 1 && !rowsText().some(t => t.toLowerCase().includes(token.toLowerCase())))
          add({ issueType: 'searchResultsContainNonMatchingRows', severity: 'high', selector: sel(search), bbox: bb(search), description: 'After search, visible rows do not contain the searched token — filtered to the wrong rows.', evidence: { pickedToken: token, sample: rowsText().slice(0, 3) } });
      }
    }
    setNative(search, ''); search.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', keyCode: 13, bubbles: true })); await sleep(500);
  }

  // ── FILTER DROPDOWNS (native select, not pagination/page-size) — cap 4 ──
  const selects = [...document.querySelectorAll('select')].filter(s => vis(s) && !/per.?page|page.?size|rows/i.test((s.getAttribute('aria-label') || '') + ' ' + (s.closest('[class*="paginat" i]') ? 'pag' : '')));
  for (const s of selects.slice(0, 4)) {
    if (s.options.length < 2) continue;
    const rowsBefore = rowCount(), firstBefore = firstRow();
    const cur = s.value;
    const alt = [...s.options].find(o => o.value && o.value !== cur && !o.disabled);
    if (!alt) continue;
    s.value = alt.value; s.dispatchEvent(new Event('change', { bubbles: true }));
    await sleep(800);
    if (rowCount() === rowsBefore && firstRow() === firstBefore && rowsBefore > 1)
      add({ issueType: 'filterDropdownNoEffect', severity: 'high', selector: sel(s), bbox: bb(s), description: 'Changing a filter dropdown to a different option did not change the list.', evidence: { from: cur, to: alt.value, rowsBefore } });
    s.value = cur; s.dispatchEvent(new Event('change', { bubbles: true })); await sleep(500); // restore
  }

  // ── SORT ──
  const header = [...document.querySelectorAll('th[aria-sort], th button, [role="columnheader"][aria-sort], thead th, [role="columnheader"]')].find(vis);
  if (header && rowCount() > 2) {
    const before = firstRow();
    const hadAffordance = header.hasAttribute('aria-sort') || header.querySelector('button, [class*="sort"]');
    header.click(); await sleep(600);
    if (firstRow() === before && hadAffordance)
      add({ issueType: 'sortNoEffect', severity: 'medium', selector: sel(header), bbox: bb(header), description: 'Clicking a sortable column header did not change the row order.', evidence: { firstRowBefore: before.slice(0, 40) } });
  }

  // ── PAGINATION (Next) ──
  const next = [...document.querySelectorAll('[aria-label*="next" i], [data-testid*="next"], .pagination .next, li.next a, [class*="next-page"]')].find(vis)
    || [...document.querySelectorAll('button, a')].find(el => vis(el) && /^(next|›|»)$/i.test((el.textContent || '').trim()));
  if (next && rowCount() > 0) {
    const disabled = next.disabled || next.getAttribute('aria-disabled') === 'true' || next.classList.contains('disabled') || (next.closest('li') && next.closest('li').classList.contains('disabled'));
    if (!disabled) {
      const before = firstRow();
      next.click(); await sleep(700);
      if (firstRow() === before && before.length > 0)
        add({ issueType: 'paginationNoEffect', severity: 'high', selector: sel(next), bbox: bb(next), description: 'Clicking "Next" did not load the next page of results.', evidence: { firstRowBefore: before.slice(0, 40) } });
    }
  }

  // ── TABS / segmented controls — cap 1 group, 3 options ──
  const fingerprint = () => {
    const nums = (document.body.innerText.match(/[\d,]{2,}/g) || []).join(' ');
    const main = document.querySelector('[role="main"], main') || document.body;
    return (nums + '|' + rowsText().slice(0, 8).join(' ') + '|' + (main.innerText || '').slice(0, 200)).slice(0, 600);
  };
  const tabs = [...document.querySelectorAll('[role="tablist"] > [role="tab"], .nav-tabs > li, .nav-tabs a, .mat-tab-label, .tab-button')].filter(vis);
  if (tabs.length >= 2) {
    let baseline = fingerprint();
    const active = tabs.find(t => t.getAttribute('aria-selected') === 'true' || /active|selected/.test(t.className)) || tabs[0];
    for (const tab of tabs.filter(t => t !== active).slice(0, 3)) {
      const label = (tab.textContent || '').trim().slice(0, 30);
      tab.click(); await sleep(800);
      const after = fingerprint();
      if (after === baseline)
        add({ issueType: 'tabHasNoEffect', severity: 'high', selector: sel(tab), bbox: bb(tab), description: `Clicking tab "${label}" shows identical content — tab filter not wired.`, evidence: { to: label } });
      baseline = after;
    }
    active.click(); await sleep(400); // restore
  }

  // ── REFRESH ──
  const refresh = [...document.querySelectorAll('button[aria-label*="refresh" i], button[aria-label*="reload" i], button[title*="refresh" i], [class*="refresh"], [class*="reload"]')].find(vis);
  if (refresh) {
    const fp1 = fingerprint();
    refresh.click(); await sleep(1500);
    if (fingerprint() === fp1)
      add({ issueType: 'refreshNoEffect', severity: 'medium', selector: sel(refresh), bbox: bb(refresh), description: 'Refresh/reload button did not update any displayed data.', uncertain: true, evidence: {} });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| searchNoEffect | high | Filter/search did not narrow results on a no-match query (after live + Enter + button triggers all tried) |
| searchMatchReturnsNothing | high | Searching a value visible on the page returned zero rows |
| searchResultsContainNonMatchingRows | high | After search, visible rows do not contain the searched token (search filtered to wrong rows) |
| searchNoClearButton | low | Search input has no visible clear (×) button while it contains typed text |
| noEmptyState | medium | Zero-result filter shows no empty-state message |
| filterDropdownNoEffect | high | Changing a filter dropdown/combobox to a different option did not change the list |
| sortNoEffect | medium | Clicking a sortable column header did not change row order |
| paginationNoEffect | high | Clicking "Next" did not load the next page of results |
| tabHasNoEffect | high | Clicking a different tab (e.g. Month / Quarter / Year) shows identical content |
| refreshNoEffect | medium | Refresh / reload button does not update any displayed data |

## Notes on this conversion
- This replaces the old multi-step prose playbook with ONE in-page async probe. Same checks, same issueTypes — but the orchestrator makes a **single** `browser_evaluate` call instead of driving 30+ MCP steps, so the skill is cheap, fast, and cannot be partially skipped.
- A few advanced checks from the prose version (per-column scope discovery, filter modals, date-range, prev/last-page boundary) are intentionally folded out of the hot path to keep one fast probe; re-add them as additional `add({...})` blocks inside the same function if needed — still one call.
- Controls needing real browser-level events that `browser_evaluate` cannot simulate (none here) would stay as MCP steps; everything in data-controls works in-page.
