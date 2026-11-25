---
name: ci-monitor
description: "Self-healing CI loop: checks CI on main and open PRs, spawns `mbe agent run` fixes, validates them via the Reviewer Agent Contract, auto-merges green fix PRs, files issues for the rest. Circuit breaker after 3 failed fix PRs. Invoke with /ci-monitor."
user-invocable: true
---

# CI Monitor

Monitor GitHub Actions CI health and respond to failures. Fixes simple issues automatically via a self-healing loop, escalates complex ones to the issue queue.

## Circuit Breaker State

Track consecutive fix-PR CI failures in a local counter. Reset to 0 on any successful fix.

```bash
CONSECUTIVE_FAILURES=0
MAX_CONSECUTIVE_FAILURES=3
```

If `CONSECUTIVE_FAILURES >= MAX_CONSECUTIVE_FAILURES`, **stop the loop** and report:

> "Circuit breaker tripped: 3 consecutive fix PRs failed CI. Manual review required."

Do not attempt further fixes in this session.

---

## Workflow

### Step 1: Check Main Branch CI

```bash
gh run list --branch main --limit 5 --json status,conclusion,databaseId,headBranch,name,createdAt
```

Examine the results:

- If all 5 runs have `conclusion: "success"` → **main is healthy**, proceed to Step 3
- If any run has `conclusion: "failure"` → proceed to Step 2

### Step 2: Diagnose and Self-Heal Failure

For each failed run:

```bash
gh run view <databaseId> --log-failed 2>&1 | head -200
```

#### 2a: Check for Existing Fix

```bash
gh issue list --label "ci-fix" --state open --search "<error keyword>" --json number,title
gh pr list --state open --label "ci-fix" --json number,title,headRefName
```

If an open `ci-fix` issue **or** an open fix PR already exists for this failure, **skip it** — it is already being tracked.

#### 2b: Classify the Failure

**Classify into one of these types:**

| Type         | Signal in logs                                                       |
| ------------ | -------------------------------------------------------------------- |
| `lint`       | `eslint`, `prettier`, `react/no-unescaped-entities`, unused variable |
| `typecheck`  | `tsc`, `TS`, `Type error`, missing import, wrong type                |
| `build`      | `turbo`, `vite`, `esbuild`, broken dependency chain, missing export  |
| `test`       | `vitest`, snapshot mismatch, assertion failure, mock drift           |
| `drift`      | `registry.json`, `dependency-graph`, generated artifact out of sync  |
| `migration`  | Prisma schema, SQL syntax error, migration ordering                  |
| `infra`      | Docker, database connectivity, network, timeout                      |
| `dependency` | `pnpm`, lockfile conflict, version mismatch                          |

**Fixable failures** (spawn self-healing agent):

- `lint` — ESLint/Prettier errors
- `typecheck` — Type errors, missing imports, wrong types
- `drift` — Stale generated artifacts (`pnpm regen`)
- `test` — Snapshot mismatches, assertion failures from recent changes where the fix is localized
- `build` — Missing export, broken import, stale generated file (single-package scope)

**Escalatable failures** (file issue instead):

- `infra` — Docker, database connectivity, network timeouts — not code-fixable
- `dependency` — Conflicting peer deps, major version incompatibilities
- `migration` — Schema drift, ordering issues, SQL syntax errors requiring human review
- `test` where the failure is flaky (no recent code change in the failing area)
- `build` requiring multi-package refactoring (>3 files across >1 package)
- Any failure that has already had 2+ fix attempts this session

**Human-judgment failures** (always escalate, never auto-fix):

- Architectural violations (ADR compliance failures)
- Security-related failures
- CI workflow file problems (`.github/workflows/`)
- Authentication or credential failures

#### 2c: Self-Heal Fixable Failures

**Check circuit breaker first:**

```bash
if [ "$CONSECUTIVE_FAILURES" -ge "$MAX_CONSECUTIVE_FAILURES" ]; then
  echo "Circuit breaker tripped — stopping."
  exit 0
fi
```

Spawn a worktree agent with the full diagnosis context:

```bash
mbe agent run "Fix CI failure on main [type: <lint|typecheck|build|test|drift>]:

## Failure Summary
- Run ID: <databaseId>
- Job: <job name>
- Failure type: <classified type>
- Branch: main

## Error Log (key lines)
\`\`\`
<relevant error output, ≤30 lines>
\`\`\`

## Fix Instructions
1. pnpm bootstrap:worktree
2. Reproduce the failure locally: <relevant command>
3. Fix the root cause (do NOT skip or disable tests/lint)
4. Run gates: pnpm lint && pnpm typecheck && pnpm test (in affected package)
4b. Before pushing: pnpm build --filter @mbe/cli... && pnpm regen (stage regenerated artifacts by path)
5. Push branch, open PR with title: 'fix(ci): <brief description>'
6. Include 'Fixes CI run <run URL>' in the PR body

Security rules: never hardcode secrets, no SQL injection, no XSS. Never modify .github/workflows/." \
  --max-budget 0.75 --adapter auto
```

`--adapter auto` enables rate-limit failover: if Claude returns 429, the adapter cascade tries gemini then opencode before giving up. Opus-tier tasks (deep architecture analysis) should pin `--adapter claude` to stay on the Claude provider.

Note the PR number from agent output for Step 2d.

#### 2d: Validate the Fix (Reviewer Agent Contract)

After the agent opens a PR, wait for CI to complete:

```bash
gh pr checks <PR_NUMBER> --watch --fail-fast --interval 30
node scripts/ci-gate-status.mjs check --pr <PR_NUMBER>
```

