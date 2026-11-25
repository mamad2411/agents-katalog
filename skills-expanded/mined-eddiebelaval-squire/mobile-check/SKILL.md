---
name: Mobile Check
slug: mobile-check
description: Comprehensive front-to-back mobile verification using Playwright MCP. Tests at iPhone mini viewport (375x667) as the bas
category: operations
complexity: complex
version: "1.0.0"
author: "id8Labs"
triggers:
  - "mobile-check"
  - "mobile check"
tags:
  - operations
  - tool-factory-retrofitted
---

# /mobile-check - Mobile Readiness Verification


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

Comprehensive front-to-back mobile verification using Playwright MCP. Tests at iPhone mini viewport (375x667) as the baseline — if it works here, it works everywhere.

## Trigger
- `/mobile-check` - Full mobile audit of all key pages
- `/mobile-check [url]` - Check a specific page/route
- `/mobile-check [page1] [page2]` - Check specific pages
- `/mobile-check extreme` - Also test at 320px (iPhone SE 1st gen)

## Philosophy

> Test the smallest screen. Trust the rest.

The iPhone 13 mini / SE viewport (375x667) is the floor for modern mobile. If your layout doesn't break here, every larger device is covered. This skill runs a real browser at that viewport and systematically checks every failure mode that CSS alone can't catch.

## Device Targets

| Device | Width | Height | When |
|--------|-------|--------|------|
| iPhone 13 mini / SE | 375px | 667px | Always (primary) |
| iPhone SE 1st gen | 320px | 568px | `/mobile-check extreme` only |
| iPad Mini | 768px | 1024px | Tablet check (optional, if `tablet` arg) |

## Prerequisites

Before running checks, the skill MUST:
1. Detect if a dev server is running (check localhost:3000, 3001, 8080)
2. If not running, start it: `npm run dev` or `next dev` (background)
3. Wait for the server to be ready before proceeding
4. Detect the project's routing structure to find key pages

## Verification Layers

```
+-----------------------------------------------+
|  Layer 1: Viewport & Meta                      |
|  - viewport meta tag present                   |
|  - No horizontal overflow at 375px             |
|  - No content wider than viewport              |
+-----------------------------------------------+
|  Layer 2: Layout & Overflow                    |
|  - No horizontal scrollbar                     |
|  - All containers respect viewport width       |
|  - Fixed/sticky elements don't overlap content |
|  - No elements bleeding off-screen             |
+-----------------------------------------------+
|  Layer 3: Touch Targets                        |
|  - All interactive elements >= 44x44px         |
|  - Adequate spacing between tap targets        |
|  - No overlapping clickable areas              |
+-----------------------------------------------+
|  Layer 4: Typography & Readability             |
|  - No text smaller than 12px rendered          |
|  - Line lengths readable (not 1-2 words/line)  |
|  - No text truncated without indication        |
|  - Font sizes scale appropriately              |
+-----------------------------------------------+
|  Layer 5: Navigation                           |
|  - Mobile nav accessible (hamburger, etc.)     |
|  - Nav items reachable with one hand           |
|  - Back navigation works                       |
|  - No orphan pages (can't navigate away)       |
+-----------------------------------------------+
|  Layer 6: Forms & Inputs                       |
|  - Input fields visible and tappable           |
|  - Keyboard doesn't obscure inputs             |
|  - Proper input types (tel, email, number)     |
|  - Labels visible (not just placeholders)      |
+-----------------------------------------------+
|  Layer 7: Media & Images                       |
|  - Images responsive (no overflow)             |
|  - No broken images                            |
|  - Videos/embeds scale to viewport             |
+-----------------------------------------------+
|  Layer 8: Performance (lightweight)            |
|  - Page loads without JS errors                |
|  - No failed network requests                  |
|  - Console errors logged                       |
+-----------------------------------------------+
```

## Execution Protocol

### Phase 1: Discovery

1. **Detect dev server** — check common ports
2. **Detect routing** — scan for `app/` directory (Next.js App Router), `pages/`, or config
3. **Build page list** — if no specific pages given in $ARGUMENTS:
   - Read the routing structure from the filesystem
   - Identify all user-facing routes (skip API routes, middleware)
   - Prioritize: homepage, auth pages, main feature pages, settings
   - Cap at 10 pages max per run (user can specify more)

### Phase 2: Viewport Setup

Use Playwright MCP to configure the browser:

