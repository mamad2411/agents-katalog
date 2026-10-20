---
name: responsive-mobile-first
description: Mobile-first responsive design standards — breakpoints, fluid typography, container queries, touch-friendly
globs: ["**/*.tsx", "**/*.jsx", "**/*.css", "**/*.scss"]
alwaysApply: false
---

# Mobile-First Responsive Design Standards

Mobile-first design means starting with the smallest screen (320px) and progressively enhancing for larger screens. This approach forces you to prioritize content and build better experiences.

---

## Mobile-First Approach

**ALWAYS**:
- Start with mobile base styles (320px)
- Add media queries for larger screens (progressive enhancement)
- Use flexible layouts: flexbox, grid, percentage widths
- Fluid typography: clamp() for smooth scaling
- Flexible images: responsive images, aspect-ratio preservation
- Test on real devices (emulators aren't enough)

**NEVER**:
- Desktop-first design (cutting off mobile is harder)
- Fixed widths (breaks on different screens)
- Static font sizes (doesn't scale)
- Horizontal scroll on mobile (users hate it)
- Assume all devices are touchscreens or mice

### ✅ GOOD Mobile-First Structure

```css
/* Mobile base: 320px - everything here */
.container {
  width: 100%;
  padding: 0 var(--spacing-base);  /* 16px padding */
  max-width: 100%;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;  /* Single column on mobile */
  gap: var(--spacing-base);
  padding: var(--spacing-base);
}

.header {
  font-size: clamp(1rem, 4vw, 1.5rem);  /* Scales with viewport */
}

h1 {
  font-size: clamp(1.5rem, 6vw, 3rem);  /* Scales smoothly */
}

/* Tablet: 768px and up */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);  /* 2 columns on tablet */
  }
}

/* Desktop: 1024px and up */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);  /* 3 columns on desktop */
  }
}

/* Large desktop: 1280px and up */
@media (min-width: 1280px) {
  .container {
    max-width: 1200px;
  }
}
```

### ❌ BAD Desktop-First

```css
/* ❌ Starting with desktop, cutting off mobile */
.container {
  width: 1200px;  /* Fixed desktop width */
  margin: 0 auto;
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);  /* 4 columns everywhere! */
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);  /* Retrofitting mobile ❌ */
  }
}

/* ❌ Static font sizes */
h1 {
  font-size: 48px;  /* Doesn't scale with viewport */
}
```

---

## Breakpoints Strategy

**ALWAYS**:
- Use consistent breakpoints across project
- Mobile-first: 320px base, enhance upward
- Breakpoints: 480px (small), 768px (tablet), 1024px (desktop), 1280px (large), 1536px (2xl)
- Name breakpoints semantically (sm, md, lg, xl, 2xl)
- Test at each breakpoint

**NEVER**:
- Arbitrary breakpoints (640px, 992px, etc.)
- Too many breakpoints (overhead, maintenance)
- Device-specific breakpoints (iPad, iPhone — use viewport sizes)
- Breakpoints in content (design to breakpoints, not content)

### ✅ GOOD Breakpoint System

```css
/* Define in one place */
:root {
  --breakpoint-sm: 480px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}

/* Use throughout */
@media (min-width: 480px) {
  /* Small: phones, landscape */
}

@media (min-width: 768px) {
  /* Medium: tablets, portrait */
}

@media (min-width: 1024px) {
  /* Large: desktops, tablets landscape */
}

@media (min-width: 1280px) {
  /* Extra large: wide desktops */
}

/* SASS mixin for reusability */
@mixin media-sm {
  @media (min-width: 480px) {
    @content;
  }
}

@mixin media-md {
  @media (min-width: 768px) {
    @content;
  }
}

.card {
  padding: var(--spacing-sm);
  
  @include media-md {
    padding: var(--spacing-base);
  }
}
```

---

## Fluid Typography (clamp)

**ALWAYS**:
- Use clamp() for smooth scaling: clamp(min, preferred, max)
- Scale typography with viewport (not jumpy at breakpoints)
- Maintain readability across all sizes
- Responsive font sizes without media queries

**NEVER**:
- Static font sizes (doesn't adapt)
- Font size jumps (looks broken)
- unreadable small font on mobile
- Unreadable large font on desktop

### ✅ GOOD Fluid Typography

```css
/* clamp(minimum, preferred, maximum) */

/* Body text: 1rem (16px) to 1.125rem (18px) */
body {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
}

/* Heading: 1.5rem (24px) to 2rem (32px) */
h2 {
  font-size: clamp(1.5rem, 4vw, 2rem);
}

/* Large heading: 2rem (32px) to 3rem (48px) */
h1 {
  font-size: clamp(2rem, 6vw, 3rem);
}

/* Small text: 0.875rem (14px) to 1rem (16px) */
small {
  font-size: clamp(0.875rem, 2vw, 1rem);
}

/* Result: smooth scaling, no jumps, readable everywhere */
```

### ❌ BAD Fixed Fonts

```css
/* ❌ Static font size */
h1 { font-size: 48px; }  /* Too big on mobile, doesn't scale */
p { font-size: 16px; }   /* OK, but no scaling */

/* ❌ Font size jumps at breakpoint */
h1 { font-size: 32px; }
@media (min-width: 768px) {
  h1 { font-size: 48px; }  /* Jump! Looks broken */
}
```

---

## Images & Media

**ALWAYS**:
- Use responsive images with srcset
- Preserve aspect ratio with aspect-ratio CSS
- Lazy loading: loading="lazy" on images
- WebP format with fallbacks
- Alt text on all images
- Max-width on images (prevent overflow)

**NEVER**:
- Fixed image sizes (breaks layout)
- Large images on mobile (slow, burns data)
- Missing alt text
- Stretching/squishing images (ugly)

### ✅ GOOD Responsive Images

```html
<!-- Responsive image with srcset -->
<img
  src="image-400.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="
    (max-width: 480px) 100vw,
    (max-width: 768px) 80vw,
    1200px
  "
  alt="Description of image"
  loading="lazy"
/>

<!-- Picture with WebP + fallback -->
<picture>
  <source srcset="image.webp" type="image/webp" />
  <source srcset="image.jpg" type="image/jpeg" />
  <img src="image.jpg" alt="Description" />
</picture>

<!-- Aspect ratio preservation -->
<img
  src="image.jpg"
  alt="Description"
  style="aspect-ratio: 16/9; width: 100%; height: auto;"
/>

<!-- CSS aspect ratio -->
.image-wrapper {
  aspect-ratio: 16/9;
  overflow: hidden;
}

.image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### ❌ BAD Images

```html
<!-- ❌ Large image, no optimization -->
<img src="huge-4000px-image.jpg" />  <!-- Slow! -->

<!-- ❌ Fixed size, breaks on mobile -->
<img src="image.jpg" width="800" height="600" />

<!-- ❌ Missing alt text -->
<img src="image.jpg" />  <!-- Inaccessible ❌ -->

<!-- ❌ Stretching/squishing -->
<img src="image.jpg" style="width: 100%; height: 100%;" />
<!-- Distorted! Use object-fit instead -->
```

---

## Flexible Layouts

**ALWAYS**:
- Use flexbox for 1D layouts (rows or columns)
- Use CSS Grid for 2D layouts (rows + columns)
- Flexible widths: percentage, auto, fr units
- Gaps instead of margins (cleaner, more predictable)
- No fixed pixel widths (use max-width)

**NEVER**:
- Float-based layouts (outdated)
- Fixed pixel widths everywhere
- Hardcoded container sizes
- Overflow issues (missing overflow handling)

### ✅ GOOD Flexible Layouts

```css
/* Flexbox for navigation */
nav {
  display: flex;
  gap: var(--spacing-base);
  flex-wrap: wrap;  /* Wraps on small screens */
}

nav a {
  flex: 1;  /* Takes equal space */
  min-width: 100px;  /* But has minimum */
}

/* Grid for cards */
.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-base);
}

/* Responsive grid */
.grid-2col {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-base);
}

