---
name: launch-readiness
description: "Help PMs ensure launches are well-planned with nothing falling through the cracks. Use before any feature launch, experiment rollout, or release."
---

# Launch Readiness

Help PMs run launch readiness checklists and make go/no-go recommendations. Ensures launches are planned, risks are surfaced, and stakeholders are aligned.

## When to Use

- Before a feature launch
- Before an experiment rollout
- Before a product release
- Go/no-go meeting prep
- When asked "are we ready to launch?"

## Process / Template

### 1. Define Launch Scope

- What is being launched? (feature, experiment, release)
- Target audience and rollout plan (% of users, segments)
- Launch date and any phased milestones

### 2. Run the Checklist

**Product & Quality**
- [ ] All P0/P1 bugs resolved or accepted
- [ ] Acceptance criteria met
- [ ] Edge cases and error states handled
- [ ] Rollback plan documented

**Technical**
- [ ] Feature flags / kill switches in place
- [ ] Monitoring and alerting configured
- [ ] Performance and load tested (if applicable)
- [ ] Data pipeline or analytics verified

**Legal, Compliance, Security**
- [ ] Legal review complete (if required)
- [ ] Privacy/compliance checks done
- [ ] Security review (if applicable)

**Go-to-Market**
- [ ] Support team briefed and docs updated
- [ ] Customer-facing comms ready (if applicable)
- [ ] Internal launch post drafted

**Stakeholders**
- [ ] Key stakeholders informed
- [ ] Escalation path defined
- [ ] Post-launch review scheduled

### 3. Assess Risks

- What could go wrong?
- Mitigation in place?
- Acceptable residual risk?

### 4. Make Go/No-Go Recommendation

| Status | Criteria |
|--------|----------|
| **Go** | All critical items green, risks acceptable |
| **Conditional Go** | Minor items open; launch with monitoring |
| **No-Go** | Critical gaps; delay until resolved |

### 5. Document Decision

- Summary of checklist outcome
- Open items and owners
- Go/no-go recommendation with rationale
- Next steps (if no-go or conditional)

## Output

A **Launch Readiness Summary** including:
- Checklist status (green/yellow/red per area)
- Risk assessment
- Go/no-go recommendation
- Open items with owners
- Post-launch plan (monitoring, review)
