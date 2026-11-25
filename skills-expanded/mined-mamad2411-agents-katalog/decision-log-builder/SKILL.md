---
name: decision-log-builder
description: Build a structured decision log from emails, meetings, and Teams messages. Use when user asks to "log decisions", "track decisions", "what did we decide", "what we agreed", "why was this decided", "decision history", or "build a decision log". Do NOT use for action item extraction (use meeting-intel), open question tracking, or general meeting summaries.
cowork:
  category: analysis
  icon: TaskListLtr
---

# Decision Log Builder

Build a structured decision log from the user's communications by identifying finalized decisions and capturing context, owners, and rationale.

## When NOT to Use

- Action item extraction from a single meeting — use `meeting-intel`
- General daily/weekly summaries — use `daily-briefing`
- Open questions or unresolved debates — this skill only captures *finalized* decisions
- Drafting a decision memo for stakeholders — use `stakeholder-comms`

## Workflow

1. **Confirm the review period.** If the user did not specify one, default to the last 30 days and tell them. Ask only if they push back.

2. **Search in parallel across sources** using `SearchM365` with `sources=["email", "teams"]` and `ListCalendarView` for meeting subjects/bodies. Use decision-language queries:
   - "we decided"
   - "agreed to"
   - "confirmed"
   - "final call"
   - "going with"
   - "approved"
   - "signed off"
   Pull recent results from each source. Paginate via `next_link` when "all decisions" is requested.

3. **Filter to real decisions.** Include only items that establish direction or finalize an outcome. Exclude:
   - Opinions, preferences, or suggestions
   - Open discussion threads with no resolution
   - Proposals still awaiting approval
   - Status updates that reference past decisions without making new ones

4. **For each decision capture:**
   - **Date** — closest available timestamp (message sent date, meeting date)
   - **Decision** — one-sentence statement of what was decided
   - **Participants** — who was in the conversation, if identifiable
   - **Rationale** — only if explicitly stated; do not infer
   - **Owner** — person accountable for execution, if identifiable
   - **Source** — alias link to the originating email/meeting/chat (e.g., `[msg_3]`, `[evt_7]`, `[chat_2]`)

5. **Deduplicate.** If the same decision appears across multiple sources (e.g., a meeting and a follow-up email), group them under one entry and merge sources.

6. **Flag risk items.** Mark decisions that:
   - Have no clear owner → flag as **"No owner"**
   - Show conflicting direction across sources → flag as **"Conflict — review needed"** with both source links

7. **Handle empty results.** If no decisions are found, say so plainly and summarize the closest near-decisions (open proposals, items pending sign-off) with source links.

8. **Output format:**
   - A structured table: **Date | Decision | Owner | Source**
   - Followed by a **Key Themes & Risks** section (3–5 sentences) highlighting patterns, ownership gaps, or conflicting directions

## Guardrails

- **Ground every entry in a source.** Each row must trace to a specific email, meeting, or chat — link via alias brackets.
- **Do not fabricate rationale or owners.** If not stated explicitly, leave blank or mark "Not stated".
- **Respect privacy.** If a decision appears in a `private` or `confidential` event, omit the subject and note "Private meeting" instead.