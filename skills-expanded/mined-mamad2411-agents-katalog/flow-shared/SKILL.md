---
name: flow-shared
description: Shared prompts and references for flow skills. Not invoked directly.
disable-model-invocation: true
---

# Flow Shared

**Do not invoke directly.** Resolve this directory, then read prompts/references from here.

## Path resolver

1. `.agents/skills/flow-shared/`
2. `.cursor/skills/flow-shared/`
3. `~/.cursor/skills/flow-shared/`

## Contents

- `references/execute-loop.md` — per-task dispatch loop (both lanes)
- `references/tdd-red-green.md` — TDD cycle for implement + patch
- `references/subagent-model-size.md` — pick a right-sized model per subagent dispatch
- `prompts/implementer.md` — prompt body for implementer subagents (`/flow-spec`, `/flow-patch`)
- `prompts/reviewer.md` — review checklist for reviewer subagents (both lanes)
