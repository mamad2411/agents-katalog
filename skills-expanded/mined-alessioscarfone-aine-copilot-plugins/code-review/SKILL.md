---
name: code-review
description: Run a multi-perspective code review that spawns parallel reviewer agents focused on different quality dimensions — simplicity/DRY, bugs/correctness, and project conventions — then consolidates findings into a single prioritized report. Use when the user asks to review code, check for bugs, audit recent changes, review a branch or PR, inspect code quality, or wants a second pair of eyes on their work. Also triggers on "review my changes", "anything wrong with this code", "check before I push", "sanity check", or "code audit". Do not use for implementing features, writing new code, or refactoring — those have their own workflows.
---

# Code Review

## Phase 1: Determine Review Scope

Initial request: $ARGUMENTS

**Actions**:
1. Create a todo list to track progress through all phases
2. Determine what code to review. The user may specify the scope explicitly; if not, infer from context or ask:

   | User says | Scope |
   |---|---|
   | "review my changes" / no specific scope | Unstaged changes (`git diff`) |
   | "review what I'm about to commit" | Staged changes (`git diff --cached`) |
   | "review this branch" / "compare to main" | Branch diff (`git diff main...HEAD`) |
   | "review these files" / specific paths | Only those files |
   | "review this PR" / PR number | Changes in the PR (`git diff main...HEAD` or the PR's base) |

3. Run the appropriate `git diff` command to get the changeset. If the diff is empty, tell the user and ask them to clarify

---

## Phase 2: Parallel Review

Capture the changeset (diff output or file contents) from Phase 1 as `codeContent`. Then read [references/agent-prompts.md](references/agent-prompts.md) and launch the 3 `code-reviewer` agents in **parallel**, substituting `<scope-description>` and `${codeContent}` in each prompt.

The three agents cover: **simplicity/DRY**, **bugs/correctness**, **conventions/abstractions**.

---

## Phase 3: Consolidate & Report

Once all three agents have returned:

1. **Deduplicate**: If multiple agents flagged the same issue, merge them into one finding and note that multiple reviewers caught it (this increases its priority)
2. **Classify severity**:
   - **Critical** — Bugs, security vulnerabilities, data loss risks, or anything that will break in production
   - **Important** — Convention violations, missing tests, DRY issues, or patterns that will cause maintenance pain
   - **Minor** — Style nits, minor simplification opportunities (include only if the list is short)
3. **Sort** by severity (critical first), then by how many reviewers flagged it
4. **Present** the consolidated report using this format:

```
## Code Review Summary

Reviewed: <scope description>
Reviewers: simplicity/DRY, bugs/correctness, conventions/abstractions

### Critical (X issues)

**1. [Short title]** — `path/to/file.ts:42`
[Description of the issue]
Flagged by: bugs/correctness, conventions
Suggested fix: [concrete suggestion]

### Important (X issues)
...

### Minor (X issues)
...

### What looks good
[Brief note on things the reviewers found well-done — balanced feedback matters]
```

5. If no high-confidence issues were found across any dimension, confirm the code looks good with a brief summary of what was checked

---
