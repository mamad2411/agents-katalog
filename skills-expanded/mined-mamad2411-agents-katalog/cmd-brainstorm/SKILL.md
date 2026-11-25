---
name: cmd-brainstorm
description: Command — Open a brainstorming session for any new feature, component, or behavior change before writing code.
---

# /brainstorm

Invokes `Skill(devkit:brainstorming)` and starts the design-before-code dialogue.

Argument `[topic]` (optional): seed text for the brainstorming session ("e.g. add notifications", "rate-limit the orders API"). If omitted, the assistant asks what you want to design.

Terminal state: an approved spec and an invocation of `Skill(devkit:planning)` to write the implementation plan.

## Arguments

`[topic]`
