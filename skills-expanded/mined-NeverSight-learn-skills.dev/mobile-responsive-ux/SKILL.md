---
name: mobile-responsive-ux
description: Mobile UX patterns including touch targets, gestures, responsive design, and mobile-specific considerations
license: MIT
---

# Mobile & Responsive UX

## Touch Target Sizes

| Standard | Size | Notes |
|----------|------|-------|
| WCAG 2.2 AA | 24×24px | Absolute minimum |
| Apple HIG | 44×44px | Recommended minimum |
| Material Design | 48×48px | Recommended minimum |
| Comfortable | 48×48px+ | Best for accessibility |

### Spacing Between Targets
- Minimum: 8px between touch targets
- Recommended: 16px for comfortable tapping
- Critical actions: Extra spacing to prevent mis-taps

## Mobile Navigation Patterns

### Bottom Navigation (Recommended)
Best for: 3-5 primary destinations

**Guidelines:**
- Maximum 5 items
- Icon + text label for each
- Highlight active state clearly
- Most important items in thumb-reach zone

**Thumb Zone (Right-handed)**
```
┌─────────────────┐
│  Hard to reach  │
│                 │
│  Comfortable    │
│                 │
│  Easy to reach  │
└─────────────────┘
```

### Hamburger Menu
Best for: Secondary navigation, settings

**Guidelines:**
- Use clear ☰ icon or "Menu" label
- Full-screen overlay on mobile
- Easy close (X button + tap outside)
- Remember scroll position

### Tab Bar
Best for: Parallel content sections

**Guidelines:**
- Maximum 5 tabs
- Scrollable if more needed
- Clear active state
- Consider icons + text

## Gesture Patterns

| Gesture | Common Use | Consider |
|---------|------------|----------|
| Tap | Select, activate | Primary interaction |
| Long press | Context menu, select mode | Discoverable alternative needed |
| Swipe horizontal | Delete, archive, navigation | Provide visual hint |
| Swipe vertical | Refresh, dismiss, scroll | Pull-to-refresh standard |
| Pinch | Zoom in/out | Images, maps |
| Double tap | Zoom, like | Secondary action |
| Drag | Reorder, move | Provide handle affordance |

### Gesture Best Practices
- Always provide button alternative for gestures
- Add visual hints for available gestures
- Use standard platform conventions
- Provide haptic feedback when appropriate

## Responsive Design Checklist

### Content
- [ ] Text readable without zooming (16px+ base)
- [ ] Images scale appropriately
- [ ] No horizontal scrolling required
- [ ] Tables adapt or scroll horizontally
- [ ] Long words break appropriately

### Interaction
- [ ] Touch targets ≥44px
- [ ] Adequate spacing between targets
- [ ] Forms usable with on-screen keyboard
- [ ] Dropdowns have mobile-friendly alternatives
- [ ] Date pickers use native when possible

### Layout
- [ ] Single column on mobile
- [ ] Critical content above fold
- [ ] Navigation accessible
- [ ] Fixed headers not too tall
- [ ] Bottom nav in thumb zone

## Mobile-First CSS

```css
/* Base: Mobile styles */
.container {
  padding: 16px;
  font-size: 16px;
}

.grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Tablet: 768px+ */
@media (min-width: 768px) {
  .container {
    padding: 24px;
  }
  
  .grid {
    flex-direction: row;
    flex-wrap: wrap;
  }
  
  .grid-item {
    flex: 0 0 calc(50% - 8px);
  }
}

/* Desktop: 1024px+ */
@media (min-width: 1024px) {
  .container {
    padding: 32px;
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .grid-item {
    flex: 0 0 calc(33.333% - 11px);
  }
}
```

## Mobile Form UX

### Input Types
| Data | Input Type | Keyboard |
|------|------------|----------|
| Email | `type="email"` | @ and .com keys |
| Phone | `type="tel"` | Number pad |
| Number | `type="number"` | Number pad |
| URL | `type="url"` | .com and / keys |
| Search | `type="search"` | Search button |
| Date | `type="date"` | Date picker |

### Form Best Practices
- Use large touch targets for inputs
- Show inline validation
- Enable autocomplete (`autocomplete` attribute)
- Use appropriate `inputmode` for custom keyboards
- Avoid dropdowns when possible (use segmented controls)
- Group related fields
- Show keyboard-appropriate labels

### Keyboard Handling
```html
<input
  type="text"
  inputmode="numeric"
  pattern="[0-9]*"
  autocomplete="cc-number"
  enterkeyhint="next"
/>
```

## Safe Areas

Handle notches, home indicators, and rounded corners:

```css
.app-container {
  padding-top: env(safe-area-inset-top);
  padding-right: env(safe-area-inset-right);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
}

/* For fixed bottom navigation */
.bottom-nav {
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
}
```

## Mobile Performance UX

### Image Optimization
```html
<img
  src="image-800.jpg"
  srcset="
    image-400.jpg 400w,
    image-800.jpg 800w,
    image-1200.jpg 1200w
  "
  sizes="(max-width: 600px) 100vw, 50vw"
  loading="lazy"
  alt="Description"
/>
```

### Lazy Loading
- Images below fold: `loading="lazy"`
- Iframes: `loading="lazy"`
- Heavy components: Dynamic import with Suspense

### Perceived Performance
- Show skeleton screens immediately
- Progressive image loading (blur-up)
- Optimistic UI for common actions
- Prefetch likely next pages

## Offline & Slow Network

### Offline States
- Clear "offline" indicator
- Cache critical content
- Queue actions for sync
- Show last updated timestamp

### Slow Network Handling
- Skeleton screens
- Lower quality images first
- Retry failed requests
- Show progress for large uploads

## Mobile Testing Checklist

### Device Testing
- [ ] Test on actual devices (not just emulators)
- [ ] Test on different screen sizes
- [ ] Test in portrait and landscape
- [ ] Test with different text sizes (accessibility)
- [ ] Test with one-handed use

### Network Testing
- [ ] Test on slow 3G
- [ ] Test offline mode
- [ ] Test intermittent connection
- [ ] Test large file uploads

### Input Testing
- [ ] Test with on-screen keyboard
- [ ] Test keyboard dismissal
- [ ] Test with voice input
- [ ] Test copy/paste
