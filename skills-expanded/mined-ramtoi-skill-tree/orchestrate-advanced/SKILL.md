---
name: orchestrate-advanced
description: "Deep orchestrator: split a large goal into independent chunks, delegate each to a sub-orchestrator running orchestrate in its own branch. Trigger: /orchestrate-advanced, 'split and ship'."
ships_with:
  agents: [orch-sub-orchestrator, orch-researcher, orch-planner, orch-griller, orch-implementer,
           orch-reviewer]
  hooks:
    - name: orch-scope-guard
      event: PreToolUse
      tools: [Edit, Write, MultiEdit, Bash]
      command: scripts/scope-guard.sh
      activation: while-running
    - name: orch-report-guard
      event: SubagentStop
      tools: []
      command: scripts/report-guard.sh
      activation: while-running
    - name: orch-unit-brief
      event: SubagentStart
      tools: []
      command: scripts/unit-brief.sh
      activation: while-running
  permissions:
    deny: ["Bash(git push --force:*)"]
    ask: ["Bash(gh pr merge:*)"]
---

# Orchestrate Advanced

## Role

You are the super. You split one large goal into independent chunks, delegate each chunk to
a sub-orchestrator that runs the whole `orchestrate` loop in its own worktree and branch, and
integrate the chunks in merge order. You never implement, and you never read a chunk's diff
or open its `reports/` — you react to the 12-line chunk report and the trailer of the log it
names, the same way `orchestrate` reacts to a unit.

This skill **composes** `orchestrate`. Lanes, gates, profiles, steering, and confinement all
live there and are not repeated here: every sub-orchestrator runs that loop unchanged, and
you read `orchestrate/references/steering.md` when a chunk reports red or blocked.

## The super loop

1. Run `orchestrate`'s kickoff unchanged: `scripts/setup.sh`, PLAN.md, lane pick, profile.
2. Apply the chunking rule (`references/chunking.md`). If it fails, **stop and run plain
   `orchestrate`**, and say so.
3. Write PLAN.md's Chunks table (`references/super-plan.md`) and `plans/chunks/<chunk>.md`
   per chunk (`references/chunk-brief.md`).
4. Per chunk: create the branch and worktree, write the pending marker (below), pick the
   runner (`references/runners.md`), spawn the sub-orchestrator. Chunks run in parallel;
   their file sets are disjoint by construction.
5. React to each 12-line report (`references/chunk-report.md`). `green` -> integrate.
   `blocked` -> the resume protocol. `red` -> steering, exactly as `orchestrate`'s steering
   reference says.
6. After the last chunk: integrate in merge order, then run **one full gate** on the merged
   tree.

## Entry test

The chunking rule holds only when: every chunk's files are disjoint from every other
chunk's, every chunk has one gate that goes green alone, every chunk clears at least the
light lane, and there are three or more qualifying chunks. If it does not hold, stop here —
run plain `orchestrate` with waves instead, and say why in one line.

## Depth cap

Three levels, hard: **1** you, the super. **2** a sub-orchestrator, one per chunk. **3** its
units. A depth-3 unit spawns nothing. This is structural, not a rule you enforce by
attention: `orch-sub-orchestrator` is the only definition in `agents/` carrying the `Agent`
tool, and its own body names the five `orch-*` types as all it may spawn. None of the five
carries `Agent`, so nothing at depth 3 can fan out further.

## Where to read next

| File | Read it when |
|---|---|
| `references/chunking.md` | Applying the entry test, or explaining why a cut failed it |
| `references/chunk-brief.md` | Writing a chunk's brief |
| `references/chunk-report.md` | A chunk reports back; deciding how to react |
| `references/runners.md` | Choosing claude-nested vs codex-exec for a chunk |
| `references/super-plan.md` | Writing or resuming the Chunks table in PLAN.md |

## Writing the pending marker

Before spawning a chunk's sub-orchestrator, write
`<chunk workspace>/units/_pending/<chunk-id>.json`:

```json
{"schema_version": 1, "chunk": "<chunk-id>", "slug": "<slug>", "depth": 2,
 "runner": "claude-nested", "worktree": "<abs worktree>", "workspace": "<abs workspace>",
 "brief_path": "<abs brief>", "report_path": "<abs report>", "allowed": ["<path>", "..."],
 "created_at": "<iso8601>", "notes": []}
```

`allowed` is the brief's Allowed files list, copied unchanged, so the brief and the hook can
never disagree. Then write the worktree's pointer at
`$(git -C <worktree> rev-parse --git-dir)/orch-units` holding this chunk's absolute
`units/` directory on one line. `scripts/unit-brief.sh` claims this pending file per agent id
the first time each sub-agent starts; nothing else writes the marker.

## Anti-patterns

- Two chunks sharing a file, a lockfile, a migration, or a generated file.
- Cutting a chunk below the light lane just to hit three chunks.
- The super implementing instead of delegating.
- Opening a chunk's `reports/` instead of reading its 12-line return.
- Asking a human a question an options list in a `blocked` report already answers.
