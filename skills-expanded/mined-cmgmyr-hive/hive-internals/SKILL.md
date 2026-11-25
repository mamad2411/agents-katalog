---
name: hive-internals
description: Mechanism, measurements, and incident history behind hive's rule-file prohibitions - tmux panes and typing, the store and data dir, worker state and hooks, the native addon and interpreter pin, the tool contract (lifecycle matrix, naming, CLI/MCP split), project scoping, and profile files. Consult before touching src/tmux.ts, src/spawn.ts, src/scheduler.ts, src/tools/*.ts, src/cli.ts, src/db.ts, src/dataDir.ts, src/backup.ts, src/abi.ts, src/context.ts, src/hook.ts, or src/profiles.ts, and whenever a rule file's short prohibition needs the "why" behind it.
---

# hive-internals

Seven rule files in `.claude/rules/`, plus `test/CLAUDE.md`, state prohibitions only - short, imperative, enforced by code. The reasoning behind each one - the incident that produced it, the measurement that pins the number, the mechanism that explains why the alternative doesn't work - lives here instead, so it costs nothing until something actually needs it.

Each reference file mirrors one rule file's original content, unabridged, in the order the rule file used to present it. Read the rule file first for the prohibition; come here for why it exists.

## References

- `references/tmux-and-panes.md` - tmux panes and typing into them: the private-server-vs-default-store refusal, why `tmux_target` is always a pane id, the dialog and unsubmitted-text holds, the six paths that can type into a pane, why a tmux timeout is a third outcome, `execFileSync` argument arrays, iTerm's minimal PATH. The largest reference here by far.
- `references/store-and-datadir.md` - the store and the data dir: why the data dir is read at call time, the 2026-07-28 incident that made test isolation enforced rather than conventional, append-only migrations, the write-lock rules, and what a live restore does to open connections.
- `references/worker-state.md` - worker state and hooks: why `agent_state_log` is append-only, five incidents where worker state was wrong and how each was closed, why a spawned or resumed worker's first idle is not a finish, why wake bodies are delivered verbatim, a standing watch's `OWNED_BY_WATCH` parent filter, and the conversation hold's TTL, ceiling, and the reattach bug that moved the ceiling to `due_at`.
- `references/native-addon.md` - the native addon and the interpreter pin: why hive pins an absolute interpreter, the Node-API floor and why it's checked per release line, what a plain `npm install` does and doesn't fix, and the SessionStart hook as the one entry point the pin doesn't cover.
- `references/tool-contract.md` - the tool contract: the verified lifecycle matrix, the naming convention for a new tool's verb, why write tools return slim receipts, the unknown-key strictness mechanism, and the CLI/MCP split.
- `references/project-scoping.md` - project scoping: why a worker's files and its store are separate questions, the mechanics of a cross-project spawn, and the accepted residuals in that design.
- `references/profile-files.md` - profile files: why widening resolution from three named files to any `.md` was mostly a type change, the RED-first proof behind the filename guard, why `profileFileNames` makes drift reporting correct for an extra with no code of its own, and why `worker.md` stays excluded from doctor's unset-var scan.
- `references/test-CLAUDE.md` - the suite's own isolation guards: the 227-leaked-servers incident and the four socket states behind verifying a tmux kill, the fd-exhaustion measurement, and the `scripts/run-tests.mjs` leak-manifest mechanics.

## Using this

Search by topic across all eight with `grep -rn "<term>" .claude/skills/hive-internals/references/`, or open the one file that matches the rule you're extending. This is reference material, not a todo list - nothing here needs promoting elsewhere.
