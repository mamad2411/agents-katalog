---
name: stacksmith-review
version: 1.0.0
description: "Review suite for any software project. Modes: code (diff and logic review), design (UI/UX quality audit), security (vulnerability and threat surface scan). Trigger when reviewing a PR or diff, auditing UI quality, or checking for security issues before merging or shipping."
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
  - WebSearch
---

## Command routing

Parse the user's invocation:

- `/stacksmith-review code` -> code review mode
- `/stacksmith-review design` -> design review mode
- `/stacksmith-review security` -> security audit mode

If no mode is provided, ask which review mode they want.

All timeline logs in this skill use:
- `skill: "stacksmith-review"`
- `mode: "code-review" | "design-review" | "security"`

---

## Mode: `code`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_REPO=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
echo "REPO: $_REPO"
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
[ -z "$_BASE" ] && git rev-parse --verify origin/main >/dev/null 2>&1 && _BASE="main"
[ -z "$_BASE" ] && git rev-parse --verify origin/master >/dev/null 2>&1 && _BASE="master"
_BASE="${_BASE:-main}"
echo "BASE: $_BASE"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
( [ -f requirements.txt ] || [ -f pyproject.toml ] ) && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
[ -f Cargo.toml ] && echo "STACK:rust"
git fetch origin $_BASE --quiet 2>/dev/null || true
DIFF_INS=$(git diff origin/$_BASE --stat 2>/dev/null | tail -1 | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo "0")
DIFF_DEL=$(git diff origin/$_BASE --stat 2>/dev/null | tail -1 | grep -oE '[0-9]+ deletion' | grep -oE '[0-9]+' || echo "0")
DIFF_TOTAL=$((DIFF_INS + DIFF_DEL))
echo "DIFF_LINES: $DIFF_TOTAL"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(auth|login|session|token|password|permission|role|access)' && echo "SCOPE_AUTH=true" || echo "SCOPE_AUTH=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '\.(rb|py|go|rs|java|cs|php)$' && echo "SCOPE_BACKEND=true" || echo "SCOPE_BACKEND=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '\.(tsx?|jsx?|vue|svelte|css|scss)$' && echo "SCOPE_FRONTEND=true" || echo "SCOPE_FRONTEND=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(migration|schema|\.sql)' && echo "SCOPE_MIGRATIONS=true" || echo "SCOPE_MIGRATIONS=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(api|routes|endpoints|controllers)' && echo "SCOPE_API=true" || echo "SCOPE_API=false"
_COMMITTERS=$(git log --since="30 days ago" --format="%ae" 2>/dev/null | sort -u | wc -l | tr -d ' ')
[ "${_COMMITTERS:-0}" -gt 1 ] && echo "REPO_MODE=collaborative" || echo "REPO_MODE=solo"
```

If on the base branch with no diff: "Nothing to review - you're on the base branch. Switch to a feature branch."

### Step 1 - Scope drift detection

Before reviewing code quality, check whether they built what was requested:

```bash
git log origin/$_BASE..HEAD --oneline 2>/dev/null
cat TODOS.md 2>/dev/null | head -20
cat PLAN.md 2>/dev/null | head -30
```

Identify stated intent from commit messages, `PLAN.md`, and `TODOS.md`.
Run `git diff origin/$_BASE --stat` and compare files changed vs. stated intent.

Output:

```text
Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
Intent: <1-line summary>
Delivered: <1-line summary>
[If drift: each out-of-scope change]
[If missing: each unaddressed requirement]
```

This is informational only.

### Step 2 - Get the diff

```bash
git fetch origin $_BASE --quiet
git diff origin/$_BASE
```

If diff is over 500 lines: ask the user which areas to focus on first.

### Step 3 - Critical pass (core review)

Apply against the full diff.

SQL and data safety:
- string interpolation in SQL
- user-controlled input in WHERE/ORDER BY without parameterization
- missing DB transactions on multi-step writes
- unbounded queries
- locking migrations
- non-reversible migrations

Race conditions and concurrency:
- check-then-act without atomic locking
- `find_or_create_by` without uniqueness constraints
- shared mutable state
- `await` inside loops where `Promise.all` is possible
- missing locks

Auth and trust boundaries:
- new routes missing auth middleware
- authorization defaulting to allow
- direct object reference
- token validation without expiration
- untrusted input without validation

Error handling:
- promises without `.catch()` or `try/catch`
- catch-all handlers
- swallowed errors
- external API calls without timeout
- missing null/undefined guards

Completeness gaps:
- new enum/status values not handled everywhere
- new API response fields not handled in consumers
- new code paths with no tests

### Confidence calibration

Every finding must include a confidence score.

| Score | Meaning | Action |
|-------|---------|--------|
| 9-10 | Verified by reading specific code | Show normally |
| 7-8 | High-confidence pattern match | Show normally |
| 5-6 | Moderate | Show with caveat |
| 3-4 | Low confidence | Appendix only |
| 1-2 | Speculation | Only report if P0 |

Finding format:

```text
[P0/P1/P2] (confidence: N/10) file:line - description
```

### Step 4 - Specialist dispatch

Always dispatch when `DIFF_LINES >= 50`:
1. Testing specialist
2. Maintainability specialist

Conditional:
3. Security specialist if `SCOPE_AUTH=true` or backend diff > 100 lines
4. Performance specialist if backend or frontend scope exists
5. Data migration specialist if migration scope exists
6. API contract specialist if API scope exists

If `DIFF_LINES < 50`: skip specialists and print `Small diff ($DIFF_LINES lines) - specialists skipped.`

Dispatch selected specialists in parallel via Agent. Each specialist gets:
- the relevant checklist
- stack context
- JSON-lines output format
- `NO FINDINGS` when clean

Deduplicate by `path:line:category`, keep highest confidence, apply gates, compute:

```text
quality_score = max(0, 10 - (critical_count * 2 + informational_count * 0.5))
```

Testing specialist checklist:

```text
Missing negative-path tests
Missing edge-case coverage
Test isolation violations
Flaky test patterns
New public functions with zero coverage
Changed methods where tests only cover old behavior
```

Security specialist checklist:

```text
Missing input validation at trust boundaries
Auth/authz checks defaulting to allow
Direct object reference
Role escalation
Weak hashing
Non-constant-time comparison on secrets
Secrets in source code
XSS escape hatches with user data
Command injection
SSRF
Path traversal
```

Performance specialist checklist:

```text
N+1 queries
Missing DB indexes
O(n^2) patterns
Linear search inside maps
String concatenation in loops
Heavy new production dependencies
Barrel imports
Fetch waterfalls
Unbounded list endpoints
Synchronous I/O inside async handlers
```

Data migration specialist checklist:

```text
Non-reversible migrations
Table-locking ALTER TABLE
Missing indexes on new foreign keys
Data backfill in migration
Migration assumes specific data state
Old schema removed before old code is gone
```

API contract specialist checklist:

```text
Response shape changed without version bump
Required/optional contract drift
New required request field without default
Error response shape changed
Pagination contract changed
Auth requirement changed on existing endpoint
```

Adversarial subagent (always runs):

```text
You are an adversarial reviewer. Read the diff with `git diff origin/<BASE>`.

