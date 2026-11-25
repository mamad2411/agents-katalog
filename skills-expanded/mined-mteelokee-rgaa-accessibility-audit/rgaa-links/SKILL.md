---
name: rgaa-links
description: "Audit a web page for RGAA v4.1.2 Theme 6 – Links accessibility compliance. Checks that every link is explicit (its purpose can be understood from its text alone or from context) and that every link has a non-empty accessible name. Use this skill when someone asks to check link accessibility, verify RGAA Theme 6, audit link texts, or check for empty or ambiguous links on a website."
---

# RGAA Links Accessibility Audit (Theme 6)

Audits a web page against the 2 criteria of RGAA v4.1.2 Theme 6: Links.

## Audit procedure

### Step 1: Gather link data

```javascript
(() => {
  const links = [];
  document.querySelectorAll('a[href], [role="link"]').forEach(el => {
    const img = el.querySelector('img');
    const svg = el.querySelector('svg');
    const ariaLabel = el.getAttribute('aria-label');
    const ariaLabelledby = el.getAttribute('aria-labelledby');
    const title = el.getAttribute('title');
    const textContent = el.textContent.trim();

    // Compute accessible name
    let accessibleName = '';
    if (ariaLabelledby) {
      const ids = ariaLabelledby.split(/\s+/);
      accessibleName = ids.map(id => document.getElementById(id)?.textContent.trim() || '').join(' ');
    } else if (ariaLabel) {
      accessibleName = ariaLabel;
    } else if (textContent) {
      accessibleName = textContent;
    } else if (img && img.alt) {
      accessibleName = img.alt;
    } else if (title) {
      accessibleName = title;
    }

    links.push({
      href: el.getAttribute('href')?.substring(0, 120),
      tag: el.tagName.toLowerCase(),
      visibleText: textContent.substring(0, 80),
      accessibleName: accessibleName.substring(0, 120),
      hasImage: !!img,
      imgAlt: img?.getAttribute('alt'),
      hasSvg: !!svg,
      svgTitle: svg?.querySelector('title')?.textContent,
      ariaLabel: ariaLabel,
      ariaLabelledby: ariaLabelledby,
      title: title,
      isEmptyLink: !accessibleName.trim(),
      context: el.closest('p, li, td, th, h1, h2, h3, h4, h5, h6')?.textContent.trim().substring(0, 150)
    });
  });
  return JSON.stringify(links.slice(0, 80), null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 6.1** – Every link is explicit (except in special cases).

A link is explicit if its purpose can be determined from one of the following:
- The link text alone (best)
- The link text combined with its context: the enclosing sentence, paragraph, list item, table cell, or the associated heading, plus aria-label or title attribute

Check for problematic patterns:
- Generic text: "click here", "read more", "learn more", "link", "here" → ❌ unless context makes it clear
- Image-only links where the alt text is generic → ❌
- Links whose visible text and aria-label convey different destinations → ⚠️ Warning (aria-label should start with the visible text per WCAG 2.5.3)

Special cases: ambiguity is acceptable if the link context (sentence, paragraph, list item, heading, table cell, or table headers) makes the destination clear.

**Criterion 6.2** – Every link has a non-empty accessible name.

Check that every `<a href>` and `[role="link"]` element has a computed accessible name that is not empty. Failing patterns:
- `<a href="..."></a>` (empty link)
- `<a href="..."><img src="..." alt=""></a>` (image link with empty alt, no other text)
- `<a href="..."><svg>...</svg></a>` without aria-label or `<title>` in SVG
- `<a href="..."><span></span></a>` (only empty elements)

### Step 3: Generate report

List all problematic links with their current accessible name (or lack thereof), the issue detected, and a recommended fix. Group issues by type:
1. Links with no accessible name at all (critical)
2. Links with generic/ambiguous text (important)
3. Links with mismatched visible text and aria-label (warning)

WCAG references: 9.1.1.1 (A), 9.2.4.4 (A), 9.2.5.3 (A), 9.4.1.2 (A)
