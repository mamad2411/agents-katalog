---
name: retrospective-formats
description: Post-mortem structure, 5 Whys root cause analysis, blameless retrospective patterns, and improvement recommendation formats. Use when facilitating a cycle retrospective, conducting a post-mortem, or generating structured improvement recommendations.
---

# Retrospective Formats

A retrospective that produces a list of "what went wrong" without actionable improvements is a venting session, not a process tool. This skill covers the formats for structuring retrospectives so they reliably produce root causes and committed improvements — not just observations.

## When to Use This Skill

- Running a post-mortem after a completed product cycle
- Facilitating a retrospective after a launch incident
- Identifying recurring process failures across multiple cycles
- Generating improvement recommendations that will actually be implemented
- Reviewing past retrospectives to check whether improvements were adopted

## Core Concepts

### 1. Blameless by Default

Systems and processes fail more often than individuals. A blameless retrospective:
- Asks "what in our process allowed this to happen?" not "who caused this?"
- Assumes everyone involved had good intentions and the best information available
- Produces systemic improvements rather than individual reprimands

This is not about avoiding accountability — it's about producing improvements that prevent recurrence.

### 2. Separate Symptoms from Root Causes

A symptom is what was observed. A root cause is why it happened. Treating symptoms produces local fixes. Treating root causes prevents recurrence.

```
Symptom: "The feature shipped 2 weeks late"
Root cause: "Acceptance criteria were incomplete at the start of the cycle,
             requiring two rounds of rework during implementation"
```

### 3. Improvements Must Be Specific and Owned

"Improve communication" is not an improvement. "Before each cycle, Product and Engineering will co-review the feature spec within 2 days of PRD approval" is an improvement.

Each improvement must have:
- A concrete action
- An owner
- A due date or implementation cycle

## Cycle Post-Mortem Format

```markdown
# Post-Mortem: [Cycle / Feature Name]

**Cycle dates:** [Start] → [End]
**Facilitator:** [Name]
**Participants:** [Names / roles]
**Date of retrospective:** [Date]

---

## Cycle Summary

**What we set out to do:**
[Restate the PRD goal and success criteria]

**What we shipped:**
[What actually launched — including any descopes]

**Outcome vs. target:**
| Metric | Target | Actual | Delta |
|--------|--------|--------|-------|
| [Primary metric] | [Target] | [Actual] | [+/-] |
| [Secondary metric] | [Target] | [Actual] | [+/-] |

**Timeline:**
| Planned | Actual | Variance |
|---------|--------|---------|
| [Milestone] | [Actual date] | [+/- days] |

---

## What Went Well

[Things that worked and should be preserved or amplified]

| What | Why It Worked | Should We Formalize It? |
|------|--------------|------------------------|
| [Observation] | [Explanation] | [Yes / No / Maybe] |

---

## What Went Wrong

[Problems encountered — factual, not evaluative]

| What | When It Occurred | Impact |
|------|-----------------|--------|
| [Problem] | [Phase / date] | [Consequence] |

---

## Root Cause Analysis

[For each significant problem, identify the root cause]

### Problem: [Name]

**5 Whys:**
1. Why did [Problem] occur? → [Answer]
2. Why did [Answer from 1]? → [Answer]
3. Why did [Answer from 2]? → [Answer]
4. Why did [Answer from 3]? → [Answer]
5. Why did [Answer from 4]? → [Root cause]

**Root cause:** [Final answer from the Why chain]
**Category:** Process / Tooling / Spec quality / Communication / External

---

## Improvement Recommendations

| # | Improvement | Root Cause Addressed | Owner | Target Cycle |
|---|------------|---------------------|-------|-------------|
| 1 | [Specific, actionable change] | [Which root cause] | [Name] | [When] |

---

## Recurring Patterns (across cycles)

[Issues that have appeared in previous post-mortems and haven't been resolved]

| Pattern | First Observed | Occurrences | Status |
|---------|---------------|-------------|--------|
| [Pattern] | [Cycle name] | [X times] | [Open / In Progress / Resolved] |
```

## The 5 Whys Technique

### How to Use It

Start with the symptom (the observable problem). Ask "why did this happen?" five times, going deeper each time. Stop when you reach a root cause that is:
- Actionable (something the team can change)
- Systemic (not just a one-time event)
- Root (not itself caused by something else)

### Worked Example

```
Problem: The checkout feature missed the launch date by 10 days.

Why 1: Why did it miss the launch date?
→ The backend API wasn't ready when frontend integration was scheduled to start.

Why 2: Why wasn't the backend API ready on time?
→ The API contract changed mid-cycle, requiring a significant rework.

Why 3: Why did the API contract change mid-cycle?
→ The feature spec didn't define the API contract — it was left to engineering to figure out during implementation.

Why 4: Why didn't the feature spec define the API contract?
→ The spec review process doesn't require API contracts to be defined before development begins.

Why 5: Why doesn't the spec review process require API contracts?
→ There's no checklist for spec completeness review; completeness is assessed informally.

Root cause: Spec completeness review has no formal checklist, allowing API contracts
            to be undefined at the start of development cycles.

Improvement: Add API contract definition as a required gate in the spec review
             checklist, with Product and Engineering sign-off required before
             the cycle begins.
```

## Improvement Recommendation Qualities

A good improvement recommendation is:

- **Specific:** Describes exactly what changes, not a vague direction
- **Owned:** One person is accountable for implementation
- **Time-bound:** Has a clear target (next cycle, by [date])
- **Testable:** Can be verified — either it was done or it wasn't
- **Proportionate:** Matches the severity of the problem it addresses

### Improvement Prioritization

When multiple improvements are identified, prioritize by:

| Score | Frequency × Impact |
|-------|-------------------|
| High | Recurring issue that affects cycle outcomes significantly |
| Medium | Recurring issue with moderate impact OR first-time issue with high impact |
| Low | First-time issue with low impact |

Commit to high-priority improvements. Note medium-priority improvements. Document low-priority improvements but don't commit resources.

## Trend Analysis Across Cycles

Review the last 3–5 post-mortems before each new one to identify:

1. **Improvements that were committed but not implemented** — why? What happened?
2. **Problems that have appeared more than once** — the systemic fix hasn't been found yet
3. **What the same root category keeps producing** — if "spec quality" appears in 4 of 5 retrospectives, that's the domain to focus on

```markdown
## Cross-Cycle Trend Summary

### Root Cause Categories (last 5 cycles)

| Category | Frequency | Trend |
|----------|-----------|-------|
| Spec quality / completeness | 4/5 cycles | Persistent |
| External dependency delays | 3/5 cycles | Persistent |
| Scope expansion mid-cycle | 2/5 cycles | Improving |
| Test coverage gaps | 1/5 cycles | Resolved |

### Improvement Adoption Rate

| Improvement | Committed In | Status |
|-------------|-------------|--------|
| [Improvement] | [Cycle] | Adopted / Partially adopted / Not adopted |
```

## Best Practices

1. **Run the retrospective within one week of cycle completion** — memories are fresh and teams are still engaged
2. **Document before the meeting** — ask participants to write what went well/wrong before gathering; reduces groupthink
3. **Time-box root cause analysis** — 5 Whys for each problem, maximum 10 minutes; deeper analysis becomes post-mortem meetings
4. **Close the loop on previous improvements** — start every retrospective by reviewing the previous cycle's commitments
5. **Distinguish "we should have" from "we will"** — retrospectives produce "we will" commitments, not "we should have" observations
