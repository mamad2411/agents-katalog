---
name: comparison
description: "Compare two pages or browser views side by side: staging vs production, mobile vs desktop, or before vs after changes. Outputs structured diffs of content, forms, and links."
---

# Visual/Page Comparison

Compare two web pages to find differences in content, structure, forms, and
links. Uses Brijio's multi-browser support to compare pages across
different browsers, tabs, or environments.

## When to Use

- Comparing staging vs production for deployment verification
- Comparing mobile (Safari) vs desktop (Chrome) views
- Verifying A/B test variants render correctly
- Checking if a page changed since last review (regression detection)
- Comparing before/after a code deployment

## Workflow

### 1. Check Connection

Call `list_browsers` to see connected browsers. You need at least one connected
browser. For cross-browser comparison, you need two (e.g., Chrome and Safari).

### 2. Read Page A

Navigate to the first page (or ask the user to navigate there) and call
`read_current_page` with `includeContent: true`. Store the full response as
**Page A**.

If comparing two browsers, specify `browserInstanceId` for each read:

```
read_current_page(browserInstanceId: "chrome-abc123", includeContent: true)
→ Page A (Chrome)
```

### 3. Read Page B

Navigate to the second page and read again:

```
read_current_page(browserInstanceId: "safari-xyz789", includeContent: true)
→ Page B (Safari)
```

For single-browser comparison, ask the user to navigate to the second page
before reading.

### 4. Compare

Diff the two page contexts across these dimensions:

| Dimension     | What to Compare                            |
| ------------- | ------------------------------------------ |
| **URL**       | Different paths, query params, hash routes |
| **Title**     | Page title differences                     |
| **Links**     | Missing/added links, changed URLs or text  |
| **Forms**     | Different fields, labels, types, options   |
| **Actions**   | Missing/added buttons, changed labels      |
| **Editables** | Different contenteditable content          |

### 5. Output Structured Diff

Present the comparison as a structured diff:

```
## Page Comparison: Staging vs Production

### URL
- Staging: https://staging.example.com/settings
- Production: https://www.example.com/settings

### Links
- Added in Staging: "Beta Features" → /settings/beta
- Removed in Staging: "Legacy Export" → /export/old
- Changed in Staging: "Help" URL /help → /support

### Forms
- Settings form (f1):
  - Added field: "Theme" (select: light/dark/auto)
  - Removed field: "Legacy Mode" (checkbox)
  - Changed label: "Notifications" → "Notification Preferences"

### Actions
- Added in Staging: "Export as CSV" button
```

### 6. Assess Impact

For each difference, categorize:

| Category        | Meaning                                               |
| --------------- | ----------------------------------------------------- |
| **Expected**    | Intentional changes (new features, design updates)    |
| **Regression**  | Unintended changes (missing content, broken forms)    |
| **Environment** | Expected differences (different URLs, different data) |

## Cross-Browser Comparison

When both Chrome and Safari are connected:

1. Read the same URL in both browsers using `browserInstanceId`
2. Compare `forms`, `links`, and `actions` — these should be similar but may
   differ due to browser-specific rendering
3. Pay special attention to:
   - Safari-only missing features (different JavaScript support)
   - Chrome-only features (different CSS support)
   - Different form control types (date pickers, file inputs)

## Single-Browser Comparison

If only one browser is connected:

1. Read Page A (first URL/state) on the current tab
2. Open Page B in a new tab using `open_tab`:

   ```
   open_tab(url: "https://example.com/page-b")  → { tabId: "12345", ... }
   ```

3. Read Page B using the returned `tabId`:

   ```
   read_current_page(tabId: "12345", includeContent: true)  → Page B
   ```

4. Compare the two results

This works well for before/after comparison (e.g., before and after a settings
change, before and after form submission). The original tab stays intact so
you can switch back to it with `read_current_page` (no `tabId`) if needed.

## Pitfalls

### Short-Lived IDs

Element IDs are **not stable across pages**. When comparing, never reference
IDs from Page A while interacting with Page B. Use labels, text, and URLs for
matching — not element IDs.

### Dynamic Content

Pages with live data (dashboards, social feeds) will always show differences.
Focus on structural comparisons (forms, links, navigation) rather than
content that naturally changes.

### Authentication Differences

If comparing staging vs production, ensure both environments are authenticated
with equivalent accounts. A logged-in page will show forms and actions that an
anonymous page won't have.

### Rate Limiting

Reading two pages in quick succession may trigger rate limits or anti-bot
protections. Space out reads by a few seconds if you encounter errors.

### Content Chunks

For large pages, `read_current_page` may return paginated content. Use
`list_resources` and `read_resource` to get all content chunks for complete
comparison.
