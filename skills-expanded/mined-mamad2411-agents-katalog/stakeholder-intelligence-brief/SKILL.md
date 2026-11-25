---
name: stakeholder-intelligence-brief
description: |
  Prepare a two-minute stakeholder briefing from recent email and Teams history.
  Reviews the last 90 days of communications with a specific person and produces
  a structured snapshot of commitments made, open/unresolved items, and observable
  communication patterns — based only on visible signals, no inferred intent.

  Use when user asks: "prep me for my meeting with [person]", "brief me on
  [person]", "stakeholder context for [person]", "what's my history with
  [person]", "relationship history with [person]", "get me up to speed on
  [person] before our meeting", "what have I committed to [person]", "what's
  open with [person]", "stakeholder briefing", "two-minute brief on [person]".

  Do NOT use for: scheduling meetings (use schedule-meeting), preparing for
  a specific meeting's agenda from a transcript (use meeting-intel), or
  drafting messages to the person (use stakeholder-comms).
cowork:
  category: productivity
  icon: PersonInfo
---

# Stakeholder Intelligence Brief

Produce a concise, evidence-based briefing on a single stakeholder using only
the user's own email and Teams history from the last 90 days.

## Workflow

### 1. Resolve the person
- If no name was provided, ask once: "Who would you like the briefing on?"
- Resolve the name via `SearchPeople` / `GetUserDetails`.
- If multiple plausible matches exist (common name, multiple directory hits),
  list the top candidates with job title and email and ask the user to pick.
  Do not guess.

### 2. Gather communications (in parallel)
Run these lookups concurrently — they are independent:

- `SearchM365(sources=["email"], from_user="<resolved email>", after="<today - 90d>")`
- `SearchM365(sources=["email"], query="to:<resolved email>", after="<today - 90d>")` — for messages the user sent to them
- `ListChatMessages(person="<resolved name or email>", since="<today - 90d>", top=50)`
- Optionally `SearchM365(sources=["teams"], from_user="<resolved email>", after="<today - 90d>")` for channel mentions

Paginate with `next_link` if the user has dense history with this person.

### 3. Extract signals
From the retrieved messages, identify:

- **Commitments made**: things the user said they would do ("I'll send…",
  "I'll get back to you on…", "we'll have that by…"). Cite the message
  and date.
- **Open asks / unresolved threads**: questions or asks from the stakeholder
  that have no visible reply, or threads where the user said "I'll follow
  up" without a later resolution.
- **Incomplete follow-ups**: items where the user promised a deliverable
  whose due date has passed with no closing message.

### 4. Observe communication patterns
Report only what is directly visible:

- **Frequency**: rough cadence over the 90-day window (e.g., "weekly", "burst
  in March then silent")
- **Response gaps**: longest stretch without exchange, and any messages from
  the stakeholder still unanswered
- **Urgency / escalation language**: presence (not interpretation) of phrases
  like "urgent", "ASAP", "escalating", "please advise". Quote them; do not
  infer mood.

Do NOT speculate about intent, sentiment, or relationship health beyond the
observable signals.

### 5. Handle thin data
If fewer than ~5 messages exist across the 90-day window, say so explicitly
and summarize only what is present. Do not pad the briefing.

### 6. Produce the briefing
Output as plain markdown (inline, not a file) with these sections:

- **Relationship Snapshot** — 1-2 sentences: role, how they relate to the
  user, rough cadence.
- **Commitments Made** — bulleted list with date and message link `[msg_N]`.
- **Open or Unresolved Items** — bulleted list with date and link.
- **Communication Pattern Signals** — frequency, gaps, escalation language
  (if present).

Use bracketed aliases (`[msg_3]`, `[chat_7]`) so each citation is clickable.

## When NOT to Use

- Drafting a message to the person → use `stakeholder-comms`
- Preparing a specific meeting from a transcript → use `meeting-intel`
- Scheduling or rescheduling time with the person → use `schedule-meeting`
- Performance evaluation of the person → refuse (org policy)

## Guardrails

- Ground every claim in a retrieved message; never fabricate commitments,
  dates, or quotes.
- Quote escalation language verbatim; do not characterize tone.
- If the user is the stakeholder's manager or vice versa, still report only
  observable signals — no performance judgments.
- Output is inline markdown unless the user explicitly asks for a file.