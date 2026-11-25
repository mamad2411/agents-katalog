---
name: cli-review-fix
disable-model-invocation: true
description: "Send code review requests to external CLI tools (Codex CLI, Gemini CLI), critically evaluate findings, fix valid issues, and present a fix report. Auto-detects context (PR, branch, uncommitted changes). Uses bundled wrapper scripts for both Codex and Gemini. For Gemini, prefers the code-review extension (interactive mode with full-file access) when installed. Run /cli-review-fix to launch all available CLIs, or /cli-review-fix codex for a specific one."
---

# CLI Review & Fix

Dispatch code review requests to external CLI agents (Codex CLI, Gemini CLI),
critically evaluate their findings, fix valid issues, and present a consolidated
fix report. Runs CLIs in parallel when multiple are available. Single-pass — no
re-review loops.

## Invocation

| Invocation | Behavior |
|---|---|
| `/cli-review-fix` | Launch ALL available CLIs in parallel |
| `/cli-review-fix codex` | Codex CLI only |
| `/cli-review-fix gemini` | Gemini CLI only |

## Prerequisites

Check CLI availability before running. If a requested CLI is missing, show
install instructions and continue with any other available CLIs.

| CLI | Check | Auth |
|---|---|---|
| Codex | `command -v codex` | `OPENAI_API_KEY` env var |
| Gemini | `command -v gemini` | Google auth (run `gemini` once) |
| Gemini code-review ext (optional) | `~/.gemini/extensions/code-review/` exists | Included with Gemini auth |

The extension is optional but recommended — it lets Gemini read full files
during review, significantly reducing false positives. Install:
`gemini extensions install https://github.com/gemini-cli-extensions/code-review`

If neither CLI is available, inform the user and point to the install links:
- Codex CLI: https://github.com/openai/codex
- Gemini CLI: https://github.com/google-gemini/gemini-cli

## Scripts

The skill bundles small scripts for context detection and Codex invocation.
Prefer them over hand-written shell snippets so review behavior stays
predictable.

**Script path resolution:** Check in this order:
1. `.agents/skills/cli-review-fix/scripts/` — project-local install
2. `~/.claude/skills/cli-review-fix/scripts/` — global install for Claude Code
3. `skills/cli-review-fix/scripts/` — repo-local (when running from source)
4. Other global paths by preference of the agent

Use whichever path exists.

**Detect script:**
```bash
<resolved>/cli-review-detect.sh [full]
```

Pass `full` as argument when the user explicitly requests a full codebase review.

**Output:** JSON with fields:
- `codex`, `gemini` — boolean CLI availability
- `gemini_code_review_ext` — boolean, code-review extension installed
- `context` — `"pr"`, `"branch"`, `"uncommitted"`, `"full"`, or `"none"`
- `base` — base branch for diff (empty when not applicable)
- `current_branch`, `default_branch` — branch info
- `diff_lines` — diff size estimate (for large diff warnings)
- `pr_number`, `pr_url`, `pr_title` — PR metadata (empty when no PR)

The script also creates `.agents/scratch/` for output files.

**Codex runner:**
```bash
<resolved>/cli-review-codex.sh <pr|branch|uncommitted|full> [base]
```

Use it for every Codex review invocation. For diff-based contexts it builds a
strict stdin prompt from `references/codex-review-prompt.md`, appends the
actual diff, and runs `codex exec -`. This avoids the current Codex CLI
behavior where `exec review --base ...` cannot be paired with custom
instructions and tends to over-explore the repository. For explicit full
codebase reviews, the wrapper falls back to `codex exec review`.

If deeper debugging is needed, set `CLI_REVIEW_DEBUG_JSON=1` before running the
Codex wrapper. It will write JSONL events to
`.agents/scratch/codex-review.jsonl` and stderr to
`.agents/scratch/codex-review.stderr`.

**Gemini runner:**
```bash
<resolved>/cli-review-gemini.sh <pr|branch|uncommitted|full> [base]
```

Use it for every Gemini review invocation. For PR and branch contexts, the
wrapper prefers Google's code-review extension when installed — this runs Gemini
in interactive mode where it can read full files, significantly reducing false
positives. When the extension is not installed, or for uncommitted/full contexts,
the wrapper falls back to rich pipe mode: sends the review prompt + full contents
of changed files + the diff to `gemini --model pro -p - --sandbox`.

Stderr goes to `.agents/scratch/gemini-review.stderr`.

## Context Detection

The detect script implements this decision tree (priority order):

