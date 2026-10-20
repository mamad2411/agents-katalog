---
name: "Mobile Gesture Handler"
version: "1.0.0"
description: "Handles touch gestures including swipe, pinch, long press, and drag. Provides unified gesture recognition across iOS and Android."
author: "workspace"
activated: false
---

# Mobile Gesture Handler

Handles touch gestures including swipe, pinch, long press, and drag. Provides unified gesture recognition across iOS and Android.

## Decision Framework

### When to Apply
Use when: Touch interactions, swipe navigation, drag-and-drop on mobile, pinch-to-zoom, mobile-specific UX

### When NOT to Apply
Don't use when: Desktop-only applications, simple tap interactions

## Anti-Patterns

### 1. Tiny Touch Targets
```css
/* BAD: 20px target */
.icon-button { width: 20px; height: 20px; }

/* GOOD: 44px minimum per Apple/Google guidelines */
.icon-button { width: 44px; height: 44px; min-width: 44px; min-height: 44px; }
```

### 2. No Gesture Feedback
Always provide visual feedback during gestures (swipe reveals, drag handles, etc.).


## Trigger Phrases

- "Touch gestures"
- "Swipe navigation"
- "Pinch to zoom"
- "Long press"
- "Mobile interactions"

## Patterns

### Swipe Detector
```javascript
function useSwipe(onSwipeLeft, onSwipeRight, threshold = 50) {
  const touchStart = useRef(null);
  
  const onTouchStart = (e) => { touchStart.current = e.touches[0].clientX; };
  const onTouchEnd = (e) => {
    if (!touchStart.current) return;
    const diff = touchStart.current - e.changedTouches[0].clientX;
    if (Math.abs(diff) > threshold) {
      diff > 0 ? onSwipeLeft?.() : onSwipeRight?.();
    }
    touchStart.current = null;
  };

  return { onTouchStart, onTouchEnd };
}
```

### Long Press
```javascript
function useLongPress(callback, delay = 500) {
  const timerRef = useRef(null);
  
  const start = () => { timerRef.current = setTimeout(callback, delay); };
  const cancel = () => clearTimeout(timerRef.current);
  
  return {
    onTouchStart: start, onTouchEnd: cancel, onTouchMove: cancel,
    onMouseDown: start, onMouseUp: cancel, onMouseLeave: cancel,
  };
}
```

## Integration
- Works with: accessibility-pattern-library, component-lifecycle-manager

