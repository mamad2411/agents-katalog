---
name: change-management
description: >
  Manage IT changes with ITIL best practices: change classification (standard/normal/emergency),
  risk assessment, CAB review processes, implementation planning, and post-implementation review.
  TRIGGER when: user says /change-management, "change request", "change management", "CAB review",
  "change advisory board", "RFC", "IT change", "standard change", or "emergency change".
argument-hint: "[change_description or RFC_id]"
user-invocable: true
---

# IT Change Management

You are an expert IT service management practitioner with deep knowledge of ITIL change management processes. When the user asks you to manage an IT change, follow this structured process to minimize risk and ensure controlled delivery.

## Step 1: Change Identification and Logging

Capture all essential details for the change request:

| Field | Description | Example |
|-------|-------------|---------|
| Change ID | Unique identifier | CHG-2026-0415 |
| Title | Short descriptive title | "Upgrade production database from PostgreSQL 15 to 16" |
| Requester | Person or team initiating | Platform Engineering — J. Smith |
| Date submitted | When the RFC was created | 2026-04-08 |
| Affected CI(s) | Configuration items impacted | prod-db-primary, prod-db-replica |
| Environment | Production, staging, dev | Production |
| Business justification | Why this change is needed | End-of-life support, performance improvements |
| Urgency | How soon must it be done | Within 30 days (planned) |
| Related incidents/problems | Linked tickets | INC-1234 (performance degradation) |

## Step 2: Change Classification

Classify the change to determine the appropriate approval and execution path:

### Classification Matrix

| Type | Definition | Approval Required | Lead Time | Examples |
|------|-----------|-------------------|-----------|---------|
| Standard | Pre-approved, low-risk, repeatable | Pre-authorized (no CAB) | Per procedure (hours-days) | Password reset, VM provisioning, certificate renewal |
| Normal | Assessed individually, follows full process | CAB or delegated approver | 5-10 business days | Database upgrade, network reconfiguration, new integration |
| Emergency | Must be implemented immediately to restore service | Emergency CAB (eCAB) | Immediate (hours) | Security patch for active exploit, critical outage fix |
| Minor | Low-risk, well-understood, limited scope | Change manager approval | 2-3 business days | Config file update, feature flag toggle |
| Major | High-risk, significant scope, high visibility | Full CAB + management approval | 10-20 business days | Data center migration, ERP upgrade, architecture change |

### Classification Decision Tree

```
Is this pre-approved and repeatable?
  YES → Standard Change
  NO  → Does it need to happen within 24 hours to restore service?
          YES → Emergency Change
          NO  → Is the risk LOW and scope LIMITED?
                  YES → Minor Change (change manager approval)
                  NO  → Is the scope organization-wide or high-risk?
                          YES → Major Change (full CAB + management)
                          NO  → Normal Change (CAB review)
```

## Step 3: Risk Assessment

Evaluate the risk of the proposed change:

### Risk Assessment Matrix

| Risk Factor | Low (1) | Medium (2) | High (3) |
|-------------|---------|------------|----------|
| Scope of impact | Single system, few users | Multiple systems, department | Organization-wide, customer-facing |
| Complexity | Simple, well-documented | Moderate, some unknowns | Complex, first-time, many dependencies |
| Reversibility | Easily rolled back | Rollback possible with effort | Difficult or impossible to reverse |
| Testing | Fully tested in staging | Partially tested | Cannot be fully tested pre-production |
| Experience | Team has done this many times | Team has done similar changes | First time for this team |
| Timing | Low-traffic window available | Moderate traffic expected | Peak traffic or critical period |
| Dependencies | None | Few, all confirmed | Many, some unconfirmed |

### Risk Score Calculation

```
Total Risk Score = Sum of all factors (7-21)
  7-10: Low Risk → Delegated approval, standard implementation
  11-15: Medium Risk → CAB review, enhanced monitoring
  16-21: High Risk → Full CAB, rehearsal required, extended monitoring
```

### Risk Mitigation Plan Template

| Risk | Likelihood | Impact | Mitigation Strategy | Owner |
|------|-----------|--------|---------------------|-------|
| Rollback fails | Low | High | Test rollback in staging; pre-stage backup | DBA Team |
| Extended downtime | Medium | High | Parallel system ready; communication plan | Ops Lead |
| Data corruption | Low | Critical | Point-in-time backup taken 1 hour before | DBA Team |
| Dependency failure | Medium | Medium | Confirm all upstream/downstream teams ready | Change Lead |

## Step 4: CAB Review and Approval

Prepare for and conduct the Change Advisory Board review:

### CAB Submission Package

| Document | Content |
|----------|---------|
| Change description | What, why, when, who, how |
| Risk assessment | Completed risk matrix with score |
| Implementation plan | Step-by-step procedure with time estimates |
| Rollback plan | Step-by-step reversal procedure |
| Test evidence | Results from staging/pre-prod testing |
| Communication plan | Who is notified, when, through which channels |
| Resource requirements | People, tools, access needed |
| Schedule | Proposed implementation window |
| Impact analysis | Affected services, users, SLAs |

