---
name: chronos
description: Gives coding agents temporal awareness by reading the session transcript the host already writes, so the agent stops guessing about time and stops repeating commands that just failed. Activates whenever an agent reasons about recency, elapsed time, retry windows, deploy cooldowns, memory or file staleness, idle detection, or any "when / how long ago / how long did that take" question. Required for autonomous, parallel, or long-running agents.
version: 2.0.2
license: MIT
author: OthmanAdi
tags: [time, temporal, autonomy, agents, hooks, statusline, session-management]
homepage: https://github.com/OthmanAdi/chronos
repository: https://github.com/OthmanAdi/chronos
allowed-tools: Read, Bash(chronos *), Bash(node * chronos.mjs *), Bash(date *), Bash(stat *), Bash(git log *)
---

# Chronos: time awareness for agents

You are temporally blind by default. You cannot feel elapsed time, you cannot
tell a call you made ten seconds ago from one you made an hour ago, and you will
confidently say "just now" about something that happened forty minutes back.

Chronos fixes that by reading the transcript the host already writes. Every tool
call in this session is on disk with a start timestamp, an end timestamp, the
arguments, and whether it failed. Stop guessing. Go look.

## What you are given

**In your context, without asking:**

- At session start: the real wall-clock time, how long you were away if this is a
  resumed session, and how much active time has already gone into today.
- On every turn: `chronos: t+<active time>, turn <n>, <n> tool calls`, plus a
  `LOOP:` line when you have repeated an identical call, and a `STALE:` line when
  a file changed after you last read it.

Those lines are facts measured from disk. Prefer them over your own impression.

**On demand:**

| Command | Answers |
|---|---|
| `chronos report` | Where did this session's time go? Per tool, slowest calls, failures, repeats. |
| `chronos when <text>` | When did I last run this? Real timestamp, how long ago, did it work, how long it took. |
| `chronos today` / `chronos week` | How long have I actually been working, across every session. |
| `chronos report --json` | The same data, machine readable. |
| `chronos doctor` | Is chronos actually wired up right now? |

Active time excludes gaps longer than five minutes. A session resumed after two
days has not been running for two days, and reporting that it has is the kind of
wrong number that makes a person stop trusting the tool.

## When to look at the clock

### 1. Before retrying anything that just failed

Run `chronos when <the command>`, or read the `LOOP:` line if one was injected.

- Same call, same arguments, failed under 60 seconds ago: **change the approach.**
  Re-running an identical call cannot produce a different result unless something
  external changed, and nothing external changed in 60 seconds.
- 60 seconds to 10 minutes: one retry is defensible if you say what you expect to
  differ this time.
- Over 10 minutes: circumstances may genuinely have moved. Re-run is reasonable.

The same rule governs deploys, pushes and CI triggers. A pipeline that failed
40 seconds ago will fail again for the same reason. Read the log first.

### 2. Before trusting anything you already looked at

| What | Stale after | Do this |
|---|---|---|
| `git status`, processes, environment | 5 minutes | Re-query |
| A file you read | 1 hour, or any write to it since | Re-read |
| Persistent memory, knowledge-graph facts | 7 days since written | Re-verify |
| API responses: prices, PR state, issues | 5 minutes | Re-fetch |
| Build or test results | Any source change since that run | Re-run |
| Your own earlier claim | Always | Check the transcript |

A `STALE:` line in your context already did this check for one case: a file that
was written after you last read it. The other rows in this table are yours to
apply, and chronos will not remind you about them.

### 3. Before summarising or reporting progress

Let the elapsed time set the length:

- under 5 minutes: answer, no recap;
- 5 to 30 minutes: one paragraph on what changed;
- over 30 minutes: `chronos report`, and use its real numbers.

### 4. Before starting something long or destructive

Check whether the same tool has been getting slower. `chronos report` lists the
slowest calls and the average per tool. If the last few runs of a command are each
well above its average, something is degrading. Say so rather than waiting quietly.

### 5. Idle detection in autonomous loops

When the injected context says the user has been away and you are still looping
unattended: stop, summarise, list the open decisions, and ask. Chronos tells you
about an absence once it passes 30 minutes; the statusline shows one from 1
minute. Always escalate past two hours of session time with no user input,
whatever either threshold says.

### 6. Never say "just now" or "in a moment"

Replace every vague interval with a measured one.

- Wrong: "I just tried that."
- Right: "That exact command failed 47 seconds ago. Repeating it will not help."

- Wrong: "Let's wait a bit and retry."
- Right: "Retry at 14:32 local, three minutes from now."

### 7. Date and time questions

Never answer from memory or from your training data. In order:

1. The `now` line injected at session start, if the session is young.
2. `chronos report`, whose numbers come from the transcript's own timestamps.
3. `date -u +"%Y-%m-%dT%H:%M:%SZ"`, or `Get-Date -AsUTC -Format o` on PowerShell 7,
   or `Get-Date -Format o` on Windows PowerShell 5.1.

## Failure modes to avoid

- Do not count turns or messages to estimate elapsed time. Message count and wall
  clock are unrelated; one long tool call can span more time than fifty messages.
- Do not trust your own earlier "just now". The transcript is the record; your
  context is a summary of it.
- Do not treat a resumed session's span as time worked. Use active time.
- Do not go silent in an autonomous loop. Rule 5 always applies.
- Do not assume chronos is installed. If you never saw a `chronos:` line in your
  context, it is not running: fall back to the shell commands below and say so.

## Degraded mode: no hooks on this platform

Chronos ships hooks for Claude Code. On a host without them you still follow every
rule above, you just gather the facts yourself:

| Need | POSIX | PowerShell |
|---|---|---|
| Now, UTC | `date -u +"%Y-%m-%dT%H:%M:%SZ"` | `Get-Date -Format o` |
| File mtime | `stat -c %Y f` (GNU), `stat -f %m f` (BSD/macOS) | `(Get-Item f).LastWriteTimeUtc` |
| Last commit time | `git log -1 --format=%cI -- <path>` | same |

State it plainly when you do: "No chronos context in this session; this timestamp
comes from `date -u`."

## Why this is a skill and not a note in a prompt

From arxiv 2510.23853, "Your LLM Agents are Temporally Blind" (October 2025): even
with timestamps present in context, the strongest frontier models reach only 65%
alignment with human temporal judgment, and timestamps appear in under 4% of
reasoning traces. Putting a clock in the context is not enough. The model has to
be told when to look at it. The seven rules above are that instruction.
