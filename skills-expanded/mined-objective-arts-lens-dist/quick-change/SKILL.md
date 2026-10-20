---
name: quick-change
description: Simple changes done right. Make the change, clean up after yourself, report what happened.
---

# /quick-change [description]

For simple changes that don't warrant full planning — with a built-in cleanup pass.

> **No arguments?** Describe this skill and stop. Do not execute.

## What Is This?

`/quick-change` is the **light workflow**: make a small change carefully, then clean up what you wrote. One command instead of two.

Use this when:
- Add a field to a model/DTO
- Rename something
- Add a parameter
- Small bug fix
- Add a button/link
- Update a constant

**If the change touches 5+ files or has design decisions → use `/build` or `/improve` instead.**

## Canon Skills (Auto-Invoke)

### Always Active

| Skill | Why |
|-------|-----|
| `/clarity` | Kernighan - naming, simplicity |
| `/refactoring` | Fowler - safe small changes |
| `/style` | Google - match existing patterns |

### By Change Type

| Change Type | Invoke | Why |
|-------------|--------|-----|
| Rename | `/clarity` | Kernighan naming principles |
| Bug fix | `/legacy` | Feathers' characterization before change |
| Validation | `/owasp` | Input validation is security |
| Database | `/sql` | Celko's column design |

### By Language

**TypeScript/JavaScript:**
| Pattern | Invoke |
|---------|--------|
| `*.ts`, `*.tsx` | `/typescript`, `/cherny` |
| `*.js`, `*.jsx` | `/js-safety`, `/crockford` |
| `*.spec.ts`, `*.test.ts` | `/dodds`, `/test-doubles` |

