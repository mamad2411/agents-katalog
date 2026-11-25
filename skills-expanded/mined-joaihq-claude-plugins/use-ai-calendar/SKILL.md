---
name: use-ai-calendar
description: Use the AI Calendar JoAi app plugin when the task needs AI Calendar tools or workflows.
---

# AI Calendar

Connect AI Calendar to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the AI Calendar tools available in this app.
- Explain what setup or authentication AI Calendar needs before I run an action.
- Use AI Calendar to help me with the task I describe next.

## Action Inventory

- `calendar-create-event` (collect) — Create an event on the agent's local calendar or connected Google/Microsoft/Apple calendar. Supports weekly, biweekly, and monthly recurrence for scheduling recurring meetings like syncs and standups — each instance gets its own JoAi meeting invite link.
- `calendar-delete-event` (collect) — Delete an event from the agent's connected calendar. The call is routed to the correct provider automatically.
- `calendar-feed-create` (collect) — Add a public iCalendar feed that imports events into this team's JoAi updates. Set the source timezone, choose whether incoming events publish automatically, and provide only public properties that websites may display.
- `calendar-feed-delete` (collect) — Remove an iCalendar source from this team's imported updates. This stops future imports for that source while preserving the explicit approval step for a destructive configuration change.
- `calendar-feed-list` (collect) — List the iCalendar feeds that import events into this team's JoAi updates. See each source's sync status, publishing setting, and public event properties so an agent can manage the team's calendar imports.
- `calendar-feed-sync` (collect) — Fetch one iCalendar source now and apply its changes to this team's imported updates. The result reports how many events were created, updated, archived, or unchanged so an agent can confirm the synchronization outcome.
- `calendar-feed-update` (collect) — Change an existing iCalendar source for this team's imported updates. Update its source address, timezone, sync state, publishing preference, or safe public properties without changing unrelated calendar sources.
- `calendar-list-events` (collect) — List upcoming events from the agent's connected calendar within a date range.
- `calendar-update-event` (collect) — Update an existing event on the agent's connected calendar. Supply only the fields you want to change.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
