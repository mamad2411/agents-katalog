---
name: sbdc-daily-meeting-prep-crm-drafts
description: Daily SBDC meeting prep and {{CRM}} draft packet for {{USER}}
---

> **Schedule:** Daily
> **Needs:** Gmail, Google Calendar, {{CRM}}, workspace files, Zoom, Drive
> **Helper scripts (yours, not included):** learnings.py

# Daily SBDC Meeting Prep + {{CRM}} Draft Packet

## Objective

Create one concise daily SBDC work packet for {{USER}} using the University of Maryland / SBDC Google account, not the FNX Pearl account. The packet should reduce context-loading before meetings and create draft {{CRM}} note scaffolds for recent meetings that still need logging.

This task is designed for a weekday morning scheduler run. It should be useful even when there are no meetings: early-exit with a short status when there is nothing to prepare or draft.

## Context Budget Rule (Read This First)

**This task runs in a single session with a finite context window.** The biggest
threat is accumulating Gmail threads, Drive documents, wiki articles, and
attendance sheets across multiple client meetings in the parent context. A day
with 3-4 meetings can easily cross the compaction threshold and trigger
autocompact thrashing — the session repeatedly compacts and reloads, burning
tokens without finishing.

**The fix: per-client research goes into an isolated subagent.** The parent
session holds only the calendar event list (small, structured) and the compact
summaries each subagent returns. It never holds raw Gmail threads, Drive
documents, attendance sheets, or wiki article text.

### Subagent isolation pattern

After Step 1 classifies meetings, for each client meeting dispatch a subagent
with these inputs: event title, date/time, attendees, client email. The subagent
performs ALL research for that meeting (attendance check, Gmail search, Drive
search, wiki lookup) and returns a **compact structured JSON** (target: under
2,000 tokens per meeting) with these fields:

```json
{
  "clientName": "First Last",
  "clientEmail": "from attendees",
  "businessName": "if found",
  "attended": true,
  "attendanceEvidence": "roster row found / no external attendee / no doc",
  "priorNoShows": 0,
  "rebooked": false,
  "meetingType": "triage | strategy | follow-up | intro",
  "isFirstMeeting": true,
  "lastInteractionSummary": "one sentence from Gmail",
  "likelyObjective": "inferred from context",
  "keyDocumentsFound": ["doc title — one line each"],
  "questionsToAsk": ["from context gaps"],
  "resourcesToHaveReady": ["from wiki + prior threads"],
  "risksOrMissing": ["what could not be found"],
  "suggestedOpening": "one sentence",
  "crmDraftReady": true,
  "evidenceReviewed": ["list of sources checked"],
  "topicsDiscussed": ["from prior meeting context"],
  "adviceGiven": ["from prior threads"],
  "clientActionItems": ["from prior threads"],
  "advisorCommitments": ["from prior threads"],
  "followUpContext": "any pending follow-up from Gmail",
  "wikiArticlesRelevant": ["slug list"]
}
```

If the subagent finds the meeting was a no-show (no external attendee on roster),
it sets `"attended": false` and returns only the no-show fields — no {{CRM}}
draft fields.

The parent uses these compact returns to assemble the full packet. It never
reads Gmail, Drive, attendance docs, or wiki articles directly.

## Step 0: Read Learnings First (Required)

**Before touching Calendar, Gmail, or Drive**, read the canonical learnings store:

```
{{WORKSPACE_ROOT}}/memory/learnings/<namespace>/*.json
```

**Do not read this file whole, do not chunk-read it, and do not burn a subagent
on it.** It exceeds the tool-result token cap and keeps growing, so a whole-file
read truncates silently. Query it with the two-stage index/detail pattern instead:

1. Run `py {{WORKSPACE_ROOT}}/learnings.py list` in `{{WORKSPACE_ROOT}}`
   (Desktop Commander `start_process`, shell `cmd`). This prints an index -
   one line per active entry as `key [namespace] first-130-chars`.
2. Scan the index and pick the entries relevant to this run.
3. Pull full text for only those with `py {{WORKSPACE_ROOT}}/learnings.py list --full KEY1 KEY2 ...`.

