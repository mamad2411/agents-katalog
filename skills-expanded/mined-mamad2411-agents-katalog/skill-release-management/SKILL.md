---
name: skill-release-management
description: Release planning and scheduling, semantic versioning (semver), rollout strategies (canary, blue-green, gradual), changelog generation, rollback procedures, production validation. Use when planning releases, creating rollout strategies, or managing version bumps.
version: 1.0.0
---

# Skill: Release Management

Plan releases. Roll out safely. Roll back fast.

## Semantic Versioning

- `MAJOR.MINOR.PATCH` (e.g., 2.1.3)
- **MAJOR**: Breaking changes (2.0.0)
- **MINOR**: New features, backward-compatible (1.5.0)
- **PATCH**: Bug fixes (1.4.2)

## Rollout Strategy

**Stage 1: Canary** (5%, monitor 30 min)
- If good → proceed
- If bad → rollback immediately

**Stage 2: Gradual** (25% → 50% → 75%, each 1 hour)
- Monitor: Error rate < 0.1%, latency stable
- If any stage fails → rollback

**Stage 3: Full** (100%, monitor 4 hours)
- On-call team watches

## Pre-Release Checklist

- [ ] All tests pass
- [ ] No linting/type errors
- [ ] Performance: no regressions
- [ ] Security: scan passed
- [ ] Accessibility: WCAG AA
- [ ] Documentation updated
- [ ] Release notes written
- [ ] Rollback tested in staging
- [ ] Monitoring configured
- [ ] On-call briefed

## Release Notes

```
## v2.1.0 — [Date]

### ✨ New
- Feature 1
- Feature 2

### 🐛 Fixed
- Bug 1

### ⚠️ Breaking
- Change 1 (migration guide)

### 📊 Timeline
- 10:00 UTC: Canary (5%)
- 10:30 UTC: Gradual (25%)
- 11:30 UTC: Full (100%)
```

## Rollback

**< 5 minutes**:
1. Detect issue
2. Declare rollback
3. Execute (tested before)
4. Verify (health checks)
5. Post-mortem

---

**Status**: Ready for release work  
**Best for**: Release planning, rollout, versioning
