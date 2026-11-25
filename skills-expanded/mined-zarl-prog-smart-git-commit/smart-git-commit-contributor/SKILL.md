---
name: smart-git-commit-contributor
description: >
  Use this skill when contributing to ANY open source repo or team
  codebase — forking, branching, committing, opening PRs, or responding
  to review comments. Triggers on: "open a PR", "contribute to",
  "fork this repo", "submit my changes", "respond to review",
  "address feedback", "my PR got a comment", "prepare contribution",
  "make my PR better", "ready to submit". Produces PRs that look
  professional, get reviewed faster, and get merged. Handles the full
  contributor lifecycle from fork to merge.
---

# Smart Git Commit — Contributor Skill

Extends the base skill with a full contributor workflow. Use this when
contributing to any open source repo. Follow every phase in order.

<!-- line-limit: 400 -->

---

## Phase 0: Fork and Sync Check

Run the fork sync checker:

```bash
bash contributor/scripts/fork-check.sh
```

Checks performed:
- Is this a fork? (`git remote -v` shows both `origin` and `upstream`)
- Is the fork up to date with upstream main?
  - `git fetch upstream`
  - `git log HEAD..upstream/main --oneline`
- If behind: rebase before doing anything else
  - `git rebase upstream/main`
- If no upstream set: asks for the original repo URL
  - `git remote add upstream <url>`

**Output**: `SYNCED` or list of commits the contributor is behind.

---

## Phase 1: Branch Naming

Run the branch name enforcer:

```bash
bash contributor/scripts/branch-name.sh
```

**Never contribute from `main` or `master`.**

Enforced pattern:
```
<type>/<issue-number>-<short-description>
```

Examples:
- `feat/234-add-oauth-login`
- `fix/189-resolve-token-expiry`
- `docs/301-update-contributing-guide`
- `chore/445-upgrade-axios`

If on the wrong branch: creates a correctly named one automatically:
```bash
git checkout -b <correct-name>
```

---

## Phase 2: Commit Quality

Reuse the existing SKILL.md phases 1–7 for every commit.

Every commit uses the **5-part format**:
```
CONTEXT / CHANGE / WHY / IMPACT / footers
```

Read `skills/smart-git-commit/SKILL.md` Phase 5 for full rules.

**Remember**: Maintainers judge contribution quality by commit quality.
A structured commit = trusted contributor, faster review.

---

## Phase 3: PR Readiness Check

Run the readiness checker:

```bash
bash contributor/scripts/pr-readiness.sh
```

Checklist (hard stops marked with **✗**, warnings marked with **⚠**):

| Check | Type |
|-------|------|
| ✗ Tests pass (run the repo's test suite) | Hard stop |
| ✗ No secrets in diff (reuse scan-secrets.sh) | Hard stop |
| ✗ Not targeting `main` directly (must be feature branch) | Hard stop |
| ✗ Fork is synced with upstream (no merge conflicts) | Hard stop |
| ⚠ CONTRIBUTING.md rules followed | Warning |
| ⚠ Related issue linked | Warning |
| ⚠ Docs updated if behavior changed | Warning |
| ⚠ Screenshots added if UI changed | Warning |
| ⚠ Breaking change documented | Warning |

**Output**: `READY` or list of blocking items with fix instructions.

---

## Phase 4: PR Title Construction

Read `contributor/templates/pr-title.md` for the complete guide.

Formula:
```
<type>(<scope>): <imperative summary under 72 chars>
```

Same rules as commit subject line — imperative mood, no period.

**The PR title IS the merge commit message on most repos.**
It must make sense in a CHANGELOG.

| Good | Bad |
|------|-----|
| `feat(auth): add Google OAuth login with refresh token rotation` | `Added oauth stuff and fixed some things` |
| `fix(api): handle null response on connection timeout` | `fixed a bug` |

---

## Phase 5: PR Body Construction

Read `contributor/templates/pr-body-full.md` for the complete template.

Build a PR body with these exact sections:

| Section | Content |
|---------|---------|
| **What changed and why** | Paste CHANGE and WHY from commit messages |
| **Context** | Paste CONTEXT from commit messages |
| **Type of change** | Checkboxes for bug fix, feature, breaking, docs, perf, refactor |
| **How to test** | Numbered steps a maintainer can follow to verify |
| **Screenshots** | Before/after if UI changed |
| **Related issues** | `Closes #N` or `Refs #N` |
| **Checklist** | Tests, secrets, docs, CONTRIBUTING, breaking changes |
| **Notes for maintainer** | Trade-offs, follow-up work, things to flag |

---

## Phase 6: Create the PR

1. Read `contributor/templates/pr-body-full.md` to build the body
2. Run the readiness check: `bash contributor/scripts/pr-readiness.sh`
3. If **READY**:

```bash
gh pr create \
  --title "<phase 4 title>" \
  --body "<phase 5 body>" \
  --draft
```

**Always draft first** — never open a ready-for-review PR without
telling the user and getting confirmation.

After creation: show the PR URL and say "mark as ready when you've
done a final self-review."

---

## Phase 7: Responding to Review Comments

**Triggers**: "my PR got a comment", "respond to review",
"address feedback", "maintainer said..."

Run the review response helper:

```bash
bash contributor/scripts/review-response.sh
```

### Response Rules

1. **Always thank** the reviewer by name first (one line, genuine)
2. For each comment: **acknowledge** → **explain your thinking** → **show the fix**
3. **Never argue**, never get defensive
4. If you disagree: explain your reasoning once, clearly, then **defer**
5. After fixing: **push new commits**, **resolve conversations**, **post summary**

### Response Format

Read `contributor/templates/review-response.md` for the template.

### After All Fixes Are Addressed

```bash
git add <fixed files>
git commit  # Use 5-part format with type "fix" or "refactor"
git push origin <branch>
gh pr comment --body "All review comments addressed in <commit hash>"
```
