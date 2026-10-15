---
name: stacksmith-qa
version: 1.0.0
description: "QA flow for any software project. Default mode runs the full test-fix-verify loop; report-only and quick variants available. Trigger when running tests, verifying a bug fix, auditing test coverage, or doing a QA pass before a release."
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

- `/stacksmith-qa` -> full QA mode
- `/stacksmith-qa --report-only` -> report-only mode
- `/stacksmith-qa --quick [URL]` -> quick variant

If both `--report-only` and `--quick` are present, stay in report-only mode and use the quick scope.

All timeline logs in this skill use:
- `skill: "stacksmith-qa"`
- `mode: "qa" | "qa-only"`

---

## Shared preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
echo "BASE: $_BASE"
echo "REPO: $_REPO"
[ "$_BRANCH" = "$_BASE" ] && echo "ON_BASE=true" || echo "ON_BASE=false"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
( [ -f requirements.txt ] || [ -f pyproject.toml ] ) && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
ls jest.config.* vitest.config.* playwright.config.* cypress.config.* .rspec pytest.ini 2>/dev/null
ls -d test/ tests/ spec/ __tests__/ e2e/ 2>/dev/null
mkdir -p ~/.mystack/qa-reports
_REPORT_FILE="$HOME/.mystack/qa-reports/$(date +%Y%m%d-%H%M%S)-qa-report.md"
echo "REPORT_FILE: $_REPORT_FILE"
```

Mode selection:
- diff-aware mode when on a feature branch with no URL provided
- URL mode when URL is provided
- quick mode when `--quick` is present

If no URL and `ON_BASE=true`: "You're on the base branch. Either switch to a feature branch for diff-aware testing, or provide a URL."

---

## Mode: full QA (`mode = qa`)

### Diff-aware mode

When activated with no URL on a feature branch:

#### Phase 1 - Analyze the diff

```bash
git fetch origin $_BASE --quiet
git diff origin/$_BASE --name-only
git log origin/$_BASE..HEAD --oneline
cat TODOS.md 2>/dev/null | head -20
```

Identify affected routes/pages from changed files:
- controller/route files -> which URL paths they serve
- view/template/component files -> which pages render them
- model/service files -> which pages use those models
- API files -> test endpoints directly
- CSS files -> which pages include them

Framework detection:

```bash
grep -r "resources\|get\|post\|put\|delete\|patch" config/routes.rb 2>/dev/null | head -20
find . -name "*.ts" -o -name "*.js" | xargs grep -l "router\.\|app\." 2>/dev/null | head -10
grep -r "@app\.\|@router\." --include="*.py" 2>/dev/null | head -20
```

Detect running app:

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null && echo "APP:3000" || \
curl -s -o /dev/null -w "%{http_code}" http://localhost:4000 2>/dev/null && echo "APP:4000" || \
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null && echo "APP:8080" || \
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null && echo "APP:5173" || \
echo "APP:not_found"
```

If no running app: ask the user for the URL or how to start it.

#### Phase 2 - Build test plan

For each affected route/page, build a test matrix:

| Route/Page | Change type | Tests to run | Priority |
|-----------|-------------|--------------|----------|
| `/payments/new` | Added validation | Submit empty, invalid, valid | P0 |
| `/api/users/:id` | Auth check added | Unauthenticated, wrong user, correct user | P0 |
| `/dashboard` | New component | Renders, empty state, error state | P1 |

Cross-reference commit messages and TODOs to verify the branch does what it was supposed to do.

#### Phase 3 - Execute tests

API/backend examples:

```bash
curl -s -X POST http://localhost:3000/api/payments \
  -H "Content-Type: application/json" \
  -d '{}' | jq .

curl -s http://localhost:3000/api/users/2 \
  -H "Authorization: Bearer <user-1-token>" | jq .
```

Frontend/UI testing: describe each step, expected state, and actual state.

For each test:
- Pass - describe what was verified
- Fail - exact symptom and evidence
- Unexpected - anything unplanned that happened

#### Phase 4 - Fix loop

For each failure:
1. locate root cause first
2. write the minimal fix
3. write a regression test that would have caught this specific bug
4. commit atomically:

```bash
git add -p
git commit -m "fix: [exact description]\n\nRegression: [test name that covers this]"
```

5. re-test the failing case

Iron Law: every bug fixed must add one regression test.

### URL mode (systematic exploration)

#### Phase 1 - Orient

```bash
curl -s -o /dev/null -w "%{http_code}" <URL>
```

Map the application:
- visit the homepage
- list navigation targets
- detect framework
- check for console errors on landing

#### Phase 2 - Explore

At each page:
1. visual scan
2. interactive elements
3. forms
4. navigation
5. states
6. responsiveness at 375px

Core features get thorough coverage. Secondary pages get a light scan.

#### Phase 3 - Document issues immediately

```text
ISSUE-NNN: [title]
Severity: P0 / P1 / P2
Steps to reproduce:
  1. [step]
  2. [step]
  3. [result]
Expected: [what should happen]
Actual: [what actually happens]
Evidence: [screenshot path or curl output]
```

#### Phase 4 - Fix loop

Same as diff-aware mode.

#### Phase 5 - Health score

Compute category scores and weighted average:

| Category | Weight | Score | How to score |
|----------|--------|-------|-------------|
| Console errors | 15% | ? | 0 errors=100, 1=80, 3+=40 |
| Broken links | 10% | ? | 0=100, 1=85, 3+=50 |
| Form handling | 20% | ? | All forms work=100, 1 broken=60 |
| Navigation | 15% | ? | All paths work=100, 1 dead end=75 |
| Error states | 15% | ? | All handled=100, silent failures=40 |
| Visual quality | 10% | ? | No obvious issues=100, layout broken=50 |
| Mobile usability | 15% | ? | Works one-handed=100, broken=30 |

Interpretation:
- 90-100: ship it
- 75-89: minor issues, fix before ship
- 60-74: significant issues, fix before ship
- below 60: major issues, do not ship

### Report

```text
## QA Report [feature/URL] [date]

### Mode: [diff-aware | URL | quick]
### Branch: [branch] | Base: [base]

### Summary
Tests run: N | Passed: N | Failed: N | Fixed: N (with regression tests)
Health score: N/100 [interpretation]

### Changes tested
- [route/component] - [result]

### Bugs found & fixed
1. [description] - file:line - regression test: [test name]

### Issues found (not yet fixed)
1. [ISSUE-NNN] [P0] [description] - blocking: [yes/no]

### Regression tests added
- [test file]: [test names]

### Recommendation
[SHIP / FIX FIRST / INVESTIGATE]
```

### Test framework bootstrap (if no tests exist)

If no framework is detected, offer to bootstrap:

```text
No test framework found. I can set one up that fits this project.

RECOMMENDATION: A - add tests now. Every stacksmith-qa bug fix adds a regression test,
and without a framework, that is not possible.

A) Bootstrap the best-fit framework with a basic passing test
B) Skip - I'll add tests later
```

If A: scaffold and commit separately as `git commit -m "test: bootstrap [framework]"`.

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-qa\",\"mode\":\"qa\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: report-only (`mode = qa-only`)

### Core rule

This mode reports only. It never:
- edits any file
- runs `git commit`
- fixes bugs
- makes code changes of any kind

Every bug found goes into the report. Zero changes to the codebase.

### Scope

If URL provided: use it.

If no URL and on a feature branch:

```bash
git diff origin/$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||') --name-only 2>/dev/null | head -20
git log --oneline -5 2>/dev/null
```

Identify affected routes from changed files. Detect running app:

```bash
for port in 3000 4000 8080 5173 5000; do
  curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port" 2>/dev/null | grep -q "200\|301\|302" && echo "APP_URL=http://localhost:$port" && break
done
```

### Build test plan

| Test case | URL/action | What to check | Priority |
|-----------|-----------|---------------|----------|
| Homepage loads | / | Status 200, no console errors | P0 |
| Primary flow | [diff-derived or specified] | End-to-end | P0 |
| Auth boundary | Protected route, no auth | Redirect to login | P0 |
| Form validation | Empty submit | Error shown | P1 |
| Empty state | List with no data | Helpful message | P1 |
| Mobile | Homepage at 375px | Layout intact | P2 |

### Execute tests

For each test case, describe:
1. what action was taken
2. what was observed
3. result: Pass / Fail / Unexpected

Backend/API examples:

```bash
curl -s -X GET "http://localhost:<port>/api/resource" | python3 -m json.tool 2>/dev/null | head -20
curl -s -X GET "http://localhost:<port>/api/protected" | head -5
curl -s -X POST "http://localhost:<port>/api/resource" \
  -H "Content-Type: application/json" \
  -d '{}' | head -10
grep -i "error\|exception\|fatal" log/development.log 2>/dev/null | tail -10
```

### Document each bug immediately

```text
ISSUE-NNN: [title]
Severity: P0 / P1 / P2
Found on: [URL or route]
Steps to reproduce:
  1. [step]
  2. [step]
  3. [observed result]
Expected: [what should happen]
Actual: [what actually happens]
Suggested fix: [optional]
```

### Health score

| Category | Weight | Score | Basis |
|----------|--------|-------|-------|
| Console errors | 15% | ? | 0=100, 1=80, 3+=40 |
| Broken links/routes | 10% | ? | 0=100, 1=85, 3+=50 |
| Form handling | 20% | ? | All forms work=100, 1 broken=60 |
| Auth boundaries | 15% | ? | All enforced=100, 1 bypass=20 |
| Error states | 15% | ? | Handled gracefully=100 |
| Visual quality | 10% | ? | No obvious issues=100 |
| Mobile | 15% | ? | Works at 375px=100 |

Composite = weighted average.

### Write report file

Write to `~/.mystack/qa-reports/<timestamp>-qa-report.md`:

```markdown
# QA Report <feature/URL>
_<date> - /stacksmith-qa --report-only - <branch>_

## Summary
- **Mode:** [diff-aware | URL | quick]
- **Tests run:** N
- **Passed:** N
- **Failed:** N
- **Health score:** N/100

## Health Score Breakdown
| Category | Score | Notes |
[table]

## Bugs Found

### P0 - Blockers
[issues]

### P1 - Broken features
[issues]

### P2 - Minor/cosmetic
[issues]

## Passed checks
- [what passed]

## Testing environment
- URL: [tested URL]
- Branch: [branch]
- Date: [date]
```

Tell the user: "Report written to `~/.mystack/qa-reports/<filename>`. N bugs found - none were fixed. Use `/stacksmith-qa` for the full test-fix-verify loop."

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-qa\",\"mode\":\"qa-only\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
