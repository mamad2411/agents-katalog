---
name: code-smell-detection
description: Scans a diff or folder for long methods, feature envy and god classes, and proposes the smallest change that removes each smell. It reports before editing.
---

# Code smell detection

Look at changed code first; scan the rest only if asked. Report evidence, not taste.

## Steps

1. Get the scope: `git diff main...HEAD --stat` for a branch, or the folder the user named. Read each changed file in full.
2. Check for these, with the threshold that makes each a finding:
   - Long method: over about 40 lines, or more than one level of abstraction in one body.
   - Feature envy: a method that reads another object's fields more than its own.
   - God class: many unrelated fields and methods, or a name ending in Manager or Helper that everything depends on.
   - Long parameter list: more than four, or booleans that switch behavior.
   - Shotgun surgery: one change forcing edits in many files.
   - Primitive obsession: the same string or number pair passed around with rules attached.
3. For every finding, locate the exact lines and pick the smallest fix: extract method, move method, introduce parameter object, replace flag with two functions.
4. Rank by how often the code changes (use `git log --oneline -- <file>` to count). A smell in cold code is low priority.
5. Do not edit. Present the list and ask which items to apply. Apply only the ones approved, one at a time, running tests after each.

## Rules

- Never propose a smell without a line reference.
- Do not flag style, naming or formatting.
- Behavior stays identical; if tests are missing, say so before refactoring.

## Report

A ranked list: location, smell, why it hurts here, smallest fix, estimated risk (low, medium, high).
