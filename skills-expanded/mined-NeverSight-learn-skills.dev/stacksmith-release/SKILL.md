---
name: stacksmith-release
version: 1.0.0
description: "Release flow for any software project. Modes: prepare (pre-release checklist and PR creation), land (merge, tag, and confirm deployment), docs (sync changelogs and documentation). Trigger when cutting a release, shipping a feature branch, or syncing docs after a merge."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - AskUserQuestion
---

## Command routing

Parse the user's invocation:

- `/stacksmith-release prepare` -> PR-prep mode
- `/stacksmith-release land` -> merge and deploy mode
- `/stacksmith-release docs` -> documentation sync mode

If no mode is provided, ask whether they want `prepare` or `land`.

All timeline logs in this skill use:
- `skill: "stacksmith-release"`
- `mode: "ship" | "land-and-deploy" | "docs-sync"`

---

## Mode: `prepare`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
[ -z "$_BASE" ] && git rev-parse --verify origin/master >/dev/null 2>&1 && _BASE="master"
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
echo "BASE: $_BASE"
echo "REPO: $_REPO"
_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
echo "$_REMOTE" | grep -q "github.com" && echo "PLATFORM=github"
echo "$_REMOTE" | grep -q "gitlab" && echo "PLATFORM=gitlab"
which gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo "GH_CLI=true" || echo "GH_CLI=false"
_COMMITTERS=$(git log --since="30 days ago" --format="%ae" 2>/dev/null | sort -u | wc -l | tr -d ' ')
[ "${_COMMITTERS:-0}" -gt 1 ] && echo "REPO_MODE=collaborative" || echo "REPO_MODE=solo"
git fetch origin $_BASE --quiet 2>/dev/null || true
git diff origin/$_BASE --stat 2>/dev/null | tail -3
git log origin/$_BASE..HEAD --oneline 2>/dev/null
DIFF_LINES=$(git diff origin/$_BASE --stat 2>/dev/null | tail -1 | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
echo "DIFF_LINES: $DIFF_LINES"
```

### Step 1 - Pre-flight

1. If `BRANCH == BASE`: abort with "You're on the base branch. Ship from a feature branch."
2. `git status` - if uncommitted changes exist, describe them and ask whether to commit, stash, or abort.
3. Show what's being shipped:
   - `git diff origin/$_BASE --stat`
   - `git log origin/$_BASE..HEAD --oneline`

### Step 2 - Review readiness dashboard

Check if `stacksmith-review code` has been run on this branch:

```bash
_REVIEWED=$(grep "\"skill\":\"stacksmith-review\"" ~/.mystack/timeline.jsonl 2>/dev/null | \
  grep "\"mode\":\"code-review\"" | grep "\"branch\":\"$_BRANCH\"" | tail -1 || echo "")
[ -n "$_REVIEWED" ] && echo "REVIEW_STATUS=done" || echo "REVIEW_STATUS=none"
_REVIEW_DATE=$(echo "$_REVIEWED" | grep -oE '"ts":"[^"]*"' | cut -d'"' -f4 || echo "")
echo "REVIEW_DATE: ${_REVIEW_DATE:-never}"
_QA_REVIEWED=$(grep "\"skill\":\"stacksmith-qa\"" ~/.mystack/timeline.jsonl 2>/dev/null | \
  grep "\"branch\":\"$_BRANCH\"" | tail -1 || echo "")
[ -n "$_QA_REVIEWED" ] && echo "QA_STATUS=done" || echo "QA_STATUS=none"
_QA_DATE=$(echo "$_QA_REVIEWED" | grep -oE '"ts":"[^"]*"' | cut -d'"' -f4 || echo "")
echo "QA_DATE: ${_QA_DATE:-never}"
```

Display:

```text
+============================================================+
|              REVIEW READINESS DASHBOARD                     |
+============================================================+
| Review       | Status          | Date                      |
|--------------|-----------------|---------------------------|
| Code Review  | [DONE / MISSING]| [date or never]           |
| QA           | [DONE / MISSING]| [date or never]           |
+------------------------------------------------------------+
| VERDICT: [CLEARED / NOT CLEARED]                           |
+============================================================+
```

If `REVIEW_STATUS=none`:
- print "No prior code review found - prepare mode will run a lightweight inline review."
- if `DIFF_LINES > 200`: recommend `/stacksmith-review code`
- continue, do not block

### Step 3 - Sync with base

```bash
git fetch origin $_BASE
git merge origin/$_BASE --no-edit
```

If merge conflicts: show each conflict and ask whether to keep mine, keep theirs, or show both.

### Step 4 - Run tests

Detect and run the test suite:

```bash
[ -f package.json ] && _TEST_CMD=$(node -e "const p=require('./package.json'); console.log(p.scripts&&p.scripts.test||'npm test')" 2>/dev/null || echo "npm test")
[ -f Gemfile ] && _TEST_CMD="bundle exec rspec"
[ -f go.mod ] && _TEST_CMD="go test ./..."
[ -f Cargo.toml ] && _TEST_CMD="cargo test"
[ -f requirements.txt ] && _TEST_CMD="python -m pytest"
_CLAUDE_TEST=$(grep -A2 "## Testing" CLAUDE.md 2>/dev/null | grep -v "^##" | head -1 | tr -d ' ')
[ -n "$_CLAUDE_TEST" ] && _TEST_CMD="$_CLAUDE_TEST"
echo "TEST_CMD: $_TEST_CMD"
$_TEST_CMD 2>&1 | tee /tmp/mystack_tests.txt
```

Test failure ownership triage:
- in-branch failure -> stop, fix before shipping
- pre-existing failure -> classify based on repo mode and ask how to handle

If collaborative and GH CLI is available, issue creation is allowed for pre-existing failures.

### Step 5 - Coverage audit

Goal: 100 percent of new code paths have at least one test.

```bash
find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" -o -name "*_spec.*" | grep -v node_modules | wc -l
```

For each changed file:
1. read the file
2. search for corresponding test file
3. trace every function, branch, and error path

Coverage rubric:
- strong: behavior + edge cases + error paths
- medium: happy path only
- weak: implementation tests
- none: no tests

If test framework is missing, offer the same bootstrap flow as `/stacksmith-qa`.

### Step 6 - Pre-landing review (if no prior code review)

If `REVIEW_STATUS=none`, run a lightweight inline review using the critical-only checklist from `/stacksmith-review code`:
- SQL injection
- race conditions
- auth boundaries
- missing error handling
- obvious security issues

If critical issues are found: fix or get approval before pushing.

### Step 7 - Push and open PR

```bash
git push origin $_BRANCH
```

If GH CLI is available:

```bash
gh pr create \
  --title "[auto-detect from branch name and commits]" \
  --body "$(cat <<'EOF'
## What
[1-2 sentences: what does this change do]

## Why
[Why is this needed]

## How
[Brief technical description]

## Testing
- Tests run: N passed
- Coverage: [summary]
- QA: [what was manually tested]

## Checklist
- [ ] Tests pass
- [ ] No secrets committed
- [ ] Migrations reversible (if applicable)
- [ ] Docs updated (or /stacksmith-release docs run)
EOF
)"
```

If no GH CLI: print the PR description for the user to copy.

### Step 8 - Ship report

```text
## Release Report [branch] [date]

