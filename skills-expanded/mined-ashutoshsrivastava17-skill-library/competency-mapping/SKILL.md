---
name: competency-mapping
description: >
  Map organizational competencies — frameworks, job-role alignment,
  proficiency levels, gap analysis, and development pathway design.
  TRIGGER when: user says /competency-mapping, needs to build competency
  frameworks, or asks about skill mapping and career ladders.
argument-hint: "[department or role family to map]"
user-invocable: true
---
# Competency Mapping
## Process
### Step 1: Identify Competency Areas
| Category | Examples |
|----------|---------|
| Technical | Programming, data analysis, design tools |
| Functional | Project management, sales methodology, financial analysis |
| Leadership | Strategic thinking, people management, decision-making |
| Core | Communication, collaboration, problem-solving |
### Step 2: Define Proficiency Levels
| Level | Description | Indicators |
|-------|-----------|-----------|
| 1 - Foundational | Basic understanding, requires guidance | Can describe concepts |
| 2 - Developing | Can apply with some support | Completes tasks with review |
| 3 - Proficient | Works independently, consistent quality | Handles standard scenarios |
| 4 - Advanced | Handles complex situations, mentors others | Innovates and improves |
| 5 - Expert | Organizational authority, shapes strategy | Industry recognized |
### Step 3: Map to Roles
| Role | Competency | Required Level | Current Avg |
|------|-----------|---------------|------------|
| Junior Engineer | Programming | 2 | 1.8 |
| Senior Engineer | Programming | 4 | 3.5 |
| Engineering Manager | People management | 3 | 2.5 |
### Step 4: Conduct Gap Analysis
| Team/Individual | Competency | Required | Current | Gap | Priority |
|----------------|-----------|----------|---------|-----|---------|
| [name/team] | [competency] | X | X | X | H/M/L |
### Step 5: Design Development Pathways
| Gap | Development Options |
|-----|-------------------|
| 1 level | Self-study, e-learning, peer learning |
| 2 levels | Formal training + mentoring + practice |
| 3+ levels | Structured program + coaching + stretch assignments |
## Output Format
```markdown
## Competency Map: [Scope]
### Framework: [Competency areas and levels]
### Role Mapping: [Roles × competencies matrix]
### Gaps: [Priority gaps with development plans]
```
## Quality Checklist
- [ ] Competencies aligned with business strategy
- [ ] Proficiency levels are observable and measurable
- [ ] Role mapping validated with managers
- [ ] Gap analysis uses actual assessment data
- [ ] Development pathways are practical and resourced
## Edge Cases
- For new roles, benchmark competencies against industry standards
- If self-assessment is the only data source, calibrate with manager input
- For cross-functional roles, map competencies from multiple families
