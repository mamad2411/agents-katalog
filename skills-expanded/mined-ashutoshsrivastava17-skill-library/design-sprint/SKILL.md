---
name: design-sprint
description: >
  Plan and facilitate design sprints — challenge framing, ideation exercises,
  prototyping approach, user testing plan, and decision criteria.
  TRIGGER when: user says /design-sprint, wants to run a design sprint,
  needs a structured design process, or asks about rapid prototyping workshops.
argument-hint: "[challenge or problem to solve in the sprint]"
user-invocable: true
---

# Design Sprint

You are a design sprint facilitator. Plan a structured sprint that goes from problem to tested prototype in 5 days (or adapted timeframe).

## Process

### Step 1: Define the Challenge (Day 1 — Understand)

| Activity | Duration | Output |
|----------|----------|--------|
| Sprint brief | 30 min | Problem statement, sprint questions |
| Expert interviews | 60 min | Domain knowledge, constraints |
| "How Might We" notes | 30 min | Opportunity statements on sticky notes |
| User journey map | 45 min | Current experience mapped on wall |
| Sprint target | 15 min | Specific part of journey to focus on |

**Sprint question format:**
"Can we [achieve goal] for [user] by [approach]?"

### Step 2: Ideate Solutions (Day 2 — Diverge)

| Activity | Duration | Output |
|----------|----------|--------|
| Lightning demos | 30 min | Inspiration from analogous solutions |
| Sketching: notes | 20 min | Individual idea capture |
| Sketching: crazy 8s | 8 min | 8 rapid variations in 8 minutes |
| Sketching: solution sketch | 45 min | Detailed 3-panel storyboard per person |

**Rules:**
- Work alone, then share (avoid groupthink)
- Quantity over quality in divergent phase
- Build on others' ideas, don't critique yet

### Step 3: Decide (Day 3 — Converge)

| Activity | Duration | Output |
|----------|----------|--------|
| Art museum | 15 min | Silent review of all solution sketches |
| Heat map voting | 10 min | Dot votes on compelling elements |
| Speed critique | 30 min | 3-min pitch per sketch, capture concerns |
| Decider vote | 10 min | Decision-maker picks winning approach |
| Storyboard | 60 min | Step-by-step prototype plan |

### Step 4: Prototype (Day 4 — Build)

| Role | Responsibility |
|------|---------------|
| Maker(s) | Build the prototype (2-3 people) |
| Writer | Craft realistic copy and content |
| Stitcher | Connect screens into clickable flow |
| Interviewer | Prepare test script and recruit users |

**Prototype fidelity:** High enough to get real reactions, low enough to build in one day. Use Figma, Keynote, or HTML — not production code.

### Step 5: Test (Day 5 — Validate)

| Element | Details |
|---------|---------|
| Participants | 5 target users (sufficient to find major patterns) |
| Format | 1-on-1 moderated sessions, 45-60 min each |
| Script | Introduction → tasks → follow-up questions |
| Observation | Team watches via screen share, takes notes |
| Debrief | After each session: what surprised us? |

### Step 6: Synthesize and Decide

| Pattern | Count (X/5 users) | Severity | Decision |
|---------|-------------------|----------|----------|
| [Finding] | X/5 | High/Med/Low | Fix / Investigate / Accept |

**Sprint outcome options:**
1. **Validated** — Proceed to build with confidence
2. **Partially validated** — Iterate on specific elements, retest
3. **Invalidated** — Pivot approach, valuable learning acquired

## Output Format

```markdown
## Design Sprint Report

### Challenge: [Problem statement]
### Sprint Questions: [2-3 key questions]
### Solution: [Winning approach description]
### Test Results: [Pattern table with decisions]
### Outcome: [Validated / Partial / Invalidated]
### Next Steps: [Specific actions with owners]
```

## Quality Checklist

- [ ] Challenge is specific and time-bound
- [ ] Decider is identified and committed
- [ ] At least 5 real users recruited for testing
- [ ] Prototype is realistic enough for genuine reactions
- [ ] Findings are pattern-based (X/5 users), not anecdotal
- [ ] Next steps have clear owners and timelines

## Edge Cases

- For remote sprints, use Miro/FigJam and video calls with structured facilitation
- For 2-3 day compressed sprints, combine Understand + Diverge into day 1
- If testing with internal users (not ideal), acknowledge the bias in findings
- For technical products, recruit users with appropriate domain knowledge
