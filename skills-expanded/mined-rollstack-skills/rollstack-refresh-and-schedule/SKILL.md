---
name: rollstack-refresh-and-schedule
description: Keep a Rollstack report up to date. Refresh its data from the sources now, and set when it updates, and so is emailed, on its own. Use when the user wants a recurring report, such as a weekly business review, monthly board pack or QBR, refreshed or scheduled.
license: MIT
---

# Refresh and schedule a Rollstack report

Set up the connection first with the `rollstack-getting-started` skill. Start by reading the report with `getReport`. Its answer includes the report's `type`, its current `schedules`, `lastRunStatus`, and `running` (whether a run is going on now).

## Refresh it now

1. Call `startReportRun`. On a `SlideDeck` report, Rollstack refreshes the data from its sources, then repairs failed calculations and slides with AI. On another type, it refreshes every visualization and updates the report's file. Pass `datasheetIds` to refresh only some sources. If a run is already going on, you get that run's id with `started: false`, and nothing new starts.
2. Call `getReportRun` with the run's id. It waits up to 30 seconds, so call it again while the `status` is `running`.
3. When it ends, tell the user which datasheets or visualizations couldn't be refreshed, if any.

## Schedule it

`updateReportSchedules` **replaces** all of a report's schedules, at most 10. So:

1. Read the current schedules with `getReportSchedules`.
2. Show the user the full list you're about to set, the existing ones they want to keep included, and get their go.
3. Send the whole list.

Each schedule needs:

- `frequency`: `hourly`, `daily`, `weekly`, `monthly` or `quarterly`.
- `timezone`, such as `America/New_York`. Every time in the schedule is local to it.
- `startDate`: a local date and time written as if it were UTC. For example, `2026-11-02T09:00:00Z` means 9:00 on November 2 in the schedule's timezone.
- For `hourly`: `selectedTimes`, the times of day as `HH:mm`, such as `["09:00", "13:00"]`.
- For the other frequencies: `cronExpression`, five fields. For example, `0 9 * * 1` is every Monday at 9:00, and `0 9 L * *` is 9:00 on the last day of each month.

Rollstack checks schedules every 15 minutes, so every time must fall on `:00`, `:15`, `:30` or `:45`. An empty list removes every schedule. A scheduled run updates the whole report.

## Email it

A scheduled run emails the report to its recipients when its email is set up, unless the email's `trigger` is `none`. On a `SlideDeck` report, a run started with `startReportRun` never does. On an older report, a run of the whole report started with `startReportRun` emails it too when its `trigger` is `all`: tell the user who would get it before you start the run, and Rollstack asks them to confirm it. To set the recipients, test the email or send it now, use the `rollstack-send-report-email` skill.

## Why an update failed

`listReportRuns` lists the runs that ended, newest first, with what started each and why it failed. On an older report, `listReportSyncs` shows how each sync did and why it failed: pass the failed ones as `syncIds` to `startReportRun` to update only those.

## Limits

- Only the report's editors can change its schedules. A 403 means the user needs edit access, or the token lacks the `slide_decks:write` scope.
