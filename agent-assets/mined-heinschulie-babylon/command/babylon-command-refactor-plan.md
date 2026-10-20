---
allowed-tools: Read,Edit,Write,Bash,Glob,Grep,WebFetch
description: Interactive refactor planning — interviews user, explores codebase, produces a tiny-commit plan, files as GitHub issue
model: opus
---

# Purpose

Create a detailed, incremental refactor plan through a structured user interview. Explore the codebase to validate assertions, break the refactor into the smallest possible commits, and file the result as a GitHub issue. Follow the Instructions and Workflow sections below.

## Instructions

- This is an interactive, multi-turn conversation. Ask questions and wait for answers before proceeding.
- Prioritize understanding the problem deeply before proposing solutions.
- Explore the actual codebase to verify every claim the user makes about current state.
- Present alternative approaches the user may not have considered.
- Be extremely detailed and thorough during the interview phase — push back on vague answers.
- Hammer out exact scope: what changes and what does NOT change.
- Check test coverage in the affected area; flag gaps.
- Follow Martin Fowler's advice: "make each refactoring step as small as possible, so that you can always see the program working." Every commit must leave the codebase in a working state.
- Do NOT include specific file paths or code snippets in the GitHub issue — they go stale fast. Use plain English descriptions of modules and interfaces instead.
- Use `gh issue create` to file the final plan.

## Workflow

1. Ask the user for a long, detailed description of the problem and any solution ideas they have.
2. Explore the repo to verify assertions and understand current codebase state.
3. Ask whether the user has considered other options; present alternatives.
4. Interview the user about implementation details — be thorough and specific.
5. Define exact scope: what will change, what will NOT change.
6. Check test coverage in the affected area. If insufficient, ask the user about their testing plans.
7. Break the implementation into a plan of tiny commits, each leaving the codebase working.
8. Create a GitHub issue using the template below:

```
## Problem Statement
The problem from the developer's perspective.

## Solution
The agreed-upon solution from the developer's perspective.

## Commits
A LONG, detailed implementation plan in plain English. Each commit is the smallest possible step that leaves the codebase working.

## Decision Document
Implementation decisions made during the interview:
- Modules to be built/modified
- Interface changes
- Technical clarifications
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

## Testing Decisions
- What makes a good test for this refactor (test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (similar tests already in the codebase)

## Out of Scope
Things explicitly excluded from this refactor.

## Further Notes (optional)
Any additional context.
```

## Report

After filing the issue, respond with:
- The GitHub issue URL
- A one-line summary of the agreed scope
- Count of planned commits
- Any unresolved questions or risks flagged during the interview