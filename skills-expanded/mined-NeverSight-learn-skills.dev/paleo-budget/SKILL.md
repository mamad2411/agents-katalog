---
name: paleo-budget
description: 'Use when user says "budget", "token limit", "stay under N tokens", or wants per-task token caps. Enforce a hard token budget per task/response — track estimate, stop before limit, summarize if exceeded. Off: "no budget" / "unlimited".'
version: 2.4.1
license: MIT
metadata:
  hermes:
    tags: [tokens, budget, cap, efficiency]
    related_skills: [paleo, paleo-trim-context]
---

# paleo-budget
Hard token budget per task. Cap spend, never overflow.

## Rules
- Set budget up front: "budget 2000" = max ~2000 out-tokens for the whole task.
- Estimate before writing: rough tok ≈ chars / 4. Track running count.
- Stop at ~90% budget. If answer incomplete, summarize remainder in bullets.
- Tight budget → pair with `paleo` (terse). budget + paleo = max save.
- Code/commands stay exact — budget hits prose, not correctness.

## Levels
- `soft`: warn near limit, keep going.
- `hard` (default): cut off at limit, summarize the tail.
- `strict`: fail-loud if estimate exceeds budget before starting.

## Switch
- `/budget 1500 soft|hard|strict` set cap + mode.
- "no budget" / "unlimited" → off.

## Gotchas
- Token estimate is approximate (chars/4). Leave 10% headroom.
- Never truncate the critical part of the answer — summarize instead.
- Budget = output cap. Input/context not counted unless user says "total".
