---
name: ui-test-ux-quality
description: "Quality-beyond-correctness E2E testing patterns. Catches visual glitches, performance issues, layout shifts, and intermediate bad states. Triggers on: flicker test, visual stability, performance budget, negative assertion, CLS test, drag drop test, animation test."
---

# Quality-Beyond-Correctness E2E Testing

Test that features work correctly AND feel right. Catch issues that "technically work" but provide a broken user experience.

---

## The Problem

Standard E2E tests verify final state correctness:

```typescript
// This passes even if the UI flickered, jumped, or showed wrong states during drag
await page.dragAndDrop('.event', '.time-slot');
await expect(page.locator('.time-slot .event')).toBeVisible(); // Final state is correct
```

But users experience the **entire operation**, not just the end result. A drag-drop that briefly shows the event in the wrong location before correcting is broken, even if the final state is correct.

---

## The Patterns

### 1. Negative Assertions During Actions

Assert that bad states **never appear** during an operation:

```typescript
import { assertNeverAppears } from './ui-test-ux-quality-helpers';

test('drag to time slot never shows event in All Day row', async ({ page }) => {
  // Start monitoring for the bad state BEFORE the action
  const neverAllDay = assertNeverAppears(
    page,
    '.all-day-row .event[data-id="123"]',
    'Event should never appear in All Day row during time slot drag'
  );

  // Perform the drag operation
  await page.dragAndDrop('.event[data-id="123"]', '.time-slot-9am');

  // Stop monitoring and verify no violations occurred
  await neverAllDay.verify();

  // Also verify correct final state
  await expect(page.locator('.time-slot-9am .event[data-id="123"]')).toBeVisible();
});
```

### 2. Performance Budgets

Fail tests when operations exceed acceptable durations:

```typescript
import { withPerformanceBudget } from './ui-test-ux-quality-helpers';

test('event modal opens within performance budget', async ({ page }) => {
  await withPerformanceBudget(page, {
    operation: 'open event modal',
    budget: 150, // milliseconds
    action: async () => {
      await page.click('.event[data-id="123"]');
      await expect(page.locator('[role="dialog"]')).toBeVisible();
    },
  });
});

test('drag-drop completes render quickly', async ({ page }) => {
  await withPerformanceBudget(page, {
    operation: 'drag-drop render',
    budget: 100,
    action: async () => {
      await page.dragAndDrop('.event', '.time-slot');
      await expect(page.locator('.time-slot .event')).toBeVisible();
    },
  });
});
```

### 3. Visual Stability (No Layout Shift)

Detect elements that jump or shift during operations:

```typescript
import { assertNoLayoutShift } from './ui-test-ux-quality-helpers';

test('calendar does not shift when loading events', async ({ page }) => {
  // Monitor specific element(s) for position changes
  const stable = assertNoLayoutShift(page, {
    selector: '.calendar-grid',
    threshold: 2, // Allow up to 2px movement (for subpixel rendering)
  });

  await page.goto('/calendar');
  await page.waitForSelector('.event'); // Wait for events to load

  await stable.verify();
});

test('sidebar toggle does not cause content jump', async ({ page }) => {
  const stable = assertNoLayoutShift(page, {
    selector: '.main-content',
    threshold: 0, // No movement allowed
  });

  await page.click('[data-testid="sidebar-toggle"]');
  await page.waitForTimeout(300); // Wait for animation

  await stable.verify();
});
```

### 4. Render Stability (No Flicker)

Ensure elements don't appear/disappear/reappear during operations:

```typescript
import { assertStableRender } from './ui-test-ux-quality-helpers';

test('event list does not flicker during filter', async ({ page }) => {
  // Counts mount/unmount cycles for matching elements
  const stable = assertStableRender(page, {
    selector: '.event-card',
    maxMountCycles: 1, // Should only mount once, never unmount and remount
  });

  await page.fill('[data-testid="search"]', 'meeting');
  await page.waitForTimeout(500); // Debounce + render time

  await stable.verify();
});
```

### 5. CLS (Cumulative Layout Shift) Measurement

Use the browser's Layout Instability API:

```typescript
import { measureCLS } from './ui-test-ux-quality-helpers';

test('page load has acceptable CLS', async ({ page }) => {
  const cls = await measureCLS(page, async () => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000); // Allow late-loading content
  });

  expect(cls).toBeLessThan(0.1); // Good CLS score per Web Vitals
});
```

