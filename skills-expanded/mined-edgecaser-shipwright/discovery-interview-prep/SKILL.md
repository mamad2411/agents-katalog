---
name: discovery-interview-prep
description: "Generates comprehensive preparation materials for customer discovery interviews including interview guides, screener criteria, and debrief templates. Grounded in the Jobs-to-Be-Done methodology and \"The Mom Test\" principles."
category: discovery
default_depth: standard
---

# Discovery Interview Prep

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Generates comprehensive preparation materials for customer discovery interviews including interview guides, screener criteria, and debrief templates. Grounded in the Jobs-to-Be-Done methodology and "The Mom Test" principles.

## When to Use

- Preparing for a round of customer discovery interviews
- Training new PMs or researchers on interview technique
- Shifting from opinion-gathering to evidence-gathering conversations
- Need a structured guide to avoid leading questions

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick prep for an ad-hoc conversation or follow-up call | Interview Guide only (Warm-Up + Core Discovery) |
| **Standard** | Planned discovery sprint with recruited participants | All sections |
| **Deep** | High-stakes research (e.g., new market entry, pivoting ICP) | All sections + assumption-to-question traceability matrix, moderator notes with contingency probes |

**Omit rules:** At Light depth, skip Screener Criteria and Debrief Template. Produce only a ready-to-use question flow.

## Framework

### The Mom Test Principles

Every interview guide must follow Rob Fitzpatrick's rules:

1. **Talk about their life, not your idea**, Ask about past behavior, not hypothetical future behavior
2. **Ask about specifics, not generics**, "Walk me through the last time you..." not "Do you usually..."
3. **Listen, don't pitch**, The interview is for learning, not selling
4. **Seek disconfirming evidence**, Actively look for reasons your assumptions are wrong

### Interview Guide Generation

**Inputs needed from the PM:**
- Target persona or segment
- Discovery objective (what you're trying to learn)
- Current assumptions to test (optional but recommended)
- Product area or domain context

**Guide structure:**

```markdown
# Discovery Interview Guide
## Context: [objective]
## Persona: [who we're talking to]
## Duration: [30-60 min recommended]

### Warm-Up (5 min)
- [Rapport-building questions about their role/context]
- [Establish they fit the target persona]

### Core Discovery (20-40 min)
#### Theme 1: [Current behavior]
- "Walk me through the last time you [relevant activity]..."
- "What happened next?"
- "How did you decide to [action]?"
- [Follow-up probes for specifics]

#### Theme 2: [Pain points and workarounds]
- "What's the hardest part about [activity]?"
- "Tell me about a time that was particularly frustrating..."
- "What did you try? What happened?"

#### Theme 3: [Outcomes and motivation]
- "What would it mean for you if [problem] were solved?"
- "How do you measure success for [activity] today?"
- "What have you tried to solve this? What happened?"

### Wrap-Up (5 min)
- "Is there anything I should have asked but didn't?"
- "Who else do you think I should talk to about this?"
- [Thank them, discuss next steps]

### DO NOT ASK
- Leading questions: "Don't you think X would be great?"
- Hypothetical questions: "Would you use a product that..."
- Opinion questions: "What do you think about..."
```

### Screener Criteria

Generate a screener to qualify participants:

```markdown
# Participant Screener
## Must-have criteria (all required):
- [Criterion 1, e.g., "Has performed [activity] in the past 30 days"]
- [Criterion 2, e.g., "Decision-maker or strong influencer for [domain]"]

## Nice-to-have criteria (at least 2 of N):
- [Criterion A]
- [Criterion B]

## Disqualification criteria:
- [e.g., "Works at a competitor"]
- [e.g., "Has not experienced the target problem"]

## Screening questions (for recruitment):
1. [Question that maps to must-have criterion 1]
2. [Question that maps to must-have criterion 2]
```

### Debrief Template

Generate a post-interview debrief template:

```markdown
# Interview Debrief
## Participant: [ID / name]
## Date: [date]
## Interviewer: [name]

### Key Quotes (verbatim)
- "[Quote 1]", context: [when they said this]
- "[Quote 2]", context: [when they said this]

### Observations
- [Behavior observed or described]
- [Emotion detected]
- [Workaround mentioned]

### Surprises (things we didn't expect)
- [Surprise 1]

### Assumption Validation
| Assumption | Supported? | Evidence |
|---|---|---|
| [Assumption 1] | Yes / No / Mixed | [What they said/did] |

### Follow-Up Actions
- [ ] [Action item]
```

## Minimum Evidence Bar

**Required inputs:** Target persona or segment, discovery objective, and product domain context. At least one assumption to test is strongly recommended.

**Acceptable evidence:** Prior interview transcripts, survey verbatims, support tickets, behavioral analytics, sales call notes, or documented stakeholder hypotheses.

**Insufficient evidence:** If no discovery objective or target persona is provided, state "Insufficient evidence for interview guide generation" and stop and recommend running the Jobs-to-Be-Done skill to define a learning goal before attempting this skill.

**Hypotheses vs. findings:**
- **Findings:** Screener criteria and "DO NOT ASK" guardrails must reflect known anti-patterns or prior research.
- **Hypotheses:** Interview questions are inherently hypothesis-driven, each Core Discovery theme should be labeled with the assumption it tests.

## Output Format

Produce three documents:
1. **Interview Guide**, ready-to-use question flow
2. **Screener**, recruitment qualification criteria
3. **Debrief Template**, post-interview capture sheet

**Shipwright Signature (required closing):**
4. **Decision Frame**, Key assumptions the interview round will test, trade-off between breadth vs. depth of questioning, confidence in screener fit with evidence quality, owner, interview dates, revisit trigger
5. **Unknowns & Evidence Gaps**, Segments not yet covered, assumptions with no interview questions mapped to them
6. **Pass/Fail Readiness**, PASS if each in-scope discovery theme has enough Mom Test-compliant questions to reveal the material behavior or decision, and the screener filters to the target persona. At Light depth, the screener is not required. Do not add questions merely to fill a list: omit an unsupported theme and name the evidence gap. FAIL if questions are leading, hypothetical, or the persona is undefined.
7. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Asking "would you use X?"**, People can't reliably predict future behavior
- **Not asking for specifics**, "Usually" and "generally" hide the truth; push for "last time"
- **Talking more than listening**, The interviewer should speak < 30% of the time
- **Skipping the debrief**, Insights decay fast; debrief within 24 hours
- **Only interviewing fans**, Include churned users, non-users, and detractors

## Weak vs. Strong Output

**Weak:**
> "What challenges do you face with project management?"

Generic, invites opinion rather than behavior. Produces unreliable data.

**Strong:**
> "Walk me through the last time a project deadline slipped. What happened first?"

Anchored to a specific past event, elicits behavioral sequence, follows Mom Test principles.
