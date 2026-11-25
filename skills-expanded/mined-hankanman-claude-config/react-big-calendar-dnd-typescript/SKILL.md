---
name: react-big-calendar-dnd-typescript
description: |
  Fix TypeScript errors when integrating react-big-calendar drag-and-drop addon in Next.js/React projects. Use when: (1) Getting "Module has no exported member 'EventInteractionArgs'" error, (2) EventWrapperProps type missing 'children' property causing type errors, (3) stringOrDate type mismatches in onEventDrop/onEventResize handlers. Covers proper type imports and generic type parameters for withDragAndDrop HOC.
author: Claude Code
version: 1.0.0
date: 2026-02-05
---

# react-big-calendar Drag-and-Drop TypeScript Integration

## Problem
When adding drag-and-drop functionality to react-big-calendar with TypeScript, you encounter multiple type errors that aren't obvious from the documentation. The main module doesn't export all necessary types, and the DnD wrapper requires explicit generic parameters.

## Context / Trigger Conditions

**Error 1**: `TS2305: Module '"react-big-calendar"' has no exported member 'EventInteractionArgs'`

**Error 2**: `TS2339: Property 'children' does not exist on type 'EventWrapperProps<CalendarEvent>'`

**Error 3**: `Type 'stringOrDate' is not assignable to type 'Date'` in drag handlers

**When you see these**:
- Adding `withDragAndDrop` HOC to Calendar component
- Implementing `onEventDrop` or `onEventResize` handlers
- Using custom `EventWrapper` component with context menus or tooltips
- TypeScript strict mode enabled

## Solution

### Step 1: Import Types from Correct Locations

The DnD types are NOT exported from the main `react-big-calendar` module. Import from the addon:

```typescript
// ❌ WRONG - EventInteractionArgs not in main exports
import { Calendar, type EventInteractionArgs } from "react-big-calendar";

// ✅ CORRECT - Import DnD types from addon
import { Calendar, type EventWrapperProps } from "react-big-calendar";
import withDragAndDrop, { type EventInteractionArgs } from "react-big-calendar/lib/addons/dragAndDrop";
```

### Step 2: Add Generic Type Parameters to withDragAndDrop

The HOC needs explicit event and resource types:

```typescript
// Define your event type
interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  resource: {
    type: "availability" | "booking";
    // ... other properties
  };
}

// ❌ WRONG - No type parameters
const DnDCalendar = withDragAndDrop(Calendar);

// ✅ CORRECT - Explicit generic types
const DnDCalendar = withDragAndDrop<CalendarEvent, object>(Calendar);
```

### Step 3: Handle EventWrapperProps Children

`EventWrapperProps` doesn't include `children` by default. Extend it:

```typescript
// ❌ WRONG - Missing children property
const EventWrapper = (props: EventWrapperProps<CalendarEvent>) => {
  const { event, children } = props; // Error: children doesn't exist
  return <div>{children}</div>;
};

// ✅ CORRECT - Extend with children
const EventWrapper = useCallback(
  (props: EventWrapperProps<CalendarEvent> & { children?: React.ReactNode }) => {
    const { event, children } = props;
    return (
      <ContextMenu event={event}>
        {children}
      </ContextMenu>
    );
  },
  [dependencies]
);
```

### Step 4: Handle stringOrDate Type in Drag Handlers

The drag/resize handlers receive `stringOrDate` type (can be Date or string). Convert to Date:

```typescript
// ❌ WRONG - Assumes Date type
const handleEventDrop = ({ event, start, end }: { event: CalendarEvent; start: Date; end: Date }) => {
  // Type error: start/end might be strings
  await moveEvent(event.id, start, end);
};

// ✅ CORRECT - Use EventInteractionArgs and convert
const handleEventDrop = useCallback(
  (args: EventInteractionArgs<CalendarEvent>) => {
    const { event, start, end } = args;

    // Convert stringOrDate to Date
    const startDate = start instanceof Date ? start : new Date(start);
    const endDate = end instanceof Date ? end : new Date(end);

    await moveEvent(event.id, startDate, endDate);
  },
  [dependencies]
);
```

### Complete Example

```typescript
import { useState, useCallback } from "react";
import { Calendar, type EventWrapperProps } from "react-big-calendar";
import withDragAndDrop, { type EventInteractionArgs } from "react-big-calendar/lib/addons/dragAndDrop";

interface CalendarEvent {
  id: string;
  title: string;
  start: Date;
  end: Date;
  resource: { type: string };
}

// Create typed DnD calendar
const DnDCalendar = withDragAndDrop<CalendarEvent, object>(Calendar);

function MyCalendar() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);

  // Event wrapper with children support
  const EventWrapper = useCallback(
    (props: EventWrapperProps<CalendarEvent> & { children?: React.ReactNode }) => {
      const { event, children } = props;
      return <div data-event-id={event.id}>{children}</div>;
    },
    []
  );

  // Drag handler with stringOrDate conversion
  const handleEventDrop = useCallback(
    (args: EventInteractionArgs<CalendarEvent>) => {
      const { event, start, end } = args;
      const startDate = start instanceof Date ? start : new Date(start);
      const endDate = end instanceof Date ? end : new Date(end);

      // Update event...
      setEvents((prev) =>
        prev.map((e) =>
          e.id === event.id ? { ...e, start: startDate, end: endDate } : e
        )
      );
    },
    []
  );

  return (
    <DnDCalendar
      events={events}
      startAccessor="start"
      endAccessor="end"
      draggableAccessor={() => true}
      resizable
      onEventDrop={handleEventDrop}
      onEventResize={handleEventDrop}
      components={{
        eventWrapper: EventWrapper,
      }}
    />
  );
}
```

## Verification

After applying these fixes:
1. ✅ No TypeScript errors about missing exports
2. ✅ EventWrapper accepts children without type errors
3. ✅ Drag handlers accept EventInteractionArgs properly
4. ✅ Date conversion handles both Date and string inputs
5. ✅ `pnpm types` (or `tsc --noEmit`) passes with no errors

## Notes

- **Type Definition Location**: The separation of DnD types is intentional—they're addon-specific, not core calendar types
- **Generic Parameters Required**: Without `<CalendarEvent, object>`, the DnD calendar defaults to `<object, object>` which loses your custom event typing
- **stringOrDate Design**: The library allows both Date objects and ISO strings for flexibility, but TypeScript needs explicit handling
- **Children Property**: `EventWrapperProps` is designed for internal rendering. Adding children is safe for custom wrappers (context menus, tooltips, etc.)
- **React 18+**: Use `useCallback` with proper dependencies to avoid re-creating wrapper components on every render

## Common Pitfalls

1. **Importing from wrong module**: Always import `EventInteractionArgs` from the addon, not main module
2. **Missing generic types**: `withDragAndDrop(Calendar)` loses type safety—always add `<EventType, ResourceType>`
3. **Assuming Date type**: Never assume `start`/`end` are Date objects—always check/convert
4. **Forgetting children**: If wrapping events in context menus/tooltips, extend `EventWrapperProps` with children

## References

- [react-big-calendar TypeScript Definitions](https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/react-big-calendar)
- [react-big-calendar DnD Addon](https://github.com/jquense/react-big-calendar/tree/master/src/addons/dragAndDrop)
- [TypeScript Handbook: Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)
