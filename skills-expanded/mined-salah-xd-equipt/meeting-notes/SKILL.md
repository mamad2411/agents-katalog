---
name: meeting-notes
description: "Transforms raw meeting notes or transcripts into structured Notion pages with executive summary, key decisions, action items with owners and deadlines, and open questions. Use when a user has messy meeting notes, a transcript, or bullet points from a call and needs them organized into an actionable format in Notion."
allowed-tools: Read Write Glob mcp__claude_ai_Notion__notion-create-pages mcp__claude_ai_Notion__notion-search mcp__claude_ai_Notion__notion-fetch
metadata:
  author: Salah-XD
  version: "1.0"
---

# Meeting Notes

## When to Use This Skill

Use this skill when:
- A user has raw meeting notes, bullet points, or a transcript and needs them turned into a structured document
- Someone finished a call and wants to capture decisions, action items, and next steps before they forget
- A user pastes a transcript (from Otter, Fathom, Fireflies, or manual notes) and says "organize this"
- A team lead needs meeting notes sent to stakeholders in a clear, scannable format
- A user wants action items tracked with owners and deadlines in Notion

**DO NOT** use this skill for:
- Writing agendas or meeting prep documents (this skill processes notes AFTER the meeting)
- Creating project plans or SOPs from scratch (use sop-builder instead)
- General note-taking or journaling with no meeting context
- Summarizing documents, articles, or content that is not from a meeting or call

---

## Core Principle

MEETING NOTES EXIST TO DRIVE ACTION, NOT TO DOCUMENT EVERYTHING THAT WAS SAID. EVERY STRUCTURED NOTE MUST ANSWER: WHAT WAS DECIDED, WHO IS DOING WHAT, BY WHEN, AND WHAT IS STILL UNRESOLVED.

---

## Meeting Type Reference

| Meeting Type | Primary Focus | Key Sections to Emphasize |
|-------------|--------------|--------------------------|
| **Client call** | Deliverables, expectations, next steps | Action items with clear owners on both sides, deliverable deadlines, client feedback |
| **Team standup** | Blockers, priorities, ownership | What each person is working on, blockers that need resolution, handoffs |
| **Strategy session** | Decisions, owners, trade-offs | Decisions made (and rationale), options considered but rejected, assigned owners |
| **Sales call** | Objections, follow-ups, deal status | Prospect pain points, objections raised, promised follow-ups, next meeting date |
| **Kickoff** | Scope, roles, milestones | Project scope confirmation, team roles, key milestones and dates |
| **1-on-1** | Feedback, goals, blockers | Discussion points, commitments made, personal goals or concerns raised |

---

## Step 1: Understand

Read the raw notes or transcript and identify what you are working with.

1. **Accept the input** — the user will paste or provide raw notes in one of these formats:
   - Messy bullet points from a live call
   - A full transcript (automated or manual)
   - A file path to a transcript or notes document
   - A voice-to-text dump with no formatting

2. **If the user provides a file path**, read the file using the Read tool

3. **Identify the meeting type** by scanning for cues:
   - Client names, deliverables, invoices, timelines --> **Client call**
   - "Yesterday I worked on," blockers, standups --> **Team standup**
   - Options discussed, pros/cons, strategic goals --> **Strategy session**
   - Pricing, objections, demos, proposals, "next steps to close" --> **Sales call**
   - Scope, roles, project overview, "getting started" --> **Kickoff**
   - Feedback, performance, personal goals --> **1-on-1**

4. **If the meeting type is unclear**, ask the user: "What kind of meeting was this? (client call, standup, strategy session, sales call, kickoff, or 1-on-1)"

5. **Identify participants** — extract every name mentioned in the notes. If names are missing, ask: "Who was on this call?"

**GATE: Do not proceed to Step 2 until you know the meeting type and participant names.**

---

## Step 2: Extract

Pull structured information from the raw notes. Every meeting produces these five sections regardless of type.

### 2A: Executive Summary

Write 3-5 sentences summarizing the meeting. Answer:
- What was this meeting about?
- What was the main outcome or conclusion?
- What is the single most important next step?

**Write in past tense.** The meeting already happened.

