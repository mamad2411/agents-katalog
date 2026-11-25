---
name: council
description: "Runs the four-seat council for hard-to-reverse or contested Hikma decisions: new commands, lockfile or config schema, writes outside the project, breaking changes, new dependencies. Advisory only. Use when the user says @council, run the council, council review, or quick check."
---

# Council

A structured review of one decision from four fixed viewpoints, so the human decides with the tensions in view. Advisory only: it never edits files, runs commands, or implements anything. Nothing follows a run until the human confirms.

## When to run it

- Hard to reverse: lockfile or config schema, a new command, a public flag, a new dependency.
- High blast radius: anything that writes outside the project, touches the user's home, or changes what `push` does.
- Genuinely contested: reasonable engineers would disagree.

Skip it when the answer is obvious or the change is small and reversible.

## Seats

Exactly four. Do not add a fifth; if a lens is missing, fold it into the closest seat.

| Seat | File | Lens |
| --- | --- | --- |
| The Architect | `references/the-architect.md` | Integrity, trust boundaries, reversibility |
| The Shipper | `references/the-shipper.md` | User value, smallest useful version, momentum |
| The Critic | `references/the-critic.md` | Simplicity and long-term maintenance cost |
| The Terminal User | `references/the-terminal-user.md` | macOS, Linux, Windows, scripts, CI, no-TTY |

## How to run it

1. State the decision in one paragraph: the question, constraints, options considered.
2. Read the four seat files. If you can spawn subagents, give each seat only the decision and its own file so seats do not see each other; otherwise answer each seat separately and do not let one soften another.
3. Each seat answers in the output contract below.
4. Synthesize: where seats agree, where they conflict, and what the conflict shows. Artificial consensus means the run failed.
5. Present the synthesis and stop. Wait for the human.

Quick check: one paragraph per seat plus a one-line synthesis.

## Output contract

Each seat:

```
**Verdict:** <seat verdict word>
**Findings:** up to 4 bullets
**Must-fix:** numbered list, or none
```

Synthesis:

```
## Decision
## Confidence   (high / medium / low)
## Dissent      (a seat that did not approve and why it was overridden, or none)
## Reopen if
```

Record an accepted decision as a short note on the relevant board task, not in this skill.