Think like an attacker and a chaos engineer. Find ways this code will fail in
production - not style issues, not missing tests, actual breakage or security holes.

Look specifically for:
- race conditions
- auth bypasses
- silent data corruption
- resource leaks
- swallowed failures
- trust boundary violations

For each finding: describe the exact failure scenario and classify as
FIXABLE or INVESTIGATE.
```

### Step 5 - Fix-first

Output summary header:

```text
Pre-Landing Review: N issues (X critical, Y informational) - PR Quality: N/10
```

Classify findings as AUTO-FIX or ASK.

AUTO-FIX examples:
- missing `.catch()`
- missing null guard where nullability is demonstrated
- missing `LIMIT` on an unbounded query
- obvious typo in an error message

ASK examples:
- auth checks
- race-condition fixes
- API contract changes
- anything touching payments, sessions, or sensitive data

For AUTO-FIX items:
- apply each fix
- commit with `git commit -m "fix: [description] (stacksmith-review code)"`
- report `[AUTO-FIXED] file:line - problem - what was done`

For ASK items: batch them into one AskUserQuestion with recommended fixes.

### Step 6 - Documentation staleness check

```bash
for doc in README.md ARCHITECTURE.md CONTRIBUTING.md CLAUDE.md; do
  [ -f "$doc" ] && echo "DOC: $doc" || true
