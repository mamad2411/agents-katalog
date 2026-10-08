---
name: cr-3-review
disable-model-invocation: true
description: Perform a comprehensive code review workflow on the current branch changes. Gathers business context, analyzes diffs, and generates structured review output with prioritized issues.
context: fork
agent: general-purpose
---

Perform a comprehensive code review workflow on the current branch changes.

## Arguments

- `$ARGUMENTS`: Base branch to compare against (default: `master`)
  - Example: `/cr-3-review main` or `/cr-3-review develop`

## Workflow Steps

### Step 1: Gather Business Context

1. **Read context file** (if exists):
   - Check for `.claude/context.md` in the project root
   - This file contains business logic, specs, and system design prepared by the developer
   - Use this context to verify implementation alignment

2. **Scan CLAUDE.md for relevant docs**:
   - Read the project's `CLAUDE.md` (documentation TOC)
   - Based on the changed files/features, identify relevant docs mentioned
   - Read those docs to understand related requirements and design decisions

3. **Check for testing philosophy** (if test files changed):
   - Look for `docs/rails_testing_philosophy.md` in the project root
   - If found, read it and use as additional criteria for reviewing test changes
   - Apply these project-specific testing standards alongside general test review

4. **Keep this context in mind** for subsequent review steps to verify:
   - Implementation aligns with business requirements
   - Edge cases from specs are handled
   - Design decisions are followed
   - Test changes follow project's testing philosophy (if available)

### Step 2: Read Reviewer Feedback (if exists)

1. Check for `.claude/reviewer-feedback.md`
2. If exists:
   - Parse all reviewer items (they have structured format from `/cr-2-feedback`)
   - Store items for merging in Step 6
   - Reviewer items take priority for overlapping concerns
3. If not exists:
   - Continue with AI-only review (no reviewer feedback to merge)

### Step 3: Get the Diff and Commit Messages

1. Determine base branch: Use `$ARGUMENTS` if provided, otherwise `master`
2. Run `git diff <base-branch>...HEAD` to get all changes on this branch
3. Run `git log <base-branch>..HEAD --format='%H%n%B%n---'` to get the **full commit
   message bodies** (not `--oneline`). Commit bodies frequently carry the decision and
   the reasoning behind it — that is context the diff alone does not show. Keep this
   for Step 5 (documentation) and Step 6 (review).
4. If empty, try `git diff HEAD~1` for the latest commit
5. **If still no diff found, STOP and report error:**
   ```
   Error: No changes found to review.
   - No diff between current branch and <base-branch>
   - No changes in the latest commit
   Please ensure you have uncommitted or committed changes to review.
   ```

### Step 4: Dead Code Analysis

Before reviewing, search for code made dead by this MR's changes:

1. **From the diff, extract:**
   - Methods/functions that were **deleted or renamed**
   - Methods/functions whose **callers were removed** (e.g., a call site was deleted)
   - Conditions/guards that make downstream code **unreachable**

