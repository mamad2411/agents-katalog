---
name: workflow-design
description: >
  Design operational workflows — process mapping, role assignments, automation opportunities, approval chains, SLA definition, and exception handling.
  TRIGGER when: user says /workflow-design, needs to design a new workflow, or asks about process design and automation.
argument-hint: "[relevant context]"
user-invocable: true
---

# Workflow Design
## Process
### Step 1: Document Current State
| Element | Details |
|---------|---------|
| Process name | What workflow to design/redesign |
| Trigger | What initiates the workflow |
| Inputs | What information/materials are needed |
| Steps | Current sequence of activities |
| Outputs | What the workflow produces |
| Stakeholders | Who is involved at each step |
### Step 2: Map the Process
For each step:
| Step | Actor | Action | System | Duration | Decision? |
|------|-------|--------|--------|----------|----------|
| 1 | [role] | [action] | [tool] | [time] | Y/N |
### Step 3: Identify Improvements
| Issue | Type | Impact |
|-------|------|--------|
| Manual data entry | Automation opportunity | Time savings |
| Email approvals | Bottleneck | Cycle time |
| Unclear ownership | Role ambiguity | Delays |
| No SLA | Missing accountability | Variable quality |
### Step 4: Design New Workflow
- Define clear triggers and entry criteria
- Assign ownership for each step
- Set SLAs for time-sensitive steps
- Add approval gates only where necessary
- Design exception handling paths
### Step 5: Plan Automation
| Step | Automation Type | Tool |
|------|----------------|------|
| [step] | Full automation | [tool] |
| [step] | Partial (human review) | [tool] |
| [step] | Notification/routing | [tool] |
### Step 6: Define SLAs
| Step | SLA | Escalation |
|------|-----|-----------|
| [step] | X hours | Notify manager |
| [step] | X days | Auto-reassign |
## Output Format
```markdown
## Workflow: [Name]
### Trigger: [What starts it]
### Steps: [Sequence with roles and SLAs]
### Automation: [What can be automated]
### SLAs: [Time targets]
```
## Quality Checklist
- [ ] Current state documented before redesigning
- [ ] Each step has a clear owner
- [ ] SLAs defined for critical steps
- [ ] Exception paths handled
- [ ] Automation opportunities identified
## Edge Cases
- For cross-department workflows, get agreement from all stakeholders
- If automating, plan for edge cases that require human judgment
- For regulated processes, ensure compliance at each step