```
1. browser_resize({ width: 375, height: 667 })
   -- iPhone 13 mini / SE viewport
2. browser_navigate({ url: "<dev-server-url>" })
3. browser_snapshot()
   -- Capture initial state
```

### Phase 3: Per-Page Audit

For each page in the list, run ALL layers:

```
FOR each page:
  1. browser_navigate({ url: page_url })
  2. browser_snapshot()
     -- Read the accessibility tree: check element sizes, roles, structure
  3. browser_console_messages()
     -- Check for JS errors, warnings
  4. browser_network_requests()
     -- Check for failed requests (4xx, 5xx)
  5. browser_evaluate({
       expression: "..." -- Run DOM audit scripts (see Audit Scripts below)
     })
  6. browser_take_screenshot({ filename: "mobile-check-{page-slug}-375.png" })
     -- Visual record at mobile viewport
  7. Record findings per layer
```

### Phase 4: Audit Scripts (run via browser_evaluate)

These scripts inspect the live DOM at the current viewport:

**Horizontal Overflow Check:**
```javascript
(function() {
  var docWidth = document.documentElement.clientWidth;
  var overflowing = [];
  document.querySelectorAll('*').forEach(function(el) {
    var rect = el.getBoundingClientRect();
    if (rect.right > docWidth + 1 || rect.left < -1) {
      overflowing.push({
        tag: el.tagName,
        class: el.className ? el.className.toString().slice(0, 60) : '',
        width: Math.round(rect.width),
        right: Math.round(rect.right),
        overflow: Math.round(rect.right - docWidth)
      });
    }
  });
  return { docWidth: docWidth, overflowCount: overflowing.length, elements: overflowing.slice(0, 10) };
})()
```

**Touch Target Size Check:**
```javascript
(function() {
  var interactive = document.querySelectorAll('a, button, input, select, textarea, [role="button"], [onclick], [tabindex]');
  var tooSmall = [];
  interactive.forEach(function(el) {
    var rect = el.getBoundingClientRect();
    if (rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44)) {
      tooSmall.push({
        tag: el.tagName,
        text: (el.textContent || '').trim().slice(0, 30),
        width: Math.round(rect.width),
        height: Math.round(rect.height),
        class: el.className ? el.className.toString().slice(0, 40) : ''
      });
    }
  });
  return { total: interactive.length, tooSmall: tooSmall.length, elements: tooSmall.slice(0, 15) };
})()
```

**Text Size Check:**
```javascript
(function() {
  var textNodes = [];
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  var tooSmall = [];
  while (walker.nextNode()) {
    var node = walker.currentNode;
    if (node.textContent.trim().length < 2) continue;
    var parent = node.parentElement;
    if (!parent) continue;
    var style = window.getComputedStyle(parent);
    var size = parseFloat(style.fontSize);
    if (size < 12) {
      tooSmall.push({
        text: node.textContent.trim().slice(0, 40),
        fontSize: size + 'px',
        tag: parent.tagName,
        class: parent.className ? parent.className.toString().slice(0, 40) : ''
      });
    }
  }
  return { tooSmallCount: tooSmall.length, elements: tooSmall.slice(0, 10) };
})()
```

**Viewport Meta Check:**
```javascript
(function() {
  var meta = document.querySelector('meta[name="viewport"]');
  return {
    exists: !!meta,
    content: meta ? meta.getAttribute('content') : null,
    hasWidthDevice: meta ? meta.getAttribute('content').includes('width=device-width') : false,
    hasInitialScale: meta ? meta.getAttribute('content').includes('initial-scale=') : false
  };
})()
```

**Fixed/Sticky Element Check:**
```javascript
(function() {
  var fixed = [];
  document.querySelectorAll('*').forEach(function(el) {
    var style = window.getComputedStyle(el);
    if (style.position === 'fixed' || style.position === 'sticky') {
      var rect = el.getBoundingClientRect();
      fixed.push({
        tag: el.tagName,
        position: style.position,
        top: Math.round(rect.top),
        height: Math.round(rect.height),
        class: el.className ? el.className.toString().slice(0, 40) : '',
        coversPercent: Math.round((rect.height / window.innerHeight) * 100)
      });
    }
  });
  return { count: fixed.length, elements: fixed.slice(0, 10) };
})()
```

