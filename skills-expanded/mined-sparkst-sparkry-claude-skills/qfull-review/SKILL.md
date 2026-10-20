---
name: QFULL-REVIEW
version: 1.0.0
description: Comprehensive multi-agent code review with automated fix loops. Use whenever the user wants a thorough review before merging — "review everything", "full review", "review my changes", "is this ready to merge", or /qfull-review. Handles PR creation, 3-5 parallel review agents, iterative P0-P2 fixing (up to 4 cycles), test validation, then /code-review and /simplify as final polish.
trigger: QFULL-REVIEW
---

# Full Review Pipeline

A comprehensive review skill that takes current work through PR creation, multi-agent parallel
review, iterative fix cycles, and final polish. Designed to catch everything — bugs, security
issues, edge cases, missing requirements, failure scenarios — before code ships.

## When This Runs

The user has finished a chunk of work and wants it thoroughly reviewed and cleaned up before
merging. They may or may not have created a PR yet.

## Pipeline Overview

```
Phase 1: PR Setup          → Ensure changes are in a PR (create if needed)
Phase 2: Parallel Review   → 3-5 agents review in parallel
Phase 3: Fix Loop          → Fix P0-P2 findings, re-review (up to 4 cycles)
Phase 4: Final Polish      → Run /code-review:code-review then /simplify
```

## Phase 1: PR Setup

Determine the current state of the work:

1. Run `git status` and `git diff --stat HEAD` to understand what's changed
2. Check if a PR already exists for the current branch:
   ```bash
   gh pr list --head $(git rev-parse --abbrev-ref HEAD) --state open --json number,url
   ```
3. **If no PR exists:**
   - Stage all relevant changes (not .env, credentials, or build artifacts)
   - Create a commit with a descriptive message summarizing the work
   - Push to remote
   - Create a PR targeting the appropriate base branch (usually `staging` per CLAUDE.md git rules)
   - Use the PR body format from the system prompt (Summary + Test plan)
4. **If PR exists:** Note the PR number and URL, proceed to Phase 2

Output: PR URL for reference throughout the review.

## Phase 2: Parallel Review

### Size the review team

Count the lines changed:
```bash
git diff $(gh pr view --json baseRefName --jq .baseRefName)...HEAD --stat | tail -1
```

| Lines Changed | Agents | Coverage |
|---|---|---|
| < 100 | 3 | Bug scan, Security, Edge cases |
| 100–500 | 4 | + Requirements compliance |
| 500+ | 5 | + Code quality / usability |

### Launch review agents

Launch ALL agents in a single message (parallel, not sequential). Each agent gets the same
context briefing plus its specific focus area.

**Context briefing (include in every agent prompt):**
- The PR URL and what it does (1-2 sentence summary)
- The list of changed files
- The base branch
- Path to CLAUDE.md for project conventions
- Instruction: "Read each changed file. Return findings as a prioritized list with P0/P1/P2 severity, file path, line numbers, and a concrete description of the issue."

**Agent 1 — Bug & Logic Scan:**
Focus on runtime failures, incorrect logic, broken control flow, data loss scenarios,
type mismatches, and off-by-one errors. Read only the changed files — shallow scan for
obvious bugs. Ignore style and things a linter would catch.

**Agent 2 — Security Review:**
Focus on injection vectors (shell, SQL, XSS, template), auth/authz gaps, secret exposure,
TOCTOU races, unsafe deserialization, path traversal, and dependency risks.
Check GitHub Actions workflows for command injection via untrusted inputs.

**Agent 3 — Edge Cases & Failure Scenarios:**
Focus on error handling gaps, race conditions, timeout behavior, empty/null inputs,
concurrent access, network failures, partial failures, and retry logic.
Think about what happens when things go wrong, not just the happy path.

**Agent 4 — Requirements & Convention Compliance** (100+ line changes):
Read CLAUDE.md and check all changes against it. Verify git branch rules, testing
requirements, documentation organization, and quality gate compliance. Check that
no MUST rules are violated.

**Agent 5 — Code Quality & Usability** (500+ line changes):
Focus on API ergonomics, error messages, configuration complexity, documentation gaps,
naming clarity, and whether the code is understandable to someone seeing it for the first
time. Also check for dead code, unused variables, and unnecessary complexity.

### Severity Definitions

Give these to every agent:

- **P0 — Blocks ship.** Will cause runtime failure, data loss, security vulnerability,
  or violates a MUST rule. Must be fixed before merge.
- **P1 — Should fix.** Likely bug, poor error handling that will bite someone, missing
  validation at a system boundary, or significant maintainability concern. Fix before merge
  unless there's a strong reason not to.