### 2B: Key Decisions

Extract every decision that was made. A decision is a commitment to a specific course of action.

Format each decision as:
```
- [DECISION]: [What was decided] — Owner: [who is responsible]
```

If no decisions were made, write: "No formal decisions were recorded in this meeting."

### 2C: Action Items

Extract every task, follow-up, or commitment. Each action item MUST have three fields:

| Who | What | By When |
|-----|------|---------|
| Sarah | Send revised proposal to client | Friday Feb 21 |
| Matt | Set up staging environment | End of day Tuesday |
| Lisa | Share competitor analysis with team | Before next standup |

**Rules for action items:**
- If no owner is stated, flag it: "Owner: **TBD — needs assignment**"
- If no deadline is stated, flag it: "By when: **TBD — needs deadline**"
- **NEVER invent deadlines or owners that are not in the notes** — flag missing info instead
- Action items with both an owner and a deadline are "complete." Items missing either are "incomplete" and must be flagged

### 2D: Open Questions

List anything that was raised but not resolved:
```
- [OPEN]: Who is handling the API integration? (raised by Matt, no resolution)
- [OPEN]: Do we need legal review before launching? (mentioned but not discussed)
```

### 2E: Key Discussion Points

Summarize the major topics discussed in 2-4 bullet points each. These are not decisions or action items — they are context that stakeholders need to understand the meeting.

**Emphasis by meeting type:**
- **Client call**: Focus on client feedback, deliverable status, expectation changes
- **Standup**: Focus on blockers, progress updates, handoffs between team members
- **Strategy session**: Focus on options considered, trade-offs discussed, rationale for decisions
- **Sales call**: Focus on prospect pain points, objections, buying signals, competitor mentions
- **Kickoff**: Focus on scope boundaries, role assignments, risk areas identified
- **1-on-1**: Focus on feedback themes, growth areas, commitments

---

## Step 3: Present

Show the structured notes to the user for approval before creating the Notion page.

Present the output in this exact format:

```
## Meeting Notes: [Meeting Title]
**Date:** [date if mentioned, otherwise "Not specified"]
**Type:** [meeting type]
**Participants:** [names]

---

### Executive Summary
[3-5 sentences]

---

### Key Decisions
- [DECISION]: ... — Owner: ...

---

### Action Items

| Who | What | By When |
|-----|------|---------|
| ... | ... | ... |

**Incomplete items (need assignment):**
- [item needing owner or deadline]

---

### Open Questions
- [OPEN]: ...

---

### Key Discussion Points
**[Topic 1]**
- ...

**[Topic 2]**
- ...
```

Then ask: "Does this capture everything? I can add, remove, or revise any section before saving to Notion."

**GATE: Do not proceed to Step 4 until the user approves. Acceptable approvals: "looks good," "yes," "save it," "send it to Notion," or similar affirmative. Maximum 3 revision rounds — after 3 rounds, ask the user to specify exact changes line by line.**

---

## Step 4: Act

Create a structured Notion page with the approved meeting notes.

### 4A: Find the Right Location in Notion

1. Call `notion-search` to find an existing meeting notes database or workspace
   - Search for terms: "Meeting Notes," "Meetings," "Notes," "Standup," or the project/client name
2. If a database or page is found, confirm with the user: "I found [page/database name] in your Notion. Should I add the notes there?"
3. If nothing is found, ask: "Where in Notion should I save these? You can give me a page URL, or I can create a new page in your workspace."

### 4B: Create the Notion Page

Call `notion-create-pages` to create a page with this structure:

**Page title:** `[Meeting Type] — [Meeting Title or Topic] — [Date]`
Example: `Client Call — Acme Website Redesign — Feb 14 2026`

**Page content structure using Notion blocks:**

1. **Heading 2:** Executive Summary
   - Paragraph block with the 3-5 sentence summary

2. **Heading 2:** Key Decisions
   - Bulleted list block for each decision
   - Bold the decision label and include owner

3. **Heading 2:** Action Items
   - To-do block for each action item (these render as checkboxes in Notion)
   - Format: `[owner] — [task] — [deadline]`
   - Items with missing owner or deadline: append **(needs assignment)** or **(needs deadline)**

