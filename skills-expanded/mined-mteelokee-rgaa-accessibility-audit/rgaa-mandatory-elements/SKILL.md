---
name: rgaa-mandatory-elements
description: "Audit a web page for RGAA v4.1.2 Theme 8 – Mandatory HTML elements accessibility compliance. Checks for valid doctype, valid generated source code, default page language, valid language codes, page title presence and relevance, language change indicators, proper use of HTML tags (not for presentation only), and reading direction changes. Use this skill when someone asks to check HTML validity, page language, page title, RGAA Theme 8, or basic HTML accessibility requirements."
---

# RGAA Mandatory Elements Accessibility Audit (Theme 8)

Audits a web page against the 10 criteria of RGAA v4.1.2 Theme 8: Mandatory Elements.

## Audit procedure

### Step 1: Gather page metadata

```javascript
(() => {
  const html = document.documentElement;
  const results = {
    doctype: document.doctype ? `<!DOCTYPE ${document.doctype.name}>` : null,
    htmlLang: html.getAttribute('lang'),
    htmlXmlLang: html.getAttribute('xml:lang'),
    htmlDir: html.getAttribute('dir'),
    title: document.title,
    charset: document.characterSet,
    metaCharset: document.querySelector('meta[charset]')?.getAttribute('charset'),

    // Language changes
    langChanges: [],

    // Tags used for presentation only
    presentationTags: {
      hasInlineStyles: document.querySelectorAll('[style]').length,
      bTags: document.querySelectorAll('b').length,
      iTags: document.querySelectorAll('i').length,
      sTags: document.querySelectorAll('s').length,
      uTags: document.querySelectorAll('u').length,
      fontTags: document.querySelectorAll('font').length,
      centerTags: document.querySelectorAll('center').length,
      bigTags: document.querySelectorAll('big').length,
      smallUsedForStyle: 0,
      brSequences: 0
    },

    // Direction changes
    dirChanges: []
  };

  // Language changes in content
  document.querySelectorAll('[lang], [xml\\:lang]').forEach(el => {
    if (el !== html) {
      results.langChanges.push({
        tag: el.tagName.toLowerCase(),
        lang: el.getAttribute('lang'),
        xmlLang: el.getAttribute('xml:lang'),
        text: el.textContent.trim().substring(0, 60)
      });
    }
  });

  // Check for consecutive <br> (presentational use)
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  let node;
  while (node = walker.nextNode()) {
    if (node.tagName === 'BR' && node.nextElementSibling?.tagName === 'BR') {
      results.presentationTags.brSequences++;
    }
  }

  // Direction changes
  document.querySelectorAll('[dir]').forEach(el => {
    if (el !== html) {
      results.dirChanges.push({
        tag: el.tagName.toLowerCase(),
        dir: el.getAttribute('dir'),
        text: el.textContent.trim().substring(0, 60)
      });
    }
  });

  return JSON.stringify(results, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 8.1** – Page has a doctype.
The page must start with `<!DOCTYPE html>` (HTML5) or a valid DTD reference.

**Criterion 8.2** – Generated source code is valid.
Check for critical validity issues:
- No duplicate `id` attributes
- Tags are properly opened and closed
- Tags are properly nested
- Attributes are not duplicated on the same element

```javascript
// Quick duplicate ID check
(() => {
  const ids = {};
  const duplicates = [];
  document.querySelectorAll('[id]').forEach(el => {
    const id = el.id;
    if (ids[id]) duplicates.push(id);
    ids[id] = (ids[id] || 0) + 1;
  });
  return JSON.stringify({ duplicateIds: duplicates, totalIds: Object.keys(ids).length });
})()
```

**Criterion 8.3** – Default language is present.
`<html>` must have a `lang` attribute (and/or `xml:lang` for XHTML).

**Criterion 8.4** – Language code is valid and relevant.
The `lang` value must be a valid ISO 639-1/639-2 code and match the actual language of the page content. Common codes: fr, en, de, es, it, pt, nl, ar, zh, ja.

**Criterion 8.5** – Page has a title.
`<title>` element must exist and not be empty.

**Criterion 8.6** – Page title is relevant.
The title should identify the page content and ideally include the site name. It should be unique across the site. Check that it is not generic like "Home" or "Untitled".

**Criterion 8.7** – Language changes are indicated in the code.
Any passage of text in a different language than the page default must have a `lang` attribute on a surrounding element. This requires visual/content inspection.

**Criterion 8.8** – Language change codes are valid.
Each `lang` attribute on sub-elements must be a valid ISO language code.

**Criterion 8.9** – Tags are not used for presentation only.
HTML tags must be used according to their semantic meaning:
- No `<h1>`-`<h6>` used just for visual styling
- No `<blockquote>` used just for indentation
- No `<table>` used just for layout without `role="presentation"`
- No consecutive `<br>` used for spacing
- No deprecated presentational elements (`<font>`, `<center>`, `<big>`, etc.)

**Criterion 8.10** – Reading direction changes are signaled.
Content in right-to-left scripts (Arabic, Hebrew) must use `dir="rtl"`. Content in left-to-right scripts within an RTL context must use `dir="ltr"`.

### Step 3: Generate report

For each criterion, report the status and any issues found. Language-related criteria (8.7, 8.8) and semantic misuse (8.9) may require content analysis beyond pure code inspection.

WCAG references: 9.1.3.1 (A), 9.2.4.2 (A), 9.3.1.1 (A), 9.3.1.2 (AA), 9.4.1.1 (A), 9.4.1.2 (A)
