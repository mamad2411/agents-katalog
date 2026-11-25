---
name: ili-fleet
description: Answer questions across every registered familiar project — tasks, timelines, overdue and upcoming work, project health, and the daily brief.
---

# familiar — Fleet

A **stateless query** across the projects listed in `~/.familiar/fleet.md`. It is read-only except **update**, the one
branch that changes a project, and only through `scripts/apply_change.py` after a shown batch and a yes
(`AGENTS.md` → the third declared exception). Everything else written lives in `_overview/` inside this hub.

## Context contract

- **Required context:** `~/.familiar/fleet.md` (the registry), `hub-settings.md` (this hub's categories), `brief-settings.md` (beside `AGENTS.md`, not in `_overview/`) and `_overview/digest.md`
- **Conditional context:** `_overview/frontier.md`, `next-two-weeks.md`, `health.md`, `brief-latest.md` for the branch that needs them; `~/.familiar/time-off.md` for **time off**; one named project's `5-System/Memory/status-snapshot.md`, `4-Trackers/tasks.md` or `4-Trackers/timeline.md` only when the digest cannot answer the question
- **Excluded context:** project `1-Inputs/`, `2-Drafts/`, `3-Knowledge/`, and any project not marked `included` in the registry
- **Updates:** `_overview/` only, by running the scripts, and a project's milestone, task or meeting state only through **update**; `brief-settings.md` and `hub-settings.md` → `me` only when the user asks to change a setting; `~/.familiar/time-off.md` only as **time off** says
- **Capabilities:** file-read, shell (optional). Without shell, take the manual path.
- **Completion:** every included project is accounted for — answered, or named with what was missing — and nothing is guessed

## Branches

First read `brief-settings.md`. If it has `initialized: no`, run **Setup** before anything else. If it has
`initialized: yes` but no `agenda_kinds` line, ask Setup step 4 alone, once, before answering. Then pick from the
question; with none stated, run **overview**.

- **overview** — what is active, what is overdue, what is next. Answer from `digest.md`. Put projects with the most overdue or nearest dates first, whatever their lifecycle, and say which are STALE.
- **lifecycle** — set or change a project's lifecycle (`active`, `paused`, `reference`, `closed`) when the user asks, with `python scripts/fleet_overview.py --set-lifecycle "<name>" <value>`. It edits only the registry row, after a dated backup.
- **registry** — add, include, exclude or recategorise a project when the user asks. Add: `python scripts/fleet_overview.py --discover "<folder>"` lists unregistered projects (it writes nothing); show them, and run it again with `--apply` only on a yes. Exclude or include again: `--set-included "<name>" no|yes`, which keeps the row (deleting it is the user's hand edit). Category: `--set-category "<name>" work|personal|unset`. State the change and get a yes before each write; each edits only that registry row, after a dated backup, and nothing in the project.
- **tasks** — what can be started, across projects. Answer from `frontier.md`.
- **timelines** — what lands in the next two weeks, and which projects collide or crowd a week. Answer from `next-two-weeks.md`; the collision check is yours: group dated items by week and name weeks where two or more projects both have deliverables.
- **health** — stale snapshots, unreadable projects, projects running a bundled script. Answer from `health.md`.
- **weekly** — the week-ahead brief. See **Weekly brief** below.
- **brief** — the daily brief: overdue, due soon, key dates up to six weeks out, collisions, startable work, stale data. See **Brief** below.

- **time off** — the user's own time off, which the brief shades on its timeline and flags on any milestone due then. It lives in
  `~/.familiar/time-off.md`, beside the registry, so every hub on this machine reads the same list. Asked to add one, show the
  exact line (`- YYYY-MM-DD to YYYY-MM-DD — note`, or one date for a single day) and append it only after a yes. If the file
  is missing, create it with a `# Time off` heading and that line. Remove a line only when the user names it. List: read the
  file and say which periods fall in the brief's six weeks. Then offer `python scripts/brief.py` to refresh the page.

- **update** — change milestones, tasks or meetings in one or several projects in one pass: a date moved, a deadline dropped, a task
  finished, a meeting moved or cancelled. See **Update** below.

- **setup** — first-run walkthrough, run when `brief-settings.md` has `initialized: no`. See **Setup**.

## Update

For "deadline X moved on project 1, Y is no longer needed on project 2, T12 is done". The user's words become change
lines; a script makes each change; nothing is written before the user has seen the batch and said yes.

1. **Turn the words into lines**, one per project and ID, in the format `python scripts/apply_change.py --help` shows:
   `<project> | milestone M-04 | due 2026-11-03 | reason: ...`, `<project> | milestone M-07 | status not-applicable | reason: ...`,
   `<project> | task T-12 | done` (also `reopen`, `due`, `no-date <reason>`), and a rename,
   `<project> | task T-12 | title New wording | reason: ...` (also `milestone M-04 | title ...`). Pasted lines in that
   format are used as they are. Only those changes exist here: a milestone's due, status, confirmed date or name, a task's
   done, reopen, date or name, and the meeting changes below. New rows, owners and anything in `project-context.md` are
   changes to make inside the project; say so. A rename needs a reason; a title cannot contain `|`, `**` or `—`.
   Name only projects this hub covers. Resolve a vague reference ("the CDA filing date") by reading that project's
   `timeline.md` or `tasks.md`; if more than one row fits, ask. Never guess an ID. A date move and "no longer needed" each need a reason: ask
   when none was given, and keep `|` out of it. "No longer needed" is the milestone status `not-applicable`; nothing is deleted.
   **Meetings** are edit-only, like milestones: move one date, cancel one date, end or change a series. The hub never
   creates a meeting; "add a weekly check-in" is a change to make inside that project (say so). A series is `S-nn`, a
   single meeting `X-nn`; read the project's `4-Trackers/meetings.md` (or `_overview/brief-latest.json` → `meetings`,
   whose `ref` is the ID to name) to find it, and ask when more than one fits. Every meeting line needs a reason:
   `<project> | meeting S-01 | move 2026-10-20 to 2026-10-21 [14:00-14:30] | reason: ...`,
   `<project> | meeting S-01 | cancel 2026-10-27 | reason: ...`, `<project> | meeting S-01 | end 2027-02-02 | reason: ...`
   (also `status paused|active|ended`, `time HH:MM-HH:MM`, `rule weekly:<day>`), and for a single meeting
   `<project> | meeting X-01 | move 2026-11-06 [13:00-14:00] | reason: ...` or `| cancel | reason: ...`, and a rename of
   either, `<project> | meeting S-01 | title New name | reason: ...`. One date of a
   series is two parts, "from" and "to"; "move the Tuesday check-in" means that one date, not the series. In the preview
   include any `NEW OVERLAP` and time-off note.
   **Agendas** are a short topic list for one meeting date (the date the brief shows, after any move) or a series'
   standing list, kept in the project's `meetings.md`. They need no reason; topics are split by `;`, so keep `;` and `|`
   out of a topic: `<project> | meeting S-01 | agenda 2026-10-28 | items: Action items; Timeline check`,
   `<project> | meeting S-01 | agenda standing | items: ...`, or `<project> | meeting X-01 | agenda 2026-11-04 | none: <why>`.
   "Remind me about the agenda on Monday" is `<project> | meeting S-01 | remind 2026-10-26 on 2026-10-28`: it is kept in
   this hub's `_overview/agenda-snoozes.md` only and never written to the project; the preview says hub-local.
2. **Preview.** Write the lines to `_overview/pending-changes.txt` (replace what is there), run
   `python scripts/apply_change.py preview`, and show the user the whole result in plain terms: each project, before and
   after, and any refused or unreadable line. Include the "still depends on this" and "still names it" lines: those are
   dependent milestones and snapshot or task lines that will not change yet. A milestone that other open work depends on
   is the user's call (`calendar-rules.md`: a fixed external date does not move because a predecessor slipped).
3. **Apply** only after an explicit yes to that preview: `python scripts/apply_change.py apply --yes`. If the user changes
   anything, rewrite the file and preview again. Never pass `--yes` on your own judgement.
4. **Report** each line as done or failed, from the output. Say plainly that each project's snapshot, other tracker and
   downstream milestones are not yet reconciled: its status-log says so, and the next session in that project finishes it.
   Do not edit those files from here. Then run `python scripts/brief.py` yourself, without asking: the yes to the preview
   covered the refresh, and it writes only `_overview/`. Say the page is refreshed and give the full path of `brief-latest.html`;
   if the run fails, say so and the changes stand. Every applied line is also in `_overview/change-log.md`. After any
   meeting change other than an agenda or a reminder,
   end with: update your own calendar (Outlook or Google) to match; the hub keeps notes only and syncs nothing.
5. **No script, no edit.** If the script cannot run, there is no manual path for a write: tell the user to make the change in the
   project.

## Setup

One offer at a time; wait for the answer before the next. Make no change the user has not agreed to.

0. If `~/.familiar/fleet.md` is missing, or lists no project this hub covers, ask which folder holds the
   user's familiar projects. Run `python scripts/fleet_overview.py --discover "<folder>"` (it only lists),
   show what it found, and run it again with `--apply` only on the user's yes. Offer the same for another
   folder until the user has none left. If nothing is found, say a project must be set up first and stop.
1. Run `python scripts/fleet_overview.py`, then say in two lines what this hub covers: its categories
   and how many projects were read.
2. Offer the daily brief. On yes, set `enabled: yes` in `brief-settings.md`.
3. If yes, offer a schedule. Ask for a time and days, show `python scripts/schedule.py enable --time
   HH:MM --days ... --print`, and pass `--yes` only after the user agrees to that exact entry. If they
   decline, say the brief will still be written when they open the hub.
4. Offer agenda reminders: "Remind you to set an agenda before which meetings — client, internal, both, or none?
   How many business days ahead?" (the default is 2, the most 10; time off is skipped, public holidays are not
   known). On an answer, set `agenda_kinds` and `agenda_lead_days` in `brief-settings.md`. On none or a decline, set
   `agenda_kinds: none` so it is not asked again. Say that the brief page then flags those meetings with Set agenda,
   No agenda needed and Remind me on…, applied like any other page change (**update**).