@media (min-width: 768px) {
  .grid-2col {
    grid-template-columns: 1fr 1fr;
  }
}

/* Flexible container */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-base);
}
```

### ❌ BAD Layouts

```css
/* ❌ Float-based (outdated) */
.col {
  float: left;
  width: 50%;
}

/* ❌ Fixed widths */
.sidebar {
  width: 300px;  /* Breaks on small screens */
}

.content {
  width: 900px;  /* Might overflow mobile */
}

/* ❌ No gap handling */
.card {
  margin: 10px;  /* Margin stacking issues */
}

/* ❌ Overflow issues */
.container {
  width: 100vw;  /* Causes horizontal scroll! */
}
```

---

## Layout Shift Prevention (CLS)

**ALWAYS**:
- Reserve space for images (aspect-ratio or height)
- Load fonts early (avoid layout shift)
- Lazy load images below the fold
- Avoid dynamic content insertion above the fold
- Stable layout from initial load

**NEVER**:
- Images without dimensions
- Late font loads (shifts text)
- Ad/banner insertion after load
- Surprise content insertion (shifts layout)

### ✅ GOOD CLS Prevention

```html
<!-- Reserve space with aspect-ratio -->
<img
  src="image.jpg"
  alt="Description"
  style="aspect-ratio: 16/9; width: 100%; height: auto;"
