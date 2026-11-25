---
name: cr-refactor-boundaries
description: Refactoring boundary preferences for normal feature and bug-fix work. Use when deciding how much surrounding code to change, clean up, rename, move, or restructure.
---

# Refactor Boundaries

Use these defaults unless the user explicitly asks for a broader cleanup.

## Default Scope

- Keep diffs scoped to the request unless broader cleanup is explicitly needed.
- Keep changes focused on the requested task.
- Touch nearby code only when it directly improves readability, correctness, or maintainability of the requested change.
- Prefer targeted edits over broad cleanup passes.

## What Is Usually OK

- Small cleanup in the same file while implementing the requested change.
- Tightening names or structure when it makes the modified code easier to understand.
- Removing obviously dead local code discovered in the touched area.
- Fixing small inconsistencies that are directly adjacent to the change.

## What To Avoid By Default

- Do not refactor unrelated files just because they could be improved.
- Do not introduce new abstractions during feature work unless they are clearly justified by the change.
- Do not perform sweeping renames, file moves, or architecture cleanup unless asked.
- Do not convert existing patterns to a new style across the codebase as part of a small task.
- Do not expand scope from implementation into design-system or infrastructure work unless the task actually calls for it.

## Abstraction Guardrails

- A little duplication is often better than introducing a premature shared helper.
- If an abstraction only helps the current change a little, keep the logic local.
- Extract only when reuse is real, the concept is clearly distinct, or the main code becomes meaningfully easier to follow.

## Existing Code Quality

- Respect local conventions unless they are actively blocking a clean implementation.
- Improve messy code incrementally, not ideologically.
- Preserve public APIs and established behavior unless a change is required.

## When To Escalate

Pause and ask before doing broader refactors such as:

- moving code across feature boundaries,
- redesigning component APIs,
- changing shared helpers used in many places,
- renaming public exports,
- replacing existing patterns project-wide.

## Examples

### Usually OK: small adjacent cleanup

```ts
export const formatUsd = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};
```

If touching this file already, simplifying an obvious local implementation is fine.

### Usually avoid: unrelated abstraction during feature work

```ts
// Asked: add a status badge to invoices page
// Avoid: extracting a new cross-app status helpers module
// unless the task actually justifies it.
```

### Usually avoid: broad cleanup from a narrow request

```ts
// Asked: fix one modal action
// Avoid: renaming modal props across the whole app,
// moving files, and rewriting related hooks in the same task.
```

### Escalate first when scope expands

```ts
// This change now requires redesigning a shared component API.
// Pause and ask before continuing with the broader refactor.
```

## Output Checklist

Before finishing, check:

- Did I stay focused on the requested task?
- Did I avoid broad cleanup unrelated to the change?
- Are any abstractions I introduced clearly justified?
- Would the diff feel appropriately scoped to the request?
- Did I preserve behavior and public surfaces unless change was necessary?