4. **Heading 2:** Open Questions
   - Bulleted list block for each unresolved question

5. **Heading 2:** Key Discussion Points
   - Heading 3 for each topic
   - Bulleted list for points under each topic

6. **Divider** between each major section

### 4C: Confirm Delivery

Present the confirmation:

```
Meeting notes saved to Notion.

Page: "[Meeting Type] — [Topic] — [Date]"
Location: [workspace or database name]
Sections: Executive Summary, Key Decisions, Action Items, Open Questions, Discussion Points
Action items: [X] total ([Y] complete, [Z] need owner or deadline)

Tip: Open the page in Notion to check off action items as they are completed.
```

---

## Example 1: Client Kickoff Call

**User pastes:**

```
kickoff call with acme corp today
- met with sarah (PM) and dave (CTO)
- project is website redesign, 8 pages total
- they want new design by end of march
- budget confirmed at 12k, 50% upfront
- sarah will send brand guidelines by friday
- dave wants the staging site on their servers not ours
- we talked about CMS options, went with wordpress
- need to figure out who handles content migration
- i said id send the project timeline by monday
- they mentioned maybe adding a blog later but not in this phase
```

**Step 1 — Understand:**
Meeting type: Kickoff (new project, scope, roles, timelines). Participants: Sarah (PM, Acme), Dave (CTO, Acme), user.

**Step 2 — Extract:**

**Step 3 — Present:**

```
## Meeting Notes: Acme Corp Website Redesign — Kickoff
**Date:** Feb 14, 2026
**Type:** Kickoff
**Participants:** Sarah (PM, Acme Corp), Dave (CTO, Acme Corp), [user]

---

### Executive Summary
Kickoff call for the Acme Corp website redesign project. The scope
is confirmed at 8 pages with a $12K budget and a target completion
of end of March. WordPress was selected as the CMS. The staging
environment will be hosted on Acme's servers per Dave's request.
Content migration ownership is still unresolved.

---

### Key Decisions
- [DECISION]: CMS platform will be WordPress — Owner: [user]
- [DECISION]: Staging site hosted on Acme's servers, not ours — Owner: Dave
- [DECISION]: Budget set at $12K, 50% upfront payment — Owner: Sarah
- [DECISION]: Blog is out of scope for this phase — Owner: all parties

---

### Action Items

| Who | What | By When |
|-----|------|---------|
| Sarah | Send brand guidelines | Friday Feb 21 |
| [user] | Send project timeline | Monday Feb 17 |
| Dave | Provide staging server access | **TBD — needs deadline** |

**Incomplete items:**
- Dave: staging server access has no deadline assigned

---

### Open Questions
- [OPEN]: Who handles content migration? (raised but not assigned)
- [OPEN]: Blog addition — will this be a Phase 2 project? (mentioned
  as a possibility, not decided)

---

### Key Discussion Points
**Project Scope**
- 8-page website redesign confirmed
- Blog explicitly deferred to a potential future phase

**Technical Setup**
- WordPress selected as CMS after discussing options
- Staging environment to be hosted on Acme's servers per Dave's preference

**Budget and Payment**
- $12K total, 50% upfront
- Payment terms confirmed during the call
```

User approves. Notion page created: "Kickoff — Acme Corp Website Redesign — Feb 14 2026."

---

## Example 2: Weekly Team Standup

**User pastes:**

```
standup notes 2/13

matt - working on the onboarding flow redesign, should be done by
thursday. blocked on getting final copy from marketing, pinged
them twice already.

jen - finished the payment integration tests yesterday. moving to
the checkout bug today. no blockers.

carlos - still working on the api rate limiting. found an edge case
with batch requests, needs to talk to jen about how checkout
handles retries. targeting end of week.

general - sprint ends friday. demo is monday at 2pm. everyone
needs to have their PRs merged by EOD thursday.
```

**Step 3 — Present:**

