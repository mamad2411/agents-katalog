---
name: walking-skeleton-plan
description: Turns an approved spec into docs/SLUG-plan.md. Step 1 is a walking skeleton (the main path working end to end with the minimum in each layer), and every later step adds exactly one capability, stays integrated, leaves no orphan code and says what can be tested when it is done. Use it whenever the user asks for an implementation plan, a roadmap, incremental steps, a walking skeleton, vertical slices, or "how would you build this", once a spec or clear requirements exist.
---

# Walking skeleton plan

## Principles

- **Step 1 is a walking skeleton.** It runs the main path of the spec end to end: for example "a customer places an order, the system stores it and the order list shows it". Each layer that the main path crosses has the minimum (for example data, logic, interface, tests). It stays in the codebase as the base.
- **One capability per step.** A step adds one thing: cancel an order, validation, edit, delete, a config option.
- **Always integrated.** At the end of every step the project builds, the main path works and the full test suite passes.
- **No orphan code.** Every function, table, dependency and template added in a step has a caller in that same step.
- **Testable.** Every step says what can be tested when it is done: automated tests and one manual check.
- **One feature.** A step is not a feature. The whole plan runs on the branch of the feature (`git-commit-organizer`), with commits per step.

## Ordering

1. Walking skeleton first.
2. Next, anything that changes the shape of every later step. Example: the error format of the API before the first endpoints that return errors, so every later endpoint uses it from the start and tests are adapted once.
3. Then features, one per step.
4. Then hardening that does not change the public interface (for example limits, security settings, configuration).
5. Styles and final documentation review last.

State the ordering decisions in the plan so the user can challenge them.

## Output

`docs/<slug>-plan.md`, in the document language of `simplified-technical-language`:

```markdown
# <Feature> Implementation Plan

| | |
| --- | --- |
| Spec | [<slug>-spec.md](<slug>-spec.md) |
| Branch | `<branch>` |

## Overview           table: step | name | acceptance criteria covered
## Steps
### Step 1 - Walking skeleton
**Adds:** …
**Can be tested when done:** …
```

## Coverage check

Every acceptance criterion must appear in the overview at least once. Check it with a script, not by eye:

```bash
for i in $(seq 1 NN); do
  id=$(printf 'AC-%02d' "$i")   # use the id form of the spec
  grep -q "$id" <(sed -n '/^## Overview/,/^## Steps/p' docs/<slug>-plan.md) || echo "missing $id"
done
```

Mark criteria that a step covers only partly, and name the step that completes them.

## Finish

Commit the plan (`git-commit-organizer`). In the chat, show the step list grouped by phase and the ordering decisions. Offer `work-items-breakdown` if the user tracks work in a tool. Ask before you start `execute-plan-loop`.
