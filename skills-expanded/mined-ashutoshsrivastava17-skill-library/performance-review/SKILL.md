---
name: performance-review
description: >
  Structure a performance review cycle including self-assessments, manager
  reviews, peer feedback, calibration sessions, and rating frameworks.
  TRIGGER when: user asks about performance reviews, review cycle, calibration,
  performance management, self-assessment, peer feedback, ratings, or
  performance improvement plans.
argument-hint: "[--cycle <annual|semi-annual|quarterly>] [--phase <setup|writing|calibration|delivery>]"
user-invocable: true
---

# Performance Review Cycle

You are a senior People Operations leader. Design and execute a rigorous, fair performance review process that drives growth, accountability, and retention.

## Step 1: Gather Context

| Field | Required | Default | Notes |
|-------|----------|---------|-------|
| Review Cycle | No | Semi-annual | Annual, semi-annual, or quarterly |
| Current Phase | No | Full cycle design | Setup, writing, calibration, or delivery |
| Organization Size | No | — | Affects calibration approach |
| Existing Framework | No | None | Build new or improve existing |
| Rating Scale | No | 5-point | See options below |
| Competency Model | No | — | Company-specific competencies if any |

## Step 2: Review Cycle Timeline

### Semi-Annual Cycle (adapt for annual/quarterly)

| Phase | Timeline | Duration | Owner |
|-------|----------|----------|-------|
| 1. Cycle Kickoff | Week 1 | 1 week | HR / People Ops |
| 2. Self-Assessment | Weeks 2-3 | 2 weeks | All employees |
| 3. Peer Feedback | Weeks 2-3 | 2 weeks | Selected peers (3-5) |
| 4. Manager Review Writing | Weeks 4-5 | 2 weeks | All managers |
| 5. Calibration Sessions | Week 6 | 1 week | Leadership + HR |
| 6. Review Delivery | Weeks 7-8 | 2 weeks | Managers |
| 7. Goal Setting | Weeks 7-8 | Concurrent | Manager + Employee |
| 8. Cycle Retrospective | Week 9 | 1 week | HR / People Ops |

## Step 3: Rating Framework

### 3.1 Rating Scale Options

**5-Point Scale (Recommended)**

| Rating | Label | Distribution Target | Description |
|--------|-------|-------------------|-------------|
| 5 | Exceptional | 5-10% | Consistently exceeds expectations; top performer |
| 4 | Exceeds Expectations | 20-25% | Frequently exceeds expectations; strong performer |
| 3 | Meets Expectations | 50-60% | Consistently meets expectations; solid contributor |
| 2 | Needs Improvement | 10-15% | Partially meets expectations; development needed |
| 1 | Does Not Meet | 0-5% | Fails to meet expectations; immediate action required |

### 3.2 Evaluation Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Results / Impact | 40% | Achievement of goals, business outcomes delivered |
| Competencies / How | 30% | Behaviors, skills, and how results were achieved |
| Growth / Development | 15% | Learning trajectory, skill acquisition, stretch goals |
| Collaboration / Culture | 15% | Teamwork, mentoring, living company values |

## Step 4: Review Components

### 4.1 Self-Assessment Template

```
SELF-ASSESSMENT — {Review Period}
═════════════════════════════════

Name: _______________    Role: _______________
Manager: _______________  Level: _______________

1. KEY ACCOMPLISHMENTS
   List your 3-5 most significant achievements this cycle.
   For each, describe the impact and how it aligned with your goals.

   a. _______________
   b. _______________
   c. _______________

2. GOALS REVIEW
   Review each goal set at the beginning of the cycle.

   | Goal | Status | Evidence of Progress | Self-Rating |
   |------|--------|---------------------|-------------|
   |      |        |                     |             |

3. COMPETENCY SELF-RATING
   Rate yourself on each competency (1-5) with specific examples.

   | Competency | Rating | Evidence |
   |-----------|--------|----------|
   |           |        |          |

4. DEVELOPMENT & GROWTH
   - What new skills or knowledge did you acquire?
   - Where did you stretch beyond your comfort zone?
   - What feedback did you act on?

5. CHALLENGES & SUPPORT NEEDED
   - What obstacles did you face?
   - What support would help you perform better?

6. CAREER ASPIRATIONS
   - Where do you see yourself in 12-18 months?
   - What development experiences would help you get there?
```

### 4.2 Peer Feedback Template

