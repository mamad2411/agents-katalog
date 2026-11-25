---
name: rgaa-navigation
description: "Audit a web page for RGAA v4.1.2 Theme 12 – Navigation accessibility compliance. Checks for two navigation systems (menu + sitemap or search), consistent menus across pages, relevant sitemap, accessible sitemap and search, labeled landmark regions, skip links to main content, coherent tab order, no keyboard traps, single-key shortcut controls, and dismissible hover/focus content. Use this skill when someone asks to check navigation accessibility, verify RGAA Theme 12, audit keyboard navigation, skip links, or tab order."
---

# RGAA Navigation Accessibility Audit (Theme 12)

Audits a web page against the 11 criteria of RGAA v4.1.2 Theme 12: Navigation.

## Audit procedure

### Step 1: Gather navigation data

```javascript
(() => {
  const nav = {};

  // Navigation systems
  nav.navElements = [];
  document.querySelectorAll('nav, [role="navigation"]').forEach(el => {
    nav.navElements.push({
      tag: el.tagName.toLowerCase(),
      ariaLabel: el.getAttribute('aria-label'),
      ariaLabelledby: el.getAttribute('aria-labelledby'),
      linkCount: el.querySelectorAll('a').length,
      firstLinks: Array.from(el.querySelectorAll('a')).slice(0, 5).map(a => ({
        text: a.textContent.trim().substring(0, 40),
        href: a.href?.substring(0, 80)
      }))
    });
  });

  // Search form
  nav.searchForm = null;
  const searchInput = document.querySelector('input[type="search"], [role="search"] input, input[name*="search"], input[name*="query"], input[name*="q"]');
  if (searchInput) {
    const searchContainer = searchInput.closest('[role="search"], form');
    nav.searchForm = {
      hasRoleSearch: !!document.querySelector('[role="search"]'),
      inputType: searchInput.type,
      inputLabel: searchInput.getAttribute('aria-label') || document.querySelector(`label[for="${searchInput.id}"]`)?.textContent.trim(),
      isInNav: !!searchInput.closest('nav, [role="navigation"]')
    };
  }

  // Skip links
  nav.skipLinks = [];
  const firstLinks = Array.from(document.querySelectorAll('a[href^="#"]')).slice(0, 10);
  firstLinks.forEach(a => {
    const target = a.getAttribute('href');
    const targetEl = target && target.length > 1 ? document.querySelector(target) : null;
    nav.skipLinks.push({
      text: a.textContent.trim().substring(0, 60),
      href: target,
      targetExists: !!targetEl,
      targetTag: targetEl?.tagName.toLowerCase(),
      targetRole: targetEl?.getAttribute('role'),
      isVisible: getComputedStyle(a).position !== 'absolute' || getComputedStyle(a).clip !== 'rect(0px, 0px, 0px, 0px)',
      becomesVisible: !!a.matches(':focus-within, :focus') || a.className.includes('skip') || a.className.includes('sr-only')
    });
  });

  // Sitemap link
  nav.sitemapLink = null;
  document.querySelectorAll('a').forEach(a => {
    const text = a.textContent.trim().toLowerCase();
    if (text.includes('plan du site') || text.includes('sitemap') || text.includes('plan de site')) {
      nav.sitemapLink = { text: a.textContent.trim(), href: a.href?.substring(0, 100) };
    }
  });

  // Landmark regions
  nav.landmarks = [];
  document.querySelectorAll('header, footer, main, nav, aside, [role="banner"], [role="main"], [role="contentinfo"], [role="navigation"], [role="complementary"], [role="search"], [role="region"]').forEach(el => {
    nav.landmarks.push({
      tag: el.tagName.toLowerCase(),
      role: el.getAttribute('role') || el.tagName.toLowerCase(),
      ariaLabel: el.getAttribute('aria-label'),
      ariaLabelledby: el.getAttribute('aria-labelledby')
    });
  });

  // Tab order check: get all focusable elements in DOM order
  const focusable = document.querySelectorAll('a[href], button:not([disabled]), input:not([disabled]):not([type="hidden"]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])');
  nav.focusableCount = focusable.length;
  nav.positiveTabindexCount = document.querySelectorAll('[tabindex]:not([tabindex="0"]):not([tabindex="-1"])').length;

  // Keyboard shortcut attributes
  nav.accesskeys = [];
  document.querySelectorAll('[accesskey]').forEach(el => {
    nav.accesskeys.push({
      key: el.getAttribute('accesskey'),
      tag: el.tagName.toLowerCase(),
      text: el.textContent.trim().substring(0, 40)
    });
  });

  return JSON.stringify(nav, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 12.1** – Two navigation systems exist.
The site must provide at least two of: navigation menu, sitemap, search engine. This is a site-wide criterion.

**Criterion 12.2** – Menus and navigation bars are consistent across pages.
The main navigation must be present in the same position and same order on every page. Compare with other pages of the site.

**Criterion 12.3** – Sitemap page is relevant.
If a sitemap exists, it must represent the actual site structure and all pages must be reachable from it.

**Criterion 12.4** – Sitemap is accessible from every page.
The sitemap link must be accessible via the same mechanism on every page (usually in header or footer).

**Criterion 12.5** – Search engine is reachable consistently.
The search function must be accessible from the same location on every page.

**Criterion 12.6** – Landmark regions are consistently identified.
Regions appearing on multiple pages (`<header>`, `<nav>`, `<main>`, `<footer>`) must have the same labels across pages. When multiple landmarks of the same type exist, each must have a distinct `aria-label`.

**Criterion 12.7** – Skip link to main content exists.
There must be a skip link (first or among the first focusable elements) allowing keyboard users to jump to the main content area. The link target must exist and be the main content region.

**Criterion 12.8** – Tab order is coherent.
The tab order must follow the visual reading order. Check for `tabindex` values > 0 (which disrupt natural order) and ensure no confusing focus jumps.

**Criterion 12.9** – No keyboard traps.
Every focusable element must allow the user to move focus away using Tab, Shift+Tab, Escape, or arrow keys. Test by tabbing through the entire page.

**Criterion 12.10** – Single-key shortcuts can be deactivated or remapped.
If character key shortcuts (single letter/number/symbol) exist, they must be deactivatable or remappable, or active only when the relevant component has focus.

**Criterion 12.11** – Additional content on hover/focus is dismissible.
Content appearing on hover or focus (tooltips, dropdowns) must be dismissible (Escape), hoverable (pointer can move to it), and persistent (stays until dismissed).

### Step 3: Keyboard testing

Tab through the page to verify:
1. Skip link works and is visible on focus
2. All navigation items are reachable by keyboard
3. Tab order is logical
4. No keyboard traps exist
5. Dropdowns and submenus work with keyboard

### Step 4: Generate report

WCAG references: 9.2.1.1 (A), 9.2.1.2 (A), 9.2.1.4 (A), 9.2.4.1 (A), 9.2.4.3 (A), 9.2.4.5 (AA), 9.2.4.8 (AAA), 9.3.2.3 (AA)
