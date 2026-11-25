---
name: github
description: "Complete GitHub workflow — auth, repo management, PR lifecycle, issues, code review, CI, and releases via gh CLI and REST API."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, git, CLI, REST-API, Pull-Requests, Issues, Code-Review, CI-CD]
    related_skills: [plan, systematic-debugging, test-driven-development]
---

# GitHub — Complete Workflow Skill

Unified guide for all GitHub operations: authentication, repository management, pull requests, issues, code review, releases, and CI. Each section shows `gh` CLI first, then `git + curl` fallback.

## When to Use

- User needs to authenticate with GitHub (tokens, SSH, gh CLI)
- User needs to create/clone/fork/manage repos
- User wants to create or review PRs, manage issues
- User needs to set up secrets, releases, branch protection
- Any GitHub API or git remote operation

## Reference Files

Detailed references live in the skill's `references/` directory:

| Reference | Covers |
|-----------|--------|
| `references/github-api-cheatsheet.md` | Full REST API endpoint reference: repos, PRs, issues, actions, releases, secrets, pagination, rate limits, curl patterns |
| `references/pre-push-secret-audit.md` | Secret scanning pre-push checklist, `git rm --cached`, orphan-branch history rewrite, GitHub Secret Scanning response |
| `references/bloated-history-recovery.md` | Orphan-branch scalpel push, git-filter-repo, BFG — purge bloated files from history |
| `references/ci-troubleshooting.md` | CI failure patterns: test, lint, type, build, permission, timeout, Docker — with diagnosis steps and auto-fix decision tree |
| `references/conventional-commits.md` | Commit message format: types, scopes, breaking changes, issue linking |
| `references/project-git-conventions.md` | Extract & formalize git conventions from a project's existing commit history |
| `references/profile-readme.md` | GitHub profile README mechanics and user content conventions |
| `references/review-output-template.md` | PR review summary template, severity guide, inline comment format |
| `references/install-skill-from-github.md` | Install an agent skill from GitHub/ClawHub/iwencai — source verification, security audit, download, deps |
| `references/install-binary-from-github-releases.md` | Download & install a pre-built CLI binary from GitHub Releases — platform detect, checksum, PATH |

## Templates

| Template | Use |
|----------|-----|
| `templates/bug-report.md` | GitHub issue: bug report template |
| `templates/feature-request.md` | GitHub issue: feature request template |
| `templates/pr-body-bugfix.md` | PR description: bug fix |
| `templates/pr-body-feature.md` | PR description: feature/change |

## Scripts

| Script | Use |
|--------|-----|
| `scripts/gh-env.sh` | Auth detection and repo context: source this to auto-detect gh vs curl, set `$GITHUB_TOKEN`, `$GH_USER`, `$GH_OWNER`, `$GH_REPO` |

---

## Quick Start — Auth Detection

```bash
source "${HERMES_HOME:-$HOME/.hermes}/skills/github/scripts/gh-env.sh"
# Sets: GH_AUTH_METHOD, GITHUB_TOKEN, GH_USER, GH_OWNER, GH_REPO
```

If `gh` is not available or not authenticated, the script falls through to `curl` + token from `~/.hermes/.env` or `~/.git-credentials`.

---

## 1. Authentication

Two paths: **gh CLI** (rich API access) or **git-only** (no sudo needed).

### gh CLI Login

```bash
gh auth login                          # Interactive browser
gh auth status                         # Verify
echo "<token>" | gh auth login --with-token  # Headless
gh auth setup-git                      # Propagate to git
```

### Git-Only (HTTPS with PAT)

```bash
git config --global credential.helper store
# Then push once — git prompts for username + PAT
```

See `github-auth` subsection below for SSH key setup.

### Helper: Extract Token

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  GITHUB_TOKEN=$(gh auth token)
elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
  GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
