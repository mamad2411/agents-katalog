---
name: rgaa-frames
description: "Audit a web page for RGAA v4.1.2 Theme 2 – Frames accessibility compliance. Checks that every iframe and frame has a title attribute and that the title is relevant. Use this skill when someone asks to check frame or iframe accessibility, verify RGAA Theme 2, or audit embedded content accessibility on a website."
---

# RGAA Frames Accessibility Audit (Theme 2)

This skill audits a web page against the 2 criteria of RGAA v4.1.2 Theme 2: Frames.

## Audit procedure

### Step 1: Gather frame data

Use `javascript_tool` to extract all frame elements:

```javascript
(() => {
  const frames = [];
  document.querySelectorAll('iframe, frame').forEach(el => {
    frames.push({
      tag: el.tagName.toLowerCase(),
      title: el.getAttribute('title'),
      src: el.src?.substring(0, 150),
      ariaLabel: el.getAttribute('aria-label'),
      ariaHidden: el.getAttribute('aria-hidden'),
      width: el.width,
      height: el.height
    });
  });
  return JSON.stringify(frames, null, 2);
})()
```

### Step 2: Evaluate criteria

**Criterion 2.1** – Every frame must have a title.
Check that every `<iframe>` and `<frame>` has a non-empty `title` attribute.

**Criterion 2.2** – Frame titles must be relevant.
The title must describe the content or purpose of the frame (not just "iframe" or be empty). For example, a YouTube embed should say "Video: [title]" rather than just "YouTube video player".

### Step 3: Generate report

Report for each frame: its source, whether it has a title, and whether that title is relevant. Provide fix recommendations for any issues found.

WCAG references: 9.4.1.2 Name, Role, Value (A)
