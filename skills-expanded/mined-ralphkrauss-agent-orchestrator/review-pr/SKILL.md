---
name: review-pr
description: Full branch review against main across 9 dimensions (plan compliance, financial, events, tests, currency, performance, security, quality, simplification). Reviews ALL changes on the branch, not just the current session. Use when user says "review pr", "review-pr", "review branch", "self review", "self-review", "review before PR", "quality gate", "pre-PR review", "check before PR", or wants a full quality review before creating a pull request.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Review PR (Branch-Scoped)

Full quality gate that reviews ALL changes on the current branch vs main across 9 dimensions. Unlike `/review` (which only checks uncommitted session changes), this reviews the entire branch diff — every commit since diverging from main. Sits between `/implement-plan` and `/create-pr`.

## Instructions

### Step 1: Determine Scope

1. Get the current branch: `git branch --show-current`
2. Parse user arguments to determine diff scope:
   - **No arguments** (default): branch vs main -- `git diff main...HEAD`
   - **Commit range**: e.g., `HEAD~3` -- `git diff HEAD~3...HEAD`
   - **File filter**: e.g., `src/Core/` -- append `-- src/Core/` to the diff command
3. Count changed files and lines to set expectations:
   ```bash
   git diff main...HEAD --stat
   ```
4. If the diff is empty, report "No changes to review" and stop.

### Step 1b: Load Context and Implementation Plan

1. Check if a context file exists at `contexts/{branch-name}/context.md`
   - If it exists, read it. This contains pre-curated research: critical path, must-read file manifest, external provider knowledge, internal architecture patterns, and test patterns.
   - Use this context to understand the intent behind the changes — it informs which documentation to cross-reference and which invariants are most critical to verify.
2. Check if a plan exists for this branch: `plans/{branch-name}/plan.md`
2. If the plan index exists, read it to find all sub-plan files
3. Read each sub-plan file to extract:
   - **Decisions** — the design choices agreed during planning
   - **Scope** — what's in scope and explicitly out of scope
   - **Risks & Edge Cases** — identified risks and their expected mitigations
   - **Implementation Tasks** — the task list with acceptance criteria
4. If no plan exists, note "No plan found — skipping plan compliance dimension" and continue
5. The plan serves as the **source of truth** for what the ticket intended to achieve. Use it in Step 3 to verify the implementation matches intent.

### Step 2: Load Diff and Classify Files

1. Read the full diff: `git diff main...HEAD` (or user-specified range)
2. Get the list of changed files: `git diff main...HEAD --name-only`
3. Classify each changed file into categories the project's review checklist recognizes (typical buckets: safety-critical / domain / integration / UI / infrastructure / tests / config). Adapt the buckets to the codebase's actual structure.
4. Enable **strict mode** automatically if any safety-critical files are in the diff (excluding test code) — money handling, irreversible mutations, regulated flows, security boundaries, etc.
5. Log which categories are present and which review dimensions will be N/A

### Step 2b: Load Review Rules

Read all `.agents/rules/*.md` files to have the full rule set available for the review dimensions.

Log: "Review rules loaded from .agents/rules/"

### Step 3: Run Review Dimensions

Load the plan (from Step 1b), any project-maintained review checklist (e.g., `docs/reviewing/checklist.md`), and the `.agents/rules/` (from Step 2b), then execute the relevant dimensions. Typical dimensions:

0. **Plan Compliance** -- implementation matches planned scope, decisions honored, tasks completed, nothing missing
1. **Safety-critical Integrity** -- idempotency, audit trails, correctness of irreversible writes, transactional outcomes
2. **Domain Events / State Transitions** -- event registration on state transitions, stable stream IDs, deferred events
3. **Test Coverage** -- new/changed code has tests, edge cases covered, test patterns correct
4. **Locale / Configuration** -- no hardcoded locale-specific values, correct config resolution
5. **Performance** -- N+1 queries, unnecessary round trips, hot-path overhead
6. **Security** -- input validation, authorization checks, no secrets in code
7. **Code Quality** -- naming, SOLID, consistency with codebase patterns, component size limits
8. **Simplification** -- dead code, over-engineering, unnecessary abstractions

For each dimension:
- **Skip** if no relevant files changed (mark N/A with reason)
- Check the project's static checklist items if one exists
- **Also check `.agents/rules/` rules** — for each rule relevant to this dimension, verify the diff does not exhibit the anti-pattern. If it does, report it with the rule file and section.
- Provide **evidence** for every finding (file path + line number)
- Classify findings by severity:
  - **Critical** -- blocks PR: safety-critical incorrectness, data loss risk, missing audit trail, broken idempotency
  - **Important** -- should fix: pattern violations, missing tests for changed logic, security gaps
  - **Minor** -- acceptable debt: naming issues, unused imports, dead code
  - **Suggestion** -- nice-to-have: refactoring opportunities, documentation improvements

**Strict mode**: when enabled, any safety-critical invariant violation in production code is automatically Critical. Test files are exempt — they legitimately use patterns that would be violations in production code.

### Step 3b: Critical Documentation Validation

For each file in the diff that touches crucial logic (money/safety-critical flows, third-party integrations, domain state transitions, irreversible mutations):

1. **Identify the relevant documentation** — find the docs that describe how this code should behave (`docs/`, architecture notes, third-party spec files, `AGENTS.md` sections, context file)
2. **Read the documentation** — do not rely on memory or pattern-matching. Actually read the doc.
3. **Verify correctness against the doc** — trace the code path and confirm it implements what the documentation specifies. Check:
   - Are the method calls correct? (correct method on the correct service, correct event type)
   - Are the parameters in the right order with the right types?
   - Does the flow match the documented sequence?
   - Are edge cases from the documentation handled?
   - Does the implementation match the plan's Decisions and acceptance criteria?
