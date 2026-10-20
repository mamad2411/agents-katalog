---
name: sloth-blueprint
description: "Use when an approved Maycrest spec needs turning into a bite-sized TDD implementation plan a contractor could execute cold — before any code is touched on a client build."
---

# Sloth Blueprint — From Approved Spec to Executable Plan 🦥

## Overview

Take an approved spec and write an implementation plan a contractor with zero context for
our codebase could execute. Document everything: which files to touch per task, the actual
code, how to test it, what passing looks like. Whole plan as bite-sized tasks. DRY. YAGNI.
TDD. Frequent commits.

Assume a skilled developer who knows almost nothing about our stack or the client's domain,
and who doesn't know our test design conventions. Spell it out.

**Announce at start:** "I'm using sloth-blueprint to write the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md` (client/Corey preference overrides).

## Scope Check

If the spec covers multiple independent subsystems, it should have been decomposed during
[sloth-spec](../sloth-spec/SKILL.md). If it wasn't, suggest splitting into separate plans —
one per subsystem. Each plan must produce working, testable software on its own.

## File Structure First

Before defining tasks, map which files get created or modified and what each is responsible
for. This is where decomposition gets locked in.

- Design units with clear boundaries and one responsibility each.
- Prefer smaller, focused files. Files that change together live together — split by
  responsibility, not by technical layer.
- In existing codebases, follow established patterns; only split a file if it's grown unwieldy.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement minimal code to pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use sloth-build to implement this plan
> task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

Every task references [sloth-tdd](../sloth-tdd/SKILL.md) — failing test first, always.

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts:123-145`
- Test: `exact/path/to/file.test.ts`

- [ ] **Step 1: Write the failing test**

```typescript
test('rejects double-booking the van', async () => {
  const result = await book({ slot: taken });
  expect(result.error).toBe('Slot already booked');
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx vitest run src/booking.test.ts -t "double-booking"`
Expected: FAIL with "book is not defined"

- [ ] **Step 3: Write minimal implementation**

```typescript
export async function book({ slot }: BookInput) {
  if (await isTaken(slot)) return { error: 'Slot already booked' };
  return { ok: true };
}
```

- [ ] **Step 4: Run test to verify it passes** → Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/booking.ts src/booking.test.ts
git commit -m "feat: reject double-booking the house van"
```
````

## No Placeholders

Every step contains the actual content an engineer needs. These are **plan failures** —
never write them:

- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without the actual test code)
- "Similar to Task N" (repeat the code — tasks may be read out of order)
- Steps describing *what* without showing *how* (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Remember

- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Self-Review

After writing the full plan, check it against the spec with fresh eyes. This is a checklist
you run yourself — not a subagent dispatch.

1. **Spec coverage** — skim each spec requirement. Can you point to a task that implements it?
   List gaps; add tasks for any requirement with no home.
2. **Placeholder scan** — search for the red flags above. Fix them.
3. **Type consistency** — do types, signatures, and names in later tasks match earlier ones?
   `clearLayers()` in Task 3 and `clearFullLayers()` in Task 7 is a bug.

Fix issues inline and move on.

## Execution Handoff

After saving the plan, hand off to execution:

> "Plan complete and saved to `docs/plans/<filename>.md`. Recommended execution:
> subagent-driven via [sloth-build](../sloth-build/SKILL.md) — a fresh subagent per task with
> review between tasks. Ready to start?"

## Integration with the Maycrest roster

- Input comes from [sloth-spec](../sloth-spec/SKILL.md); never plan against an unapproved spec.
- Every task is built around [sloth-tdd](../sloth-tdd/SKILL.md).
- Execution runs through [sloth-build](../sloth-build/SKILL.md), dispatching `maycrest-automate` specialists.
- Final readiness is certified by [sloth-verify](../sloth-verify/SKILL.md) and `maycrest-ops:reality-checker`.

---
*Adapted from the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers) project (© 2025 Jesse Vincent). See [NOTICE](../../NOTICE).*
