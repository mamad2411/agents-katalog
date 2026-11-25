---
name: code-review
description: Review a change (a diff, a branch or a pull request) for correctness, risk and clarity. Use when asked to review code or to check work before it is merged.
---

# Code review

Review the change the way a careful colleague would, and report what you find in order of
importance.

## Steps

1. Find out what the change is for: the description, the linked issue, or the commit messages.
   If its purpose is unclear, say so first.
2. Read the whole diff, then read the code around it. A line that looks fine alone can break
   a caller you have not seen.
3. Check, in this order:
   - **Correctness.** Does it do what it claims? Look at edge cases: empty input, errors,
     concurrency, and the first and last item.
   - **Risk.** Security, data loss, migrations, public interfaces and anything that is hard
     to undo.
   - **Tests.** Do they fail without the change? Do they cover the edge cases above?
   - **Clarity.** Names, structure, and comments that explain why.
4. Run the project's tests and checks if you can, and say what you ran.

## How to report

- Start with a one-line verdict: ready, ready after small fixes, or needs rework.
- List problems from most to least serious. For each, give the file and line, what is wrong,
  and a suggested fix.
- Keep suggestions of taste apart from real problems, and label them as such.
- Say what you did not check.
- Do not edit the code under review unless you were asked to.
