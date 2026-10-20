---
name: crm-productivity
description: Notes, tasks, note/task targets, timeline activities, and calendar events in the CRM (Twenty). Use for logging meeting notes, creating follow-ups and reminders, linking activity to records, and reviewing what happened on an account.
---

# CRM Productivity

Read the `crm` skill first. The cardinal rule here: **a note or task that is
not targeted at a record is invisible** on that record's timeline — always
create the target link right after creating the note/task.

## Notes

1. `Create note` with `title` and `bodyV2` (rich text body).
2. `Create note targets` (plural) linking the note to every relevant record:
   each target row carries `noteId` plus exactly one of `personId`,
   `companyId`, `opportunityId` (or a custom object id field, e.g. a deal or
   family office). One note can target several records — a meeting note
   typically targets the person, their company, and the active deal.
3. Read back with `Search notes` / `Search note targets` filtered by record
   id; `Update note` to append or fix content; `Delete note target` to unlink
   without deleting the note.

## Tasks

- `Create task` with `title`, `bodyV2`, `dueAt` (ISO 8601), `status`
  (read the exact select values from the schema — typically TODO /
  IN_PROGRESS / DONE), and `assigneeId` (a workspace member id — resolve via
  `Search workspace members`, never guess).
- Link to records with `Create task targets` exactly like note targets.
- Follow-up pattern: after logging a call/meeting note, offer a task
  ("Follow up with X") due at a concrete date, targeted at the same records.
- Queries: my open tasks = `Search tasks` with
  `assigneeId[eq]:<id>,status[neq]:DONE` ordered by `dueAt`; overdue = add
  `dueAt[lt]:<now>`. `Group tasks` by status or assignee for workload views.

## Timeline activities

Timeline activities are the audit feed on each record. `Search timeline
activities` filtered by the record id answers "what happened on this
account". They are mostly system-generated; only Create/Update one when
deliberately backfilling history, and say so.

## Calendar events

- `Search calendar events` by date range or participant to review meetings;
  `Find calendar event` + `Search calendar event participants` for details.
- `Create Calendar Event` schedules a new event (title, start/end,
  participants). Confirm with the user before creating or deleting events —
  calendars may sync outward to Google/Microsoft.
- Prep pattern: upcoming meetings this week → for each participant, pull CRM
  context (`crm-records`, `crm-pipeline`) and recent notes into a brief.
