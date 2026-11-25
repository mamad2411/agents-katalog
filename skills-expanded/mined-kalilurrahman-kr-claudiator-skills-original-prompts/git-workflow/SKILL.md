---
name: git-workflow
description: Design a Git branching strategy and workflow for a team. Outputs branch naming, merge strategy, CI/CD integration, and release process.
argument-hint: [team size, release cadence, project type]
allowed-tools: Read, Write
---

# Git Workflow Strategy

Design a complete Git workflow tailored to team size, release cadence, and deployment model. Not generic Git Flow — a specific branching strategy, merge policy, CI/CD integration, and release process that matches how the team actually works.

## Process

1. **Assess team context.** Team size (1-5, 5-20, 20+), release frequency (daily, weekly, monthly), deployment model (continuous, scheduled, manual).
2. **Choose base strategy.** Trunk-based (small teams, continuous deployment), Git Flow (scheduled releases), GitHub Flow (continuous deployment with staging), GitLab Flow (environment branches).
3. **Define branch types.** Main, develop, feature, release, hotfix — which ones are needed?
4. **Set merge policy.** Squash, merge commit, rebase — per branch type.
5. **Integrate CI/CD.** What runs on which branches? When to deploy?
6. **Define release process.** Tagging, versioning, changelog generation.
7. **Set protection rules.** Required reviews, status checks, linear history.
8. **Document edge cases.** Hotfixes, rollbacks, long-running features.

## Output Format

### Git Workflow Strategy: [Team Name]

**Team Size:** [number] engineers  
**Release Cadence:** [Daily/Weekly/Bi-weekly/Monthly]  
**Deployment Model:** [Continuous/Scheduled/Manual]  
**Recommended Strategy:** [Trunk-Based/Git Flow/GitHub Flow/GitLab Flow]

---

## Branch Structure

### Permanent Branches

#### `main`
- **Purpose:** Production-ready code, always deployable
- **Protection:** Require 2 reviews, all CI checks must pass, no force push
- **Deploy Target:** Production environment (auto-deploy on merge)
- **Merge From:** `release/*` branches (scheduled releases) or `feature/*` (continuous deployment)
- **Merge Strategy:** Squash and merge (clean history)

#### `develop` (if using Git Flow)
- **Purpose:** Integration branch for next release
- **Protection:** Require 1 review, CI must pass
- **Deploy Target:** Staging environment (auto-deploy on push)
- **Merge From:** `feature/*`, `bugfix/*`
- **Merge Strategy:** Merge commit (preserve feature branch history)

### Temporary Branches

#### `feature/*`
- **Naming:** `feature/JIRA-123-add-user-search`
- **Branch From:** `develop` (or `main` if trunk-based)
- **Merge To:** `develop` (or `main`)
- **Lifetime:** 1-5 days max (delete after merge)
- **CI:** Run tests + linting on every push
- **Review:** 1-2 reviewers required

#### `release/*`
- **Naming:** `release/v2.3.0`
- **Branch From:** `develop`
- **Merge To:** `main` (when ready) + back-merge to `develop`
- **Lifetime:** 1-3 days (stabilization period)
- **CI:** Full test suite + integration tests + smoke tests
- **Purpose:** Final QA, bug fixes, version bumping

#### `hotfix/*`
- **Naming:** `hotfix/critical-auth-bug`
- **Branch From:** `main` (current production)
- **Merge To:** `main` + `develop`
- **Lifetime:** Hours (expedited review)
- **CI:** Full test suite
- **Purpose:** Critical production fixes that cannot wait for next release

---

## Workflow Diagram

```
Trunk-Based (Continuous Deployment):

  main  ────────●─────────●─────────●──────→ (auto-deploy to prod)
                 ↑         ↑         ↑
                 │         │         │
       feature/A ─┘  feature/B ─┘  feature/C ─┘

Git Flow (Scheduled Releases):

  main     ────────────────●────────────────→ (manual deploy)
                           ↑
                           │
  release/v2.0 ───────────┘
                      ↑
                      │
  develop  ──●────●───●────●───●──────────→ (auto-deploy to staging)
             ↑    ↑        ↑   ↑
             │    │        │   │
    feature/A ┘  feature/B ┘  bugfix/C ┘
```

---

## Merge Policy

### Feature → Develop/Main
- **Strategy:** Squash and merge
- **Reason:** Clean history, single commit per feature
- **Commit Message Format:** `[JIRA-123] Add user search with filters`
- **Requirements:** 
  - 1-2 approved reviews
  - All CI checks pass (tests, linting, security scan)
  - Branch up-to-date with target
  - No merge conflicts

### Release → Main
- **Strategy:** Merge commit
- **Reason:** Preserve release history, tag the merge commit
- **Tag Format:** `v2.3.0` (semantic versioning)
- **Requirements:**
  - QA sign-off
  - All tests pass
  - Changelog updated
  - Version bumped in package.json/setup.py/etc.

### Hotfix → Main
- **Strategy:** Merge commit
- **Reason:** Urgency, preserve hotfix context
- **Tag Format:** `v2.3.1` (patch version bump)
- **Requirements:**
  - 1 review (expedited)
  - Tests pass
  - Post-merge: Immediately back-merge to `develop`

---

## CI/CD Integration

