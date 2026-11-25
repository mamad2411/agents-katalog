---
name: self-audit
description: >
  Meta-gate that audits the current session's own actions before any commit — philosophy, scope, convention, and token-budget violations. Read-only on session state; emits a single inline table verdict. Use as the final step of any multi-edit / multi-cycle task.
  Triggers: "self-audit", "audit yourself", "self-check", "셀프 점검", "셀프 감사", "내 행동 점검", "before commit"
version: 0.1.0
ssl:
  scheduling:
    anti_triggers:
      - "SSL audit of a SKILL.md target — use galmuri:skill-audit"
      - "Completion-claim gate on code/UI — use galmuri:polish"
      - "Test-gap / coverage inspection — use galmuri:ralphi"
      - "Decision forcing — use harnish:forki"
  structural:
    scenes: [Survey, Check, Verdict, Halt-or-Pass]
    resumable: false
    branches:
      - "0 violations → 'self-audit clean, proceed to commit'"
      - "1+ violations → halt, list violations + propose fixes, wait for user 'go'"
      - "report length > 1500 tokens → write to tmp/self-audit-<ts>.md and link"
  logical:
    tools: [Bash, Read]
    side_effects:
      reads: ["git diff (current session changes)", "git status", "current branch name"]
      writes:
        - "tmp/self-audit-<ts>.md when the inline report would exceed 1500 tokens"
      deletes: []
      network: []
    idempotent: true
    rollback: null
---

# galmuri:self-audit — session action gate

> "검증 없이 완료 선언하지 않는다." A pre-commit meta-gate. Audits **Claude's own actions in the current session**, not external code.

## When to run

- Before any commit on a feature branch
- After any multi-cycle task (`polish` / `ralphi` / `audit` loop) completes
- When the user says "audit yourself" / "self-check" / "셀프 점검"
- Automatically as the final step of any multi-edit task

If invoked bare on a quiet diff, ask: *"Anything in this session you want me to scrutinise specifically? e.g. a scope decision you weren't sure about, a refactor you want double-checked."*

## Step 1: Survey

Collect the audit surface for this session:

```bash
git status --short
git diff --stat
git branch --show-current
git log -1 --pretty=%H            # baseline SHA for comparisons
```

Do **not** read full file contents — only the diff and stat. The point is to check *what changed in this session*, not to review the whole codebase.

## Step 2: Check (4 axes)

### 2-A. Philosophy violations (highest severity)

| Check | Pattern (rg over `git diff`) |
|---|---|
| ROP — no `withTimeout` or defensive `{timeout: N}` introduced | `rg -nP 'withTimeout\|timeout:\s*\d+'` |
| ROP — no silent try/catch wrappers added | `rg -nP 'catch\s*\([^)]*\)\s*\{[^}]*$'` |
| SSOT — no hardcoded version-specific field names | `rg -nP 'v\d+\.\w+\|schema_v\d'` |
| "compress" preserved structure (no H2 / step removal) | manual diff inspection |
| Locale separation — en / ko / jp content in correct file | `rg -l '[가-힣]' diff` filtered by `.md$` (not `.ko.md`/`.jp.md`) |

### 2-B. Scope violations

- Did I act on an ambiguous affirmative ("예", "ok", "그래") *while* a pending follow-up question was open?
- Did I invent tooling, helpers, or abstractions not asked for?
- Did I delete or modify at scale (>5 files) without proposing the candidate set first?

### 2-C. Convention violations

- `testid` constants are UPPER_SNAKE_CASE — `rg 'data-testid="[a-z]'` over diff
- No raw `px` / hex values outside design-token files
- No deep imports bypassing a public API surface

### 2-D. Token-efficiency violations

- Did I output > 30 lines of report content directly to chat (should be a file under `docs/reports/` or `tmp/`)?
- Did I quote entire functions or files in verifier output?
- Did I batch multiple cycles into a single commit?
- Did I retry a failing command in a `sleep` loop instead of diagnosing the root cause?

## Step 3: Verdict (inline table)

Output exactly this table — one row per check, ✓ or ✗ only. Evidence is a path / line / rg pattern, never a quoted block.

```
| Check                                              | Status | Evidence                       | Fix                            |
|----------------------------------------------------|--------|--------------------------------|--------------------------------|
| ROP — no withTimeout / defensive timeout           | ✓/✗    | file:line                      | revert + use Result type       |
| ROP — no silent try/catch                          | ✓/✗    | file:line                      | rethrow or convert to Result   |
| SSOT — no hardcoded version field names            | ✓/✗    | file:line                      | parse-don't-validate           |
| Compress preserved structure                       | ✓/✗    | section diff stat              | restore deleted section        |
| Locale separation respected                        | ✓/✗    | file:line                      | move content to correct file   |
| Scope confirmed before ambiguous affirmative       | ✓/✗    | conversation turn              | revert action, re-confirm      |
| No invented tooling                                | ✓/✗    | file path                      | remove invented helper         |
| Bulk modify proposed before applying              | ✓/✗    | files changed count            | revert + propose list          |
| testid UPPER_SNAKE_CASE                            | ✓/✗    | file:line                      | rename constant                |
| No raw px / hex outside tokens                     | ✓/✗    | file:line                      | use design token               |
| No deep imports bypassing public API               | ✓/✗    | file:line                      | use public re-export           |
| Chat output ≤ 30 lines                             | ✓/✗    | last report length             | move to docs/reports/          |
| No entire-file quoting in verifier output          | ✓/✗    | output line range              | summarize + link               |
| One cycle = one commit                             | ✓/✗    | `git log` last N commits       | split commit                   |
| No sleep-loop retry of failing command             | ✓/✗    | shell history                  | diagnose root cause            |
```

## Step 4: Halt-or-Pass

- **0 violations** → emit one line: `self-audit clean, proceed to commit.`
- **1+ violations** → halt. List violations + propose fixes. Wait for explicit "go" / "proceed" / "이대로 가" before any further action.

## Token budget

- Inline table ≤ 1500 tokens. If the diff is too large for an inline pass, write the report to `tmp/self-audit-<ts>.md` and emit only a one-line summary + path to chat.

## What this skill does NOT do

- ✗ Modify any session file
- ✗ Audit other repos / other sessions
- ✗ SSL-decompose a SKILL.md (that is `galmuri:skill-audit`)
- ✗ Replace `galmuri:polish` (which gates UI/code-completion claims) or `galmuri:ralphi` (which budgets quality loops)
