---
name: use-appointment
description: Use the Appointment JoAi app plugin when the task needs Appointment tools or workflows.
---

# Appointment

Connect Appointment to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Appointment tools available in this app.
- Explain what setup or authentication Appointment needs before I run an action.
- Use Appointment to help me with the task I describe next.

## Action Inventory

- `appointment-availability` (collect) — Collect booking details and return appointment availability from the target agent calendar.
- `appointment-book` (collect) — Browse available time slots and book an appointment.
- `appointment-book-confirm` (collect) — Book a confirmed appointment slot for the target agent.
- `appointment-booking-link` (link) — Get the public booking link for your appointment page. Share this link so people can book appointments with you directly.
- `appointment-cancel` (collect) — Cancel an existing booked appointment and optionally provide a reason. Frees up the time slot so it becomes available for new bookings again.
- `appointment-cancel-public` (collect) — Cancel a booked appointment from the public booking widget.
- `appointment-configure` (collect) — Open and update the appointment configuration for this agent.
- `appointment-confirm` (collect) — View a confirmed appointment with calendar download and join link. Share this page so attendees can add the meeting to their calendar.
- `appointment-email-confirm` (collect) — Sends a booking confirmation email to the attendee after an appointment is booked.
- `appointment-onboarding` (collect) — Start appointment onboarding by opening calendar integration setup for this agent.
- `appointment-policy-get` (collect) — View the appointment booking policy for your team: availability, buffer times, notice periods, and configured services.
- `appointment-policy-upsert` (collect) — Save the appointment booking policy for your agent. Configure timezone, availability, synchronized business opening hours, slot intervals, buffer times, and booking rules.
- ...and 4 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