`--watch` only waits: it reports `fail=0 pend=0` both when CI is green and when CI never ran (#3969). The decision comes from the classifier's `state`, handled per `.claude/implement-queue.md` § ci-status (`gate-missing` → dispatch and re-poll; `gate-unattributed`/`unknown` → abstain).

**If `state` is `failed`:**

```bash
CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
```

If `CONSECUTIVE_FAILURES >= MAX_CONSECUTIVE_FAILURES`: stop and report the circuit breaker trip. Otherwise continue.

**If `state` is `green`** (only then), run a Reviewer sub-agent to validate the fix before auto-merging:

```bash
# Gather review inputs
DIFF=$(gh pr diff <PR_NUMBER>)
CHANGED_FILES=$(gh pr diff <PR_NUMBER> --name-only)
PR_TITLE=$(gh pr view <PR_NUMBER> --json title --jq .title)
```

Dispatch the Reviewer (per the [Reviewer Contract](../../../docs/agents/reviewer-contract.md)):

- `subagent_type: "reviewer"`, `isolation: "none"`, model: `haiku`, budget: `$0.05`
- Include: the full Reviewer Contract, the diff, changed files, task description (`"Fix CI failure: <type> on main"`)
- Acceptance criteria: `["CI passes on fix PR", "No tests skipped or disabled", "Root cause addressed, not symptom masked"]`

**On Reviewer `"pass"` (score ≥ 7):**

```bash
gh pr merge <PR_NUMBER> --squash --delete-branch
CONSECUTIVE_FAILURES=0  # reset on successful fix
```

**On Reviewer `"flag"` (score < 7):**

```bash
CONSECUTIVE_FAILURES=$((CONSECUTIVE_FAILURES + 1))
```

Comment on the PR with the Reviewer's verdict and issues, then escalate to issue filing (Step 2e).

**On Reviewer timeout/error:** log warning, proceed to merge (fail-open).

#### 2e: Escalate Complex or Unfixable Failures

For failures classified as escalatable or when self-healing fails:

```bash
gh issue create \
  --title "[CI] <failure-type>: <brief description>" \
  --label "ci-fix" --label "ready" \
  --body "## CI Failure

**Workflow**: <workflow name>
**Run**: <run URL>
**Branch**: main
**Failure type**: <lint|typecheck|build|test|drift|migration|infra|dependency>

## Error Log

\`\`\`
<relevant error output, truncated to key lines>
\`\`\`

## Analysis

<brief analysis of what went wrong and potential fix approaches>

## Why not auto-fixed

<reason: flaky, multi-package refactor, infrastructure issue, etc.>

---
*Created by automated CI monitor on $(date +%Y-%m-%d)*"
```

### Step 3: Check Open PR Health

```bash
gh pr list --state open --json number,title,headRefName --limit 10
```

For each open PR:

1. Focus on PRs created by the agent (branch names starting with `agent/`)
2. Classify its CI state; never decide "failing" from a rollup or a `--jq` filter:

```bash
node scripts/ci-gate-status.mjs check --pr <NUMBER>
```

Only `state: "failed"` counts as failing. `pending` is still running, and `gate-missing` is CI that never ran (dispatch and re-poll); both need different handling than a fix, per `.claude/implement-queue.md` § ci-status.

If an agent-created PR has `state: "failed"`:

**Check circuit breaker:**

```bash
if [ "$CONSECUTIVE_FAILURES" -ge "$MAX_CONSECUTIVE_FAILURES" ]; then
  echo "Circuit breaker tripped — filing issue instead of retrying."
  # Escalate to Step 2e instead
fi
```

If not tripped, attempt one fix:

```bash
# Get the failure details: the classifier's `reason` names what failed; read job logs via `gh run view --log-failed`
node scripts/ci-gate-status.mjs check --pr <NUMBER>

# Spawn fix agent for the PR
mbe agent run "Fix failing CI checks on PR #<NUMBER> [type: <classified type>]:

## Failure Details
- PR: #<NUMBER>
- Failing checks: <check names>

## Error Log
\`\`\`
<check failure logs>
\`\`\`

Fix the root cause, run pnpm lint && pnpm typecheck && pnpm test on affected packages, then push the fix to the same branch." \
  --max-budget 0.50 --adapter auto
```

`--adapter auto` enables rate-limit failover (claude → gemini → opencode on 429). These PR fix runs are haiku/sonnet-tier — opus-tier tasks should pin `--adapter claude`.

Track result as before. On fix-PR CI failure, increment `CONSECUTIVE_FAILURES`.

### Step 4: Report Status

Provide a brief summary of actions taken:

- Failures found and their types
- Fixes attempted (with PR numbers)
- Reviewer verdicts (pass/flag, scores)
- Issues filed
- Circuit breaker state (current count / 3)

If everything is green: "CI is healthy. All recent runs passing, no PR check failures."

---

## CI Workflow Reference

The CI pipeline (`.github/workflows/ci.yml`) has these jobs:

| Job                  | What It Checks                                               | Failure Type    |
| -------------------- | ------------------------------------------------------------ | --------------- |
| `lint`               | ESLint across all packages                                   | `lint`          |
| `typecheck`          | TypeScript compilation, Prisma client generation             | `typecheck`     |
| `architecture-audit` | ADR compliance and dependency checks via `@mbe/cli`          | escalate        |
| `build`              | Full monorepo build, registry.json validation, catalog drift | `build`/`drift` |
| `test`               | Vitest test suite with coverage                              | `test`          |
| `migrations`         | Prisma migrations against test PostgreSQL database           | `migration`     |

Common failure patterns:

- **lint**: Usually a missing `import type`, unused variable, or formatting issue
- **typecheck**: Type errors, missing imports, wrong types
- **architecture-audit**: ADR violations or forbidden dependency patterns — **always escalate**
- **build**: Often a missing export, broken dependency chain, or stale generated file
- **test**: Snapshot mismatches, assertion failures from behavior changes, mock drift
- **migrations**: Schema drift, migration ordering issues, SQL syntax errors
- **drift**: Regenerated artifacts out of sync — fix with `pnpm regen`

## Safety Rules

- **Never retry a run** — diagnose and fix the root cause instead
- **Budget cap** — $0.75 per main-branch fix, $0.50 per PR fix
- **Never modify CI workflow files** — if the workflow itself is broken, create an issue
- **Never skip or disable tests** — fix the test or the code, not the test runner config
- **Circuit breaker** — stop after 3 consecutive fix-PR CI failures; never let the loop spin on a systematic problem
- **Reviewer gate** — every auto-merged fix PR must pass the Reviewer Agent Contract (score ≥ 7) before merge
- **Escalate security/arch** — never auto-fix ADR violations, security failures, or workflow file issues
