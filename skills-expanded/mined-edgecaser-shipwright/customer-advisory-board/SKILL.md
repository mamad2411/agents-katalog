---
name: customer-advisory-board
description: "Designs and prepares all materials for Customer Advisory Board sessions: agenda design, discussion guides, pre-read materials, facilitation notes, and post-session synthesis templates. Ensures CAB meetings produce actionable strategic input rather than devolving into feature request sessions."
category: customer-intelligence
default_depth: standard
---

# Customer Advisory Board (CAB) Prep

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Designs and prepares all materials for Customer Advisory Board sessions: agenda design, discussion guides, pre-read materials, facilitation notes, and post-session synthesis templates. Ensures CAB meetings produce actionable strategic input rather than devolving into feature request sessions.

## When to Use

- Preparing for a quarterly or annual CAB meeting
- Standing up a new Customer Advisory Board program
- Redesigning a CAB that's become a complaint forum instead of a strategic input channel
- Synthesizing outputs from a completed CAB session

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick prep for an informal customer round-table or single-topic check-in | Define CAB Objectives, one Discussion Guide |
| **Standard** | Preparing a full quarterly or annual CAB session | All sections |
| **Deep** | Standing up a new CAB program or redesigning one that has gone off-track | All sections + member selection criteria, multi-session arc plan, CAB charter document |

**Omit rules:** At Light depth, skip Design the Agenda, Pre-Work Materials, and Post-Session Synthesis template. Produce only the strategic questions and a single discussion guide.

## Framework

### Step 1: Define CAB Objectives

```markdown
## CAB Session: [Date]

### Strategic Questions We Need Answered
1. [Question, e.g., "How is AI changing your team's workflow, and where do you still struggle?"]
2. [Question, e.g., "What would make you expand usage to additional teams?"]
3. [Question, e.g., "How do you evaluate and buy tools in this category?"]

### What This Session is NOT
- A feature request collection session
- A product demo
- A support escalation forum
- A sales opportunity

### Success Criteria
We'll know this CAB was successful if:
- [ ] We have clear signal on [strategic question 1]
- [ ] We identify [N] new insights we didn't have before
- [ ] Participants rate the session [X]+/10 on value
- [ ] We produce [N] actionable recommendations for the product team
```

### Step 2: Design the Agenda

```markdown
## CAB Agenda, [Date, Time, Duration]

### Pre-Work (sent 1 week before)
- [ ] Pre-read: [Topic context doc, 1-2 pages max]
- [ ] Pre-survey: [3-5 questions to prime thinking and gather baseline data]

### Agenda

| Time | Block | Format | Facilitator | Goal |
|---|---|---|---|---|
| 0:00-0:10 | Welcome & ground rules | Presentation | [Host] | Set expectations |
| 0:10-0:25 | Context setting | Brief presentation | [PM] | Share relevant trends/data |
| 0:25-0:55 | Discussion 1: [Topic] | Facilitated discussion | [Facilitator] | Explore strategic question 1 |
| 0:55-1:05 | Break | | | |
| 1:05-1:35 | Discussion 2: [Topic] | Small group exercise | [Facilitator] | Explore strategic question 2 |
| 1:35-1:55 | Discussion 3: [Topic] | Open forum | [Facilitator] | Explore strategic question 3 |
| 1:55-2:00 | Wrap-up & next steps | Closing | [Host] | Thank participants, preview next session |

### Ground Rules (shared at opening)
1. This is a strategic conversation, not a support session
2. All perspectives are valuable, we want disagreement
3. Chatham House Rule: insights can be shared, attribution stays in the room
4. We'll share a synthesis within [N] days
5. We commit to reporting back on what we did with your input
```

### Step 3: Write Discussion Guides

For each discussion block:

```markdown
### Discussion Guide: [Topic]

**Objective:** [What we want to learn]
**Duration:** [N] minutes
**Format:** [Full group / Small groups / Paired exercise]

#### Opening Question (5 min)
"[Broad, open question to get everyone talking]"
- e.g., "How has [trend] affected your team in the past 6 months?"

#### Core Questions (15-20 min)
1. "[Deeper question that gets at the strategic need]"
   - Probe: "[Follow-up if they stay surface-level]"
   - Probe: "[Follow-up to get specifics]"

2. "[Question that explores trade-offs]"
   - e.g., "If you had to choose between [A] and [B], which matters more and why?"

3. "[Question that tests an assumption]"
   - e.g., "We've been assuming [X]. Does that match your experience?"

#### Closing Question (5 min)
"If you could change one thing about how [product/category] works, what would it be?"

#### Facilitator Notes
- Watch for: [signals that indicate strong agreement/disagreement]
- Redirect if: [the conversation goes toward feature requests or complaints]
- Capture: [specific data points, competitor mentions, workflow descriptions]

#### DO NOT Ask
- Leading questions that pitch our roadmap
- Yes/no questions (always open-ended)
- "Would you use [feature X]?" (hypothetical, not valid signal)
```

