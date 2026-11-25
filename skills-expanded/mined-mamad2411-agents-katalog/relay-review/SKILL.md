---
name: relay-review
argument-hint: "[run-id or branch-name or PR-number]"
description: Independent PR review against Done Criteria in a fresh context, free from planning bias. Use after dispatch completes and a PR exists.
context: fork
compatibility: "Requires gh CLI. Context isolation is enforced per-platform (see Context Isolation section)."
metadata:
  related-skills: "relay, relay-plan, relay-dispatch, relay-merge"
---

# Relay Review

Independent PR review against the Done Criteria contract and scoring rubric. Use `scripts/review-runner.js` so round count, reviewer invocation, PR comments, and manifest transitions stay script-managed.

## Context Isolation

Reviews MUST run in a fresh context — no prior planning, dispatch, or conversation history. This prevents planning bias from influencing the verdict.

| Platform | Mechanism | How |
|----------|-----------|-----|
| Claude Code | `context: fork` frontmatter | Automatic — this SKILL.md's frontmatter triggers it |
| Codex (reviewer adapter) | `--ephemeral --sandbox read-only` | Automatic — `invoke-reviewer-codex.js` passes these flags |
| Claude (reviewer adapter) | `--bare --no-session-persistence` | Automatic — `invoke-reviewer-claude.js` passes these flags |
| Codex (as orchestrator) | Start a new session | Manual — do not continue from the dispatch session |
| Other / Fallback | Prefix prompt | Prepend: "You are reviewing code you did NOT write. You have no context about why it was written this way." |

When using `--reviewer codex` or `--reviewer claude`, isolation is handled by the adapter scripts. When orchestrating manually or from an unsupported platform, you must ensure isolation yourself.

## Setup: Establish the anchor

1. Get the PR diff and Done Criteria (this runs in a fresh context — fetch everything needed):
```bash
PR_NUM=$(gh pr list --head <branch> --json number -q '.[0].number')
BRANCH=$(gh pr view $PR_NUM --json headRefName -q '.headRefName')
gh pr diff $PR_NUM > /tmp/pr-diff.txt

# Issue number extraction — try each method until one succeeds:
ISSUE_NUM=$(gh pr view $PR_NUM --json closingIssuesReferences -q '.[0].number')
# Fallback 1: grep PR body for issue keywords
[ -z "$ISSUE_NUM" ] && ISSUE_NUM=$(gh pr view $PR_NUM --json body -q '.body' | grep -oiE '(closes|fixes|resolves|refs|related to) #[0-9]+' | grep -oE '[0-9]+' | head -1)
# Fallback 2: extract from branch name (try issue-<N> first, then any number)
if [ -z "$ISSUE_NUM" ]; then
  ISSUE_NUM=$(echo "$BRANCH" | grep -oE 'issue-[0-9]+' | grep -oE '[0-9]+')
  [ -z "$ISSUE_NUM" ] && ISSUE_NUM=$(echo "$BRANCH" | grep -oE '[0-9]+' | tail -1)
fi
# If all fail: escalate — cannot review without Done Criteria
[ -z "$ISSUE_NUM" ] && echo "ERROR: Cannot determine issue number. Provide it manually." && exit 1
gh issue view $ISSUE_NUM  # Done Criteria / Acceptance Criteria source
```

2. **Fix the anchor** — these do NOT change across rounds:
   - Done Criteria from the issue (the contract)
   - Rubric factors + targets from the Score Log (if relay-plan was used)
   - Original scope boundary ("do not change" areas)

3. Preferred path: let the review runner invoke an isolated reviewer directly:
```bash
RUN_ID=<run-id-from-dispatch>
node ${CLAUDE_SKILL_DIR}/scripts/review-runner.js --repo . --run-id "$RUN_ID" --pr "$PR_NUM" --reviewer codex --json
```

Supported built-in adapters:
- `--reviewer codex`
- `--reviewer claude`

Notes:
- `codex` uses a read-only structured-output adapter and must return a full two-phase verdict.
- `claude` requires an authenticated local Claude CLI session.

4. Fallback path for unsupported environments or debugging:
```bash
node ${CLAUDE_SKILL_DIR}/scripts/review-runner.js --repo . --branch "$BRANCH" --pr "$PR_NUM" --prepare-only --json
```

