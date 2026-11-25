---
name: memory-handoff
description: Portable session handoff across agent CLIs. Read the project's handoff file when a session starts on known work; write or update it when a session ends or before context runs out. One plaintext markdown file per project gives any CLI (opencode, claude code, aider) a shared memory so the next session starts mid-thought instead of cold.
allowed-tools: read, bash
license: Apache-2.0
---

## When to use

Load this skill when a session touches a project that has a handoff
file, when the user asks to "hand off", "pick up where we left off", or
"save context", or when a session is long enough that losing it would
hurt (roughly: more decisions made than fit in what you can trust
yourself to recall later).

The contract is one markdown file per project at a fixed location. Any
agent that can read and write files can use it. No daemon, no database,
no lock-in: the file is the memory.

## The handoff file

Default location: `~/.agent/handoffs/<project-slug>.md`, where the slug
is the project directory name (for `~/dev/src/crawlkit`, the slug is
`crawlkit`). `$AGENT_HANDOFF_DIR` overrides the directory. The path for
a slug prints with `scripts/handoff.sh path <slug>`.

Use `scripts/handoff.sh read <slug>` to locate and print the file, and
write it back with any file-writing mechanism the host agent has.

The file has five fixed sections, in this order:

```markdown
# handoff: <project-slug>

## Status
One paragraph: what this project is and where it stands. A stranger
should be able to act after reading only this.

## Open threads
Bulleted list of unfinished work, newest first. Each item names the
branch, file, or command needed to resume it.

## Decisions
Dated, one line each, irreversible or expensive-to-reverse choices
only. Rationale lives in the repo, not here.

## Next step
The single most useful thing to do first, as an imperative sentence
with the exact command if there is one.

## Updated
ISO timestamp of the last write and the name of the agent or human
that wrote it.
```

## Steps

1. At session start on known work: read the file. Treat `Next step` as
   the default first action and `Open threads` as the agenda. Say out
   loud what you picked up, so the human can correct stale context.
2. Before doing irreversible work, check `Decisions` for a dated line
   that contradicts what you are about to do.
3. On session end, on `save context`, or when the session is long:
   rewrite the file. Rewrite whole sections rather than appending;
   stale handoffs are worse than none. Keep `Status` under 150 words.
4. Every write updates the `Updated` line: timestamp plus which agent
   wrote it (for example `2026-10-25T14:00Z by opencode`).
5. Never put secrets, tokens, or credentials in the file. It is
   plaintext in a home directory and often synced by dotfile tooling.

## Anti-patterns

- Do not dump session transcripts into the file. Handoff is decisions
  and pointers, not history.
- Do not create a second format beside an existing one: if the project
  already has `NOTES.md` or a task tracker the human maintains, ask
  before introducing the handoff file.
- Do not write a handoff for throwaway work; the file earns its keep
  on multi-session projects only.

See [references/handoff-schema.md](references/handoff-schema.md) for a
filled-in example.
