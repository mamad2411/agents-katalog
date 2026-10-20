---
name: git-workflow
description: Git workflow standards — branch naming, commit messages, merge strategy, conflict resolution
alwaysApply: false
---

# Git Workflow Standards — Commits, Branches, Merge Strategy

Good git hygiene makes history readable, enables bisecting, and documents intent. Bad commits make review painful and history useless.

---

## Branch Naming Convention

**ALWAYS**:
- Format: `{type}/{ticket-id}-{description}`
- Types: `feature`, `fix`, `chore`, `refactor`, `docs`, `perf`
- Lowercase with hyphens (no spaces, underscores, or camelCase)
- Include ticket ID (links to issue tracker)
- Keep description short (≤ 50 characters)

**NEVER**:
- Branch names with spaces: `my feature` (breaks commands)
- Uppercase: `Feature/123-My-Branch` (inconsistent)
- No ticket ID (disconnected from work tracking)
- Generic names: `feature/update`, `fix/bug` (not descriptive)

### ✅ GOOD Branch Names

```
feature/123-user-authentication
feature/456-add-payment-integration
fix/789-cart-total-calculation
chore/890-update-dependencies
perf/901-optimize-database-queries
docs/912-api-documentation
refactor/923-service-layer-redesign
```

### ❌ BAD Branch Names

```
Feature/123-User-Authentication         # Uppercase, hard to type
my-feature-branch                        # No ticket ID
feature/update-stuff                     # Vague description
Feature 123 User Auth                    # Spaces, inconsistent
feat/123/user/auth/improvements         # Too deep, unclear
```

---

## Commit Message Format: Conventional Commits

**ALWAYS**:
- Format: `{type}({scope}): {subject}`
- Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `perf`, `test`, `ci`
- Scope: optional but helpful (module, file, or area)
- Subject: imperative, present tense, no period, ≤ 50 chars
- Body: explain WHY (not WHAT), wrap at 72 chars
- Footer: `Closes #123` to link to issue

**NEVER**:
- Vague commits: `"update"`, `"fix bug"`, `"changes"`
- Past tense: `"Fixed bug"` (use present: `"Fix bug"`)
- Final period in subject: `"Add user authentication."`
- Generic scope: `"fix(code)"` (use specific area)

### ✅ GOOD Commit Messages

```
feat(auth): add JWT token refresh logic

Implement refresh token rotation to improve security.
- Generate new access token on refresh endpoint
- Invalidate old refresh tokens after use
- Add 15-minute expiration on refresh tokens

Closes #456
```

```
fix(cart): prevent double-charge on retry

Payment processing was calling charge endpoint twice
when network timeout occurred. Add idempotency key
to prevent duplicate charges in retry scenarios.

Closes #789
```

```
perf(database): add index on orders.user_id

Query performance on order lookups was slow (200ms).
Adding index on user_id reduces to 5ms P50 for typical queries.

Closes #901
```

```
chore(deps): update typescript to 5.2.0

- Update tsconfig to use ES2022 target
- Fix type errors from stricter type checking
- All tests passing

Closes #912
```

### ❌ BAD Commit Messages

```
fix bug                          # Vague, no context
Fixed the authentication issue.  # Past tense, period, too generic
update                           # One word, meaningless
WIP                              # Work in progress should be squashed
feat: stuff                       # No scope, vague subject
fix(code): make it work         # Generic scope, unhelpful
```

---

## Commit Granularity

