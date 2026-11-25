---
name: auditing-web-quality
description: Perform comprehensive web page quality audits using Chrome DevTools MCP including responsive layout verification, interactive element testing, console/network error detection, and accessibility checks. Use when user mentions "quality check", "UI check", "page audit", "responsive check", "deploy check", or asks to verify a web page before deployment. Also triggers on Japanese terms like "品質チェック", "UIチェック", "表示確認", "デプロイ前確認", "レスポンシブ確認", "アクセシビリティ確認".
---

# Web Quality Audit

Systematically verify web page quality through Chrome DevTools MCP, producing a prioritized issue report.

## Audit Modes

Determine the mode from user intent:

- **Quick Check** (default): Responsive + console errors. Use when user says "check this page" without specifics.
- **Full Audit**: All checks below. Use when user mentions "full", "deploy", "comprehensive", or "before release".
- **Targeted**: Single category only. Use when user specifies one area (e.g., "responsive check").

## Workflow

### 1. Setup

Navigate to the target URL using `mcp__chrome-devtools__navigate_page`. If no URL given, ask the user.

Capture baseline:
- `mcp__chrome-devtools__take_snapshot` for structural analysis
- `mcp__chrome-devtools__take_screenshot` for visual reference
- `mcp__chrome-devtools__list_console_messages` for existing errors

### 2. Responsive Layout Check

Test these viewports using `mcp__chrome-devtools__emulate`:

| Device | Width | Height | Touch |
|--------|-------|--------|-------|
| Desktop | 1920 | 1080 | false |
| Tablet | 768 | 1024 | true |
| Mobile | 375 | 667 | true |

For each viewport:
1. `mcp__chrome-devtools__resize_page` to set dimensions
2. `mcp__chrome-devtools__take_screenshot` to capture layout
3. `mcp__chrome-devtools__take_snapshot` to check element visibility

**Check items:**
- Text overflow from containers (especially buttons and cards)
- Horizontal scrollbar appearance
- Element overlap or hidden content
- Navigation usability at each breakpoint

### 3. Interactive Element Check

Reset to desktop viewport, then:

1. Identify all interactive elements from snapshot (buttons, links, forms)
2. `mcp__chrome-devtools__click` each primary button - verify response
3. For forms: `mcp__chrome-devtools__fill` with empty values, submit, verify validation messages appear
4. For links: verify `href` attributes are non-empty

**Check items:**
- All buttons are clickable and produce visible response
- Empty form submission triggers validation errors
- No dead links (href="#" or empty)
- Loading/skeleton states appear on data fetch

### 4. Console and Network Error Check

1. `mcp__chrome-devtools__list_console_messages` with `types: ["error", "warn"]`
2. `mcp__chrome-devtools__list_network_requests` and check for failed requests (4xx/5xx)

**Check items:**
- Zero uncaught JS errors
- Zero failed resource loads (images, scripts, fonts)
- No CORS errors
- No deprecation warnings in critical paths

### 5. Accessibility Check

From snapshot, verify:
- All images have alt text (or aria-label)
- Form inputs have associated labels
- Heading hierarchy is sequential (h1 > h2 > h3, no skips)
- Focus order is logical (tab through interactive elements using `mcp__chrome-devtools__press_key` with "Tab")
- Color contrast via visual screenshot inspection

### 6. Scroll and Navigation Check

1. `mcp__chrome-devtools__evaluate_script` to scroll to page bottom:
   ```javascript
   () => { window.scrollTo(0, document.body.scrollHeight); return document.body.scrollHeight; }
   ```
2. `mcp__chrome-devtools__take_screenshot` at bottom
3. Scroll back to top and verify
4. Check for sticky headers/footers behaving correctly

## Issue Severity

Classify each finding:

| Severity | Criteria | Example |
|----------|----------|---------|
| **Critical** | Blocks user flow or causes data loss | Button not clickable, form submission fails silently |
| **Major** | Significantly degrades UX | Text overflow making content unreadable, broken responsive layout |
| **Minor** | Cosmetic or non-blocking | Console warning, slight alignment issue |

## Report Format

Output findings as:

```
## Quality Audit Report

**URL**: [audited URL]
**Mode**: [Quick Check / Full Audit / Targeted]
**Verdict**: [PASS / FAIL (Critical issues found) / WARN (Major issues only)]

### Critical Issues
- [severity] [category] Description of issue (viewport/context)

### Major Issues
- [severity] [category] Description of issue (viewport/context)

### Minor Issues
- [severity] [category] Description of issue (viewport/context)

### Summary
- Checked: [list of completed checks]
- Issues: [N] Critical, [N] Major, [N] Minor
- Recommendation: [Go / No-Go / Conditional]
```

## Quick Reference

| Check Category | Quick Check | Full Audit |
|---------------|:-----------:|:----------:|
| Responsive    | Yes         | Yes        |
| Console/Network | Yes      | Yes        |
| Interactive   | No          | Yes        |
| Accessibility | No          | Yes        |
| Scroll/Nav    | No          | Yes        |
