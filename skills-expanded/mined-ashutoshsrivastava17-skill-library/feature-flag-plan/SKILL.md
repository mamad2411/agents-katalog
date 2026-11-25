---
name: feature-flag-plan
description: >
  Plan feature flag implementations — flag types, lifecycle management, targeting rules, rollout strategies, cleanup processes, and tech debt prevention.
  TRIGGER when: user says /feature-flag-plan, needs to implement feature flags, or asks about progressive rollout strategies.
argument-hint: "[system or project context]"
user-invocable: true
---

# Feature Flag Plan

You are a software delivery specialist. Design a feature flag strategy that enables safe progressive rollouts while managing technical debt.

## Process

### Step 1: Classify Flag Types
| Type | Lifespan | Example | Cleanup |
|------|----------|---------|---------|
| Release flag | Days-weeks | New feature rollout | Remove after 100% rollout |
| Experiment flag | Weeks | A/B test variant | Remove after decision |
| Ops flag | Permanent | Kill switch, circuit breaker | Keep, review annually |
| Permission flag | Permanent | Premium feature gating | Keep, managed by product |

### Step 2: Design Flag Lifecycle
| Phase | Activities |
|-------|-----------|
| Create | Define flag, set default (off), document purpose and owner |
| Configure | Set targeting rules, rollout percentage |
| Rollout | Progressive: 1% → 10% → 50% → 100% with monitoring |
| Evaluate | Measure impact, decide ship/revert |
| Cleanup | Remove flag code, delete flag definition, close ticket |

### Step 3: Define Targeting Rules
| Rule Type | Use Case |
|-----------|----------|
| Percentage | Gradual rollout to random % of users |
| User segment | Beta users, internal, enterprise tier |
| Geography | Region-specific launches |
| Device/platform | Mobile-only, desktop-only |
| Time-based | Enable during business hours only |

### Step 4: Set Monitoring Requirements
For each flag rollout, monitor:
| Metric | Check |
|--------|-------|
| Error rates | No increase vs control |
| Performance | Latency within SLA |
| Business metrics | Conversion, engagement as expected |
| Rollback trigger | Auto-disable if error rate > threshold |

### Step 5: Prevent Technical Debt
| Practice | Details |
|----------|---------|
| Expiration dates | Every release flag gets a cleanup deadline |
| Flag audit | Monthly review of all active flags |
| Stale flag alerts | Alert if flag is > 30 days old and still partial |
| Maximum active flags | Limit to N active release flags per service |
| Code review | Flag cleanup is part of the definition of done |

### Step 6: Select Tooling
| Tool | Type | Strengths |
|------|------|----------|
| LaunchDarkly | SaaS | Full-featured, enterprise, SDKs for all platforms |
| Unleash | Open source | Self-hosted, good feature set |
| Flagsmith | Open source/SaaS | Simple, good API |
| Split | SaaS | Experimentation focus |
| Custom | In-house | Full control, no vendor dependency |

## Output Format
```markdown
## Feature Flag Plan: [Feature Name]
### Flag: [name] | Type: [release/experiment/ops/permission]
### Targeting: [rules]
### Rollout: [phase plan with percentages]
### Monitoring: [metrics to watch]
### Cleanup: [deadline and owner]
```

## Quality Checklist
- [ ] Flag type and lifecycle are defined
- [ ] Targeting rules are documented
- [ ] Monitoring is configured before rollout
- [ ] Rollback mechanism tested
- [ ] Cleanup deadline set
- [ ] No more than N active release flags

## Edge Cases
- For server + client flags, ensure consistency (avoid flicker)
- If flag evaluation is latency-sensitive, use local evaluation with cached config
- For flags that control database migrations, plan carefully (can't easily toggle back)
- If regulations require audit trails, ensure flag changes are logged