---

## Helper Implementation

Copy the helpers file to your project's e2e directory:

```
templates/ui-test-ux-quality-helpers.ts → your-project/e2e/helpers/ui-test-ux-quality-helpers.ts
```

Or import key patterns directly into test files.

---

## When to Use Each Pattern

| Scenario | Pattern |
|----------|---------|
| Drag-and-drop operations | `assertNeverAppears` + `withPerformanceBudget` |
| Modal/dialog opening | `withPerformanceBudget` |
| Page load/navigation | `measureCLS` + `assertNoLayoutShift` |
| Data loading | `assertStableRender` (no flicker) |
| Animations | `assertNoLayoutShift` with appropriate threshold |
| Timing/category changes | `expectMutualExclusivity` (element in one location) |
| Tab panels, wizards | `expectMutualExclusivity` |
| Any interactive feature | Combine patterns as needed |

---

## Integration with Test Structure

Use Playwright's test fixtures to make helpers available:

```typescript
// e2e/fixtures.ts
import { test as base } from '@playwright/test';
import * as quality from './helpers/ui-test-ux-quality-helpers';

export const test = base.extend<{ quality: typeof quality }>({
  quality: async ({}, use) => {
    await use(quality);
  },
});

// In tests:
test('feature works correctly', async ({ page, quality }) => {
  const neverBad = quality.assertNeverAppears(page, '.error-state');
  // ... test logic
  await neverBad.verify();
});
```

---

## Debugging Failures

When a quality assertion fails:

1. **Negative assertion failed**: The bad state appeared during the operation
   - Check render order in React components
   - Look for optimistic updates that show wrong state
   - Verify CSS transitions aren't revealing intermediate states

2. **Performance budget exceeded**: Operation took too long
   - Profile with browser DevTools
   - Check for excessive re-renders
   - Look for synchronous work blocking the main thread

3. **Layout shift detected**: Element moved unexpectedly
   - Check for late-loading content pushing things around
   - Verify CSS doesn't depend on content size
   - Use skeleton loaders with fixed dimensions

4. **Render stability failed**: Element mounted multiple times
   - Check for key prop issues in React lists
   - Look for state changes causing unmount/remount
   - Verify Suspense boundaries aren't flashing

---

## Best Practices

1. **Test the operation, not just the result** — Most bugs happen during transitions
2. **Set realistic budgets** — 100-200ms for UI operations, <0.1 CLS for page loads
3. **Combine patterns** — A single feature may need multiple quality checks
4. **Use thresholds wisely** — Allow for subpixel rendering (1-2px) but be strict on logic
5. **Test both happy path AND edge cases** — Slow networks, large datasets, rapid interactions

---

## Site-Level UX Coherence Audit

Use this section when validating full-site quality after UI/content changes.

### Scope and Viewports

- Audit all changed routes plus core nav-entry pages (home, primary docs/support, key feature pages)
- Check each page at desktop and at least one narrow mobile viewport

### Browser/Device Coverage Alignment

When Builder/test-flow runtime preferences request expanded coverage:

- `all-major` browser scope: run quality checks across Chromium, Firefox, and WebKit
- `desktop+mobile` device scope: include at least one mobile profile in addition to desktop

When defaults are selected (`chromium-only`, `desktop-only`), keep this skill fast and focused.

### Cross-Page Checks

1. Diagram and flow coherence
   - Directionality is explicit (no ambiguous connectors)
   - Actor labels and sequence steps are readable and consistent

2. Navigation behavior
   - Mobile hamburger menu opens/closes cleanly
   - Overlay/backdrop layering does not trap or block interactions
   - Links remain discoverable and usable on touch devices

3. Code-block usability
   - Copy controls are visible and tappable on mobile
   - Code content wraps/scrolls without clipping

4. Short-page spacing consistency
   - Avoid large dead zones on sparse detail pages
   - Preserve intentional visual rhythm across breakpoints

### Findings Format (Required)

Group findings by severity: `critical`, `high`, `medium`, `low`.
For each finding include:
- page URL/path
- user impact
- recommended fix
- artifact reference (screenshot path) when available

### Post-Fix Re-Verification

After fixes, run a targeted second pass on affected pages only:
- Re-check the same viewport(s) and interactions
- Mark each finding as resolved or still failing
- Do not sign off while unresolved critical findings remain

### Temporary Artifact Hygiene