```
0. Detect default branch (git symbolic-ref or main/master fallback)

1. Full codebase?
   "full" argument passed to detect script
   → CONTEXT = "full"

2. PR?
   gh pr view --json number,baseRefName,url,title 2>/dev/null
   → success: CONTEXT = "pr", base = baseRefName

3. Branch diff?
   current branch ≠ DEFAULT_BRANCH, commits ahead
   → CONTEXT = "branch", base = DEFAULT_BRANCH

4. Uncommitted changes?
   git status --porcelain → non-empty
   → CONTEXT = "uncommitted"

5. Nothing to review
   → CONTEXT = "none"
```

## Execution Flow

### Phase 1: Review

1. **Detect** — run `cli-review-detect.sh` (or `cli-review-detect.sh full` if
   user requested full codebase review). Parse the JSON output.
2. **Validate** — check `codex`/`gemini` fields against requested CLIs. If a
   specific CLI was requested but unavailable, show install link and stop. If
   neither is available, show both install links and stop. If `context` is
   `"none"`, inform user and stop.
3. **Report context** — tell the user what was detected (e.g., "Detected PR #42,
   reviewing diff against main")
4. **Launch CLIs** — run selected CLIs. Prefer sub-agents for parallel execution
   (see Sub-Agent Recommendation). If sub-agents fail due to permissions, fall
   back to direct Bash calls with `run_in_background`. For Codex, call
   `cli-review-codex.sh` rather than assembling the command manually. Output
   goes to `.agents/scratch/codex-review.md` and/or
   `.agents/scratch/gemini-review.md`.
5. **Collect results** — read output from `.agents/scratch/`
6. **Present review findings** — format per `references/output-format.md` with
   severity levels and engine agreement tags

### Phase 2: Evaluate & Fix

9. **Critically evaluate** each finding (see Critical Evaluation below)
10. **Fix valid issues** — apply fixes for findings that pass evaluation
11. **Test** — run project tests if available (`npm test`, `pytest`, `make test`,
    etc.). If tests fail after a fix, revert that fix.
12. **Present fix report** — single report to the user (see Fix Report below)

## CLI Commands

Quick reference. See `references/cli-commands.md` for full flag details and
troubleshooting.

### Codex CLI

Use the wrapper script, not raw `codex exec review`, for diff-based reviews.
The wrapper keeps Codex focused on the diff and only uses built-in review for
explicit full codebase runs.

| Context | Command |
|---|---|
| PR | `cli-review-codex.sh pr <baseRefName>` |
| Branch | `cli-review-codex.sh branch <default-branch>` |
| Uncommitted | `cli-review-codex.sh uncommitted` |
| Full codebase | `cli-review-codex.sh full` |

### Gemini CLI

Use the wrapper script for Gemini reviews. For PR and branch contexts it prefers
the code-review extension (interactive mode with full-file access) when
installed. Falls back to rich pipe mode for other contexts or when the extension
is not available.

| Context | Command |
|---|---|
| PR | `cli-review-gemini.sh pr <baseRefName>` |
| Branch | `cli-review-gemini.sh branch <default-branch>` |
| Uncommitted | `cli-review-gemini.sh uncommitted` |
| Full codebase | `cli-review-gemini.sh full` |

## Critical Evaluation

**Never trust CLI review findings at face value.** Before fixing, evaluate EACH
finding:

1. **Verify the claim** — Read the actual code at the referenced file:line. Does
   the description match reality? CLI tools may misread context, reference wrong
   lines, or describe code that doesn't exist.

2. **Check for hallucinations** — CLI tools may fabricate issues: non-existent
   variables, imagined type mismatches, phantom security vulnerabilities. Confirm
   the issue exists in the actual code before fixing.

3. **Assess the fix** — Even if the issue is real, the suggested fix may be
   wrong, break existing behavior, or conflict with project conventions. Evaluate
   before applying. A better fix may exist.

4. **Conflicting suggestions** — When Codex and Gemini suggest different fixes
   for the same issue, evaluate both against project conventions and code
   context. Pick the better one, or mark as QUESTION if human judgment is needed.

## Fix Process

For each finding that passes critical evaluation:

1. Read the referenced file and understand the surrounding code
2. Apply the fix (or a better fix if the suggestion is suboptimal)
3. After all fixes, run project tests if they exist
4. If a test fails, revert the fix that caused it and mark as DEFERRED
5. Record each finding's status for the fix report

## Fix Report

Present a single fix report to the user after all fixes are applied. Load
`references/output-format.md` for the full template.

### Format

Two parts: a **summary table** for quick scanning, then **numbered details**.

```markdown
## CLI Review Fix Report

**Context:** [PR #N / Branch diff / Uncommitted / Full codebase]
**Engines:** [Codex CLI, Gemini CLI]
**Findings:** N total → X fixed, Y wontfix, Z deferred, W question

### Summary

| # | Severity | Location | Finding | Source | Status |
|---|----------|----------|---------|--------|--------|
| 1 | CRITICAL | file.ts:L42 | Issue description | AGREED | FIXED |
| 2 | HIGH | file.ts:L100 | Issue description | CODEX | WONTFIX |
| ... | ... | ... | ... | ... | ... |

### Details

**1. file.ts:L42 `symbol`** — CRITICAL — FIXED
What was wrong, what was changed, verification result.

**2. file.ts:L100 `symbol`** — HIGH — WONTFIX
Why this was rejected (hallucination, intentional design, etc).
```

Source column: `AGREED` (both engines), `CODEX` (Codex only), `GEMINI`
(Gemini only), or the engine name when only one was used.

### Fix Statuses

| Status | Meaning | Required Info |
|---|---|---|
| FIXED | Issue resolved in code | What was changed + verification |
| WONTFIX | Intentionally not fixing | Reason (cite docs/conventions if applicable) |
| DEFERRED | Valid but not fixing now | Why (test failure, needs design decision, tracked issue) |
| QUESTION | Needs human decision | Specific question for the user |

## Result Presentation

Load `references/output-format.md` for full templates.

### Severity Levels

| Severity | Meaning |
|---|---|
| CRITICAL | Security vulnerabilities, data loss, crashes |
| HIGH | Bugs, logic errors, broken functionality |
| MEDIUM | Code quality, performance, maintainability |
| LOW | Style, naming, minor improvements |

### Multi-Engine Agreement Tags

| Tag | Meaning |
|---|---|
| AGREED | Both engines flagged the same issue — higher confidence |
| CODEX ONLY | Only Codex flagged this |
| GEMINI ONLY | Only Gemini flagged this |

## Sub-Agent Recommendation

When the Agent tool is available, prefer sub-agents for CLI execution. Each
CLI review takes minutes, so parallel sub-agents save significant wall-clock
time.

**Recommended split:**

- **Review sub-agent(s)** — one per CLI for parallel execution. Each runs the
  CLI tool, parses output, and returns a concise structured finding list (not
  the full raw CLI output).
- **Fix sub-agent** (optional) — receives the parsed finding list, reads
  referenced files, critically evaluates each finding, applies fixes, runs
  tests. Returns the fix report.

**Why:** CLI review output can be very large (especially full codebase reviews).
Sub-agents absorb this without bloating the main conversation. Parallel
execution is also natural — each CLI in its own sub-agent.

**Permission caveat:** Sub-agents inherit stricter permission defaults and
cannot prompt the user for interactive approval. If a sub-agent fails because
Bash permission for the CLI command was denied or timed out, fall back to
running CLIs from the main context using `run_in_background` for parallelism.
Pre-configuring CLI permissions in project or user settings (e.g., allowing
`bash(codex exec:*)` and `bash(gemini:*)`) eliminates this issue.

**Fallback:** If the Agent tool is not available or sub-agents fail due to
permissions, run everything in the main context. Use `run_in_background` Bash
calls for parallel CLI execution. The skill works either way.

## Edge Cases

| Scenario | Behavior |
|---|---|
| Neither CLI installed | Show install instructions for both; stop |
| One CLI fails, other succeeds | Present results from successful CLI; note failure with error |
| Specific CLI requested but missing | Error with install instructions for that CLI; stop |
| No reviewable context | Inform user; suggest making changes or specifying scope |
| Large diff (>3000 lines) | Warn user; offer to scope to specific directories or file types |
| CLI times out | Report timeout; present any partial results |
| Codex diff review drifts or hangs | Use `cli-review-codex.sh` instead of raw `codex exec review --base ...` |
| Sub-agent CLI call fails (permissions) | Retry from main context with `run_in_background`; do not abort |
| Gemini extension command fails | Wrapper auto-falls back to rich pipe mode with stderr warning |
| `origin/HEAD` differs from PR base | Wrapper logs warning; extension diffs against `origin/HEAD` |
| CLI returns no findings | Report "no findings" for that engine; skip fix phase |
| User says "full codebase" | Skip context detection; use full codebase mode |
| All findings are hallucinations | WONTFIX each with explanation; no code changes made |
| Tests fail after a fix | Revert that fix; mark as DEFERRED with test failure details |
| No project tests found | Skip test step; note "no tests available" in fix report |
| Conflicting suggestions (Codex vs Gemini) | Evaluate both; pick better one or mark QUESTION |

## Reference Loading

Load only what you need for the current step:
- CLI flags and troubleshooting → `references/cli-commands.md`
- Codex diff review prompt → `references/codex-review-prompt.md`
- Gemini review prompt template → `references/review-prompt.md`
- Result and fix report formatting → `references/output-format.md`

## Scope Limits

This skill is on-demand and single-pass. It does **not**:
- Loop or re-review — evaluates and fixes once, then reports
- Post results to GitHub or create commits (user decides what to do with fixes)
- Run as a hook or in CI
- Replace the agent's own review — it adds external perspectives and auto-fixes
