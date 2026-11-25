---
name: rgaa-information-structure
description: "Audit a web page for RGAA v4.1.2 Theme 9 – Information structure accessibility compliance. Checks that headings are used to structure information, the document structure is coherent (header/nav/main/footer landmarks), lists use proper markup (ul/ol/dl), and quotations are correctly marked up. Use this skill when someone asks to check heading structure, landmark regions, semantic HTML structure, RGAA Theme 9, or content organization accessibility."
---

# RGAA Information Structure Accessibility Audit (Theme 9)

Audits a web page against the 4 criteria of RGAA v4.1.2 Theme 9: Information Structure.

## Audit procedure

### Step 1: Gather structural data

```javascript
(() => {
  const structure = {};

  // Headings hierarchy
  structure.headings = [];
  document.querySelectorAll('h1,h2,h3,h4,h5,h6,[role="heading"]').forEach(el => {
    const level = el.tagName?.match(/H(\d)/)?.[1] || el.getAttribute('aria-level');
    structure.headings.push({
      level: parseInt(level),
      text: el.textContent.trim().substring(0, 80),
      tag: el.tagName.toLowerCase(),
      ariaLevel: el.getAttribute('aria-level'),
      isHidden: getComputedStyle(el).display === 'none' || getComputedStyle(el).visibility === 'hidden',
      ariaHidden: el.getAttribute('aria-hidden')
    });
  });

  // Landmark regions
  structure.landmarks = [];
  const landmarkSelectors = {
    'banner': 'header, [role="banner"]',
    'navigation': 'nav, [role="navigation"]',
    'main': 'main, [role="main"]',
    'contentinfo': 'footer, [role="contentinfo"]',
    'complementary': 'aside, [role="complementary"]',
    'search': '[role="search"], search',
    'form': '[role="form"]',
    'region': '[role="region"]'
  };

  Object.entries(landmarkSelectors).forEach(([type, selector]) => {
    document.querySelectorAll(selector).forEach(el => {
      structure.landmarks.push({
        type: type,
        tag: el.tagName.toLowerCase(),
        role: el.getAttribute('role'),
        ariaLabel: el.getAttribute('aria-label'),
        ariaLabelledby: el.getAttribute('aria-labelledby'),
        text: el.textContent.trim().substring(0, 40)
      });
    });
  });

  // Lists
  structure.lists = {
    ul: document.querySelectorAll('ul').length,
    ol: document.querySelectorAll('ol').length,
    dl: document.querySelectorAll('dl').length,
    liOutsideList: document.querySelectorAll('li:not(ul > li):not(ol > li):not(menu > li)').length,
    dtOutsideDl: document.querySelectorAll('dt:not(dl > dt)').length,
    ddOutsideDl: document.querySelectorAll('dd:not(dl > dd)').length,
    roleList: document.querySelectorAll('[role="list"]').length,
    roleListitem: document.querySelectorAll('[role="listitem"]').length
  };

  // Quotations
  structure.quotations = {
    blockquote: document.querySelectorAll('blockquote').length,
    q: document.querySelectorAll('q').length,
    cite: document.querySelectorAll('cite').length
  };

  return JSON.stringify(structure, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 9.1** – Information is structured by appropriate use of headings.

Check heading hierarchy:
- There should be at least one `<h1>` on the page
- Heading levels should not skip (e.g., h1 → h3 without h2)
- Headings should reflect the actual content organization
- Content sections should start with a heading
- Headings should not be empty

**Criterion 9.2** – Document structure is coherent.

Check landmarks/sectioning:
- The page has a `<header>` or `[role="banner"]`
- The page has a `<nav>` or `[role="navigation"]` (at least one)
- The page has a `<main>` or `[role="main"]` (exactly one)
- The page has a `<footer>` or `[role="contentinfo"]`
- Multiple landmarks of the same type have distinguishing `aria-label` values
- The `<main>` is not nested inside another landmark (except the document itself)
- Content outside landmarks should be minimal

**Criterion 9.3** – Lists are correctly structured.

- Unordered lists use `<ul>` > `<li>`
- Ordered lists use `<ol>` > `<li>`
- Definition lists use `<dl>` > `<dt>` + `<dd>`
- No `<li>` outside of `<ul>`, `<ol>`, or `<menu>`
- No `<dt>` or `<dd>` outside of `<dl>`
- `[role="list"]` contains `[role="listitem"]` children
- Visual lists (items separated by line breaks or commas) that represent a list of items should use proper list markup

**Criterion 9.4** – Quotations are correctly marked up.

- Block quotations use `<blockquote>`
- Inline quotations use `<q>`
- `<blockquote>` and `<q>` are not used for non-quotation purposes (like indentation)
- The `cite` attribute references the source when applicable

### Step 3: Generate report

Present the heading tree visually (indented by level), list all landmarks, and flag any structural issues.

WCAG references: 9.1.3.1 (A), 9.2.4.1 (A), 9.2.4.6 (AA), 9.2.4.10 (AAA)
