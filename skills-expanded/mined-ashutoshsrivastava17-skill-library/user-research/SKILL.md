---
name: user-research
description: >
  Plan, structure, and document user research — interview guides, survey design, usability test plans.
  TRIGGER when: user says "plan research", "interview guide", "survey questions",
  "usability test", "research plan", or needs to design a study.
argument-hint: "[plan|interview|survey|usability-test] [research topic]"
user-invocable: true
---

# User Research

Design rigorous user research studies — from research questions to discussion guides, survey instruments, and usability test plans.

## Operations

### Research Plan — `$ARGUMENTS` contains "plan"

Generate a complete research plan:

```
## Research Plan — {topic}

### Objective
{What we want to learn and why it matters for the product}

### Research Questions
1. {Broad question — e.g., "How do users currently manage their invoices?"}
2. {Specific question — e.g., "At what point do users abandon the checkout flow?"}
3. {Evaluative question — e.g., "Can users complete the onboarding in under 5 minutes?"}

### Method Selection
| Method | Best For | Recommended When |
|---|---|---|
| Interviews (1:1) | Deep understanding of behaviors, motivations, mental models | Exploratory research, complex domains |
| Surveys | Quantifying attitudes, preferences at scale | Validating hypotheses, measuring satisfaction |
| Usability testing | Evaluating task completion, identifying friction | Testing prototypes or live products |
| Card sorting | Understanding mental models for information architecture | Designing navigation, categorization |
| Diary studies | Longitudinal behavior patterns | Understanding habits, real-world usage over time |
| A/B testing | Measuring behavioral impact of design changes | Optimizing specific interactions with traffic |

**Selected method**: {method} — {rationale}

### Participants
- **Target**: {user segment or persona}
- **Sample size**: {N} participants
  - Interviews: 5-8 for pattern saturation
  - Surveys: 100+ for statistical significance
  - Usability: 5 per round (catches ~85% of issues)
- **Recruitment criteria**:
  - Include: {demographics, behaviors, experience level}
  - Exclude: {who to filter out and why}
- **Incentive**: {compensation recommendation}

### Timeline
| Phase | Duration | Activities |
|---|---|---|
| Planning | {N} days | Finalize guide, recruit participants |
| Fieldwork | {N} days | Conduct sessions |
| Analysis | {N} days | Code data, identify themes |
| Reporting | {N} days | Synthesize and present findings |

### Deliverables
- {Research guide / survey instrument}
- {Raw data / transcripts}
- {Synthesis report with insights and recommendations}
```

### Interview Guide — `$ARGUMENTS` contains "interview"

```
## Interview Guide — {topic}

### Session Setup
- **Duration**: 45-60 minutes
- **Format**: {remote / in-person} — {moderated / unmoderated}
- **Recording**: {audio / video / notes only} — get consent first
- **Materials needed**: {prototype link, consent form, note-taking template}

### Introduction (5 min)
> "Thank you for joining. I'm researching {topic} to understand {goal}.
> There are no right or wrong answers — I'm interested in your honest experience.
> This session will take about {N} minutes. {Recording consent language}.
> Do you have any questions before we start?"

### Warm-Up (5 min)
- Tell me about your role and what a typical day looks like.
- How long have you been {relevant context}?

### Core Questions (30-40 min)

#### Topic 1: {Current behavior}
1. Walk me through how you currently {task}. Start from the beginning.
   - *Probe*: What happens next?
   - *Probe*: How do you decide {decision point}?
2. When was the last time you {specific behavior}? Tell me about that.
3. What's the hardest part of {task}?
   - *Probe*: Why is that difficult?
   - *Probe*: How do you work around it?

#### Topic 2: {Pain points & needs}
4. What frustrates you most about {current solution}?
5. If you could change one thing, what would it be?
   - *Probe*: What would that enable you to do?

#### Topic 3: {Evaluation} (if testing a concept/prototype)
6. {Task prompt}: "Imagine you need to {goal}. Show me how you'd do that."
   - *Observe*: Where do they click first? Do they hesitate?
   - *Probe*: What did you expect to happen?
   - *Probe*: Was anything confusing?

### Wrap-Up (5 min)
- Is there anything about {topic} we haven't discussed that you think is important?
- Would you be open to a follow-up session if we have more questions?
- Thank you for your time.

### Interviewer Notes Template
| Question | Key Quote | Behavior/Observation | Sentiment |
|---|---|---|---|
| Q1 | | | |
| Q2 | | | |
```

