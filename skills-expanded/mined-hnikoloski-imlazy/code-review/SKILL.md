---
name: code-review
description: Two roles — request a code review (dispatch reviewer subagent) and receive a code review (process feedback rigorously). Use after each task in planning full mode, before merge, or when stuck
---

# code-review

## When to use

- After each task in `planning` (full mode)
- Before merging a feature
- When stuck (fresh perspective unblocks you)
- After fixing a complex bug

## Requesting a review

**Step 1: Get git SHAs**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main for pre-merge review
HEAD_SHA=$(git rev-parse HEAD)
```

**Step 2: Dispatch code reviewer subagent** using the template at `code-reviewer.md` (next to this skill). Fill in:
- `{DESCRIPTION}` — brief summary of what was built
- `{PLAN_OR_REQUIREMENTS}` — what it should do
- `{BASE_SHA}` / `{HEAD_SHA}` — the commit range
- `{GIT_DIFF}` — output of `git diff BASE_SHA..HEAD_SHA`

**Step 3: Act on feedback**
- **Critical** → fix immediately, re-review
- **Important** → fix before proceeding
- **Minor** → note for later
- **Reviewer is wrong** → push back with technical reasoning and evidence; don't blind-implement

Never skip review because "it's simple". Never ignore Critical issues. Never proceed with unfixed Important issues.

## Receiving a review

When you receive code review feedback, apply this process before implementing anything:

1. **Verify the feedback is technically correct.** Read the cited file and line. Does the issue actually exist there?

2. **Distinguish severity.** Critical issues block progress. Important issues should be fixed. Minor issues are optional. If the reviewer didn't label severity, ask for clarification.

3. **Never blind-implement Critical feedback without checking it first.** A reviewer can be wrong. If something feels off, verify with a test or look at the actual code.

4. **Push back when the reviewer is wrong.** "The test at line 42 already covers that edge case — here is the assertion: [paste test]." Technical evidence beats assertion.

5. **Fix, then re-request review.** Don't mark "fixed" without actually running the test suite.

Common pitfalls:
- Implementing all feedback without verifying — can introduce new bugs
- Dismissing feedback without checking — misses real issues
- Treating Minor as Critical — wastes time on low-impact polish
