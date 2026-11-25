---
name: accessibility
description: "Audit web pages for accessibility issues: missing alt text, unlabeled controls, heading hierarchy, ARIA landmarks, and color contrast — on authenticated pages that automated scanners can't reach."
---

# Accessibility Audit

Audit web pages for common accessibility issues using Brijio's page
context data. Unlike automated scanners (Lighthouse, axe) that run on public
pages, this skill audits pages behind authentication — admin panels, dashboards,
internal tools, and staging environments.

## When to Use

- Auditing authenticated pages that Lighthouse can't reach
- Checking a11y during QA on staging or internal tools
- Verifying WCAG 2.1 compliance on pages requiring login
- Quick spot-checks after UI changes

## What Brijio Can Detect

Brijio provides page context (`links`, `forms`, `actions`, `editables`),
which enables these checks:

| Check             | Data Source              | What to Look For                                           |
| ----------------- | ------------------------ | ---------------------------------------------------------- |
| Link text         | `links`                  | Empty or generic link text ("click here", "read more")     |
| Button labels     | `actions`                | Missing labels, icon-only buttons without aria-label       |
| Form labels       | `forms.controls`         | Controls without `label`, duplicate labels, generic labels |
| Heading hierarchy | content                  | Skipping levels (h1 → h3, no h2), multiple h1s             |
| Alt text          | `links` (images)         | Images acting as links without descriptive text            |
| Required fields   | `forms.controls`         | Required fields without visual indication                  |
| Select options    | `forms.controls.options` | Selects with no options, placeholder-only options          |

## What Brijio Cannot Detect

These require CSS/rendered analysis that Brijio doesn't provide:

- **Color contrast ratios** — needs computed styles and colors
- **Keyboard focus order** — needs interactive testing
- **Screen reader output** — needs ARIA computation
- **Touch target sizes** — needs CSS layout information
- **Animation/motion** — needs runtime observation

For these, recommend the user run Lighthouse or axe on the page directly.

## Workflow

### 1. Check Connection

Call `list_browsers` to confirm a browser is connected and on the target page.

### 2. Read the Full Page

Call `read_current_page` with `includeContent: true` to get all available data.
For large pages, also call `list_resources` and `read_resource` to get content
chunks.

### 3. Audit Links

```
For each link in links[]:
  - Is text empty? → "Missing link text"
  - Is text generic ("click here", "read more", "more", "here")? → "Vague link text"
  - Is url a hash-only anchor ("#")? → "Empty anchor link"
  - Does text contain a URL instead of description? → "URL as link text"
```

### 4. Audit Actions (Buttons)

```
For each action in actions[]:
  - Is text empty? → "Unlabeled button"
  - Is text a single character or icon? → "Possible icon button without aria-label"
  - Is text generic ("Submit", "OK")? → Note: may need more context
```

### 5. Audit Form Controls

```
For each form in forms[]:
  For each control in controls[]:
    - Is label empty or missing? → "Unlabeled form control"
    - Is label generic ("Enter text", "Field 1")? → "Generic form label"
    - Is type "hidden"? → Note: verify it's intentional
    - For type "select-one" or "select-multiple":
      - Are options empty? → "Empty select dropdown"
      - Is first option a placeholder ("Choose...", "Select...")?
        → Note placeholder option exists
    - If required but no visual indicator? → "Required field without indicator"
```

### 6. Audit Content (Heuristics)

```
For content chunks:
  - Multiple h1 elements? → "Multiple h1 headings on single page"
  - h3 without preceding h2? → "Skipped heading level"
  - Text with ALL CAPS segments? → "Possible screen reader abbreviation issue"
  - Very long paragraphs? → "Consider breaking into smaller sections"
```

### 7. Output Audit Report

```markdown
## Accessibility Audit: [Page Title]

**URL:** https://example.com/settings
**Date:** 2026-05-28
**Browsers:** Chrome (connected)

### Critical (WCAG Level A)

- 🔴 [form-3, control "email"] Missing label — screen readers cannot identify
  this field
- 🔴 [link "click here"] Vague link text — "click here" doesn't describe the
  destination

### Important (WCAG Level AA)

- 🟡 [form-1, control "phone"] Generic label "Enter text" — should describe
  the expected format
- 🟡 [action "✕"] Icon-only button — needs aria-label for screen readers

### Minor (Best Practice)

- ⚪ [heading] Skipped h2 level — page has h1 then h3, no h2
- ⚪ [form-2, select "country"] Placeholder option "Choose..." — acceptable but
  consider aria-label

### Summary

- Critical: 2
- Important: 2
- Minor: 2
- Total issues: 6
```

## Pitfalls

### Dynamic Content

Pages may load content after the initial read. If you suspect dynamic content:

1. Click any "Load more" or "Expand" actions
2. Re-read the page
3. Audit the updated content

### Single-Page Applications

SPA pages may have multiple "views" that share the same URL. Ask the user to
navigate to each view and audit separately. Report the URL + view name (e.g.,
"Settings > Privacy" not just "/settings").

### Authenticated Context

Some accessibility features only appear for logged-in users (skip links,
admin menus, user-specific navigation). These are precisely the features this
skill is designed to audit — but remember the same page may look different to
different user roles.

### False Positives

- Not every icon button is a11y failure — some use `aria-label` which
  Brijio doesn't surface directly. Flag these as "possible" issues.
- "Choose..." placeholder options are a common pattern — flag as minor, not
  critical.
- Multiple h1s may be intentional in section-based designs — flag as minor.