```
PEER FEEDBACK — {Employee Name}
════════════════════════════════

Reviewer: _______________    Relationship: _______________

1. What are this person's greatest strengths?
   (Provide specific examples)

2. What is one area where this person could grow or improve?
   (Be constructive and specific)

3. How effectively does this person collaborate with others?
   (1-5 rating + examples)

4. What impact has this person had on the team or project?
   (Specific outcomes or contributions)

5. Any additional feedback?
```

### 4.3 Manager Review Template

```
MANAGER REVIEW — {Employee Name}
═════════════════════════════════

Manager: _______________    Review Period: _______________

OVERALL RATING: ___/5

RESULTS / IMPACT (40%):
Rating: ___/5
{Narrative with specific examples, data, and outcomes}

COMPETENCIES / HOW (30%):
Rating: ___/5
{Narrative on behaviors, skills demonstrated, and how work was done}

GROWTH / DEVELOPMENT (15%):
Rating: ___/5
{Narrative on learning, stretch assignments, and development progress}

COLLABORATION / CULTURE (15%):
Rating: ___/5
{Narrative on teamwork, mentoring, and values alignment}

KEY STRENGTHS:
1.
2.
3.

DEVELOPMENT AREAS:
1.
2.

GOALS FOR NEXT CYCLE:
1.
2.
3.

CAREER DISCUSSION NOTES:
{Summary of career aspirations and development plan}

COMPENSATION RECOMMENDATION:
[ ] No change  [ ] Merit increase: ___%  [ ] Promotion to: ___
```

## Step 5: Calibration Process

### 5.1 Calibration Meeting Structure

| Step | Duration | Activity |
|------|----------|----------|
| 1 | 5 min | Ground rules: fairness, evidence-based, confidential |
| 2 | 15 min | Review proposed rating distribution vs. target |
| 3 | 30 min | Discuss outliers: all 5s, all 1-2s, and borderline cases |
| 4 | 20 min | Cross-team calibration for same-level employees |
| 5 | 10 min | Finalize ratings and document decisions |
| 6 | 10 min | Review promotion and compensation recommendations |

### 5.2 Calibration Rules

- Every employee rated 5 or 1 must be discussed with specific evidence
- No manager can rate more than 20% of their team as 5 without calibration approval
- Ratings must be supported by outcomes and behaviors, not tenure or seniority
- HR facilitator ensures distribution aligns with guidelines (not forced ranking)
- Recency bias check: evidence must span the full review period

### 5.3 Calibration Output

```
CALIBRATION SUMMARY — {Department}
═══════════════════════════════════

Rating Distribution:
  5 (Exceptional):     {X}% (target: 5-10%)
  4 (Exceeds):         {X}% (target: 20-25%)
  3 (Meets):           {X}% (target: 50-60%)
  2 (Needs Improve):   {X}% (target: 10-15%)
  1 (Does Not Meet):   {X}% (target: 0-5%)

Promotions Approved:     {X}
PIPs Recommended:        {X}
Compensation Actions:    {X} merit increases, {X} equity refreshes
```

## Step 6: Review Delivery Guidelines

### Manager Coaching for Delivery

| Do | Don't |
|----|-------|
| Start with the overall rating | Bury the rating at the end |
| Use specific examples for every point | Rely on vague statements |
| Acknowledge the employee's self-assessment | Ignore what they wrote |
| Be direct about development areas | Sugarcoat underperformance |
| Discuss career growth and next steps | Make it purely backward-looking |
| Listen actively; leave space for response | Monologue for 30 minutes |
| Document agreements and action items | Leave the conversation without clear next steps |

### Conversation Structure (45-60 min)

1. **Opening** (5 min): Set a collaborative tone, share the agenda
2. **Overall assessment** (5 min): State the rating and high-level summary
3. **Strengths deep-dive** (10 min): Celebrate achievements with evidence
4. **Development areas** (10 min): Discuss growth opportunities constructively
5. **Employee perspective** (10 min): Invite their reaction, questions, and input
6. **Goals and development plan** (10 min): Set forward-looking objectives
7. **Closing** (5 min): Summarize action items, express confidence

## Edge Cases

- **New hires (<6 months)**: Provide developmental feedback only; no formal rating. Note "too early to rate" in the system
- **Manager changes mid-cycle**: Both managers contribute; current manager owns the final review with prior manager's input
- **Performance Improvement Plan (PIP)**: If rating is 1, create a structured 30/60/90 day PIP with clear, measurable criteria for success
- **Disagreements**: If an employee disputes their rating, document the disagreement and offer an escalation path (skip-level or HR review)
- **Remote/distributed teams**: Ensure manager has sufficient visibility; supplement with peer feedback and output-based evidence
- **High performers wanting to leave**: Use the review to address retention proactively; connect to career pathing and compensation

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
