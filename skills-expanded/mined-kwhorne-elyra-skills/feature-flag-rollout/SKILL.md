---
name: feature-flag-rollout
description: Plan and execute a safe feature rollout using flags - design the flag, ramp gradually, monitor, and clean up. Use when the user asks about feature flags, gradual rollout, dark launches, kill switches, canary releases, or A/B test plumbing.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep, edit
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [feature-flags, rollout, deployment]
---

# Feature Flag Rollout

A feature flag separates **deploy** from **release**. Used well, it makes shipping boring. Used badly, it creates a graveyard of dead branches and "wait, is this flag still doing something?"

## When to use

- "Roll this feature out behind a flag"
- "Plan a gradual launch for X"
- "Add a kill switch for Y"
- "Canary / dark launch …"
- "Clean up old flags"

## Decide: do you actually need a flag?

Flags have a cost (complexity, code paths, cleanup debt). Use them when:

- ✅ Risky change you want to **dark launch** or **canary**
- ✅ Need a **kill switch** for critical functionality
- ✅ Gradual **rollout by user/segment/region**
- ✅ **A/B test** plumbing
- ✅ Decouple deploy from launch (deploy now, announce later)

Skip flags when:

- ❌ Trivial low-risk change
- ❌ Refactor with no user-visible change
- ❌ You'd never actually turn it off
- ❌ The "flag" is really a config setting (use config)

## Flag types

| Type | Lifetime | Example |
|---|---|---|
| **Release flag** | Days to weeks | Roll out a new feature gradually |
| **Experiment flag** | Weeks | A/B test variant assignment |
| **Ops flag / Kill switch** | Indefinite | Disable expensive feature under load |
| **Permission flag** | Permanent (becomes entitlement) | Premium-only features |

The first two **must be cleaned up**. The last two are permanent and should be named differently so they aren't confused with rollout flags.

## Designing the flag

### Naming

- `<area>.<feature>.<variant>`: `checkout.new_address_form.enabled`
- Verbs/states, not adjectives: `enabled`, `enable_new_x`, `use_v2` — not `is_better`
- Include type prefix if it helps: `release_`, `ops_`, `exp_`

### Default

- **Default `false` in code.** If the flag service is unreachable, you should get the *old, safe* behavior — not the new untested one.
- Document the default in the flag definition.

### Evaluation point

- Evaluate **as close to the decision as possible** — easier to reason about, harder to leak between contexts
- Cache the evaluation per request, not per process (consistency within a request, freshness between)
- For user-facing flags: bucket by stable user ID so the same user gets the same answer on retries

### Boundary

A flag should wrap **one logical change**. If turning it off requires turning off three flags, you've split the change wrong.

```ts
// ✅ Single boundary
if (flags.checkout.new_address_form.enabled(user)) {
  return <NewAddressForm />;
}
return <OldAddressForm />;

// ❌ Scattered checks — old code dies a thousand cuts
if (flags.x) doA();
if (flags.x) doB();
if (flags.x) renderC();
```

## Rollout plan

Plan the ramp **before** flipping anything.

### Standard ramp

| Stage | Audience | Watch for | Duration |
|---|---|---|---|
| 0% | Internal only (staff/dogfooding) | Functional bugs, obvious breakage | 1–3 days |
| 1% | 1% of users | Error rate, latency, key metric | 1–2 days |
| 10% | 10% of users | Same + qualitative feedback | 2–3 days |
| 50% | 50% of users | Same + cohort comparison vs control | 2–3 days |
| 100% | Everyone | Tail still looks normal | — |

Pause and investigate at any stage if metrics regress. Pause is cheap; rolling back from 100% with no flag is not.

### Targeting strategies

| Strategy | Use for |
|---|---|
| **Percentage** | Simple rollouts |
| **User ID hash** | Stable assignment (user keeps same variant) |
| **Account / org** | B2B, opt-in beta users |
| **Region** | Geographic rollout, regulatory rollout |
| **Allowlist** | Specific beta users, internal staff |
| **Denylist** | Exclude problem accounts |
| **Attribute-based** | Plan tier, signup date, etc. |

## Monitoring during the rollout

For each ramp stage, define **success criteria** before flipping:

```markdown
## Stage: 10%

**Success looks like:**
- Error rate for `flag=true` users within 0.1pp of `flag=false`
- p95 latency for `flag=true` within 50ms of `flag=false`
- Key metric (conversion / activation / etc.) not worse for `flag=true`

**Halt if:**
- Any of the above breach
- New error type appears in `flag=true` cohort
- User reports of broken behavior

**Decision time:** <date>
```

Instrument **both arms** (flag on AND flag off) with the same metrics so you can compare. A flag without measurement is just deploying to prod and crossing your fingers.

## Kill switch

Every non-trivial new feature should be **flippable in seconds without a deploy**. Verify:

- [ ] Can be disabled from the flag UI / config
- [ ] Disable propagates within <60s
- [ ] Disabled state was tested (not assumed to work)
- [ ] Cached results don't pin users to the disabled feature
- [ ] Background jobs check the flag at execution, not at enqueue

## Cleanup — the part everyone skips

A flag has three lives: ramping → at 100% → cleaned up. Skipping the third creates **flag debt**.

### When to remove a release flag

- Has been at 100% for ≥ 2 weeks with no rollback
- No business reason to keep the toggle (it's not a kill switch)

### Removal procedure

1. Audit usage: `grep -RIn '<flag-name>' .` — surface every reference
2. Delete the `if`/`else` and keep the new branch only
3. Delete the flag definition
4. Delete dead code that the old branch reached
5. Remove tests of the old branch (keep tests of the new behavior)
6. Verify the flag is gone from the flag service too (or it'll mislead future readers)
7. Commit: `chore(flags): remove <flag-name> (rolled out <date>)`

### Find stale flags

```bash
# Flags last toggled > N days ago — query your flag service

# Flags in code (rough)
grep -RInE 'flags\.[a-z_.]+\.enabled|isEnabled\(["'\''][a-z_]+|featureFlag\(' \
  --include='*.{js,ts,jsx,tsx,php,py,rb,go}' . \
  | awk -F: '{print $1":"$2}' | sort -u

# Flags defined but never read (or vice versa)
# (compare your flag-definitions file with usage)
```

A regular **flag spring cleaning** (monthly or quarterly) is much cheaper than the rolling cost of ambient confusion.

## Output format

```markdown
## Feature flag rollout plan: <feature>

**Flag:** `<area>.<feature>.<variant>`
**Type:** release / ops / experiment / permission
**Default:** false
**Owner:** @<person>

### Rollout ramp
| Stage | % | Audience | Duration | Decision criteria |
|---|---|---|---|---|
| 0 | staff | internal | 2 days | no functional bugs |
| 1 | 1% | random | 2 days | err/latency within thresholds |
| 2 | 10% | random | 3 days | … |
| … | … | … | … | … |
| 100% | all | — | — | — |

### Monitoring
- Compare metric A on flag=true vs flag=false
- Compare metric B on flag=true vs flag=false
- Alert if <condition>

### Kill switch verified
- ✅ Tested disable in staging
- ✅ Propagation < 60s
- ✅ No cached state pins users

### Cleanup plan
- Remove flag by <date>: <how>
```

## Anti-patterns

- ❌ Flag default `true` if the flag service is down
- ❌ Multiple flags wrapping the same logical change
- ❌ Flags evaluated once at process boot — toggle does nothing without restart
- ❌ Bucketing by `request.id` instead of user — same user sees both variants alternately
- ❌ Going 0% → 100% in one step
- ❌ "Temporary" flag that's been at 100% for 9 months
- ❌ Removing the flag definition but leaving the `if` in the code (always-false branch becomes dead code)
- ❌ Kill switch you've never actually flipped — flip it in staging quarterly
- ❌ A/B test without a control or without significance
- ❌ Flags storing business logic ("if flag X and not Y and user is...") — that's config, not a flag

## References

- [Martin Fowler — Feature Toggles](https://martinfowler.com/articles/feature-toggles.html) — the canonical breakdown
- [LaunchDarkly Best Practices](https://docs.launchdarkly.com/guides/flags/best-practices)
- [GitHub's experimentation platform](https://github.blog/engineering/architecture-optimization/experimentation-platform/) — real-world write-up
