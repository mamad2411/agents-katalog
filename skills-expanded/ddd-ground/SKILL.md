---
name: ddd-ground
description: >
  Produce a documentation-grounded plan with cited decisions and useful
  snippets, save its research, or continue an authorized implementation.
license: MIT
compatibility: Install together with sibling skills ddd, ddd-scope, ddd-ground, and ddd-verify; the main procedure is referenced at ../ddd/SKILL.md.
metadata:
  author: ddd-methodology
  version: "0.8.0"
---

# Ground the plan and implementation

Load the `ddd` skill completely, through your native skill tool when you have one, otherwise by reading
[DDD](../ddd/SKILL.md), and apply **Keep one persistent note and ground the
plan**, performing steps 1 and 2 first wherever questions or sources are missing.
That skill owns the procedure and Documentation basis format.

Finish a planning request with a saved plan: cited decisions, useful snippets
labeled by origin and execution status, checks to run, and open questions. Stop
before implementation when only a plan was requested.

For authorized implementation, continue through DDD's steps 4 and 5. Consult
new APIs and research failed assumptions before workarounds; maintain the same
note and compare actual code against sources. No claims or trace ledgers are required.

Keep proposed application explanations visibly proposed until implementation
and checks establish them. Use snippets only for consequential choices.
