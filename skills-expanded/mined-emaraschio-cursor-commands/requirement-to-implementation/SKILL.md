---
name: requirement-to-implementation
description: Structured workflow for taking a requirement (feature, bug, refactor, chore, or performance task) from any source (Notion, GitHub, conversation) through planning, approval, implementation, verification, and documentation. Use when the user provides a requirement, task, ticket, or asks to implement something.
user-invocable: false
---
# Requirement to Implementation

Structured workflow that turns a requirement into verified, documented code. Every task (feature, bug fix, refactor, chore, or performance improvement) flows through the same phases.

## Phase 0: Intake

Identify the requirement source and extract key information.

| Source | Action |
|--------|--------|
| **Notion ticket** | Use Notion MCP to fetch ticket details, acceptance criteria, and linked context |
| **GitHub issue** | Use `gh issue view` to pull title, body, labels, and linked PRs |
| **Conversation** | Extract the requirement from what the user described |
| **Sentry issue** | Use Sentry MCP to pull error details, stack traces, and affected users |

Produce a one-paragraph **requirement summary** confirming your understanding. Ask the user about literally anything:technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious, be very in-depth and continue interviewing me continually until it's complete, then write the plan to the file.

## Phase 1: Context Loading

Read the Memory Bank to ground yourself in project state:

1. `.cursor/memory-bank/projectbrief.md`: scope and goals
2. `.cursor/memory-bank/productContext.md`: product context
3. `.cursor/memory-bank/techContext.md`: tech stack and constraints
4. `.cursor/memory-bank/systemPatterns.md`: architecture and patterns
5. `.cursor/user-memory-bank/activeContext.md`: current focus
6. `.cursor/user-memory-bank/progress.md`: what's done, what's pending

If any file is missing or stale, note it; you'll update them in Phase 5.

## Phase 2: Exploration & Analysis

Explore the codebase to map the blast radius of the change:

1. **Identify affected files**: entry points, services, APIs, jobs, UI, tests
2. **Read existing patterns**: find similar implementations to follow
3. **Spot risks**: PII/sensitive data exposure, authorization gaps, integration side effects, migration needs
4. **Note test coverage**: existing tests that need updating, gaps that need filling

Use exploratory subagents for broad investigations. Use targeted searches for specific lookups.

## Phase 3: Plan & Approve

Present a structured plan to the user. **Do not implement until approved.**

### Plan Template

```text/markdown
## Requirement
[One-sentence summary]

## Approach
[High-level description of the solution]

## Changes
1. [File/area]: [what changes and why]
2. [File/area]: [what changes and why]
...

## Verification Strategy
- [ ] [How you'll verify correctness (tests, manual checks, etc.)]
- [ ] [Specific test files to create or update]

## Risks & Considerations
- [Anything the user should be aware of]

## Questions (if any)
- [Clarifying questions that surfaced during exploration]
```

Ask **4-6 clarifying questions** if ambiguities remain. Wait for answers before finalizing the plan.

Once the user approves, proceed to implementation.

## Phase 4: Implement

1. **Create a TodoWrite task list** mirroring the approved plan's changes
2. **Mark each todo `in_progress`** as you begin it, `completed` when done
3. **Work step by step**: one todo at a time, verifying as you go

### Verification (flexible per task)

Choose the verification approach that fits:

| Task Type | Approach |
|-----------|----------|
| **Bug fix** | Write a failing test first, then fix, then verify it passes |
| **New feature** | Implement, then write specs covering happy path + edge cases |
| **Refactor** | Ensure existing specs still pass, add specs for new behavior |
| **Performance** | Benchmark before/after, verify no regression in specs |
| **Chore** | Verify with linter, specs, or manual confirmation as appropriate |

After each meaningful change, run the project's test command for affected paths (for example `npm test`, `pytest`, `go test ./...`, `bundle exec rspec`; use what the host repo documents). Fix failures before moving on.

### Implementation Principles

- Follow existing patterns found in Phase 2
- One concern per change: don't mix unrelated modifications
- Check lints after substantive edits
- If a step reveals the plan was wrong, **stop and re-plan** with the user

## Phase 5: Document

After implementation is complete and verified:

1. **Update `.cursor/user-memory-bank/activeContext.md`**: reflect current focus and recent changes
2. **Update `.cursor/user-memory-bank/progress.md`**: mark what's done, note what's next
3. **Update `.cursor/memory-bank/systemPatterns.md`**: if new patterns were introduced
4. **Update `.cursor/memory-bank/techContext.md`**: if tech stack or constraints changed

## Quick Reference: Phase Flow

```text/markdown
Intake → Context → Explore → Plan → [Approve] → Implement → Document
  ↑                            ↓
  └──── Re-plan if needed ─────┘
```

**Cardinal rule**: No implementation without an approved plan. Plans are cheap; rework is expensive.

## Guardrails

- No implementation without an approved plan: present the plan and wait for explicit approval before writing production code.
- Do not skip intake or exploration on an ambiguous requirement; map the blast radius first.
- Commit or push only on explicit user request; never print or commit secrets.
