---
name: incremental-implementation
description: Delivers changes in thin, independently verifiable vertical slices. Each slice is a complete, testable increment that adds user-facing value. Feature flags, safe defaults, rollback plans, strict commit discipline, and integration testing at every slice prevent the "big bang" merge disaster.
---

# Incremental Implementation

## Overview

The classic failure mode: a developer works on a feature for 2 weeks in a long-lived branch, merges 3000 lines of untested code, and spends another week fixing the integration chaos. This is **big bang delivery** and it is the #1 cause of delayed releases and production incidents.

Incremental implementation replaces this with **thin vertical slices**:
- Each slice adds a complete, user-facing capability (no horizontal layers like "all the backend work" then "all the frontend work")
- Each slice is independently testable
- Each slice is deployable (even if hidden behind a feature flag)
- No branch lives longer than 2 days
- Every merge is low-risk because the diff is small and tested

The mantra: **Make the change easy, then make the easy change. Then ship it.**

## When to Use

| Trigger | Description |
|---------|-------------|
| Any feature > 1 day of work | Must be sliced, never built in one shot |
| Multiple developers on same area | Parallel slices reduce merge conflicts |
| High-risk changes | Payment, auth, data migration |
| New team or unfamiliar codebase | Small slices reduce blast radius |
| Deploying to production frequently | Every slice must be safe to ship |
| Refactoring large code sections | Incremental extraction, not rewrite |

**Do NOT use** when: the change is genuinely atomic (rename a variable, fix a typo, change one config value), or when time-to-market is measured in hours and risk is zero.

## Slicing Strategy

### Thin Vertical Slices

A vertical slice cuts across all layers (DB → API → UI) but implements only one tiny end-to-end behavior.

**Good slice:** "User can view their profile name" (DB: add name column, API: GET /profile returns name, UI: show name on profile page)

**Bad slice (horizontal):** "Profile API layer" — no user-visible outcome, untestable until UI is built

**Bad slice (too big):** "Profile page" — covers name, photo, bio, settings, all in one branch

### Slicing Heuristics

| Instead of this horizontal slice | Do this vertical slice |
|----------------------------------|----------------------|
| "Build all database models" | "User can register" (User model + auth + UI) |
| "Build all API endpoints" | "User can view their profile" (1 endpoint + UI) |
| "Build the admin dashboard" | "Admin can see user count" (1 widget + 1 metric) |
| "Add notifications system" | "User gets email on signup" (1 trigger + 1 channel) |

### Slice Size Rules

- **Target:** 50-200 lines of code per slice
- **Maximum:** 400 lines (beyond this, slice is too big)
- **Test ratio:** at least 1:1 test code to implementation code
- **Time:** 2-4 hours per slice (never exceed 1 day)
- **Commits:** 1-5 commits per slice (never a single giant commit)

## Feature Flags

Every incomplete feature MUST be hidden behind a feature flag.

### Implementation

```typescript
// Feature flag configuration
const features = {
  newProfilePage: process.env.FEATURE_NEW_PROFILE === 'true',
  darkMode: false, // will be toggled via admin panel
  experimentalExport: Math.random() < 0.1, // gradual rollout, 10%
}
```

### Feature Flag Lifecycle

| Phase | Flag State | Behavior | When |
|-------|-----------|----------|------|
| Development | Default off | Only visible in dev/test | During slice implementation |
| Internal testing | Enabled for test accounts | Specific users can access | After slice 1 is complete |
| Beta | Gradually enabled (10%, 25%, 50%) | Random subset of users | After all slices complete |
| GA | Enabled for all | Everyone sees it | After validation |
| Cleanup | Remove flag | Code is permanent | 1 week after GA |

**Never** leave a feature flag in the code for more than 2 weeks after GA. Stale flags accumulate and confuse.

## Safe Defaults

When adding new behavior, the system must not regress if the new code fails.

### Default Patterns

```typescript
// Pattern 1: Safe fallback
try {
  return await newService.process(data);
} catch {
  logger.warn('New service failed, falling back to legacy');
  return await legacyService.process(data);
}

// Pattern 2: Progressive enhancement
const result = await fetchData();
if (features.newDisplay) {
  return enhancedFormat(result); // New display layer on top of same data
}
return result; // Original format untouched

// Pattern 3: Dark launch
const newResult = await newService.process(data);
// Don't return it yet — just log comparison metrics
logger.info({ oldResult, newResult }, 'Dark launch comparison');
return oldResult;
```

**Golden rule:** The new code path must never fail more loudly than the old one. If the new path throws, the old path must work exactly as before.

## Rollback Plans

Every slice must have a rollback plan documented BEFORE merge.

### Rollback Levels

| Level | Action | Time | Risk |
|-------|--------|------|------|
| L1 | Revert the commit | 1 min | Low — if no schema migration |
| L2 | Feature flag off | 1 min | Lowest — no deploy needed |
| L3 | Database migration rollback | 5 min | Medium — data loss possible |
| L4 | Full previous deploy | 15 min | High — other changes may revert |

### Rollback Checklist (pre-merge)

- [ ] Can this change be reverted with `git revert`? (If schema change, need L3 plan)
- [ ] If feature-flagged, what's the flag kill switch?
- [ ] What data, if any, is written by this change? Is it reversible?
- [ ] Is there a monitoring alert that would fire if this fails?
- [ ] Who is responsible for pulling the rollback trigger?