For screenshot/script capture during audits:
- Use project-local `.tmp/visual-audit/` (or similar `.tmp/` path)
- Avoid leaving temporary JS capture files in tracked source/test directories

---

## 6. State Stability After Mutations

Verify that state changes persist and don't get overwritten by competing renders (cache invalidation, refetch, realtime subscriptions).

**The Problem:** Optimistic updates make initial assertions pass, but competing render mechanisms can overwrite state milliseconds later. Tests complete before the second render happens.

```typescript
// This passes even when the event jumps to wrong location after 500ms:
await page.selectOption('[data-testid="timing"]', 'slot-am');
await page.click('[data-testid="save"]');
await expect(page.locator('.slot-row-am .event')).toBeVisible(); // ✅ Passes (optimistic)
// ...but 500ms later, cache invalidation moves it to timed area
```

**The Solution:** Use `expect.poll()` to verify state remains stable over time:

```typescript
import { expect, test } from '@playwright/test';

test('event timing change persists after save', async ({ page }) => {
  // Make the change
  await page.selectOption('[data-testid="timing-select"]', 'slot-am');
  await page.click('[data-testid="save"]');
  
  // Wait for initial render
  const eventInSlot = page.locator('.slot-row-am .event[data-id="123"]');
  await expect(eventInSlot).toBeVisible();
  
  // Assert state remains stable for 2 seconds (catches competing render bugs)
  // Poll every 100ms, fail if element ever becomes invisible
  await expect.poll(
    async () => await eventInSlot.isVisible(),
    {
      message: 'Event should remain in slot row after save (competing render bug detected)',
      timeout: 2000,
      intervals: [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    }
  ).toBe(true);
  
  // Verify persistence after refresh (catches optimistic-only bugs)
  await page.reload();
  await expect(eventInSlot).toBeVisible();
});
```

**When to use:** ANY test involving create, update, or delete operations where:
- React Query, SWR, or similar caching libraries are used
- Realtime subscriptions (WebSocket, SSE) might push updates
- Multiple components render the same data
- Drag-and-drop or reordering operations

### Using the assertStateStability Helper

For cleaner test code, use the helper from `templates/ui-test-ux-quality-helpers.ts`:

```typescript
import { assertStateStability } from './helpers/ui-test-ux-quality-helpers';

test('event timing change persists after save', async ({ page }) => {
  await page.selectOption('[data-testid="timing-select"]', 'slot-am');
  await page.click('[data-testid="save"]');
  
  const eventInSlot = page.locator('.slot-row-am .event[data-id="123"]');
  await expect(eventInSlot).toBeVisible();
  
  // Assert stability for 2 seconds
  await assertStateStability(page, {
    locator: eventInSlot,
    duration: 2000,
    expectVisible: true,
    errorContext: 'Event should remain in slot row after save',
  });
  
  // Verify persistence
  await page.reload();
  await expect(eventInSlot).toBeVisible();
});
```

### Difference from assertStableRender

| Pattern | What it catches | When to use |
|---------|-----------------|-------------|
| `assertStableRender` | Flicker during operations (mount/unmount cycles) | Page loads, filter changes, search |
| `assertStateStability` | State overwritten AFTER operation completes | Mutations (create/update/delete) |

Use **both** when testing mutations that might also cause flicker:

```typescript
// Monitor for flicker during save
const noFlicker = assertStableRender(page, { selector: '.event-list', maxMountCycles: 1 });

await page.click('[data-testid="save"]');
await expect(eventInSlot).toBeVisible();

// Verify no flicker occurred
await noFlicker.verify();

// Then verify state remains stable
await assertStateStability(page, { locator: eventInSlot, duration: 2000, expectVisible: true });
```

---

## 7. Mutual Exclusivity Testing

Assert that an element appears in **exactly one** location — catching bugs where elements render in multiple places due to competing render mechanisms.

**The Problem:** Standard E2E tests only verify positive assertions ("is element visible in expected location?"). They pass even when the element ALSO appears in other locations:

```typescript
// This passes even when the event appears in BOTH locations:
await page.click('[data-testid="save"]');
await expect(page.locator('.timed-area .event')).toBeVisible(); // ✅ Passes
// ...but event is also visible in .all-day-row (bug!)
```

**The Solution:** Define all possible locations, then assert the element is in exactly one:

