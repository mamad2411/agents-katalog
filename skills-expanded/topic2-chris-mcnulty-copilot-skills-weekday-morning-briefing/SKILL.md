---
name: weekday-morning-briefing
description: |
  Compiles and sends Chris McNulty's personal weekday morning briefing — a
  single start-of-day email covering top news, location-aware weather, Boston
  sports, enterprise AI news, open threads awaiting reply, priority client
  updates, committed tasks, and today's calendar in Pacific Time.
  Use when Chris asks to "send my weekday morning briefing", "give me my weekday briefing",
  "run my weekday briefing", "start my workday", "what's on my plate today",
  "brief me for today", or "what did I miss overnight" on a workday.
  Only run if the requesting user is Chris McNulty; otherwise use `morning-briefing`.
  Do NOT use for: end-of-day wrap-ups, full inbox triage of every message,
  scheduling or rescheduling (use schedule-meeting), deep prep for one named
  meeting (use meeting-intel), or weekend catch-ups unrelated to a workday start.
cowork:
  category: productivity
  icon: WeatherSunny
---

# Weekday Morning Briefing

Chris McNulty's start-of-day briefing (CTO, Synozur). Assembles eight sections
from live sources and **sends them inline in the email body as clean, branded
HTML**. The bar: a scannable, factual, prioritized read Chris can act on in a
couple of minutes.

## Delivery

- **To:** `<Chris's primary email>` and `<briefing alias email>`
- **Subject:** `Morning Briefing — {today's date}` (e.g. `Morning Briefing — June 23, 2026`)
- **All times in Pacific Time (PT).**

### Build a normal HTML document and send it from a file

Send a well-formed HTML email. The reliable path in this tenant is to **write the
HTML to a file and send that file as the body** — passing a large HTML string
*inline* gets HTML-escaped/treated as plain text by the mail tool, which is what
collapses everything into one run-on block. The fix is the file-based send, not
exotic markup: standard semantic HTML (`<h2>`, `<p>`, `<ul>/<li>`, `<table>`)
renders correctly in Outlook/M365 mail when the body comes from a file with
`content_type="HTML"`.

1. **Build a complete, self-contained HTML document.** Include
   `<!DOCTYPE html><html><head>…</head><body>…</body></html>`. Inline all CSS
   (no external stylesheets/CDNs — many mail clients strip `<link>` and `<style>`
   in `<head>`, so put critical styling in inline `style="..."` attributes on the
   elements themselves and keep any `<style>` block minimal).
2. **Use ordinary semantic structure**, no per-line table hacks:
   - One `<h2>` per section header (e.g. `style="color:#810FFB;font-size:18px;margin:18px 0 6px;"`).
   - Bullets as `<ul><li>…</li></ul>`; short prose as `<p>`.
   - A title block at top: an `<h1>`-style title and a subtitle line
     (date · "All times Pacific").
   - **Section 8 (calendar) is a real `<table>`** with a header row
     (Time PT / Subject / With / Where) and one `<tr>` per event, bordered `<td>`s.
   - Suggested body wrapper:
     `font-family:'Segoe UI',Arial,sans-serif; color:#1a1a1a; line-height:1.5; max-width:760px;`
3. **Save the document to `output/morning-briefing-{YYYY-MM-DD}.html`.**
4. **Send the saved file as the body:**
   `SendEmailWithAttachments(to=[<Chris's primary email>, <briefing alias email>], subject="Morning Briefing — {human-readable date}", body_file_path="output/morning-briefing-{YYYY-MM-DD}.html", content_type="HTML")`.
   Pass the file path via `body_file_path` — do **not** paste the HTML into an
   inline `body` argument (that is the path that gets flattened/escaped).

### Pre-send gate (block until it passes)

- `content_type` is **HTML**.
- The body is sent via **`body_file_path`** pointing at the saved file (not an
  inline HTML string).
- The HTML is a complete document (`<!DOCTYPE>` / `<html>` / `<body>`) with
  **inline CSS** on styled elements.
- **8 section headers** (`<h2>`) are present, in order.
- The calendar is rendered as a real `<table>` with a header row and one row per
  event.
- The saved HTML artifact exists in `output/` (confirm with `Glob output/**/*`).

Note: if a future run shows the body arriving mangled despite `body_file_path`,
verify `content_type="HTML"` was actually set and re-send — do not switch back to
inline body or invent a tables-only workaround.

## Workflow

Create a task list so progress is visible. Run the independent
lookups in parallel where possible (calendar, email, Teams, web searches), then
assemble. Resolve "today" and the 24h/48h windows from the current local time
(PT); on Monday, extend look-backs through the weekend.

### Section order (all eight, in this sequence)

1. **Top News** — today's top 2-3 US or world headlines (`web_search`). One
   factual sentence each. No editorializing, no opinion.

2. **Weather** — first determine Chris's **current location**: scan recent
   `ListCalendarView` events, travel blocks, and any available
   out-of-office entries. He's based in the Pacific Northwest (Bothell, WA) but
   travels frequently — use the location implied by today's events if he's on
   the road, otherwise default to Bothell. Then `web_search` today's forecast
   for that location: current conditions, high/low, and any notable alerts.

3. **Sports** — his four Boston teams: **Red Sox, Patriots, Bruins, Celtics**.
   For each team that is **in season**: show its **last result** if it played in
   the past 24h, and its **next game** (date, time PT, opponent) if one falls in
   the next 24h. **Skip any team in its off-season.** Use `web_search`.