fi
```

---

## Golden Rule — Commit is Not Done Until Push Succeeds

**On any shared repo with multiple collaborators, `git commit` and `git push` are a single atomic action.** Do not stop after staging or committing. The operation is only complete when:
1. `git push` succeeds (no network errors, no rejections)
2. `git status` confirms the local branch is up to date with `origin/HEAD`

This applies to ALL git changes — not just PR branches but also direct pushes to shared branches, file renames, AGENTS.md edits, README updates, anything that touches tracked files in a repo others pull from. A local-only commit blocks nobody; it's invisible to colleagues who do `git pull` and will cause them stale diffs or merge conflicts.

Common failure pattern: staging files after `mv` (instead of `git mv`), then getting distracted by the delete-add mismatch in `git status` and stopping without committing. Break out of this by doing `git add -A` to let git detect the rename, then commit + push immediately.

If push fails (network blip, auth issue), retry immediately — don't move on to the next task until `git status` shows clean.

**Summary:** `git status` → `git add -A` → `git commit` → `git push`. No gap.

## 2. Repository Management

### Clone

```bash
gh repo clone owner/repo
git clone https://github.com/owner/repo.git
```

### Create

```bash
gh repo create my-project --public --clone
curl -X POST -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"my-project","private":false}'
```

### Fork & Sync

```bash
gh repo fork owner/repo --clone
git remote add upstream https://github.com/owner/repo.git
git fetch upstream && git merge upstream/main
```

### Settings, Protect Branches, Releases

```bash
gh repo edit --description "..." --visibility public
gh release create v1.0.0 --generate-notes
```

See `references/github-api-cheatsheet.md` for full API endpoint reference.

---

## 3. Issues

### List, View, Create

```bash
gh issue list --state open --label "bug"
gh issue view 42
gh issue create --title "..." --body "..." --label "bug"
```

### Triaging (Labels, Assignees, Comments)

```bash
gh issue edit 42 --add-label "priority:high" --add-assignee @me
gh issue comment 42 --body "Investigating..."
gh issue close 42
```

### Templates

Use `templates/bug-report.md` and `templates/feature-request.md` for well-structured issue bodies.

---

## 4. Pull Requests

### Branch & Commit

```bash
git checkout -b feat/add-auth
git add . && git commit -m "feat(auth): add OAuth login"
git push -u origin HEAD
```

### Commit -> Push Immediately (Collaborative Repos)

When multiple people work on the same remote, **always push after every commit**. The remote is the shared source of truth -- a local-only commit blocks nobody until it's pushed, and the colleague who `git pull`s gets staleness errors or merge conflicts instead of the latest.

Rule: `git commit && git push` is a single logical action, not two separate events. Do not declare "committed" as done -- the operation is only complete after the push succeeds and `git status` confirms the branch is up to date with `origin/HEAD`.

Caveat: on single-developer repos or personal branches with no push notifications, this isn't critical. Detect the context: if the user mentions colleagues, a shared deploy branch, or a team repo, push immediately.

### Splitting a Batch of Changes into Individual Commits

When `git status` shows multiple modified files with distinct purposes, split them into logically separate commits rather than one large commit:

1. **Scan first** -- `git status` then `git diff --stat` to see the scope of every change
2. **Read diffs** -- `git diff <file>` for each file to understand what was actually changed
3. **Group by logic** -- files that share the same purpose (same feature, same bugfix, same doc section) go in one commit; unrelated changes go in separate commits
4. **Commit individually** -- `git add <file(s)> && git commit -m "type(scope): description"` for each group
5. **Push when done** -- push all commits at once (or after each one if working with a shared remote)

This produces a clean, reviewable commit history where each commit tells one coherent story. The `--stat` output shows the user the scale of each change before they review it, and read-file/grep calls give them the detail they need for the commit message body.

### Create PR

```bash
gh pr create --title "feat: ..." --body "$(cat templates/pr-body-feature.md)" --label "enhancement"
```

### Monitor CI

```bash
gh pr checks --watch
```

### Auto-Fix CI Loop

1. `gh run view <RUN_ID> --log-failed` → identify failure
2. Fix code → `git commit -m "fix: ..." && git push`
3. Re-check
4. Max 3 attempts per CI failure chain

### Merge

```bash
gh pr merge --squash --delete-branch
```

### Naming & Commit Conventions

Use Conventional Commits (`references/conventional-commits.md`):
- `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `ci:`, `chore:`, `perf:`

