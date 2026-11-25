---
name: qa-test-export
section: interactive
description: "Tests file download/export functionality: detects Export/Download buttons, verifies they are enabled, wired to a real href/handler (not a dead # / javascript:void(0)), offer a format choice, and trigger a download or feedback. The DETECTION runs as ONE in-page async probe; downloaded-file content verification stays a short MCP step because a real browser download cannot be read from inside browser_evaluate."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
cacheVersion: "1.0.0"
requires: [hasExportOption]
---
## How the orchestrator runs this (ONE probe call + optional MCP download-verify)

🚨 **The DETECTION half of this skill is an EXECUTABLE in-page probe.** Make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function scans for export/download controls, checks they are enabled, checks format variety, clicks the primary export control in-page, drives any export-config dialog, and inspects the resulting DOM for a triggered download link / file URL / data URI and for user feedback — returning `findings[]` in one round-trip. It does its own waits via in-page `setTimeout` promises. It **self-skips** (returns `[]`) when no export/download control exists — except it emits a single `exportButtonNotFound` (low) when the page has a data table but no export control. The probe removes its own `data-argus-export*` marker attributes before returning. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields.

**`executable: partial`** — the probe covers Phase-1 download-*trigger* detection (does an export button exist, is it enabled, is it wired, does it offer formats, does clicking it surface a download/feedback). It CANNOT read the bytes of a real browser download, so **Phase-2 content verification (file vs on-screen table) stays a short MCP step** — see "## MCP steps (download verify)" below. The orchestrator runs the MCP step ONLY when the probe reports `downloadTriggered: true` in its envelope finding.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-export' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const selOf = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  const exportRe = /\b(export|download|csv|excel|xls|xlsx|pdf|print)\b/i;
  const hasDataTable = !!document.querySelector('table, mat-table, [role="grid"], [class*="data-table"]');

  // ── scan export controls ──
  const candidates = [...document.querySelectorAll('button, [role="button"], a[download], a[href*="export"], a[href*="download"], a[href*=".csv"], a[href*=".pdf"], a[href*=".xlsx"], [aria-label*="export" i], [aria-label*="download" i]')]
    .filter(vis)
    .filter(el => exportRe.test(el.innerText || el.getAttribute('aria-label') || el.title || el.getAttribute('href') || ''));

  if (candidates.length === 0) {
    if (hasDataTable) add({ issueType: 'exportButtonNotFound', severity: 'low', selector: 'table', description: 'Page has a data table/list but no export/download button is visible.', evidence: {} });
    return out;
  }

  // formats + enabled set
  const formats = [];
  candidates.forEach((el, i) => {
    el.setAttribute('data-argus-export', String(i));
    const label = (el.innerText || el.getAttribute('aria-label') || el.title || '').trim();
    if (/csv/i.test(label)) formats.push('csv');
    else if (/excel|xls/i.test(label)) formats.push('excel');
    else if (/pdf/i.test(label)) formats.push('pdf');
    else if (/print/i.test(label)) formats.push('print');
    else formats.push('generic');
  });
  const cleanup = () => { for (const el of document.querySelectorAll('[data-argus-export], [data-argus-export-confirm]')) { try { el.removeAttribute('data-argus-export'); el.removeAttribute('data-argus-export-confirm'); } catch (_) {} } };
  const enabled = candidates.filter(el => !el.disabled && el.getAttribute('aria-disabled') !== 'true' && getComputedStyle(el).pointerEvents !== 'none');

  if (enabled.length === 0) {
    add({ issueType: 'exportButtonDisabled', severity: 'medium', selector: selOf(candidates[0]), bbox: bb(candidates[0]), description: 'Export button(s) present but all are disabled (aria-disabled / pointer-events:none).', evidence: {} });
    cleanup();
    return out;
  }

  const uniqFormats = [...new Set(formats)];
  if (uniqFormats.length === 1 && hasDataTable)
    add({ issueType: 'exportMissingFormatChoice', severity: 'low', selector: selOf(enabled[0]), bbox: bb(enabled[0]), description: 'Only one export format is available on a page with rich data (no CSV+PDF/Excel choice).', evidence: { availableFormats: uniqFormats } });

  // ── click the primary export control ──
  const primary = enabled[0];
  const primaryLabel = (primary.innerText || primary.getAttribute('aria-label') || '').trim().slice(0, 80);
  primary.click();
  await sleep(600);

  // ── export-config dialog? drive the confirm button ──
  const findDialog = () => { const d = document.querySelector('[role="dialog"][aria-modal="true"]:not([aria-hidden="true"]), mat-dialog-container, .swal2-popup:not([aria-hidden="true"])'); if (d) { const r = d.getBoundingClientRect(); if (r.width > 0) return d; } return null; };
  let dialog = findDialog();
  if (dialog) {
    const confirm = [...dialog.querySelectorAll('button')].find(b => /\b(export|download|confirm|ok|proceed|generate)\b/i.test(b.innerText || ''));
    if (confirm) { confirm.click(); await sleep(1000); }
    if (findDialog())
      add({ issueType: 'exportDialogBroken', severity: 'medium', selector: selOf(dialog), bbox: bb(dialog), description: 'An export-config dialog appeared but its Confirm/Export button did not dismiss it or proceed.', evidence: { buttonLabel: primaryLabel } });
  }

  // ── wait for download / tab, then inspect DOM ──
  await sleep(2500);
  let downloadTriggered = false, linkBroken = false, href = null;
  const dl = [...document.querySelectorAll('a[download], a[href*=".csv"], a[href*=".pdf"], a[href*=".xlsx"], a[href^="blob:"], a[href^="data:"]')];
  if (dl.length > 0) {
    downloadTriggered = true;
    const h = dl[0].getAttribute('href') || '';
    if (!h || h === '#' || h.startsWith('javascript:')) { linkBroken = true; href = h; }
    else href = h.slice(0, 200);
  } else if (/\.(csv|pdf|xlsx|xls|zip|txt)(\?.*)?$/i.test(location.href)) {
    downloadTriggered = true; href = location.href;
  }

  if (!downloadTriggered)
    add({ issueType: 'exportNoDownloadTriggered', severity: 'high', selector: selOf(primary), bbox: bb(primary), description: 'Export button clicked but after ~3s no download link, file URL, or data URI appeared and no new tab opened.', evidence: { buttonLabel: primaryLabel } });
  if (linkBroken)
    add({ issueType: 'exportLinkBroken', severity: 'high', selector: selOf(primary), bbox: bb(primary), description: 'Export download link href is blank, "#", or javascript:void(0) with no download attribute.', evidence: { href } });

  // ── feedback (toast / spinner / progress) ──
  const hasFeedback = [...document.querySelectorAll('mat-snack-bar-container, [class*="snackbar"], [class*="toast"], [role="alert"], .alert-success, [class*="success-message"], mat-progress-bar, [class*="loading"], [class*="progress"]')].some(vis);
  if (!hasFeedback)
    add({ issueType: 'exportNoFeedback', severity: 'medium', selector: selOf(primary), bbox: bb(primary), description: 'Export initiated but no loading indicator, toast, or progress appeared while the download was pending.', evidence: { buttonLabel: primaryLabel } });

  // envelope finding so the orchestrator knows whether to run the MCP content-verify step
  add({ issueType: '_exportProbeMeta', severity: 'info', selector: selOf(primary), description: 'Phase-1 export-trigger detection complete. downloadTriggered drives whether the MCP Phase-2 content-verify step runs.', evidence: { downloadTriggered, href, primaryLabel, hasDataTable } });

  cleanup();
  return out;
}
```

## MCP steps (download verify) — Phase 2, runs only if `downloadTriggered: true`

`browser_evaluate` cannot read the bytes of a real browser download, so file-vs-table content verification stays a short MCP-driven step. Run it ONLY when the probe's `_exportProbeMeta` finding reports `downloadTriggered: true`. (Drop `_exportProbeMeta` from the JSONL — it is an internal signal, not a bug.)

```
PRE-CLICK (before re-triggering the export for content capture):
  a. snapshot = browser_evaluate(probe.captureTableSnapshot)   // headers, first 5 rows verbatim, totalRowCount from pager
  b. Write snapshot to {runId}/exports/{cellId}-snapshot.json
  c. exportDir = "{project-root}/.tmp/{runId}/exports/{cellId}"  ;  mkdir -p {exportDir}
  d. Arm MCP download routing to {exportDir} (browser_handle_download / context.expect_download), timeout 8000.

