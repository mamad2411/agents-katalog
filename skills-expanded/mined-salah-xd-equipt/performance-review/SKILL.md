---
name: performance-review
description: "Builds performance review templates with self-assessment sections, manager feedback, goal setting, and development planning for team growth."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Performance Review

## When to Use This Skill

Use this skill when you need to:
- Create performance review templates for employees or contractors
- Design self-assessment and manager feedback sections
- Build goal-setting frameworks tied to performance outcomes
- Establish a review cadence with development planning

**DO NOT** use this skill for PIP templates (use pip-template), hiring scorecards, or compensation planning. This is for regular performance evaluation.

---

## Core Principle

A PERFORMANCE REVIEW IS NOT A REPORT CARD — IT IS A STRUCTURED CONVERSATION THAT ALIGNS EXPECTATIONS, RECOGNIZES PROGRESS, AND SETS DIRECTION FOR GROWTH.

---

## Phase 1: Review Design

Define the review structure and criteria.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Team size** | "How many people will you be reviewing?" | 1-5 |
| **Review frequency** | "How often do you want to do reviews? (quarterly, biannual, annual)" | Quarterly |
| **Roles** | "What roles are being reviewed?" | No default |
| **Current process** | "Do you have any existing review process?" | None |
| **Key metrics** | "How do you measure success for these roles?" | No default |
| **Rating system** | "Preference: numbered scale, descriptive labels, or no ratings?" | Descriptive labels |

### Rating System

```
## Performance Rating Scale

| Rating | Label | Definition |
|--------|-------|-----------|
| 5 | Exceptional | Consistently exceeds expectations. Top 10% performance. |
| 4 | Exceeds Expectations | Regularly goes above and beyond. Strong contributor. |
| 3 | Meets Expectations | Delivers what is asked reliably. Solid performance. |
| 2 | Needs Improvement | Falls short in some areas. Specific support needed. |
| 1 | Unsatisfactory | Significantly below standards. Immediate action required. |
```

**GATE: Confirm review design before building templates.**

---

## Phase 2: Build Templates

Create the complete review document.

### Self-Assessment Template

```
## Self-Assessment: [Name]

**Review period:** [Date range]
**Role:** [Title]

### Accomplishments
List your top 3-5 accomplishments this period. Include specific outcomes and metrics.

1.
2.
3.

### Goals Review
For each goal set last period, rate your progress:

| Goal | Target | Result | Self-Rating |
|------|--------|--------|-------------|
| [Goal 1] | [Target] | [Actual result] | [1-5] |
| [Goal 2] | [Target] | [Actual result] | [1-5] |

### Challenges
What obstacles did you face? What could have gone better?

### Development
What skills did you develop this period? What do you want to learn next?

### Feedback for Manager
What support or resources would help you be more effective?
```

### Manager Review Template

```
## Performance Review: [Name]

**Review period:** [Date range]
**Reviewer:** [Manager name]
**Role:** [Title]
**Date:** [Date]

---

### Performance Summary

**Overall rating:** [1-5 with label]

### Core Competencies

| Competency | Rating | Evidence / Examples |
|-----------|--------|-------------------|
| Quality of work | [1-5] | [Specific examples] |
| Reliability / Deadlines | [1-5] | [Specific examples] |
| Communication | [1-5] | [Specific examples] |
| Initiative / Ownership | [1-5] | [Specific examples] |
| [Role-specific competency] | [1-5] | [Specific examples] |

### Goal Achievement

| Goal | Target | Result | Rating | Comments |
|------|--------|--------|--------|----------|
| [Goal 1] | [Target] | [Actual] | [1-5] | [Context] |

### Strengths
What this person does well — be specific with examples.

1.
2.
3.

### Areas for Growth
Where this person should focus development — be specific and constructive.

1.
2.

### Next Period Goals

| Goal | Success Metric | Target Date |
|------|---------------|-------------|
| [Goal 1] | [Measurable outcome] | [Date] |
| [Goal 2] | [Measurable outcome] | [Date] |
| [Goal 3] | [Measurable outcome] | [Date] |

### Development Plan

| Skill to Develop | Action | Support Needed | Timeline |
|-----------------|--------|---------------|----------|
| [Skill] | [Training, project, mentoring] | [Resources from manager] | [When] |

---

### Signatures

**Employee:** _______________ Date: ___
**Manager:** _______________ Date: ___
```

