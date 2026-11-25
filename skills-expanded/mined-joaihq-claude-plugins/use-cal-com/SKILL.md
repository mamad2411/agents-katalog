---
name: use-cal-com
description: Use the Cal.com JoAi app plugin when the task needs Cal.com tools or workflows.
---

# Cal.com

Connect Cal.com to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Cal.com tools available in this app.
- Explain what setup or authentication Cal.com needs before I run an action.
- Use Cal.com to help me with the task I describe next.

## Action Inventory

- `cal-cancel-booking` (collect) — Cancel an existing Cal.com booking by its unique identifier.
- `cal-create-booking` (collect) — Create a new booking on Cal.com for a specific event type and time slot.
- `cal-get-available-slots` (collect) — Get available time slots for a Cal.com event type within a date range.
- `cal-get-booking` (collect) — Retrieve details of a specific Cal.com booking by its unique identifier.
- `cal-list-bookings` (collect) — Retrieve all bookings for the authenticated Cal.com user. Filter by status, date range, or event type.
- `cal-list-event-types` (collect) — List all available event types for the authenticated Cal.com user.
- `cal-reschedule-booking` (collect) — Reschedule an existing Cal.com booking to a new time slot.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
