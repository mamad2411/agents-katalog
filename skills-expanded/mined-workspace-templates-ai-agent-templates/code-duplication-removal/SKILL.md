---
name: code-duplication-removal
description: Detects copy-pasted blocks and merges them into one abstraction only when the copies change together, leaving look-alikes that evolve apart untouched.
---

# Code duplication removal

Merge copies that share a reason to change. Leave the rest.

## Steps

1. Detect candidates with a tool if the project has one (`npx jscpd`, `pmd cpd`, or the linter's duplicate rule); otherwise search for repeated distinctive lines with grep. Ignore generated files, tests and migrations unless asked.
2. For each pair or group, read all copies side by side. Write down exactly what differs: constants, types, one branch, a name.
3. Check how they evolved: `git log -L<start>,<end>:<file>` or `git log --oneline -- <file>` for each copy. If a past fix was applied to all copies together, they change together. If they were edited at different times for different reasons, they only look alike.
4. Decide with this rule: merge when copies change together and the differences can be expressed as parameters without adding more than two flags. Wait (the rule of three) when there are only two copies and the intent is unclear. Leave alone when the copies belong to different features, even if the code is the same today.
5. When merging, extract the shared part into a function or component with a name from the domain, pass the differences as arguments or callbacks, and put it where both callers can import it without a cycle.
6. Replace one copy at a time and run the tests after each. If tests do not cover them, add one per copy first.
7. Delete nothing until all callers use the shared version.

## Rules

- No boolean flag parameters that switch behavior; make two functions.
- No shared helper with more than four parameters; reconsider the split.
- Do not touch public signatures in the same change.

## Report

Groups found, which were merged and which left apart with the reason, lines removed and tests run.