Useful shortcuts: `--namespace sbdc` narrows the index to SBDC entries;
`--skill sbdc-daily-meeting-prep-crm-drafts` (or `--skill sbdc-post-meeting`)
returns the full text of everything written by that task; `--grep TERM` returns
full rows matching a term.

Prioritise, in this order:

- Anything describing a mistake that must not be repeated.
- Entries in the `sbdc` namespace, and entries whose `skill` is
  `sbdc-daily-meeting-prep-crm-drafts` or `sbdc-post-meeting`.
- Entries describing how {{USER}}'s systems and connectors behave.

Each entry is one JSON file carrying every field (type, confidence, evidence, ...),
so `--grep` and `--full` return the whole record.

**If a learnings entry contradicts an assumption you were about to make, the learnings entry wins.** This step is not optional. It exists so runs stop rediscovering known issues.

## Step 1: Classify Every Client Meeting as Attended or No-Show

Do this **before** writing any prep, any {{CRM}} draft, or any follow-up email. A no-show misread as an attended session produces a fabricated counseling note, which is a compliance problem.

**The definitive test is the Google Meet attendance sheet roster.** For each client meeting, find the attendance doc in the meeting's Drive folder (titled `<Meeting Name> - <date> - Attendance`) and read it. It is a tiny file, two to four rows.

- **No attendee row from outside {{ORG}}'s email domain = the client never joined = NO-SHOW.**
- A row with a masked email (rendered like `abcd****@***.com`) is the client. External emails are always masked; addresses on {{ORG}}'s email domain appear in full. Match clients by the First name / Last name columns, not by email.

Signals that are **NOT** reliable on their own:

- **The existence of an attendance doc.** It is generated whenever {{USER}} joins the call, including when nobody else shows. Its existence proves nothing; only its roster contents do.
- **Duration.** A no-show ran 63 minutes on 2026-07-16 because {{USER}} and a colleague stayed on and used the time. Another ended after 12 minutes. Duration says nothing about attendance.
- **A missing transcript.** Sessions hosted on another advisor's Zoom (for example VBOC-hosted) leave no transcript in {{USER}}'s Drive despite occurring. Distinguish this from an *empty* transcript (header/footer only, no dialogue), which does indicate a no-show.

Corroborating signals worth checking once the roster has answered the question:

- A client email around or after the meeting time apologizing or citing a mix-up.
- A self-rebooking on the public calendar link shortly afterward.

**When a meeting is a no-show:**

- Produce **no** {{CRM}} note, **no** hours, and **no** post-meeting follow-up email.
- Do **not** emit a placeholder scaffold full of `[not found - confirm]` fields. That invites a fabricated log entry.
- Instead report it under a **No-Shows** heading with: client, date/time, whether they have no-showed before, whether they have rebooked, and whether they sent any explanation.
- Flag repeat no-shows. {{USER}}'s booking policy states that missing a meeting without notice may delay rebooking.
- If a rebooked session is on the calendar, treat it as a first substantive contact, not a follow-up.

## Account And Data Boundaries

- Use {{USER}}'s University of Maryland / SBDC Google Calendar, Gmail, and Drive context.
- Do not use `{{YOUR_EMAIL}}` or FNX Pearl calendars unless an event is clearly copied there for SBDC work.
- Treat client information as sensitive SBDC advising data.
- Do not send email, create calendar events, edit Drive files, or update {{CRM}} automatically.
- Produce drafts and checklists only.
- Do not invent missing client facts. Mark unknowns as `[not found - confirm]`.
- Use plain language, direct and warm, with data-before-opinions.

## Inputs To Review

**The Calendar scan (below) runs in the parent context — it returns small,
structured event data. Everything else (Gmail, Drive, wiki, attendance) runs
inside the per-client subagent described in the Context Budget Rule above.**

### Calendar (parent context)

Look at:

