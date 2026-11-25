---
name: booking-logic
description: Use this skill when implementing or modifying any booking-related feature: slot availability calculation, booking creation, cancellation, overlap detection, or schedule management. This is the most critical domain of the application.
---

# Booking Logic — Hair Salon Booking App

## Core Concept
A slot is **available** if and only if ALL of the following are true:
1. The date is not in `days_off`
2. The day of week has an active `schedule_rule`
3. The slot start time is ≥ `open_time`
4. The slot end time (start + service duration) is ≤ `close_time`
5. The slot does not overlap any existing `confirmed` or `pending` booking

---

## Slot Availability Algorithm

```ts
// features/booking/utils.ts

export function getAvailableSlots(
  date: Date,
  scheduleRule: ScheduleRule | null,
  existingBookings: TimeRange[],
  serviceDurationMinutes: number,
  daysOff: DayOff[]
): string[] {
  // 1. Check day off
  if (isDayOff(date, daysOff)) return []

  // 2. Check schedule rule exists and is active
  if (!scheduleRule || !scheduleRule.is_active) return []

  // 3. Generate all possible slots (every 15 minutes)
  const slots = generateTimeSlots(
    scheduleRule.open_time,
    scheduleRule.close_time,
    SLOT_INTERVAL_MINUTES
  )

  // 4. Filter slots that fit the service duration without overlap
  return slots.filter((slot) => {
    const slotStart = parseTimeToDate(date, slot)
    const slotEnd = addMinutes(slotStart, serviceDurationMinutes)

    // Must end before or at closing time
    const closingTime = parseTimeToDate(date, scheduleRule.close_time)
    if (slotEnd > closingTime) return false

    // Must not overlap existing bookings
    return !existingBookings.some((booking) =>
      isOverlapping(
        { start: slotStart, end: slotEnd },
        { start: booking.start, end: booking.end }
      )
    )
  })
}
```

---

## Overlap Detection (critical — test this thoroughly)

```ts
export function isOverlapping(a: TimeRange, b: TimeRange): boolean {
  // Two ranges overlap if one starts before the other ends
  // AND the other starts before the first ends
  return a.start < b.end && b.start < a.end
}
```

> ⚠️ Edge case: `a.end === b.start` must return `false` (back-to-back is allowed)

---

## Booking Creation Flow

```
Client submits form
  → Validate input (server-side)
  → Re-check slot availability (race condition protection)
  → Insert booking with status: 'pending'
  → Send request-received email with the 20 € deposit information
  → Return booking id + cancel_token to client
```

> Always re-check availability server-side before inserting.
> A slot valid at form render may be taken by the time the form is submitted.
> Client-created bookings remain `pending` until the admin validates that the 20 € deposit has been paid.
> `pending` bookings still block availability so the slot cannot be double-booked.

---

## Admin Confirmation Flow

```
Admin opens booking detail
  → Confirms deposit has been received
  → Update booking status to 'confirmed'
  → Send final confirmation email via Resend
```

## Client Reminder Flow

```
An external scheduler calls /api/cron/client-reminders every 15 minutes
  → Verify Authorization header against CRON_SECRET
  → Find confirmed bookings around J-1 and 2h before the appointment
  → Send the client reminder email through Resend
  → Mark the matching reminder timestamp on bookings to avoid duplicates
```

> Client reminders are sent only for `confirmed` bookings.
> Each reminder type has its own idempotency column:
> `client_day_before_reminder_sent_at` and `client_two_hours_reminder_sent_at`.
> Vercel Hobby only supports daily Cron Jobs, so 15-minute reminders must use
> an external scheduler or a Vercel Pro plan.

---

## Cancellation Flow

```
Client clicks cancel link (email contains /cancel?token=UUID)
  → Display a confirmation page first (do not mutate on GET)
  → Client explicitly confirms the cancellation
  → Verify cancel_token exists and booking status is not 'cancelled'
  → Update booking status to 'cancelled'
  → Send cancellation confirmation email
```

## Review Request Flow

```
Admin opens a completed confirmed booking
  → Send an email containing /avis/deposer?booking_id=UUID&token=REVIEW_TOKEN
  → Client submits a rating and comment
  → Re-verify booking_id + review_token and appointment eligibility server-side
  → Insert one hidden review linked to the booking and service
  → Hairdresser publishes or rejects the review from the dashboard
```

> `review_token` is distinct from `cancel_token`. Client identity, email, and service
> are copied from the verified booking and never trusted from the public form.

---

## Types

```ts
// types/booking.ts

export interface TimeRange {
  start: Date
  end: Date
}

export interface DayOff {
  date: string // ISO date 'YYYY-MM-DD'
  reason?: string
}

export interface ScheduleRule {
  day_of_week: number // 0–6
  open_time: string   // 'HH:MM'
  close_time: string  // 'HH:MM'
  is_active: boolean
}
```

---

## Constants

```ts
// features/booking/utils.ts
export const SLOT_INTERVAL_MINUTES = 15
export const MAX_ADVANCE_BOOKING_DAYS = 60
```

---

## Forbidden Patterns
- Never trust client-side slot availability — always revalidate server-side
- Never store `ends_at` as client input — always compute it from `starts_at + duration`
- Never allow booking on `cancelled` service
- Never expose `cancel_token` in public listing endpoints