This writes round artifacts under `~/.relay/runs/<repo-slug>/<run-id>/`, including:
- `review-round-N-prompt.md`
- `review-round-N-done-criteria.md`
- `review-round-N-diff.patch`

The runner reviews the retained checkout recorded in `paths.worktree`, not the repo root. It also records `review.last_reviewed_sha`, enforces `review.max_rounds`, and escalates when the same issue fingerprint repeats 3 consecutive rounds.

## Review Loop

Two phases, run in order. Each round re-measures against the **original anchor**, not the previous round's state.

### Phase 1: Spec Compliance

5. Review the diff against Done Criteria (see `references/reviewer-prompt.md` or the generated `review-round-N-prompt.md`):
   - **Faithfulness**: Each Done Criteria item implemented? Scope respected?
   - **Stubs/placeholders**: Any `return null`, empty bodies, TODO in production paths?
   - **Integration**: Does it break callers/consumers of changed code?
   - **Security**: Auth/token handling, input validation, injection risks?

6. **Rubric verification** (when Score Log present):
   - Re-run ALL automated checks independently — do not trust the executor's reported results
   - Re-score ALL evaluated factors with fresh eyes (1-10)
   - Any required factor below target → issue
   - Score divergence ≥2 points from the executor → flag for review

7. **Phase 1 gate**: Issues found → return a structured verdict with `verdict=changes_requested`, then re-dispatch (see Re-dispatch below). Do NOT proceed to Phase 2 until Phase 1 passes.

### Phase 2: Code Quality (only after Phase 1 PASS)

8. Run a code review skill on changed files — check code quality, patterns, conventions, structural issues (use the platform's best-matching skill, e.g., Claude Code: `/review`; if no skill is available, perform the quality review inline inside the structured reviewer round)
9. Run a code simplification skill on changed files — unnecessary complexity, dead code, verbose patterns (use the platform's best-matching skill, e.g., Claude Code: `/simplify`; if no skill is available, review for simplification inline before returning `verdict=pass`)
10. Issues found → return `verdict=changes_requested`, then re-dispatch and **repeat from step 5** (Phase 1 — quality fixes can regress spec compliance)

### Drift and stuck detection (both phases)

Before any re-dispatch, check:
- **Scope:** Does the fix address a review issue, or is it scope creep?
- **Regression:** Are previously passing rubric factors still passing?
- **Churn:** Is the total diff growing without convergence?
- **Stuck:** Same issue 3+ consecutive rounds → escalate immediately (not fixable by the executor).

### Converge

11. Both phases pass → produce a structured verdict with:
    - `verdict=pass`
    - `next_action=ready_to_merge`
    - `issues=[]`

**Safety cap: 20 rounds total.** Ceiling, not target — most PRs converge in 1-3 rounds. Hitting the cap means something is structurally wrong; escalate.

## Verdict + Audit Trail

12. If you used the fallback path, apply the structured verdict with the review runner:
```bash
node ${CLAUDE_SKILL_DIR}/scripts/review-runner.js --repo . --run-id "$RUN_ID" --pr "$PR_NUM" --review-file /tmp/review-verdict.json
```

The runner:
- validates the JSON verdict
- optionally invokes the reviewer adapter itself when `--reviewer <name>` is used
- rejects the round if the reviewer mutates the repo and escalates the manifest
- writes the PR audit comment
- updates the relay manifest to `ready_to_merge`, `changes_requested`, or `escalated`
- writes `review-round-N-verdict.json`
- writes `review-round-N-raw-response.txt` when it invoked the reviewer itself
- writes `review-round-N-policy-violation.txt` if the reviewer changed files
- writes `review-round-N-redispatch.md` when changes are requested

<!-- NOTE: gate-check.js now treats the latest relay-review or relay-review-round comment as authoritative and blocks merge on CHANGES_REQUESTED or ESCALATED. -->

## Re-dispatch (when issues found)

Use the generated `review-round-N-redispatch.md` artifact as the targeted fix prompt. It already includes the issue list, scope guardrail, and original Done Criteria.

See `references/evaluate-criteria.md` for escalation policy (auto re-dispatch vs ask user).
