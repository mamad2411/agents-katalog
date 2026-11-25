---
name: timezone-seeding-day-of-week-bug
description: |
  Fix validation errors "Start time must be before end time" when seeding time-based
  data with timezone conversion. Use when: (1) Database seeding fails with time ordering
  validation errors despite correct local times, (2) Timezone conversion causes day-of-week
  changes that break time comparisons, (3) Early morning times (00:00-06:00) wrap to
  previous day after UTC conversion, (4) Seeding availability blocks, schedules, or
  recurring time-based data. Covers proper timezone conversion with day tracking and
  exclusive date ranges.
author: Claude Code
version: 1.0.0
date: 2026-02-05
---

# Timezone Seeding Day-of-Week Bug

## Problem

When seeding time-based database records with timezone conversion (e.g., availability
blocks, schedules, recurring events), validation errors like "Start time must be before
end time" occur even though the local times are correct. The root cause is that timezone
conversion can change the day-of-week, making the end time appear to come before the
start time when stored in UTC.

## Context / Trigger Conditions

**Symptoms:**
- Database seeding fails with validation error: "Start time must be before end time"
- Validation error: "Effective from must be before effective until"
- Local times are correct (e.g., 9:00 AM - 5:00 PM) but fail when converted to UTC
- Issue occurs primarily with early morning times (midnight to ~6 AM)
- Error appears in timezones with negative UTC offsets (e.g., America/Los_Angeles UTC-8)

**When this occurs:**
- Seeding availability blocks, schedules, or recurring events
- Converting local time to UTC for database storage
- Using date-fns-tz or similar timezone conversion libraries
- Time validation happens after conversion but before storage
- Day-of-week tracking is needed (e.g., "Monday 9:00 AM - 5:00 PM")

## Root Cause

Timezone conversion can shift times across day boundaries, changing the day-of-week:

**Example (London timezone, UTC+0):**
```typescript
// Monday 00:00 in Europe/London
fromZonedTime('2024-01-01T00:00:00', 'Europe/London')
// → 2024-01-01T00:00:00Z (still Monday, day 1)

// Monday 17:00 in Europe/London
fromZonedTime('2024-01-01T17:00:00', 'Europe/London')
// → 2024-01-01T17:00:00Z (still Monday, day 1)
```

**Example (Los Angeles timezone, UTC-8):**
```typescript
// Monday 00:00 in America/Los_Angeles
fromZonedTime('2024-01-01T00:00:00', 'America/Los_Angeles')
// → 2024-01-01T08:00:00Z (still Monday, day 1)

// Monday 01:00 in America/Los_Angeles
fromZonedTime('2024-01-01T01:00:00', 'America/Los_Angeles')
// → 2024-01-01T09:00:00Z (still Monday, day 1)
```

**The Problem:**
```typescript
// Naive conversion (WRONG)
const startTime = fromZonedTime('2024-01-01T00:00:00', 'America/Los_Angeles');
// → 2024-01-01T08:00:00Z (Monday in UTC)

const endTime = fromZonedTime('2024-01-01T17:00:00', 'America/Los_Angeles');
// → 2024-01-02T01:00:00Z (TUESDAY in UTC! ❌)

// Storing only time part:
startTime.toISOString() // "08:00:00Z" (Monday)
endTime.toISOString()   // "01:00:00Z" (Tuesday, but day lost!)

// Validation fails: 01:00 < 08:00 ❌
```

**What happens:**
1. Local Monday 5:00 PM (17:00) converts to Tuesday 1:00 AM UTC
2. Time portion extracted: "01:00:00Z"
3. Day-of-week changes from Monday (1) to Tuesday (2)
4. When comparing just times: 01:00 < 08:00, validation fails
5. Database schema expects times on SAME day-of-week

## Solution

### Fix 1: Track Day-of-Week During Conversion

Create a helper function that returns BOTH the converted time AND the day-of-week:

