---
name: qa-smoke-test
description: >
  Run automated QA tests on desktop apps or websites. Smoke tests, visual regression,
  UI validation, accessibility checks, end-to-end flows. Use when: "test this app",
  "smoke test", "check if login works", "validate the UI", "visual regression",
  "verify button is clickable", "test flow", "QA check", "accessibility audit".
allowed-tools:
  - mcp__sh__screenshot_file
  - mcp__sh__screenshot
  - mcp__sh__ocr
  - mcp__sh__ui_tree
  - mcp__sh__ui_find
  - mcp__sh__browser_dom
  - mcp__sh__browser_page_info
  - mcp__sh__browser_js
  - mcp__sh__browser_wait
  - mcp__sh__browser_navigate
  - mcp__sh__wait_for_state
  - mcp__sh__locate_with_fallback
  - mcp__sh__read_with_fallback
  - mcp__sh__apps
  - mcp__sh__windows
  - mcp__sh__focus
  - mcp__sh__memory_record_learning
  - mcp__sh__memory_record_error
  - mcp__sh__memory_errors
  - mcp__sh__memory_query_patterns
---

# QA Smoke Testing & UI Validation

You are running automated quality assurance tests using ScreenHand's inspection and interaction tools.

## Intelligence Wrapper

Every tool call returns automatic hints. Watch for:
- **`[HINT]`** — known selectors for the app/site under test
- **`[WARNING]`** — this tool has failed before, here's the fix
- **`[STRATEGY]`** — suggested next step based on past test sequences

## Test Plan Structure

Before any action, define the test plan:

```
Test Plan: {App/Site Name}
===========================
1. [CHECK_NAME]: {assertion}
2. [CHECK_NAME]: {assertion}
...
```

Each assertion must be verifiable: "element X exists", "text Y is visible", "page loads under 3s", "button Z is clickable".

## Phase 1: Baseline Capture

1. Take initial `screenshot_file` — this is the "before" state.
2. For web: `browser_page_info` — capture URL, title, initial text.
3. For native apps:
   - `apps` — verify the app is running, get `pid`
   - `windows` — identify target window, get `windowId`
   - `ui_tree(pid)` — capture the element hierarchy
4. For canvas/custom-drawn UIs: `ocr` — screenshot + text extraction with bounding boxes. Use when `ui_tree` returns empty.
5. Check verified patterns: `memory_query_patterns(scope="{app_name}")` — known working selectors.
6. Record the baseline for comparison.

## Phase 2: Execute Test Checks

### Element Existence
```
locate_with_fallback(text="Submit Button")
→ PASS if element found with bounds
→ FAIL if "not found"
```

Uses the fallback chain: AX → CDP → OCR. Most thorough detection.

### Text Presence
```
wait_for_state(condition="text_appears", text="Welcome back")
→ PASS if text found within timeout
→ FAIL if timeout exceeded
```

### Element Interactivity (Web)
```javascript
// Check if button is enabled and visible
const btn = document.querySelector('button.submit');
const style = getComputedStyle(btn);
return JSON.stringify({
  exists: !!btn,
  visible: style.display !== 'none' && style.visibility !== 'hidden',
  enabled: !btn.disabled,
  clickable: btn.offsetWidth > 0 && btn.offsetHeight > 0
});
```

Use `browser_js` with this check.

### Element Interactivity (Native)
```
ui_find(text="Submit")
→ Check AXEnabled attribute in result
→ PASS if enabled=true
→ FAIL if enabled=false or not found
```

### Page Load Performance (Web)
```javascript
const timing = performance.getEntriesByType('navigation')[0];
return JSON.stringify({
  loadTime: timing.loadEventEnd - timing.startTime,
  domReady: timing.domContentLoadedEventEnd - timing.startTime,
  ttfb: timing.responseStart - timing.requestStart
});
```

### Accessibility Audit (Web)
```javascript
const issues = [];
// Images without alt
document.querySelectorAll('img:not([alt])').forEach(img =>
  issues.push({type: 'missing-alt', element: img.src}));
// Buttons without text
document.querySelectorAll('button').forEach(btn => {
  if (!btn.textContent.trim() && !btn.getAttribute('aria-label'))
    issues.push({type: 'empty-button', element: btn.outerHTML.slice(0, 100)});
});
// Form fields without labels
document.querySelectorAll('input:not([type=hidden])').forEach(input => {
  if (!input.getAttribute('aria-label') && !document.querySelector(`label[for="${input.id}"]`))
    issues.push({type: 'unlabeled-input', element: input.name || input.type});
});
// Color contrast (basic)
// Focus order
document.querySelectorAll('a, button, input, select, textarea').forEach((el, i) => {
  if (el.tabIndex < 0) issues.push({type: 'negative-tabindex', element: el.tagName});
});
return JSON.stringify(issues);
```

### Visual Regression
1. Take `screenshot_file` at each step
2. Compare OCR text from `screenshot` between baseline and current state
3. Flag any text that appeared or disappeared unexpectedly

## Phase 3: End-to-End Flow Testing

For user flow testing (e.g., "test the login flow"):

1. Define the flow steps
2. Execute each step using the automate-app or browser tools
3. After EACH step, verify the expected state
4. Record PASS/FAIL per step
5. Take `screenshot_file` at each step for evidence

## Phase 4: Test Report

Produce a structured report:

```
Test Report: {App/Site Name}
============================
Date: {date}
Total: {N} checks
Passed: {P} ✓
Failed: {F} ✗
Skipped: {S} -

Results:
  ✓ [element_exists] Submit button is present
  ✓ [text_visible] Welcome message appears
  ✗ [interactivity] Save button is disabled (expected: enabled)
  ✓ [performance] Page loads in 1.2s (threshold: 3s)
  ✗ [a11y] 3 images missing alt text

Screenshots:
  - baseline: /path/to/screenshot1.png
  - after_login: /path/to/screenshot2.png

Failed Check Details:
  [interactivity] Save button:
    Expected: enabled=true
    Actual: enabled=false, aria-disabled="true"
    Suggestion: Check if form validation is blocking the button
```

## Learning from Results

After each test run:
- `memory_record_learning(scope="qa/{app}", method="{tool}", pattern="{what worked}", confidence=0.9)` for each passing check
- `memory_record_error(tool="{tool}", error="{what failed}", resolution="{suggested fix}")` for each failing check
- Check `memory_errors(tool="{tool}")` to see if failures match known patterns

$ARGUMENTS