**Java:**
| Pattern | Invoke |
|---------|--------|
| `*.java` | `/java` (Bloch's field/API design) |
| `*Test.java` | `/test-doubles` |

**Python:**
| Pattern | Invoke |
|---------|--------|
| `*.py` | `/python-idioms`, `/python-patterns` |
| `test_*.py` | `/test-doubles` |

**C#:**
| Pattern | Invoke |
|---------|--------|
| `*.cs` | `/csharp-depth` |

**Go:**
| Pattern | Invoke |
|---------|--------|
| `*.go` | `/simplicity` (Pike's Go proverbs) |

---

## Process

### Step 1: Understand

Read the existing code around the change. Check how similar things are done nearby.

### Step 2: Make the Change

Follow existing patterns. Complete the circuit — if you add a field, update everywhere it matters.

### Step 3: Verify Checklist

Run the checklist for your change type (see below). Don't skip items.

### Step 4: Clean What You Wrote

Review every file you just touched against the cleanup tables below. Fix issues inline — don't leave them for a separate pass.

### Step 5: Build + Test

Confirm build passes and tests pass.

### Step 6: Report

List what was changed and what was cleaned.

---

## Checklists (Step 3)

### For Adding a Field/Property

- [ ] Added to model/entity
- [ ] Added to DTO (if separate)
- [ ] Added to API request/response
- [ ] Added to UI form (if user-facing)
- [ ] Added to UI display (if displayed)
- [ ] Added to validation
- [ ] Added to tests
- [ ] Added to any mappings/transformers
- [ ] Database migration (if persisted)

### For Renaming

- [ ] Renamed in definition
- [ ] Renamed in ALL usages (grep to verify)
- [ ] Renamed in tests
- [ ] Renamed in comments/docs
- [ ] API backwards compatibility considered

### For Adding a Parameter

- [ ] Added to function signature
- [ ] Updated all call sites
- [ ] Updated tests
- [ ] Updated docs/JSDoc
- [ ] Default value if appropriate

### For Bug Fix

- [ ] Root cause identified (not just symptom)
- [ ] Fix is minimal (not refactoring in disguise)
- [ ] Test added to prevent regression
- [ ] Related code checked for same bug

---

## Cleanup Tables (Step 4)

### AI-Generated Antipatterns

| Smell | What to Look For | Fix |
|-------|------------------|-----|
| Over-abstraction | Factory/Builder/Wrapper used only once | Inline it |
| Defensive paranoia | `if (x != null)` when x can never be null | Remove check |
| Reimplementing stdlib | Custom `deepClone`, `isEmpty`, `capitalize` | Use library |
| Comment spam | `// loop through users` above `for...of` | Delete comment |
| Speculative features | Config option with only one value used | Remove option |
| Enterprise naming | `AbstractUserFactoryManager` | Simplify name |
| Wrapper classes | Class that just delegates to another | Inline or remove |
| Unused parameters | `function foo(a, b, c)` but `c` never used | Remove parameter |
| Over-generic types | `Result<T, E, M, C>` for simple return | Simplify type |

### Common Problems

| Problem | Threshold | Fix |
|---------|-----------|-----|
| Vague names | `data`, `result`, `temp`, `item`, `info` | Rename to intent |
| Magic numbers | Hardcoded values | Extract to constant |
| Dead code | Unused imports, unreachable code | Delete |
| Redundant code | Duplicate logic | Extract or remove |

### Naming Smells

| Smell | Example | Fix |
|-------|---------|-----|
| Generic -er | `Processor`, `Handler`, `Manager` | Name for what it does |
| Impl suffix | `UserServiceImpl` | `UserService` if only one |
| I- prefix | `IUserService` | `UserService` (TS isn't C#) |
| Type in name | `userString`, `countInt` | `user`, `count` |
| Negative booleans | `isNotValid`, `hasNoErrors` | `isValid`, `hasErrors` |

### Self-Test Questions

1. **Would I mass-delete this in code review?** → Delete it
2. **Does this abstraction have more than one use?** → If no, inline it
3. **Would a new team member understand this name?** → If no, rename it
4. **Is this check possible to fail?** → If no, remove it
5. **Did I write this or did I request it?** → If not requested, remove it

---

## Output Format

```markdown
## Quick Change: [description]

CHANGE_TYPE: [add-field | rename | add-param | bug-fix | other]

### Changed

| File:Line | What Changed |
|-----------|-------------|
| src/user.ts:12 | Added `email` field to User model |
| src/user.dto.ts:8 | Added `email` to UserDTO |

### Checklist

- [x] Model updated
- [x] DTO updated
- [x] Tests updated
- [ ] N/A: No UI for this field

### Cleaned

| File:Line | Issue | What Was Done |
|-----------|-------|---------------|
| src/user.ts:45 | Defensive paranoia | Removed null check on required field |
| src/user.ts:23 | Comment spam | Deleted `// Get the user` above `getUser()` |

### Summary

| | Count |
|---|-------|
| Files changed | N |
| Checklist items | N/N |
| Issues cleaned | N |

BUILD: pass
TESTS: pass

QUICK_CHANGE_COMPLETE
```

## What NOT to Fix

Leave these for dedicated skills:

| Issue | Use Instead |
|-------|-------------|
| Long functions (>30 lines) | `/improve` |
| Deep nesting (>3 levels) | `/improve` |
| Complex refactoring | `/improve` |
| Security issues | `/security-review` |
| Static analysis | `/qodana-review` |

## Common Mistakes to Avoid

| Mistake | Example | Do This Instead |
|---------|---------|-----------------|
| Incomplete circuit | Added field to model, forgot DTO | Grep for the type name, update all |
| Inconsistent naming | `user_name` in DB, `userName` in code, `name` in UI | Match existing pattern exactly |
| Speculative additions | "Added createdAt while I was there" | Only what was requested |
| Missing validation | Added `email` field with no format check | Add validation if the field has constraints |
| No test | "It's just a field" | Add test, especially for validation |

## When to Escalate

Use `/build` or `/improve` instead if:
- You're touching 5+ files
- There are design decisions to make
- You're unsure about the right approach
- The "simple" change is revealing complexity

## vs Other Workflows

| Workflow | When to Use | Overhead |
|----------|-------------|----------|
| `/build` | New feature from scratch | Full pipeline |
| `/improve` | Refine existing code | Full pipeline |
| `/quick-change` | Add field, rename, small fix | Light (checklist + cleanup) |
