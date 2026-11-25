---
name: resource-planning
description: >
  Plan operational resources — demand forecasting, capacity modeling, skill matrix, utilization targets, and contingency planning.
  TRIGGER when: user says /resource-planning, needs to plan resource allocation, or asks about capacity planning.
argument-hint: "[relevant context]"
user-invocable: true
---

# Resource Planning
## Process
### Step 1: Assess Current Capacity
| Resource | Available | Utilized | Remaining |
|----------|----------|---------|-----------|
| [team/role] | X FTE | X FTE (X%) | X FTE |
### Step 2: Forecast Demand
| Project/Initiative | Resources Needed | Timeline | Priority |
|-------------------|-----------------|----------|----------|
| [project] | X FTE of [role] | [dates] | H/M/L |
### Step 3: Identify Gaps
| Role | Supply | Demand | Gap | Strategy |
|------|--------|--------|-----|---------|
| [role] | X FTE | X FTE | X FTE | Hire/Contract/Defer |
### Step 4: Build Allocation Plan
| Resource | Q1 | Q2 | Q3 | Q4 |
|----------|-----|-----|-----|-----|
| [name/role] | [project] | [project] | [project] | [project] |
### Step 5: Plan Contingencies
| Risk | Mitigation |
|------|-----------|
| Key person unavailable | Cross-training, backup assignments |
| Demand exceeds plan | Pre-approved contractor list |
| Project delayed | Reallocation plan |
## Output Format
```markdown
## Resource Plan: [Period]
### Capacity: [Current state]
### Demand: [Forecast by project]
### Gaps: [Shortfalls and strategies]
### Allocation: [Assignment matrix]
```
## Quality Checklist
- [ ] Current capacity accurately measured
- [ ] Demand forecast includes all known projects
- [ ] Gaps have clear fill strategies
- [ ] Allocation avoids single points of failure
- [ ] Contingency plans exist for key risks
## Edge Cases
- For shared resources, establish priority rules and escalation
- If demand significantly exceeds supply, force-rank projects
- For seasonal businesses, plan for peak/off-peak staffing
