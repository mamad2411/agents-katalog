---
name: branded-ui
description: "Use when rendering or creating UI components with @repo/ui brand tokens, motion, or states."
---

# Branded Components & Motion System Guide

Authoritative usage guide for branded UI components and motion tokens exported from `@repo/ui`.

---

## 1. Motion System

Import motion tokens from `@repo/ui`:
```typescript
import { duration, easing, scale, color } from '@repo/ui';
```

- `duration`: Predefined animation durations (`micro`, `transition`, `breathe`, `meaningful`, `ceremony`)
- `easing`: Easing functions (`standard`, `decelerate`, `accelerate`)
- `scale`: Scale tokens (`enter`, `rest`, `breatheMin`, `breatheMax`)
- `color`: Brand and neutral color palettes

---

## 2. Core Branded Components

### BrandPulse
Replaces `ActivityIndicator` / `Spinner` for all loading states. Uses the brand mark with a breathing animation.
```typescript
import { BrandPulse } from '@repo/ui';

// Default size
<BrandPulse />

// Custom size and color
<BrandPulse size={28} tintColor="#D4843A" />
```

### BrandedErrorState
For error/offline states. Uses the brand mark in muted amber (caution color), static (no breathing — absence of the loop signals "paused").
```typescript
import { BrandedErrorState } from '@repo/ui';

<BrandedErrorState
  title="Connection lost"
  message="Please check your internet connection and try again"
>
  <Button onPress={retry}>Try again</Button>
</BrandedErrorState>
```

### Success Feedback Components
Two deliberate tiers of success feedback:
- `SuccessCheck`: For trivial actions (field saved, item checked). Fast, generic checkmark.
- `SuccessGlow`: For meaningful milestones (first connection, session booked). Branded heart with motes.

```typescript
import { SuccessCheck, SuccessGlow } from '@repo/ui';

// Trivial success
<SuccessCheck size={22} />

// Meaningful success
<SuccessGlow size={64} />
```

### BrandedEmptyState
For empty states. Uses the brand mark as an outline (not filled), signifying "hasn't bloomed yet."
```typescript
import { BrandedEmptyState } from '@repo/ui';

<BrandedEmptyState
  title="No items yet"
  message="Create your first item to get started"
  subtle={false} // Set to true for subtle breathing animation
>
  <Button onPress={create}>Create item</Button>
</BrandedEmptyState>
```

### Skeleton Loading Components
For content loading placeholders using responsive layouts:
```typescript
import { ShimmerBlock, BrandedSkeletonCard, BrandedSkeletonList } from '@repo/ui';

<ShimmerBlock width="70%" height={12} />
<BrandedSkeletonCard />
<BrandedSkeletonList count={6} />
```

---

## 3. Layout & Transitions

### Responsive Layout Utilities
```typescript
import { useBreakpoint, useResponsiveGrid } from '@repo/ui';

const breakpoint = useBreakpoint(); // 'phone' | 'tablet' | 'desktop'
const { columns, maxWidth } = useResponsiveGrid();
```

### Screen Transitions (Expo Router)
```typescript
import { softCrossfadeScale, sharedTransitionTiming } from '@repo/ui';

<Stack.Screen name="example" options={softCrossfadeScale} />
```

---

## 4. Backward Compatibility Rules
- The original `EmptyState` component is preserved with its original API (including `icon` and `description` props).
- New branded components are exported with `Branded` prefix to avoid breaking existing imports.
- Use branded versions for new screens; do not arbitrarily rewrite existing unbranded call sites without user approval.
