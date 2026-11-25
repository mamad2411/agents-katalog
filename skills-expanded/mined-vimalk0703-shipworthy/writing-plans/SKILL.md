---
name: writing-plans
description: Creates bite-sized (2-5 min) implementation plans with TDD flow, quality gate checkpoints, security considerations, and performance impact notes. Plans reference architecture.md constraints.
invoke_when: Use when writing an implementation plan after brainstorming is approved, or breaking down a large task into manageable steps before coding begins.
---

# Writing Plans

## Purpose

Transform an approved design into a sequence of small, verifiable tasks that follow TDD discipline.

## Plan Structure

Save plans to `.shipworthy/plans/[feature-name].md`.

### Header
```markdown
# Implementation Plan: [Feature Name]
**Design Spec**: [link to spec]
**Architecture Constraints**: [relevant Mandatory Rules from architecture.md]
**Date**: [YYYY-MM-DD]
```

### File Map
Before defining tasks, list every file that will be created or modified:
```markdown
## File Map
- `src/services/user-service.ts` — NEW: user service logic
- `src/routes/users.ts` — MODIFY: add new endpoints
- `src/types/user.ts` — MODIFY: add new types
- `tests/services/user-service.test.ts` — NEW: service tests
```

### Tasks
Each task follows TDD flow and takes 2-5 minutes:

```markdown
## Task 1: [Descriptive Name]
**Files**: [exact paths]
**Test first**: [the test to write, with actual code — not pseudocode]
**Implementation**: [the code to write — actual code, not descriptions]
**Verification**: [command to run: `npm test`, `npm run build`, etc.]
**Quality gate**: [what proves this task is done]
```

### Rules for Tasks
1. **Zero placeholders** — every task has actual code, not "implement the logic here"
2. **2-5 minutes each** — if a task takes longer, break it down further
3. **TDD flow** — test first, then implementation, then verification
4. **One responsibility** — each file should have one clear purpose (SOLID)
5. **Atomic commits** — each task should be committable independently
6. **Consistent naming** — type/method names must be consistent across ALL tasks
7. **Architecture compliance** — every task must reference which architecture rules it satisfies

### Security & Performance Sections
```markdown
## Security Considerations
- [What input validation is needed?]
- [What authentication/authorization applies?]
- [Any sensitive data handling?]

## Performance Impact
- [New database queries introduced?]
- [Bundle size impact?]
- [API response time expectations?]
```

## Task Tracking Integration

After writing the plan, use Claude Code's Task system to make progress visible:

1. **Create a Task for each plan task** using `TaskCreate` — the subject should match the task name from the plan (e.g., "Task 1: Create user service with validation")
2. **Set dependencies** if tasks must run in order — use `addBlockedBy` so the task list reflects the execution sequence
3. Tasks appear in the Claude Code UI, giving the user real-time progress visibility

This is especially valuable for Builder-tier users who want to see momentum without reading implementation details.

## Presenting the Plan

After writing the plan:
1. Show the user the task list with file map
2. Highlight any architecture constraints that influenced the plan
3. Ask: "Ready to start executing? I'll follow TDD for each task."

<HARD-GATE>
DO NOT invoke `executing-plans` or begin any implementation until your human partner has explicitly approved the plan.
Acceptable approval signals: "looks good", "approved", "go ahead", "yes", "proceed", "let's do it", "start", or similar affirmative.
NOT acceptable: silence, "hmm", "interesting", "okay" (too ambiguous), or no response. If unclear, ASK: "I have the plan ready. Should I start executing it?"
The plan is a CONTRACT. Once approved, both you and your human partner agree on what will be built.
</HARD-GATE>

4. On approval, invoke `executing-plans` skill

---

## Rationalization Pressure Test

These are excuses you might generate to skip writing a plan. Each one is wrong.

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|---------------|-------------------|
| "This feature is straightforward enough to just build" | "Straightforward" features still have hidden dependencies, edge cases, and ordering concerns | Write a lightweight plan. Even 5 bullet points prevent wrong-order implementation |
| "Planning slows us down" | Rework from no plan is 3-10x slower than the plan itself | A 5-minute plan saves a 2-hour rewrite. Math is math |
| "The brainstorming doc IS the plan" | A brainstorming doc captures WHAT to build. A plan captures HOW and IN WHAT ORDER | Convert the design into sequenced, testable tasks |
| "I'll keep the plan in my head" | Context windows are finite. You will lose track of what's done vs. what's left | Write it down. `.shipworthy/plans/` exists for this reason |
| "The user wants to see code, not documents" | The user wants working code. Plans produce working code faster than winging it | Write the plan quickly, show the task list, start executing |
| "This is only 2-3 files" | File count is not complexity. A 2-file payment integration needs a plan | If it touches money, auth, or data: plan it |
