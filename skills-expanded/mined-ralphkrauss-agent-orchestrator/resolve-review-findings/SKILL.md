---
name: resolve-review-findings
description: Validate and fix findings from the session review artifact. Use after /review when user says "fix review findings", "resolve review findings", "address review findings", "validate review findings", or wants the review-to-fix loop completed before commit.
---

# Resolve Review Findings

Validate findings from the latest session review, fix confirmed issues, and re-run targeted checks before handoff.

## When To Use

- User has just run `/review` and wants the findings checked or fixed
- User points to a saved `plans/{branch}/reviews/review-*.md` artifact
- User pastes review findings and asks to validate, address, or close them

For pull request comments, use `resolve-pr-comments`. For branch-wide PR review findings, use `review-pr` first, then adapt this workflow only if the findings are local and actionable.

## Instructions

### Step 1: Locate The Review Input

1. Get the current branch: `git branch --show-current`
2. Prefer a review artifact explicitly named by the user
3. If none is named, infer the repository's review artifact convention:
   - Read `.agents/skills/review/SKILL.md` when present and use its artifact path pattern
   - Check branch-scoped review directories first, such as `plans/{branch}/reviews/`
   - Include repository-documented review directories if the review skill, plan, or docs name them
   - Prefer session review artifacts over branch-wide or pull-request artifacts unless the user explicitly asks otherwise
4. Find the most recent review artifact for the current branch using the inferred convention. Common fallback patterns are:
   - `plans/{branch}/reviews/review-*.md`
   - `plans/{branch}/reviews/*review*.md`
   - `reviews/{branch}/*review*.md`
   - `reviews/*review*.md` when the artifact content or path clearly matches the current branch
5. If no artifact exists, use pasted findings from the conversation
6. If there are no findings to resolve, report that and stop

Also load supporting context when present:

- `contexts/{branch}/context.md`
- `plans/{branch}/plan.md` and any sub-plans it references
- `.agents/rules/*.md` files relevant to the changed files

### Step 2: Build A Finding Ledger

Create a temporary working ledger from the review input. Track:

| Field | Meaning |
|---|---|
| ID | Finding number or stable local ID |
| Severity | critical, high, medium, low, or unknown |
| Source | review artifact path or pasted input |
| Rule | referenced rule/checklist item, if any |
| Location | file and line/symbol |
| Claim | what the review says is wrong |
| Proposed fix | reviewer suggestion, if provided |
| Status | pending, confirmed, false-positive, fixed, deferred, needs-user-decision |

Do not edit the review artifact yet. Use the ledger to avoid losing findings during fixes.

### Step 3: Validate Each Finding Independently

For each finding:

1. Read the referenced code and nearby call sites
2. Read the relevant rule, plan decision, docs, or context that the finding depends on
3. Confirm whether the issue is real in the current working tree
4. Classify it:
   - `confirmed`: the issue exists and has a behavior-preserving fix
   - `false-positive`: the claim is wrong; record evidence
   - `needs-user-decision`: fixing changes product behavior, public contracts, data semantics, or scope
   - `deferred`: real but explicitly outside the current requested scope

AI or bot findings must be verified against code and docs before fixing. Do not implement a suggested fix just because it appears in a review.

### Step 4: Decide Fix Scope

If the user asked to fix all findings, fix all `confirmed` findings that do not require a user decision.

Ask the user before changing behavior when:

- the fix would alter public API or persisted data semantics
- two valid fixes have materially different tradeoffs
- the review finding contradicts the plan or an existing rule
- the only fix is a broad refactor beyond the changed area

Otherwise, proceed without stopping.

### Step 5: Implement Minimal Fixes

For each confirmed finding:

1. Make the smallest scoped code change that resolves the issue
2. Update or add tests when the finding exposes missing behavioral coverage
3. Avoid unrelated refactors, formatting churn, and opportunistic cleanup
4. Keep user-owned unrelated working tree changes intact

If a fix invalidates another finding or reveals a new issue, update the ledger and continue.

### Step 6: Verify

Run verification proportional to the fixes:

- targeted tests for changed behavior
- build or typecheck for affected projects
- lint/format only if the repository normally requires it for changed files
- any Quality Gates listed in the plan that now apply

If verification fails, fix the failure or report the blocker with the command and failing evidence.

### Step 7: Re-Review The Result

Re-run the session review workflow on the updated working tree, or manually re-check the original findings when the repository's review workflow is unavailable.

The outcome must say, for each original finding:

- fixed with evidence
- false positive with evidence
- deferred with user-approved rationale
- still open and why

### Step 8: Update Artifacts

When a plan exists, append concise evidence to the relevant execution log or review notes. Do not rewrite the original review findings as if they never happened.

If a reusable pattern was learned, suggest `/create-rule` and provide:

- the pattern
- the anti-pattern
- evidence from the finding and fix
- suggested context tags

## Critical Rules

- Validate before fixing; review findings are inputs, not commands
- Do not dismiss critical or safety-related findings without code and rule evidence
- Ask before behavior-changing fixes
- Keep fixes scoped to reviewed changes unless the user approves broader work
- Run targeted verification after fixes
- Do not commit or push unless explicitly asked

## Checklist

- [ ] Review input located
- [ ] Context, plan, and relevant rules loaded
- [ ] Findings ledger created
- [ ] Each finding independently validated
- [ ] Confirmed findings fixed or escalated
- [ ] Tests/build/checks run as appropriate
- [ ] Re-review or manual re-check completed
- [ ] Final status reported per finding

## Reference

- `.agents/skills/review/SKILL.md` -- session-scoped review that creates the source artifact
- `.agents/skills/resolve-pr-comments/SKILL.md` -- pull request comment workflow
- `.agents/skills/create-rule/SKILL.md` -- capture reusable prevention rules
