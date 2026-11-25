---
name: runnable
description: "Use when the user asks for a one-word acknowledgement drill — replies with exactly the word the drill names."
version: 0.1.0
---

# runnable

## Intent

Give the eval-run exercise a minimal, valid target: a skill whose eval suite
is deterministic-clean and cheap to execute, with one case that fails its
expectation by design so a runner has a real failure to report.

## Inputs

- A drill prompt naming what to say.

## Preconditions

- None.

## Procedure

1. Read the drill prompt.
2. Reply with exactly what it asks for, nothing more.

## Output

- The requested reply, verbatim.

## Examples

Input: `Say the word apple.`
Output: `apple`

## Anti-patterns

- Adding commentary around the requested reply.
