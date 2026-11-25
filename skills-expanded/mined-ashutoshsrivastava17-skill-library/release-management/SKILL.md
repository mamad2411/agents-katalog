---
name: release-management
description: >
  Manage IT releases — release planning, packaging, testing gates,
  deployment windows, communication, and post-release validation.
  TRIGGER when: user says /release-management, needs to plan a release,
  or asks about release coordination and deployment management.
argument-hint: "[release or deployment to plan]"
user-invocable: true
---

# Release Management

## Process
### Step 1: Define Release Scope
| Element | Details |
|---------|---------|
| Release ID | Unique identifier |
| Type | Major / Minor / Patch / Emergency |
| Components | Applications, infrastructure, config changes |
| Dependencies | Cross-team or external dependencies |
| Risk level | High / Medium / Low |

### Step 2: Plan Release
| Phase | Duration | Activities |
|-------|----------|-----------|
| Planning | 1-2 weeks | Scope, dependencies, risk assessment |
| Build | Per sprint | Development, unit testing |
| Testing | 1-2 weeks | Integration, regression, UAT |
| Staging | 1-3 days | Pre-production deployment, smoke tests |
| Production | Scheduled window | Deployment, validation |
| Hypercare | 1-7 days | Enhanced monitoring, rapid response |

### Step 3: Define Testing Gates
| Gate | Criteria | Owner |
|------|----------|-------|
| Code complete | All features merged, no blockers | Dev lead |
| QA signoff | Test plan executed, no P1/P2 bugs | QA lead |
| Security scan | No critical/high vulnerabilities | Security |
| Performance | Meets SLA benchmarks | Performance team |
| UAT | Business stakeholder approval | Product owner |

### Step 4: Schedule Deployment
| Factor | Consideration |
|--------|-------------|
| Window | Low-traffic period, team availability |
| Duration | Estimated deployment time + buffer |
| Rollback | Maximum time before rollback decision |
| Communication | Stakeholder notification schedule |
| On-call | Support team coverage during and after |

### Step 5: Execute Release
| Step | Action | Verification |
|------|--------|-------------|
| 1 | Pre-deployment checklist complete | Signoff |
| 2 | Deploy to production | Deployment success |
| 3 | Smoke tests | Critical paths working |
| 4 | Monitor dashboards | No anomalies |
| 5 | Notify stakeholders | Confirmation sent |
| 6 | Begin hypercare | Enhanced monitoring active |

### Step 6: Post-Release Review
| Question | Answer |
|----------|--------|
| Did the release go as planned? | |
| Were there any issues? | |
| What could improve next time? | |
| Are all success criteria met? | |

## Output Format
```markdown
## Release Plan: [ID]
### Scope: [components and changes]
### Schedule: [timeline with gates]
### Risk: [assessment and mitigations]
### Communication: [notification plan]
```

## Quality Checklist
- [ ] All testing gates passed
- [ ] Rollback plan documented and tested
- [ ] Communication sent to stakeholders
- [ ] Deployment window confirmed
- [ ] Monitoring enhanced for hypercare
- [ ] Post-release review scheduled

## Edge Cases
- For emergency releases, use abbreviated process with post-hoc review
- For zero-downtime requirements, use blue-green or canary deployments
- If multiple teams coordinate, assign a release manager as single point