**Input Type Check (forms):**
```javascript
(function() {
  var inputs = document.querySelectorAll('input, textarea, select');
  var issues = [];
  inputs.forEach(function(el) {
    var rect = el.getBoundingClientRect();
    var problems = [];
    if (el.tagName === 'INPUT') {
      var type = el.getAttribute('type') || 'text';
      if (el.name && el.name.match(/email/i) && type !== 'email') problems.push('should be type=email');
      if (el.name && el.name.match(/phone|tel/i) && type !== 'tel') problems.push('should be type=tel');
      if (el.name && el.name.match(/url|website/i) && type !== 'url') problems.push('should be type=url');
    }
    if (rect.width < 250 && rect.width > 0) problems.push('narrow input (' + Math.round(rect.width) + 'px)');
    if (rect.height < 44 && rect.height > 0) problems.push('short input (' + Math.round(rect.height) + 'px)');
    if (!el.getAttribute('aria-label') && !el.labels?.length && !el.getAttribute('placeholder')) {
      problems.push('no label or placeholder');
    }
    if (problems.length > 0) {
      issues.push({
        tag: el.tagName,
        type: el.getAttribute('type') || 'text',
        name: el.name || el.id || '(unnamed)',
        problems: problems
      });
    }
  });
  return { totalInputs: inputs.length, issueCount: issues.length, issues: issues.slice(0, 10) };
})()
```

### Phase 5: Extreme Mode (if `extreme` arg)

After the 375px pass, resize to 320px and re-run:
```
browser_resize({ width: 320, height: 568 })
-- Re-run Phase 3 for all pages
-- Compare results with 375px pass
```

### Phase 6: Report

Generate a structured report organized by severity:

```
=============================================
   MOBILE READINESS REPORT
   Viewport: 375x667 (iPhone mini/SE)
   Pages checked: N
   Date: YYYY-MM-DD
=============================================

OVERALL VERDICT: PASS / PASS WITH WARNINGS / FAIL

--- CRITICAL (blocks shipping) ------------------
[List any horizontal overflow, broken layouts,
 unusable navigation, JS errors]

--- WARNINGS (fix before launch) ----------------
[Touch targets < 44px, small text, missing
 input types, narrow form fields]

--- INFO (nice to fix) --------------------------
[Minor spacing, optimization suggestions]

--- PER-PAGE BREAKDOWN -------------------------

Page: / (Homepage)
  Viewport:     PASS - no overflow
  Touch:        WARN - 3 targets under 44px
  Text:         PASS - all text >= 12px
  Nav:          PASS - hamburger menu works
  Forms:        N/A
  Media:        PASS - all images responsive
  Performance:  PASS - 0 console errors
  Screenshot:   mobile-check-homepage-375.png

Page: /login
  Viewport:     PASS
  Touch:        PASS
  Text:         PASS
  Nav:          PASS
  Forms:        WARN - email input is type=text
  Media:        N/A
  Performance:  PASS
  Screenshot:   mobile-check-login-375.png

[... repeat for each page ...]

--- SCREENSHOTS --------------------------------
All screenshots saved to:
  ~/Development/artifacts/{project}/mobile-check/

--- FIX PROMPTS --------------------------------
[For each CRITICAL/WARNING, provide a copy-paste
 prompt to fix the specific issue]

=============================================
```

### Screenshot Location

All screenshots go to: `~/Development/artifacts/{project}/mobile-check/`

If project can't be determined: `~/Development/artifacts/_general/mobile-check/`

Create the directory if it doesn't exist.

## Integration

- Run BEFORE `/ship` or `/commit-push-pr` for any UI changes
- Pairs with `/verify visual` (which checks desktop)
- Can be triggered after `/verify` as a mobile-specific layer

## Error Classification

| Severity | Examples | Verdict Impact |
|----------|----------|----------------|
| CRITICAL | Horizontal overflow, broken nav, content hidden, JS crash | FAIL |
| WARNING | Touch targets < 44px, text < 12px, missing input types | PASS WITH WARNINGS |
| INFO | Minor spacing, could optimize images, unused CSS | PASS |

## Notes

- The 375px test is the money test. If you pass 375px, you pass mobile.
- Screenshots are the proof. Always take them.
- The audit scripts run in the actual browser DOM — they catch real rendering issues that static analysis misses.
- This skill does NOT test actual device behavior (haptics, camera, etc). It tests viewport-based layout readiness.
- For React Native / Expo apps, use `/appstore-readiness` instead — this skill is for responsive web apps.
