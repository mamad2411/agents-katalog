# Review This — Post-Implementation Code Review

You have just finished implementing changes. Before moving on, perform a rigorous code review by spawning a **principal-engineer** subagent.

## What To Do

### Step 1: Gather the diff

Run these commands in parallel:
- `git diff` (unstaged changes)
- `git diff --staged` (staged changes)
- `git status --short` (to identify untracked files)

### Step 2: Spawn the principal-engineer review

Use the **Task** tool with `subagent_type: "principal-engineer"` to perform the review. Provide the subagent with:

- The full diff of changes (both staged and unstaged)
- The list of files created or modified
- Any relevant context about what was implemented and why

Use this prompt structure for the subagent:

```
You are reviewing code changes just made in the cowork-mcp project. This is NOT a nitpick review. Ignore minor style preferences, trivial naming quibbles, and cosmetic issues — the linter handles those.

## Changed Files

[Insert list of modified/created files]

## Diff

[Insert full git diff output]

## Context

[Insert description of what was implemented]

## Review Focus Areas

### 1. Architectural Alignment
- Do changes follow patterns in `CLAUDE.md` and `docs/CONTEXT.md`?
- Are all Graph API calls routed through `graph/client.py` GraphClient singleton?
- Are all token operations routed through `auth/token_store.py`?
- Does `BearerAuthMiddleware` still cover all routes?

### 2. Coding Standards Compliance
- Follow `CLAUDE.md` rules?
- **Python**: type annotations on all public functions, no bare `Any` without justification, ruff-compliant, mypy strict-mode clean?
- No raw MSAL calls outside `auth/`, no raw httpx calls to Graph outside `graph/client.py`?

### 3. Completeness
- Error handling at Graph API boundaries (surface as MCP tool errors, not raw exceptions)?
- Pagination handled (`@odata.nextLink`) in all new list operations?
- New scope toggles registered in `config.py` Settings AND `graph/client.py` SCOPE_MAP?
- Missing tests? (>80% coverage target, Graph calls mocked, 401 paths tested)
- Unhandled edge cases or missing validation at system boundaries?

### 4. Correctness & Safety
- Potential runtime errors (None access on Graph response fields)?
- Security concerns: hardcoded secrets, tokens in logs, bearer auth bypass?
- Token cache file permissions enforced after writes?
- MSAL authority string correct (`consumers` not `common`)?

### 5. Simplicity & YAGNI
- Over-engineering for a single-user personal project?
- Unnecessary abstractions that add complexity without benefit?
- Could it be simpler while meeting requirements?

## What To Read

Before reviewing, read these project references:
- `CLAUDE.md` — project rules
- `auth/token_store.py` — token storage patterns
- `server.py` — BearerAuthMiddleware and tool registration

## Output Format

Write your findings to a REVIEW.md file in the relevant plan directory (if reviewing a plan), or create a REVIEW.md file in the project root (if reviewing standalone changes).

Format the REVIEW.md file as follows:

---
# Code Review

**Date**: {today's date}
**Reviewer**: Claude Opus 4.6 (principal-engineer)

## Summary
One-paragraph overall assessment.

## Findings

### 🔴 CRITICAL: [Finding Title]
**File**: `path/to/file.py` (lines X-Y)

**Issue**: Clear description of what is wrong or missing

**Recommendation**: Specific fix or approach

**Rationale**: Why this matters (reference CLAUDE.md rule, principle, or invariant)

(Repeat for each critical finding)

### 🟡 MODERATE: [Finding Title]
(Same format as critical)

### 🟢 MINOR: [Finding Title]
(Same format as critical)

## Verdict
- ✅ **PASS**: No critical or moderate findings. Ship it.
- ⚠️ **PASS WITH CHANGES**: Moderate findings exist. Address them, then ship.
- ❌ **NEEDS REWORK**: Critical findings exist. Must fix before proceeding.
---

**Severity Levels**:
- 🔴 **CRITICAL**: Must fix — correctness/security/architecture violation
- 🟡 **MODERATE**: Should fix — standards compliance, missing tests, completeness gaps
- 🟢 **MINOR**: Consider — simplification opportunities, minor improvements
```

### Step 3: Verify REVIEW.md was written

After the review completes:

1. **Check that REVIEW.md was created** — in the project root or relevant plan directory
2. **Read the REVIEW.md file** and parse the findings
3. **Share the summary and verdict** with the user

### Step 4: Address all findings

After reviewing the findings:

1. **Address all 🔴 CRITICAL findings** immediately
2. **Address all 🟡 MODERATE findings** — these should be fixed before the work is considered complete
3. **Consider 🟢 MINOR findings** — implement if they genuinely improve the code without over-engineering
4. **Report back** to the user what was changed in response to the review

If you disagree with a finding, explain your reasoning to the user rather than silently ignoring it.

### Step 5: Re-run tests

After addressing findings, run the full check suite to ensure fixes didn't break anything:

```bash
make check-all
```

## When to Use This Command

Use `/review-this` after:
- Completing a plan implementation
- Making significant changes to existing code
- Adding a new feature or capability
- Before creating a pull request
- Whenever you want a second opinion on code quality

## Notes

- This review complements, not replaces, automated linting and testing
- The principal-engineer agent has deep context on cowork-mcp architecture and standards
- The review is thorough but focused on meaningful issues, not nitpicks
- If the verdict is PASS, you've done good work — ship it with confidence!
