---
name: human-blockers
description: Sweep every project for gates only Keith can clear, rank them by the clock they start, and write the shared list. Use for "what am I blocking", "what's waiting on me", "human blockers".
disable-model-invocation: true
---

# Human blockers

A **human gate** is a step no agent can take: a browser console, a bank detail, a phone in a pocket, a signature, a paid account, a key that only exists behind someone's login. They are the slowest thing in every project here and they are recorded in whichever file happened to be open when they appeared. This skill collects them into one ranked list.

The list lives at `~/.claude/BLOCKERS.md`, one line per open gate. Every skill that creates a gate appends to it; this skill reconciles it against the scattered sources and rewrites it. Read it, don't recall it.

## 1. Sweep

```bash
python ~/.claude/skills/human-blockers/scripts/sweep.py
```

It prints `file:line: text` candidates from every memory file, every `docs/LAUNCH.md` under the home directory, and the current `BLOCKERS.md`. Add `--root <dir>` to scan repos parked outside home. It collects; it does not judge, so expect prose about past state in the output.

## 2. Judge each candidate

A candidate earns a row only if all three hold. Drop it otherwise, and do not report what you dropped.

1. **Open.** Not shipped, merged, submitted or already met. A line describing how something was done last month is not a gate.
2. **Human-only.** Keith is the only one who can clear it. If an agent could do it with the tools in this session, it is a task, not a gate: do it or say so, but keep it off the list.
3. **Blocking.** Something real waits on it. A nice-to-have with nothing downstream is a backlog item.

Read the source file around any candidate you are unsure about. A one-line grep hit is not enough context to call something open, and a list that reports cleared gates trains Keith to stop reading it.

## 3. Rank by the clock, not by effort

Sort by when the gate stops blocking, not by how long it takes Keith.

- **Starts a clock** goes first. A 14-day Play closed test is 30 seconds of work and two weeks of waiting; started today it clears on day 14, started next week it moves the launch. Same for anything with review queues, bank verification, or a fixed opening date.
- **Then breadth.** A gate blocking four later stages beats one blocking a single screen.
- **Then cost to Keith.** Only as the tie-break, and never as the sort key: a five-minute job that unblocks nothing still ranks below a two-week clock.

For each row, state the wall-clock lead time explicitly. "Play closed test: 14 days once started" is the number that makes the ranking obvious.

## 4. Write and report

Rewrite `~/.claude/BLOCKERS.md`:

```markdown
# Blockers

> Gates only Keith can clear. Rewritten by /human-blockers; appended by any skill that creates a gate.

## <project>
- [ ] <gate in one line> | clock: <lead time or "none"> | blocks: <what waits> | source: <file:line>
```

Then report the top rows in chat, longest clock first, with the one action that starts each. Keep it to what Keith can act on today. No secret values in the file or in chat: name the key, never print it.

## Producers

This skill reads; the gates are written by whoever creates them. Both wired 2026-09-06:

- `/idea-to-store` appends a row for every `open` line it writes to a project's `docs/LAUNCH.md`.
- `/dev-framework-rl` appends a row on every escalate-to-human, at any stage.

A gate that reaches `BLOCKERS.md` only through the sweep is a producer that did not fire. When you notice one, wire the producer rather than widening the sweep patterns: a broader grep finds the same gate later and never finds it sooner.

## Sources

`scripts/sweep.py` reads `~/.claude/projects/C--Users-skf-s/memory/*.md`, `*/docs/LAUNCH.md` under each `--root`, and `~/.claude/BLOCKERS.md`. Its marker list was measured against those files, not guessed. One structural rule sits beside the keywords: a line starting `- [ ]` is a candidate on the strength of the box alone, and its own box outranks a word like "closed" or "live" in its prose (history in `docs/incidents.md`, 2026-09-07). If a project keeps its gates somewhere else, add the path to `sources()` rather than working around it in chat.
