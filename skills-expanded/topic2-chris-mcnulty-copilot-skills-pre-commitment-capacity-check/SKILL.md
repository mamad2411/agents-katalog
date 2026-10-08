---
name: pre-commitment-capacity-check
description: |
  Before committing to a new engagement, SOW, project, or ask, review actual
  workload and flag capacity risks across calendar, sent email, and Teams.
  Reads the referenced SOW or proposal if one exists (docx, pdf, xlsx) to
  extract hours, roles, and scope. Sweeps the next 30 days of calendar, the
  last two weeks of sent email for explicit commitments, and recent Teams
  chats for open asks. Produces a recommendation with confidence score.

  Use when user asks: "can I take on [project]", "do I have capacity for
  [SOW]", "should I commit to [engagement]", "capacity check on this SOW",
  "pre-commitment check", "can I lead [project]", "should I sign this SOW",
  "am I free to take [client]", "bandwidth check", "before I agree to this",
  "is this a good time to add something".

  Do NOT use for: routine calendar review (use calendar-management), meeting
  scheduling (use schedule-meeting), morning briefings (use daily-briefing),
  or post-commitment workload rebalancing.
cowork:
  category: analysis
  icon: TaskListLtr
---

# Pre-Commitment Capacity Check

Reconcile a proposed commitment against the user's real workload — calendar,
sent email, and Teams — before they say yes. Output is a recommendation with
named tradeoffs, not a binary verdict.

## When to Use

Trigger when the user is evaluating whether to take on something new: a SOW,
proposal, project, client engagement, or any ask. The user may reference a
document, or may just be asking generally ("good time to add something?").

## When NOT to Use

- Routine weekly calendar review → `calendar-management`
- Scheduling a single meeting → `schedule-meeting`
- Daily/morning workload overview → `daily-briefing`
- Already-committed projects needing rebalancing → answer directly
- Capacity for someone else → answer directly with a manual lookup

## Workflow

### Step 1 — Locate and read the engagement document (if one exists)

If the user references a SOW, proposal, or estimate, find it:
1. `Glob input/**/*` for uploaded files
2. `SearchM365` with the project/client name + "SOW" or "estimate"
3. Ask if not found

Read with `ReadFileContent` (SharePoint/OneDrive) or `Read` (local). Extract
binary office files via `python-docx` (docx), `openpyxl` (xlsx), or the `pdf`
skill. Pull the estimate/launchpad workbook separately if it exists — that's
where roles and per-activity hours usually live.

From the document, capture:
- **Total hours**, **total investment**, **elapsed duration**
- **Phases/epics** with per-phase hours
- **Roles required** — note which role(s) the user would fill
- **Deliverables** per phase
- **Scope inclusions** and **explicit exclusions**

**Scope-framing check (critical):** Compare the user's casual description to
the SOW's actual scope. Flag mismatches explicitly — e.g., user says
"redesign" but SOW says "narrative refinement" and excludes rebranding.

If no document is referenced, skip the SOW extraction and proceed to the
workload sweep — the user is asking a general capacity question.

### Step 2 — Calendar sweep (next 30 days)

Call `ListCalendarView` from today through `today + 30 days` (or
`today + elapsed_weeks + 1 buffer week` if a SOW window is known). Use
`select=subject,start,end,isOrganizer,showAs,isAllDay`. Set `top=200`.

Classify every event:

| Bucket | Signal |
|--------|--------|
| **OOF / travel** | `showAs=oof`, multi-day `isAllDay`, subject contains "Travel", "Offsite", conference names |
| **Daily focus block** | Recurring same-time block organized by user (e.g. "Calendar Block - Reveille") |
| **Recurring commitment** | Weekly/biweekly meetings |
| **Ad-hoc meeting** | One-off events |
| **Available** | Implied gaps |

Identify **full weeks blocked** (OOF or travel spanning Mon–Fri).

### Step 3 — Sent-email sweep (last two weeks)

Call `ListMessages(folder_id="sentitems", received_after=<14 days ago>,
top=100)`. Scan subject + body for explicit commitment phrases:

- "I'll handle", "I'll send", "I'll review", "I'll get back to you"
- "I'll have this by", "I can deliver", "I'll own this"
- "By [date]", "before [date]"
- "Send you a draft", "follow up with you"

For each match, capture the recipient, subject, and what was promised.
These are **committed work** the calendar may not show.

### Step 4 — Teams sweep (recent chats)

Call `ListChats(top=20)` and for chats with recent activity, pull messages
via `ListChatMessages(person=<other>, since=<10 days ago>, top=20)`. Look for:

- **Open asks** directed at the user ("can you...", "would you mind...")
- **In-progress discussions** likely to convert to work (proposals being
  shaped, problems escalating)
- **Unanswered questions** to the user

These are **likely incoming work** — not yet committed but trending toward it.

### Step 5 — Compute capacity vs. requirement

For each week in the window:

- **Blocked weeks** (OOF/travel Mon–Fri): subtract entirely
- **Partial weeks:** ~25h/week deep-work capacity, deduct daily focus blocks
  and recurring meetings
- Sum → **available hours**

If a SOW is in play: compare to required hours and match phases to available
windows. Heavy drafting needs contiguous blocks; coaching/discovery phases fit
around meetings.

### Step 6 — Recommend

Lead with one of three recommendations, calibrated per `deep-reasoning`:

1. **Take it on solo** / **good time to add something** — capacity ≥ 1.3×
   required, no critical-phase week blocks, scope matches strengths
2. **Take it on with a partner or role split** — capacity exists but
   elapsed timeline collides with travel; name which role to delegate and
   which phase fits which window
3. **Decline or defer** / **not a good time** — required hours > available,
   or critical phases fall inside blocked weeks, or sent-email/Teams sweep
   shows the next two weeks are already over-committed

State **confidence** (0–100). Below 75 → flag what would change it.

### Step 7 — Output format

Concise. Use this structure:

```
**Recommendation (confidence ~N):** [one-line verdict — good time to add /
take solo / partner-split / not a good time]

**Scope reality check** *(if SOW referenced):* [flag framing mismatch]

**Engagement** *(if SOW referenced):* Xh / $Y / ~Z weeks. Phases: [list].

**Current obligation load:**
- *Committed:* [calendar weeks blocked + sent-email promises with dates]
- *Likely incoming:* [Teams open asks + in-progress threads]

**High-capacity weeks:** [specific week-of dates already at/over capacity]

**Suggested split** *(if applicable):* [role/phase fit per available window]
```

Every line should be specific to this user's actual data — no generic
advice.

## Guardrails

- **Never guess hours or scope** — if SOW unreadable, ask before recommending
- **Travel/OOF beats optimism** — blocked weeks cannot host deep work
- **Daily focus blocks are real** — treat as committed
- **Surface scope mismatch before the capacity math** — wrong scope framing
  makes the capacity answer meaningless
- **Confidence below 75 → state what's missing** rather than asserting
- **Sent-email commitments count as work** — even if not on the calendar
- **Teams in-progress threads are signal, not noise** — flag them

## Anti-Patterns

- Generic "you're busy but it could work" answers
- Counting tentative invites as busy time (they're optional)
- Skipping the scope-framing check and going straight to hours
- Recommending without naming specific weeks/dates
- Ignoring sent-email promises because they aren't on the calendar
- Treating the SOW's elapsed-duration estimate as a hard fact when the user
  has OOF weeks inside it