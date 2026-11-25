---
name: automation-audit
description: >
  Audit workflows for automation — task inventory, repetition frequency,
  complexity scoring, tool selection, ROI estimation, and implementation priority.
  TRIGGER when: user says /automation-audit or asks about automating repetitive tasks.
argument-hint: "[workflow or team to audit]"
user-invocable: true
---
# Automation Audit
## Process
### Step 1: Inventory Tasks
| Task | Frequency | Duration | Who | Automatable? |
|------|-----------|----------|-----|-------------|
| [task] | Daily/Weekly/Monthly | X min | [role] | Full/Partial/No |
### Step 2: Score Automation Potential
| Criteria | Weight | Score (1-5) |
|----------|--------|------------|
| Repetition frequency | 25% | Higher = more frequent |
| Rule-based (vs judgment) | 25% | Higher = more rule-based |
| Error-prone | 20% | Higher = more error-prone |
| Time consuming | 15% | Higher = more time |
| Data availability | 15% | Higher = more structured |
### Step 3: Estimate ROI
| Task | Hours/Month | Automation Cost | Payback Period |
|------|-----------|----------------|---------------|
| [task] | X hours | $X (one-time) | X months |
### Step 4: Select Tools
| Approach | Examples | Best For |
|----------|---------|---------|
| No-code | Zapier, Make, Power Automate | Simple integrations |
| Low-code | Retool, n8n | Data workflows |
| Scripts | Python, Bash | Technical teams |
| RPA | UiPath, Automation Anywhere | Legacy system interaction |
| AI/LLM | Claude, GPT | Unstructured data processing |
### Step 5: Prioritize Implementation
| Priority | Task | ROI | Effort | Confidence |
|----------|------|-----|--------|-----------|
| 1 | [task] | High | Low | High |
## Output Format
```markdown
## Automation Audit: [Scope]
### Inventory: [Task list with automation scores]
### Top Opportunities: [Ranked by ROI]
### Tool Recommendations: [Per task]
### Implementation Plan: [Phased timeline]
```
## Quality Checklist
- [ ] All repetitive tasks inventoried
- [ ] Automation potential scored objectively
- [ ] ROI calculated with realistic estimates
- [ ] Tool selection matches team capability
- [ ] Implementation prioritized by value
## Edge Cases
- For tasks requiring judgment, consider AI-assisted (not fully automated) approaches
- If team lacks technical skills, prioritize no-code solutions
- For regulated processes, ensure audit trail in automated workflows