```typescript
import { expectMutualExclusivity, snapshotElementLocations } from './helpers/ui-test-ux-quality-helpers';

test('event appears in exactly one location after timing change', async ({ page }) => {
  // Define all possible locations for this element
  const eventLocator = page.locator('.event[data-id="123"]');
  const locations = [
    { name: 'All Day Row', locator: page.locator('.all-day-row').locator(eventLocator) },
    { name: 'Timed Area', locator: page.locator('.timed-area').locator(eventLocator) },
    { name: 'Slot Row', locator: page.locator('.slot-row').locator(eventLocator) },
  ];

  // Change event to timed
  await page.selectOption('[data-testid="timing"]', 'timed');
  await page.click('[data-testid="save"]');

  // Assert element is in Timed Area and NOT in other locations
  await expectMutualExclusivity(page, {
    elementDescription: 'Event after timing change',
    expectedLocation: locations[1], // Timed Area
    forbiddenLocations: [locations[0], locations[2]], // All Day Row, Slot Row
    duration: 2000, // Monitor for 2 seconds to catch delayed bugs
  });
});
```

### Debugging with snapshotElementLocations

When a test fails, use `snapshotElementLocations` to see where the element actually is:

```typescript
test.only('debug: where is the event?', async ({ page }) => {
  // ... perform the operation
  
  const result = await snapshotElementLocations(page, {
    elementDescription: 'Event 123',
    locations: [
      { name: 'All Day Row', locator: page.locator('.all-day-row .event[data-id="123"]') },
      { name: 'Timed Area', locator: page.locator('.timed-area .event[data-id="123"]') },
      { name: 'Slot Row', locator: page.locator('.slot-row .event[data-id="123"]') },
    ],
  });
  
  console.log('Element found in:', result.locations);
  // Output: Element found in: ['Timed Area', 'All Day Row']  // Bug! Should only be one
  console.log('Details:', result.details);
  // Output: { 'All Day Row': true, 'Timed Area': true, 'Slot Row': false }
});
```

### When to Use Mutual Exclusivity Testing

| Scenario | Why |
|----------|-----|
| Calendar events (all-day vs timed vs slot) | Events can only be in one time category |
| Tab panels | Only one panel should be visible at a time |
| Modal/dialog states | A modal is either open or closed, not both |
| Navigation states | Active nav item should only highlight one link |
| Wizard steps | Only one step should be visible at a time |
| Drag-and-drop | Item should only be in source OR destination |

### Using assertMutualExclusivity (Instant Check)

For quick assertions without monitoring duration:

```typescript
import { assertMutualExclusivity } from './helpers/ui-test-ux-quality-helpers';

// Instant check - no duration monitoring
await assertMutualExclusivity(page, {
  elementDescription: 'Event 123',
  expectedLocation: { name: 'Timed Area', locator: timedAreaEvent },
  forbiddenLocations: [
    { name: 'All Day Row', locator: allDayEvent },
    { name: 'Slot Row', locator: slotEvent },
  ],
});
```

### Combining with State Stability

For mutations, combine mutual exclusivity with state stability to catch both immediate duplicates AND delayed bugs:

```typescript
test('event timing change is correct and stable', async ({ page }) => {
  await page.selectOption('[data-testid="timing"]', 'timed');
  await page.click('[data-testid="save"]');

  // First, verify mutual exclusivity over time (catches duplicates AND delayed bugs)
  await expectMutualExclusivity(page, {
    elementDescription: 'Event after timing change',
    expectedLocation: { name: 'Timed Area', locator: timedAreaEvent },
    forbiddenLocations: [
      { name: 'All Day Row', locator: allDayEvent },
      { name: 'Slot Row', locator: slotEvent },
    ],
    duration: 2000,
  });

  // Then verify persistence after refresh
  await page.reload();
  await assertMutualExclusivity(page, {
    elementDescription: 'Event after reload',
    expectedLocation: { name: 'Timed Area', locator: timedAreaEvent },
    forbiddenLocations: [
      { name: 'All Day Row', locator: allDayEvent },
      { name: 'Slot Row', locator: slotEvent },
    ],
  });
});
```

### Difference from Other Patterns

| Pattern | What it catches | When to use |
|---------|-----------------|-------------|
| `assertNeverAppears` | Bad state appears during operation | Drag-drop, transitions |
| `assertStateStability` | State disappears after operation | After mutations |
| `expectMutualExclusivity` | Element in multiple locations | Timing changes, routing, tabs |

Use **mutual exclusivity** when the element should always exist somewhere, but only in ONE place.
