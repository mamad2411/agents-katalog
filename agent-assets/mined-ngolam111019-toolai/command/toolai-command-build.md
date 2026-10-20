---
name: build
description: Implement tasks incrementally using TDD and vertical slices
---

# /build — Incremental Implementation

> "The simplest thing that could work."

## Purpose

Implement tasks one at a time using Test-Driven Development. Each increment leaves the system in a working, testable state.

## Prerequisites

- A plan exists (`tasks/todo.md`)
- Understanding of task acceptance criteria

## Workflow

### For Each Task

#### Step 1: Load Context

```
1. Read the task's acceptance criteria
2. Identify relevant existing code and patterns
3. Understand types and interfaces involved
```

#### Step 2: RED — Write Failing Test

```javascript
// Write a test that describes expected behavior
// This test MUST fail initially

describe('createTask', () => {
  it('should create a task with title and return id', async () => {
    const result = await createTask({ title: 'Test' });
    expect(result.id).toBeDefined();
    expect(result.title).toBe('Test');
  });
});
```

Run test — confirm it **fails**.

#### Step 3: GREEN — Minimal Implementation

```javascript
// Write the MINIMUM code to pass the test
// No extra features, no premature optimization

async function createTask({ title }) {
  const task = await db.task.create({ data: { title } });
  return task;
}
```

Run test — confirm it **passes**.

#### Step 4: REFACTOR — Improve Code Quality

```javascript
// Clean up while keeping tests green
// - Improve naming
// - Extract helpers if needed
// - Remove duplication
```

Run tests — confirm they **still pass**.

#### Step 5: Verify & Commit

```bash
# Run full test suite
npm test

# Run build
npm run build

# Commit with clear message
git add .
git commit -m "feat(tasks): add createTask function"
```

#### Step 6: Mark Complete

Update `tasks/todo.md`:
```markdown
- [x] Task 1.1: Create task endpoint
```

### Rules

| Rule | Why |
|------|-----|
| **100-line limit** | Test before writing more than ~100 lines |
| **Touch only what's needed** | Don't refactor adjacent code |
| **Keep it building** | Project must compile after each increment |
| **Feature flags** | Use flags for incomplete features that need merging |
| **Rollback-friendly** | Each increment should be independently revertable |

### When Stuck

If a step fails:

1. **Stop** — Don't push through broken code
2. **Diagnose** — Use `/debug` to find root cause
3. **Fix** — Address the actual problem
4. **Guard** — Add test to prevent recurrence
5. **Resume** — Continue from where you stopped

## Red Flags

Stop and reassess if you find yourself:

- Writing > 100 lines without testing
- Mixing unrelated changes in one commit
- Expanding scope mid-task
- Breaking the build between increments
- Creating abstractions "for later"

## Output

- Working, tested code
- Updated `tasks/todo.md` with completed items
- Clean git history with atomic commits

## Next Step

After all tasks complete, run `/review` for final quality check.
