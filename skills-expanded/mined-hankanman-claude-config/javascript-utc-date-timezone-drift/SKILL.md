---
name: javascript-utc-date-timezone-drift
description: |
  Fix timezone drift when using JavaScript Date methods with UTC-stored times. Use when: (1) Times shift by user's timezone offset (e.g., 09:00 UTC becomes 10:00 in BST browsers), (2) Database stores times in UTC but display shows wrong hours, (3) Inconsistent time behavior across users in different timezones, (4) Using getHours/getMinutes/setHours with Date objects that should stay in UTC. Replace local time getters/setters with UTC variants to prevent automatic timezone conversion.
author: Claude Code
version: 1.0.0
date: 2026-02-06
---

# JavaScript UTC Date Timezone Drift Fix

## Problem

When working with JavaScript Date objects that represent UTC times (e.g., from a database or API), using local time methods like `getHours()`, `getMinutes()`, or `setHours()` causes **timezone drift**. The browser automatically applies the user's local timezone offset, causing times to shift unexpectedly.

This creates silent bugs where:
- 09:00 UTC appears as 10:00 for users in BST (UTC+1)
- 09:00 UTC appears as 01:00 for users in PST (UTC-8)
- Times work correctly for developers in UTC but fail in production for global users

## Context / Trigger Conditions

**Use this skill when you see:**

1. **Time shift by timezone offset**: A time stored as 09:00 UTC displays as 10:00, 01:00, or another value depending on user location

2. **Inconsistent behavior across timezones**: Times appear correct for some users but wrong for others

3. **Database times don't match display**: Your database stores `2026-01-01T09:00:00Z` but the UI shows different hours

4. **Working with UTC-stored times**: You're using `Date` objects created from ISO 8601 strings with `Z` suffix or from database timestamps stored in UTC

5. **Code uses local getters/setters**:
   ```typescript
   date.getHours()      // ❌ Returns local hour
   date.setHours(h)     // ❌ Sets local hour
   date.getMinutes()    // ❌ Returns local minute
   date.setMinutes(m)   // ❌ Sets local minute
   ```

**Error symptoms:**
- Times appear shifted by 1-14 hours depending on user location
- No JavaScript errors thrown (silent bug)
- Works correctly in development (UTC timezone) but fails in production
- Different behavior for users in different countries

## Solution

### Step 1: Identify UTC Date Objects

First, confirm you're working with UTC times:

```typescript
// These are UTC dates (should use UTC methods):
const utcDate = new Date("2026-01-01T09:00:00Z");       // ISO string with Z
const fromDB = new Date(dbTimestamp);                    // Database UTC timestamp
const fromAPI = new Date(apiResponse.startTime);         // API UTC timestamp

// These are local dates (local methods OK):
const localDate = new Date(2026, 0, 1, 9, 0);          // Local constructor
const userInput = new Date(datePickerValue);            // User-selected local time
```

### Step 2: Replace Local Methods with UTC Variants

**Reading time components:**

```typescript
// ❌ WRONG: Local getters apply timezone offset
const hours = date.getHours();       // 09:00 UTC → 10:00 in BST browser
const minutes = date.getMinutes();   // Returns local minutes

// ✅ CORRECT: UTC getters preserve UTC time
const hours = date.getUTCHours();    // Always returns UTC hours
const minutes = date.getUTCMinutes(); // Always returns UTC minutes
```

**Setting time components:**

```typescript
// ❌ WRONG: Local setters apply timezone offset
const newDate = new Date(date);
newDate.setHours(hours, minutes);     // Sets local time, then converts to UTC
// If user is in BST: setHours(9, 0) → 09:00 BST → 08:00 UTC

// ✅ CORRECT: UTC setters work directly in UTC
const newDate = new Date(date);
newDate.setUTCHours(hours, minutes);  // Sets UTC time directly
// Regardless of timezone: setUTCHours(9, 0) → 09:00 UTC
```

### Step 3: Complete Method Mapping

