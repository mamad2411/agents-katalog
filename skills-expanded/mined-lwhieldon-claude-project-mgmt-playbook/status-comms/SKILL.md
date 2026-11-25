---
name: status-comms
description: Draft the same project status story in multiple formats - a status email, slide bullets, or a dashboard narrative - tuned to the audience. Use when asked for a status email, executive update, or slide-ready status. Usage - /status-comms audience and format, plus the data source
---

# Status Communications

Draft multi-format status communications from project data or a conversational summary of the
week. One status story, formatted for each audience that needs it.

## Step 1: Understand What's Needed

Determine from `$ARGUMENTS` and the conversation:

- **Audience:** Who is receiving this? (Client executive, internal team, steering committee, project sponsor)
- **Format:** Email, slide bullets, dashboard narrative, formal report, or all of the above
- **Source data:** CSV status file, free-text summary, or conversation context
- **Tone:** How sensitive is the current situation? Is there bad news to communicate?

If a `status-data.csv` or project notes are referenced, read them. If the `/status-report` skill
already produced a report this session, build from it rather than re-deriving the status.

## Step 2: Assess and Summarize Status

Before drafting, synthesize:

- Overall RAG status (🔴 Red / 🟡 Amber / 🟢 Green) with specific rationale. Present it as a
  proposal for the delivery lead to confirm.
- Key wins this period
- Active risks or issues and their trajectory (getting better, stable, getting worse)
- Notable upcoming milestones in the next 2 weeks

## Step 3: Draft in the Requested Format(s)

### Email Format
Professional status email suitable for forwarding to client stakeholders.

Subject line: `[Project Name]: Week [#] Status Update | [RAG Status]`

Structure:
- Opening sentence: overall status and one-line summary
- Accomplishments: 3 to 5 bullets
- Upcoming: 3 to 5 bullets with dates
- Risks/Issues: brief table or 2 to 3 bullets
- Actions needed from client: explicit asks, if any
- Closing

### PowerPoint / Slide Format
Short bullets optimized for a status slide:
- Overall: [RAG]: [one-line rationale]
- Accomplishments: 3 to 5 bullets (10 words or fewer each)
- Next 2 weeks: 3 to 5 bullets with dates
- Key risks: 2 to 3 bullets with owner
- Actions: table with Action | Owner | Due Date

If the user wants an actual `.pptx` or `.docx` file rather than bullets, Claude's built-in
document skills can build one from this content when they are available in the session.

### Dashboard / Narrative Format
2 to 3 paragraph narrative suitable for a project management dashboard or executive briefing note.

Every format ends with: *Drafted with Claude Code on YYYY-MM-DD; reviewed by [NAME]*

## Handling Bad News

When status is 🔴 Red or the situation is sensitive:

1. Lead with facts, not apologies
2. State the issue clearly in the first sentence
3. Immediately follow with: what caused it, what is being done, and by when the situation will be resolved or re-assessed
4. Avoid hedging language such as "we believe," "hopefully," or "it seems." Replace with direct statements or explicit uncertainty: "we do not yet know X; we will have an answer by [date]"

Bad news delivered by a person is a competence signal. Delivered only by a document, it reads as
a complaint. Draft the message; recommend the delivery lead deliver it in person or by call
first, with the written version as the record.

## Tone Calibration

| Audience | Tone | Lead With |
|---|---|---|
| C-suite / Board | Concise, decisive | Bottom line, then evidence |
| Project sponsor | Direct, collaborative | Status + what you need |
| Internal team | Frank, action-focused | Issues + next steps |
| Client PM | Professional, detailed | Accomplishments + risks |