**GATE: Present templates for review and customization.**

---

## Phase 3: Conversation Guide

Prepare for the review conversation.

### Review Meeting Structure (45-60 minutes)

```
## Performance Review Meeting Agenda

1. **Opening (5 min):** Set a positive, constructive tone. Review the purpose.
2. **Self-assessment discussion (10 min):** Let the employee share their perspective first.
3. **Manager feedback (15 min):** Share ratings, strengths, and growth areas with examples.
4. **Goal review (10 min):** Discuss progress on previous goals.
5. **Goal setting (10 min):** Collaboratively set goals for next period.
6. **Development planning (5 min):** Agree on skill development actions.
7. **Close (5 min):** Summarize key points, confirm next steps.
```

### Difficult Conversation Framework

For underperformance (rating 1-2):

1. State the specific behavior or result (not character)
2. Explain the impact on the business or team
3. Listen to their perspective
4. Collaboratively define what needs to change
5. Set a clear improvement timeline with check-ins
6. Confirm the consequences if improvement does not happen

---

## Phase 4: Follow Through

Ensure reviews drive actual development.

### Post-Review Actions

```
## Post-Review Checklist

- [ ] Finalize review document and file securely
- [ ] Send copy to the employee
- [ ] Schedule mid-period check-in (halfway to next review)
- [ ] Begin any agreed development actions (training, resources)
- [ ] Update compensation if tied to review cycle
```

### Mid-Period Check-In Template

```
## Mid-Period Check-In: [Name] — [Date]

**Goals progress:**
| Goal | Status | On Track? |
|------|--------|-----------|
| [Goal] | [Update] | Yes / At Risk / No |

**Development progress:** [Update on skill development actions]
**Any blockers or support needed?**
**Feedback in either direction?**
```

### Annual Review Cycle

```
## Review Calendar

| Month | Action |
|-------|--------|
| [Month 1] | Distribute self-assessment forms |
| [Month 1 + 1 week] | Self-assessments due |
| [Month 1 + 2 weeks] | Manager reviews completed |
| [Month 1 + 3 weeks] | Review meetings held |
| [Month 1 + 4 weeks] | Goals and development plans finalized |
| [Mid-period] | Mid-period check-ins |
```

---

## Anti-Patterns

- **Surprise feedback** — nothing in a review should be news. Give feedback in real-time throughout the period.
- **Recency bias** — rating based on last 2 weeks instead of the full review period. Keep notes throughout.
- **Vague feedback** — "You need to communicate better" is useless. "You missed the deadline notification on the Smith project, which caused a 3-day delay" is actionable.
- **All 3s** — rating everyone "Meets Expectations" avoids hard conversations but helps no one. Differentiate honestly.
- **No follow-through** — a review without goal tracking and check-ins is a wasted hour.

---

## Recovery

- **User has never given a performance review:** Start with a simple 3-question framework: What went well? What could improve? What are your goals next quarter?
- **Employee disagrees with the rating:** Listen. Ask for specific examples supporting their view. Adjust if warranted, explain if not.
- **User only has contractors:** Adapt to a project feedback model — review after each project or quarterly, focused on deliverable quality and collaboration.
- **Reviews feel awkward:** They get easier with practice. Use the conversation guide as a script the first few times.
- **No metrics to evaluate against:** Set metrics NOW for the next review period. For this review, use qualitative assessment with specific examples.