### PR Body Templates

Use `templates/pr-body-bugfix.md` for bug fixes and `templates/pr-body-feature.md` for features.

---

## 5. Code Review

### Local Pre-Push Review

```bash
git diff main...HEAD
git diff main...HEAD --stat
# Check for: secrets, debug prints, merge markers
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|<<<<<<\|======="
```

### PR Review (Other People's PRs)

```bash
gh pr diff 123 --name-only
gh pr checkout 123
# Review each file, run tests, then:
gh pr review 123 --approve --body "LGTM"
# Or with inline comments:
gh pr review 123 --request-changes --body "See inline comments."
```

### Review Output Format

Use `references/review-output-template.md` for structured review comments:
- 🔴 **Critical** — blocks merge (security, data loss, crashes)
- ⚠️ **Warnings** — should fix (non-critical bugs, missing error handling)
- 💡 **Suggestions** — non-blocking improvements
- ✅ **Looks Good** — positive reinforcement

### Pre-Push Security Scan

Before committing, always scan for:
```bash
# Hardcoded secrets
git diff --cached | grep "^+" | grep -iE "(api_key|secret|password|token)\s*=\s*['\"][^'\"]{6,}['\"]"
# Debug artifacts
git diff --cached | grep "^+" | grep -E "print\(|console\.log|TODO|FIXME|debugger"
# SQL injection
git diff --cached | grep "^+" | grep -E "execute\(f\"|\.format\(.*SELECT"
```

### Pre-Push Secret Audit for Config Repos

When pushing personal/dotfiles repos, run the full secret audit in `references/pre-push-secret-audit.md` to avoid leaking tokens, sessions, or credentials into git history.

---

## 6. GitHub Actions / CI

```bash
gh workflow list
gh run list --branch $(git branch --show-current) --limit 5
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID> --failed
gh workflow run ci.yml --ref main
```

### Secrets

```bash
gh secret set API_KEY --body "value"
gh secret list
```

### Branch Protection

```bash
curl -X PUT -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{"required_status_checks": {"strict": true, "contexts": ["ci/test"]}, "required_pull_request_reviews": {"required_approving_review_count": 1}}'
```

---

## 7. Install from GitHub

### Install a Skill from a Repo / Registry

Installing an agent skill from GitHub, ClawHub, or the iwencai SkillHub square — source identification, security verification, dependency install, validation. **Full workflow: `references/install-skill-from-github.md`.**

Key points:
- Identify source first: GitHub URL, ClawHub page, or iwencai square — each has a different workflow
- ClawHub installs: verify publisher, run `hermes skills inspect`, read security audit, **ask user before installing**
- GitHub installs: fetch README/INSTALL.md, detect skills dir, download files, install deps, validate
- Multi-skill repos (`skills/` dir with several SKILL.md): use `npx skills add <repo> -y -g` instead of manual download
- Skill + MCP-server combos: install npm package globally, copy skill to both Claude and Hermes, configure MCP in both
- iwencai square: check zip vs JSON response, set `IWENCAI_BASE_URL` / `IWENCAI_API_KEY`, scripts are pure stdlib

### Install a Pre-built Binary from Releases

Downloading and installing a CLI binary from GitHub Releases — check package manager first, platform/arch detection, checksum verify, PATH install. **Full workflow: `references/install-binary-from-github-releases.md`.**

