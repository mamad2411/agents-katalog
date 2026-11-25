---
name: mycelium
description: Decide whether to spawn subagents (one, or several in parallel) to search, investigate or edit, and brief them well; passes finding notes between agents so they don't redo the same exploration. Use before delegating to an agent and after an agent reports findings.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/bin/mycelium *), Bash("${CLAUDE_SKILL_DIR}/bin/mycelium" *)
---

# mycelium

!`"${CLAUDE_SKILL_DIR}/bin/mycelium" mode --banner`

Agents that do not expand the line above (e.g. Codex): run
`<this-skill-dir>/bin/mycelium mode --banner` first and follow it.

Delegation costs a fresh context per agent. Default to doing the work
yourself: a single file lookup, a small edit or one test command never
needs an agent.

`mycelium` is not on PATH: always use the full `<this-skill-dir>/bin/mycelium`
path. Notes live in `<git root>/.mycelium/notes.json`. From a folder of repos,
name files as `<repo>/<path>`: each note goes to the repo that holds the file.

**Before spawning an agent**

1. Delegate only a bounded task with a finish condition. Prefer one agent;
   run agents in parallel only for independent tasks.
2. Check shared notes: `<this-skill-dir>/bin/mycelium brief "<task>"`.
3. Write the brief with these lines. The plugin's gate hook fills in a
   missing `Task:` (from the description), `Return:` and `Budget:` and adds
   matching notes as `Known:`, so a thin brief still runs once:
   ```
   Task: <one question or change, with a finish condition>
   Known: <relevant notes from `brief`, or "none relevant">
   Return: <findings with file:line, answer, unresolved questions>
   Budget: <N tool calls>
   ```
   `Budget:` is a hard limit: the agent gets a wrap-up line 3 calls before
   it, and every call past it is refused, so it replies with partial
   findings instead of looping. Without one, the agent type's default
   applies, scaled by the budget level (`bin/mycelium budget
   low|medium|high|extreme`, or the plugin's `agent_budget` option).
4. Never spawn a second agent for the same investigation: reuse the first
   result or continue that agent. The gate denies a near-identical repeat
   unless a `Not a duplicate: <how>` line explains the difference.
5. Use a specialist, not `general-purpose` (the gate reroutes it unless the
   brief has a `Why general: <reason>` line): `scout` reads and searches,
   `landscaper` makes one bounded change, `botanist` runs builds and tests
   and diagnoses failures. A copied skill installs them with
   `bin/mycelium install-agents`.
6. Don't check on a running background agent; wait for its completion
   notice.

**After an agent returns**

A reply's `Notes:` block (`- <topic> | <finding> | <file>...`, part of
`scout`'s format; add it to your `Return:` for other agents) is recorded
by the plugin's SubagentStop hook. Record any other durable finding once,
with the files it describes:
```
<this-skill-dir>/bin/mycelium note "<subsystem>" "<finding>" <file>...
```
Notes are hashed against their files; `bin/mycelium list --stale` shows
notes whose files changed. Re-check, then `bin/mycelium verify <id>`, or
`bin/mycelium drop <id>`. Keep task status out of notes (or use
`--kind status`, which is never briefed).

Gate modes, hook setup, note format: `references/protocol.md`.
