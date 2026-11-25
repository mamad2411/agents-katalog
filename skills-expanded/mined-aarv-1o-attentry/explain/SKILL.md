---
name: explain
description: Explain one Attentry finding in full and how to fix it. Use when the person gives a file:line from Attentry, or asks why Attentry flagged something.
argument-hint: <file:line>
---

Call Attentry's `explain` tool with the location the person gave ($ARGUMENTS), as `file:line`.
It answers with what the code does, what can go wrong, and the steps to fix and check it.

Pass that on in plain words, then offer to make the fix. If there's no finding at that line,
the answer lists the lines in that file that do have findings: ask which one they meant.