- **P2 — Fix while here.** Real issue but lower impact — stale comments, minor inefficiency,
  cosmetic inconsistency, or a pattern that's not ideal but works. Fix because we're already
  touching this code.

## Phase 3: Fix Loop

After all review agents return:

1. **Aggregate findings** — Deduplicate across agents (same file + same issue = one finding).
   Keep the highest severity if agents disagree.

2. **Score each finding** — For any finding that might be a false positive, launch a Haiku
   agent to verify. Drop findings scored below 50 confidence. Use the scoring rubric:
   - 0: False positive, doesn't stand up to scrutiny
   - 25: Might be real, but couldn't verify
   - 50: Real but minor / unlikely in practice
   - 75: Verified real issue, will be hit in practice
   - 100: Confirmed, will happen frequently

3. **Fix all P0-P2 findings using worktree agents.** Group findings by file or logical
   area so agents don't conflict, then launch fix agents in parallel — each in its own
   git worktree for isolation.

   For each fix agent, use `isolation: "worktree"` when spawning via the Agent tool:
   ```
   Agent(
     prompt: "Fix these findings: [list]. Read each file, make the minimal change...",
     isolation: "worktree"
   )
   ```

   Each worktree agent gets a clean copy of the repo and can edit freely without
   conflicting with other agents. The agent result will include the worktree path
   and branch name if changes were made.

   **Grouping strategy** — avoid merge conflicts by ensuring no two agents touch the
   same file:
   - Group findings by file path. All findings in `scripts/watch-deployment.sh` go to
     one agent; all findings in `.github/workflows/` go to another.
   - If a single file has 5+ findings, give them all to one agent.
   - If findings span many files but are logically related (e.g., "rename X everywhere"),
     give them to one agent.

4. **Merge worktrees back** — After all fix agents complete:
   ```bash
   # For each worktree that made changes:
   git merge <worktree-branch> --no-edit
   ```
   If a merge conflict occurs (rare given the grouping strategy), resolve it manually —
   read both sides, pick the correct version, and continue.

   After all merges, clean up the worktree branches:
   ```bash
   git branch -d <worktree-branch>
   ```

5. **Run tests** — After merging all fixes, run the project's test suite to catch regressions:
   ```bash
   pnpm validate   # typecheck + lint + unit tests
   ```
   Also run any co-located spec files for modified code (`*.spec.ts` next to changed files).
   If Playwright e2e tests exist for the affected area, run those too:
   ```bash
   npx playwright test tests/e2e/smoke/   # smoke suite
   ```
   If any tests fail, fix them before proceeding. A fix that breaks tests is not a fix.

6. **Re-review** — After fixing, launch a fresh round of review agents (same team size)
   focused on the files that were modified during fixes. This catches regressions and
   issues introduced by the fixes themselves.

7. **Repeat** up to 4 total review cycles. Stop early if:
   - A cycle returns zero findings above the confidence threshold
   - A cycle returns only P2 findings (fix them, then stop — no need to re-review P2 fixes)

8. **If still finding P0/P1 after 4 cycles**, report the remaining findings to the user
   with full context and ask for guidance.

### Fix Loop State Tracking

Track progress across cycles:
```
Cycle 1: X findings (Y P0, Z P1, W P2) → fixed N
Cycle 2: X findings (Y P0, Z P1, W P2) → fixed N
...
```

Report this summary after each cycle so the user can see convergence.

## Phase 4: Final Polish

After the fix loop completes:

1. **Run /code-review:code-review** — This provides the formal code review with strict
   confidence scoring (80+ threshold). It catches anything the fix loop may have introduced
   and provides the final seal of approval.

2. **Run /simplify** — This runs the three parallel review agents (reuse, quality, efficiency)
   and applies cleanup fixes. This is the last pass before the code ships.

3. **Report** — Summarize what was done:
   - Total findings across all cycles
   - What was fixed
   - Final state (clean, or remaining items with explanation)
   - PR URL

## Important Guidelines

- **Do not skip phases.** Even if the code "looks fine," run the full pipeline. The point
  of this skill is thoroughness.
- **Parallel, not sequential.** Always launch review agents in a single message. The whole
  point of multi-agent review is speed through parallelism.
- **Fix, don't just report.** This is not a read-only review. The skill fixes everything
  it finds. Only escalate to the user when genuinely stuck after 4 cycles.
- **Respect CLAUDE.md.** All fixes must comply with project conventions. Read CLAUDE.md
  before making any changes.
- **Stay on the working branch.** Per git branch rules, work happens on `staging` or feature
  branches. Never push to `main`.