```
## Meeting Notes: Weekly Standup
**Date:** Feb 13, 2026
**Type:** Team Standup
**Participants:** Matt, Jen, Carlos

---

### Executive Summary
Weekly standup covering sprint progress. Matt is blocked on
marketing copy for the onboarding redesign. Jen completed payment
tests and is moving to the checkout bug. Carlos found an edge case
in API rate limiting that requires coordination with Jen. Sprint
ends Friday with a demo scheduled for Monday at 2pm.

---

### Key Decisions
No formal decisions were recorded in this meeting.

---

### Action Items

| Who | What | By When |
|-----|------|---------|
| Matt | Complete onboarding flow redesign | Thursday Feb 13 |
| Matt | Follow up with marketing for final copy | **ASAP — blocker** |
| Jen | Fix checkout bug | **TBD — needs deadline** |
| Carlos | Finish API rate limiting work | End of week (Friday Feb 14) |
| Carlos | Talk to Jen about checkout retry handling | **TBD — needs deadline** |
| Everyone | Merge all PRs | EOD Thursday Feb 13 |

---

### Open Questions
- [OPEN]: Has marketing received Matt's copy requests? (pinged
  twice, no response noted)

---

### Key Discussion Points
**Sprint Status**
- Sprint ends Friday, demo is Monday at 2pm
- All PRs must be merged by EOD Thursday

**Blockers**
- Matt blocked on marketing copy for onboarding flow — has
  escalated twice with no response
- Carlos needs Jen's input on how checkout handles retries
  before he can resolve the batch request edge case
```

User approves. Notion page created: "Standup — Weekly Team Standup — Feb 13 2026."

---

## Recovery and Troubleshooting

### Raw Notes Are Too Messy or Incomplete

If the notes contain fewer than 3 meaningful data points:
1. Tell the user: "These notes are thin. I can structure what is here, but the output will have gaps."
2. Ask: "Can you add any details from memory? Specifically: what was decided, who committed to doing what, and what is still unresolved?"
3. If the user cannot add more, proceed with what is available. Flag every missing field with **TBD** and note: "These notes were generated from incomplete source material."

### Cannot Identify Meeting Type

If the notes give no clues about the meeting type:
1. Default to a general meeting format (all five sections, no type-specific emphasis)
2. Ask the user: "I was not able to determine the meeting type from the notes. What kind of meeting was this?" Then re-emphasize the correct sections.

### Notion Search Returns No Results

1. Inform the user: "I could not find a meeting notes workspace in your Notion."
2. Ask: "Would you like me to create a new page, or do you have a specific Notion page URL I should use?"
3. If the user provides a URL, call `notion-fetch` with that URL to locate the correct workspace
4. If the user wants a new page, call `notion-create-pages` to create a standalone page

### Notion Page Creation Fails

1. Retry once with a simplified page structure (title + plain text body, no special block types)
2. If it fails again, **save the structured notes to a local file instead:**
   - Path: `meeting-notes-output/[meeting-type]-[topic]-[date].md`
   - Example: `meeting-notes-output/kickoff-acme-redesign-2026-02-14.md`
3. Inform the user: "Could not save to Notion. Notes saved locally at [path]. You can paste them into Notion manually."
4. **Notion failure does not block delivery** — the structured notes are the primary output

### If 3 Attempts at Any Step Fail

**Stop and deliver what you have.** Present the structured notes directly in the chat. Tell the user: "I was unable to save to Notion after multiple attempts. Your structured meeting notes are above — you can copy them directly into Notion or any document."

---

## Pre-Delivery Checklist

Before saving to Notion, verify every item:

| Check | What to Verify |
|-------|----------------|
| Meeting type identified | Type matches the content of the notes |
| All participants listed | Every name from the notes appears in the header |
| Summary is 3-5 sentences | Not a paragraph, not one line |
| Summary is past tense | The meeting already happened |
| Every decision has an owner | No orphaned decisions without accountability |
| Every action item has Who + What | Both fields present for every item |
| Missing deadlines flagged as TBD | Never invented a deadline not in the notes |
| Missing owners flagged as TBD | Never assigned an owner not in the notes |
| Open questions listed | Unresolved items are not buried in discussion points |
| Discussion points match meeting type | Emphasis aligns with the meeting type reference table |
| User approved before Notion save | Never save without explicit user confirmation |
