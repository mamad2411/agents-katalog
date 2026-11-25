---
name: qa-test-upload-e2e
section: interactive
description: "Tests the full file upload lifecycle. DETECTION (find an upload control, max-size hint, multiple support, image-upload) and post-upload VERIFICATION (progress shown? error? file persisted? success feedback? preview?) run as in-page async probes; the actual file selection uses the MCP browser_file_upload tool. Catches silent upload failures, missing progress indicators, and files that upload but never appear in the list."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
cacheVersion: "1.0.0"
requires: [hasFileUpload]
---
# qa-test-upload-e2e — File Upload Lifecycle Testing

Upload controls are notoriously brittle. A file can "upload" but silently fail server-side, show a spinner that never resolves, or succeed but not appear in the list. This skill catches those three failure modes.

**Uses a tiny test file** — writes a small `.txt` file to `.tmp/argus-upload-test.txt` before testing. Never uploads real user data.

## How the orchestrator runs this (probe + an upload MCP step)

🚨 This skill is **`executable: partial`**. Selecting a real file requires the OS file-chooser, which only the MCP `browser_file_upload` tool can drive — `browser_evaluate` cannot put a real file on an `<input type=file>`. Everything else (scanning for the control, checking progress, evaluating the final state) is in-page.

1. Write the test file to disk (see **## Setup**).
2. ONE detection probe: `uploadState = browser_evaluate(probe, {mode:'scan'})`. If it returns a `uploadButtonNotFound` finding (and `_stateForMcp.found=false`) → self-skip after recording it. Otherwise it tags the input and reports max-size / multiple / image hints (and may emit `uploadMaxSizeUnclear` / `uploadMultipleNotSupported`).
3. Run **## MCP steps (upload)** to actually select the file, then call the probe in `progress` and `final` modes to evaluate the result.

## What it checks (8 issue types)

| issueType | severity | what it catches |
|---|---|---|
| `uploadButtonNotFound` | low | Page has a form or media section but no file upload control is found |
| `uploadNoProgress` | medium | File selected, upload started, but no spinner/progress bar/status text appeared during upload |
| `uploadFailed` | high | Upload API call returned a non-2xx response OR error message appeared in UI after upload |
| `uploadNotPersisted` | high | Upload appeared to succeed (no error shown) but the uploaded filename does NOT appear anywhere in the page after waiting |
| `uploadMaxSizeUnclear` | low | Upload control has no max file size hint (no `accept` attribute, no label mentioning MB limit) |
| `uploadNoPreview` | low | Image upload completed but no thumbnail/preview appeared (image uploads should show previews) |
| `uploadMultipleNotSupported` | low | Upload control lacks `multiple` attribute on a page that likely handles multiple files (documents/gallery page) |
| `uploadSuccessNoFeedback` | medium | Upload completed but no success toast/snackbar/message appeared |

## Self-skip conditions

The `scan` probe returns `_stateForMcp.found=false` (and emits `uploadButtonNotFound`) when none of these exist:
```
input[type="file"], [class*="upload"], [class*="file-drop"], [class*="dropzone"],
[aria-label*="upload" i], [class*="file-input"], [class*="file-picker"]
```

## Setup — create test file

Before the scan probe, the orchestrator writes the test file (the file must exist on the local filesystem before `browser_file_upload` is called, and `browser_file_upload` requires an **absolute path**):
```
testFilePath = "{project-root}/.tmp/argus-upload-test.txt"
Content: "argus-upload-test 2026-06-08"
```
Use the Write tool or a Bash `echo`.

## Interactive Probe (browser_evaluate, async)

```js
async (args) => {
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-upload-e2e' }, o));
  const visW = e => { const r = e.getBoundingClientRect(); return r.width > 0 && getComputedStyle(e).display !== 'none'; };
  args = args || {};

  // ── SCAN mode (default): find an upload control, tag it, report hints ──
  if (!args.mode || args.mode === 'scan') {
    const inputs = [...document.querySelectorAll('input[type="file"]')];
    const buttonTriggers = [...document.querySelectorAll('[class*="upload-btn"], [class*="file-btn"], [aria-label*="upload" i], button[onclick*="upload"], [class*="dropzone"] button, [class*="file-drop"] button')]
      .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; });

    if (inputs.length === 0 && buttonTriggers.length === 0) {
      add({ issueType: 'uploadButtonNotFound', severity: 'low', selector: 'body', description: 'Page has a form or media section but no file upload control was found.', evidence: {} });
      out._stateForMcp = { found: false };
      return out;
    }

    const primaryInput = inputs[0] || null;
    if (primaryInput) primaryInput.setAttribute('data-argus-upload-input', '1');
    const triggerBtn = buttonTriggers[0];
    if (triggerBtn) triggerBtn.setAttribute('data-argus-upload-trigger', '1');

    const accept = (primaryInput && primaryInput.getAttribute('accept')) || '';
    const surroundingText = ((primaryInput && primaryInput.closest('form,mat-form-field,[class*="upload"]') && primaryInput.closest('form,mat-form-field,[class*="upload"]').innerText) || '').toLowerCase();
    const hasMaxSizeHint = /\b\d+\s*(mb|kb|gb|byte|limit|max)\b/i.test(surroundingText) || accept.length > 0;
    const multipleSupported = !!(primaryInput && primaryInput.getAttribute('multiple') != null);
    const likelyMultiPage = /\b(document|attachment|media|gallery|files|images)\b/i.test(document.title + location.pathname);
    const isImageUpload = /image|photo|picture|avatar|thumbnail/i.test(accept + surroundingText);

    if (!hasMaxSizeHint)
      add({ issueType: 'uploadMaxSizeUnclear', severity: 'low', selector: primaryInput ? '[data-argus-upload-input="1"]' : '[data-argus-upload-trigger="1"]', description: 'Upload control has no max file size hint (no accept attribute, no label mentioning an MB limit).', evidence: { accept } });
    if (!multipleSupported && likelyMultiPage)
      add({ issueType: 'uploadMultipleNotSupported', severity: 'low', selector: primaryInput ? '[data-argus-upload-input="1"]' : '[data-argus-upload-trigger="1"]', description: 'Upload control lacks the multiple attribute on a page that likely handles multiple files.', evidence: {} });

    out._stateForMcp = {
      found: true,
      inputSelector: primaryInput ? '[data-argus-upload-input="1"]' : null,
      triggerSelector: triggerBtn ? '[data-argus-upload-trigger="1"]' : null,
      needsButtonClick: !primaryInput && !!triggerBtn,
      isImageUpload
    };
    return out;
  }

  // ── PROGRESS mode: did a spinner/progress indicator appear during upload? ──
  if (args.mode === 'progress') {
    const progressSel = 'mat-progress-bar, mat-progress-spinner, [role="progressbar"], [class*="upload-progress"], [class*="progress-bar"], [class*="spinner"], [class*="uploading"], [class*="loading"]';
    const hasProgress = [...document.querySelectorAll(progressSel)].some(visW);
    if (!hasProgress)
      add({ issueType: 'uploadNoProgress', severity: 'medium', selector: '[data-argus-upload-input="1"]', description: 'File selected and upload started, but no spinner/progress bar/status text appeared during upload.', evidence: {} });
    return out;
  }

  // ── FINAL mode: error? persisted? success feedback? preview? — args: { testFileName, isImageUpload } ──
  if (args.mode === 'final') {
    const bodyText = document.body.innerText || '';
    const errorEls = [...document.querySelectorAll('[role="alert"], mat-error, [class*="upload-error"], [class*="error-message"], .alert-danger')];
    const hasError = errorEls.some(visW);
    const errorEl = errorEls.find(e => e.getBoundingClientRect().width > 0);
    const errorText = errorEl ? (errorEl.innerText || '').trim().slice(0, 200) : null;

    const baseName = (args.testFileName || '').replace('.txt', '');
    const fileAppearedInUI = bodyText.includes(args.testFileName) || (baseName && bodyText.includes(baseName)) || !!document.querySelector('[class*="file-name"], [class*="filename"], [class*="attachment-name"]');

    const successSel = 'mat-snack-bar-container, [class*="snackbar"], [class*="toast"], [role="alert"][class*="success"], .alert-success, [class*="success-message"]';
    const hasSuccessFeedback = [...document.querySelectorAll(successSel)].some(visW);
    const hasPreview = !!document.querySelector('[class*="preview"] img, [class*="thumbnail"] img, [class*="upload-preview"]');

    if (hasError)
      add({ issueType: 'uploadFailed', severity: 'high', selector: '[data-argus-upload-input="1"]', description: 'Upload failed — an error message appeared in the UI after upload (or the upload API returned non-2xx).', evidence: { errorText } });
    else {
      if (!fileAppearedInUI)
        add({ issueType: 'uploadNotPersisted', severity: 'high', selector: '[data-argus-upload-input="1"]', description: 'Upload appeared to succeed (no error shown) but the uploaded filename does NOT appear anywhere in the page after waiting.', evidence: { testFileName: args.testFileName } });
      if (!hasSuccessFeedback)
        add({ issueType: 'uploadSuccessNoFeedback', severity: 'medium', selector: '[data-argus-upload-input="1"]', description: 'Upload completed but no success toast/snackbar/message appeared.', evidence: {} });
      if (args.isImageUpload && !hasPreview)
        add({ issueType: 'uploadNoPreview', severity: 'low', selector: '[data-argus-upload-input="1"]', description: 'Image upload completed but no thumbnail/preview appeared.', evidence: {} });
    }
    return out;
  }

  // ── CLEANUP mode ──
  if (args.mode === 'cleanup') {
    for (const el of document.querySelectorAll('[data-argus-upload-input], [data-argus-upload-trigger]')) {
      try { el.removeAttribute('data-argus-upload-input'); el.removeAttribute('data-argus-upload-trigger'); } catch (_) {}
    }
    return [];
  }

  return out;
}
```

> The probe attaches a non-ticketed `_stateForMcp` field (tagged input/trigger selectors + flags). Only objects with an `issueType` become tickets.

## MCP steps (upload)

Using `uploadState._stateForMcp.*`:

1. If `needsButtonClick`: `browser_click(triggerSelector)`, `browser_wait_for(time=400)`.
2. `browser_file_upload(selector=inputSelector, files=[testFilePath])`, `browser_wait_for(time=500)`.
3. `browser_evaluate(probe, {mode:'progress'})` — may emit **uploadNoProgress (medium)**.
4. `browser_wait_for(time=3000)` (5 s ceiling), then `browser_evaluate(probe, {mode:'final', testFileName:'argus-upload-test.txt', isImageUpload: uploadState._stateForMcp.isImageUpload})` — may emit **uploadFailed / uploadNotPersisted / uploadSuccessNoFeedback / uploadNoPreview**.
5. `browser_evaluate(probe, {mode:'cleanup'})` — always, even on error.

## Hard rules

1. **Only upload the test `.txt` file** — never upload real user files or large binaries.
2. **Mandatory cleanup** — run the probe's `cleanup` mode to remove all `data-argus-upload-*` attributes.
3. **Wait max 5 s** for upload completion — `browser_wait_for(time=3000)` ceiling.
4. **Sonnet model** — upload result interpretation (did it really persist?) requires judgment.
5. **Do NOT delete the uploaded test file from the server** — leave cleanup to `qa-test-crud`'s emergency cleanup or manual review. The `.txt` content makes it clearly a test artifact.

## Notes on this conversion
- `executable: partial`. Scan/detection, progress check, final-state evaluation, and cleanup are folded into ONE multi-mode `browser_evaluate` probe (`scan` / `progress` / `final` / `cleanup`) that emits findings directly. The only genuine MCP step is `browser_file_upload`, since `browser_evaluate` cannot place a real file on an `<input type=file>`.