- Yesterday, today, and tomorrow in America/New_York.
- Events likely to be SBDC advising work: SBDC, UMD, eCenter, Intro, Triage, Strategy, Follow-Up, Business Assistance, MIC, client names, program meetings, TEDCO, SBA, SBIR/STTR, MBE, government contracting, manufacturing, AI co-working.

For each relevant event, capture:

- Event title
- Date/time
- Attendees
- Meeting type if inferable
- Location or video link presence
- Description notes, if available

### Gmail (subagent context only)

For each meeting/client surfaced by Calendar, the subagent searches recent SBDC/UMD Gmail for:

- The client/contact name
- Business name
- Email address (IMPORTANT: always search by the client's email address directly, not just by name — this catches returning clients and older correspondence that name searches miss. {{USER}} has 7+ years of Gmail history.)
- Recent attachments, scheduling messages, follow-up promises, intake context, pitch decks, business plans, or action items

If a name-based search returns no results, the email-address search is mandatory before marking a client as `[not found - confirm]`.

Default lookback:

- 90 days for named clients (extend to all-time for email-address searches if 90 days returns nothing)
- 14 days for program/admin meetings

### Google Drive (subagent context only)

For each meeting/client surfaced by Calendar, the subagent searches Drive for:

- Intake forms
- Business plans
- Pitch decks
- Notes/transcripts
- Prior deliverables
- Capability statements
- Financial projections
- Workshop or program files

### SBDC Wiki (subagent context only, git repo — canonical)

The subagent uses the SBDC wiki as process/reference context, read from the CANONICAL copy `{{WORKSPACE_ROOT}}/sbdc-advising/wiki/` — NOT Google Drive. As of 2026-07-28 Drive's `wiki\` is a read-only ingest inbox that lags the repo by design.

- `wiki/triage-session-framework.md`
- `wiki/strategy-session-framework.md`
- `wiki/crm-logging.md`
- `wiki/client-intake-and-policies.md`
- `wiki/client-email-templates.md`
- Relevant topic articles, such as MBE, financing, SBIR/STTR, government contracting, AI, business planning, or capital readiness

If a client name appears in the local wiki, use that article as client context. If no article exists, rely on Calendar/Gmail/Drive evidence.

## Output Format

Use this exact structure.

```
# SBDC Daily Packet - YYYY-MM-DD

## Executive Snapshot
- Meetings to prepare:
- Meetings likely needing {{CRM}} drafts:
- No-shows detected:
- Highest-risk follow-up:
- Items needing {{USER}} judgment:

## No-Shows
(Omit this section entirely if there were none. Never draft a {{CRM}} note or
follow-up email for anything listed here.)

### [Client] - [Date/Time]
- Roster evidence:
- Prior no-shows:
- Rebooked:
- Client explanation:
- Suggested handling:

## Today's Meeting Prep

### [Time] - [Client / Meeting Title]
- Meeting type:
- Business/client context:
- What appears to have happened last:
- Likely objective for this meeting:
- Key documents/evidence found:
- Questions to ask:
- Resources to have ready:
- Risks / missing information:
- Suggested opening:

## Tomorrow Look-Ahead

### [Time] - [Client / Meeting Title]
- Why this matters:
- Prep needed before tomorrow:

## {{CRM}} Draft Backlog

### [Client / Meeting Title] - [Meeting Date]
- Evidence reviewed:
- Session type:
- Draft counseling note:
- Recommended Area(s) of Assistance:
- Economic impact / milestones mentioned:
- Follow-up tasks:
- Compliance cautions:

## Follow-Up Drafts To Consider

### [Recipient / Client]
Subject:

[Draft email or short follow-up message]

## Open Questions
- [Question] - why it matters
```

## {{CRM}} Draft Rules

Draft notes should be compliant, factual, and concise. Include:

- What the client asked for
- What {{USER}} advised or likely should advise based on evidence
- Resources discussed or recommended
- Next steps assigned to client
- Next steps assigned to {{USER}}

Do not include:

- Speculation presented as fact
- Sensitive personal details unless necessary for advising compliance
- Unsupported revenue/job/loan outcomes
- Long transcripts

Use `[not found - confirm]` for any missing facts.

**Exception:** never emit a `[not found - confirm]` scaffold for a no-show. See Step 1 - no-shows get a No-Shows entry, not a draft note.

**Areas of Assistance:** `wiki/crm-logging.md` defers to "{{CRM}}'s dropdown taxonomy" but does not enumerate it, and no wiki article contains the list. Any Area of Assistance in this packet is inferred - always mark it for confirmation against the actual dropdown. Do not invent a taxonomy.

## Step D: Dispatch Post-Meeting Runs For Today (Required)

After the packet is written, schedule one post-meeting processing run per client
meeting on today's calendar, so each meeting is processed shortly after it ends
instead of waiting for a polling window.

**First, clear stale dispatches.** Call `list_scheduled_tasks` and delete every
task whose ID starts with `post-meeting-` and whose date segment is earlier than
today. One-time tasks auto-disable after firing but are not removed, so without
this the task list grows without bound.

**Then dispatch.** For each of today's meetings that looks like a client session
(external attendee from outside {{ORG}}'s email domain, and not LUNCH, Planning, Paperwork, Tag Up,
or another internal meeting), call `create_scheduled_task` with:

- `taskId`: `post-meeting-YYYYMMDD-HHMM-<short-client-slug>` using the meeting's
  end time and a short kebab-case slug of the client or business name.
- `fireAt`: the meeting's scheduled end time **plus 15 minutes**, as an ISO 8601
  timestamp with the America/New_York offset. The buffer exists because Google
  Meet transcripts take several minutes to land in Drive after a call ends.
- `description`: `Post-meeting processing for <client> (<date>)`
- `prompt`: a self-contained instruction along these lines, with the bracketed
  values filled in:

  > Run the SBDC post-meeting workflow defined in
  > `{{WORKSPACE_ROOT}}/Scheduled/sbdc-post-meeting/SKILL.md`.
  > Read that file first and follow every step in it, including Step 0
  > (read learnings) and Step 7 (save learnings).
  >
  > Scope this run to a single meeting: "[event title]", which was scheduled to
  > end at [end time] on [date]. The client attendee is [client email if known,
  > otherwise "the {{COLLEAGUE_EMAIL}} attendee on the event"]. Skip the calendar scan
  > for other meetings.
  >
  > If the meeting's transcript is not yet available in Drive, do not treat it as
  > a no-show and do not create a draft. The transcript may still be processing.
  > Instead, call `create_scheduled_task` to schedule one retry of these same
  > instructions 15 minutes from now, with the taskId suffixed `-retry1`
  > (or `-retry2` if this run is already `-retry1`), and stop. After two retries
  > with no transcript, report the meeting as "transcript never appeared" and
  > apply the no-show checks in the post-meeting skill.

Do not dispatch for meetings that have already ended by the time this task runs,
and do not dispatch for tomorrow's meetings - tomorrow's morning run covers them.

Note in the packet's Executive Snapshot how many post-meeting runs were
dispatched, so {{USER}} can see the day's automation at a glance.

## Step N: Consolidate Learnings (Required)

At the end of each run, apply the `durable-learning-protocol` skill to this run.

Identify durable learnings worth preserving - reusable insights that would save time, prevent mistakes, or capture {{USER}}'s preferences. Do not save one-off client facts, temporary statuses, or generic advice.

Before writing, check the existing store for a matching `key` and update or supersede rather than appending a duplicate. Write with Desktop Commander `write_file` in `mode: "append"`, one JSON object per line, ASCII only (no em dashes or special Unicode).

Good candidates from this task: connector quirks, Drive/Gmail/Calendar behaviors, no-show and attendance signals, {{CRM}} logging rules {{USER}} confirms, wiki gaps, and any correction {{USER}} issues on the packet.

Do not write client names, PII, or financial specifics into the learnings store.

> {{USER}} has authorized this automation to save non-sensitive durable learnings automatically when confidence and usefulness are both 8 or higher. For lower-confidence or lower-usefulness items, propose the learning in a **Learnings To Save** section at the end of the packet instead of writing it.