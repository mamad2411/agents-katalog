---
name: mobile-responsive-design
description: |
  Mobile-first responsive design patterns. Apply when building any UI that must work on
  phones, tablets, and desktops. Covers breakpoint strategy, touch targets, responsive
  typography, fluid layouts, and Telegram Mini App specific requirements.
---

# Mobile-First Responsive Design

## Mobile-First Approach
Always write base styles for mobile, then add complexity for larger screens:
```css
/* Mobile first — base styles */
.card { padding: 12px; font-size: 14px; }

/* Tablet */
@media (min-width: 768px) { .card { padding: 20px; font-size: 16px; } }

/* Desktop */
@media (min-width: 1024px) { .card { padding: 28px; } }
```

## Touch Target Requirements
```css
/* Minimum 44×44px for all interactive elements (Apple HIG) */
.btn, .link, input[type="checkbox"], input[type="radio"] {
  min-height: 44px;
  min-width: 44px;
}

/* Adequate spacing between touch targets */
.action-list > * + * { margin-top: 8px; }
```

## Fluid Typography
```css
/* Scales smoothly between breakpoints */
:root {
  --text-base: clamp(14px, 2.5vw, 16px);
  --text-lg: clamp(16px, 3vw, 20px);
  --text-xl: clamp(20px, 4vw, 28px);
  --text-2xl: clamp(24px, 5vw, 36px);
}
```

## Tailwind Responsive Grid
```tsx
// Product grid — 1 col mobile, 2 tablet, 3-4 desktop
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
  {products.map(p => <ProductCard key={p.id} product={p} />)}
</div>

// Sidebar layout — stacked mobile, side-by-side desktop
<div className="flex flex-col lg:flex-row gap-6">
  <aside className="w-full lg:w-72 lg:shrink-0"><Filters /></aside>
  <main className="flex-1 min-w-0"><ProductGrid /></main>
</div>
```

## Telegram Mini App Specifics
```typescript
import WebApp from '@twa-dev/sdk';

// Always initialize and expand
WebApp.ready();
WebApp.expand();

// Use Telegram theme colors
const tgTheme = {
  bg: WebApp.backgroundColor,
  text: WebApp.themeParams.text_color,
  hint: WebApp.themeParams.hint_color,
  button: WebApp.themeParams.button_color,
  buttonText: WebApp.themeParams.button_text_color,
};

// MainButton for primary actions
WebApp.MainButton.setParams({
  text: "Buyurtma berish",
  color: tgTheme.button,
  text_color: tgTheme.buttonText,
}).show().onClick(() => handleCheckout());

// BackButton
WebApp.BackButton.show().onClick(() => navigate(-1));

// Haptic feedback
WebApp.HapticFeedback.impactOccurred('light'); // on button tap
WebApp.HapticFeedback.notificationOccurred('success'); // on success

// Safe area (avoid notch / home indicator)
const safeAreaInset = {
  top: WebApp.safeAreaInset?.top ?? 0,
  bottom: WebApp.safeAreaInset?.bottom ?? 0,
};
```

## Common Mobile Pitfalls
```tsx
// ❌ Horizontal scroll killer — always add to root
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />

// ❌ Avoid fixed widths — use max-width + width:100%
// ❌ Avoid hover-only interactions (no hover on touch)
// ✅ Always provide tap/click alternative to hover states
// ✅ Use position: sticky not fixed for headers (avoids iOS bugs)
// ✅ Test at 320px width — the smallest common screen
```