### Survey Design — `$ARGUMENTS` contains "survey"

```
## Survey Design — {topic}

### Survey Metadata
- **Objective**: {what we're measuring}
- **Target audience**: {who should take this}
- **Estimated completion time**: {N} minutes (keep under 10)
- **Distribution**: {email, in-app, link}

### Question Design Principles
- Lead with easy, non-threatening questions
- Group by topic, flow logically
- Mix question types to reduce fatigue
- Avoid double-barreled questions ("Is the app fast and easy to use?")
- Use balanced scales (equal positive and negative options)
- Include "N/A" or "Prefer not to say" where appropriate
- Randomize option order for non-ordinal choices

### Questions

#### Section 1: Demographics / Segmentation
1. {Segmentation question} — {Single select / Multi select}
   - Options: ...

#### Section 2: {Core topic}
2. {Rating scale question} — Likert 5-point
   - Strongly disagree / Disagree / Neutral / Agree / Strongly agree
3. {Multiple choice question} — Single select
   - Options: ...
   - Other (please specify): ___
4. {Open-ended question} — Free text
   - "In your own words, describe..."

#### Section 3: {Satisfaction / NPS}
5. How likely are you to recommend {product} to a colleague? — NPS (0-10)
6. What is the primary reason for your score? — Free text

### Analysis Plan
- Quantitative: {means, distributions, cross-tabs by segment}
- Qualitative: {thematic coding of open-ended responses}
- Key metrics: {NPS, satisfaction score, task frequency}
```

### Usability Test Plan — `$ARGUMENTS` contains "usability"

```
## Usability Test Plan — {feature/product}

### Objective
{What we're evaluating and what success looks like}

### Setup
- **Prototype/Build**: {link or description}
- **Environment**: {remote moderated / remote unmoderated / in-person}
- **Tool**: {platform — e.g., Maze, UserTesting, Lookback, Zoom}
- **Participants**: {N}, {criteria}
- **Duration**: {N} minutes per session

### Tasks

| # | Task Prompt | Success Criteria | Max Time |
|---|---|---|---|
| 1 | "You want to {goal}. Starting from this screen, show me how you'd do that." | Reaches {target screen/state} without help | 3 min |
| 2 | "Now imagine you need to {goal}." | Completes {action} correctly | 2 min |
| 3 | "Something went wrong with {scenario}. What would you do?" | Finds {error recovery path} | 3 min |

### Metrics
| Metric | How Measured |
|---|---|
| Task success rate | % completing each task without assistance |
| Time on task | Seconds from prompt to completion |
| Error rate | Wrong clicks or dead ends per task |
| Satisfaction | Post-task SEQ (Single Ease Question, 1-7) |
| Overall satisfaction | Post-test SUS (System Usability Scale) |

### Post-Test Questions
1. What was the easiest part of using this?
2. What was the most confusing part?
3. If you could change one thing, what would it be?

### Reporting Template
| Task | Success Rate | Avg Time | Errors | Avg SEQ | Key Finding |
|---|---|---|---|---|---|
| Task 1 | {N}% | {N}s | {N} | {N}/7 | {observation} |
```

## Quality Standards

- **No leading questions**: "How much did you love this feature?" is biased. "How would you describe your experience?" is neutral.
- **One concept per question**: Never ask about two things at once.
- **Observe behavior, not just opinions**: What people do matters more than what they say they'd do.
- **Pilot test**: Always recommend testing the guide/survey with 1-2 people before full launch.
- **Ethics**: Include consent, data handling, and right-to-withdraw in all study designs.

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