## Commit Discipline

Incremental implementation requires **clean, atomic commits**. Every commit is a slice.

### Commit Rules

1. **One logical change per commit.** Not "WIP" or "fixes" — a coherent, reviewable unit.
2. **Commit message format:**
   ```
   type(scope): short description under 50 chars

   Longer explanation if needed. Why this approach, not
   what the code does (the diff shows that).

   - Bullet points for trade-offs
   - Links to issues or specs
   ```
3. **Every commit must pass tests.** If it doesn't pass tests, it's not a commit (it's a stash).
4. **No "fix merge" commits.** Rebase instead of merge.
5. **No commented-out code.** Delete it. That's what git history is for.

### Commit Types

| Type | Use | Example |
|------|-----|---------|
| `feat` | New user-facing feature | `feat(profile): add name display to profile page` |
| `fix` | Bug fix | `fix(auth): handle expired tokens gracefully` |
| `refactor` | Code restructuring | `refactor(db): extract user model to separate file` |
| `test` | Adding or fixing tests | `test(api): add auth middleware tests` |
| `chore` | Tooling, config, deps | `chore(deps): upgrade vitest to v1.2` |
| `docs` | Documentation | `docs(api): update endpoint docs` |

### Branch Strategy

- Branch from main
- Implement 1-3 slices per branch
- Keep branch lifetime < 2 days
- Rebase onto main before opening PR
- Squash commits per slice on merge (not the entire branch into one commit)

## Integration Testing at Each Slice

Every slice must include integration tests that verify the slice end-to-end.

### Test Coverage per Slice

```typescript
// Slice: User can view profile name
describe('View profile name', () => {
  it('returns 200 with name for authenticated user', async () => {
    const user = await createTestUser({ name: 'Alice' });
    const res = await request(app)
      .get(`/profile`)
      .set('Authorization', `Bearer ${user.token}`);
    expect(res.status).toBe(200);
    expect(res.body.name).toBe('Alice');
  });

  it('returns 401 for unauthenticated request', async () => {
    const res = await request(app).get('/profile');
    expect(res.status).toBe(401);
  });
});
```

### Integration Testing Rules

- Each slice adds tests for the new behavior
- Existing tests must still pass (no regression)
- Tests are part of the slice, not an afterthought
- If a slice can't be integration-tested, it's not a slice — re-slice it

## Anti-Rationalization Table

| Temptation | Why It Happens | Why It's Dangerous | What To Do Instead |
|------------|----------------|--------------------|--------------------|
| "I'll just build the whole thing in one branch" | Speed illusion | Merge hell, integration surprises | Slice into 3-5 vertical increments. Merge each in < 2 days. |
| "I don't need feature flags for this" | Overconfidence | Incomplete feature in production | Wrap in a flag. It takes 2 lines. Remove it later. |
| "I'll add tests after the feature is done" | Deadline pressure | Tests never get written | Tests are part of each slice. No slice without tests. |
| "The change is too small to have a rollback plan" | Complacency | Small change + bad schema migration = big incident | Feature flag. Always. |
| "I'll fix the merge conflicts later" | Laziness | Conflicts compound, become unmanageable | Rebase daily. Conflicts become small and frequent. |
| "I can make an exception to commit discipline" | Urgency bias | WIP commits accumulate, history becomes garbage | Commit discipline IS what enables speed. Don't break it. |
| "The integration test is too hard for this slice" | Slice is too big | Untested code in production | Break the slice smaller until it's testable |
| "I need to refactor first, then I'll test" | Fear of changing untested code | Refactoring without tests is blind | Write characterization tests first |

## Red Flags

1. Branch older than 3 days — too long-lived, risk of conflicts
2. Diff larger than 400 lines — slice is too big
3. No feature flag for incomplete feature — half-baked code in production
4. No rollback plan — "we'll fix forward" is not a plan
5. Commit messages are "WIP", "fix", or "updates" — no discipline
6. PR has more than 5 commits for a single slice — too fragmented
7. Integration tests added after the PR, not as part of it
8. Tests don't cover the new behavior — testing the wrong thing
9. Schema migration is irreversible — no down migration
10. "I'll clean this up later" appears in code comments — no you won't

## Verification

- [ ] **Feature is sliced** into 3-5 thin vertical increments
- [ ] **Each slice is independently testable** — integration test exists
- [ ] **Each slice is deployable** — either feature-flagged or safe by default
- [ ] **Feature flags** wrap all incomplete features
- [ ] **Feature flag lifecycle planned** — from dev to cleanup
- [ ] **Safe defaults** in place — old path works if new path fails
- [ ] **Rollback plan documented** — at L1 or L2 level
- [ ] **Commit discipline** — atomic commits, proper messages, no WIP
- [ ] **Branch lifetime** < 2 days — no long-lived branches
- [ ] **Every commit passes tests** — CI green before merge
- [ ] **Schema migrations are reversible** — down migration exists
- [ ] **Stale feature flags** have removal plan

### Vertical Slice Checklist (pre-implementation)

```
For each slice, verify:
  □ Slice adds user-visible value (not just infrastructure)
  □ Slice is < 400 lines of code
  □ Slice has integration tests
  □ Slice has a safe default path if it fails
  □ Slice is feature-flagged (if incomplete)
  □ Slice has rollback plan (at least git revert)
  □ Slice can be reviewed in < 30 minutes
  □ Slice will be merged in < 2 days
```