done
```

For each doc found: if the diff changes behavior described there and the doc was not updated, flag it as informational and suggest `/stacksmith-release docs`.

### Final output format

```text
## Code Review [branch] [date]
Scope Check: [CLEAN / DRIFT / MISSING]
Diff: N lines (+N/-N across N files)
Specialists: [list dispatched]
PR Quality Score: N/10

### AUTO-FIXED (N issues)
- file:line - description - what was done

### NEEDS DECISION (N issues)
[batched AskUserQuestion]

### INFORMATIONAL NOTES
- file:line - observation

### Looks good
- [things done well]

### Adversarial review
[Findings or "No additional issues found"]
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-review\",\"mode\":\"code-review\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `design`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
git diff origin/$_BASE --name-only 2>/dev/null | grep -iE '\.(tsx?|jsx?|vue|svelte|css|scss|html)$'
[ -f DESIGN.md ] && echo "DESIGN_SPEC: DESIGN.md" || echo "DESIGN_SPEC: none"
```

If `DESIGN_SPEC` exists: read it and use it as the review standard.

### Step 1 - Read the code before auditing

For each changed frontend file, read it fully, not just the diff. Understand:
- component structure and hierarchy
- states rendered
- user interactions handled
- page context

### Step 2 - Audit (10 dimensions)

Rate each from 0 to 10. For low scores, write one concrete code-level fix.

| Dimension | Score | Finding | Fix |
|-----------|-------|---------|-----|
| Hierarchy | ? | [what's wrong] | [specific code change] |
| Whitespace | ? | | |
| Typography | ? | | |
| Color | ? | | |
| Consistency | ? | | |
| Copy | ? | | |
| Empty states | ? | | |
| Error states | ? | | |
| Motion | ? | | |
| Mobile | ? | | |

### AI slop scan

Flag any present:

| Slop pattern | Present? | Location |
|-------------|----------|----------|
| Generic action labels | ? | |
| Empty state boilerplate | ? | |
| Error boilerplate | ? | |
| Non-grid spacing | ? | |
| 3+ nested card levels | ? | |
| `dangerouslySetInnerHTML` or `.html_safe` with user content | ? | |
| No hierarchy | ? | |
| Spinner-only loading states | ? | |
| 7+ column tables all shown by default | ? | |
| Disabled buttons with no visual communication | ? | |

### Step 3 - Interact for judgment calls

For fixes that change user-facing copy or significantly alter layout, ask one AskUserQuestion before changing:

```text
[Re-ground: which component, which screen]

[Problem in plain English]

RECOMMENDATION: A because [one-line reason]

A) [Specific change]
B) [Alternative]
C) Leave as-is
```

One question at a time.

### Step 4 - Fix (atomic commits per dimension)

For each issue:
1. Make the fix
2. Commit atomically:

```bash
git commit -m "design: [dimension] - [specific change]"
```

One commit per dimension. Do not bundle changes.

### Step 5 - Report

```text
## Design Review [component/page] [date]

### Scope
Files reviewed: [list]
Changed frontend files: [list]

### Dimension scores
| Dimension | Before | After |
[table]

### AI slop resolved
| Pattern | Where | Fix |
[table]

### Commits
[list of commits]

### Remaining
- [issue] - needs: [what]
```

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-review\",\"mode\":\"design-review\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```

---

## Mode: `security`

### Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
_BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||')
_BASE="${_BASE:-main}"
echo "BRANCH: $_BRANCH"
git diff origin/$_BASE --name-only 2>/dev/null | head -30
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(auth|login|session|token|password|permission|role|access|oauth|jwt)' && echo "SCOPE_AUTH=true" || echo "SCOPE_AUTH=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(payment|billing|stripe|charge|invoice|subscription)' && echo "SCOPE_PAYMENT=true" || echo "SCOPE_PAYMENT=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(upload|file|attachment|media|s3|blob|storage)' && echo "SCOPE_UPLOAD=true" || echo "SCOPE_UPLOAD=false"
git diff origin/$_BASE --name-only 2>/dev/null | grep -qiE '(api|routes|endpoints|webhook|controller|handler)' && echo "SCOPE_API=true" || echo "SCOPE_API=false"
[ -f Gemfile ] && echo "STACK:ruby"
[ -f package.json ] && echo "STACK:node"
( [ -f requirements.txt ] || [ -f pyproject.toml ] ) && echo "STACK:python"
[ -f go.mod ] && echo "STACK:go"
```

### Zero-noise policy

Report a finding only if all three are true:
1. Confidence >= 8/10
2. Concrete exploit scenario
3. Independently verified at exact file:line

Confidence calibration:
- 10: confirmed vulnerability
- 9: very high
- 8: high
- 6-7: appendix only
- 0-5: do not report

### Step 1 - Automated quick scan

```bash
grep -rEn "(api_key|api_secret|secret_key|password|passwd|private_key|access_token)\s*[:=]\s*['\"][^'\"]{8,}" \
  --include="*.rb" --include="*.py" --include="*.ts" --include="*.js" --include="*.go" \
  --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=vendor . 2>/dev/null | \
  grep -iv "example\|placeholder\|your_\|<.*>\|ENV\[" | head -20