| ❌ Local Method | ✅ UTC Equivalent | Purpose |
|----------------|-------------------|---------|
| `getHours()` | `getUTCHours()` | Get hour (0-23) |
| `getMinutes()` | `getUTCMinutes()` | Get minute (0-59) |
| `getSeconds()` | `getUTCSeconds()` | Get second (0-59) |
| `getMilliseconds()` | `getUTCMilliseconds()` | Get millisecond (0-999) |
| `getDay()` | `getUTCDay()` | Get day of week (0-6) |
| `getDate()` | `getUTCDate()` | Get day of month (1-31) |
| `getMonth()` | `getUTCMonth()` | Get month (0-11) |
| `getFullYear()` | `getUTCFullYear()` | Get year |
| `setHours(h, m, s, ms)` | `setUTCHours(h, m, s, ms)` | Set time components |
| `setMinutes(m, s, ms)` | `setUTCMinutes(m, s, ms)` | Set minute and smaller |
| `setSeconds(s, ms)` | `setUTCSeconds(s, ms)` | Set second and smaller |
| `setDate(d)` | `setUTCDate(d)` | Set day of month |
| `setMonth(m, d)` | `setUTCMonth(m, d)` | Set month and day |
| `setFullYear(y, m, d)` | `setUTCFullYear(y, m, d)` | Set year, month, day |

### Step 4: Real-World Example

**Before (buggy code with timezone drift):**

```typescript
// Expand weekly availability to specific dates
function expandAvailability(availability, startDate, endDate) {
  const instances = [];
  let currentDate = new Date(startDate);

  while (currentDate <= endDate) {
    if (currentDate.getDay() === availability.dayOfWeek) {
      const instanceStart = new Date(currentDate);
      // ❌ BUG: Using local getters/setters
      instanceStart.setHours(
        availability.startTime.getHours(),      // Returns local hour!
        availability.startTime.getMinutes()     // Returns local minute!
      );
      // For BST user: 09:00 UTC becomes 10:00 BST, then treated as 10:00 UTC

      instances.push(instanceStart);
    }
    currentDate.setDate(currentDate.getDate() + 1);
  }

  return instances;
}

// Result: Times shift by timezone offset (1 hour in BST, 8 hours in PST, etc.)
```

**After (fixed with UTC methods):**

```typescript
// Expand weekly availability to specific dates
function expandAvailability(availability, startDate, endDate) {
  const instances = [];
  let currentDate = new Date(startDate);

  while (currentDate <= endDate) {
    if (currentDate.getUTCDay() === availability.dayOfWeek) {
      const instanceStart = new Date(currentDate);
      // ✅ FIXED: Using UTC getters/setters
      instanceStart.setUTCHours(
        availability.startTime.getUTCHours(),   // Returns UTC hour
        availability.startTime.getUTCMinutes()  // Returns UTC minute
      );
      // Always works in UTC: 09:00 UTC stays 09:00 UTC

      instances.push(instanceStart);
    }
    currentDate.setUTCDate(currentDate.getUTCDate() + 1);
  }

  return instances;
}

// Result: Times stay in UTC regardless of user's timezone
```

## Verification

After applying the fix:

1. ✅ **Test in multiple timezones**: Change your system timezone and verify times don't shift
2. ✅ **Check database roundtrip**: Save a time, reload, verify it matches
3. ✅ **Compare UTC strings**: Use `.toISOString()` to verify times are identical
4. ✅ **Test edge cases**: Midnight (00:00), noon (12:00), end of day (23:59)

**Test script:**

```typescript
// Save this as test-timezone-drift.ts
const utcTime = new Date("2026-01-01T09:00:00Z");

console.log("Original UTC time:", utcTime.toISOString());
// Should print: 2026-01-01T09:00:00.000Z

// Wrong: Local methods (will vary by timezone)
const localHours = utcTime.getHours();
console.log("Local getHours():", localHours);
// BST user sees: 10 (wrong!)
// PST user sees: 1 (wrong!)

// Correct: UTC methods (consistent everywhere)
const utcHours = utcTime.getUTCHours();
console.log("UTC getUTCHours():", utcHours);
// All users see: 9 (correct!)

// Reconstruct time using local methods (buggy)
const buggyDate = new Date("2026-02-01");
buggyDate.setHours(utcTime.getHours(), utcTime.getMinutes());
console.log("Buggy reconstruction:", buggyDate.toISOString());
// BST user sees: 2026-02-01T09:00:00.000Z (should be 08:00 - 1 hour drift!)

// Reconstruct time using UTC methods (correct)
const fixedDate = new Date("2026-02-01");
fixedDate.setUTCHours(utcTime.getUTCHours(), utcTime.getUTCMinutes());
console.log("Fixed reconstruction:", fixedDate.toISOString());
// All users see: 2026-02-01T09:00:00.000Z (correct!)
```

