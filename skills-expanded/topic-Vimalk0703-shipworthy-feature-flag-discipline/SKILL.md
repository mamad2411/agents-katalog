---
name: feature-flag-discipline
description: Manage feature flags with discipline -- expiration dates, kill switches, percentage rollouts, user targeting, and mandatory cleanup. Prevent feature flags from becoming permanent tech debt.
invoke_when: Use when implementing feature flags, planning a gradual rollout, adding a kill switch, cleaning up stale flags, or reviewing code that uses feature toggles.
---

# Feature Flag Discipline

## Core Principle

Feature flags are a deployment tool, not a permanent branching mechanism. Every flag must have an expiration date, an owner, and a cleanup plan. A flag at 100% for more than 30 days is tech debt, not a feature flag.

---

## 1. Flag Types and Lifecycle

| Flag Type | Purpose | Lifespan | Example |
|---|---|---|---|
| **Release flag** | Decouple deployment from release | Days to weeks | `enable_new_checkout_flow` |
| **Experiment flag** | A/B testing | Weeks (until statistically significant) | `experiment_pricing_page_v2` |
| **Ops flag** | Kill switch for operational control | Permanent (but rarely toggled) | `enable_recommendation_engine` |
| **Permission flag** | User entitlements and access | Permanent (managed by product) | `enable_enterprise_sso` |

**Only ops flags and permission flags are allowed to live permanently. Release flags and experiment flags must be removed after rollout or experiment completion.**

---

## 2. Flag Registration -- Required Metadata

Every flag must be registered with the following metadata at creation time:

```typescript
interface FeatureFlag {
  key: string;                    // e.g., "enable_new_checkout_flow"
  type: 'release' | 'experiment' | 'ops' | 'permission';
  owner: string;                  // Team or individual responsible
  description: string;            // What this flag controls
  createdAt: string;              // ISO date
  expiresAt: string;              // ISO date -- REQUIRED for release and experiment flags
  jiraTicket: string;             // Cleanup ticket created at flag creation time
  defaultValue: boolean;          // What happens if the flag system is down
  killSwitchSafe: boolean;        // Can this be turned off instantly without data loss?
}
```

### Example Registration

```typescript
const flags = {
  enable_new_checkout_flow: {
    key: 'enable_new_checkout_flow',
    type: 'release',
    owner: 'payments-team',
    description: 'Enables the redesigned checkout flow with Apple Pay support',
    createdAt: '2025-06-01',
    expiresAt: '2025-07-15',
    jiraTicket: 'PAY-1234',
    defaultValue: false,         // If flag system is down, use old checkout
    killSwitchSafe: true,        // Can disable instantly, user retries with old flow
  },
};
```

---

## 3. Kill Switches -- Disable in Under 1 Minute

Every non-trivial feature must have a kill switch that can disable it in under 1 minute, without a deployment.

### Requirements

- Kill switch toggles are propagated to all instances within 60 seconds.
- Kill switches do not require a code deployment.
- Kill switches do not require database migrations to take effect.
- The kill switch must be accessible to on-call engineers (not just the feature owner).

### Implementation Pattern

```typescript
// Flag evaluation with fast propagation
class FeatureFlagClient {
  private cache: Map<string, boolean> = new Map();
  private pollInterval: NodeJS.Timeout;

  constructor(private flagService: FlagService) {
    // Poll every 10 seconds for flag changes
    this.pollInterval = setInterval(() => this.refresh(), 10_000);
    this.refresh(); // Initial load
  }

  async refresh(): Promise<void> {
    try {
      const flags = await this.flagService.getAllFlags();
      this.cache = new Map(flags.map(f => [f.key, f.enabled]));
    } catch (error) {
      // On failure, keep using cached values -- do not clear the cache
      logger.warn('Failed to refresh feature flags, using cached values', { error });
    }
  }

  isEnabled(flagKey: string, context?: FlagContext): boolean {
    // If flag system is completely down and cache is empty, use default
    if (!this.cache.has(flagKey)) {
      return getDefaultValue(flagKey);
    }
    return this.cache.get(flagKey)!;
  }
}
```

### Kill Switch Checklist for On-Call

```markdown
## Kill Switch Runbook

1. Go to [Flag Management Dashboard URL].
2. Search for the flag key.
3. Toggle the flag to OFF.
4. Verify propagation: check the /debug/flags endpoint on 2-3 instances.
5. Verify user-facing behavior: test the affected flow manually.
6. Notify the flag owner in Slack.
```

---

## 4. Percentage Rollout

Roll out gradually to catch issues before they affect all users.

### Recommended Rollout Schedule

| Day | Percentage | Verification |
|---|---|---|
| Day 1 | 1% | Monitor error rates, latency, and business metrics |
| Day 2 | 5% | Compare metrics between flag-on and flag-off cohorts |
| Day 3 | 25% | Check for edge cases in support tickets |
| Day 5 | 50% | Full metric comparison, stakeholder sign-off |
| Day 7 | 100% | Start the 30-day cleanup countdown |