4. **Report discrepancies** as Critical findings with evidence from both the code and the doc

This step is what separates a mechanical pattern check from a real review. Pattern compliance does not prove correctness — a handler can follow every naming convention and still call the wrong service method.

### Step 4: Auto-Fix Minor Issues

Collect all Minor and Suggestion findings that are safe to auto-fix:
- Unused imports
- Dead code (unused private functions/methods, unreferenced private fields)
- Missing `readonly`/`const` on fields that are never reassigned (where idiomatic)
- Trailing whitespace, unnecessary blank lines

**Do NOT auto-fix**:
- Anything that changes business logic or public API surface
- Any code in safety-critical files
- Naming changes that affect serialization (e.g., JSON/protobuf field names)

Apply fixes to the working tree. Do not commit -- leave changes for user review. Track what was fixed for the presentation step.

### Step 5: Smart Verification

After auto-fixes are applied:
- **Cosmetic-only fixes** (formatting, dead code removal, unused imports): run the project's targeted build command on affected modules only
- **Business logic touched** (by auto-fix or user-requested fix): run the project's targeted test command on the affected test suite (see project conventions in `AGENTS.md`)

Report verification results. If build or tests fail after auto-fix, revert the failing fix and report it.

### Step 6: Save Artifact

```bash
BRANCH=$(git branch --show-current)
mkdir -p plans/$BRANCH/reviews
ARTIFACT=plans/$BRANCH/reviews/review-pr-$(date +%Y-%m-%d).md
```

If file exists for today, append counter: `review-pr-2026-04-01-2.md`

Write the full review output (all dimensions, findings, verdicts) to `$ARTIFACT`. This creates a durable record for PR history and cross-referencing with Codex review artifacts.

### Step 7: Present Findings

Present findings grouped by severity (Critical first, then Important, Minor, Suggestion):

**For each Critical/Important finding:**
- File path and line number
- What is wrong and why it matters
- Proposed specific fix
- Ask user: **fix now**, **defer**, or **dismiss**

**For auto-fixed items:** summarize what was changed with file paths.

**For N/A dimensions:** list with reason for skip.

**End with overall assessment:**
- **Ready for PR** -- no Critical/Important findings remaining
- **Needs fixes** -- Critical/Important findings need resolution before PR
- **Blocked** -- Critical findings that require architectural changes

**After the assessment, suggest Codex second opinion:**
> "Run `/review-pr-codex` for a GPT-powered second opinion? (requires Codex CLI installed)"

This is informational only — do not run `/review-pr-codex` automatically.

### Step 8: Knowledge Capture — Rule Check

For violations with no corresponding existing rule — these are the strongest signal for new rules. Check `.agents/rules/` for coverage. If a finding represents a reusable pattern (not a one-off typo or naming nit), suggest `/create-rule`. Provide:
- The pattern (rule text)
- The anti-pattern (the bad code that was caught, with example)
- The evidence (source: PR number, the review finding that surfaced it)
- Suggested context tags (what kind of work this applies to)

**Do NOT write rule files directly** — `/create-rule` handles dedup, ID assignment, index update, and source tracking.

## Critical Rules

- **Evidence-based** -- every finding must cite file:line. No vague "looks wrong" assessments.
- **No false confidence** -- if unable to determine whether something is an issue, flag it for user review rather than silently passing.
- **Safety-critical code is sacred** -- any safety-critical violation is Critical, no exceptions. This includes idempotency gaps, missing audit trails, incorrect state handling, direct property mutation on invariant-bearing aggregates.
- **Test code is exempt from strict mode** -- test files legitimately use patterns that would be violations in production code.
- **Don't fix what isn't broken** -- auto-fix only clearly wrong things (unused code, naming). Never auto-fix code that is working correctly just to make it "better".
- **Scope hygiene** -- only review files that are in the diff. The review covers changes, not the entire codebase.
- **One review, not a rewrite** -- findings should be actionable and specific. Do not propose rewrites of working code.
- **Build/test constraints** -- use the project's targeted build/test commands. Never run full apps. Only run affected test suites.
- **Leave fixes uncommitted** -- all changes stay in the working tree for user review.
- **Single agent, sequential** -- do not spawn subagents. Execute all steps in the current session.

## Checklist

- [ ] Scope determined (branch vs main, commit range, or file filter)
- [ ] Plan loaded (or noted as absent)
- [ ] Diff loaded and files classified into categories
- [ ] Review rules loaded from `.agents/rules/`
- [ ] Financial strict mode enabled/disabled based on file classification
- [ ] All 9 dimensions executed (or marked N/A with reason) — checklist + lessons
- [ ] Findings classified by severity with evidence
- [ ] Minor issues auto-fixed (cosmetic only, no business logic)
- [ ] Verification run (build for cosmetic fixes, tests for logic changes)
- [ ] Critical/Important findings presented with fix proposals
- [ ] User decisions recorded (fix/defer/dismiss) for each finding
- [ ] Overall assessment delivered (Ready / Needs fixes / Blocked)

## Reference

- `docs/reviewing/checklist.md` -- detailed per-dimension checks (9 dimensions)
- `.agents/rules/` -- review rules (auto-loaded by path patterns)
- `plans/{branch-name}/plan.md` -- implementation plan index (if exists)
- `AGENTS.md` -- repository-wide constraints and financial platform DNA
- `docs/guides/financial-application-principles.md` -- financial invariants and anti-patterns
- `.agents/skills/implement-plan/SKILL.md` -- preceding step in the workflow
- `.agents/skills/create-pr/SKILL.md` -- next step in the workflow