```typescript
import { fromZonedTime } from "date-fns-tz";
import { format } from "date-fns";

/**
 * Convert local time to UTC while tracking day-of-week changes
 *
 * @param dayOfWeek - Local day of week (0 = Sunday, 6 = Saturday)
 * @param time - Local time in HH:mm format
 * @param timezone - IANA timezone string
 * @returns Object with UTC day-of-week and time
 */
function availabilityTimeToUTC(
  dayOfWeek: number,
  time: string,
  timezone: string,
): { dayOfWeek: number; utcTime: Date } {
  // 1. Create reference date for the specified day-of-week
  const referenceDate = new Date("2024-01-01"); // Monday
  referenceDate.setDate(referenceDate.getDate() + dayOfWeek);

  // 2. Set the local time
  const [hours, minutes] = time.split(":").map(Number);
  referenceDate.setHours(hours, minutes, 0, 0);

  // 3. Convert to UTC (this may change the day)
  const utcDate = fromZonedTime(referenceDate, timezone);

  // 4. Return BOTH the new day-of-week and the time
  return {
    dayOfWeek: utcDate.getUTCDay(), // New day after conversion
    utcTime: new Date(`1970-01-01T${format(utcDate, "HH:mm")}:00Z`),
  };
}
```

**Usage in seeding:**

```typescript
// Before (WRONG - ignores day changes)
await db.availability.create({
  data: {
    userId: user.id,
    dayOfWeek: 1, // Monday
    startTime: fromZonedTime('2024-01-01T00:00:00', timezone),
    endTime: fromZonedTime('2024-01-01T17:00:00', timezone),
    // If timezone is UTC-8, endTime is now TUESDAY but dayOfWeek still says MONDAY
    timezone,
  },
});

// After (CORRECT - tracks day changes)
const start = availabilityTimeToUTC(1, "00:00", timezone);
const end = availabilityTimeToUTC(1, "17:00", timezone);

await db.availability.create({
  data: {
    userId: user.id,
    dayOfWeek: start.dayOfWeek, // Use converted day (may differ from input)
    startTime: start.utcTime,
    endTime: end.utcTime,
    timezone,
  },
});
```

### Fix 2: Use Exclusive End Dates for Date Ranges

For single-day events or blockouts, use exclusive end dates (next day) to avoid
validation errors:

```typescript
// Before (WRONG - same date fails validation)
await db.availability.create({
  data: {
    userId: user.id,
    status: "BUSY",
    effectiveFrom: new Date("2024-12-25"),
    effectiveUntil: new Date("2024-12-25"), // ❌ Same date, fails < check
  },
});

// After (CORRECT - exclusive end date)
const blockoutDate = new Date("2024-12-25");
const exclusiveEnd = new Date(blockoutDate);
exclusiveEnd.setDate(exclusiveEnd.getDate() + 1); // Next day

await db.availability.create({
  data: {
    userId: user.id,
    status: "BUSY",
    effectiveFrom: blockoutDate,
    effectiveUntil: exclusiveEnd, // ✅ 2024-12-26, passes < check
  },
});
```

## Verification

1. **Test with Multiple Timezones:**
   ```bash
   # Test with UTC+0 (no shift expected)
   TIMEZONE=Europe/London pnpm db:seed

   # Test with UTC-8 (shift expected for early/late times)
   TIMEZONE=America/Los_Angeles pnpm db:seed

   # Test with UTC+8 (opposite shift)
   TIMEZONE=Asia/Hong_Kong pnpm db:seed
   ```

2. **Verify Seeded Data:**
   ```typescript
   // Check that day-of-week matches the UTC times
   const blocks = await db.availability.findMany();

   for (const block of blocks) {
     const startDay = block.startTime.getUTCDay();
     const endDay = block.endTime.getUTCDay();

     console.log(`Block ${block.id}:`);
     console.log(`  Stored dayOfWeek: ${block.dayOfWeek}`);
     console.log(`  Start time day: ${startDay}`);
     console.log(`  End time day: ${endDay}`);
     console.log(`  Match: ${block.dayOfWeek === startDay && startDay === endDay}`);
   }
   ```

3. **Check Validation:**
   ```typescript
   // Verify start < end in all cases
   const invalidBlocks = await db.availability.findMany({
     where: {
       // This should return 0 results
       startTime: { gte: db.raw('end_time') },
     },
   });

   console.log(`Invalid blocks: ${invalidBlocks.length}`); // Should be 0
   ```

## Example

Real-world bug from RoadDux driving instructor platform seeding:

**Symptom:** Seeding failed with validation error for Emily Chen's availability.

