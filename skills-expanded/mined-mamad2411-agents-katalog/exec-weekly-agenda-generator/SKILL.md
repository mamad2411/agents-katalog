---
name: exec-weekly-agenda-generator
description: Synthesize the past week across meetings, chat, email, and calendar to generate a ranked list of 5-10 topics for the weekly leadership team meeting. Use when the user asks to prep for their leadership meeting, generate meeting topics, build the agenda, or says "prep me for Monday."
---

# Weekly Leadership Agenda Generator

Surface the highest-value topics from the past week for the weekly leadership team meeting. The goal is to replace memory-based prep with a systematic sweep of every signal source, so nothing falls through the cracks.

This is **not** a meeting-minutes generator or a status report. It is a decision-and-discussion agenda optimized for:

- topics that need the full leadership team (not 1:1s)
- items that are specific and traceable to this week's activity
- forced ranking so the meeting stays tight

## Setup

Fill in once (or let the agent ask):

- `[LEADERSHIP TEAM]` — a roster of who's in the room and the domain each owns (e.g., "Alex — Product/Eng, Sam — Revenue, Priya — People, Jordan — Finance"). Used to tag which domains each topic touches and to route single-domain items to 1:1s.
- `[MEETING NOTES TOOL]` — where meeting notes/transcripts live (Granola, Fathom, Otter, Fireflies, etc.)
- `[EMAIL]` — your sent-mail, as a signal source
- `[CHAT]` — your team chat (Slack, Teams), as a signal source
- `[AI CHAT HISTORY]` (optional) — transcripts of your own AI/agent sessions from the week, if you keep them. Often where the deepest thinking happens.

The skill degrades gracefully: if a source isn't available, flag it and keep going with the rest.

## When to Use

- The evening before or the morning of the weekly leadership meeting
- When the user says "prep for the leadership meeting," "what should I raise," "build the agenda," or "prep me for Monday"

## Workflow

Copy this checklist and work through it:

```text
Weekly Leadership Agenda Progress
- [ ] Step 1: Find last week's leadership meeting notes
- [ ] Step 2: Pull meetings from the past week
- [ ] Step 3: Pull sent email from the past week
- [ ] Step 4: Pull chat activity from the past week
- [ ] Step 5: Scan AI chat history from the past week (optional)
- [ ] Step 6: Extract candidate topics from all sources
- [ ] Step 7: Filter, score, and rank the top 5-10 topics
- [ ] Step 8: Format and present the agenda
```

## Step 1: Find Last Week's Leadership Meeting Notes

From [MEETING NOTES TOOL], find the most recent prior leadership meeting. Extract:

- **Decisions made** — done; don't re-raise unless implementation stalled
- **Action items assigned** — carry-forward candidates
- **Open threads** — discussions that ended without resolution or were deferred
- **Topics tabled** — anything punted due to time

Label all carry-forward items clearly in the final output. They get automatic inclusion in the candidate list.

## Step 2: Pull Meetings From the Past Week

Pull summaries for the week's meetings. For meetings with leadership-relevant signal, go into the transcript for detail.

Look for:

- Decisions that need leadership ratification or awareness
- Cross-functional issues that surfaced in multiple meetings
- Blockers or risks that require leadership intervention
- Strategic shifts or new information that changes priorities
- Alignment gaps (disagreements, unclear ownership, competing priorities)
- Personnel or org issues that need leadership awareness
- Wins worth celebrating

Skip: routine 1:1 status updates, scheduling logistics, single-domain topics already handled.

## Step 3: Pull Sent Email

Scan sent mail from the past 7 days. Look for:

- Emails escalating or flagging an issue to multiple leaders
- External communications leadership should know about (board, investors, key customers, press)
- Strategic decisions communicated that need broader alignment
- Replies signaling a change in direction or priority

Skip: scheduling, short acknowledgments, routine approvals.

## Step 4: Pull Chat Activity

Fetch recent messages the user sent or participated in. Focus on substantive threads, not reactions or one-liners.

Look for:

- Cross-functional debates or escalations
- Threads where the user weighed in on a product, strategy, or org question
- Threads involving multiple leaders (strong signal for full-team relevance)
- Urgent issues raised in chat that lack a clear owner or resolution
- FYI-level updates the leadership group should be aware of

Skip: social channels, short acknowledgments, HR/legal-sensitive threads.

## Step 5: Scan AI Chat History (Optional)

If the user keeps transcripts of their AI/agent sessions, scan the last 7 days for:

- Strategic analysis or decision-framing the user worked through
- Data pulls or analyses that revealed something leadership should see
- Issues the user spent significant time on (time invested = importance signal)
- Hiring, org design, or people topics processed

This is often where the deepest thinking happens. Mine it carefully.

