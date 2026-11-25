---
name: rgaa-consultation
description: "Audit a web page for RGAA v4.1.2 Theme 13 – Consultation accessibility compliance. Checks that time limits are controllable, new windows are not opened without warning, downloadable documents are accessible, cryptic content has alternatives, no flashing/seizure-inducing content, moving content is controllable, content works regardless of orientation, touch gestures have alternatives, pointer actions are cancellable, and motion-triggered features can be disabled. Use this skill when someone asks to check content consultation accessibility, verify RGAA Theme 13, audit auto-refresh, new windows, or downloadable documents accessibility."
---

# RGAA Consultation Accessibility Audit (Theme 13)

Audits a web page against the 12 criteria of RGAA v4.1.2 Theme 13: Consultation.

## Audit procedure

### Step 1: Gather consultation data

```javascript
(() => {
  const data = {};

  // Meta refresh
  const metaRefresh = document.querySelector('meta[http-equiv="refresh"]');
  data.metaRefresh = metaRefresh ? metaRefresh.getAttribute('content') : null;

  // Links opening new windows
  data.newWindowLinks = [];
  document.querySelectorAll('a[target="_blank"], a[target="blank"]').forEach(a => {
    data.newWindowLinks.push({
      text: a.textContent.trim().substring(0, 60),
      href: a.href?.substring(0, 100),
      title: a.getAttribute('title'),
      ariaLabel: a.getAttribute('aria-label'),
      hasVisualIndicator: !!a.querySelector('[class*="external"], [class*="new-window"], [aria-hidden]'),
      hasScreenReaderText: !!a.querySelector('.sr-only, .visually-hidden')
    });
  });

  // Downloadable documents
  data.downloadLinks = [];
  document.querySelectorAll('a[href$=".pdf"], a[href$=".doc"], a[href$=".docx"], a[href$=".xls"], a[href$=".xlsx"], a[href$=".ppt"], a[href$=".pptx"], a[href$=".odt"], a[href$=".ods"], a[href$=".odp"], a[download]').forEach(a => {
    data.downloadLinks.push({
      text: a.textContent.trim().substring(0, 60),
      href: a.href?.substring(0, 100),
      format: a.href?.split('.').pop()?.toLowerCase(),
      title: a.getAttribute('title'),
      indicatesFormat: /pdf|doc|xls|ppt|odt/i.test(a.textContent),
      indicatesWeight: /[0-9]+ ?(ko|mo|kb|mb|go|gb)/i.test(a.textContent)
    });
  });

  // Auto-playing or moving content
  data.autoplayMedia = [];
  document.querySelectorAll('video[autoplay], audio[autoplay]').forEach(el => {
    data.autoplayMedia.push({
      tag: el.tagName.toLowerCase(),
      controls: el.controls,
      muted: el.muted,
      loop: el.loop
    });
  });

  // Animations (CSS)
  data.animations = {
    hasAnimations: !!document.querySelector('[class*="animate"], [class*="marquee"], [class*="scroll"], [class*="blink"], [class*="carousel"], [class*="slider"]'),
    marquees: document.querySelectorAll('marquee').length,
    blinkTags: document.querySelectorAll('blink').length
  };

  // Orientation lock
  data.orientationLock = null;
  // Check CSS for orientation media queries (manual step)

  // Touch gesture patterns (manual inspection needed)
  data.hasTouchGestures = !!document.querySelector('[class*="swipe"], [class*="pinch"], [class*="drag"]');

  return JSON.stringify(data, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 13.1** – Time limits are controllable.
If the page auto-refreshes or has a session timeout:
- `<meta http-equiv="refresh">` with a time value must allow the user to stop, extend, or remove the limit
- Session timeouts must warn the user and allow extension
- Exceptions: time limit > 20 hours, real-time events, essential time limits

**Criterion 13.2** – New windows are not opened without warning.
Every `target="_blank"` link must indicate it opens a new window:
- In the link text itself (e.g., "opens in a new window")
- Via `title` attribute mentioning it
- Via a visually hidden `<span>` inside the link
- Via an icon with appropriate alt text

**Criterion 13.3** – Downloadable documents are accessible.
Office documents (PDF, DOC, XLS, PPT, ODT, etc.) available for download must be accessibility-compliant themselves, OR an accessible HTML alternative must be provided.

**Criterion 13.4** – Accessible version of documents is up to date.
If an accessible alternative version exists for a document, it must contain equivalent information and be updated when the original changes.

**Criterion 13.5** – Cryptic content has an alternative.
ASCII art, emoticons, and cryptic syntax must have a text alternative (via `aria-label`, `title`, or `abbr`). Example: ":-)" should have `title="smiling emoticon"`.

**Criterion 13.6** – Cryptic content alternatives are relevant.
The text alternative must accurately describe the meaning.

**Criterion 13.7** – No seizure-inducing flashing.
No content should flash more than 3 times per second. No content should produce sudden brightness changes. This applies to images, videos, animations, and CSS transitions.

**Criterion 13.8** – Moving/blinking content is controllable.
Any auto-playing animation, carousel, scrolling text, or blinking content:
- Must have a pause/stop mechanism
- The mechanism must be the first element (or among the first) before the moving content
- No `<marquee>` or `<blink>` tags

**Criterion 13.9** – Content is usable regardless of screen orientation.
Content must work in both portrait and landscape orientations unless a specific orientation is essential (e.g., a piano app). No CSS `orientation: portrait` lock without alternative.

**Criterion 13.10** – Touch gestures have alternatives.
Complex gestures (multi-finger, path-based like swiping) must have single-pointer alternatives. Examples:
- Swipe carousel → must also have previous/next buttons
- Pinch to zoom → must also have zoom +/- buttons
- Drag to reorder → must also allow click-based reordering

**Criterion 13.11** – Pointer actions are cancellable.
For single-pointer actions:
- Prefer `click`/`mouseup` over `mousedown` (allows cancellation by moving away)
- Down-event actions must have an undo mechanism
- `mouseup` must abort if pointer moved away from the target

**Criterion 13.12** – Motion-triggered features can be disabled.
Features triggered by device motion (shaking, tilting) must:
- Have an accessible alternative (button, control)
- Be disableable by the user

### Step 3: Generate report

For each criterion, check the applicable elements and report issues. Many criteria (document accessibility, orientation, complex gestures) require manual testing beyond code inspection.

WCAG references: 9.1.4.2 (A), 9.2.1.1 (A), 9.2.1.4 (A), 9.2.2.1 (A), 9.2.2.2 (A), 9.2.3.1 (A), 9.2.5.1 (A), 9.2.5.2 (A), 9.2.5.4 (AA), 9.3.2.5 (AAA)
