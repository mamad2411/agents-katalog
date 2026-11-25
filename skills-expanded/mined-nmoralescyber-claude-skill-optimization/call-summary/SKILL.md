---
name: call-summary
description: Processes call notes, transcripts, or recordings into structured summaries — extracts action items, drafts follow-up emails, generates internal CRM-grade summaries, captures objections and next steps. Make sure to use this skill whenever the user says summarize this call, process my call notes, draft follow-up from this transcript, recap this meeting, build action items from this call, capture next steps from [meeting], or describes having raw call notes/transcript that needs to be turned into structured outputs. Works with rough notes, full transcripts (Gong, Fireflies, Otter, Zoom), or audio if transcribed. Produces three outputs: customer-facing follow-up email, internal team summary, and CRM-loggable note. Do NOT use for: prepping for an upcoming call (use sales:call-prep), drafting a response to a non-call customer message (use customer-support:draft-response), generating outreach (use sales:draft-outreach), or extracting action items from email threads (handle directly). Defining characteristic: "input is call notes or transcript, output is structured artifacts."
---

# Call Summary

Turns raw call notes/transcripts into structured action items, follow-up emails, and CRM summaries.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Input is call notes, transcript, or recording | Prepping for an upcoming call → `sales:call-prep` |
| Output needs to be customer follow-up + internal summary | Drafting a non-call customer reply → `customer-support:draft-response` |
| Capturing objections, commitments, next steps | Drafting cold outreach → `sales:draft-outreach` |
| Logging activity in CRM | Extracting action items from email → handle directly |

## Three outputs from one input

This skill produces three artifacts simultaneously, because every call needs all three:

### 1. Customer-facing follow-up email
For sending to the customer/prospect within hours of the call. Reinforces what was discussed, locks in commitments.

```
Subject: [Specific topic] — recap and next steps

Hi [Name],

Thanks for the time today. Quick recap and next steps so we're aligned:

What we discussed:
- [Key point 1]
- [Key point 2]
- [Key point 3]

What you'll do:
- [Action they own, with deadline if discussed]

What I/we'll do:
- [Action you own, with deadline]
- [Action you own, with deadline]

Next touchpoint:
- [Date, format, agenda]

[Anything else they specifically asked for — link to resource, intro, doc, etc.]

Best,
[Your name]
```

Length: under 150 words. Direct. Names actions, not feelings.

### 2. Internal team summary
For Slack channel, project tracker comment, or team email. Different audience than the customer email.

```
**[Customer/Prospect Name] call recap — [Date]**

**Attendees:** [their side] / [our side]

**Stage / context:** [where this fits in the deal/relationship]

**Key takeaways:**
- [Insight 1 the team should know]
- [Insight 2]
- [Insight 3]

**Decisions made:**
- [What was agreed]

**Open questions / risks:**
- [Things that need follow-up]
- [Risk signals to watch]

**Action items (owned):**
- [Person]: [action] by [date]
- [Person]: [action] by [date]

**Next touchpoint:** [Date / format]

**Mood:** [Positive / Neutral / Concerning — with brief why]
```

### 3. CRM activity log
Short, structured, searchable. Fits in the "log activity" field most CRMs have.

```
[Date] [Type: Demo/Discovery/Negotiation/QBR/etc.] - [Duration]

Attendees: [Names + roles]

Outcome: [Advanced / Held / Stalled / Lost]

Key points:
- [Bullet]
- [Bullet]
- [Bullet]

Next step: [Specific, with date]

Risks: [If any]

Tags: [#topics, #competitors, #features-discussed]
```

## Extraction taxonomy

For every call, extract these signals:

### Decisions made
Things explicitly agreed during the call. Use exact language. "We'll do X by Y" = a decision.

### Action items
Discrete tasks with explicit owners and (ideally) deadlines.

| Owner | Action | Deadline |
|---|---|---|
| [Name] | [Specific verb + object] | [Date or "TBD"] |

If no owner was named, flag it: "Owner unclear — needs assignment"

### Objections raised
Concerns the customer/prospect voiced, even if you addressed them. Track these for pattern analysis across deals.

| Objection | Their stated concern | Your response | Resolved? |
|---|---|---|---|
| Price | "Above our budget" | Offered phased rollout | Pending |
| Security | "Need SOC 2" | Sent report | Yes |

### Pain points / problems they shared
Their stated problems, in their language. These become discovery gold for future calls.

### Competitive mentions
Any competitor named. What they said. How they're being evaluated.

### Stakeholders surfaced
New people mentioned in the call. Track for org map building.

### Quotes worth saving
Verbatim customer language that captures their problem in their words. Sales gold; case study material.

### Risk signals
- Champion seemed disengaged
- New blocker appeared
- Procurement/legal mentioned for first time
- Competitor announced late
- Budget question raised
- Timeline shifted

### Positive signals
- Champion engaged and thinking out loud
- New stakeholder added (positive sign of internal champion building)
- Specific use case identified
- Pricing discussed without resistance
- Implementation timeline talked about specifically

## Cybersecurity call context (if applicable)

For security-product sales calls especially, also extract:

- **Compliance requirements** mentioned (SOC 2, ISO, HIPAA, PCI, FedRAMP)
- **Security questionnaire** discussed (CAIQ, SIG, custom — and their length)
- **Pen test requirements** (do they require one? on what cadence?)
- **DPA/BAA needs** (data processing or business associate agreement)
- **Incident history** they shared (often signals urgency)
- **Existing security stack** named (your integration story)
- **CISO involvement** stage (early CISO involvement = serious deal)

## Cadence recommendations after the call

Based on extracted signals, recommend follow-up cadence:

| Call outcome | Suggested follow-up |
|---|---|
| Strong positive momentum | Same-day follow-up email; next call within 7 days |
| Stalled / no clear next step | Same-day follow-up reframing the value; ask for next step in writing |
| Objection raised, not resolved | Same-day follow-up with specific objection-handling content |
| Lost / dead-end | Polite close-the-loop; ask permission to stay in touch quarterly |
| Internal-stakeholder commitment needed | Same-day follow-up to champion; ask for intro to other stakeholder |

## Anti-patterns

- **Verbatim transcript pasted as summary** — defeats the purpose
- **Action items without owners** — they don't get done
- **Same email to customer and internal team** — different audiences, different content
- **No mood / signal capture** — calls have texture; capture it
- **Missing next step** — every call should resolve to a specific next action
- **Sandbagging signals** — reps soften concerning signals; capture honestly
- **Verbatim customer quotes without context** — quotes need framing

## Output

For every call processed:
1. Customer-facing follow-up email (ready to send)
2. Internal team summary (Slack/team-channel ready)
3. CRM activity log (paste-ready)
4. Action item table with owners
5. Risk + positive signal flags
6. Suggested follow-up cadence
7. Anything that should chain to another skill (e.g., escalation flag → `customer-support:customer-escalation`)