### Step 4: Post-Session Synthesis

```markdown
## CAB Synthesis: [Date]

### Participants
| Name | Company | Role | Segment |
|---|---|---|---|

### Key Themes (ranked by strength of signal)

#### Theme 1: [Assertion, not a label]
**Strength:** [Strong / Moderate / Emerging]
**Supporting voices:** [N] of [total] participants
**Key quotes:**
- "[Quote]", [Participant, anonymized if needed]
- "[Quote]", [Participant]
**Implication for product:** [What this means for our strategy]

#### Theme 2: [Assertion]
...

### Surprises (things we didn't expect)
- [Surprise 1]: [Description and significance]

### Contradictions (where participants disagreed)
- [Topic]: [View A] vs. [View B], [what this tension tells us]

### Validated Assumptions
| Assumption | Validated? | Evidence |
|---|---|---|
| [Assumption 1] | Yes / No / Partial | [What participants said] |

### Action Items
| Action | Owner | Due Date | Report Back |
|---|---|---|---|
| [Specific action based on CAB input] | [Name] | [Date] | [Next CAB / email update] |

### Report-Back Commitment
We will share the following with CAB members by [date]:
- Summary of themes heard
- Actions we're taking based on their input
- Timeline for next session
```

## Minimum Evidence Bar

**Required inputs:** At least 2-3 strategic questions the business needs answered, a confirmed participant list (or target criteria), and context on what has changed since the last CAB (or the business context if this is the first).

**Acceptable evidence:** Prior CAB synthesis documents, product roadmap context, recent customer research findings, NPS/CSAT trends, competitive landscape shifts, strategic planning inputs.

**Insufficient evidence:** If you have no strategic questions defined and no context on what the business needs to learn, state "Insufficient evidence for CAB Objectives" and stop. Recommend running a stakeholder alignment session or the Shipwright jobs-to-be-done skill to define learning goals before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Themes, validated assumptions, and participant sentiment from Post-Session Synthesis must be grounded in what participants actually said.
- **Hypotheses:** Discussion Guide questions and anticipated themes may be speculative, label pre-session assumptions as "To be validated during session."

## Output Format

Produce a CAB Preparation Package with:
1. **Objectives & Success Criteria**, what we need to learn
2. **Agenda**, timed, formatted, with facilitator assignments
3. **Discussion Guides**, question flows with probes and facilitator notes
4. **Pre-Work Materials**, pre-read and pre-survey
5. **Synthesis Template**, ready-to-fill post-session document

**Shipwright Signature (required closing):**
6. **Decision Frame**, strategic insights surfaced and options they inform, trade-offs between competing member perspectives, confidence level with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, strategic questions not yet answered, segments or personas unrepresented in the CAB, assumptions still untested
8. **Pass/Fail Readiness**, PASS if strategic questions are defined, agenda is timed with discussion guides, and synthesis template is ready (at Light depth: PASS if strategic questions are defined and at least one discussion guide is complete); FAIL if no strategic questions exist or the session is structured as a feature-request forum
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **No strategic questions**, Without clear learning objectives, CABs become unfocused
- **Feature request forums**, Redirect tactfully: "That's great product feedback, let me capture that separately. For today, I'd love to understand the underlying need."
- **Same voices dominate**, Use small group exercises and round-robins to hear from everyone
- **No follow-through**, If you don't report back on what you did with their input, members disengage
- **Inviting the wrong people**, CAB members should be strategic thinkers, not just your loudest customers

## Weak vs. Strong Output

**Weak:**
> "Theme: Customers want better reporting."

A label, not an insight. No strength of signal, no supporting evidence, no implication.

**Strong:**
> "Theme: Current reporting forces manual export-and-reformat cycles before exec review (Strong signal, 6 of 8 participants, unprompted). Implication: embedded executive summary views could reduce time-to-insight and strengthen the champion's internal case."

Assertion-formatted theme, quantified signal strength, grounded in what participants said, with a clear product implication.
