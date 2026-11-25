---
name: beta-program
description: >
  Design beta programs — participant selection, feedback collection, bug triage,
  success criteria, NDA management, and graduation criteria.
  TRIGGER when: user says /beta-program or asks about running a beta test.
argument-hint: "[feature or product to beta test]"
user-invocable: true
---
# Beta Program Design
## Process
### Step 1: Define Beta Scope
| Element | Details |
|---------|---------|
| Feature/product | What's being tested |
| Beta type | Closed (invite) / Open / Public preview |
| Duration | Typical 2-6 weeks |
| Participants | Target count (10-50 for closed, more for open) |
| Goals | What you want to learn |
### Step 2: Select Participants
| Criteria | Priority |
|----------|---------|
| Represents target persona | Must |
| Active product user | Should |
| Willing to provide feedback | Must |
| Diverse use cases | Should |
| Technical sophistication matches product | Should |
### Step 3: Set Up Feedback Collection
| Channel | Purpose | Cadence |
|---------|---------|---------|
| In-app feedback | Bug reports, feature requests | Continuous |
| Survey | Structured assessment | Weekly or end-of-beta |
| Interview | Deep qualitative insight | 5-8 participants |
| Usage analytics | Behavioral data | Continuous |
| Community/forum | Peer discussion | Continuous |
### Step 4: Manage Bug Triage
| Severity | Response | Action |
|----------|----------|--------|
| Blocker | 4 hours | Hotfix or workaround |
| Critical | 24 hours | Fix in next beta build |
| Major | 48 hours | Fix before GA |
| Minor | 1 week | Backlog for GA or post-GA |
### Step 5: Define Graduation Criteria
| Criterion | Threshold |
|-----------|----------|
| No blocker/critical bugs | 0 open |
| User satisfaction | NPS > X or CSAT > X/5 |
| Core workflow completion | > 90% can complete key tasks |
| Performance | Meets SLA targets |
| Documentation | Complete and reviewed |
### Step 6: Transition to GA
- Thank beta participants (recognition, early access, swag)
- Communicate changes made based on feedback
- Archive beta feedback for future reference
- Update documentation with beta learnings
## Output Format
```markdown
## Beta Program: [Feature]
### Scope: [What, duration, participant count]
### Selection: [Criteria and recruitment plan]
### Feedback: [Collection methods]
### Graduation: [Criteria for GA readiness]
```
## Quality Checklist
- [ ] Beta goals clearly defined
- [ ] Participant selection criteria documented
- [ ] Feedback channels set up before launch
- [ ] Bug triage process established
- [ ] Graduation criteria are specific and measurable
## Edge Cases
- For enterprise beta, involve customer success in recruitment
- If beta reveals major issues, plan for extended beta
- For public beta, prepare for support volume
