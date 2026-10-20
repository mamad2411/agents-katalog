---
name: pr-standards
description: Pull request standards — size limits, description format, checklist, review process
globs: ["**/*.cs", "**/*.ts", "**/*.md", "**/*.yml"]
alwaysApply: false
---

# Pull Request Standards

Quality PR standards ensure reviews are fast, thorough, and aligned on expectations.

## PR Size & Scope

**ALWAYS**:
- **Maximum 400 lines of changes** (fewer is better, ~200 ideal)
- **One feature or fix per PR** (not multiple unrelated changes)
- **Linked to a ticket** (issue number in title or description)
- **Reviewed before merge** (minimum 1 approval)
- **Tests included** (not added in separate PR)
- **Ready-to-merge** (not "draft" or "WIP" if asking for review)

**NEVER**:
- 1000+ line PRs (split into smaller PRs)
- Multiple features in one PR (review fatigue)
- Tests added in separate PR (proves code works now)
- Incomplete PRs marked "ready" (ask for feedback in draft mode)
- Approved without tests passing
- Merged without changelog entry (if user-facing)

### Why Size Matters

```
50 lines   → 5-10 min review, catches most issues ✅
200 lines  → 20-30 min review, thoughtful feedback 👍
400 lines  → 1 hour review, details can be missed ⚠️
1000 lines → 2+ hours or cursory review (bad)     ❌
```

---

## PR Description Template

```markdown
## What
Brief description of what this PR does.

## Why
Explanation of why this change was needed.
Link to ticket: Closes #123

## How
Technical approach taken. Key decisions made.
If complex: explain trade-offs or alternatives considered.

## Testing
How was this tested?
- [ ] Unit tests added (coverage > 80%)
- [ ] Integration tests added (if applicable)
- [ ] Manual testing done (describe)
- [ ] Test results: all passing

## Before & After
If visual/behavior change: show screenshots or before/after code.

## Checklist
- [ ] Code follows style guide (ran formatter)
- [ ] No console.log / debug code left
- [ ] No hardcoded secrets or sensitive data
- [ ] Updated CHANGELOG.md (if user-facing)
- [ ] Updated docs if behavior changed
- [ ] No breaking changes (or documented migration)
```

---

## Code Review Checklist (For Reviewers)

**Before Approving, Check:**

- [ ] **Tests**: All passing, coverage not decreased
- [ ] **Security**: No secrets, SQL injection, XSS vulnerabilities
- [ ] **Performance**: No N+1 queries, allocations in loops, blocking awaits
- [ ] **Style**: Matches project conventions (run formatter)
- [ ] **Docs**: Updated if behavior changed, comments explain WHY
- [ ] **Size**: <= 400 lines (or split if larger)
- [ ] **Scope**: Single feature/fix (not multiple unrelated changes)
- [ ] **Linked**: Issue number in title or description
- [ ] **No TODOs**: Unless linked to a follow-up ticket
- [ ] **Mergeable**: No conflicts, CI green

---

## PR Feedback Levels

### 🟢 Approve
- All checks pass
- No blocking issues
- Ready to merge immediately

### 🟡 Request Changes
- Issues found that must be fixed before merge
- Give specific, actionable feedback
- Explain severity (Critical/High/Medium/Low)

### 🔵 Comment
- Suggestion for improvement
- Not blocking
- Can merge without addressing (but consider it)

### 🚫 Reject
- Do not merge under any circumstances
- Critical security issue
- Breaking change not approved
- Tests failing

---

## Common PR Issues & How to Fix

| Issue | Example | Fix |
|-------|---------|-----|
| **Too Large** | 1200 lines, 8 files | Split into 2-3 PRs by feature |
| **Missing Tests** | No test file added | Add tests before merge |
| **Secrets** | API key in code | Use env vars, regenerate key |
| **No Docs** | Behavior changed, no docs updated | Update README or JSDoc |
| **Poor Description** | Just "updates" | Rewrite: what/why/how |
| **Unlinked** | No issue number | Add "Closes #123" |
| **Stale** | Hasn't been reviewed in 1 week | Ping reviewer or rebirth PR |

---

## Review Etiquette

✅ **GOOD Feedback:**
```
"Line 47: This could cause N+1 queries if called in a loop. 
Solution: Move the query outside the loop or batch load.
Example:
// Before
for (var item in items)
  user = await db.Users.FirstAsync(u => u.Id == item.UserId);

// After
var userIds = items.Select(i => i.UserId).Distinct();
var users = await db.Users.Where(u => userIds.Contains(u.Id)).ToDictionary(u => u.Id);
"
```

❌ **BAD Feedback:**
```
"This is wrong" ← vague, no guidance
"You should have used LINQ" ← no example
"Bad performance" ← no explanation
```

---

## ✅ Good PR Example

```
## What
Add password reset flow to user authentication.

## Why
Closes #342. Users locked out of account had no way to recover.

## How
1. New endpoint: POST /api/auth/password-reset
2. Sends verification email with 1-hour token
3. User visits reset link, sets new password
4. Token invalidated after use
Security: Password reset tokens are cryptographically random, stored hashed.

## Testing
- [ ] Added PasswordResetService_Tests.cs (15 tests, 92% coverage)
- [ ] Added PasswordResetController_Tests.cs (8 tests)
- [ ] Manual: tested full flow (request → email → reset → login)
- [ ] Edge cases: expired token, reused token, invalid email

## Before & After
Before: 0 password reset option (user had to contact support)
After: Self-service password reset via email

## Checklist
- [x] Code follows style guide
- [x] No hardcoded secrets (uses ${PASSWORD_RESET_EMAIL_KEY})
- [x] CHANGELOG.md updated
- [x] API docs updated (Swagger)
- [x] No breaking changes
```

---

## Blocked PRs

**PR is "Blocked" when:**
- Waiting for another PR to merge first
- Blocked on external dependency
- Waiting for design decision
- Waiting for user feedback

**Action**: Label as "blocked", explain blocker, set clear unblocking condition.

---

## PR Merge Criteria

✅ **Can Merge:**
- 1+ approval (Core contributors)
- 0 rejected reviews
- All tests passing
- No merge conflicts
- Linked to ticket
- Description complete
- All conversations resolved

❌ **Cannot Merge:**
- Tests failing
- Security issue found
- Code coverage decreased
- Conflicts (not resolved)
- Missing approval
- Explicitly rejected

---

## PR Checklist

Before marking "Ready for Review":
- [ ] Feature/fix complete and working
- [ ] Tests written and passing (> 80% coverage)
- [ ] No console.log, hardcoded values, or debug code
- [ ] Code formatted (linter passing)
- [ ] Docs updated (if behavior changed)
- [ ] CHANGELOG.md updated (if user-facing)
- [ ] Description filled in with what/why/how
- [ ] Linked to issue (#123)
- [ ] Reviewed own code first (catch obvious mistakes)

---

## Performance & Size Targets

| Metric | Target | Example |
|--------|--------|---------|
| **Lines Changed** | < 400 | Small focused change ✅ |
| **Files Changed** | < 8 | Changes isolated ✅ |
| **Review Time** | 10-30 min | Quick feedback ✅ |
| **Time to Merge** | < 24 hours | Not stale ✅ |

---

## Summary

Good PRs are:
- **Small** (easy to understand)
- **Focused** (one thing per PR)
- **Tested** (proofs it works)
- **Documented** (why/how)
- **Quick** (reviewed quickly)

This speeds up review, catches issues early, and keeps master stable.