## Step 6: Extract Candidate Topics

Cast a wide net. For each source, pull out anything that could be a leadership topic. Capture:

- The raw issue or signal
- Which source(s) it came from
- Which domain(s) it touches (map against [LEADERSHIP TEAM])
- Whether it's a carry-forward from last week

Aim for 15-25 raw candidates before filtering.

## Step 7: Filter, Score, and Rank

### Filter First

Remove any topic that:

- **Only involves one leader's domain** and can be handled in a 1:1. Not worth full-team time.
- **Is generic or standing** (e.g., "review metrics"). Every topic must trace to something specific that happened this week.
- **Is already resolved.** Don't re-raise a made-and-communicated decision unless implementation is off track.
- **Is HR/legal-sensitive** and shouldn't go to the full group. Flag separately for offline handling.

### Score Remaining Topics (1-5 each)

- **Cross-functional reach:** How many domains does this touch? 2+ domains score highest.
- **Urgency:** Is there a deadline? Topics with deadlines in the next few days get a 5 and a deadline marker.
- **Impact:** How much does this matter for direction, revenue, product, or team? Strategic and customer-impacting issues score highest.
- **Unresolved tension:** Active disagreement, unclear ownership, competing priorities? These are the highest-leverage topics because only the full team can resolve them.

Composite = reach + urgency + impact + unresolved tension.

### Rank and Cut

- Keep the top 5-10.
- If more than 10 survive, force-rank and cut.
- Still-open carry-forwards from last week get automatic inclusion (but are still ranked).
- Cross-cutting signals (topics that appeared in 2+ separate conversations) get a ranking boost.

## Step 8: Format and Present

```text
# Weekly Leadership Agenda — [date]

Sources scanned:
- [X] meetings reviewed
- [X] sent emails scanned
- [X] chat threads reviewed
- [X] AI chat sessions scanned
- Last week's meeting: [found/not found], [X] carry-forwards identified

---

## 1. [Topic Title]

**Treatment:** discuss | inform | decide | follow-up
**Involves:** [Leader name(s) / domain(s)]
**Source(s):** [Meeting name, chat thread, email, transcript — be specific]
[CARRY-FORWARD] — if from last week
[DEADLINE: date] — if time-sensitive
[CROSS-CUTTING] — if surfaced in 2+ conversations

**Why it matters / why now:**
[2-3 sentences. Be specific about what changed or what is at risk.]

**Suggested framing:**
[What to say or ask to open the topic. 1-3 sentences in the user's voice.]

---

[Repeat for each topic]

---

## Below the Cut
[Topics that didn't make the top 10, one line each, so the user can override the ranking]

## 1:1 Candidates
[Important but single-domain topics — better handled in a 1:1. List with the relevant leader so they can be routed.]
```

### Treatment Definitions

- **discuss:** Needs group input. The user opens the topic and facilitates.
- **inform:** FYI only. Context shared, no discussion unless someone flags a concern.
- **decide:** Needs a call. The user frames the decision and the team makes it in the meeting.
- **follow-up:** Checking on a prior commitment. Quick status, not a new discussion.

## Guardrails

- **No generic standing items.** "Review metrics" is not a topic. "Q2 pipeline is tracking 15% below plan and the team disagrees on whether to adjust targets" is a topic.
- **No single-domain items in the main list.** Route them to 1:1 Candidates.
- **Max 10 topics.** If you have 12, cut harder. A short agenda with real discussion beats a packed one that becomes a status report.
- **Every topic must cite its source.** If you can't point to a meeting, thread, email, or transcript, it doesn't belong.
- **Carry-forwards and cross-cutting signals are clearly labeled.**
- **Deadline items are flagged.**
- **No confidential HR/legal items in the main list.**

## Edge Cases

- **Light week:** Still produce 3-5 topics; lean on carry-forwards and chat. A quiet week may itself be worth noting ("no escalations this week — is that good, or are we not hearing about problems?").
- **A source is unavailable:** Flag it explicitly and proceed with the rest. Don't silently skip.
- **No carry-forwards from last week:** Note it. Either last week was unusually clean, or notes weren't captured.
- **Too many high-priority topics:** If 15+ clear the cutoff, group related items into compound topics (e.g., "Q2 revenue risks" combining pipeline + pricing + churn) with sub-bullets.

## Anti-Patterns

- Don't generate a status report. This is an agenda for decisions and discussion.
- Don't include already-resolved topics unless implementation is stalled or the resolution needs ratification.
- Don't pad the list to hit 10. Five strong topics beat ten mediocre ones.
- Don't skip a source silently — flag it and explain.
- Don't invent topics. Every item must trace to a real signal from the week.
- Don't include detailed minutes or long summaries. Keep each topic tight: title, why, framing, who, source.