Tests: N passed, N failed (N pre-existing, handled)
Coverage: [summary]
Pre-landing review: [SKIPPED / N issues found, N fixed]
PR: [URL or "ready - push manually"]

Status: shipped
Next: Run /stacksmith-release docs to update documentation
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-release\",\"mode\":\"ship\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `land`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
echo "BASE: $_BASE"
_REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
echo "$_REMOTE" | grep -q "github.com" && echo "PLATFORM=github"
echo "$_REMOTE" | grep -q "gitlab" && echo "PLATFORM=gitlab"
which gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1 && echo "GH_CLI=true" || echo "GH_CLI=false"
[ -f fly.toml ] && echo "DEPLOY_PLATFORM=fly"
[ -f render.yaml ] && echo "DEPLOY_PLATFORM=render"
( [ -f vercel.json ] || [ -d .vercel ] ) && echo "DEPLOY_PLATFORM=vercel"
[ -f netlify.toml ] && echo "DEPLOY_PLATFORM=netlify"
[ -f Procfile ] && echo "DEPLOY_PLATFORM=heroku"
grep -i "production.*url\|prod.*url\|PROD_URL" CLAUDE.md 2>/dev/null | head -3
gh pr view --json number,title,state,baseRefName 2>/dev/null | head -5 || echo "GH_PR=not_found"
```

If `GH_CLI=false`: "No GitHub CLI found. Run `gh auth login` to enable auto-merge. Alternatively, merge the PR manually and re-run `/stacksmith-release land` to handle deploy verification."

### Step 1 - Pre-flight

1. If no PR found: ask for the PR number or URL.
2. Validate PR state:

```bash
gh pr view --json state,reviewDecision,mergeable,statusCheckRollup -q '{state:.state, mergeable:.mergeable, reviews:.reviewDecision}'
```

- if already merged: skip to deploy verification
- if conflicting: stop
- if CI is failing: stop and show the failing checks

3. Tell the user what PR was found and current CI status.

### Step 2 - Wait for CI (if pending)

```bash
gh pr checks --watch 2>/dev/null || echo "Watching CI... (ctrl+c to stop and merge anyway)"
```

Poll every 30 seconds, up to 20 minutes. Report progress every 3 minutes.

If checks fail, ask whether to investigate now, merge anyway, or abort.

### Step 3 - Merge

```bash
gh pr merge --auto --squash --delete-branch 2>/dev/null || \
gh pr merge --squash --delete-branch 2>/dev/null
```

If a merge queue exists, wait for the final merge commit checks.

### Step 4 - Detect deploy strategy

```bash
gh run list --branch $_BASE --limit 5 --json name,status,workflowName,headSha,createdAt 2>/dev/null
```

Determine deploy type:
- CI/CD auto-deploy
- Fly.io
- Vercel
- Render
- Manual

### Step 5 - Wait for deploy

If CI/CD workflow detected:

```bash
gh run watch $(gh run list --branch $_BASE --limit 1 --json databaseId -q '.[0].databaseId' 2>/dev/null) 2>/dev/null
```

Poll every 30 seconds, up to 15 minutes. Report every 2 minutes.

If deploy fails: show the failing step and ask whether to show logs, roll back, or handle manually.

### Step 6 - Verify production health

```bash
_PROD_URL=$(grep -i "production.*url\|PROD_URL" CLAUDE.md 2>/dev/null | sed 's/.*: *//' | head -1)
if [ -n "$_PROD_URL" ]; then
  _STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$_PROD_URL" 2>/dev/null)
  echo "PROD_STATUS: $_STATUS"
  _TIME=$(curl -s -o /dev/null -w "%{time_total}" "$_PROD_URL" 2>/dev/null)
  echo "RESPONSE_TIME: ${_TIME}s"
