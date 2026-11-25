---
name: calendar
description: Plan the operator's time - events (one-off and recurring), free time, structured plans (meal plans, shopping lists, workouts) with typed events, checklists, tables and groups via CalendarBulkCreate and CalendarBlockPatch, and their personal to-do tasks with the Planner tools.
requires: calendar, board, scheduling
---
# Calendar and planner

## Which tool for which request

- **An appointment the operator will attend** (a meeting, a doctor's visit, a flight, a birthday): a calendar
  event, `CalendarCreate`. It has a start and an end and shows on the calendar.
- **Something the operator has to do** ("buy a gift", "send the report by Friday"): a planner task,
  `PlannerTaskCreate`. Give it a `due_date` (and `due_time` if it matters). When they want to set time aside
  for it, also give `scheduled_start`/`scheduled_end`: that blocks the time on their calendar.
- **Something *you* must do later** ("check the deploy tomorrow at 9", "every Monday send me a summary"):
  that is not the calendar at all. Use `ScheduleCreate`, which runs you at that time.
- "Remind me to…" is a task with a reminder when it is the operator's own to-do, and `ScheduleCreate` when
  you are the one who has to act. Ask if it is unclear.
- These planner tasks are the operator's own list. The Board (`BoardAdd`) is your plan of work in a session;
  never put the operator's errands there.

## Reading

- `CalendarEvents` returns occurrences: a weekly meeting appears once per week, each with its own `id`,
  its series' `event_id`, its `occurrence_start` and the calendar's name. With `query` it searches instead.
- `CalendarList` gives the calendars (ids, which are writable, which are read-only subscriptions), their
  sync status, and the settings: the operator's time zone and working hours.
- `PlannerTasks` with `view` = `today`, `overdue`, `upcoming`, `inbox`, `done` or `all`.
- Before saying "you are free at…", call `CalendarFindTime`. Never infer free time from memory or from a
  partial read; it looks across every visible calendar and every time-blocked task.

## Dates, times and zones

- Times you send are ISO 8601 with an explicit offset. Name the IANA `timezone` the event lives in;
  without one the operator's calendar zone is used. A recurring event repeats on that zone's wall clock,
  so "every Monday at 10:00" stays at 10:00 across daylight-saving changes.
- Resolve relative dates ("tomorrow", "next Friday", "in the evening") in the operator's time zone from
  `CalendarList`, not in UTC. When a date or time is genuinely ambiguous ("next weekend", "after lunch",
  a time with no zone for a call with someone abroad), ask; when you choose, state the assumption in your
  reply ("I put it at 19:00 Moscow time").
- All-day events take the dates' midnights; the end is exclusive (a one-day event on 5 October ends on 6 October).

## Changing and deleting

- Read first, then pass the event's `event_id` and `version`; a stale version is refused so that you never
  overwrite a change made meanwhile. Read again and retry rather than guessing.
- For a recurring event, decide the scope and confirm it with the operator when they did not say:
  `scope="this"` with that occurrence's `occurrence_start` changes or removes one occurrence;
  `scope="all"` changes the whole series. Moving "the meeting on Thursday" means `this`.
- Repeat rules are RRULEs: `FREQ=WEEKLY;BYDAY=MO,WE`, `FREQ=MONTHLY;BYMONTHDAY=1`, `FREQ=DAILY;COUNT=10`.
- Subscriptions are read-only; create events in a writable calendar. An event in a connected calendar
  shows `pending_sync` until its provider confirms it. When it shows `conflict`, the provider changed it
  too: tell the operator what differs and let them choose in the app; do not overwrite it yourself.
- Completing a repeating task with `PlannerTaskComplete` records it as done and moves it to the next date.

## Structured entries: types, blocks, groups

An event can carry more than a description. Use the structure whenever the content is a list, a table,
steps or numbers: the operator ticks items in the app, the totals are computed, and you can read back what
they marked. Never paste a 40-line list into `description`.

- **Blocks** are the body of an event, in order: `markdown {text}`, `checklist {items: [{text, checked}]}`,
  `table {columns: [{key, label, type: text|number|money|checkbox|link|date, unit?, aggregate?: sum|avg|count}],
  rows: [{cells: {...}}]}`, `steps {items: [{text, duration_min?}]}`, `fields {items: [{label, value, unit?}]}`,
  `link {url, label}`, `action {action: url, label, url}` or `action {action: agent, label, prompt}`.
  A shopping basket is a table with a `checkbox` column ("bought") and a `money` column with `aggregate: sum`.
  Ids are generated for blocks, items and rows you leave without one.
- **Types** (`CalendarTypeUpsert`) describe a kind of event once: `fields_schema` (kcal, protein_g, meal…),
  `default_blocks` (what a new event of the type starts with), `display.chip` (`"{meal} · {kcal} kcal"`, the
  short label in the calendar) and `aggregates` (`[{field: "kcal", op: "sum", per: "day", label, target:
  [1900, 2100]}]`, shown under each day). Look at `CalendarTypeList` first and reuse a type that fits;
  starters exist for `todo-list`, `shopping`, `appointment` and `routine`. A field value that does not fit
  the schema is kept and shown in `field_issues`; fix it rather than ignore it.
- **Groups** (`CalendarGroupCreate`) hold the events of one plan ("Menu 14-20 October"). The whole plan can
  then be moved (`CalendarGroupShift`), repeated next week (`CalendarGroupDuplicate`, ticks cleared),
  hidden, archived or deleted at once. `CalendarList` lists the groups.
- **Status** is `planned`, `done`, `skipped` or `cancelled`; set it with `CalendarUpdate`.

### Making a plan (a week of meals, a training block)

1. `CalendarTypeList`; if nothing fits, one `CalendarTypeUpsert` (for meals: `meal` with `kcal`, `protein_g`,
   an enum `meal`, `default_blocks` of a `checklist` "Products" and `steps` "Recipe", a chip and a daily kcal
   aggregate).
2. One `CalendarGroupCreate` for the plan.
3. One `CalendarBulkCreate` with every event (`type` and `group_id` once at the top level), each with its
   `fields` and blocks. Thirty-five meals are one call, not thirty-five.
4. Shopping orders are events of type `shopping` in the same group, their basket a table.

### Reading back and following up

- `CalendarEvents` lists events with `progress` and `chip` but without block bodies; pass
  `include_blocks=true` (or `event_id`) when you need the items and their ids.
- Tick or edit a few items with `CalendarBlockPatch` (`set_checked`, `add_item`, `update_cell`…); ticks need
  no version. Replace the whole body with `CalendarUpdate(blocks=...)` only when rewriting it.
- `CalendarEventHistory` shows who ticked what and when (`operator` or `agent:<session>`).
- To act when the operator finishes something, register a standing intent: the calendar announces
  `calendar checklist.completed: "<event>" block "<block>" n/n …`, `calendar event.status_changed: … planned -> done`
  and `calendar group.completed: group "<name>" …`, each once per transition. For example
  `IntentCreate(pattern="calendar checklist.completed.*Basket", action="build the next order without the bought items")`.
- An `action` block with `action: agent` puts a button on the event; pressing it sends its `prompt` with the
  event's current state to `session_id` as the operator's message. Leave `session_id` out to mean this session.
- In a connected Google, Outlook or CalDAV calendar the blocks appear as plain text after the description
  (`☐/☑` items, table rows). They stay structured here; an edit made there is kept as a separate text block.
