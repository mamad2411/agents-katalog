---
name: calendly-office-hours-scheduling
description: Share Calendly scheduling links and check availability for office hours using calendly_* tools — read-only unless policy allows booking on behalf of students.
---

# Calendly office hours scheduling

## Purpose

Help TAs and lecturers **communicate office hours** using the connected Calendly account: list event types, check availability windows, and share the right scheduling URL — aligned with **`office-hours-and-help-queue`**.

## When to Use

- Student asks how to book office hours.
- TA needs this week's OH slots or the public scheduling link.
- Lecturer configures OH event types for the course.

## When NOT to Use

- Classroom syllabus sync → **course-context-from-classroom**.
- General calendar holds without Calendly → **google-calendar** / **coordinate-meetings**.

## Expected Outcome

- Correct **scheduling URL** or event type for the course OH.
- Availability summary for a proposed window (UTC ISO-8601).
- OH announcement text the human can post (what to bring, time limits).

## Workflow

1. **`calendly_verify_connection`** or **`calendly_get_current_user`**.
2. **`calendly_list_event_types`** — pick the OH event type (confirm name with lecturer).
3. For availability questions: **`calendly_get_event_type_availability`** with `startTime` / `endTime` in UTC.
4. Optionally **`calendly_list_scheduled_events`** for the lecturer's upcoming OH blocks.
5. Draft student-facing text; human sends via approved channel (Classroom announcement, email, etc.).

## Boundaries

- Do not book on a student's behalf unless institutional policy explicitly allows agent-initiated booking.
- Never expose private invitee details from scheduled events.