5. Every project starts as `active`. List the included projects with their snapshot dates and ask
   which, if any, are `paused` (on hold, will resume), `reference` (kept for lookup, nothing in
   progress) or `closed` (finished). For each the user names, run
   `python scripts/fleet_overview.py --set-lifecycle "<name>" <value>`. The hub owns lifecycle; it is
   a column in `~/.familiar/fleet.md`, so nothing is written to the project. Name any project the
   digest marks STALE or STALE? and say the brief will keep flagging it until it is updated or its
   lifecycle is changed.
6. Ask what name, or names, mean the user in an Owner field ("Sam", "Sam, SL"). On an answer, set `me:` in
   `hub-settings.md`; the brief's page highlights those owners. Mention that time off can be added any time
   with `/fleet` (see **time off**).
7. Set `initialized: yes`, including when the user declined every offer. Then answer the original
   question, or run **overview** if there was none.

If the shell is unavailable, skip steps 1 and 3, say so, and do the rest.

A hub with `initialized: yes` and no `agenda_kinds` line in `brief-settings.md` was set up before agenda reminders:
ask step 4 alone, once, then carry on. Until it is answered the brief behaves as `agenda_kinds: none`.

## Brief

`scripts/brief.py` writes one page, `_overview/brief-<date>.md`, and copies it to `brief-latest.md`.
The same run writes `brief-latest.json` (the same facts as data) and `brief-latest.html`, a fixed
page filled from that data that opens in any browser: urgent items first, a six-week timeline,
one card per project. Never build or edit a page yourself; the script owns it.
Its settings are in `brief-settings.md` at the hub's top level, beside `AGENTS.md`; the days and time
it runs are not, they belong to the operating system's scheduler.

