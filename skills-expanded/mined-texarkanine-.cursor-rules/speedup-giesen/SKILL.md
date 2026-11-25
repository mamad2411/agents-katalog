---
name: speedup-giesen
description: Audit a finished, behavior-correct codebase for work you can stop doing so it gets faster without changing what it does. Report the stupid-class findings and wait; do not edit until the operator picks which items to cut. Use when the product already works and the ask is speed, a 10x or 100x win, or whether you are doing something stupid. Not for new features, a YAGNI simplification pass, or clever micro-opts that add machinery.
---

# The Giesen Speedup

> look, I'm sorry, but the rule is simple:
> if you made something 2x faster, you might have done something smart
> if you made something 100x faster, you definitely just stopped doing something stupid
>
> — Fabian Giesen (@rygorous), 11 June 2020, https://x.com/rygorous/status/1271296834439282690

That quote is the stance. Do not unpack it into a performance textbook. Hunt wasted work, not cleverness. This pass is an audit. Fixing is a later turn, after the operator chooses which findings to cut.

## The Pass

1. Confirm the product already behaves correctly. If the ask is a new feature or a behavior change, stop — this skill does not apply.
2. Name the surfaces that must get cheaper: whatever the operator named, or else the boot or request path the user actually waits on. Do not hunt the rest of the tree.
3. Walk those surfaces for wasted work. The class looks like: the same job every tick or render, parsing more than the answer requires, a new connection per request, rebuilding what is already in hand, destroying work before the replacement exists. Those are examples of the class, not a checklist to exhaust.
4. Classify each candidate. Stopping it is something stupid (the 100× class) or something smart (the 2× class: a new cache layer, a clever algorithm, an architecture rewrite). Keep the first on the report. Leave the second off unless the operator asked for clever.
5. Report the stupid-class findings as a numbered list. Each item names the surface, the wasted work, why it is the 100× class, and what you would stop doing. If you only found 2×-smart candidates, report those and stop. Do not edit the product. Do not edit tests.
6. Stop and wait. The operator may strike items that look like waste but are load-bearing. Do not apply cuts until they name which findings to fix. Do not start When fixing in the same turn as the report.

## When fixing

Only after the operator has named which findings to cut.

1. Apply only those named stupid-class cuts. Observable behavior stays. Do not add machinery to go faster.
2. Change tests only if the speedup can be wrong in a way the old suite would still pass. Then add the smallest test that fails when that shortcut is wrong, not a test of the new internals. Reusing a result that then goes stale - where before, the result was computed fresh each time - is one such hole.
3. Verify behavior still holds. Report what you stopped doing and which class of speedup it is. When you can time the named surface, put the observed multiplier next to the class label.
