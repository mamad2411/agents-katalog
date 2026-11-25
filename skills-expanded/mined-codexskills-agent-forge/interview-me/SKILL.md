---
name: interview-me
description: One-question-at-a-time interview skill that extracts what the user actually wants instead of what they think they should want. Uses structured questioning to surface hidden assumptions, constraints, and true intent before any work begins.
---

# Interview Me

## Overview

Most failed projects start with a confident misinterpretation. The user says "build me a dashboard" but means "show me the one number that matters." They say "make it scalable" but mean "handle 200 users without crashing." They say "I want AI" but mean "I want to look modern."

This skill prevents that. It uses a structured, one-question-at-a-time interview protocol to extract genuine requirements. Each question builds on the previous answer, narrowing toward a precise, testable specification. No silent assumptions. No filled-in blanks. No surprises at demo time.

The core insight: **every ambiguous statement hides a decision the user hasn't made yet.** Your job is to surface those decisions, one at a time, until the shape of the work is unmistakable.

## When to Use

| Trigger | Description |
|---------|-------------|
| Underspecified request | "Build me X" without "for whom" or "why now" |
| User explicitly invokes | "Interview me", "grill me", "are we sure?" |
| Silent requirement filling | You catch yourself guessing about scope, users, or constraints |
| Vague outcome | The success criteria isn't measurable |
| High-stakes project | Production system, customer-facing, security-sensitive |
| New domain | You lack context about the problem space |
| Multiple stakeholders | One user speaking for a team with unstated disagreements |

**Do NOT use** when: the request is trivially small (rename a variable), a spec already exists with verified clarity, or the user explicitly says "just do it, no questions."

## Process — 5-Phase Interview

### Phase 1: Context Set (2-3 questions)

Goal: Establish the boundaries before diving into specifics.

Questions to draw from (ask ONE at a time, in order):

1. "Who is this for? End users, internal team, or just you?"
2. "What's the minimum version that would be useful?" (not the ideal, the floor)
3. "Is this replacing something, or filling a gap?"
4. "When does this need to be done by? What's the real deadline, not the aspirational one?"

**Output:** Project canvas — audience, minimum viable outcome, replacement/existing context, timeline pressure.

### Phase 2: Problem Definition (3-4 questions)

Goal: Understand what problem is actually being solved.

1. "What happens if we don't build this? What pain does the status quo cause?"
2. "Who feels that pain most? How do they cope today?"
3. "How will we know this is working? What metric changes?"
4. "What have you tried before that didn't work?"

**Output:** Problem statement — current state, pain owner, success metric, prior art.

### Phase 3: Scope Calibration (3-4 questions)

Goal: Draw the line between in-scope and out-of-scope.

1. "What's a thing someone might assume is included but you want explicitly excluded?"
2. "What's the hardest part of this? Where do you expect the most complexity?"
3. "Is there a 'Phase 2' list? What would you add if you had infinite time?"
4. "What are the non-negotiables? The things you will not compromise on?"

**Output:** Scope boundary — explicit inclusions, explicit exclusions, complexity hotspots, nice-to-haves, hard constraints.

### Phase 4: Constraint Elicitation (2-3 questions)

Goal: Surface hidden technical, organizational, and design constraints.

1. "Are there existing systems this must integrate with? Any APIs, databases, or auth providers?"
2. "Any tech stack preferences or constraints? Things you want or want to avoid?"
3. "Who approves this? Are there stakeholders who need to sign off?"
4. "Any security, compliance, or accessibility requirements?"

**Output:** Constraint map — integration points, stack decisions, approval chain, regulatory needs.

### Phase 5: Confidence Check (1-2 questions)

Goal: Verify alignment before proceeding.

1. "Let me summarize what I heard. Does this sound right?" (deliver structured recap)
2. "On a scale of 1-10, how confident are you that this captures what you need?"

If confidence < 7: "What's missing? Let's go back and fix that."

**Output:** Confidence score + gap list.

## Confidence Scoring

After each phase, assign a confidence score 1-10:

| Score | Meaning | Action |
|-------|---------|--------|
| 10 | Crystal clear, no ambiguity | Proceed |
| 8-9 | Minor clarification needed | Note and proceed |
| 6-7 | Several open questions | Continue interview |
| 4-5 | Major gaps | Restart from Phase 2 |
| 1-3 | Completely misaligned | Stop, reset expectations |

**Overall confidence = minimum of all phase scores.** A Phase 1 score of 10 means nothing if Phase 4 scored 3.