### Implementation

```typescript
function isEnabledForUser(flagKey: string, userId: string, percentage: number): boolean {
  // Deterministic: same user always gets the same result for the same flag
  const hash = murmurhash3(flagKey + userId);
  const bucket = hash % 100;
  return bucket < percentage;
}

// Usage
if (isEnabledForUser('new_checkout_flow', user.id, rolloutPercentage)) {
  return renderNewCheckout();
} else {
  return renderOldCheckout();
}
```

**Critical rule:** The hash must be deterministic. The same user must consistently see the same variant. Never use `Math.random()` for rollout decisions -- it creates an inconsistent experience for the user.

---

## 5. User Targeting

Target specific user segments for testing before broad rollout.

### Targeting Rules (Evaluated in Order)

1. **Explicit overrides:** Specific user IDs always see flag on/off (for QA testing).
2. **Internal users:** Employees and beta testers see the flag first.
3. **Segment targeting:** Enterprise tier, region, plan type.
4. **Percentage rollout:** Gradual rollout to remaining users.

```typescript
function evaluateFlag(flagKey: string, user: User): boolean {
  const config = getFlagConfig(flagKey);

  // 1. Explicit override
  if (config.overrides[user.id] !== undefined) {
    return config.overrides[user.id];
  }

  // 2. Internal users
  if (config.enabledForInternal && user.isInternal) {
    return true;
  }

  // 3. Segment targeting
  for (const rule of config.targetingRules) {
    if (matchesRule(user, rule)) {
      return rule.enabled;
    }
  }

  // 4. Percentage rollout
  return isEnabledForUser(flagKey, user.id, config.percentage);
}
```

---

## 6. Flag Cleanup -- The 30-Day Rule

**Rule:** Any release or experiment flag that has been at 100% for more than 30 days must be cleaned up. The flag code, the old code path, and the flag registration are all removed.

### Automated Enforcement

```python
def find_stale_flags():
    """Run weekly to find flags that need cleanup."""
    stale_flags = []
    for flag in flag_service.get_all_flags():
        if flag.type not in ('release', 'experiment'):
            continue

        if flag.percentage == 100:
            days_at_full = (datetime.utcnow() - flag.full_rollout_date).days
            if days_at_full > 30:
                stale_flags.append({
                    "key": flag.key,
                    "owner": flag.owner,
                    "days_at_100": days_at_full,
                    "cleanup_ticket": flag.jira_ticket,
                })

    if stale_flags:
        send_slack_alert(
            channel="#engineering",
            message=f"Stale feature flags needing cleanup: {len(stale_flags)}",
            details=stale_flags,
        )
    return stale_flags
```

### Cleanup Process

1. Remove the flag evaluation from code -- make the new behavior permanent.
2. Remove the old code path that the flag was guarding.
3. Remove the flag registration from the flag service.
4. Delete any targeting rules and overrides.
5. Close the cleanup Jira ticket.
6. Update tests to remove flag-on/flag-off variants.

---

## 7. Testing with Flags

Every feature behind a flag must be tested in both states: flag on and flag off.

### Test Strategy

```typescript
describe('Checkout flow', () => {
  describe('with new_checkout_flow flag OFF (existing behavior)', () => {
    beforeEach(() => {
      featureFlags.override('new_checkout_flow', false);
    });

    it('renders the classic checkout page', () => {
      const page = renderCheckout();
      expect(page).toContain('Classic Checkout');
    });

    it('processes payment through legacy gateway', async () => {
      const result = await processPayment(order);
      expect(legacyGateway.charge).toHaveBeenCalled();
    });
  });

  describe('with new_checkout_flow flag ON (new behavior)', () => {
    beforeEach(() => {
      featureFlags.override('new_checkout_flow', true);
    });

    it('renders the new checkout page', () => {
      const page = renderCheckout();
      expect(page).toContain('New Checkout');
    });

    it('processes payment through new gateway', async () => {
      const result = await processPayment(order);
      expect(newGateway.charge).toHaveBeenCalled();
    });
  });

  describe('flag system unavailable (fallback)', () => {
    beforeEach(() => {
      featureFlags.simulateOutage();
    });

    it('falls back to default value (old behavior)', () => {
      const page = renderCheckout();
      expect(page).toContain('Classic Checkout');
    });
  });
});
```

---

## Checklist

- [ ] Every flag has an owner, description, type, and expiration date.
- [ ] A cleanup Jira ticket is created at the same time as the flag.
- [ ] Kill switches can disable a feature in under 1 minute without a deployment.
- [ ] Percentage rollouts use deterministic hashing (not random).
- [ ] Both flag states (on/off) are tested, including flag system unavailability.
- [ ] The default value (when the flag system is down) is the safe/existing behavior.
- [ ] No release or experiment flag has been at 100% for more than 30 days.
- [ ] A weekly job detects and alerts on stale flags.
- [ ] Flag evaluation is fast (< 1ms) and does not make network calls per evaluation.
- [ ] On-call engineers know how to toggle kill switches (runbook exists).