**ALWAYS**:
- One logical change per commit
- Commits should be reviewable independently (ideally)
- Include related changes in single commit (don't split overly)
- Test each commit (git bisect should work)

**NEVER**:
- Unrelated changes in one commit (hard to review)
- One huge commit for entire feature (impossible to review)
- Commits that break tests (git bisect breaks)

### ✅ GOOD Commit Granularity

```
# Feature branch: Add user registration

Commit 1: feat(auth): add user model and validation
  - Create User entity
  - Add email validation
  - Add tests for validation

Commit 2: feat(auth): implement user registration endpoint
  - POST /api/v1/users
  - Hash password with bcrypt
  - Return created user (no password)

Commit 3: feat(auth): add registration form to UI
  - Create RegisterComponent
  - Form validation on client
  - Integration with API

Commit 4: test(auth): add e2e registration test
  - Full registration flow
  - Verify user created in database
  - Verify email confirmation sent

Each commit: focused, testable, reviewable independently
```

### ❌ BAD Commit Granularity

```
# ❌ One huge commit: "Add user registration"
  - User model + validation
  - Registration endpoint
  - Form component
  - Tests
  - Database migration
  - Config changes
  ...
# 500 lines, impossible to review

# ❌ Too split: Each file is separate commit
  - feat: add User.ts
  - feat: add UserValidator.ts
  - feat: add RegisterEndpoint.ts
  # Logical feature split across unrelated commits
```

---

## Merge Strategy: Squash vs Rebase vs Merge Commit

### Feature Branches (Squash Recommended)

```
Main: A → B → C

Feature: D → E → F (3 commits)

After merge (squash):
Main: A → B → C → [Squashed D+E+F]

Benefit: Clean history, one commit per feature
Use: Most features, bugfixes
```

### Long-Lived Branches (Merge Commit)

```
Main: A → B → C

Feature: D → E → F → G → H (5 commits, weeks of work)

After merge (merge commit):
Main: A → B → C → [Merge Commit] ← merges D+E+F+G+H
                         ↓
              (entire branch history visible)

Benefit: Preserve branch history, see feature development
Use: Major features, long-running work, team collaboration
```

### Release Branches (No Rebase on Public)

```
❌ NEVER rebase on public branches
Main: A → B → C (everyone has this)

If you rebase locally:
Main: A → B → C (re-written as A' → B' → C')

Now public Main and your local don't match
Force push damages other developers' branches
```

### ✅ GOOD Merge Strategy

```bash
# Feature branch: squash before merge
git checkout feature/123-auth
git commit ...
git commit ...
git commit ...

# Before merging to main, squash
git rebase -i main
# mark commit 1: pick
# mark commits 2+: squash
# write new commit message

git push -f origin feature/123-auth

# Now merge to main
git checkout main
git merge --no-ff feature/123-auth
# Creates merge commit, all squashed into one logical commit
```

---

## Handling Merge Conflicts

**ALWAYS**:
- Resolve conflicts manually, understand both sides
- Test after resolving (conflict resolution can introduce bugs)
- Communicate with author of conflicting changes
- Keep resolution commits separate (don't squash them away)

**NEVER**:
- Accept all theirs or all ours blindly
- Merge without testing
- Rebase over someone else's published work

### ✅ GOOD Conflict Resolution

```bash
# During merge, conflicts occur
git merge feature/456-payment

# CONFLICT (content): Merge conflict in src/OrderService.ts
# Auto-merging src/OrderService.ts
# CONFLICT (content merge failed)

# 1. Understand both sides
git diff HEAD
git diff feature/456-payment

# 2. Manually resolve (editor, or use tool)
# Edit src/OrderService.ts to combine both changes

# 3. Test the resolution
npm test
# Ensure tests pass with merged code

# 4. Mark resolved and commit
git add src/OrderService.ts
git commit -m "Merge: resolve conflict in OrderService between auth and payment"
```

### Example Conflict

```typescript
// main (your changes)
// OrderService.ts
async processOrder(order: Order, userId: number) {
  const user = await this.userService.getUser(userId);
  // YOUR CODE: validate user permissions
  if (!user.canPlace Orders) {
    throw new PermissionError();
  }
  return await this.paymentService.charge(order.total);
}

// feature/456-payment (their changes)
// OrderService.ts
async processOrder(order: Order, userId: number) {
  const user = await this.userService.getUser(userId);
  // THEIR CODE: process refunds
  await this.refundService.processRefunds(order.id);
  return await this.paymentService.charge(order.total);
}

// CONFLICT MARKER
// <<<<<<< HEAD
// if (!user.canPlaceOrders) throw new PermissionError();
// =======
// await this.refundService.processRefunds(order.id);
// >>>>>>> feature/456-payment

// RESOLUTION: Combine both
async processOrder(order: Order, userId: number) {
  const user = await this.userService.getUser(userId);
  
  // Both validations
  if (!user.canPlaceOrders) throw new PermissionError();
  await this.refundService.processRefunds(order.id);
  
  return await this.paymentService.charge(order.total);
}
```

---

## Rewriting History (Before Public Push)

**ALLOWED (before push):**
- Squash commits: `git rebase -i HEAD~3`
- Amend last commit: `git commit --amend`
- Reorder commits: `git rebase -i main`

**NEVER (after public push):**
- Rebase public branches
- Force push to shared branches
- Rewrite history others depend on

### ✅ GOOD History Cleanup

```bash
# Before pushing feature branch to origin
git log --oneline
# abc1234 fix: typo in error message
# def5678 wip: testing new approach
# ghi9012 feat: add JWT validation

# Squash work-in-progress
git rebase -i main
# mark abc1234: pick
# mark def5678: squash (combine with previous)
# mark ghi9012: pick

# Now just 2 commits
git push origin feature/123-auth
```

---

## Git Workflow Checklist

- [ ] Branches named: `{type}/{id}-{description}` (lowercase, hyphens)
- [ ] Commits follow Conventional Commits format
- [ ] Subjects are imperative present tense (≤ 50 chars)
- [ ] Bodies explain WHY, not WHAT
- [ ] Commits are granular (one logical change per commit)
- [ ] Branch squashed before merge to main
- [ ] No commits that break tests (git bisect safe)
- [ ] Merge commits used for multi-commit features
- [ ] No rebasing after public push
- [ ] Conflicts resolved carefully + tested
- [ ] Issue tickets linked in commit footers
- [ ] History is clean and readable

---

## Common Scenarios

### "I have 5 commits, but they're all related—should I squash?"

**If commits are all for one feature:**
- Yes, squash before merging to main
- Easier to revert entire feature if needed
- Cleaner main branch history

**If commits are logically separate:**
- No, keep them separate
- Example: commit 1 = refactor, commit 2 = feature using refactored code

### "I committed to the wrong branch—how do I fix?"

```bash
# Created feature branch from wrong branch
git log --graph main feature/123
# Oops, feature has commits from develop too

# Solution: cherry-pick your commits onto correct branch
git checkout feature/123
git rebase main  # Rebase onto main instead
```

### "I pushed to main by mistake—how do I undo?"

```bash
# ❌ NEVER force push to main
# ✅ DO: Create a revert commit

git revert abc1234  # Creates new commit that undoes changes
git push origin main

# History shows what happened:
# ... → normal-commit → bad-commit → revert-bad-commit
```

---

## Summary

Good git workflow:
1. **Branch naming** — `type/id-description` (clear, searchable)
2. **Conventional commits** — `type(scope): subject` (automatable, searchable)
3. **Granular commits** — one logical change per commit (easy to review)
4. **Squash features** — clean main history (easy to revert)
5. **Don't rebase public** — preserve history others depend on
6. **Conflict resolution** — test after merging (understand both sides)

This makes history readable, enables git bisect, and documents intent for future developers.
