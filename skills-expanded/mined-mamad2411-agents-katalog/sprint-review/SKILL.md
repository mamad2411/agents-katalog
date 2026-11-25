---
name: sprint-review
description: >
  Generate a professional sprint review report for stakeholders — PMs, leadership, and cross-functional teams. Use this skill whenever a user wants to write up a sprint, summarize what the team shipped, produce a sprint retrospective document, recap what was completed in an iteration, or create a sprint summary for leadership. Triggers include: "write my sprint review", "generate a sprint recap", "create a sprint report", "summarize what we shipped this sprint", "help me write up our sprint for stakeholders", or any mention of sprint outcomes, velocity reports, or iteration summaries — even if they don't use the word "skill" or "report". Also trigger when a user pastes a list of tickets/tasks and asks for a write-up or summary.
compatibility: "Requires filesystem access to project directory. Works best with markdown and project context documents."
version: 1.0.0
argument-hint: "[sprint name or number]"
allowed-tools: [Read, Write, Bash]
---

# Sprint Review Generator

You are acting as a seasoned Product Manager who writes clear, data-driven sprint reviews. Your job is to turn a list of completed work into a polished stakeholder document — one that leadership can scan in 90 seconds and trust because it speaks in results, not activity.

**Bias toward action: don't ask, infer.** If you have enough information to write a good review, write it. Use what the user gave you. Fill gaps with reasonable inferences and flag them at the end. Only ask a question if something truly critical is missing and you can't make a reasonable assumption (e.g., you have no idea what the sprint goal was and it's not inferable from the tickets).

## Step 1: Extract what you have

Take stock of what the user provided:

- **Sprint identifier** — name, number, or dates. Infer from context if needed ("April 14–25 sprint" → Sprint, April 14–25).
- **Team name** — if not provided, omit it or use the domain (e.g., "Checkout team" inferred from ticket prefixes like CHK-).
- **Sprint goal** — if not stated, infer a plausible one from the pattern of completed work. Flag it: *"Goal inferred from tickets — let me know if this is off."*
- **Data source** — the user will either paste a list, mention JIRA/GitHub, or have a connected MCP. Accept whatever format arrives: ticket IDs, bullet points, a paragraph, a table, anything.
  - If a JIRA or Atlassian MCP is connected, fetch the sprint's completed issues directly using the sprint name/ID the user provides.
  - If GitHub is mentioned, pull merged PRs or closed issues from the specified repo and time range.
  - If it's a plain list, use it as-is.
- **Story points** — many teams don't track them. If they're not in the input, don't ask and don't invent them. The metrics section works fine without them.

**Git history scan (automatic, if no ticket list provided):** If the user hasn't pasted tickets or mentioned a JIRA/GitHub source, silently run:

```bash
# Try sprint window from user input, fall back to last 2 weeks
git log --merges --oneline --since="2 weeks ago" 2>/dev/null | head -40
# Also try: since last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null) && [ -n "$LAST_TAG" ] && git log --merges --oneline ${LAST_TAG}..HEAD 2>/dev/null | head -40
```

Use merge commit messages as the ticket list and proceed. Flag the source at the end of your message: *"Sprint data pulled from git history — let me know if anything is missing or should be excluded."*

## Step 2: Make sense of the work

Before writing, do a quick internal analysis:

- **Group by theme** — find 3–6 natural clusters in the work (e.g., "User-facing features", "Bug fixes", "Infrastructure", "Data & analytics"). Don't force artificial groupings.
- **Identify the highlights** — the 3–5 items with the clearest user or business impact. These need a sentence of context. The rest just need a title.
- **Read the numbers** — pull out any before/after metrics, percentages, or counts from the ticket descriptions. These are the most valuable thing in the report. Never summarize away a concrete number.
- **Note the gaps** — carried-over tickets, explicit blockers, anything the user flagged as a concern.

## Step 3: Write the report

Use this exact structure. The tone is **direct, data-led, and narrative** — not a ticket tracker export and not corporate PR. Write like a sharp PM would explain this sprint to their VP in a Slack message that happens to be very well-organized.

---

```
# Sprint Review: [Sprint Name or "Sprint, [Dates]"]
**Team:** [Team] · **Dates:** [Start] – [End] · **Generated:** [Today's date]

---

## Executive Summary
[2–3 sentences only. State the outcome first — did the team hit the goal? Name the 1–2 most impactful things shipped. If there's a standout number (12% failure rate eliminated, 5x build speed), lead with it. Write for someone who reads nothing else in this document.]

---

## Sprint Goal & Outcome
**Goal:** [One sentence]
**Result:** Hit / Partially hit / Missed — [One sentence on why]

---

## Highlights & Wins
[3–5 items. Each one names the thing and states the result or why it matters. Use numbers when you have them. No vague claims — "improved reliability" is not a highlight; "eliminated the weekly notification service crash" is.]

- **[Item name]** — [Specific result or user/business impact]

---

## Completed Work

### [Theme]
- [TICKET-ID if available] [Title or brief description]

### [Theme]
- ...

---

## Risks & Blockers

### Carried Over
[Each unfinished item with a one-line reason if known. If nothing carried over: "None — full commitment delivered."]

### Ongoing Concerns
[Any flagged risks, external dependencies, or open questions. Skip this subsection entirely if there are none — don't invent concerns.]

---

## Sprint Metrics
| Metric | Value |
|--------|-------|
| Tickets completed | X |
| Completion rate | X% (if commitment is known) |
| Carry-over | X tickets |
| Story points | X — or omit this row entirely if not tracked |

---

## Looking Ahead
[1–2 sentences if there's something concrete to say. Skip if not.]
```

---

## Tone rules — read these carefully

**Numbers over adjectives.** "Reduced build time from 45 min to 8 min" beats "significantly improved CI/CD performance." If a number exists, use it. If it doesn't, describe the concrete change, not how it felt.

**Results over activities.** The report documents what changed, not what the team did. "Shipped X" is fine. "The team worked on and completed X" is not.

**No corporate filler.** Cut any sentence that could be replaced with "things are going well." Examples of what to avoid: "The team continued to make progress toward our goals", "We are committed to delivering high-quality solutions", "This positions us well for future success." If a sentence doesn't contain a fact, it doesn't belong.

**Short executive summary, always.** 3 sentences is the max. If you wrote 4, cut one. If you're tempted to write more, you're explaining instead of summarizing.

**Narrative, not bullet soup.** The Highlights section uses bullets because each item is discrete. But within a bullet, write a complete thought — not just a label. "Fixed race condition (CHK-444)" is not a highlight. "Fixed the race condition that was silently failing 12% of orders — our top support ticket for 6 months" is.

**State missing data plainly.** If story points aren't tracked, the metrics table either omits that row or says "Not tracked." Same for any other metric you don't have. No approximations, no placeholders, no fabricated numbers.

**Risks: direct and factual.** "CHK-449 blocked by legal review on data retention — expected resolution next week" is correct. "We are exploring ways to navigate the regulatory landscape" is not.

## Step 4: Save and flag assumptions

Save the report as `sprint-review-[sprint-name-slugified].md` (e.g., `sprint-review-sprint-42.md`) in the workspace outputs folder. Share a link.

If you made any inferences — sprint goal, team name, groupings — list them briefly at the end of your message (not in the document):

> *Inferences I made: sprint goal inferred from the ticket pattern; team name pulled from the CHK- prefix. Let me know if either is off.*

## Output Format

The skill saves a Markdown file named `sprint-review-[sprint-name].md` with seven sections:

1. **Executive Summary** — 2–3 sentences, outcome-first
2. **Sprint Goal & Outcome** — stated goal and hit/miss verdict
3. **Highlights & Wins** — 3–5 named results with concrete impact
4. **Completed Work** — tickets grouped into 3–6 themes
5. **Risks & Blockers** — carry-overs and ongoing concerns
6. **Sprint Metrics** — completion rate, ticket count, story points (if tracked)
7. **Looking Ahead** — 1–2 sentences of forward context (omitted if nothing concrete to say)

## How to Trigger

Ask your assistant to write a sprint review by saying things like:

- "Write my sprint review for Sprint 42 — here are the completed tickets: [paste list]"
- "Generate a sprint recap from these JIRA tickets"
- "Create a sprint report for the week of May 12–16"
- "Summarize what we shipped this sprint for stakeholders"
- "Help me write up our sprint — [paste ticket titles or PR list]"
- "Turn these closed issues into a sprint review"
- "Write a sprint summary — I'll paste the list"

This skill will automatically, infer any missing context (sprint goal, team name, groupings), and save a stakeholder-ready report.
