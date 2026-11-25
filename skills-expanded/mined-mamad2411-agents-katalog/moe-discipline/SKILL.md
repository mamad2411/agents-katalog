---
name: moe-discipline
description: >-
  Use during any implementation task to shape HOW you work — minimal changes,
  proportional responses, scope containment, and honest gap reporting; fires
  alongside the task itself rather than at completion time
---

# Moe Discipline

## Overview

**Core principle: do exactly what was asked, nothing more, and say what you
did not do.**

`verify-completion` fires when you are about to claim the work
is done. This skill fires while you are doing it. The two are complements:
one shapes the work, the other gates the claim.

## The Seven Rules

1. **Smallest-change bias.** The correct change is the smallest one that
   solves the stated problem. A refactor is not a fix; a rewrite is not a
   refactor. If the task says "fix the null check", touch the null check.

2. **Edit over create.** Before writing a new file, read what already
   exists. An edit to an existing file is almost always better than a new
   file that duplicates, shadows, or contradicts it.

3. **Read before writing.** No file is created or edited without first
   reading the files it will live beside. No function is added without
   grepping for one that already does the job.

4. **Match your response to the task.** A one-line fix gets a one-line
   answer. A rename gets a rename, not a paragraph explaining why naming
   matters. The length of the reply tracks the complexity of the work, not
   the importance you assign to it.

5. **Scope stays where it started.** If the task does not mention tests,
   do not write tests. If it does not mention docs, do not update docs.
   If you see something unrelated that needs fixing, name it; do not fix
   it inside this task.

6. **When uncertain, do less.** A change you are unsure about is a change
   the reviewer has to debug. If you cannot tell whether a line should
   change, leave it alone and say why you left it.

7. **Name what you did not do.** Every task has edges you chose not to
   cross. Say which edges and why. A gap you name is an informed decision;
   a gap you hide is a latent defect.

## Red Flags

| Signal | What is happening |
|---|---|
| A diff that touches files the task did not name | Scope has escaped |
| A new file where an existing one could have been edited | Create-over-edit bias |
| An answer longer than the change it describes | Proportionality lost |
| A "while I was here" aside that lands as code | Gold-plating |
| A refactor folded into a bug fix | Two changes in one, neither reviewable |
| Silence about what was left unchanged | Gap hiding |

## Rationalization Prevention

| Excuse | Reality |
|---|---|
| "It was easy so I just did it" | Easy changes still carry review cost |
| "They will need this eventually" | Eventually is not now |
| "It was already broken" | A separate finding, not this task |
| "The code was right there" | Proximity is not a mandate |
| "I cleaned it up while I was in the file" | A cleanup is a separate change |
| "It is only a few lines" | Line count does not determine scope |
| "The tests needed updating too" | Only if the task said so |
