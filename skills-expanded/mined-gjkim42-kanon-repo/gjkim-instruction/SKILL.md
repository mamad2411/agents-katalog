---
name: gjkim-instruction
description: >-
  Create and maintain gjkim_instruction.md, the root document for a
  loop-engineering effort. The document holds only the minimum requirements
  and confirmed decisions, and deliberately leaves everything else open so
  that later iterations are not locked into early guesses. Use whenever the
  user mentions gjkim_instruction.md, a root document or root doc for a loop,
  loop engineering, starting a long-running agent loop on a goal, or asks to
  record a requirement or a confirmed decision for such an effort. Also use
  at the start of a loop iteration to check what is already decided versus
  still open.
---

# gjkim_instruction.md — Root Document for Loop Engineering

## Why this document exists

Loop engineering runs many short agent iterations against one long-lived
goal. Each iteration starts with little context, so it needs one stable
place that says what must be true and what has already been decided. That
place is `gjkim_instruction.md`, kept at the root of the project the loop
works on.

The failure mode this document guards against is early decision lock-in.
Whatever is written in the root document, every later iteration inherits as
if it were a requirement. If unconfirmed details get written down — a
library choice, a schema, a file layout that was only a first guess — wrong
guesses become permanent and the loop loses the freedom to find better
answers. So the document records only two kinds of content, and treats
everything else as deliberately open.

## What goes in

- **Goal**: one or two sentences on what the effort must achieve.
- **Minimum requirements**: the smallest set of outcomes that must hold
  true for the effort to succeed. Outcome-level, not implementation-level.
- **Non-goals**: outcomes the effort explicitly does not pursue, so
  iterations do not drift into them. A non-goal is a confirmed "we are not
  doing this", not merely something undecided — undecided things belong
  under "Deliberately open".
- **Confirmed decisions**: only decisions the user has explicitly
  confirmed. Each entry carries the date it was confirmed and a one-line
  why, so a later iteration can tell whether the reason still applies.
- **Deliberately open** (optional): choices that are known to be undecided,
  listed so iterations do not silently assume an answer. Listing an option
  here does not endorse it.

## What stays out

- Implementation details that were not explicitly confirmed: libraries,
  frameworks, schemas, file layouts, API shapes, deployment targets.
- Task lists, progress logs, iteration status. Those belong in issues, PRs,
  or iteration notes — the root document describes the destination, not the
  journey.
- Speculative designs or options under consideration. Mentioning them at
  most under "Deliberately open", never as requirements or decisions.
- Anything derivable from the code itself.

Litmus test for requirement vs. detail: could two meaningfully different
implementations both satisfy it? If only one implementation can, it is a
detail — leave it out until the user confirms it as a decision.

## Template

Create the document at the project root, named exactly
`gjkim_instruction.md`:

```markdown
# <effort name>

Root document for loop engineering. Read this first in every iteration.
Anything not written here is an open choice.

## Goal

<one or two sentences>

## Minimum requirements

- <outcome that must hold>

## Non-goals

- <outcome explicitly not pursued>

## Confirmed decisions

- <decision> — confirmed <YYYY-MM-DD>. Why: <one line>

## Deliberately open

- <choice known to be undecided; do not assume an answer>
```

Omit the "Non-goals" or "Deliberately open" section when there is nothing
useful to warn about. Keep the whole document around one page; if it grows
past that, details are leaking in — prune them.

## Maintaining the document

- Add a decision only when the user has explicitly confirmed it. "Leaning
  toward", "probably", or "maybe" is not confirmation.
- Record a non-goal only when the user has explicitly ruled it out. An
  option nobody has decided on yet stays under "Deliberately open".
- When an iteration must make a choice that is not in the document, make
  the best local choice, record it in that iteration's PR or notes as
  unconfirmed, and propose it to the user for confirmation. Do not write it
  into the root document yet.
- When a decision is reversed, replace the entry. The document describes
  only the current state; git history holds the old one.
- When updating, preserve existing requirements and decisions unless the
  user explicitly changes them.
