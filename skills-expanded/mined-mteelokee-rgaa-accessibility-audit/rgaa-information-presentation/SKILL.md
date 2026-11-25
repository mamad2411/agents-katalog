---
name: rgaa-information-presentation
description: "Audit a web page for RGAA v4.1.2 Theme 10 – Information presentation accessibility compliance. Checks that CSS controls presentation, content remains visible without CSS, information is preserved without CSS, text resizes to 200% without loss, background/foreground colors are paired, link distinction is visible, focus is visible, hidden content is properly managed, information is not conveyed by shape/size/position alone, responsive reflow works at 320px, text spacing is adjustable, and hover/focus additional content is dismissible/hoverable/persistent. Use this skill when someone asks to check CSS accessibility, responsive design, focus visibility, zoom compliance, or RGAA Theme 10."
---

# RGAA Information Presentation Accessibility Audit (Theme 10)

Audits a web page against the 14 criteria of RGAA v4.1.2 Theme 10: Information Presentation.

## Audit procedure

### Step 1: Gather presentation data

```javascript
(() => {
  const data = {};

  // Check CSS usage for presentation
  data.inlineStyles = document.querySelectorAll('[style]').length;

  // Focus visibility check
  data.focusElements = [];
  document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]').forEach(el => {
    const style = getComputedStyle(el);
    data.focusElements.push({
      tag: el.tagName.toLowerCase(),
      type: el.type || null,
      outlineStyle: style.outlineStyle,
      outlineWidth: style.outlineWidth,
      outlineColor: style.outlineColor,
      text: el.textContent.trim().substring(0, 40)
    });
  });

  // Hidden content
  data.hiddenContent = [];
  document.querySelectorAll('[aria-hidden="true"], [hidden], .sr-only, .visually-hidden').forEach(el => {
    data.hiddenContent.push({
      tag: el.tagName.toLowerCase(),
      ariaHidden: el.getAttribute('aria-hidden'),
      hidden: el.hasAttribute('hidden'),
      display: getComputedStyle(el).display,
      visibility: getComputedStyle(el).visibility,
      hasText: !!el.textContent.trim(),
      classes: el.className?.toString().substring(0, 60)
    });
  });

  // Check for content visible only via CSS (::before/::after with content)
  data.cssContentCount = 0;
  // This requires stylesheet inspection, flagging for manual review

  // Viewport meta
  const viewport = document.querySelector('meta[name="viewport"]');
  data.viewport = viewport ? viewport.getAttribute('content') : null;

  // Check horizontal scroll at narrow width
  data.bodyScrollWidth = document.body.scrollWidth;
  data.viewportWidth = window.innerWidth;

  return JSON.stringify(data, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 10.1** – CSS controls presentation.
CSS stylesheets (not inline styles or HTML attributes) should control layout and visual presentation. Check for `<font>`, `bgcolor`, `align`, `valign` HTML attributes, and excessive inline styles.

**Criterion 10.2** – Visible informative content remains present when CSS is disabled.
Content generated via CSS `::before`/`::after` with `content:` that carries information must also be available in the DOM. Test by disabling CSS.

**Criterion 10.3** – Information remains comprehensible when CSS is disabled.
Content should remain readable and logically ordered without CSS.

**Criterion 10.4** – Text remains readable at 200% zoom.
When browser zoom is set to 200%, text must not overflow containers, be truncated, or overlap. No horizontal scrollbar should appear for text content. The `meta viewport` must not set `maximum-scale=1` or `user-scalable=no`.

**Criterion 10.5** – CSS foreground and background colors are paired.
If CSS sets a text color, it must also set the background color (and vice versa). This prevents invisible text with high-contrast user stylesheets.

**Criterion 10.6** – Links are visually distinguishable.
Links within text blocks must be distinguishable from surrounding text by more than color alone (underline, border, font-weight, icon, etc.) or have 3:1 contrast with surrounding text.

**Criterion 10.7** – Focus is visible on every focusable element.
Every element receiving keyboard focus must have a visible focus indicator. Check that `outline: none` is not used without a replacement focus style.

**Criterion 10.8** – Hidden content is correctly hidden from assistive tech.
Content hidden with `display:none` or `visibility:hidden` should also be hidden from screen readers (no conflicting `aria-hidden="false"`). Content intended for screen readers only (`.sr-only`) should use the clip/clip-path technique, not `display:none`.

**Criterion 10.9** – Information not conveyed by shape or position alone.
Instructions like "click the round button" or "see the sidebar" must also provide a textual alternative.

**Criterion 10.10** – Information not conveyed by shape, size, or position alone.
Same principle: visual-only cues need text equivalents.

**Criterion 10.11** – Content reflows without loss at 320px width (or 256px height for horizontal content).
At 400% zoom (equivalent to 320px viewport), content must reflow without horizontal scrolling (except for data tables, maps, diagrams, video, code blocks). Check with viewport resize.

**Criterion 10.12** – Text spacing can be adjusted.
Users must be able to increase: line height to 1.5×, paragraph spacing to 2× font size, letter spacing to 0.12× font size, word spacing to 0.16× font size — without loss of content or functionality.

**Criterion 10.13** – Additional content on focus/hover is dismissible, hoverable, persistent.
Tooltips and popovers appearing on hover/focus must be:
- Dismissible (Escape key or moving pointer without moving focus)
- Hoverable (pointer can move over the additional content)
- Persistent (stays visible until dismissed or focus/hover lost)

**Criterion 10.14** – Additional CSS-only content is accessible.
Content revealed purely via CSS (`:hover`, `:focus`) must be reachable and usable with keyboard.

### Step 3: Visual testing

Several criteria require visual verification:
- Take a screenshot at normal zoom and at 200% zoom to compare
- Test at 320px width for reflow
- Tab through the page to verify focus visibility
- Apply text spacing overrides and verify no content is lost

### Step 4: Generate report

WCAG references: 9.1.3.1 (A), 9.1.3.2 (A), 9.1.3.3 (AA), 9.1.4.4 (AA), 9.1.4.8 (AAA), 9.1.4.10 (AA), 9.1.4.12 (AA), 9.1.4.13 (AA), 9.2.4.7 (AA)
