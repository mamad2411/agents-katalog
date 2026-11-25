---
name: awesome-prompts
description: "434 one-line power prompts for coding agents, split into 12 on-demand parts. Use when the user wants a short, high-density prompt to steer Claude Code, Codex, Cursor, or any coding agent - architecture, state-machine audits, debugging, planning, review, verification, learning, or steering. Match the task to a part in the index and read only that file, or run the meta-prompt to auto-pick."
---


# Awesome Prompts

Single sentences so dense every word does work. Philosophy: **density beats
length**. One loaded sentence outperforms a page of instructions. Short
prompts also get a fresh context window's full attention, so delegate real
hunting to subagents and keep the main thread narrow.

Sources and credits live in the README. This file is prompts only, so agent
context stays lean.

## Meta: let the agent pick

Paste this plus your task, idea, or code, and let the model choose:

```
Consider all the mini-prompts in this skill, pick the ones that would
improve my idea/input/software the most, and apply them.
```

Narrow it per phase: "...pick the 3 best for *planning* / *review* /
*debugging* this."

Prompt-craft rule behind every entry: name the destination, name the path,
skip the prohibitions.

- "Prefer one-liners over elaborate skills."
- "Mine text and code for operators, then combine them into prompts nobody could invent."
- "Take the prompts, generalize, and run a sweep of candidate cross-cutting defects: launch independent agents and assess."

## Parts: read only what the task needs

Each file below holds one family of one-liners. Match the task, open that file, use what fits. Read `notes.md` alongside any part.

| Part | Use when the task is about | File | Prompts |
|---|---|---|---:|
| Architecture | design, abstractions, structure, naming, contracts | `references/architecture.md` | 22 |
| State-machine | state-machine / invariant / transition-table audits | `references/state-machines.md` | 68 |
| Unicorn hunts | DISCOVER hunts: invariants, transactions, trust, stuck work | `references/unicorn-hunts.md` | 20 |
| Debugging | bugs, root cause, failure modes, unhappy paths | `references/debugging.md` | 78 |
| Planning | planning, scope, alignment, subagents, estimation | `references/planning.md` | 55 |
| Code quality | refactor, cleanup, repair sets, security sweep, hidden gems | `references/quality.md` | 82 |
| Verification | prove it: evidence, tests, PROVE set, regression gates | `references/verification.md` | 68 |
| Review | code review, PR review, review checklists | `references/review.md` | 29 |
| Agent hygiene | agent setup files, machine config, transcripts | `references/hygiene.md` | 5 |
| Learning | explain, teach, learn, understand unfamiliar code | `references/learning.md` | 16 |
| Steering | autonomy, status updates, standing instructions to the agent | `references/steering.md` | 100 |
| Notes | field principles (short - read whole file with any part) | `references/notes.md` | 0 |

Sources and credits for every prompt live in `README.md`. Prompt wording is verbatim from contributors; do not reword quoted lines when reusing them.