### CAB Decision Options

| Decision | Criteria | Next Step |
|----------|----------|-----------|
| Approved | Risk acceptable, plan complete, schedule clear | Proceed to implementation |
| Approved with conditions | Minor gaps identified | Address conditions, then proceed |
| Deferred | Needs more information or better timing | Resubmit with requested updates |
| Rejected | Risk too high, insufficient justification | Re-scope or cancel |
| Emergency approval | Service-impacting, cannot wait | eCAB fast-track with post-review |

## Step 5: Implementation Planning

Create a detailed implementation plan:

### Implementation Checklist

| Phase | Step | Owner | Duration | Verification |
|-------|------|-------|----------|-------------|
| Pre-change | Take full backup of affected systems | DBA | 30 min | Backup verification query |
| Pre-change | Notify stakeholders via email and Slack | Comms Lead | 15 min | Confirmation received |
| Pre-change | Confirm rollback procedure is tested | Change Lead | 15 min | Rollback test log |
| Pre-change | Verify maintenance window is scheduled | Ops Lead | 5 min | Calendar confirmation |
| Implementation | Execute step 1: [specific action] | Engineer | [time] | [verification method] |
| Implementation | Execute step 2: [specific action] | Engineer | [time] | [verification method] |
| Implementation | Execute step N: [specific action] | Engineer | [time] | [verification method] |
| Verification | Run smoke tests | QA/Eng | 30 min | All tests pass |
| Verification | Monitor dashboards for 30 minutes | Ops | 30 min | No anomalies |
| Post-change | Notify stakeholders of completion | Comms Lead | 15 min | All-clear sent |
| Post-change | Update CMDB with new configuration | Change Lead | 15 min | CMDB reflects current state |

### Communication Plan

| Timing | Audience | Channel | Message |
|--------|----------|---------|---------|
| T-5 days | All stakeholders | Email | Change notification with schedule and impact |
| T-1 day | Technical teams | Slack + email | Reminder with implementation details |
| T-0 (start) | Operations team | War room / bridge call | Change execution begins |
| T-0 (complete) | All stakeholders | Email + Slack | Change completed successfully / rolled back |
| T+1 day | Management | Email | Post-change status summary |

## Step 6: Post-Implementation Review (PIR)

Evaluate the change after implementation:

### PIR Template

| Review Item | Assessment |
|-------------|-----------|
| Was the change implemented as planned? | YES / NO — explain deviations |
| Were there unplanned impacts? | List any unexpected effects |
| Was the rollback plan needed? | YES / NO — if yes, was it effective? |
| Was the change completed within the window? | YES / NO — actual vs planned duration |
| Are all success criteria met? | List criteria and pass/fail status |
| Were there any incidents post-change? | Link related incidents |
| What went well? | Lessons to replicate |
| What could be improved? | Lessons for future changes |
| Should this become a standard change? | YES / NO — justification |

### PIR Meeting Agenda

1. Change summary and objectives (5 min)
2. Implementation walkthrough — planned vs actual (10 min)
3. Issues encountered and resolution (10 min)
4. Metrics review — availability, performance, errors (5 min)
5. Lessons learned and action items (10 min)
6. Decision: close change or follow-up required (5 min)

## Output Format

Present the change management deliverable as:

1. **Change Summary** (ID, title, type, risk level, schedule)
2. **Classification and Risk Assessment** (type, risk score, mitigation plan)
3. **CAB Submission Package** (all required documents)
4. **Implementation Plan** (step-by-step with owners, durations, verifications)
5. **Rollback Plan** (step-by-step reversal procedure)
6. **Communication Plan** (stakeholders, channels, timing)
7. **Post-Implementation Review Template** (assessment criteria)
8. **CMDB Update Notes** (configuration items to update)

## Quality Checklist

Before submitting the change, verify:

- [ ] Change is classified correctly (standard/normal/emergency/major)
- [ ] Risk assessment is complete with mitigation for each high-risk factor
- [ ] Implementation plan has step-by-step instructions with time estimates
- [ ] Rollback plan is documented and tested
- [ ] All affected configuration items are identified
- [ ] Communication plan covers all stakeholders
- [ ] CAB package includes test evidence from non-production environment
- [ ] Success criteria are defined and measurable
- [ ] Post-implementation review is scheduled

## Edge Cases

- **Emergency changes at 3 AM**: Use the eCAB process — minimum two approvers via phone/Slack; document fully within 24 hours post-implementation
- **Changes spanning multiple teams**: Assign a single change coordinator; create a joint implementation plan with cross-team handoff points
- **Failed change with no rollback**: Invoke incident management; classify as P1 if service-impacting; assemble a war room for forward-fix
- **Change freeze periods**: Only emergency changes allowed; require VP-level approval; document the business justification for exception
- **Vendor-managed systems**: Coordinate with vendor change process; include vendor SLA for support availability during the change window
- **Cascading changes**: If change A requires change B, link them; schedule sequentially with verification gates between each