### On Push to Feature Branch
```yaml
- Run unit tests
- Run linter (ESLint, Pylint, etc.)
- Run security scan (Bandit, npm audit)
- Build preview deployment (Vercel/Netlify style)
```

### On Push to Develop
```yaml
- Run full test suite (unit + integration)
- Deploy to staging environment
- Run smoke tests on staging
- Notify team in Slack
```

### On Merge to Main
```yaml
- Run full test suite
- Build production artifacts
- Deploy to production (blue-green or canary)
- Run smoke tests on production
- Send deployment notification
- Generate changelog from commits
```

### On Tag Creation (v*.*.*)
```yaml
- Build release artifacts
- Create GitHub/GitLab release
- Upload binaries/Docker images
- Notify customers (if SaaS)
```

---

## Branch Protection Rules

### `main`
- ✅ Require pull request before merging
- ✅ Require 2 approving reviews
- ✅ Dismiss stale reviews on new push
- ✅ Require status checks to pass:
  - `ci/tests`
  - `ci/lint`
  - `ci/security-scan`
- ✅ Require branches to be up to date
- ✅ Require linear history (no merge commits from features)
- ✅ Restrict who can push (only release managers)
- ✅ Restrict force push
- ✅ Restrict deletions

### `develop`
- ✅ Require pull request before merging
- ✅ Require 1 approving review
- ✅ Require status checks to pass:
  - `ci/tests`
  - `ci/lint`
- ❌ Do not require up to date (allows parallel merges)
- ✅ Restrict force push

---

## Release Process

### Scheduled Releases (Git Flow)

**Week Before Release:**
1. Create `release/v2.3.0` from `develop`
2. Bump version in code (`package.json`, `__version__`, etc.)
3. Generate changelog from commits: `git log develop..release/v2.3.0 --oneline`
4. Deploy release branch to staging
5. Run full QA cycle

**Release Day:**
1. Final bug fixes merged to release branch
2. Tag release branch: `git tag v2.3.0`
3. Merge release branch to `main`
4. Merge release branch back to `develop`
5. Delete release branch
6. CI/CD auto-deploys `main` to production
7. Monitor metrics for 1 hour
8. Post release notes

### Continuous Deployment (Trunk-Based)

**Daily:**
1. Feature merged to `main`
2. CI runs full test suite
3. If tests pass, auto-deploy to production
4. Monitor metrics via Datadog/New Relic
5. Roll back if error rate spikes

---

## Edge Cases

### Hotfix Process
1. Create `hotfix/critical-auth-bug` from `main`
2. Fix bug + add regression test
3. Request review (expedited, 1 reviewer)
4. Merge to `main` (triggers deploy)
5. **Immediately** back-merge to `develop` to prevent regression
6. Tag: `v2.3.1`

### Long-Running Feature Branch
- **Problem:** Feature branch open for 2+ weeks, conflicts with `develop`
- **Solution:** 
  - Rebase daily: `git rebase develop`
  - Or: Use feature flags and merge incrementally (dark launch)
  - Or: Split into smaller features

### Rollback
1. Identify last good commit: `git log main`
2. Create rollback branch: `git checkout -b rollback/v2.2.9 <commit-hash>`
3. Merge to `main` (or force push if emergency)
4. Tag: `v2.3.2` (new version, even for rollback)
5. Post-mortem: Why did the issue not get caught?

### Merge Conflict
1. Update feature branch: `git fetch && git rebase develop`
2. Resolve conflicts in IDE
3. Run tests locally
4. Force push: `git push --force-with-lease`
5. CI re-runs, review continues

---

## Commit Message Convention

Use Conventional Commits:

```
feat(auth): add OAuth2 login with Google
fix(api): handle null user_id in order endpoint
docs(readme): update deployment instructions
chore(deps): upgrade Django to 4.2
test(payments): add refund integration test
```

**Format:** `<type>(<scope>): <description>`

**Types:**
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation
- `style` — Formatting (no code change)
- `refactor` — Code restructure (no behavior change)
- `test` — Add tests
- `chore` — Build/tooling

**Benefits:**
- Auto-generate changelog
- Semantic versioning (feat = minor, fix = patch)
- Clear history

---

## Team Guidelines

### Before Starting Work
1. Pull latest: `git fetch && git pull origin develop`
2. Create feature branch: `git checkout -b feature/JIRA-123-description`

### During Development
1. Commit frequently with meaningful messages
2. Push daily (backup + visibility)
3. Rebase on `develop` if branch older than 2 days

### Before Requesting Review
1. Rebase on target branch: `git rebase develop`
2. Run tests locally
3. Self-review the diff
4. Write PR description: What? Why? How to test?

### After Merge
1. Delete feature branch (GitHub does this automatically)
2. Move ticket to "Done"
3. Monitor deployment

## Rules

- Workflow must match actual team behavior — do not copy Git Flow if team deploys 10x/day.
- Branch naming must include ticket number (JIRA-123) for traceability.
- Every environment (dev, staging, prod) must map to a specific branch or tag.
- Hotfix process must be < 2 hours from bug report to production fix.
- If team is < 5 people, use trunk-based with feature flags instead of long-lived branches.
- CI must block merge if tests fail — no "merge and fix later."
- Commit messages must be imperative mood: "Add feature" not "Added feature" or "Adds feature."
- Tag format must follow semantic versioning: `v<major>.<minor>.<patch>`.
- Include rollback procedure — every workflow needs an escape hatch.