Key points:
- Check `brew search <tool>` before GitHub Releases (prefer package manager)
- Detect platform: `uname -m` / `uname -s` (darwin-arm64, linux-amd64, ...)
- Get release info: `curl -s https://api.github.com/repos/OWNER/REPO/releases/latest`
- Verify checksum: download `.sha256`, compare with `shasum -a 256`
- Install to PATH: `chmod +x` then `mv` to `/usr/local/bin` (or `~/.local/bin` to avoid sudo)
- GFW/SSL failures: try `gh release download`, HTTP proxy (`export https_proxy=http://127.0.0.1:1082`), or `~/.local/bin`

---

## 8. Quick Reference Table

| Action | gh CLI | curl / git |
|--------|--------|------------|
| Auth check | `gh auth status` | `grep 'github.com' ~/.git-credentials` |
| Clone repo | `gh repo clone o/r` | `git clone https://github.com/o/r.git` |
| Create repo | `gh repo create n --public` | `curl POST /user/repos` |
| List issues | `gh issue list` | `curl GET /repos/o/r/issues` |
| Create issue | `gh issue create --title ...` | `curl POST /repos/o/r/issues` |
| Create PR | `gh pr create` | `curl POST /repos/o/r/pulls` |
| Merge PR | `gh pr merge --squash` | `curl PUT /repos/o/r/pulls/N/merge` |
| PR review | `gh pr review N --approve` | `curl POST /repos/o/r/pulls/N/reviews` |
| List workflows | `gh workflow list` | `curl GET /repos/o/r/actions/workflows` |
| Rerun CI | `gh run rerun N` | `curl POST /repos/o/r/actions/runs/N/rerun` |
| Create release | `gh release create v1.0` | `curl POST /repos/o/r/releases` |
| Set secret | `gh secret set KEY` | `curl PUT /repos/o/r/actions/secrets/KEY` |
| Repo info | `gh repo view` | `curl GET /repos/o/r` |
| Fork | `gh repo fork o/r` | `curl POST /repos/o/r/forks` |

---

## Pitfalls

- **Empty diff:** Check `git status` — nothing staged means no changes to review
- **Files vanished from working tree:** User may have moved them via Finder / file explorer. Do NOT `git checkout` to restore — that pulls the old tracked files back and creates a rename conflict with the user's new location. Instead: `ls` the expected location + nearby dirs to find the new path, then `git add` the new paths and `git rm --cached` the old ones (or `git add -A` to let git detect the rename). If push is rejected with a non-fast-forward, use `git push --force-with-lease` to match the on-disk state — the user's manual reorganization is the source of truth.
- **Large diff (>15k chars):** Split by file — `git diff HEAD -- specific_file.py`
- **`gh` not installed:** All operations work via `git + curl` with a `GITHUB_TOKEN`
- **Secrets in git / bloated history:** `git rm --cached` only prevents future tracking. Rotate leaked tokens. For history rewrites, see `references/bloated-history-recovery.md` — covers orphan-branch scalpel push, git-filter-repo, and BFG.
- **Credential expiry:** `gh` tokens expire. Re-run `gh auth login` or regenerate PAT.
- **403 on CI:** PRs from forks cannot access repo secrets by design.
- **Large CI log downloads:** Use `gh run view ID --log-failed` instead of downloading full zips.

## Verification Checklist

- [ ] Authentication: `gh auth status` or `GITHUB_TOKEN` set
- [ ] Auth source script: `source scripts/gh-env.sh` sets `$GH_AUTH_METHOD`, `$GH_USER`
- [ ] Git identity: `git config user.name` and `user.email` configured
- [ ] Branch naming: `feat/`, `fix/`, `refactor/`, `docs/`, `ci/` prefixes
- [ ] Conventional commits: type + (scope) + description
- [ ] Pre-commit scan: no secrets, no debug artifacts, no SQL injection
- [ ] CI: all checks pass before merge
- [ ] PR templates: use appropriate template from `templates/`
