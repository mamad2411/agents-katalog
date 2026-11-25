---
name: qa-test-workflow
section: interactive
description: "Tests status-transition workflows: finds records with actionable status buttons (Approve, Reject, Submit, Archive, Activate, Complete), clicks the action, verifies the status changed in the UI. DETECTION (actionable records, status indicators, bulk controls) and post-action VERIFICATION (status changed? feedback shown? dialog dismissed?) run as in-page async probes; the action click + any confirmation click stay as MCP steps. Catches broken approval flows, stuck state machines, and missing confirmation feedback."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
cacheVersion: "1.0.0"
requires: [hasWorkflowProcess, hasWizardFlow, hasApprovalActions]
---
# qa-test-workflow — Status Transition / Approval Flow Testing

Foundation management apps, HR systems, and any app with approval pipelines depend on status transitions. This skill tests that clicking Approve/Reject/Submit/Archive actually changes the record's status — not just that the button exists.

## How the orchestrator runs this (probe + action MCP clicks)

🚨 This skill is **`executable: partial`**. Triggering a real status transition often goes through trusted click handlers + confirmation dialogs + async API calls; the click itself stays as an MCP `browser_click` so the SPA honors it. Everything else — discovering actionable records, reading the current status, checking the confirmation dialog, checking feedback, and re-reading the status afterward — is in-page.

1. ONE discovery probe: `pageState = browser_evaluate(probe, {mode:'discover'})`. It self-skips (`_stateForMcp.found=false`, returns `[]`) when no status-action buttons exist, and may emit `workflowNoStatusIndicator` / `workflowBulkActionMissing`.
2. For each action (max 3, non-destructive first) run **## MCP steps (transition)**, calling the probe in `status` / `confirm` / `feedback` modes around the click.

## What it checks (6 issue types)

| issueType | severity | what it catches |
|---|---|---|
| `workflowTransitionFailed` | high | Status action clicked + confirmed but record status did NOT change |
| `workflowNoStatusIndicator` | medium | Page has status action buttons but no visible status label/badge on records |
| `workflowNoConfirmFeedback` | medium | Status transition completed but no toast/snackbar/alert shown to user |
| `workflowConfirmDialogBroken` | high | Confirmation dialog appeared but confirm button click did not dismiss it |
| `workflowReverseNotBlocked` | medium | An irreversible status (Archived, Rejected) can be re-activated without restriction (no disabled button or error) |
| `workflowBulkActionMissing` | low | Page has a selectable list (checkboxes) but no bulk-action controls for status changes |

## Self-skip conditions

The `discover` probe returns `_stateForMcp.found=false` when the page has NONE of these status action patterns:
```
button[approve|reject|submit|archive|activate|complete|publish|close|reopen|restore],
[aria-label*="approve" i], [aria-label*="reject" i], [aria-label*="submit" i],
[class*="approve-btn"], [class*="reject-btn"], [class*="status-action"],
mat-chip[color="warn"], mat-chip[color="accent"]
```

## Interactive Probe (browser_evaluate, async)

