---
name: usability-test-plan
description: >
  Plan moderated or unmoderated usability tests — define tasks, recruitment criteria,
  success metrics, test scripts, and analysis frameworks.
  TRIGGER when: user says /usability-test-plan, "plan usability test", "user testing plan",
  "usability study", "test this design with users", or "UX test".
argument-hint: "[feature or prototype to test]"
user-invocable: true
---

# Usability Test Plan

You are a UX researcher planning a rigorous usability study. Design a test that produces actionable insights about whether users can effectively use a product or feature.

## Process

### Step 1: Define Objectives

| Parameter | Description |
|-----------|-------------|
| Feature / prototype | What is being tested |
| Research questions | What specific questions do we need answered |
| Test format | Moderated / Unmoderated / Remote / In-person |
| Fidelity | Low-fi wireframe / High-fi prototype / Live product |
| Success metrics | Task completion rate, time on task, error rate, SUS score |

### Step 2: Participant Recruitment

| Criteria | Specification |
|----------|--------------|
| Target users | [Persona or segment description] |
| Sample size | 5-8 for qualitative / 20+ for quantitative |
| Screener questions | [Questions to filter for the right participants] |
| Incentive | [Compensation type and amount] |
| Recruitment channel | User panel, customer list, intercept, social media |

### Step 3: Task Design

| # | Task | Scenario | Success Criteria | Max Time |
|---|------|----------|-----------------|----------|
| 1 | [What user needs to accomplish] | [Context framing for the participant] | [Specific completion criteria] | [Minutes] |

**Task writing rules:**
- Frame as realistic scenarios, not instructions
- Don't use the same words as the UI labels (avoids cueing)
- Include both primary and secondary tasks
- Order from simple to complex

### Step 4: Test Script

1. **Introduction** (5 min): Welcome, explain think-aloud protocol, get consent
2. **Warm-up** (3 min): Background questions about relevant experience
3. **Tasks** (20-30 min): Execute task scenarios, observe, probe
4. **Post-task questionnaire**: SUS, SEQ, or custom scale after each task
5. **Debrief** (5 min): Overall impressions, open-ended feedback
6. **Post-test survey**: SUS (System Usability Scale) overall

### Step 5: Analysis Framework

| Metric | Measurement | Benchmark |
|--------|------------|-----------|
| Task success rate | % completed without help | >78% (industry average) |
| Time on task | Seconds per task | Compared to expert time |
| Error rate | Mistakes per task | <2 errors per task |
| SUS score | System Usability Scale | >68 (above average) |
| Satisfaction | Post-task rating | >4/5 |

## Output Format

```markdown
## Usability Test Plan: [Feature]

### Objectives
[Research questions]

### Methodology
[Format, tools, timeline]

### Participants
[Recruitment criteria, sample size, incentive]

### Task Scenarios
[Numbered task table]

### Test Script
[Moderator guide]

### Metrics & Analysis
[What to measure and how to interpret]

### Timeline
| Phase | Activity | Duration |
```

## Quality Checklist

- [ ] Research questions are specific and answerable through observation
- [ ] Tasks are realistic scenarios, not step-by-step instructions
- [ ] Participant criteria match actual target users
- [ ] Success metrics are defined before testing begins
- [ ] Moderator script avoids leading questions
- [ ] Analysis plan is defined upfront

## Edge Cases

- **Limited participant access**: Use guerilla testing with 3-5 participants; still valuable
- **Testing with internal users**: Acknowledge bias; they know more than real users
- **Accessibility testing**: Include participants with disabilities; test with assistive technology
- **Competitive benchmarking**: Test competitor's product with same tasks for comparison
