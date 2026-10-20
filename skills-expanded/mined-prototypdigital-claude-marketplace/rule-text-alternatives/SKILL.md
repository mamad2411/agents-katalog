---
name: text-alternatives
description: Provide descriptive alt text for meaningful images; empty alt for decorative; alternatives for icons and media
---

# Text Alternatives

WCAG 2.2 SC 1.1.1 (Non-text Content, Level A) requires a text alternative for every non-text element that conveys information. This is one of the highest-impact rules: a missing alt attribute makes an image completely opaque to screen reader users.

## Rules

- **Every `<img>` must have an `alt` attribute.** An `<img>` with no `alt` attribute causes screen readers to read the file path or URL aloud, which is useless or confusing.
- **Meaningful images need descriptive alt text.** The alt should convey the same information the image conveys — not just what it depicts. A chart's alt should summarize the data trend, not say "bar chart".
- **Decorative images need `alt=""`** (empty string). The element remains in the DOM but is hidden from the accessibility tree. Do not use `role="presentation"` alone without `alt=""`.
- **Icon-only buttons need an accessible name.** An SVG icon inside a `<button>` with no text must have either: an `aria-label` on the button, or a visually hidden `<span>` inside the button, or a `<title>` inside the SVG + `aria-labelledby`. Mark the SVG itself `aria-hidden="true"` so the icon's shape/path is not read.
- **Complex images (charts, diagrams, maps) need a long description.** Provide a text summary adjacent to the image, or link to a full description. `alt` alone cannot carry 300 words.
- **`<video>` and `<audio>` must have captions or transcripts.** Pre-recorded video needs captions (SC 1.2.2, Level A). Pre-recorded audio needs a transcript (SC 1.2.1, Level A). Live audio needs real-time captions (SC 1.2.4, Level AA).

## Examples

```tsx
// BAD — no alt attribute
<img src="/hero.jpg" />

// BAD — unhelpful alt
<img src="/revenue-chart.png" alt="chart" />

// GOOD — descriptive alt
<img
  src="/revenue-chart.png"
  alt="Monthly revenue grew 40% from January to June 2024, peaking at $2.4M in June."
/>

// GOOD — decorative image hidden from screen readers
<img src="/decorative-wave.svg" alt="" role="presentation" />
```

```tsx
// BAD — icon button with no accessible name
<button onClick={close}>
  <CloseIcon />
</button>

// GOOD — icon hidden; visible text equivalent provided
<button onClick={close} aria-label="Close dialog">
  <CloseIcon aria-hidden="true" />
</button>

// ALSO GOOD — visually hidden text inside the button
<button onClick={close}>
  <CloseIcon aria-hidden="true" />
  <span className="sr-only">Close dialog</span>
</button>
```

```tsx
// BAD — next/image with no alt
<Image src="/avatar.jpg" width={48} height={48} />

// GOOD
<Image src="/avatar.jpg" alt="Avatar of Sarah Chen" width={48} height={48} />

// GOOD — decorative (alt="" is the explicit signal to next/image as well)
<Image src="/flourish.svg" alt="" width={200} height={40} />
```

## Gotchas

- The "every `<img>` needs `alt`" invariant is non-negotiable; enforce it in CI with the `jsx-a11y/alt-text` lint rule rather than relying on review alone.
- Alt text should not start with "Image of" or "Photo of" — screen readers already announce the element type.
- An alt identical to a caption or adjacent heading is redundant. If the image adds nothing beyond what surrounding text already says, use `alt=""`.
- CSS background images convey no information to screen readers at all. Never use a background image to display content that needs a text alternative; use `<img>` instead.
- `aria-label` on an `<img>` takes precedence over `alt` in the accessibility tree. Don't set both.
