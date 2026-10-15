---
name: daily-retrospective
description: |-
  Trigger: the start of every user turn, regardless of what the turn is about. This skill records the turn and, on the first turn of a new day, writes up the previous working day. It applies to coding, questions, review, planning, chat, and everything else — there is no category of user turn it skips.
  Skip: only when you are a subagent dispatched to carry out one specific task. The main agent already recorded that turn, and recording it again double-counts it.
---

# Daily Retrospective

Record how the user works, and once a day hand back what the record shows.

Two things happen here, in this order, and neither one is the user's actual request. Do them, then do what the user asked for. The user never waits on this skill and never sees its mechanics.

## State

Everything lives under `~/.agents/daily-retrospective/`. Create it and both subdirectories before writing anything: `mkdir -p ~/.agents/daily-retrospective/logs ~/.agents/daily-retrospective/retrospectives`. A shell redirection does not create missing parent directories, so skipping this makes the very first write of a fresh install fail.

```text
~/.agents/daily-retrospective/
  logs/YYYY-MM-DD.md              # every prompt submitted that day, all projects
  retrospectives/YYYY-MM-DD.md    # written the following day, automatically
  state.json                      # { "version": 1, "lastNotifiedOn": "YYYY-MM-DD" }
  config.json                     # { "version": 1, "language": "<code>" }
```

All dates are local-timezone dates. Get today's date from the system rather than assuming it.

This skill is the only thing that writes into `retrospectives/`, so the presence of `retrospectives/<date>.md` is a reliable signal that the date has been handled.

## Procedure

### 0. Resolve the language

Read `config.json`.

When it is missing, determine the language of the user's current prompt and create it: `{"version": 1, "language": "<code>"}` using a language code such as `ko`, `en`, or `ja`.

When the prompt carries no clear language signal — a pasted stack trace, a bare `ok`, a lone file path — do not create the file. Log this turn in English and try again next turn. A wrong value fixed in place is worse than a few turns of delay, because every document written afterward inherits it.

Never re-detect once `config.json` exists. If the user edited it, that is the answer.

### 1. Check whether today's notification already went out

Read `state.json`. If `lastNotifiedOn` equals today, skip to step 3. This is the once-per-day guarantee: the notification appears on the first turn of a day and never again that day.

When `state.json` is absent or cannot be parsed, treat it as "not notified today" and continue to step 2. Absence is the normal state on a fresh install — the file is written the first time a retrospective is actually produced, not before. Never abandon the rest of this skill because this file could not be read; a failed read must not cost the user their log entry.

### 2. Write up the previous working day

Pick the target date: the most recent date that has a file in `logs/`, is earlier than today, and has no corresponding file in `retrospectives/`. If there is no such date, skip to step 3 without writing or announcing anything — this is the normal case on a fresh install.

Then, in this order:

1. Set `lastNotifiedOn` to today in `state.json` **before** generating anything. If two sessions start the same morning, the one that claims it wins and the other stays silent. Doing this after generation would notify twice.
2. Read `logs/<target-date>.md` and write `retrospectives/<target-date>.md`, following `references/retrospective.template.md`.

Only the most recent unwritten day is handled. Do not backfill older dates.

### 3. Record this turn

Append an entry to `logs/<today>.md` following `references/log-entry.template.md`. Create the file with its date header if it does not exist.

Append — do not read the file and write it back. Other sessions may be appending at the same time, and a whole-file write discards their entries. Use a shell append redirection.

### 4. Do what the user actually asked

Carry out the user's request normally. This skill does not change, delay, or replace it.

### 5. Add the notification, if step 2 produced one

Append exactly one sentence to the end of your response, with a Markdown link to the file:

```text
📝 Wrote up a retrospective from your 2026-08-09 session → [2026-08-09.md](file:///absolute/path/to/home/.agents/daily-retrospective/retrospectives/2026-08-09.md)
```

Resolve the real absolute path of the home directory before writing the link. The path above is a placeholder; a link that still contains it points at nothing.

One sentence. Do not summarize the retrospective's contents in your response — the link is the delivery mechanism. If nothing was generated in step 2, add nothing.

## Running In Parallel

Steps 2 and 3 are bookkeeping and should not sit between the user and their answer.

**When this session can dispatch a subagent** (a Task or Agent tool is available): hand steps 2 and 3 to it and move straight to step 4. Give it the project path, the agent name, a summary of the user's request, what was happening in the previous turn, and **the time the prompt arrived** — a subagent cannot see the conversation, and it starts late enough that its own clock would record when the bookkeeping ran rather than when the user spoke. The retrospective's rhythm section is built from these timestamps, so the drift matters. It can read `config.json` itself.

**When it cannot**: do the work inline, keeping tool calls to a minimum. One append for the log entry; one read and one write for the retrospective.

Branch on whether the capability exists, never on which provider you are. Both paths produce identical files.

## Language

Three separate rules. Applying one where another belongs is the most likely way to get this wrong.

- **Document bodies** — the `Prompt` and `Context` sentences in a log entry, and the entire retrospective including its section headings — use `config.json`'s `language`.
- **Field keys and enumerated values** — `Project`, `Agent`, `Intent`, `Prompt`, `Context`, `Signal`, and the `Intent` and `Signal` values — are always English, whatever the language setting is. They are parsing targets, not prose.
- **The notification sentence** follows the language of the current conversation, like any other thing you say. It is speech, not a stored document.

The last two rules diverging is intended, not a bug. A user whose `language` is `ko` who writes to you in English today gets a Korean retrospective file and an English notification sentence.

## Rules

- Never delay or skip the user's request to do this bookkeeping.
- Never explain this skill's tool calls, file writes, or reasoning to the user. The only visible output is the one notification sentence, once a day.
- Never store verbatim prompt text. Summaries only.
- Never write credentials, tokens, keys, or connection strings into a log. Describe what the prompt was about and leave the value out.
- Never write anything into `retrospectives/` except an automatically generated retrospective for a completed day.
