---
name: react-big-calendar-nextjs-integration
description: |
  Integrate react-big-calendar with Next.js 16 App Router and shadcn/ui. Use when: (1) Need to add a visual calendar to Next.js app, (2) Want calendar that works with server/client component split, (3) Need to integrate with shadcn/ui theming, (4) Building scheduling or availability features. Covers component structure, CSS imports in client components, date-fns localizer setup, and event styling with shadcn variables.
author: Claude Code
version: 1.0.0
date: 2026-02-03
---

# React Big Calendar + Next.js 16 + shadcn/ui Integration

## Problem
react-big-calendar is a popular calendar library but requires careful integration with Next.js 16's App Router, especially regarding client/server component boundaries, CSS imports, and theming consistency with shadcn/ui.

## Context / Trigger Conditions
- Building a calendar feature in Next.js 16 with App Router
- Using shadcn/ui for consistent design system
- Need server-side data fetching with client-side calendar interaction
- Want calendar events to match shadcn/ui color scheme

## Solution

### 1. Install Dependencies

```bash
pnpm add react-big-calendar date-fns
pnpm add -D @types/react-big-calendar
```

Note: react-big-calendar works well with `date-fns` v4+ for date manipulation.

### 2. Create Client Component with Proper Imports

```tsx
"use client";

import { useState, useMemo, useCallback } from "react";
import { Calendar, dateFnsLocalizer, View } from "react-big-calendar";
import { format, parse, startOfWeek, getDay } from "date-fns";
import { enUS } from "date-fns/locale";

// IMPORTANT: Import CSS in the client component
import "react-big-calendar/lib/css/react-big-calendar.css";
import "./custom-calendar.css"; // Your overrides

// Configure localizer OUTSIDE the component
const locales = { "en-US": enUS };
const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

export function MyCalendar({ events, onEventClick }) {
  const [view, setView] = useState<View>("month");
  const [date, setDate] = useState(new Date());

  return (
    <Calendar
      localizer={localizer}
      events={events}
      view={view}
      date={date}
      onView={setView}
      onNavigate={setDate}
      onSelectEvent={onEventClick}
      style={{ height: 600 }}
    />
  );
}
```

### 3. Style Integration with shadcn/ui

Create `custom-calendar.css` to override react-big-calendar styles with shadcn/ui CSS variables:

```css
/* Use shadcn/ui CSS variables for theming */
.rbc-calendar {
  font-family: inherit;
}

.rbc-header {
  padding: 0.75rem 0.5rem;
  font-weight: 600;
  border-bottom: 1px solid hsl(var(--border));
}

.rbc-today {
  background-color: hsl(var(--accent));
}

.rbc-off-range-bg {
  background-color: hsl(var(--muted));
}

.rbc-event {
  border-radius: 0.25rem;
  /* Use your event type colors */
}

.rbc-time-slot {
  border-top: 1px solid hsl(var(--border));
}
```

### 4. Server Component Integration Pattern

```tsx
// app/calendar/page.tsx (Server Component)
import { MyCalendarWrapper } from "./MyCalendarWrapper";

export default async function CalendarPage() {
  // Fetch data server-side
  const events = await db.event.findMany();

  // Pass to client component
  return <MyCalendarWrapper events={events} />;
}

// app/calendar/MyCalendarWrapper.tsx (Client Component)
"use client";

import { MyCalendar } from "@/components/calendar/MyCalendar";
import { useRouter } from "next/navigation";

export function MyCalendarWrapper({ events }) {
  const router = useRouter();

  const handleEventClick = (event) => {
    // Client-side navigation
    router.push(`/event/${event.id}`);
  };

  return <MyCalendar events={events} onEventClick={handleEventClick} />;
}
```

### 5. Event Styling with Custom Getter

```tsx
const eventStyleGetter = useCallback((event) => {
  let backgroundColor = "#3b82f6"; // default

  switch (event.type) {
    case "available":
      backgroundColor = "hsl(var(--success))"; // green
      break;
    case "blocked":
      backgroundColor = "hsl(var(--destructive))"; // red
      break;
    case "booked":
      backgroundColor = "hsl(var(--primary))"; // blue
      break;
  }

  return {
    style: {
      backgroundColor,
      borderRadius: "4px",
      opacity: 0.9,
      color: "white",
      border: "none",
    },
  };
}, []);

// In Calendar component
<Calendar
  {...props}
  eventPropGetter={eventStyleGetter}
/>
```

## Verification

- Calendar renders without hydration errors
- CSS loads properly (no flash of unstyled content)
- Events display with consistent shadcn/ui colors
- Navigation and view switching work smoothly
- No "use client" directive errors

## Example: Complete Calendar Component

```tsx
"use client";

import { useState, useCallback } from "react";
import { Calendar, dateFnsLocalizer, View } from "react-big-calendar";
import { format, parse, startOfWeek, getDay } from "date-fns";
import { enUS } from "date-fns/locale";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

import "react-big-calendar/lib/css/react-big-calendar.css";
import "./calendar-styles.css";

const locales = { "en-US": enUS };
const localizer = dateFnsLocalizer({
  format, parse, startOfWeek, getDay, locales,
});

interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  type: "available" | "blocked" | "booked";
}

export function AppCalendar({
  events,
  onEventClick,
  onDateSelect,
}: {
  events: CalendarEvent[];
  onEventClick?: (event: CalendarEvent) => void;
  onDateSelect?: (date: Date) => void;
}) {
  const [view, setView] = useState<View>("month");
  const [date, setDate] = useState(new Date());

  const eventStyleGetter = useCallback((event: CalendarEvent) => {
    const colors = {
      available: "#10b981",
      blocked: "#ef4444",
      booked: "#3b82f6",
    };

    return {
      style: {
        backgroundColor: colors[event.type],
        borderRadius: "4px",
        opacity: 0.9,
        color: "white",
        border: "none",
      },
    };
  }, []);

  return (
    <Card className="p-4">
      <Calendar
        localizer={localizer}
        events={events}
        view={view}
        date={date}
        onView={setView}
        onNavigate={setDate}
        onSelectEvent={onEventClick}
        onSelectSlot={({ start }) => onDateSelect?.(start)}
        eventPropGetter={eventStyleGetter}
        selectable
        style={{ height: 600 }}
      />
    </Card>
  );
}
```

## Notes

- **Performance**: For large event lists (>1000), consider virtualization or limiting date range
- **Mobile**: react-big-calendar is not mobile-optimized by default - use day view for mobile screens
- **Timezone**: Pass events with consistent timezone (UTC recommended), convert for display
- **Custom Toolbar**: Set `toolbar={false}` and build custom navigation with shadcn/ui components
- **Accessibility**: react-big-calendar has decent keyboard navigation built-in
- **Types**: Event interface should match your database schema

## Common Pitfalls

1. **CSS Import Location**: Must import CSS in client component, not server component or layout
2. **Localizer Creation**: Create localizer outside component to avoid recreation on every render
3. **Date Objects**: Ensure event start/end are JavaScript Date objects, not strings
4. **View State**: Manage view and date state to enable custom navigation controls
5. **Event IDs**: Always include unique `id` field on events for React keys

## References

- [react-big-calendar Documentation](https://jquense.github.io/react-big-calendar/api.html)
- [Next.js 16 Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)
- [shadcn/ui CSS Variables](https://ui.shadcn.com/docs/theming)
- [date-fns Documentation](https://date-fns.org/)
