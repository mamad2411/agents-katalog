---
name: scope-change-control
description: "Draft a commercial change request when scope, timeline, or budget shifts mid-project — tied back to the original SoW's assumptions and dependencies. Use when the client asks for more, the brief changes, or an assumption has turned out to be wrong. Triggers: 'write a change request', 'draft a CR', 'the scope has changed', 'handle this new ask', 'client wants to add'."
---

## Scope Change Control

Turn a mid-project scope change into a clean, commercially watertight change request. The document names what's changing, why, what it costs, what it moves, and which original assumption or dependency has triggered the change.

The point is not to say "no". The point is to make saying "yes" safe.

### Why this exists

Most agencies lose money on scope changes they never charged for. Not because they wanted to give the work away, but because the change happened in a Slack message on a Tuesday afternoon and nobody stopped to ask "is this in scope?"

A good change request does two things. It confirms *that* the work is additional — and it does so by pointing to the specific assumption, dependency, or exclusion in the original SoW that this change breaks. That's what makes it defensible. Without that link, every change request is just a fresh price negotiation.

### The framework

Every change request answers five questions:

1. **What's changing?** — concrete description of the new work or shift
2. **Why is it a change?** — which SoW assumption, dependency, or exclusion does this break
3. **What does it cost?** — fees, media, third-party, plus a contingency line if the change is fluid
4. **What moves?** — impact on critical path, launch date, and any downstream deliverables
5. **What needs to be decided, by whom, by when?** — a named decision point, not an open-ended email thread

### When to use

- The client has asked for something that wasn't in the original SoW
- An assumption has turned out to be wrong (e.g. assets aren't available, approval SLAs have slipped)
- A dependency is running late and requires a scope trade-off to hold the launch date
- You're renegotiating scope mid-project for any reason

### When not to use

- The change is trivial (sub-day effort, no critical path impact) — absorb it, log it, move on
- The change is so big it's actually a new project — start a new SoW, don't stretch the old one
- You don't have a signed SoW to change against — you have a pricing conversation, not a change request

### Prompt

```
# ROLE
You are a senior digital project manager and commercial operator with 10+ years of experience writing and negotiating change requests inside marketing, advertising, and digital agencies. You are known for change requests that are fair, specific, and defensible — they point to the original SoW, they price honestly, and they protect the agency without poisoning the client relationship.

You think like a commercial operator, not a bureaucrat. You don't use change requests to punish clients for changing their mind — you use them to keep everyone honest about what's been agreed and what's new.

# OBJECTIVE
Draft a change request for the scope change described below. The document must be specific to this engagement, tied back to the original SoW, and commercially watertight.

# INPUTS

## Original Scope of Work
<<<
{{PASTE_SOW_HERE}}
>>>

## Change Request Trigger
<<<
{{PASTE_DESCRIPTION_OF_CHANGE_HERE — what the client has asked for, what assumption has broken, what dependency is late, or what new requirement has emerged}}
>>>

## Additional Context (optional — fill in if known)
- Current project status: {{E.G. PHASE 2 OF 4, LAUNCH IN 3 WEEKS, POST-LAUNCH SUPPORT}}
- Commercial model: {{E.G. FIXED FEE, T&M, RETAINER, % OF MEDIA}}
- Client relationship context: {{E.G. UNDER PRESSURE, RECENTLY RENEWED, LEGAL-HEAVY}}
- Agency commercial constraints: {{E.G. CANNOT MOVE LAUNCH, CREATIVE TEAM AT CAPACITY, MARGIN ALREADY TIGHT}}

# METHOD — THINK IN STEPS

Step 1 — Link the change back to the SoW
- Identify which specific In Scope item, Out of Scope item, Assumption, or Dependency in the original SoW this change breaks or extends.
- Quote the original wording verbatim. This is what makes the change request defensible.

Step 2 — Quantify the delta
- Effort delta: new effort required (in person-days by role).
- Duration delta: impact on critical path and launch date.
- Cost delta: fees, media, third-party, plus contingency if the change is still fluid.
- Quality delta: any trade-offs in what gets delivered (e.g. reducing revision rounds elsewhere to hold the launch date).

Step 3 — Identify the options
- Present the client with at least two options where reasonable:
  1. Accept the change at the stated cost/timeline impact
  2. Reject or defer the change (and what that means)
  3. Optional: a trimmed version of the change at a lower cost/timeline impact
- The goal is a decision, not a negotiation.

Step 4 — Name the decision point
- Who needs to decide (named role, not "the client").
- By when (specific date — usually tied to when the next task on the critical path starts).
- What happens if no decision is made by then.

# OUTPUT FORMAT

Produce the output in clean Markdown, under 500 words in the main document. Use British English, DD/MM/YYYY dates, £ for currency.

## Change Request: {{SHORT TITLE}}

**Project:** {{PROJECT_NAME}} | **Date raised:** {{DD/MM/YYYY}} | **Raised by:** {{PM NAME / ROLE}}

### 1. What's changing
1–2 sentences describing the change, in plain language the client will recognise.

### 2. Why this is a change
The specific In Scope item, Out of Scope item, Assumption, or Dependency in the original SoW that this change breaks or extends. Quote the original wording.

### 3. Impact
- **Effort:** {{Person-days by role, or fee impact if fixed}}
- **Schedule:** {{Days added to critical path / impact on launch date}}
- **Cost:** {{£ total, broken down: agency fees / media / third-party}}
- **Quality trade-offs (if any):** {{E.g. reduced revision rounds elsewhere, MVP scope on another feature}}

### 4. Options
1. **Accept:** {{One-line consequence}}
2. **Reject/defer:** {{One-line consequence}}
3. **Trimmed version (if applicable):** {{One-line description + consequence}}

### 5. Decision needed
- **Decision owner:** {{Named role}}
- **Decision needed by:** {{DD/MM/YYYY}}
- **If no decision by that date:** {{Default action — usually hold the critical path and defer the change}}

---

### Authorisation
*Signature or written approval from the named decision owner.*

# CONSTRAINTS
- Hard limit: under 500 words for the main change request (excluding signature block).
- Every cost and schedule figure must be defensible. If you need to assume, state the assumption.
- The "Why this is a change" section must reference the original SoW directly. If you can't quote the SoW, the change request is weak.
- Plain language. No agency jargon. The client will read this.
- Use UK English spelling and DD/MM/YYYY date format.

# HONEST LIMITATIONS

After the main output, in a separate `## Reviewer Notes` section, flag:
- Cost or duration figures that are best-guesses rather than confident numbers, and who should validate them.
- Any commercial concerns (margin, relationship, precedent) that should be raised internally before sending to the client.
- Any legal or contractual implications (IP, liability, indemnities) that need sign-off before sending.
- Anything a human Account Director should pressure-test before this leaves the agency.
```

### Output you should expect

A short, structured change request (under 500 words) tied explicitly back to the original SoW, with options, a named decision point, and reviewer notes flagging the items to sense-check internally before sending.

### What to do with it

1. Sense-check internally with your Account Director and Delivery Lead. The reviewer notes tell you where to look hardest.
2. Send to the named decision owner. Don't leave it in a group email thread.
3. Log it against the project, whatever the decision. A rejected change request is still a record of what was raised and when.
4. If accepted, update the SoW with the changes (or append the signed CR to the SoW pack).

### Related skills

- `scope-of-work` — the document this skill points back to
- `assumptions-and-dependencies` — for making the SoW's Assumptions and Dependencies sections tight enough to support clean change requests
- `project-time-plan` — for updating the schedule once a change is accepted