- **Show** (the default): run `python scripts/brief.py --catch-up` first (it rebuilds today's brief if the
  registry's included projects changed since it was written), then read `_overview/brief-latest.md`. Its first line is
  `<!-- brief: <date> ok|failed; ...`. If the date is not today, say how old it is and offer to run it.
  If it says `failed`, show the failure line and stop: the cause is the registry, not the projects.
  Then give the full path of `_overview/brief-latest.html` as the easier view.
- **Run now:** `python scripts/brief.py`, then show `brief-latest.md`. A hand run always writes,
  whatever `enabled` says.
- **Status** (asked whether the brief is on, scheduled, or how it is set): report `enabled`, the other
  settings, and the stamp of `brief-latest.md`; do not paste the brief itself. If
  `scripts/schedule.py` exists, run `python scripts/schedule.py status` and report it as printed;
  otherwise say no scheduler is set up and the brief runs only on opening the hub (when enabled) or by
  hand.
- **Settings:** change `brief-settings.md` only when the user asks, one `key: value` line at a time. That includes
  turning agenda reminders on or off (`agenda_kinds`) or changing how early they come (`agenda_lead_days`).
- **Schedule:** `python scripts/schedule.py enable --time HH:MM --days weekdays|daily|mon,wed,... --print`
  shows the entry without applying it. Only after the user says yes to that exact entry, rerun it with
  `--yes` instead of `--print`; the same for `disable`. Never pass `--yes` on your own judgement: it
  writes outside the hub (`AGENTS.md` → the declared exception). `enable` also sets `enabled: yes`.
  Windows uses Task Scheduler (tested); macOS launchd and Linux systemd or cron are written from their
  docs but untested, so say so when scheduling there and check `status` afterwards.

The brief carries a data-age table and a stale-data section. Read them out with the dates: a brief
built from snapshots weeks old is not current, however recent its own stamp.

## Weekly brief

`scripts/weekly.py` writes the week-ahead brief: `_overview/weekly-<date>.md`, `weekly-latest.md`,
`weekly-latest.json` and `weekly-latest.html` (a fixed page, same rule as the daily one: never build or edit it).
The window is the coming Monday to Friday when run on a Friday, Saturday or Sunday, otherwise today through the
next 7 days. It lists cautions first (overdue carry-overs, at-risk, not-started and tentative items, same-day
collisions, heavy weeks, meeting clashes, time off, stale projects), then each day, then each project's open
tasks, then the dates just past the window. Settings are `weekly_*` in `brief-settings.md`; the day and time are
the scheduler's.

- **Show / run now:** read `_overview/weekly-latest.md` (first line `<!-- weekly: <date> ok|failed; window ...`); run
  `python scripts/weekly.py` first if the user asks for a fresh one. Give the full path of `weekly-latest.html`.
- **Schedule:** the same rules as the daily brief, with `--brief weekly`:
  `python scripts/schedule.py enable --brief weekly --time 12:00 --days sun --print`, then `--yes` only after the user
  agrees to that exact entry. `enable` sets `weekly_enabled: yes`. `status --brief weekly` reports it.

## Script path

1. Run `python scripts/fleet_overview.py` from the hub folder. It reads each included project's own
   scripts with `--root --json`, falls back to `scripts/bundled/` where a project's copy is missing or
   too old, and rewrites `_overview/*.md`.
2. Read the digest header. Each file is stamped with the date and every source revision it was built
   from; if the stamp date is not today, you did not just run the script — say so and run it.
3. Answer from the branch file. Open a single project file only when the digest cannot answer.

For a single project's raw numbers use `python scripts/fleet_overview.py --json` and select that
project; do not re-derive them by hand.

## Manual path

Use when the script cannot run (no shell, blocked, or errors). Say plainly that the script did not run
and why, then:

1. Read `~/.familiar/fleet.md` and `hub-settings.md`. Skip rows whose `included` is `no`, and rows whose
   `category` is not one of this hub's `categories` (unless it says `all`); name included rows with no
   category once, without reading them. A row whose path does not exist is
   reported as unreadable, not dropped.
2. Go **one project at a time**, reading only the file the question needs, and reduce each to a few
   lines before moving to the next. Do not hold several projects' trackers in context at once.
   - Status, as-of, last-updated: the header of `5-System/Memory/status-snapshot.md`
   - Lifecycle: the registry row's `lifecycle` cell (blank is active)
   - Open work: `4-Trackers/tasks.md`
   - Dates: `4-Trackers/timeline.md`
3. Apply the scripts' rules, not looser ones:
   - Only full `YYYY-MM-DD` dates count. "Early Dec" or "Q4" is listed as undated, never converted.
   - A task is on the frontier only when every blocker is cleared: `none`, `nothing`, `—`, or a task
     that is done. A blocker written in plain words is external and still blocks.
   - A milestone is overdue when its date is before today and it is not delivered.
   - A blank lifecycle is `active`. An active project whose snapshot is older than `stale_days`
     (`hub-settings.md`, default 30) or undated is STALE; say so.
4. State which numbers came from reading rather than the script, so they are not mistaken for the
   script's output.

## Rules for both paths

- Stay inside this hub's `categories`. A project in another category is not read, quoted or counted,
  even on request; say it belongs to the other hub.
- A project whose registry row says `included: no` is not read, quoted or counted, even when an older
  `_overview/` file still holds its items (one written before it was excluded). Rebuild that file with its
  script first; if the script cannot run, leave the project's items out and name it once as excluded.
- Missing data is reported as missing. Never estimate a date or a status.
- Projects with lifecycle `paused`, `reference` or `closed` are shown but their overdue items are
  informational, not alarms.
- Outside **update**, do not suggest edits to a project from here. Lifecycle and registration are the hub's, so change them here
  (**lifecycle**, **registry**).
- Report the registry's unreadable and excluded rows once, at the end, not per branch.