4. **Enterprise AI News** — the **top 5** enterprise/business AI news items from
   the past 24h relevant to a **consulting-firm CTO** (model releases, platform
   moves, M365/Copilot, governance, notable funding/M&A). One line each, with a
   why-it-matters angle. Use `web_search`.

   **Freshness gate — date-verify every item before including it. This section
   has previously been padded with stale/evergreen content; do not repeat that.**
   - Each item must carry an explicit publish/event date **within the last 24h**.
     If you cannot confirm the date, **drop it** — do not assume "recent."
   - **Reject** evergreen and roundup pages whose value isn't time-stamped:
     "AI in 2026" profile/ranking pages, "2026 enterprise guide" marketing pages,
     and **conference recaps for events that already happened** (e.g. a Build
     2026 recap is NOT today's news — check the event date, not the article's
     "updated" timestamp).
   - Prefer dated daily-digest / dated news sources; quote the date you verified.
   - If fewer than 5 genuinely-fresh items exist, **list only the real ones** and
     say so ("Quieter AI news day — 2 items in the last 24h") rather than topping
     up with background context. Honest short beats padded.

5. **Open Threads Awaiting Reply** — email + Teams from the **prior day** that
   are **genuinely waiting on Chris personally**. Use `ListMessages` (last ~24h,
   or since Friday EOB on Monday) and `ListChats` (unread) + direct mentions.

   **Addressee test — delivery ≠ being asked.** A message landing in Chris's
   mailbox does NOT mean it is addressed to him. Before listing a thread here,
   confirm Chris is an **actual intended recipient of the ask**:
   - Treat it as awaiting Chris only if he is in **To** (not just bcc'd via a
     list), OR he is **named directly**, OR he is the clear owner of the request.
   - **Exclude distribution-list / community / group-alias traffic** where the
     request is directed at a team or someone else. In particular, mail sent to
     MVP and community lists (e.g. `*@mstechdiscussions.com`, `MVP-NDA-*`,
     other DLs/aliases) is usually a question **to a Microsoft product team or
     the group**, not to Chris — do not surface it as "chasing your feedback."
   - When the recipients aren't obvious from the list view, call `GetMessage`
     and read `toRecipients` / the salutation before deciding. If the ask is
     aimed at "the team" / a product group and Chris is one of many list
     members, leave it out (or, at most, note it once under section 6 as
     community/ecosystem context — never as a personal to-do).
   - **Exclude** automated notifications, newsletters, and cold outreach.

6. **Priority Client Updates** — meaningful signals from client email and Teams
   over the **last 24-48h**: commitments, escalations, decisions, status changes.
   Prefer client domains and known engagements; skip routine chatter.

7. **Top 5 Committed Tasks** — the top 5 tasks/deliverables/to-dos across his
   task list, recent email, Teams, and active projects. Include owner/context
   and any due dates. Pull from his task list, flagged email, and explicit
   commitments surfaced in sections 5-6.

8. **Today's Calendar** — chronological, as a table: time (PT), subject,
   attendees, location. Use `ListCalendarView` (today 00:00-23:59 local).
   **Flag conflicts** (overlapping accepted events) and **back-to-back stretches**.
   Count only `accepted` events for density. Respect privacy: for
   `private`/`confidential` or personal events (Doctor, Personal, Interview),
   show only the time block as "Private appointment" — never echo the subject.

## Grounding & Quality Rules

- **Facts only.** News, weather, and sports come from `web_search` results —
  never from memory. If a search returns nothing in-window, say the section is
  quiet rather than filling the gap.
- **Respect the windows.** Past-24h for news/sports/AI/threads; 24-48h for client
  updates; today for calendar. Discard out-of-window results.
- **Surface, don't dump.** Each section is a prioritized highlight reel. Cap
  lengths; drop noise (newsletters, automated mail, cold outreach).
- **Distinguish "sent to a list Chris is on" from "addressed to Chris."** Never
  recommend Chris act on, reply to, or own a request that was directed at a
  team, product group, or distribution list — even though it sits in his inbox.
  Verify the addressee (see section 5) before turning any message into a "reply"
  item or a task.
- **Pagination:** when an email/Teams lookup returns `next_link` and the window
  isn't covered, keep paging before summarizing.
- **Privacy first** on the calendar (time-block sensitive events).

## When NOT to Use

- End-of-day wrap-up or "what did I accomplish" retrospectives.
- Full inbox triage of every message.
- Scheduling / rescheduling / finding a time → `schedule-meeting`.
- Deep prep for one named meeting → `meeting-intel`.

## Failure Handling

- **A lookup fails:** retry once. If it still fails, include the section with a
  one-line note ("Couldn't reach sports results this morning") rather than
  dropping it silently — Chris should know a source was unavailable, not assume
  it was empty.
- **No data in a window:** state the section is quiet ("Inbox is calm — nothing
  awaiting reply"). Never fabricate to fill a section.
- **Location ambiguous** (no travel signal): default to Bothell, WA and note the
  assumption in the weather line.
- **Off-season team:** omit it from Sports entirely; don't show a placeholder.
- **Send fails:** do not report success. Tell Chris the briefing was assembled
  but the email didn't go out, and surface the saved `output/` copy.

## Guardrails

- **Verify before reporting done:** confirm the saved HTML artifact exists in
  `output/` and the send succeeded before telling Chris it went out.
- **Outward send:** this skill sends an email to two fixed recipients — that is
  its intended action. Do not add other recipients without being asked.
- **No fabrication** of headlines, scores, forecasts, senders, tasks, or meeting
  details. Every claim traces to a tool result; if it isn't grounded, leave it out.
