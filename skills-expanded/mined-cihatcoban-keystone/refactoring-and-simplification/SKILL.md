---
name: refactoring-and-simplification
description: Improves structure without changing behavior, including legacy code with no tests - characterization tests, seams, strangler fig. Triggers - clean this module up, this legacy code has no tests and I need to change it, reduce the complexity, refactor, simplify.
---

# Refactoring and Simplification

Refactoring changes structure while preserving behavior **exactly**. The moment
behavior changes, it is not refactoring — it is a rewrite wearing a refactor's
clothes, and it will be reviewed as if nothing could break.

Simplification is not "fewer lines". It is: would a competent engineer new to
this code understand it faster than before? Compressed clever code fails that
test routinely.

## Precondition: a safety net

Never refactor code you cannot verify. The order is fixed:

1. **Tests exist and pass** → refactor freely.
2. **No tests** → write **characterization tests** first. Do not aim for
   correctness; capture *current* behavior, including behavior that looks
   wrong. Run the code, record what it produces, assert that. Now you have a
   net. Fixing the wrong behavior is a separate, later change with its own test.
3. **Cannot test it at all** (no seam, global state, hardcoded dependency) →
   create a seam first with the smallest possible edit: extract a function,
   parameterize a dependency, wrap the call. Verify manually, commit that alone,
   then proceed.

## Working method

- **Small steps, green between each.** Extract, run, commit. A refactor that
  spends 40 minutes red is a rewrite, and it will be abandoned or forced
  through.
- **Structural and behavioral changes never mix in one commit.** This is the
  single most important rule for reviewability: a diff that moves code *and*
  changes it cannot be reviewed, only trusted.
- **Automated refactorings first.** IDE rename/extract/inline are verified
  transformations; hand-editing the same change introduces typos.
- **Mikado method for tangles**: attempt the change; when it breaks something,
  note the prerequisite, revert, do the prerequisite first. You get a dependency
  tree of small safe steps instead of one enormous unlandable branch.

## What to fix, in priority order

| Smell | Why it matters | Move |
|---|---|---|
| Long function doing several things | Cannot be named, tested or reused | Extract by responsibility, not by line count |
| Deep nesting | Every level is a branch the reader must hold | Guard clauses, early return |
| Boolean parameter changing behavior | Two functions hiding in one | Split them |
| Duplicated **knowledge** | Divergence produces silent inconsistency | Unify — but only real duplication |
| Coincidental duplication | Looks alike, changes for different reasons | **Leave it.** Wrong abstraction costs more than duplication |
| Primitive obsession | Nothing prevents passing the wrong string | Introduce a value type |
| Comment explaining *what* | The code should say it | Rename, extract; keep comments for *why* |
| Dead code | Reader assumes it matters | Delete. Version control remembers |
| Stale TODO | Becomes wallpaper | Convert to an issue or delete |

**The duplication trap:** "don't repeat yourself" is about knowledge, not
characters. Two functions that look identical but serve different rules will
need to diverge; unifying them creates a parameterized monster. Prefer waiting
for the third occurrence before abstracting.

## Large-scale: strangler fig

Replacing a big component in one cut fails predictably. Instead:

1. Put a seam in front of the old component (facade, router, adapter).
2. Implement one capability behind the new implementation.
3. Route that capability's traffic to the new path — ideally shadowing first,
   comparing outputs.
4. Repeat capability by capability.
5. Delete the old component when nothing routes to it.

At every point the system works and you can stop. That property is the point:
rewrites fail because they are all-or-nothing bets on an estimate.

## When not to refactor

- Code that works, is never read, and is never modified. Ugly and stable is
  cheaper than churn.
- Immediately before a deadline-critical release — the risk is not free.
- In the same PR as a feature — the review cannot separate the two.
- Because it is not your style. "I would have written it differently" is not a
  defect. Follow the project's conventions.

## Exit checklist

- [ ] Behavior is provably unchanged: same tests, green before and after
- [ ] Characterization tests written first where none existed
- [ ] No behavioral change hidden in a structural commit
- [ ] Each step was committed green
- [ ] Complexity actually decreased (fewer branches, shallower nesting), not
      just moved elsewhere
- [ ] Only real duplication removed; coincidental duplication left alone
- [ ] Dead code deleted rather than commented out
- [ ] The result is easier for a newcomer to read, not merely shorter
