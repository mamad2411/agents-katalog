---
name: stakeholder-prep
description: Prepare for a stakeholder meeting with an agenda, talking points, anticipated objections with responses, and a follow-up email draft. Use 30 to 60 minutes before a client or executive call. Usage - /stakeholder-prep describe the meeting and who is in it
---

# Stakeholder Prep

Prepare the delivery lead for a stakeholder meeting: agenda, talking points, anticipated
objections with responses, and a ready-to-edit follow-up email. Run it 30 to 60 minutes before
the call.

## Input

`$ARGUMENTS` describes the meeting: who is attending, the purpose, and any context, for example:

```
/stakeholder-prep CFO review of project status; we are 2 weeks behind and need to discuss a scope reduction
```

Reference a project file for evidence when one exists:

```
/stakeholder-prep -- see my-projects/client/status-data.csv; meeting with CFO on the Q2 timeline
```

If the description is too thin to prepare from, ask up to three questions, then proceed.

## Output

**Meeting Objective:** one sentence describing what a successful meeting looks like.

**Suggested Agenda** (with time allocations):
- Item 1 (X min)
- Item 2 (X min)

**Key Talking Points:**
For each agenda item, 2 to 3 crisp, evidence-backed bullets. Executive audience: lead with the
bottom line, follow with supporting detail.

**Anticipated Objections / Tough Questions:**
| Question or Objection | Recommended Response |
|---|---|

Prepare for the harder questions, not the straightforward ones.

**What You Need From Them:**
- Specific decisions, approvals, or inputs. Be explicit. When asking for a decision, bring three
  options; choosing is easier than creating.

**Follow-Up Email Draft:**

Subject: [Meeting topic]: Follow-Up and Next Steps

[Opening sentence referencing the meeting]
[Summary of key decisions or agreements, 2 to 4 bullets]
[Action items table with owner and due date]
[Closing with next scheduled touchpoint]

The email is a draft. It carries the delivery lead's name, so it is not sent until they have read
it and adjusted it to what was actually said in the room.

Use a professional, confident tone.

## Example Output

**Meeting Objective:** Secure CFO approval for a 2-week timeline extension and agree on the scope reduction approach before the board update on May 15.

**Anticipated Objections:**
| Question | Recommended Response |
|---|---|
| "Why are we behind? You committed to this date." | "We hit two dependencies on client data access that weren't in the original plan. We flagged them in the Week 6 status report. Here's what we did to recover time..." |
| "What does a 2-week delay cost us?" | "Direct cost: approximately $X in additional resource time. Indirect: UAT readiness shifts to [date]. We've modeled three options; we're happy to walk through them." |
