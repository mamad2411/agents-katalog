---
name: branch-protection-rules
description: >
  Configure and audit GitHub/GitLab branch protection: required status checks, block
  force-push and deletion, linear history, admin/owner enforcement, and CODEOWNERS-required
  reviews. Use when branch protection, protected branch, required checks, force-push ban,
  require linear history, enforce admins, CODEOWNERS gate, merge request approval rules,
  hardening main/master, or release branch policies.
---

# Branch Protection Rules

## Scope And Authorization

- **In scope:** Git hosts and repositories you administer (GitHub, GitLab, Bitbucket-like controls).
- **Out of scope:** Disabling protections on repos you do not own; social-engineering admins for bypass.
- Changes to org-level rulesets affect many repos — use change tickets.
- Redact webhook secrets and deploy keys in screenshots.
- Pair with `ci-cd-pipeline-patterns`, `commit-message-conventions`, and `code-quality-standards`.

## When To Use

- Hardening `main`/`master`/`release/*` against direct pushes and force-pushes.
- Requiring PR/MR reviews, CODEOWNERS, and green CI checks before merge.
- Enabling org rulesets / required workflows centrally.
- Auditing admin bypass, stale required checks, or unprotected default branches.
- Preparing for compliance (SOC2 change management evidence).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CI pipeline design | `ci-cd-pipeline-patterns` |
| Secret scanning in git | `secrets-management-hygiene` / gitleaks |
| CODEOWNERS authoring style only | `code-review-comments-style` / ownership docs |
| Signed commits deep policy | git signing skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Target state (typical prod) |
| --- | --- |
| Direct push | Denied to default branch |
| Force push | Denied |
| Branch deletion | Denied for default/release |
| Required reviews | ≥1 (or 2 for critical); dismiss stale on new commits |
| CODEOWNERS | Required for owned paths if used |
| Status checks | Required, **latest** job names; no “any check” |
| Admin enforcement | Include administrators / no free bypass |
| History | Prefer linear (squash/rebase) if team agrees |
| Rulesets (GitHub) | Org-wide baseline + repo overrides |

## Workflow

### 1. Confirm scope and success criteria

1. Record org, repos, default branch names, critical vs sandbox repos.
2. Success: cannot push to main without PR; force-push denied; CI required; admins included; break-glass documented.
3. Inventory bots that need exception (release automation) — use fine-grained bypass actors, not “admins unrestricted”.

### 2. Inventory current protection

**GitHub CLI examples:**

```bash
gh api repos/:owner/:repo/branches/main/protection
gh api repos/:owner/:repo/rulesets
gh api orgs/:org/rulesets
# Who has admin
gh api repos/:owner/:repo/collaborators --jq '.[] | select(.role_name=="admin") | .login'
```

**GitLab:**

```bash
# Project protected branches API / UI: Settings → Repository → Protected branches
# Check: Allowed to merge/push, code owner approval, status checks
```

1. List required check names — compare to actual CI job names after renames.
2. Flag: protection exists but “Do not allow bypassing” off; or ruleset not enforced.
3. Note deployment branches and hotfix process.

### 3. Baseline and communicate

1. Screenshot/export current rules before change.
2. Announce to engineers: PR-only workflow, how hotfixes work.
3. Ensure CI is stable — flaky required checks block the org.

### 4. Apply protection (GitHub classic + rulesets)

**Classic branch protection (conceptual UI/API fields):**

1. Require pull request before merging.
2. Required approving reviews (count); require review from CODEOWNERS.
3. Dismiss stale pull request approvals when new commits are pushed.
4. Require status checks to pass; require branches to be up to date (if desired).
5. Require conversation resolution.
6. Restrict who can push (empty for PR-only).
7. Do not allow force pushes; do not allow deletions.
8. **Do not allow bypassing the above settings** (include admins).
9. Optional: require signed commits; require linear history; lock branch.

**GitHub ruleset sketch (org or repo):**

```json
{
  "name": "protect-default",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": { "include": ["refs/heads/main", "refs/heads/release/*"] }
  },
  "rules": [
    { "type": "pull_request", "parameters": {
      "required_approving_review_count": 1,
      "dismiss_stale_reviews_on_push": true,
      "require_code_owner_review": true
    }},
    { "type": "required_status_checks", "parameters": {
      "strict": true,
      "required_status_checks": [
        { "context": "lint" },
        { "context": "test" }
      ]
    }},
    { "type": "non_fast_forward" },
    { "type": "deletion" }
  ],
  "bypass_actors": []
}
```

**GitLab protected branch / MR approval:**

1. Allowed to merge: Maintainers (via MR); Allowed to push: No one (or robots).
2. Enable “Code owner approval” and approval rules (CODEOWNERS file).
3. Pipelines must succeed; optional “merge trains”.
4. Prevent force push on protected branches.

### 5. CODEOWNERS and bots

```text
# .github/CODEOWNERS or CODEOWNERS
* @org/app-team
/docs/ @org/tech-writers
/.github/workflows/ @org/platform-team
```

1. Invalid CODEOWNERS silently weakens required reviews — validate users/teams exist.
2. For release bots: use GitHub App with bypass on ruleset **limited** to that app, not all admins.
3. Pair with required status checks named **exactly** as check runs appear.

### 6. Verify with evidence

```bash
# Expect rejection
git checkout main
echo test >> README.md && git commit -am "should fail" && git push origin main || true
# PR path should work with approvals + checks
gh pr create --fill
gh pr checks
```

1. Admin account: confirm cannot force-push when enforce admins is on.
2. Rename a CI job intentionally in a branch — confirm protection fails until rules updated (document process).
3. Store before/after API JSON in the change ticket.

### 7. Operate and hand off

1. Break-glass: temporary ruleset bypass with ticket + expiry + post-review of commits.
2. Quarterly audit: rulesets, admin list, unused required checks, bot identities.
3. Document hotfix: PR with expedited review, not direct push.
4. Apply `code-quality-standards` to workflow YAML changes.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Admins | Enforced like everyone | “Admins can bypass” always on |
| Checks | Exact current job names | Required check name from 2022, always skipped |
| Bots | App-scoped bypass | Personal PATs with admin |
| Reviews | CODEOWNERS + dismiss stale | One rubber-stamp always |
| Force push | Blocked on main | Allowed “for cleanup” |
| Org baseline | Rulesets on all prod repos | Only one hero repo protected |

## Output Checklist

- [ ] Repo/org list and default branches inventoried
- [ ] Baseline protection exported
- [ ] PR reviews + CODEOWNERS configured
- [ ] Required status checks match live CI names
- [ ] Force-push and deletion blocked
- [ ] Admin bypass disabled or tightly controlled
- [ ] Bot exceptions documented and minimal
- [ ] Push-without-PR test fails as expected
- [ ] Break-glass procedure written with expiry
- [ ] `code-quality-standards` for related automation

## Rules

- Prefer org rulesets for baseline consistency.
- Never leave default branch unprotected on production code.
- Treat protection bypass as a privileged action with audit.
- Keep required checks reliable — flaky CI causes shadow bypass culture.
- This skill is SCM policy; CI contents live in `ci-cd-pipeline-patterns`.
