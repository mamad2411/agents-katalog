---
name: react-big-calendar-recurring-oneoff-events
description: |
  Properly render both recurring and one-off events in react-big-calendar with date constraints. Use when: (1) One-off events appear every week instead of just their specific date, (2) Recurring events don't respect effectiveFrom/effectiveUntil date ranges, (3) Calendar only shows current week instead of entire view range, (4) Need to generate events dynamically based on recurrence pattern and view range. Solves event generation for calendars with mixed recurring/one-off availability blocks.
author: Claude Code
version: 1.0.0
date: 2026-02-06
---

# react-big-calendar: Recurring vs One-Off Event Rendering

## Problem

react-big-calendar requires pre-generated event objects with specific `start` and `end` Date instances. When your data includes both recurring events (e.g., "every Monday 9-5") and one-off events (e.g., "January 15, 2026 only"), a naive "anchor to current week" approach causes one-off events to appear every week instead of just their specific date.

Additionally, recurring events may have date constraints (`effectiveFrom`/`effectiveUntil`) that aren't respected, causing them to appear before they start or after they end.

## Context / Trigger Conditions

**Use this skill when:**

1. **One-off events repeat incorrectly**: An event with `effectiveFrom: 2026-02-15` and `effectiveUntil: 2026-02-15` appears on Feb 15, Feb 22, Feb 29, etc. (every week)

2. **Recurring events ignore date ranges**: A recurring Monday event with `effectiveFrom: 2026-03-01` appears on Mondays in February

3. **View range issues**: Calendar only shows events for the current week, even in month view

4. **Data structure**: Your backend stores events with:
   - `dayOfWeek` (0-6, Sunday-Saturday)
   - `startTime`/`endTime` (time of day)
   - `effectiveFrom` (start date)
   - `effectiveUntil` (end date, or `null` for ongoing recurring)

**Error symptoms:**
- Events appearing on wrong dates
- One-off events duplicating every week
- Empty calendar in month view despite data existing
- Recurring events appearing before/after their effective range

## Solution

### Step 1: Calculate View Range

First, determine what date range the calendar is currently displaying based on view type:

```typescript
import {
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  startOfDay,
  endOfDay,
} from "date-fns";

let viewStart: Date;
let viewEnd: Date;

switch (view) {
  case "month":
    viewStart = startOfMonth(date);
    viewEnd = endOfMonth(date);
    break;
  case "week":
    viewStart = startOfWeek(date);
    viewEnd = endOfWeek(date);
    break;
  case "day":
  default:
    viewStart = startOfDay(date);
    viewEnd = endOfDay(date);
    break;
}
```

### Step 2: Determine Recurrence Type

Check if the event is recurring or one-off:

```typescript
// Recurring if no end date (or end date is far in future)
const isRecurring = !event.effectiveUntil;

// Convert to start of day for date comparisons
const effectiveStart = startOfDay(event.effectiveFrom);
const effectiveEnd = event.effectiveUntil
  ? startOfDay(event.effectiveUntil)
  : new Date(9999, 11, 31); // Far future
```

### Step 3: Generate Events for Recurring Blocks

For recurring events, generate one event per occurrence within the view range:

```typescript
import { addDays, isBefore, isAfter, isSameDay, isWithinInterval, getDay } from "date-fns";

if (isRecurring) {
  let currentWeekStart = startOfWeek(viewStart);
  const viewEndWeek = endOfWeek(viewEnd);

  while (isBefore(currentWeekStart, viewEndWeek) || isSameDay(currentWeekStart, viewEndWeek)) {
    // Calculate the date for this week's dayOfWeek occurrence
    const dayOffset = (event.dayOfWeek - getDay(currentWeekStart) + 7) % 7;
    const eventDate = addDays(currentWeekStart, dayOffset);

    // Check if this occurrence is within BOTH view range AND effective range
    const isInViewRange = isWithinInterval(eventDate, { start: viewStart, end: viewEnd });
    const isAfterStart = !isBefore(eventDate, effectiveStart);
    const isBeforeEnd = !isAfter(eventDate, effectiveEnd);

    if (isInViewRange && isAfterStart && isBeforeEnd) {
      const startTime = new Date(eventDate);
      startTime.setHours(event.startTime.getHours(), event.startTime.getMinutes());

      const endTime = new Date(eventDate);
      endTime.setHours(event.endTime.getHours(), event.endTime.getMinutes());

      calendarEvents.push({
        id: `${event.id}-${format(eventDate, "yyyy-MM-dd")}`, // Composite ID
        title: "Available",
        start: startTime,
        end: endTime,
        resource: {
          type: "availability",
          metadata: { isRecurring: true },
          originalData: event,
        },
      });
    }

    currentWeekStart = addDays(currentWeekStart, 7); // Next week
  }
}
```