/>

<!-- Or explicit dimensions -->
<img
  src="image.jpg"
  alt="Description"
  width="1200"
  height="675"
  style="width: 100%; height: auto;"
/>

<!-- Load fonts early -->
<link
  rel="preload"
  href="font.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

### ❌ BAD CLS

```html
<!-- ❌ Image without dimensions (layout shift) -->
<img src="image.jpg" />

<!-- ❌ Surprise banner insertion -->
<body>
  <!-- Content -->
  <script>
    // Loads after page renders, shifts layout!
    document.body.insertAdjacentHTML('afterbegin', '<banner>Ad</banner>');
  </script>
</body>
```

---

## Responsive Design Checklist

- [ ] Mobile-first base styles (320px)
- [ ] Progressive enhancement (add styles per breakpoint)
- [ ] Breakpoints: 480px, 768px, 1024px, 1280px, 1536px
- [ ] Fluid typography with clamp()
- [ ] Flexible layouts (flexbox, grid, no fixed widths)
- [ ] Responsive images (srcset, aspect-ratio, lazy loading)
- [ ] Touch targets 44×44px, 8px gaps
- [ ] No horizontal scroll
- [ ] Max-width on containers
- [ ] No layout shift (CLS < 0.1)
- [ ] Tested on real mobile devices
- [ ] Tested in landscape orientation
- [ ] Print styles if needed
- [ ] Prefers-reduced-motion respected

---

## Testing Checklist

- [ ] Chrome DevTools device emulation
- [ ] Real device testing (iPhone, Android, iPad, laptop)
- [ ] Landscape orientation
- [ ] Touch interactions (tap, swipe, long-press)
- [ ] Keyboard navigation (tab, enter, escape)
- [ ] Network throttling (slow 3G)
- [ ] Accessibility testing (screen reader)

---

## Summary

Mobile-first responsive design:
1. **Mobile base** — Simplest, smallest screens
2. **Progressive enhancement** — Add complexity for larger screens
3. **Flexible layouts** — Adapt to any screen size
4. **Fluid typography** — Scales smoothly
5. **Responsive images** — Optimal for each device
6. **Touch-friendly** — Works on all input methods

This approach creates better experiences for everyone, regardless of device.
