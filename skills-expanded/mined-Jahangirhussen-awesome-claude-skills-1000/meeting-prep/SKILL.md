---
name: meeting-prep
description: >
  Trigger when the user is preparing for a sales call, demo, discovery call, QBR, or any prospect or customer meeting. Also trigger for "help me prep for my call with [company]", "what should I ask [prospect]", or "build a pre-call brief."
source:
  repository: armaneker/claude-code-skills
  original_path: sales-intelligence-kit/skills/meeting-prep
  original_name: meeting-prep
status: canonical
---
# Meeting Prep

You are an expert sales strategist and executive coach. When this skill is triggered, build a comprehensive pre-call brief that turns any meeting from a fishing expedition into a structured, goal-driven conversation.

## Workflow

1. **Gather inputs** (if not already provided):
   - **Meeting type**: discovery, demo, technical evaluation, executive sponsor, negotiation, QBR, or renewal
   - **Company**: name, industry, size (paste lead brief if available from `lead-researcher`)
   - **Attendees**: name and title of each person on their side (ask if unknown)
   - **Previous context**: have there been prior meetings, emails, or demos? What was discussed?
   - **Meeting goal**: what does a successful outcome look like for *you* by end of the call?
   - **Calendar invite or notes**: paste any agenda or context they shared

2. **Build the brief** covering all sections below:

## Output Format

```
## Pre-Call Brief: [Company Name]
Date/Time: [meeting datetime]
Meeting type: [discovery / demo / eval / exec / QBR]

---

### Company Snapshot
[3–5 bullet summary: size, stage, industry, recent news, buying trigger]

---

### Attendee Profiles

#### [Name] — [Title]
- **Background**: [company tenure, previous roles, education if notable]
- **LinkedIn**: [url if known]
- **Their lens**: [what they care about in this conversation — ROI, technical fit, risk, team adoption]
- **Recent activity**: [relevant post, talk, or initiative]
- **Rapport opener**: [something genuine to reference — a post they wrote, a shared connection, a company milestone]

[Repeat for each attendee]

---

### Meeting Objectives

**Primary goal (must-achieve):**
[Specific outcome — e.g., "Confirm technical requirements and identify champion", "Get verbal commitment on timeline"]

**Secondary goals (nice-to-have):**
- [e.g., "Understand budget cycle and approval process"]
- [e.g., "Book next step before the call ends"]

**Their likely agenda:**
- [What they expect to get from this meeting]
- [Questions they're likely to ask]

---

### Discovery Questions

Tailor to meeting type. Ask max 5–7 questions per call — quality over quantity.

**Situation questions** (understand their world):
1. [Question]
2. [Question]

**Problem questions** (surface the pain):
1. [Question]
2. [Question]

**Implication questions** (expand the pain):
1. [Question — "What happens when X occurs?"]
2. [Question — "How does this affect [downstream team/metric]?"]

**Need-payoff questions** (get them to articulate value):
1. [Question — "If you could solve X, what would that mean for [metric]?"]

---

### Potential Objections & Responses

| Objection | Response |
|-----------|----------|
| [Expected objection] | [Prepared response] |
| [Expected objection] | [Prepared response] |

---

### Competitive Situation
[Is a specific competitor in the deal? What's your positioning? Key landmines to plant.]

---

### Suggested Agenda (15 / 30 / 45-min versions)

**15-min version:**
- 0:00 — Introductions + set the agenda (2 min)
- 0:02 — Their situation + key question (8 min)
- 0:10 — Your value prop / demo highlight (3 min)
- 0:13 — Next step (2 min)

**30-min version:**
- 0:00 — Intros + agenda (2 min)
- 0:02 — Discovery: situation + problem (12 min)
- 0:14 — Tailored demo or proof point (10 min)
- 0:24 — Objections + Q&A (4 min)
- 0:28 — Next step (2 min)

**45-min version:**
- 0:00 — Intros + agenda (3 min)
- 0:03 — Discovery: full SPIN sequence (15 min)
- 0:18 — Demo or solution overview (15 min)
- 0:33 — Technical deep-dive or pricing discussion (8 min)
- 0:41 — Objections, next step, and mutual action plan (4 min)

---

### Proposed Next Step
[Specific, time-bounded action to close this call with — not "I'll follow up", but "Can we schedule the technical eval for next Tuesday with your team?"]

---

### Open Questions to Resolve on the Call
- [What you don't know yet that this call should answer]
- [...]
```

## Meeting Type Variations

### Discovery Call Focus
Prioritize SPIN questions. Goal: qualify BANT (Budget, Authority, Need, Timeline) and identify the economic buyer. Don't demo until you understand the pain.

### Demo / Proof of Concept
Lead with their stated pain, not your feature list. Open: "Based on what you shared, I've set up the demo to show [specific scenario]. Let me know if this resonates." Map every feature to a business outcome.

### Executive Sponsor Meeting
Executives care about business outcomes, not features. Anchor everything to revenue impact, cost reduction, risk reduction, or competitive advantage. Have a one-page leave-behind ready.

### QBR / Renewal
Review the prior period honestly: wins, gaps, and what changed in their business. Come with renewal numbers ready and an expansion story if warranted. Listen first — their satisfaction level will show up in the first 5 minutes.

## Common Pitfalls — Avoid These

- **Going in without a goal**: if you don't know what a "successful call" looks like, you won't recognize it when it happens
- **Treating all attendees as one person**: each role has different concerns — tailor your questions and language
- **Pitching before you listen**: asking "Can I show you a quick demo?" in the first 5 minutes signals you don't care about their specific situation
- **Neglecting the next step**: "I'll send you some info" is not a next step — always book the follow-on meeting before you hang up
- **Over-preparing the deck, under-preparing the questions**: the conversation reveals more than the presentation

## Purpose
Prepare for sales calls, demos and QBRs.

## When NOT to use
- Running the meeting.

## Validation
- Brief has goal, attendees, questions, risks.

## Example
```text
Discovery call prep with 5 questions.
```
