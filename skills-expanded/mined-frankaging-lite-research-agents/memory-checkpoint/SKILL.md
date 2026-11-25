---
name: memory-checkpoint
type: instruction
description: Defines how to save and load agent state as checkpoint files.
---

# Memory Checkpoint

Defines how to save a checkpoint and how to load one into SI. When to checkpoint is determined by the calling context — the project, the war room, or the agent's own judgment.

---

## How to Save

Create a timestamped folder under `memory/checkpoints/`. Inside it, write one file per agent indexed by agent number.

```
memory/checkpoints/YYYYMMDD_HHMMSS/
├── agent-0.md
├── agent-1.md
└── ...
```

Each `agent-N.md` captures that agent's state. No length constraints — summarise what is needed to resume. A good checkpoint captures what would be hard to reconstruct, not a verbatim log.

```markdown
# Agent <N> — <timestamp>

**Role**: <role>
**Trigger**: <what caused this checkpoint>
**Completed**: <what was just finished>
**Next**: <exact next action>

## State
<key facts, file paths, env state, decisions made, blockers — whatever is needed to resume>
```

After writing all agent files, update `memory/SUMMARY.md` — rewrite it to point to the latest checkpoint.

```markdown
# Summary

- **Last checkpoint**: `memory/checkpoints/<timestamp>/`
- **Status**: <not_started | in_progress | blocked | complete>

## State
<key facts — file paths, important values, decisions that affect what comes next>

## Resume From
<one clear instruction: what to do next, any preconditions>
```

---

## How to Load

On resume, inject into SI in this order:

1. **Read `memory/SUMMARY.md`** — always first. Get current status and the latest checkpoint path.
2. **Read the relevant `agent-N.md`** from the latest checkpoint folder — inject the file for your agent index.
3. **Load other agents' files only if needed** — e.g. to understand what another agent did.
4. **Load older checkpoints only if needed** — e.g. to understand a past decision.

---

## Layout

```
memory/
├── SUMMARY.md
└── checkpoints/
    ├── 20260328_090000/
    │   └── agent-0.md
    ├── 20260328_142301/
    │   ├── agent-0.md
    │   └── agent-1.md
    └── 20260328_154732/
        ├── agent-0.md
        └── agent-1.md
```
