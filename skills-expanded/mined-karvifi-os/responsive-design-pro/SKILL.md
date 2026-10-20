---
name: responsive-design-pro
description: Mobile-first responsive design — breakpoints, container queries, fluid typography, touch targets
triggers: [responsive, mobile-first, breakpoints, mobile design, container query, fluid typography]
---

# SKILL: Responsive Design Pro

## Mobile-First Methodology

```css
/* ❌ WRONG: Desktop-first (overrides everywhere) */
.card {
  width: 1200px;  /* Desktop */
}
@media (max-width: 768px) {
  .card { width: 100%; }  /* Mobile override */
}

/* ✅ RIGHT: Mobile-first (progressive enhancement) */
.card {
  width: 100%;  /* Mobile default */
}
@media (min-width: 768px) {
  .card { width: 1200px; }  /* Desktop enhancement */
}
```

## Breakpoint System (Tailwind standard)
```
sm: 640px   — Small tablets
md: 768px   — Tablets  
lg: 1024px  — Laptops
xl: 1280px  — Desktops
2xl: 1536px — Large desktops

Usage:
<div className="w-full md:w-1/2 lg:w-1/3">
  Mobile: full width
  Tablet: half width
  Desktop: third width
</div>
```

## Fluid Typography
```css
/* Scales between 16px (mobile) and 24px (desktop) */
.heading {
  font-size: clamp(1rem, 2vw + 1rem, 1.5rem);
}

/* Or use CSS calc with viewport units */
.heading {
  font-size: calc(1rem + 1vw);
}
```

## Container Queries (New Standard)
```css
/* Instead of viewport breakpoints, query parent container */
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card-title {
  font-size: 1rem;
}

/* If parent container > 400px, increase font */
@container card (min-width: 400px) {
  .card-title {
    font-size: 1.5rem;
  }
}
```

## Touch Targets (Mobile Essential)
```css
/* Minimum 44x44px for touch targets */
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
}

/* Increase hit area without changing visual size */
.icon-button {
  position: relative;
  width: 24px;
  height: 24px;
}

.icon-button::before {
  content: '';
  position: absolute;
  top: -10px;
  right: -10px;
  bottom: -10px;
  left: -10px;
  /* Invisible hit area: 44x44px */
}
```

## Responsive Images
```tsx
<picture>
  {/* Mobile: optimized small image */}
  <source
    media="(max-width: 768px)"
    srcSet="/image-mobile.webp 1x, /image-mobile@2x.webp 2x"
  />
  
  {/* Desktop: larger image */}
  <source
    media="(min-width: 769px)"
    srcSet="/image-desktop.webp 1x, /image-desktop@2x.webp 2x"
  />
  
  {/* Fallback */}
  <img src="/image-desktop.jpg" alt="Description" />
</picture>
```

## Grid Patterns
```tsx
/* Auto-fit: creates as many columns as fit */
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  {cards.map(card => <Card key={card.id} />)}
</div>

/* Result:
   Mobile (< 500px): 1 column
   Tablet (500-750px): 2 columns  
   Desktop (> 1000px): 4 columns
   All automatic, no breakpoints needed
*/
```

## Quality Checks
- [ ] Mobile-first CSS (not desktop-first)
- [ ] Touch targets ≥ 44x44px
- [ ] Breakpoints follow standard (sm/md/lg/xl/2xl)
- [ ] Images optimized per device (responsive images)
- [ ] Typography scales fluidly (clamp or vw units)
- [ ] Tested on real devices (not just browser resize)
- [ ] No horizontal scroll on any screen size
- [ ] Container queries used for component-level responsiveness
