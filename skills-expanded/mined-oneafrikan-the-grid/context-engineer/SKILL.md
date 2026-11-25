<!--
  SKILL.md — Context Engineer operating manual.
  Runtime: Claude Code + ACP (swappable coding CLI). Content stays LCD — no
  assumptions about a specific repo layout beyond what the task names.
-->

# Skill: Context Engineer

## Invocation

```
/context-engineer <files or session type in scope + the budget or limit to hit>
```

Or picked up from a Signal Protocol entry. No scope or limit named: ask.

## Step 1 — Baseline

- List what loads: always-on files, per-task files, on-demand references.
- Run `python3 scripts/budget.py --report` if the repo has it, and `wc -c` on each file in scope.
- Write the numbers down. Anything you cannot measure is "unmeasured".

## Step 2 — Design

| Question | Why |
|---|---|
| Is it needed every session? | If not, move it behind a pointer |
| Does it change often? | Stable content first so a cached prefix survives |
| What is retrieved, in what chunks, ranked how, how much enters context? | Retrieval design |
| What must a compaction or handoff keep? | Decisions, open items, next step |
| Where does a trimmed rule now live? | Nothing lost in a split |

## Step 3 — Propose, then apply

- Show the diff first for a human's `CLAUDE.md` or memory files.
- State the byte cost of any always-on addition and the budget it counts against.
- Apply one change at a time.

## Step 4 — Re-measure and hand off

- Re-run the same commands. Report before and after, or "unmeasured".
- Name the independent check (the gate, or another role); label your own run a self-check.
- Prompt text changes: route to prompt-engineer. Runtime changes: route to ai-engineer. If not wired, tell the user which role should take it.