2. **For each candidate, search the codebase** (using `rg` or grep):
   - Search for references to the method/function name outside of its definition
   - Exclude test files from caller search (tests don't count as callers)
   - Exclude the method's own definition and comments

3. **Build a dead code list:**
   - Methods with **zero remaining callers** in non-test code
   - Note the confidence level: **high** (no callers found) vs **medium** (only dynamic/ambiguous callers like `send(:method_name)`)

4. **Keep this list** for use in Step 6 (review) and Step 7 (conflict detection).

**Scope:** Only analyze methods/functions in files touched by the MR. Do not scan the entire codebase for pre-existing dead code.

### Step 5: Documentation Analysis

Run both checks; each produces findings that are merged into Step 6's output using the
`### 10. Documentation` criteria (including its severity guidance and `[docs]` prefix).

**A. Do changed docs follow the repo's rules?**

Only if the diff touches documentation (`docs/**`, `*.md`, ADRs, changelogs):

1. Read the project's `docs/README.md` and skim the `docs/` tree with Glob to learn the
   real layout (which Diátaxis type lives where, ADR location and template, naming and
   index conventions, when docs are mandatory).
2. Review each changed/added doc against that policy: right location, right doc type and
   register, conventions followed, index/TOC updated, accurate against this MR's code.
3. Also flag docs the MR should have updated but didn't — search `docs/` for mentions of
   behavior, paths, flags, or endpoints this MR changed.
4. If `docs/README.md` is absent, use generic Diátaxis and note that no project doc
   policy was found.

**B. Is anything in this branch worth documenting?**

Always, even when no doc file changed:

1. Re-read the commit messages from Step 3 and `.claude/context.md` (if present),
   looking for **decisions and their rationale**: why an approach was chosen, what was
   rejected, trade-offs, constraints, gotchas. Rationale that exists only in a commit
   message is effectively lost — it belongs in `docs/`.
2. From the diff, identify newly introduced or altered **interface surface** (endpoint,
   config key, env var, CLI flag, schema, public API) and **operational procedures**.
3. For each, decide the Diátaxis type, the concrete target path per the project's own
   structure, and 1–2 lines of what to write. Raise an **ADR** finding when the change
   makes a decision future maintainers would need the reasoning for and no ADR exists.
4. Skip mechanical refactors, test-only changes, and dependency bumps.

Related skill: `doc-suggestions` does this across many MRs at once; this step is the
branch-local equivalent and shares its policy-from-`docs/README.md` grounding.

### Step 6: Code Review & Merge

Apply the review criteria defined in `~/.claude/skills/code-review-criteria/SKILL.md`,
folding in the documentation findings from Step 5.

**Merging with reviewer feedback** (if `.claude/reviewer-feedback.md` exists):

1. Start with all reviewer items (preserve exactly, mark as `👤 Reviewer`)
2. Perform AI review and add AI items (mark as `🤖 AI`)
3. For overlapping concerns (same file/area, similar issue):
   - Keep reviewer's version as primary
   - Add AI's additional context if valuable
   - Mark as `🤖 AI + 👤 Reviewer`
4. Number items sequentially within each priority section

Write the review directly to `.claude/code-review.md` using this structure:

```markdown
# Code Review Summary

**Branch:** <current-branch>
**Base:** <base-branch>
**Files Changed:** <count>
**Lines:** +<additions> / -<deletions>

## Decision Options

- **Accept**: Will fix this issue
- **Drop**: Issue is incorrect or not applicable (explain why)
- **Won't Fix**: Valid issue but intentionally not addressing (explain why)

## Approach Options

- **Suggested fix**: Use the recommended fix as-is
- **Alternative**: Your different approach (describe in Notes)

---

## Findings

### 🔴 Blocking (Must Fix)

#### 1. `<file_path:line>` - <brief title>
- **Source:** 🤖 AI / 👤 Reviewer / 🤖 AI + 👤 Reviewer
- **Issue:** <description of the problem>
- **Suggestion:** <recommended fix>
- **Decision:** _Accept / Drop / Won't Fix_
- **Approach:** _Suggested fix / Alternative_
- **Notes:** _[Your response, alternative approach details, or discussion points]_

---

### 🟡 Important (Should Fix)

#### 1. `<file_path:line>` - <brief title>
- **Source:** 🤖 AI / 👤 Reviewer / 🤖 AI + 👤 Reviewer
- **Issue:** <description>
- **Suggestion:** <recommended fix>
- **Decision:** _Accept / Drop / Won't Fix_
- **Approach:** _Suggested fix / Alternative_
- **Notes:** _[Your response, alternative approach details, or discussion points]_

---

### 🟢 Nit (Nice to Have)

#### 1. `<file_path:line>` - <brief title>
- **Source:** 🤖 AI / 👤 Reviewer / 🤖 AI + 👤 Reviewer
- **Issue:** <description>
- **Suggestion:** <recommended fix>
- **Decision:** _Accept / Drop / Won't Fix_
- **Approach:** _Suggested fix / Alternative_
- **Notes:** _[Your response, alternative approach details, or discussion points]_

---

### 💡 Suggestions

#### 1. `<file_path:line>` - <brief title>
- **Source:** 🤖 AI / 👤 Reviewer / 🤖 AI + 👤 Reviewer
- **Issue:** <description>
- **Suggestion:** <recommended fix>
- **Decision:** _Accept / Drop / Won't Fix_
- **Approach:** _Suggested fix / Alternative_
- **Notes:** _[Your response, alternative approach details, or discussion points]_

---

## 🔗 Issue Relationships

<!-- Added by Step 7 - see that step for format -->

---

## Verdict

✅/❌ **<Verdict>** - <Summary explanation>

## Key Insight

<One sentence summary of the most important observation>
```

### Step 7: Dependency, Conflict & Dead Code Conflict Analysis

After generating findings, analyze relationships between issues:

1. **Same-location issues**: Items targeting the same file/method
2. **Cascading fixes**: Fixing one issue may resolve another
3. **Conflicting solutions**: Fixes that contradict or interfere with each other
4. **Merge candidates**: Issues that should be addressed together
5. **Dead code conflicts**: Cross-reference all findings against the dead code list from Step 4 (dead code analysis). If any finding (reviewer or AI) suggests changes to code identified as dead, flag it.

**Add this section to `.claude/code-review.md` before Verdict:**

```markdown
---

## 🔗 Issue Relationships

### Cascading Fixes
<!-- Issues where fixing one resolves another -->
- **#X resolves #Y**: <explanation>

### Conflicts
<!-- Fixes that may interfere with each other -->
- **#X vs #Y**: <describe conflict and recommended resolution>

### Dead Code Conflicts
<!-- Findings that suggest changes to code with no remaining callers -->
- **#X** targets `method_name` (`file:line`) which has no callers after this MR — consider removing instead of modifying. Confidence: high/medium.

### Same-Location Changes
<!-- Issues modifying the same code area - coordinate fixes -->
- **#X, #Y, #Z** (`file:lines`): <coordination notes>

### Recommended Fix Order
<!-- Optimal sequence considering dependencies -->
1. #X - <reason>
2. #Y - <reason>
```

If no relationships found, add:
```markdown
## 🔗 Issue Relationships

No dependencies or conflicts detected between findings.
```

### Step 8: Apply Source-Based Field Defaults

After writing the review file, re-read `.claude/code-review.md` and apply defaults based on each item's Source:

- **👤 Reviewer** (or 🤖 AI + 👤 Reviewer) items: Set Decision to `Accept`, Approach to `Suggested fix`, and omit Notes
- **🤖 AI** items: Leave Decision/Approach/Notes as placeholders for the reviewer to fill in

Update the file in-place with these defaults applied.

### Step 9: Commit Review

1. Stage the review file:
   ```
   git add .claude/code-review.md
   ```

2. Commit with message:
   ```
   Add code review for <current-branch>
   ```

## Output Files

- `.claude/code-review.md` - Code review with actionable findings