**Error:**
```
ORMError: Invalid createMany args for model 'Availability':
  startTime: Start time must be before end time
```

**Root Cause:**
```typescript
// Seeding code (WRONG)
await db.availability.createMany({
  data: [
    {
      userId: emilyId,
      dayOfWeek: 1, // Monday
      startTime: fromZonedTime(
        new Date("2024-01-01T00:00:00"),
        "America/Los_Angeles"
      ), // → 2024-01-01T08:00:00Z (Monday)
      endTime: fromZonedTime(
        new Date("2024-01-01T17:00:00"),
        "America/Los_Angeles"
      ), // → 2024-01-02T01:00:00Z (TUESDAY! ❌)
      timezone: "America/Los_Angeles",
    },
  ],
});

// When extracting just time portion:
// startTime: "08:00:00" (Monday)
// endTime: "01:00:00" (Tuesday, but stored as Monday)
// Validation: 01:00 < 08:00 ❌ FAIL
```

**Fix:**
```typescript
// Helper function (CORRECT)
function availabilityTimeToUTC(
  dayOfWeek: number,
  time: string,
  timezone: string,
): { dayOfWeek: number; utcTime: Date } {
  const referenceDate = new Date("2024-01-01");
  referenceDate.setDate(referenceDate.getDate() + dayOfWeek);

  const [hours, minutes] = time.split(":").map(Number);
  referenceDate.setHours(hours, minutes, 0, 0);

  const utcDate = fromZonedTime(referenceDate, timezone);

  return {
    dayOfWeek: utcDate.getUTCDay(), // Track day change!
    utcTime: new Date(`1970-01-01T${format(utcDate, "HH:mm")}:00Z`),
  };
}

// Seeding code (CORRECT)
const start = availabilityTimeToUTC(1, "00:00", "America/Los_Angeles");
const end = availabilityTimeToUTC(1, "17:00", "America/Los_Angeles");

await db.availability.createMany({
  data: [
    {
      userId: emilyId,
      dayOfWeek: start.dayOfWeek, // Use converted day
      startTime: start.utcTime,
      endTime: end.utcTime,
      timezone: "America/Los_Angeles",
    },
  ],
});
```

**Result:** Seeding succeeds, times validate correctly across all timezones.

## Notes

### When This Pattern is Needed

This pattern is essential for:
- **Weekly schedules** stored in UTC (e.g., "Every Monday 9-5")
- **Recurring events** with timezone support
- **Availability blocks** for booking systems
- **Business hours** with multi-timezone support
- **Appointment scheduling** systems

### When to Use Exclusive End Dates

Use exclusive end dates (next day) for:
- Single-day events or blockouts
- Date ranges where start = end doesn't make semantic sense
- Schemas with `effectiveFrom < effectiveUntil` constraints
- Calendar events with "all day" semantics

### Timezone Best Practices

1. **Always store times in UTC** in the database
2. **Track day-of-week in UTC** if using recurring schedules
3. **Convert at display time** to user's local timezone
4. **Use IANA timezone identifiers** (e.g., "America/Los_Angeles", not "PST")
5. **Test with multiple timezones** including negative offsets
6. **Document timezone assumptions** in schema comments

### Common Pitfalls

1. **Extracting only time portion without day:** Loses day-of-week information
2. **Hardcoding day-of-week:** Ignores timezone conversion effects
3. **Using inclusive end dates:** Fails validation when start = end
4. **Not testing negative UTC offsets:** Most bugs appear in UTC-X timezones
5. **Assuming same day after conversion:** Early/late times often shift days

### Database Schema Considerations

If your schema stores times without dates (time-of-day format), ensure:
- Day-of-week field matches the UTC day, not local day
- Validation constraints account for timezone shifts
- Documentation explains the UTC storage pattern
- Example data includes cross-timezone test cases

## References

- [date-fns-tz Documentation](https://github.com/marnusw/date-fns-tz)
- [IANA Time Zone Database](https://www.iana.org/time-zones)
- [Timezone Best Practices - AWS](https://aws.amazon.com/blogs/infrastructure-and-automation/managing-timezone-complexity-in-global-applications/)
- [Storing Time-of-Day in PostgreSQL](https://www.postgresql.org/docs/current/datatype-datetime.html)
