# calendar skill

## mission

the calendar skill manages time-bound commitments with strict timezone discipline, conflict awareness, and confirmation-safe drafts.

it exists to turn ambiguous scheduling requests into precise, durable calendar state.

## core capabilities

- create, update, reschedule, and cancel events
- normalize user time references into explicit timezone-aware timestamps
- check availability and detect conflicts
- manage attendees, conferencing links, locations, recurrence, and reminders
- preserve event identity across edits and thread-like update flows

## boundaries

- never guess a timezone when the input is ambiguous
- never mutate an event without the full event snapshot or explicit update target
- never drop attendees, conferencing details, or recurrence rules unintentionally
- never turn a tentative hold into a definitive event without confirmation where needed
- never edit a meeting series as if it were a single instance unless the request explicitly says so

## input schema

```ts
type CalendarSkillInput = {
  mode: 'draft' | 'create' | 'update' | 'reschedule' | 'cancel' | 'availability' | 'conflict-check'
  title?: string
  start?: string
  end?: string
  timezone?: string
  attendees?: string[]
  location?: string
  conference?: {
    type: 'meet' | 'zoom' | 'teams' | 'custom'
    url?: string
  }
  recurrence?: {
    rrule: string
    until?: string
  }
  reminders?: Array<{
    method: 'popup' | 'email'
    minutesBefore: number
  }>
  sourceEventId?: string
  changes?: Record<string, unknown>
  confirmationState?: 'required' | 'confirmed' | 'not-required'
}
```

## output schema

```ts
type CalendarSkillOutput = {
  ok: boolean
  output: {
    draftId?: string
    eventId?: string
    normalizedStart?: string
    normalizedEnd?: string
    timezone?: string
    conflicts?: Array<{
      eventId: string
      title: string
      start: string
      end: string
      reason: string
    }>
    availability?: Array<{
      start: string
      end: string
      free: boolean
    }>
    nextAction: 'confirm' | 'create' | 'update' | 'cancel' | 'clarify' | 'done'
  }
  retryable: boolean
  note?: string
  trace?: Record<string, unknown>
}
```

## failure modes

- timezone ambiguity
- conflicting commitments
- recurrence edge cases
- stale event snapshots
- attendee identity mismatch
- resource or room unavailability
- all-day event misinterpretation

## recovery logic

- canonicalize every time reference before mutation
- run conflict detection before committing state
- if the request is underspecified, produce a draft and ask for the missing field instead of guessing
- if an update fails, re-fetch the current event snapshot and reapply the delta
- preserve the full updated draft for confirmation flows
- prefer explicit local-time plus timezone over implicit conversion

## advanced league implementation details

- treat calendars as constrained state machines, not plain records
- preserve series identity when editing recurring events
- compare original and updated payloads to detect accidental drift
- normalize relative phrases like tomorrow or next friday into a concrete schedule plan before execution
- generate a confirmation-safe draft whenever the user could plausibly be surprised by the result
- maintain exact time zone provenance from input to final event payload
- for meeting scheduling, separate availability discovery from event creation

## quality bar

a calendar action should never surprise the user by moving time, timezone, or attendees without a visible draft and explicit state trail