## Example: Complete Pattern

```typescript
interface AvailabilityBlock {
  id: string;
  dayOfWeek: number;        // 0-6 (Sunday-Saturday)
  startTime: Date;          // UTC time of day
  endTime: Date;            // UTC time of day
  effectiveFrom: Date;
  effectiveUntil: Date | null;
}

/**
 * Generate specific date instances from a recurring availability block
 * Uses UTC methods to prevent timezone drift
 */
function generateInstances(
  availability: AvailabilityBlock,
  startDate: Date,
  endDate: Date
): Array<{ start: Date; end: Date }> {
  const instances = [];
  let currentDate = new Date(startDate);
  const effectiveEnd = availability.effectiveUntil || endDate;

  while (currentDate <= endDate && currentDate <= effectiveEnd) {
    // ✅ Use getUTCDay() for day of week
    if (
      currentDate.getUTCDay() === availability.dayOfWeek &&
      currentDate >= availability.effectiveFrom
    ) {
      // ✅ Use setUTCHours() and getUTCHours() to preserve UTC times
      const instanceStart = new Date(currentDate);
      instanceStart.setUTCHours(
        availability.startTime.getUTCHours(),
        availability.startTime.getUTCMinutes(),
        0,
        0
      );

      const instanceEnd = new Date(currentDate);
      instanceEnd.setUTCHours(
        availability.endTime.getUTCHours(),
        availability.endTime.getUTCMinutes(),
        0,
        0
      );

      instances.push({
        start: instanceStart,
        end: instanceEnd,
      });
    }

    // ✅ Use setUTCDate() and getUTCDate() for date arithmetic
    currentDate.setUTCDate(currentDate.getUTCDate() + 1);
  }

  return instances;
}
```

## Notes

### When to Use Local Methods

Local methods are appropriate when working with **user-local times**:

```typescript
// User picks "9:00 AM" in their local timezone
const userInput = datePicker.value;  // Local date
const hours = userInput.getHours();  // ✅ OK: User expects local time
```

### When to Use UTC Methods

UTC methods are required when working with **stored UTC times**:

```typescript
// Database stores UTC timestamp
const dbTime = new Date(dbRow.start_time);  // UTC date
const hours = dbTime.getUTCHours();         // ✅ REQUIRED: Preserve UTC
```

### Timezone Library Alternatives

For complex timezone handling, consider libraries:

- **date-fns-tz**: Timezone-aware date utilities
- **luxon**: Immutable date library with timezone support
- **dayjs** with timezone plugin: Lightweight alternative

However, for simple UTC time preservation, **native UTC methods are sufficient and preferred** (no dependencies, better performance).

### Common Pitfall: Date Constructor

The `Date()` constructor itself can cause confusion:

```typescript
// ❌ Local date (uses system timezone)
new Date(2026, 0, 1, 9, 0)  // 09:00 local time

// ✅ UTC date (explicit UTC)
new Date("2026-01-01T09:00:00Z")  // 09:00 UTC

// ✅ UTC date (from timestamp)
new Date(Date.UTC(2026, 0, 1, 9, 0))  // 09:00 UTC
```

### TypeScript Type Safety

Consider creating wrapper types to enforce UTC handling:

```typescript
type UTCDate = Date & { __brand: "UTC" };

function toUTC(date: Date): UTCDate {
  return date as UTCDate;
}

function getUTCHoursSafe(date: UTCDate): number {
  return date.getUTCHours();  // TypeScript reminds you to use UTC methods
}
```

## References

- [MDN: Date.prototype.getUTCHours()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getUTCHours)
- [MDN: Date.prototype.setUTCHours()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/setUTCHours)
- [MDN: Working with dates and times](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date#working_with_dates_and_times)
- [Stack Overflow: Why does JavaScript's Date() object use local time?](https://stackoverflow.com/questions/15141762/why-does-javascripts-date-object-use-local-time)