grep -rEn "\".*\+.*params\|'.*\+.*params\|query.*\+.*user\|sql.*\+.*input\|execute.*\+" \
  --include="*.rb" --include="*.py" --include="*.ts" --include="*.js" . 2>/dev/null | \
  grep -v node_modules | head -10

npm audit --json 2>/dev/null | python3 -c "
import sys,json
try:
  d=json.load(sys.stdin)
  v=d.get('vulnerabilities',{})
  crit=[k for k,v2 in v.items() if v2.get('severity')=='critical']
  high=[k for k,v2 in v.items() if v2.get('severity')=='high']
  print(f'npm audit: {len(crit)} critical, {len(high)} high')
  for c in crit[:5]: print(f'  CRITICAL: {c}')
except: pass
" 2>/dev/null || true

pip-audit -q 2>/dev/null | head -10 || true

grep -rEn "dangerouslySetInnerHTML|\.html_safe|raw\(|v-html|innerHTML\s*=" \
  --include="*.tsx" --include="*.jsx" --include="*.rb" --include="*.vue" --include="*.ts" \
  --exclude-dir=node_modules . 2>/dev/null | head -10
```

### Step 2 - OWASP Top 10

Check relevant changed files and only report findings that pass the zero-noise test.

- A01 Broken Access Control
- A02 Cryptographic Failures
- A03 Injection
- A04 Insecure Design
- A05 Security Misconfiguration
- A06 Vulnerable Components
- A07 Authentication Failures
- A08 Software Integrity
- A09 Security Logging
- A10 SSRF

For each, inspect the actual code paths and document checked-clean areas too.

### Step 3 - STRIDE threat model

For each major new component:

| Threat | Question | Finding (if any) |
|--------|----------|------------------|
| Spoofing | Can an attacker impersonate a user, service, or system? | |
| Tampering | Can data be modified in transit or at rest without detection? | |
| Repudiation | Can users deny actions they took? | |
| Information Disclosure | Can sensitive data leak? | |
| Denial of Service | Can the feature be abused to degrade the service? | |
| Elevation of Privilege | Can a user gain more access than intended? | |

### Step 4 - Scoped deep dives

If `SCOPE_AUTH=true`:
- trace every auth decision
- verify deny-on-failure
- look for bypass paths

If `SCOPE_PAYMENT=true`:
- verify webhook signatures
- validate amount server-side
- require idempotency

If `SCOPE_UPLOAD=true`:
- validate file type by content
- enforce size limits
- ensure safe serving
- ensure no path traversal

### Step 5 - Report

```text
## Security Audit [date] [branch]

### Summary
Files reviewed: N
Scope: [AUTH / PAYMENT / UPLOAD / API]
Automated scans: npm audit [result], secrets scan [N hits / clean]

### Critical (fix before ship)
[finding blocks]

### High (fix this sprint)
[finding blocks]

### Low (track, not blocking)
[finding blocks]

### Checked, no issues found
- [A01] Access Control: [specific check description]
- [A03] Injection: [what was checked]
[list every checked category]

### Appendix - medium confidence
[findings with confidence 6-7]
```

If there are no critical or high findings: "Audit complete. No critical or high findings. [N low-priority items in appendix.]"

### Log

```bash
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"stacksmith-review\",\"mode\":\"security\",\"branch\":\"$(git branch --show-current 2>/dev/null || echo 'N/A')\",\"outcome\":\"success\",\"repo\":\"$(basename $(git rev-parse --show-toplevel 2>/dev/null) 2>/dev/null || echo 'N/A')\"}" >> ~/.mystack/timeline.jsonl
```
