---
name: launch-rollout-patterns
description: Phased rollout strategy, feature flag patterns, rollback trigger definition, and canary deployment criteria. Use when planning a product launch, designing a progressive rollout, or defining rollback thresholds.
---

# Launch Rollout Patterns

The safest launch is the one where nothing goes wrong at full scale because you caught the problem at 1% traffic. This skill covers the patterns for progressive rollout — from internal testing to full production — with clear success criteria and rollback triggers at each phase.

## When to Use This Skill

- Planning a rollout for a new feature or product
- Designing feature flag targeting for progressive exposure
- Defining rollback triggers before launch (not during an incident)
- Planning a geographic or segment-based rollout
- Reviewing a launch plan for missing safeguards

## Core Concepts

### 1. Never Big-Bang Launch

A big-bang launch (feature off → feature on for everyone simultaneously) removes your ability to:
- Attribute metric changes to the feature specifically
- Catch errors before they affect your entire user base
- Roll back without a full production incident

Every meaningful feature launch should be phased.

### 2. Define Rollback Triggers Before Launch

Rollback criteria decided during an incident are criteria decided under pressure. The question is not "should we roll back?" but "we already agreed we would roll back at this threshold — do we do it now?"

### 3. Success Thresholds, Not Just Error Thresholds

Define both what success looks like (proceed to next phase) AND what failure looks like (roll back). Without success thresholds, a rollout stays in limbo indefinitely.

## Standard Rollout Phases

```
Phase 0: Internal Testing
  Target: Internal team + selected employees
  Duration: Until no critical bugs found
  Proceed to Phase 1 when: Zero P0/P1 bugs in 48 hours

Phase 1: Alpha (Limited Beta)
  Target: 1-5% of production traffic / invited users
  Duration: 1-2 weeks minimum
  Proceed to Phase 2 when: [defined success criteria]
  Roll back when: [defined thresholds]

Phase 2: Expanded Beta
  Target: 10-25% of traffic
  Duration: 1-2 weeks
  Proceed to Phase 3 when: [defined success criteria]
  Roll back when: [defined thresholds]

Phase 3: Broad Rollout
  Target: 50-75% of traffic
  Duration: 1 week
  Proceed to Phase 4 when: [defined success criteria]
  Roll back when: [defined thresholds]

Phase 4: Full Rollout
  Target: 100% of eligible users
  Post-launch monitoring: 2 weeks active monitoring
```

Adjust phases based on feature risk level:
- **Low risk** (copy change, minor UI): Phase 0 → Phase 4 directly
- **Medium risk** (new UX, new flow): All phases, compressed timelines
- **High risk** (payment, auth, data model): All phases, extended timelines, extra monitoring

## Rollback Trigger Definition

### Template

```markdown
## Rollback Triggers: [Feature Name]

### Automatic Rollback (no human decision required)
These conditions trigger immediate rollback without waiting for approval:
- Error rate on [endpoint] exceeds [X]% for 5+ consecutive minutes
- [Metric] drops below [threshold] in any 1-hour window
- [P1 or higher bug] confirmed in production

### Manual Rollback (human decision required within 30 minutes)
These conditions trigger a team review and rollback decision:
- Conversion rate on [flow] drops > [X]pp from baseline
- Support ticket volume increases > [X]% vs. same period previous week
- NPS score drops > [X] points within 48 hours of rollout expansion

### Rollback Procedure
1. Disable feature flag for current cohort
2. Confirm metric recovery within 15 minutes
3. File incident report
4. Notify stakeholders
5. Root cause analysis before re-launch
```

### Threshold Setting Guidelines

| Metric | Conservative Threshold | Aggressive Threshold |
|--------|----------------------|---------------------|
| Error rate increase | > 1x baseline | > 3x baseline |
| Core conversion drop | > 2pp | > 5pp |
| Revenue impact | > 1% decrease | > 5% decrease |
| Support volume increase | > 20% | > 100% |
| Page load time increase | > 500ms P95 | > 1s P95 |

Use conservative thresholds for payment flows, auth, and data operations. Use aggressive thresholds for low-risk UI changes.

## Feature Flag Patterns

### Targeting Strategies

| Strategy | Use When | Implementation |
|----------|---------|---------------|
| **Percentage rollout** | Random exposure for A/B testing | Hash user ID to [0-100], enable for users < threshold |
| **Cohort targeting** | Target specific segments (new users, power users) | Match on user attribute |
| **Geographic targeting** | Phase by region (primary market → secondary) | Match on user location |
| **Beta opt-in** | Engaged users who want early access | Match on beta flag in user profile |
| **Employee-first** | Internal validation before external exposure | Match on internal user flag |

### Feature Flag States

```
OFF:     Feature completely disabled for all users
SHADOW:  Feature executes but output is not shown (backend validation)
BETA:    Feature visible to targeted cohort only
PARTIAL: Feature live for [X]% of traffic
FULL:    Feature live for all eligible users
SUNSET:  Feature disabled pending removal (post-deprecation)
```

### Flag Naming Convention

```
feature.[product-area].[feature-name].[variant]

Examples:
  feature.checkout.guest-checkout.enabled
  feature.listings.bulk-upload.rollout-pct
  feature.payments.split-payment.beta
```

## Geographic Rollout Sequencing

For products with multi-market presence:

```
Tier 1: Primary market (highest traffic, most test data)
  Launch here first. Most bugs found with the most signal.

Tier 2: Similar markets (comparable infrastructure, similar user behavior)
  Launch after Tier 1 is stable for [X] days.

Tier 3: Adjacent markets (different language, different infrastructure needs)
  Requires localization validation in addition to functional testing.

Tier 4: Emerging markets (lower bandwidth, different device distribution)
  Requires performance validation under constrained conditions.
```

## Launch Communication Plan

### Internal Communication

| Audience | Message | Timing |
|----------|---------|--------|
| Engineering | Technical details, rollback procedure, on-call escalation path | 48 hours before Phase 1 |
| Support | Feature summary, expected user questions, escalation path | 24 hours before each phase expansion |
| Leadership | Feature summary, launch plan, success metrics | 1 week before Phase 1 |
| All company | Feature announcement and availability | Phase 4 launch day |

### User Communication

- **Phase 0–2:** No external communication (internal / invited users only)
- **Phase 3:** Soft announcement to beta users
- **Phase 4:** Full release notes, in-app announcement (if warranted), external PR (if warranted)

## Post-Launch Monitoring Checklist

First 24 hours after each phase expansion:
- [ ] Error rates by endpoint (vs. baseline)
- [ ] Conversion rate for affected flows (vs. baseline)
- [ ] P95 latency for affected endpoints (vs. baseline)
- [ ] Support ticket volume and categorization (vs. baseline)
- [ ] Feature flag stats (coverage %, error segmentation between enabled/disabled)

## Best Practices

1. **Write rollback triggers before the launch plan is approved** — not after
2. **Run shadow mode for high-risk features** — execute the logic, don't show the results; validate the backend before the UI
3. **Instrument before Phase 1** — if tracking isn't in place for Phase 1, you're flying blind
4. **Set an expiry for feature flags** — flags that live forever become technical debt; schedule removal when full rollout is confirmed
5. **Socialize the rollback plan** — the engineering on-call must know the rollback procedure before launch day