```js
async (args) => {
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-workflow' }, o));
  const norm = t => (t || '').toLowerCase().trim();
  const visW = e => { const r = e.getBoundingClientRect(); return r.width > 0 && getComputedStyle(e).display !== 'none'; };
  args = args || {};

  // ── DISCOVER mode (default): find actionable records + status indicators + bulk controls ──
  if (!args.mode || args.mode === 'discover') {
    const actionLabels = /\b(approve|reject|submit|archive|activate|complete|publish|close|reopen|restore)\b/i;
    const allBtns = [...document.querySelectorAll('button, [role="button"], a[role="button"], mat-button, [mat-button], [mat-raised-button], [mat-stroked-button]')]
      .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && !el.disabled; });
    const actionBtns = allBtns.filter(btn => actionLabels.test(norm(btn.innerText) + ' ' + norm(btn.getAttribute('aria-label'))));

    if (actionBtns.length === 0) { out._stateForMcp = { found: false }; return out; }

    const actions = actionBtns.slice(0, 5).map((btn, i) => {
      btn.setAttribute('data-argus-wf-btn', String(i));
      const row = btn.closest('tr, [role="row"], mat-row, [role="listitem"], [class*="card"], [class*="record"]');
      if (row) row.setAttribute('data-argus-wf-record', String(i));
      return { selector: `[data-argus-wf-btn="${i}"]`, label: norm(btn.innerText || btn.getAttribute('aria-label') || ''), recordSelector: row ? `[data-argus-wf-record="${i}"]` : null };
    });

    // status-indicator check
    const hasActionButtons = !!document.querySelector('[data-argus-wf-btn]');
    const hasStatusLabels = !!document.querySelector('mat-chip, [class*="status-badge"], [class*="status-chip"], [class*="status-label"], [class*="badge"][class*="state"], [class*="pill"]');
    if (hasActionButtons && !hasStatusLabels)
      add({ issueType: 'workflowNoStatusIndicator', severity: 'medium', selector: 'body', description: 'Page has status action buttons but no visible status label/badge on records.', evidence: {} });

    // bulk-action check
    const checkboxes = document.querySelectorAll('input[type="checkbox"], mat-checkbox, [role="checkbox"]');
    const hasBulkCheckboxes = checkboxes.length >= 3;
    if (hasBulkCheckboxes) {
      const hasBulkStatusControls = !!document.querySelector('[aria-label*="bulk" i], [class*="bulk-action"], [class*="batch-action"]')
        || [...document.querySelectorAll('button')].some(b => /\b(bulk|select all|actions)\b/i.test(b.innerText || ''));
      if (!hasBulkStatusControls)
        add({ issueType: 'workflowBulkActionMissing', severity: 'low', selector: 'body', description: 'Page has a selectable list (checkboxes) but no bulk-action controls for status changes.', evidence: {} });
    }

    out._stateForMcp = { found: true, actions, hasBulkCheckboxes };
    return out;
  }

  // ── STATUS mode: read a record's current status — args: { recordSelector } ──
  if (args.mode === 'status') {
    if (!args.recordSelector) return [{ skill: 'qa-test-workflow', _statusText: null }];
    const record = document.querySelector(args.recordSelector);
    if (!record) return [{ skill: 'qa-test-workflow', _statusText: null }];
    const statusEl = record.querySelector('mat-chip, [class*="badge"], [class*="status"], [class*="chip"], [class*="label"][class*="state"], span[class*="tag"], .status-pill');
    if (statusEl) return [{ skill: 'qa-test-workflow', _statusText: (statusEl.innerText || '').trim().toLowerCase() }];
    const cellTexts = [...record.querySelectorAll('td, [role="cell"], mat-cell')].map(c => (c.innerText || '').trim());
    const statusWord = cellTexts.find(t => /\b(pending|approved|rejected|active|inactive|archived|submitted|completed|published|draft|open|closed)\b/i.test(t));
    return [{ skill: 'qa-test-workflow', _statusText: statusWord ? statusWord.toLowerCase() : null }];
  }

  // ── CONFIRM mode: is a confirmation dialog open? tag its confirm button ──
  if (args.mode === 'confirm') {
    const dialog = document.querySelector('[role="dialog"][aria-modal="true"]:not([aria-hidden="true"]), mat-dialog-container, .swal2-popup:not([aria-hidden="true"])');
    if (!dialog || dialog.getBoundingClientRect().width === 0) return [{ skill: 'qa-test-workflow', _dialogFound: false }];
    const confirmBtn = [...dialog.querySelectorAll('button')].find(b => /\b(yes|confirm|ok|proceed|approve|continue)\b/i.test(b.innerText || ''));
    if (confirmBtn) confirmBtn.setAttribute('data-argus-confirm', '1');
    return [{ skill: 'qa-test-workflow', _dialogFound: true, _confirmSelector: confirmBtn ? '[data-argus-confirm="1"]' : null }];
  }

  // ── FEEDBACK mode: success/error toast shown? ──
  if (args.mode === 'feedback') {
    const successSel = 'mat-snack-bar-container, [class*="snackbar"], [class*="toast"], [role="alert"], .alert-success, [class*="success-message"], .swal2-success';
    const errorSel = '[role="alert"][class*="error"], .alert-danger, mat-error, [class*="error-message"], .swal2-error';
    const ok = [...document.querySelectorAll(successSel)].some(visW);
    const err = [...document.querySelectorAll(errorSel)].some(visW);
    return [{ skill: 'qa-test-workflow', _hasSuccess: ok, _hasError: err }];
  }

  // ── REVERSE mode: after archiving, is an unblocked restore/activate button present? — args: { lastAction } ──
  if (args.mode === 'reverse') {
    const record = document.querySelector('[data-argus-wf-record]');
    if (!record) return out;
    const reverseSel = args.lastAction === 'archive' ? /\b(restore|unarchive|activate)\b/i : /\b(approve|reopen)\b/i;
    const reverseBtn = [...record.querySelectorAll('button')].find(b => reverseSel.test(b.innerText || b.getAttribute('aria-label') || ''));
    if (reverseBtn && !reverseBtn.disabled)
      add({ issueType: 'workflowReverseNotBlocked', severity: 'medium', selector: reverseBtn.id ? `#${reverseBtn.id}` : 'button[aria-label]', description: 'An irreversible status can be re-activated without restriction (no disabled button or error).', evidence: { lastAction: args.lastAction } });
    return out;
  }

  // ── CLEANUP mode ──
  if (args.mode === 'cleanup') {
    for (const el of document.querySelectorAll('[data-argus-wf-btn], [data-argus-wf-record], [data-argus-confirm]')) {
      try { el.removeAttribute('data-argus-wf-btn'); el.removeAttribute('data-argus-wf-record'); el.removeAttribute('data-argus-confirm'); } catch (_) {}
    }
    return [];
  }

  return out;
}
```

> The probe attaches non-ticketed `_*` fields (status text, dialog/confirm flags, feedback flags) the orchestrator reads to decide ticketing. Only objects with an `issueType` become tickets.

## MCP steps (transition)

Priority order (non-destructive first): `approve` > `submit` > `activate` > `complete` > `archive` > `reject`. Always test reversible actions before irreversible ones. For each action in `pageState._stateForMcp.actions` (max 3):

1. `before = browser_evaluate(probe, {mode:'status', recordSelector: action.recordSelector})` → `before[0]._statusText`.
2. `browser_click(action.selector)`, `browser_wait_for(time=600)`.
3. `c = browser_evaluate(probe, {mode:'confirm'})`. If `c[0]._dialogFound`: `browser_click(c[0]._confirmSelector)`, `browser_wait_for(time=800)`, then `c2 = browser_evaluate(probe, {mode:'confirm'})`; if `c2[0]._dialogFound` → emit **workflowConfirmDialogBroken (high)** and continue.
4. `browser_wait_for(time=600)`; `fb = browser_evaluate(probe, {mode:'feedback'})`. If `!fb[0]._hasSuccess && !fb[0]._hasError` → emit **workflowNoConfirmFeedback (medium)**.
5. `after = browser_evaluate(probe, {mode:'status', recordSelector: action.recordSelector})`. If `after[0]._statusText === before[0]._statusText` → emit **workflowTransitionFailed (high)** with `evidence:{action:action.label, statusBefore:before[0]._statusText, statusAfter:after[0]._statusText}`.
6. (Optional, only if an `archive`/`reject` action succeeded) `browser_evaluate(probe, {mode:'reverse', lastAction:'archive'})` — may emit **workflowReverseNotBlocked (medium)**.

Finally: `browser_evaluate(probe, {mode:'cleanup'})` — always, even on error.

## Hard rules

1. **Non-destructive first** — test Approve before Archive, Activate before Delete.
2. **Mandatory cleanup** — run the probe's `cleanup` mode to remove all `data-argus-wf-*` attributes.
3. **Max 3 transitions** — bounded; don't churn through every record.
4. **Sonnet model** — status text interpretation requires semantic judgment.

## Notes on this conversion
- `executable: partial`. Discovery, status read, confirm-dialog detection, feedback check, reverse-block check, and cleanup are folded into ONE multi-mode `browser_evaluate` probe. The action click (and confirm click) stay as MCP `browser_click` calls because triggering a real, SPA-honored status transition needs a trusted click + async settle that `browser_evaluate` should not fake.