fi
```

Health checks:
- HTTP 200?
- response time under 3s?
- no obvious response-body errors?

If health check fails: ask whether to roll back, wait, or treat it as known.

### Step 7 - Revert (if needed)

```bash
git revert --no-edit <merge-commit-sha>
git push origin $_BASE
gh pr create --title "Revert: [original PR title]" --body "Reverting due to production issue."
```

### Step 8 - Deploy report

```text
## Deploy Report [date]

PR: #N - [title]
Merged: [timestamp] ([duration from open to merge])
Deploy: [platform] - [duration]
Production: [URL] - [HTTP status] - [response time]

### Checks
- CI: [N checks passed]
- Deploy: [success/failed]
- Health: [healthy / degraded / down]

### Next steps
- Run /stacksmith-release docs to update documentation
- Run /stacksmith-ops retro at end of week
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-release\",\"mode\":\"land-and-deploy\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `docs`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
git log --oneline -10 2>/dev/null
git diff origin/$_BASE --name-only 2>/dev/null | head -30
find . -name "*.md" -not -path "*/node_modules/*" -not -path "*/.git/*" | sort
```

### Rule: only update what actually changed

Do not:
- add features not yet shipped
- remove warnings or caveats without reason
- rewrite sections that are still accurate
- change voice or tone significantly

Do:
- fix commands and steps that no longer work
- update feature lists to match what was shipped
- add new sections for new functionality
- remove references to removed functionality
- update CHANGELOG with what was shipped

### Step 1 - Audit each doc

For each `.md` file found, check against the diff:

| Doc | Check |
|-----|-------|
| README.md | Install steps still work? Features list current? Commands valid? |
| ARCHITECTURE.md | Diagrams match current structure? New services documented? |
| CHANGELOG.md | Unreleased section reflects this branch? Format correct? |
| CONTRIBUTING.md | Dev setup steps still accurate? Test commands valid? |
| CLAUDE.md | Skill references up to date? Custom commands documented? |
| docs/*.md | Technical details match current implementation? |

### Step 2 - Update with approval

For each file that needs a change:
1. show the exact diff you're about to make
2. ask: "Update this? (A: yes / B: no / C: show more context)"
3. on yes: apply change
4. commit: `git commit -m "docs: update [filename] - [what changed and why]"`

### Step 3 - CHANGELOG entry (if applicable)

If no CHANGELOG exists and there were meaningful changes, offer to create one.

Format for a new entry:

```markdown
## [Unreleased]

### Added
- [New feature or behavior]

### Changed
- [Changed behavior]

### Fixed
- [Bug fix]
```

### Report

```text
## Docs Sync [date]

### Updated
- [filename] - [what changed]

### Checked, no changes needed
- [filename]

### Missing docs (consider adding)
- [filename] - reason

### Commits
- [hash] docs: [description]
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-release\",\"mode\":\"docs-sync\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
