---
name: git-workflow-design
version: 1.0.0
min_mindforge_version: 0.3.0
status: stable
triggers: git workflow design, trunk based development, gitflow, branch policy, merge strategy, squash vs rebase, commit standard, branch naming, release branch, hotfix workflow, protected branch, merge queue
---

# Skill — Git Workflow Design

## When this skill activates
Any task involving git branching strategies, merge policies, commit standards,
release workflows, or repository governance.

## Mandatory actions when this skill is active

### Before recommending a workflow
1. Assess team size and release cadence.
2. Identify deployment model (continuous vs scheduled releases).
3. Consider CI/CD maturity and test coverage levels.

### Trunk-Based Development

**Characteristics:**
- Main branch is always deployable.
- Short-lived feature branches (< 2 days).
- CI runs on every commit to main.
- Feature flags for incomplete work.

**Best for:** small-to-medium teams, continuous deployment, high CI maturity.

**Rules:**
- Branch from main, merge back to main.
- No long-lived branches (except main).
- Feature flags decouple deploy from release.
- Revert fast if main breaks — don't "fix forward" under pressure.

### GitFlow

**Characteristics:**
- develop branch for integration.
- release/* branches for stabilization.
- hotfix/* branches from main for urgent fixes.
- Longer release cycles (weekly/monthly).

**Best for:** teams with scheduled releases, multiple versions in production, regulatory requirements.

**Rules:**
- Feature branches from develop.
- Release branch cut when ready — only bug fixes after cut.
- Hotfix from main, merge back to both main AND develop.
- Tag every release on main.

### Merge strategies

**Squash merge:**
- Produces clean, linear history on main.
- One commit per PR — easy to revert entire features.
- Loses granular commit history from the branch.
- Best for: feature branches with messy/WIP commits.

**Rebase merge:**
- Linear history, preserves individual commits.
- Requires clean, meaningful commits on the branch.
- Best for: teams that enforce atomic commits.

**Merge commit:**
- Preserves branch topology (merge bubbles visible).
- Easy to see "this group of commits was one PR."
- Best for: teams that value traceability over linearity.

### Branch naming conventions

**Format:** `type/ticket-description`

**Examples:**
- `feat/PROJ-123-add-oauth-login`
- `fix/PROJ-456-null-pointer-checkout`
- `chore/upgrade-react-19`
- `hotfix/payment-timeout`

**Rules:**
- Lowercase, hyphen-separated.
- Include ticket number when applicable.
- Keep descriptions short but meaningful.
- No personal names or dates in branch names.

### Protected branch rules

- **Require pull request** — no direct pushes to main/develop.
- **Require CI pass** — all status checks green before merge.
- **Require review** — at least 1 approval (2 for critical paths).
- **Require up-to-date branch** — must be rebased on latest main.
- **Restrict force-push** — disabled on main, develop, release/*.
- **Require signed commits** — for regulated environments.

### Merge queue

- Batches multiple approved PRs together.
- Tests the combined result before merging.
- Automatically reverts PRs that break the batch.
- Prevents "works individually, breaks together" scenarios.
- Available: GitHub merge queue, Mergify, Bors.

### Commit standards

**Conventional Commits format:**
```
type(scope): description

[optional body]

[optional footer]
```

**Types:** feat, fix, refactor, docs, test, chore, perf, ci, build, revert.

**Rules:**
- Subject line < 72 characters.
- Imperative mood ("add" not "added").
- Body explains WHY, not WHAT (the diff shows what).
- Footer for breaking changes: `BREAKING CHANGE: description`.
- Enforce with commitlint + husky pre-commit hook.

## Self-check before task completion
- [ ] Did I follow the mandatory actions for this skill?
- [ ] Did I apply the patterns appropriate to the context?
- [ ] Did I verify the implementation meets the criteria above?
- [ ] Did I document decisions and trade-offs made?
