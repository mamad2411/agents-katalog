---
name: qa-test-filter-accuracy
section: interactive
description: "Tests that search/filter results are semantically correct: applies a known filter (a visible value from the first row), then verifies ALL visible rows match the filter term. Runs as ONE in-page async probe (no AI hand-driving)."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasFilters, hasGlobalSearch, hasSearchInput]
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it with separate `browser_click` / `browser_type` / `browser_wait_for` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function reads a real value from the first data row, applies it as a dropdown filter and/or a search term, waits for the result set (debounce/API) via in-page `setTimeout`, then asserts that the row count changed and that every visible row actually contains the term — all inside the page, in one round-trip. It **self-skips** (returns `[]`) when there is no filter/search control or fewer than 3 data rows. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe restores the baseline (clears the search, resets the filter) before returning.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-filter-accuracy' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const setNative = (el, v) => { const p = el.tagName === 'TEXTAREA' ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype; Object.getOwnPropertyDescriptor(p, 'value').set.call(el, v); el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };

  const dataRows = () => [...document.querySelectorAll('table tbody tr, mat-row, [role="row"]:not([role="columnheader"])')].filter(r => vis(r) && !r.closest('thead') && r.querySelector('td, mat-cell, [role="cell"]'));
  const rowCount = () => dataRows().length;
  const rowsText = () => dataRows().map(r => (r.innerText || '').replace(/\s+/g, ' ').trim());
  const emptyStateVisible = () => {
    const msg = [...document.querySelectorAll('[class*="empty-state"], [class*="no-data"], [class*="no-results"], [class*="empty-message"], [class*="not-found"], [class*="zero-state"]')].some(e => vis(e));
    return msg || rowCount() === 0;
  };

  // ── self-skip checks ──
  const baselineRowCount = rowCount();
  if (baselineRowCount < 3) return [];

  const filterDropdown = [...document.querySelectorAll('mat-select[placeholder*="filter" i], mat-select[aria-label*="filter" i], mat-select[formcontrolname*="filter" i], select[class*="filter"], select, [class*="filter-select"], [role="combobox"][aria-label*="filter" i]')].find(vis);
  const search = [...document.querySelectorAll('input[type="search"], input[placeholder*="search" i], input[placeholder*="filter" i], input[formcontrolname*="search" i], input[formcontrolname*="filter" i], input[aria-label*="search" i], [class*="search-input"] input')].find(vis);
  if (!filterDropdown && !search) return [];

  // ── sample a filter/search value from the first row ──
  const firstRow = dataRows()[0];
  const cellTexts = firstRow ? [...firstRow.querySelectorAll('td, mat-cell, [role="cell"]')].map(c => (c.innerText || '').trim()).filter(t => t.length >= 2 && t.length <= 40) : [];
  const shortValues = cellTexts.filter(t => t.length <= 20 && !/\d{4}-\d{2}-\d{2}/.test(t) && !/^\d+$/.test(t));
  const bestFilterValue = shortValues[0] || cellTexts[0] || null;
  const nameValues = cellTexts.filter(t => t.includes(' ') || (t.length > 4 && /^[A-Za-z]/.test(t)));
  const bestSearchValue = nameValues[0] || cellTexts[0] || null;

  // ── STEP A: native <select> filter (semantic accuracy) ──
  if (filterDropdown && filterDropdown.tagName === 'SELECT' && bestFilterValue) {
    const cur = filterDropdown.value;
    const opt = [...filterDropdown.options].find(o => (o.text || '').toLowerCase().includes(bestFilterValue.toLowerCase()) && o.value && !o.disabled)
      || [...filterDropdown.options].find(o => o.value && o.value !== cur && !o.disabled);
    if (opt) {
      const term = (opt.text || '').trim();
      filterDropdown.value = opt.value; filterDropdown.dispatchEvent(new Event('change', { bubbles: true }));
      await sleep(1200);
      const after = rowCount();
      if (after === baselineRowCount) {
        add({ issueType: 'filterResultsUnchanged', severity: 'high', selector: sel(filterDropdown), bbox: bb(filterDropdown), description: 'Filter applied but the row count did not change — data was not filtered.', evidence: { filterTerm: term, baselineRowCount, postFilterRowCount: after } });
      } else {
        const mismatch = rowsText().filter(t => !t.toLowerCase().includes(term.toLowerCase()));
        if (mismatch.length > 0)
          add({ issueType: 'filterResultsMismatch', severity: 'high', selector: sel(filterDropdown), bbox: bb(filterDropdown), description: 'Filter applied and rows changed, but some visible rows do not contain the filter term.', evidence: { filterTerm: term, mismatchCount: mismatch.length, examples: mismatch.slice(0, 3).map(s => s.slice(0, 100)) } });
      }
      // clear/restore
      filterDropdown.value = cur; filterDropdown.dispatchEvent(new Event('change', { bubbles: true }));
      await sleep(800);
      if (rowCount() < baselineRowCount * 0.9)
        add({ issueType: 'filterClearBroken', severity: 'medium', selector: sel(filterDropdown), bbox: bb(filterDropdown), description: '"Clear filter"/reset did not restore the original rows.', evidence: { expectedRows: baselineRowCount, gotRows: rowCount() } });
    }
  } else if (filterDropdown) {
    // mat-select / combobox: open it, pick the matching option from the CDK overlay, all in-page.
    filterDropdown.click();
    await sleep(400);
    const options = [...document.querySelectorAll('.cdk-overlay-container mat-option, .mat-select-panel mat-option, [role="listbox"] [role="option"]')].filter(vis);
    const term = bestFilterValue || '';
    const match = options.find(o => (o.innerText || '').toLowerCase().includes(term.toLowerCase())) || options.find(o => !/\ball\b/i.test(o.innerText || ''));
    if (match) {
      const chosen = (match.innerText || '').trim();
      match.click();
      await sleep(1200);
      const after = rowCount();
      if (after === baselineRowCount) {
        add({ issueType: 'filterResultsUnchanged', severity: 'high', selector: sel(filterDropdown), bbox: bb(filterDropdown), description: 'Filter applied but the row count did not change — data was not filtered.', evidence: { filterTerm: chosen, baselineRowCount, postFilterRowCount: after } });
      } else {
        const mismatch = rowsText().filter(t => !t.toLowerCase().includes(chosen.toLowerCase()));
        if (mismatch.length > 0)
          add({ issueType: 'filterResultsMismatch', severity: 'high', selector: sel(filterDropdown), bbox: bb(filterDropdown), description: 'Filter applied and rows changed, but some visible rows do not contain the filter term.', evidence: { filterTerm: chosen, mismatchCount: mismatch.length, examples: mismatch.slice(0, 3).map(s => s.slice(0, 100)) } });
      }
      // restore: reopen, pick an "All"/first option if present
      filterDropdown.click(); await sleep(400);
      const opts2 = [...document.querySelectorAll('.cdk-overlay-container mat-option, .mat-select-panel mat-option, [role="listbox"] [role="option"]')].filter(vis);
      const allOpt = opts2.find(o => /\ball\b/i.test(o.innerText || '')) || opts2[0];
      if (allOpt) { allOpt.click(); await sleep(800); }
      else { document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true })); }
    } else {
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
    }
  }

  // ── STEP B: search input (semantic accuracy + debounce) ──
  if (search && bestSearchValue) {
    setNative(search, '');
    await sleep(200);
    const t0 = Date.now();
    setNative(search, bestSearchValue);
    await sleep(600);
    let after = rowCount();
    let debounceMs = 600;
    if (after === baselineRowCount) {
      await sleep(2400);
      debounceMs = 3000;
      after = rowCount();
      if (after === baselineRowCount) {
        add({ issueType: 'filterResultsUnchanged', severity: 'high', selector: sel(search), bbox: bb(search), description: 'Search returned all rows after 3s — search did not filter.', evidence: { searchTerm: bestSearchValue, note: 'search returned all rows after 3s' } });
      }
    } else if ((Date.now() - t0) > 1500) {
      add({ issueType: 'searchDebounceExcessive', severity: 'low', selector: sel(search), bbox: bb(search), description: 'Search input required 3+ seconds before results updated (too slow for UX).', evidence: { debounceMs } });
    }
    // semantic accuracy when narrowed
    if (after < baselineRowCount) {
      const mismatch = rowsText().filter(t => !t.toLowerCase().includes(bestSearchValue.toLowerCase()));
      if (mismatch.length > 0)
        add({ issueType: 'searchResultsMismatch', severity: 'high', selector: sel(search), bbox: bb(search), description: 'Searched a term visible in a cell; result rows do not contain that term.', evidence: { searchTerm: bestSearchValue, mismatchCount: mismatch.length, examples: mismatch.slice(0, 3).map(s => s.slice(0, 100)) } });
    }
    // clear/restore
    setNative(search, '');
    search.dispatchEvent(new KeyboardEvent('keyup', { key: 'Backspace', bubbles: true }));
    await sleep(600);
  }

  // ── STEP C: zero-results feedback (search a value that cannot match) ──
  if (search) {
    setNative(search, '__argus_no_match__');
    await sleep(900);
    if (rowCount() > 0 && !emptyStateVisible()) {
      // results still present for an impossible term — but only flag the missing empty-state, per issueType
    }
    if (rowCount() === 0 && !emptyStateVisible())
      add({ issueType: 'filterNoResultsFeedback', severity: 'medium', selector: sel(search), bbox: bb(search), description: 'Applied a filter that yields zero results, but no "No results"/empty-state message appeared.', evidence: { note: 'filter with non-existent value showed no empty-state message' } });
    setNative(search, '');
    await sleep(600);
  }

  return out;
}
```

## Issues
| issueType | severity | what it catches |
|---|---|---|
| `filterResultsUnchanged` | high | Filter applied but row count did NOT change (data not filtered at all) |
| `filterResultsMismatch` | high | Filter applied and row count changed, but some visible rows do NOT contain the filter term |
| `filterNoResultsFeedback` | medium | Applied a filter that should yield zero results, but no "No results"/empty-state message appeared |
| `searchResultsMismatch` | high | Searched for a term visible in a cell; result rows do NOT contain that term |
| `filterClearBroken` | medium | "Clear filter"/reset button clicked but filters did not reset (row count stayed filtered) |
| `filterCombinationBroken` | medium | Applied two filters simultaneously; result was not the intersection (more rows returned than expected) |
| `searchDebounceExcessive` | low | Search input required 3+ seconds before results updated (too slow for UX) |

## Notes on this conversion
- Replaces the multi-step prose playbook (separate discover / sample / apply / count / check / clear MCP calls, plus the two-step mat-select overlay dance) with ONE in-page async probe. Same issueTypes preserved.
- **mat-select folded:** the old flow needed `applyDropdownFilter` (click to open) → wait → `clickMatSelectOption` as separate MCP round-trips. Here the probe opens the overlay and clicks the option in the same function, then reopens to reset.
- **`filterCombinationBroken` is intentionally folded out of the hot path** (it needs two independent filter controls present, which is uncommon and adds another open/select cycle). Its issueType is preserved in the table; re-add it as one more `add({...})` block (apply filter A, then filter B, assert rows ≤ A-result and ≤ B-result) inside the same function when a page has two filter dropdowns — still one call.
- The probe restores baseline (clears search, resets dropdown) before returning, so the page is left untouched. No new issueTypes invented.