CLICK + VERIFY:
  e. browser_click(primary export control)  →  await the download
  f. downloadInfo = await downloadPromise
     If timed out → exportNoDownloadTriggered already emitted by the probe; skip Phase 2.
  g. exportFile = downloadInfo.path
     If !exportFile OR fileSize === 0 → emit exportContentEmpty (high); skip remainder.
  h. node scripts/verify-export.cjs {exportFile} {snapshotPath}
     Parse stdout JSON { findings: [...] } — each finding is emitted as-is. verify-export.cjs fires:
       exportContentEmpty / exportContentMissingColumns / exportContentRowCountMismatch / exportContentCellMismatch.
  i. Cleanup: rm {exportFile} and {snapshotPath}.

FILTER-THEN-EXPORT (catches "export ignores active filter"):
  j. If a filter input/dropdown is visible: pick a value from row 1 col 1, apply it (qa-test-data-controls applySearch pattern),
     confirm visible rows decreased, re-capture a filtered snapshot, repeat (e)-(h) — verify-export.cjs fires exportIgnoresFilter
     if the export contains rows that don't match the filter. Reset the filter to '' afterward.
```

`probe.captureTableSnapshot` (for the MCP step):

```js
() => {
  const tables = [...document.querySelectorAll('table, mat-table, [role="grid"], [role="table"]')].filter(t => { const r = t.getBoundingClientRect(); return r.width > 100 && r.height > 50; });
  if (tables.length === 0) return { headers: [], rows: [], totalRowCount: 0, filterApplied: null, filteredValue: null };
  const table = tables[0];
  let headerCells = [...table.querySelectorAll('thead th, thead [role="columnheader"]')];
  if (headerCells.length === 0) headerCells = [...table.querySelectorAll('[role="columnheader"]')];
  if (headerCells.length === 0) headerCells = [...(table.querySelector('tr') || table).querySelectorAll('th')];
  const headers = headerCells.map(h => (h.innerText || '').trim().replace(/\s+/g, ' '));
  let bodyRows = [...table.querySelectorAll('tbody tr, [role="row"]')].filter(r => !r.querySelector('th') || r.querySelector('td')).filter(r => (r.getAttribute('role') || '') !== 'rowheader');
  const rows = bodyRows.slice(0, 5).map(tr => [...tr.querySelectorAll('td, [role="cell"], [role="gridcell"]')].map(c => (c.innerText || '').trim().replace(/\s+/g, ' ')));
  let totalRowCount = bodyRows.length;
  const pagerText = (document.body.innerText || '').toLowerCase();
  const tm = /(?:of|total)[\s:]+(\d{1,6})\b/i.exec(pagerText) || /\b(\d{1,6})\s+(?:records?|results?|rows?|entries|items)\b/i.exec(pagerText);
  if (tm) totalRowCount = +tm[1];
  return { headers, rows, totalRowCount, filterApplied: null, filteredValue: null };
}
```

## Issues
| issueType | severity | description | who emits |
|---|---|---|---|
| exportButtonNotFound | low | Page has a data table or list but NO export/download button visible | probe |
| exportButtonDisabled | medium | Export button is present but disabled (aria-disabled or pointer-events:none) | probe |
| exportNoDownloadTriggered | high | Export button clicked, waited 3s, but no download link appeared and no new tab opened | probe |
| exportLinkBroken | high | Download link href is blank, `javascript:void(0)`, or `#` with no download attribute | probe |
| exportMissingFormatChoice | low | Only one format available (e.g., no CSV+PDF choice) on a page with rich data | probe |
| exportDialogBroken | medium | An export-config dialog appeared but the Confirm/Export button inside it did not work | probe |
| exportNoFeedback | medium | Export initiated but no loading indicator, toast, or progress appeared while the download was pending | probe |
| exportContentEmpty | high | Downloaded file parses to zero data rows even though the table on screen had rows | MCP verify |
| exportContentMissingColumns | high | Export is missing one or more columns shown on screen | MCP verify |
| exportContentRowCountMismatch | high | Visible row count differs from the export's row count by more than 1 | MCP verify |
| exportContentCellMismatch | high | Visible cell values from the first 5 rows are absent from the export | MCP verify |
| exportIgnoresFilter | high | A filter was applied on screen but the export contains data that doesn't match the filter | MCP verify |

## Hard rules

1. **Do NOT wait more than ~3s** for a download in the probe (`sleep(2500)` after dialog). The MCP verify step uses an 8s download timeout.
2. **Mandatory cleanup** — the probe removes all `data-argus-export*` attributes before returning.
3. **Max 1 primary export control tested** by the probe per cell — don't drive every format button.
4. **Sonnet model** — export-dialog interaction and content-mismatch judgment require it.
5. **Drop `_exportProbeMeta`** from the JSONL — it is an internal signal for the orchestrator, not a bug.

## Notes on this conversion
- `executable: partial`. The Phase-1 detection (button presence, enabled, format choice, wired href, dialog, trigger, feedback) is now ONE async `browser_evaluate` — all 7 trigger-side issueTypes fire from the probe with no AI hand-driving.
- Phase-2 content verification (`exportContent*`, `exportIgnoresFilter`) stays MCP-driven because a real browser download's bytes are not readable from inside `browser_evaluate`. The probe emits an `_exportProbeMeta` info finding carrying `downloadTriggered` so the orchestrator only spends the MCP round-trips when a download actually fired.
- All 12 issueTypes preserved.
