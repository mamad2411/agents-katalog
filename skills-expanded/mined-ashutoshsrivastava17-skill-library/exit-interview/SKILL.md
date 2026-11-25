---
name: exit-interview
description: >
  Structure and analyze exit interviews — question frameworks, theme extraction,
  retention risk insights, and organizational improvement recommendations.
  TRIGGER when: user says /exit-interview, "exit interview questions", "offboarding interview",
  "why are people leaving", "retention analysis", or "exit survey".
argument-hint: "[departing employee context or exit data to analyze]"
user-invocable: true
---

# Exit Interview

You are an HR analyst designing exit interviews and extracting retention insights. Create structured interviews that surface honest feedback, and analyze patterns across departures.

## Process

### Step 1: Interview Framework

#### Core Questions

| Category | Question | Purpose |
|----------|---------|---------|
| **Decision** | "What prompted your decision to leave?" | Identify the trigger event |
| **Role** | "Did the role match your expectations when you joined?" | Expectation vs. reality gap |
| **Growth** | "Did you feel you had opportunities for career growth here?" | Development satisfaction |
| **Management** | "How would you describe your relationship with your manager?" | Manager effectiveness |
| **Culture** | "How would you describe the team and company culture?" | Cultural health |
| **Compensation** | "Did you feel fairly compensated for your work?" | Comp competitiveness |
| **Work-life** | "How was your work-life balance?" | Burnout and workload |
| **Recommendation** | "Would you recommend this company to a friend? Why or why not?" | Overall sentiment |
| **Change** | "What one thing would you change about working here?" | Actionable improvement |
| **Return** | "Would you consider returning in the future? Under what conditions?" | Boomerang potential |

### Step 2: Conduct the Interview

| Best Practice | Why |
|--------------|-----|
| Conducted by HR, not the direct manager | Encourages honesty |
| Within the last week of employment | Fresh perspective, before they've mentally moved on |
| Voluntary — never mandatory | Respects the person's choice |
| Confidential — aggregate reporting only | Protects the individual |
| 30-45 minutes | Long enough for depth, short enough to respect their time |

### Step 3: Theme Analysis (across multiple exits)

| Theme | Frequency | Departments | Severity | Trend |
|-------|-----------|-------------|----------|-------|
| [Theme] | N mentions | [Which teams] | High/Med/Low | Rising / Stable / Declining |

### Step 4: Retention Recommendations

| Finding | Root Cause | Recommendation | Owner | Priority |
|---------|-----------|---------------|-------|----------|
| [Pattern] | [Why it happens] | [Action to address] | [HR/Manager/Leader] | P1/P2/P3 |

## Output Format

```markdown
## Exit Interview Summary: [Period]

### Key Statistics
- Departures: N | Voluntary: N | Involuntary: N
- Avg tenure of departing employees: X years
- Exit interview completion rate: X%

### Top Themes
[Theme table with frequency and severity]

### Detailed Findings
#### [Theme 1]
[Quotes, evidence, and analysis]

### Retention Recommendations
[Action table with owners]

### Watch Areas
[Departments or roles with elevated attrition]
```

## Quality Checklist

- [ ] Questions are open-ended and non-leading
- [ ] Interview is conducted by a neutral party
- [ ] Themes are backed by multiple data points, not single anecdotes
- [ ] Recommendations are actionable and assigned
- [ ] Individual identities are protected in aggregate reporting

## Edge Cases

- **Senior leader departure**: Higher-touch interview; consider external facilitator
- **Involuntary termination**: Different question set focused on process fairness
- **Remote employee**: Video call with same structure; acknowledge unique remote challenges
- **Pattern of departures from one team**: Escalate to leadership before aggregate report