**Key points:**
- Use **composite ID** `${event.id}-${date}` to distinguish weekly occurrences
- Filter by **both** view range and effective date range
- Loop through weeks, not days (more efficient)

### Step 4: Generate Events for One-Off Blocks

For one-off events, generate a single event on the specific date:

```typescript
else {
  // One-off availability: generate single event on effectiveFrom date
  const eventDate = effectiveStart;

  // Only show if within view range
  if (isWithinInterval(eventDate, { start: viewStart, end: viewEnd })) {
    const startTime = new Date(eventDate);
    startTime.setHours(event.startTime.getHours(), event.startTime.getMinutes());

    const endTime = new Date(eventDate);
    endTime.setHours(event.endTime.getHours(), event.endTime.getMinutes());

    calendarEvents.push({
      id: event.id, // Original ID (no composite)
      title: "Available",
      start: startTime,
      end: endTime,
      resource: {
        type: "availability",
        metadata: { isRecurring: false },
        originalData: event,
      },
    });
  }
}
```

**Key points:**
- Use **original ID** (no date suffix needed)
- Only generate if `effectiveFrom` is within view range
- Mark as `isRecurring: false` for visual distinction

### Step 5: Update useMemo Dependencies

Include `view` in the dependency array so events regenerate when view changes:

```typescript
const allEvents = useMemo<CalendarEvent[]>(() => {
  // ... event generation logic
  return calendarEvents;
}, [mode, availability, blockouts, bookings, date, view]);
//                                                      ^^^^ Include view
```

## Verification

After implementing this pattern:

1. ✅ One-off events appear only on their specific date
2. ✅ Recurring events appear every week within their effective range
3. ✅ No events appear before `effectiveFrom` or after `effectiveUntil`
4. ✅ Month view shows all weeks' events, not just current week
5. ✅ Changing view (month/week/day) regenerates events correctly

**Test cases:**
```typescript
// One-off block: Feb 15, 2026 only
const oneOff = {
  id: "1",
  dayOfWeek: 1, // Monday
  startTime: new Date("2026-01-01T09:00:00"),
  endTime: new Date("2026-01-01T17:00:00"),
  effectiveFrom: new Date("2026-02-15"),
  effectiveUntil: new Date("2026-02-15"),
};
// Should appear: Only on Feb 15, 2026
// Should NOT appear: Feb 8, Feb 22, or any other Monday

// Recurring block: Every Monday starting March 1
const recurring = {
  id: "2",
  dayOfWeek: 1, // Monday
  startTime: new Date("2026-01-01T09:00:00"),
  endTime: new Date("2026-01-01T17:00:00"),
  effectiveFrom: new Date("2026-03-01"),
  effectiveUntil: null, // No end date
};
// Should appear: March 2, 9, 16, 23, 30... (all Mondays from March 1 onward)
// Should NOT appear: Feb 23 or earlier Mondays
```

## Example: Complete Implementation

