---
name: feature-flags
description: Feature flag system for gradual rollouts, A/B testing, and kill switches. Outputs flag types, targeting, evaluation, and lifecycle management.
argument-hint: [release strategy, team size, rollback requirements]
allowed-tools: Read, Write, Bash
---

# Feature Flags System

Design production feature flags for safe deployments, experiments, and operational control. Not "if (flag)" — targeting rules, gradual rollouts, audit logs, emergency kill switches.

## Process

1. **Define flag types.** Release (temporary), experiment (A/B), ops (permanent), permission.
2. **Choose evaluation.** Client-side (fast), server-side (secure), hybrid.
3. **Design targeting.** User ID, percentage, attributes, custom rules.
4. **Plan storage.** Database, config, LaunchDarkly/Split.
5. **Add lifecycle.** Create → Test → Rollout → Cleanup (90 days).
6. **Implement kill switches.** Emergency disable without deploy.

## Output Format

### Feature Flags: [System Name]

**Provider:** LaunchDarkly  
**Evaluation:** Server-side with client SDK  
**Flag Types:** Release, Experiment, Ops, Permission  
**Cleanup Policy:** 90 days post-rollout

---

## Flag Types

### Release Toggles (Temporary, Days-Weeks)
```python
if flags.is_enabled('new_checkout_flow', user):
    return new_checkout()
else:
    return old_checkout()
```
**Cleanup:** Remove after 100% rollout + 2 weeks

### Experiment Flags (A/B Test, Weeks-Months)
```python
variant = flags.get_variant('checkout_button_color', user)  # blue/green/red
track_experiment('button_color', variant, user)
```

### Ops Flags (Permanent)
```python
if flags.is_enabled('maintenance_mode'):
    return {"error": "Under maintenance"}, 503
```

### Permission Flags (Permanent)
```python
if not flags.is_enabled('premium_features', user):
    abort(403)
```

---

## Targeting Strategies

### Percentage Rollout
```python
def is_enabled_percentage(flag: str, user_id: str, pct: int) -> bool:
    import hashlib
    hash_val = int(hashlib.md5(f"{flag}:{user_id}".encode()).hexdigest(), 16)
    return (hash_val % 100) < pct
```

### User Whitelist
```yaml
beta_feature:
  whitelist: [user_123, user_456]
```

### Attribute-Based
```yaml
premium_feature:
  rules:
    - if: user.tier == 'premium'
      then: enabled
    - if: user.country in ['US','CA']
      then: enabled
```

---

## Implementation

### Database-Backed
```sql
CREATE TABLE feature_flags (
    name VARCHAR(100) PRIMARY KEY,
    enabled BOOLEAN DEFAULT FALSE,
    rollout_percentage INT DEFAULT 0,
    whitelist JSONB DEFAULT '[]'
);
```

```python
def is_enabled(flag: str, user_id: str) -> bool:
    flag_obj = db.query(FeatureFlag).filter_by(name=flag).one()
    
    if user_id in flag_obj.whitelist:
        return True
    if is_enabled_percentage(flag, user_id, flag_obj.rollout_percentage):
        return True
    return flag_obj.enabled
```

### LaunchDarkly Integration
```python
import ldclient
client = ldclient.get()

user = {'key': user_id, 'email': email, 'custom': {'tier': 'premium'}}
return client.variation('feature_name', user, False)
```

---

## Gradual Rollout

Day 1: Internal (1%)
```yaml
rollout_percentage: 0
whitelist: [internal_users]
```

Day 3: Canary (5%)
```yaml
rollout_percentage: 5
```

Day 14: Majority (75%)
```yaml
rollout_percentage: 75
```

Day 21: Full (100%)
```yaml
enabled: true
```

Day 35: **Cleanup Code**
```python
- if flags.is_enabled('new_feature', user):
+ # Feature now default, flag removed
```

---

## Kill Switches

```python
@app.route('/admin/flags/<flag>/disable', methods=['POST'])
@require_admin
def kill_switch(flag):
    flag_obj.enabled = False
    flag_obj.rollout_percentage = 0
    cache.delete(f"flag:{flag}")
    audit_log.record('emergency_disable', flag)
```

### Auto-Disable on High Error Rate
```python
if error_rate > 0.1:
    flags.emergency_disable('problematic_feature')
    alert('Feature auto-disabled: 10% error rate')
```

---

## Monitoring

```python
from prometheus_client import Counter

flag_evals = Counter('flag_evaluations_total', 'Evaluations', ['flag','result'])

def is_enabled_tracked(flag, user):
    result = is_enabled(flag, user)
    flag_evals.labels(flag=flag, result=result).inc()
    return result
```

**Alerts:**
- Eval latency > 100ms
- Stale flags (90+ days unchanged)

---

## Stale Flag Detection

```python
def find_stale_flags():
    # Grep code for flag references
    used = set()
    for file in glob('**/*.py'):
        with open(file) as f:
            matches = re.findall(r"is_enabled\(['\"]([^'\"]+)", f.read())
            used.update(matches)
    
    db_flags = {f.name for f in FeatureFlag.all()}
    return db_flags - used
```

## Rules

- Default flags OFF — safer to enable than accidentally leave on.
- Release toggles MUST be removed within 90 days of 100% rollout.
- Percentage rollouts use consistent hashing — same user always gets same result.
- All state changes audit logged (who, when, old/new values).
- Kill switches required for high-risk features.
- Flag eval < 10ms — cache configs, don't query DB per request.
- Flags control code paths, not database columns.
- Stale detection runs monthly — alert unused flags.
- A/B test flags track assignment AND conversion for analysis.
- Emergency disable via admin UI without code deploy.
