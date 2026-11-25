---
name: scope-creep-detection
description: Use when a task is expanding beyond its original boundaries — detecting unplanned additions, feature creep, and yak-shaving that increase risk and delay delivery without explicit user approval.
invoke_when: Use when implementation is diverging from the original spec, when new requirements emerge mid-task, when refactoring is expanding beyond the targeted area, or when a "quick fix" is growing into a rewrite.
---

# Scope Creep Detection

## Core Rule

**Do what was asked. When the task grows beyond its original boundaries, stop and surface it — do not silently absorb scope.** Uncontrolled scope expansion is the primary cause of missed deadlines, introduced bugs, and abandoned features.

## What Is Scope Creep

Scope creep is the gradual expansion of a task beyond its original definition without explicit acknowledgment. It includes:

| Type | Example |
|------|---------|
| **Feature creep** | "While adding the search bar, I also added autocomplete, search history, and saved searches" |
| **Refactoring creep** | "I was fixing the bug in `auth.ts` but the code was messy so I rewrote the entire auth module" |
| **Dependency creep** | "To add this feature I need to upgrade the framework, which requires updating 12 other packages" |
| **Perfection creep** | "The function works but I want to optimize it, add better error messages, and improve the types" |
| **Yak shaving** | "To fix the login bug I need to update the test framework, which requires a new Node version, which requires..." |

## Detection Triggers

### Trigger 1: File Count Expansion

If a task was scoped to modify 1-3 files and is now touching 5+, flag it:

```
SCOPE CHECK: This task started as a change to auth.ts and auth.test.ts
but now involves 7 files across 3 directories.

Original scope: Fix login validation bug
Current scope: Fix login validation + refactor auth module + update middleware + add tests for 4 untested functions

Proceed with expanded scope, or return to the original task?
```

### Trigger 2: Time-Based Expansion

If a Quick Fix (expected: < 30 minutes of implementation) has not converged after significant effort, flag it:

```
SCOPE CHECK: This was classified as a Quick Fix but implementation
has grown substantially. This may indicate:
- The fix is more complex than expected (reclassify as Feature)
- Scope has expanded beyond the original bug
- A dependency chain is pulling in unplanned work

Recommend: Commit what works now, file follow-up tasks for the rest.
```

### Trigger 3: New Requirements Mid-Task

When the user introduces new requirements during implementation:

```
User: "Oh, and while you're in there, can you also add email notifications?"

SCOPE CHECK: Adding email notifications is a new feature, not part of
the original task (fix login validation).

Options:
1. Complete the current task first, then start email notifications as a separate task
2. Expand scope to include both (note: this changes the task from Quick Fix to Feature)
```

### Trigger 4: "While I'm Here" Syndrome

Detect opportunistic changes that were not part of the original task:

```
// Patterns that indicate scope creep:
- Renaming variables in files unrelated to the task
- Adding comments/docs to untouched functions
- Upgrading dependencies not required by the task
- Refactoring patterns in code that was only being read
- Adding error handling to functions that already work
```

### Trigger 5: Dependency Chain Expansion

When fixing one thing requires changing another, which requires changing another:

```
SCOPE CHECK: Dependency chain detected:
  Fix login bug
  → Requires updating auth middleware
  → Middleware depends on session library
  → Session library needs Node 20+
  → Node 20+ breaks 3 other test suites

This is yak shaving. Recommend: Fix the login bug with a targeted patch
that works with the current session library. File the upgrade as a separate task.
```

## Response Protocol

When scope creep is detected:

### Step 1: Identify and Announce

```
SCOPE CHECK: [Description of how scope has expanded]
Original task: [what was asked]
Current trajectory: [where this is heading]
```

### Step 2: Present Options

Always give the user a choice:

1. **Contain**: Return to original scope, file follow-ups for discovered work
2. **Expand**: Acknowledge the larger scope, reclassify the task size, proceed
3. **Split**: Complete the minimum viable change now, tackle expansions in separate tasks

### Step 3: Get Explicit Approval

Do not proceed with expanded scope without the user's explicit choice. Never assume they want more than they asked for.

### Step 4: Log the Decision

```typescript
{
  guardrailLayer: 'contextual',
  guardrailName: 'scope-creep-detection',
  severity: 'warning',
  description: 'Task expanded from 2 files to 7 files — user chose to split',
  action: 'warned',
  resolution: 'User chose option 3 (split) — completing original fix, filing follow-ups'
}
```

## Scope Boundaries by Task Size

| Task Size | Expected File Changes | Expected New Dependencies | Trigger Threshold |
|-----------|----------------------|--------------------------|-------------------|
| Quick Fix | 1-3 files | 0 | Flag at 4+ files or any new dependency |
| Feature | 3-10 files | 0-2 | Flag at 12+ files or 3+ new dependencies |
| Project | 10-30 files | 0-5 | Flag at 40+ files or 6+ new dependencies |

## Exceptions (Do Not Flag)

Some expansions are expected and should not be flagged:

- **Test files**: Adding tests for the changed code is always in scope
- **Type updates**: Updating types/interfaces that directly support the change
- **Import adjustments**: Adding/removing imports in files that use the changed code
- **Configuration**: Updating config files required by the change (tsconfig, eslint, etc.)
- **Documentation**: Updating docs that describe the changed behavior

## Rationalization Pressure Test

| Excuse | Counter |
|--------|---------|
| "It'll only take a minute" | Scope creep always "only takes a minute" — file it as a follow-up |
| "The code is already messy here" | Messy code survived this long. Fix what was asked, file the cleanup |
| "It's related to what I'm doing" | Related is not the same as required. Ship the task, then address related items |
| "The user will want this anyway" | Let the user decide what they want. Do what was asked |
| "It's a small refactor" | Small refactors introduce bugs in code that was working. Scope it separately |
| "I'm already in the file" | Being in the file is not a reason to change it beyond the task |

## Code Review Checklist

- [ ] Changes are limited to what the original task required
- [ ] No opportunistic refactoring in unrelated code
- [ ] No new features added beyond what was requested
- [ ] Dependency changes are justified by the task (not "while I'm here" upgrades)
- [ ] If scope expanded, user explicitly approved the expansion
- [ ] Follow-up tasks filed for discovered work outside original scope
