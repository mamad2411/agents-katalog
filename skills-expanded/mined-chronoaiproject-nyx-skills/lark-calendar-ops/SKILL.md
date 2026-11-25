---
name: lark-calendar-ops
version: "1.1"
description: Calendar assistant over the bot's NyxID-brokered Lark calendar/v4 APIs — list calendars, check free/busy across people, find a common slot, read your agenda for a window, and create or update events with attendees. Knows the event-time shape (a timestamp + timezone object, not RFC3339) and that attendees are added in a separate call, and doubles as the calendar-scope probe — on a scope 403 it reports the exact missing permission instead of failing.
metadata:
  category: plain
  tag:
    - aevatar
    - s-capability
    - lark
    - calendar
    - scheduling
    - meetings
---

# Lark Calendar Ops

Use this for scheduling asks in chat: "明天下午约个会 / 看看我和某某周四有没有空 / 我今天有什么安排 /
把周五的评审改到 4 点".

**You (the agent) run the flow yourself** via NyxID-brokered access `nyxid_proxy`
`{slug:"api-lark-bot", path:"/open-apis/calendar/v4/...", method:...}`. ⚠ Calendar scopes are NOT
yet field-proven for this bot tenant — so this skill is also the probe: run the cheapest read
first, and if it 403s, report the exact scope error verbatim plus what to grant, then stop
gracefully. Never invent availability.

## Two footguns

1. **Event times are objects, not RFC3339 strings.** `start_time` / `end_time` in a create/update
   body are `{"timestamp":"<unix seconds>","timezone":"Asia/Shanghai"}`. Convert the user's
   wall-clock to unix seconds in their timezone for the request; only use RFC3339 / human strings
   when you SAY the time back, never inside the body.
2. **Attendees and free/busy are separate from the create.** Creating an event does NOT add
   attendees — `POST .../events/{event_id}/attendees` is a second call after the create. And
   `freebusy/list` returns busy blocks WITHOUT titles for other people — report availability as
   busy/free, never invent an event title you did not read from the requester's own calendar.

## How to run it

1. **Scope probe (always first, cheap read).**
   `GET /open-apis/calendar/v4/calendars` — lists calendars visible to the bot identity.
   On 403/scope error: report verbatim, state that the tenant app needs calendar scopes
   (e.g. `calendar:calendar`, `calendar:calendar.event:read/write`, freebusy read), and stop.

2. **Resolve people and time.** Map names to open_ids via prior chat context or
   `POST /open-apis/contact/v3/users/batch_get_id?user_id_type=user_id` / chat member lookup; never
   guess ids. Convert "明天下午/周四" to concrete RFC3339 times in the user's timezone
   (default Asia/Shanghai unless the chat says otherwise) and SAY the concrete times back.

3. **Free/busy.** `POST /open-apis/calendar/v4/freebusy/list` with `time_min`/`time_max` and the
   user ids. To find a common slot: intersect the gaps, prefer working hours 10:00-18:00, offer the
   2-3 best candidates with duration.

4. **My agenda.** Read the primary calendar's events for the window
   (`GET /open-apis/calendar/v4/calendars/{calendar_id}/events` with time filters) and render:
   `[时间] 标题 (地点/链接, 参与人数)` in chronological order.

5. **Create / update (explicit confirmation required).** Echo the exact event first — title, start,
   end, timezone, attendees — and only on the user's confirm:
   `POST /open-apis/calendar/v4/calendars/{calendar_id}/events` body
   `{summary, start_time:{timestamp,timezone}, end_time:{...}}`, then add attendees via
   `POST .../events/{event_id}/attendees`. Update = `PATCH .../events/{event_id}`. Report the
   created event id and time back.

## Failure semantics

- Scope 403 anywhere → verbatim error + the missing-scope prescription from step 1; never retry.
- Attendee resolution failure → name the person you could not resolve and ask for their open_id or
  an @mention; never book with a guessed id.

## Guardrails

- Never create, modify, or delete events without an explicit user confirm of the echoed details in
  this conversation; deletion additionally requires the user to name the exact event.
- Treat other people's calendar details as sensitive: report free/busy as busy blocks, not event
  titles, unless the calendar is the requester's own.
- Only use real returned data; never ask the user for tokens — your NyxID-brokered tools handle
  all credentials.