```typescript
import { useMemo } from "react";
import { Calendar, View } from "react-big-calendar";
import {
  format,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  startOfDay,
  endOfDay,
  addDays,
  isBefore,
  isAfter,
  isSameDay,
  isWithinInterval,
  getDay,
} from "date-fns";

interface AvailabilityBlock {
  id: string;
  dayOfWeek: number; // 0-6
  startTime: Date; // Time of day
  endTime: Date;
  effectiveFrom: Date;
  effectiveUntil: Date | null;
}

function MyCalendar({
  availability,
  view,
  date,
}: {
  availability: AvailabilityBlock[];
  view: View;
  date: Date;
}) {
  const events = useMemo(() => {
    const calendarEvents = [];

    // Calculate view range
    let viewStart: Date, viewEnd: Date;
    switch (view) {
      case "month":
        viewStart = startOfMonth(date);
        viewEnd = endOfMonth(date);
        break;
      case "week":
        viewStart = startOfWeek(date);
        viewEnd = endOfWeek(date);
        break;
      default:
        viewStart = startOfDay(date);
        viewEnd = endOfDay(date);
    }

    availability.forEach((avail) => {
      const isRecurring = !avail.effectiveUntil;
      const effectiveStart = startOfDay(avail.effectiveFrom);
      const effectiveEnd = avail.effectiveUntil
        ? startOfDay(avail.effectiveUntil)
        : new Date(9999, 11, 31);

      if (isRecurring) {
        // Generate weekly occurrences
        let weekStart = startOfWeek(viewStart);
        const weekEnd = endOfWeek(viewEnd);

        while (isBefore(weekStart, weekEnd) || isSameDay(weekStart, weekEnd)) {
          const dayOffset = (avail.dayOfWeek - getDay(weekStart) + 7) % 7;
          const eventDate = addDays(weekStart, dayOffset);

          if (
            isWithinInterval(eventDate, { start: viewStart, end: viewEnd }) &&
            !isBefore(eventDate, effectiveStart) &&
            !isAfter(eventDate, effectiveEnd)
          ) {
            const start = new Date(eventDate);
            start.setHours(avail.startTime.getHours(), avail.startTime.getMinutes());

            const end = new Date(eventDate);
            end.setHours(avail.endTime.getHours(), avail.endTime.getMinutes());

            calendarEvents.push({
              id: `${avail.id}-${format(eventDate, "yyyy-MM-dd")}`,
              title: "Available",
              start,
              end,
              resource: { isRecurring: true, data: avail },
            });
          }

          weekStart = addDays(weekStart, 7);
        }
      } else {
        // One-off event
        const eventDate = effectiveStart;

        if (isWithinInterval(eventDate, { start: viewStart, end: viewEnd })) {
          const start = new Date(eventDate);
          start.setHours(avail.startTime.getHours(), avail.startTime.getMinutes());

          const end = new Date(eventDate);
          end.setHours(avail.endTime.getHours(), avail.endTime.getMinutes());

          calendarEvents.push({
            id: avail.id,
            title: "Available (One-time)",
            start,
            end,
            resource: { isRecurring: false, data: avail },
          });
        }
      }
    });

    return calendarEvents;
  }, [availability, view, date]);

  return <Calendar events={events} view={view} date={date} />;
}
```

## Notes

### Performance Considerations

- **Large recurring ranges**: If a recurring event spans years and you're showing a month view, the loop might generate hundreds of events. Consider caching or pagination.
- **Memoization**: Always use `useMemo` with correct dependencies to avoid regenerating events on every render.

### Edge Cases

1. **Cross-day events**: If `endTime < startTime` (e.g., 11 PM - 1 AM), you may need to add 1 day to the end date
2. **Timezone handling**: If `startTime`/`endTime` are stored in a specific timezone, ensure proper conversion
3. **Daylight Saving Time**: date-fns handles DST correctly, but be aware of edge cases around DST transitions

### Alternative Approaches

**Option 1: Backend generates events** - Move this logic to the server and return pre-generated events for the requested date range. Reduces client-side complexity but increases API payload.

**Option 2: Use RRULE** - For complex recurrence patterns (every other Tuesday, last Friday of month), consider using the `rrule` library with react-big-calendar's built-in support.

### Visual Distinction

Mark recurring events visually to help users distinguish them:

```css
.rbc-event.recurring {
  border: 2px dashed currentColor !important;
}

.rbc-event.recurring::before {
  content: '🔁 ';
}
```

## References

- [react-big-calendar Documentation](https://jquense.github.io/react-big-calendar/examples/index.html)
- [date-fns Documentation](https://date-fns.org/docs/Getting-Started)
- [date-fns isWithinInterval](https://date-fns.org/docs/isWithinInterval)
- [MDN: Date.prototype.getDay()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getDay)