## Escalation Triggers

Stop the interview and escalate if:

1. **Contradictory answers** — User says "must be cheap" and "must be enterprise-grade" in adjacent breaths. Escalate with: "I'm hearing tension between X and Y. Which takes priority if we can't have both?"

2. **Vanishing scope** — Every answer expands scope. "Also it should..." appears in every response. Escalate with: "The scope keeps growing. Let's freeze the current list and ship this first."

3. **Disguised solution** — User describes an implementation detail as a requirement. "I need a WebSocket connection" when they really need real-time updates. Escalate with: "What problem does the WebSocket solve? Let's start from that problem."

4. **Proxy stakeholder** — User says "they want" or "the team needs" but won't bring the actual stakeholder. Escalate with: "Can we get 15 minutes with [stakeholder]? I want to hear it from them."

5. **Mood shift** — User becomes defensive, dismissive, or impatient. Escalate with: "This may feel slow. The goal is to save time later. Bear with me."

## Anti-Rationalization Table

| Temptation | Why It Happens | Why It's Dangerous | What To Do Instead |
|------------|----------------|--------------------|--------------------|
| "I know what they mean" | Pattern matching from previous projects | Every project is different; you fill in wrong defaults | Ask one more question to confirm |
| "They're busy, let me be efficient" | Empathy for user's time | False efficiency; rework costs more than upfront clarity | "One quick question before I start..." |
| "I'll figure it out as I go" | Confidence in your adaptability | You build the wrong thing; user loses trust | "Let me confirm the direction first" |
| "This question will annoy them" | Fear of seeming incompetent | You miss critical information | "I ask everyone this — it saves us both time" |
| "I already asked enough questions" | You hit 5 questions and feel done | You stopped at Phase 2 | Complete all 5 phases |
| "They said 'make it nice' — I'll use my judgment" | Design interpretation is subjective | Taste mismatch; rework | "What does 'nice' mean? Show me examples." |
| "The deadline is tomorrow, no time to ask" | Panic | You deliver unusable output | "I can start immediately if you confirm X. Otherwise the risk is Y." |

## Red Flags

1. User can't name the audience — "everyone" or "users" without specifics
2. User can't define success — no metric, no observable outcome
3. Every answer adds scope — no willingness to cut
4. User says "you're the expert, you decide" — they're abdicating, not trusting
5. Multiple unspoken stakeholders — "they'll like it" means no one approved
6. Tech stack mandated but problem undefined — solution in search of a problem
7. "Just make it work like [famous product]" without understanding why
8. Deadline is fixed but scope is unbounded — recipe for failure

## Verification

After the interview, verify you have:

- [ ] **Audience** defined (not "users", but a specific persona)
- [ ] **Problem statement** in one sentence: "We need X because Y for Z"
- [ ] **Success metric** that is measurable and timebound
- [ ] **Scope boundary** — explicit in-scope and out-of-scope lists
- [ ] **Constraint map** — tech stack, integrations, compliance, approvals
- [ ] **Stakeholder list** — who decides, who consults, who is informed
- [ ] **Complexity assessment** — the team agrees on what's hard
- [ ] **Confidence score >= 7** — if not, continue interviewing
- [ ] **Written summary** sent to user before any implementation begins

### Structured Output Format

After completing all 5 phases, write the following to a file named `SPEC.md` in the project root:

```markdown
# Project: [Name]

## Audience
[Who is this for? Be specific.]

## Problem Statement
[One sentence: We need X because Y for Z.]

## Success Metric
[How we know it works. Measurable. Timebound.]

## Scope
### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Item 1]
- [Item 2]

### Nice-to-Haves (Phase 2)
- [Item 1]

## Constraints
- **Stack:** [tech stack]
- **Integrations:** [API/database/auth]
- **Compliance:** [requirements]
- **Approvals needed:** [who signs off]
- **Deadline:** [date]

## Complexity Hotspots
[Where the team expects difficulty.]

## Confidence Score
[Overall: X/10. Phase scores: Context X, Problem X, Scope X, Constraints X, Check X]

## Interview Log
- Q: [question] → A: [answer]
- Q: [question] → A: [answer]
```

### Gate Check

Before implementation, run the **3-Question Sanity Check**:

1. If we ship exactly this and nothing more, is it useful? (If no, reset scope.)
2. Could someone read this spec and build it without asking you questions? (If no, add detail.)
3. Is there anything in this spec that feels like a guess rather than a known fact? (If yes, mark as assumption to verify.)

If all three pass, implementation can begin.
