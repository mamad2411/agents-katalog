---
name: scan-and-fix-accessibility
description: Scan webpage for accessibility issues using startAccessibilityScan MCP tool, identify WCAG violations, and generate code fixes. Use for WCAG compliance and accessibility bug fixes.
---

# Scan and Fix Accessibility

## When to Use

- User wants to fix accessibility issues on a page
- Need to ensure WCAG compliance
- Fixing specific accessibility bugs

## MCP Tools Used

- `startAccessibilityScan` (Tool #17) - Scan webpage for accessibility issues
- `accessibilityExpert` (Tool #16) - Get WCAG guidelines and best practices

## Steps

### 1. Run Accessibility Scan

Use `startAccessibilityScan` to scan the webpage:

```
"Run accessibility scan for 'www.example.com'"
"Scan accessibility issues on localhost:3000"
"Run accessibility scan for 'https://mysite.com/checkout'"
```

**What the tool does:**
- Performs comprehensive WCAG 2.0/2.1/2.2 accessibility scan
- Returns result link with detailed violation report
- Categorizes issues by severity (Critical/High/Medium/Low)

### 2. Analyze Results

Review the scan results and categorize issues:
- **Critical**: Blocks users (missing form labels, keyboard traps)
- **High**: Major barriers (poor color contrast, missing alt text)
- **Medium**: Best practices (heading hierarchy)

### 3. Get WCAG Guidelines (Optional)

Use `accessibilityExpert` for specific guidance:

```
"What WCAG guidelines apply to form field error messages on mobile web?"
"How do I fix color contrast issues for WCAG 2.1 AA compliance?"
```

**What the tool does:**
- Provides WCAG 2.0/2.1/2.2 compliance guidance
- Answers questions about accessibility best practices
- Covers mobile and web usability standards

### 4. Fix Issues in Code

For each issue, provide specific code fix:

**Missing Alt Text:**
```html
<!-- Before -->
<img src="logo.png">

<!-- After -->
<img src="logo.png" alt="Company Logo">
```

**Poor Color Contrast:**
```css
/* Before - Contrast 2.8:1 (fails) */
color: #999;
background: #fff;

/* After - Contrast 4.6:1 (passes) */
color: #666;
background: #fff;
```

**Missing Form Label:**
```html
<!-- Before -->
<input type="email" placeholder="Email">

<!-- After -->
<label for="email">Email Address</label>
<input type="email" id="email" aria-required="true">
```

**Keyboard Navigation:**
```html
<!-- Before -->
<div onclick="handleClick()">Click me</div>

<!-- After -->
<button onclick="handleClick()">Click me</button>
```

### 4. Verify Fixes

After user implements fixes, re-scan using `startAccessibilityScan`:

```
"Re-scan www.example.com to verify accessibility issues are fixed"
"Run accessibility scan again on localhost:3000 after fixes"
```

### 5. Report Results

Confirm what was fixed and any remaining issues.

## Common Scenarios

**Scan and Fix Workflow:**
```
"Scan accessibility issues on localhost:3000"
→ Returns scan results with violations
→ Provide code fixes for each issue
→ User implements fixes
"Re-scan localhost:3000 to verify fixes"
```

**Get WCAG Guidance:**
```
"What WCAG guidelines apply to form field error messages?"
"How do I ensure my color palette is WCAG 2.1 AA compliant?"
```

## Quick Reference

**Common WCAG Requirements:**
- Images need alt text (WCAG 1.1.1)
- Color contrast ≥ 4.5:1 for text (WCAG 1.4.3)
- All interactive elements keyboard accessible (WCAG 2.1.1)
- Forms have labels (WCAG 3.3.2)
- Proper heading hierarchy (WCAG 1.3.1)

## Example

**User**: "Fix accessibility issues on my login page at localhost:3000/login"

**Workflow**:
1. Scan: Use `startAccessibilityScan` for "localhost:3000/login"
2. Results: Scan returns violations - 3 critical issues found
3. Identify: "Missing form labels, poor contrast, no keyboard nav"
4. Fix: Provide code fixes for each issue
5. Verify: Use `startAccessibilityScan` again to re-scan
6. Confirm: "All critical issues resolved ✓"
