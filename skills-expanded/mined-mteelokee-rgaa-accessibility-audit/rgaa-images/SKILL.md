---
name: rgaa-images
description: "Audit a web page for RGAA v4.1.2 Theme 1 – Images accessibility compliance. Checks that informative images have text alternatives, decorative images are correctly hidden, alternatives are relevant, CAPTCHAs have alternative access, detailed descriptions exist when needed, text images are avoided, and captions are properly linked. Use this skill whenever someone asks to check, audit, or verify image accessibility on a website, or when they mention RGAA images, alt text audit, or image accessibility compliance."
---

# RGAA Images Accessibility Audit (Theme 1)

This skill audits a web page against the 9 criteria of RGAA v4.1.2 Theme 1: Images.

## When to use

Trigger this skill when the user asks to audit image accessibility on a web page, check alt texts, verify RGAA Theme 1 compliance, or any request related to image accessibility verification.

## Prerequisites

You need access to the page via Claude in Chrome (read_page, get_page_text, javascript_tool). Make sure the target page is open in the browser before starting.

## Audit procedure

### Step 1: Gather page data

Use `javascript_tool` to extract all image-related elements from the page:

```javascript
(() => {
  const results = { imgs: [], areas: [], inputImages: [], svgs: [], objects: [], embeds: [], canvas: [], roleImgs: [], iframes: [] };

  // <img> tags
  document.querySelectorAll('img').forEach(el => {
    results.imgs.push({
      src: el.src?.substring(0, 100),
      alt: el.getAttribute('alt'),
      title: el.getAttribute('title'),
      ariaLabel: el.getAttribute('aria-label'),
      ariaLabelledby: el.getAttribute('aria-labelledby'),
      ariaHidden: el.getAttribute('aria-hidden'),
      role: el.getAttribute('role'),
      hasParentFigure: !!el.closest('figure'),
      parentFigureAriaLabel: el.closest('figure')?.getAttribute('aria-label'),
      hasFigcaption: !!el.closest('figure')?.querySelector('figcaption'),
      width: el.naturalWidth,
      height: el.naturalHeight
    });
  });

  // elements with role="img"
  document.querySelectorAll('[role="img"]').forEach(el => {
    if (el.tagName !== 'IMG') {
      results.roleImgs.push({
        tag: el.tagName.toLowerCase(),
        ariaLabel: el.getAttribute('aria-label'),
        ariaLabelledby: el.getAttribute('aria-labelledby'),
        textContent: el.textContent?.substring(0, 100)
      });
    }
  });

  // <svg> tags
  document.querySelectorAll('svg').forEach(el => {
    results.svgs.push({
      role: el.getAttribute('role'),
      ariaLabel: el.getAttribute('aria-label'),
      ariaLabelledby: el.getAttribute('aria-labelledby'),
      ariaHidden: el.getAttribute('aria-hidden'),
      hasTitle: !!el.querySelector('title'),
      titleContent: el.querySelector('title')?.textContent,
      hasDesc: !!el.querySelector('desc'),
      descContent: el.querySelector('desc')?.textContent
    });
  });

  // <area> tags
  document.querySelectorAll('area').forEach(el => {
    results.areas.push({
      href: el.getAttribute('href'),
      alt: el.getAttribute('alt'),
      ariaLabel: el.getAttribute('aria-label')
    });
  });

  // <input type="image">
  document.querySelectorAll('input[type="image"]').forEach(el => {
    results.inputImages.push({
      alt: el.getAttribute('alt'),
      title: el.getAttribute('title'),
      ariaLabel: el.getAttribute('aria-label'),
      src: el.src?.substring(0, 100)
    });
  });

  // <object type="image/...">
  document.querySelectorAll('object[type^="image"]').forEach(el => {
    results.objects.push({
      type: el.type,
      role: el.getAttribute('role'),
      ariaLabel: el.getAttribute('aria-label'),
      ariaHidden: el.getAttribute('aria-hidden')
    });
  });

  // <embed type="image/...">
  document.querySelectorAll('embed[type^="image"]').forEach(el => {
    results.embeds.push({
      type: el.type,
      role: el.getAttribute('role'),
      ariaLabel: el.getAttribute('aria-label'),
      ariaHidden: el.getAttribute('aria-hidden')
    });
  });

  // <canvas>
  document.querySelectorAll('canvas').forEach(el => {
    results.canvas.push({
      role: el.getAttribute('role'),
      ariaLabel: el.getAttribute('aria-label'),
      ariaHidden: el.getAttribute('aria-hidden'),
      fallbackContent: el.textContent?.trim().substring(0, 100)
    });
  });

  return JSON.stringify(results, null, 2);
})()
```

### Step 2: Evaluate each criterion

For each criterion, read the detailed checks from `references/criteria.md` and apply them to the collected data.

**Criterion 1.1** – Informative images must have a text alternative.
Check every `<img>`, `<area>`, `<input type="image">`, `<svg>`, `<object>`, `<embed>`, `<canvas>`, and `[role="img"]` element. If the image conveys information (not decorative), it must have an `alt`, `aria-label`, `aria-labelledby`, or `title` attribute.

**Criterion 1.2** – Decorative images must be ignored by assistive technologies.
Decorative `<img>` must have `alt=""` and no other text alternative, OR `aria-hidden="true"` / `role="presentation"`. Decorative `<svg>` must have `aria-hidden="true"` and no `<title>` or `<desc>`.

**Criterion 1.3** – Text alternatives must be relevant.
When an informative image has an alt text, check that it actually describes the image content meaningfully, not just "image" or a filename.

**Criterion 1.4** – CAPTCHA/test images must identify their nature.
If a CAPTCHA is present, its alternative should say it is a CAPTCHA and describe its function, not its content.

**Criterion 1.5** – CAPTCHAs must have an alternative access method.
If a graphical CAPTCHA exists, verify there is at least one alternative (audio, logic, etc.).

**Criterion 1.6** – Informative images needing a detailed description must have one.
Complex images (charts, infographics) need a `longdesc`, adjacent link, or `aria-describedby` pointing to a detailed description.

**Criterion 1.7** – Detailed descriptions must be relevant.
If a detailed description exists, verify its content is accurate and complete.

**Criterion 1.8** – Text images should be replaced with styled text when possible.
Flag images that contain only text and could be replaced with CSS-styled HTML text (except logos, trademarks, CAPTCHAs).

**Criterion 1.9** – Image captions must be correctly linked.
Images with captions must use `<figure>` + `<figcaption>`, with `role="figure"` and `aria-label` matching the caption.

### Step 3: Generate the report

Produce a structured report with:
- A summary score (number of criteria passed / total applicable)
- For each criterion: status (✅ Passed, ❌ Failed, ⚠️ Warning, N/A), the elements concerned, and recommendations to fix issues
- An overall compliance assessment for Theme 1

## Important notes

- Distinguishing informative from decorative images requires human judgment. Flag ambiguous cases as warnings.
- Alt text relevance is subjective — flag clearly bad alternatives (empty on informative images, filenames, "image", "photo") but note that full relevance assessment may need human review.
- Some tests (like 1.8 on text images) require visual inspection. Use screenshots when needed.
