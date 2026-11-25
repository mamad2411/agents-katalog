---
name: tracequest
description: Investigate past coding-agent sessions (Claude Code, Codex, Cursor, Droid, OpenCode, Grok, vktr, fx, DeepSeek Harness) with the TraceQuest CLI. Use when asked why runs in a project keep failing, what an earlier session did, where agent time or money went, or to write a standup or handoff from past sessions.
---

# TraceQuest

TraceQuest indexes the session files coding agents already write on this machine
(and on other machines or Cursor Cloud, once imported) and makes them searchable.
Searching and analysis are local and make no model calls.

## Install (once)

Check first: `tracequest --version`. If the command is missing:

1. Needs Node.js 22.5+ and git.
2. `git clone https://github.com/viktor-com/tracequest.git` into a folder outside
   the current project (next to it, as `../tracequest`, unless the user says otherwise).
3. In that clone: `npm install`, then `npm link` to put `tracequest` on PATH.
   If `npm link` is not allowed, use `node <clone>/bin/tracequest.js` instead.

The first command builds the index; with thousands of sessions this takes
seconds to a minute. Later runs reuse it.

## Investigate why runs keep failing

1. Sessions with errors in this project (project = the folder name):
   `tracequest find "project:<folder> errors:>0" --json`
2. Search for the error text across every agent and project:
   `tracequest search "<error text>" --limit 20`
   A fix often turns up in a session from a different agent or machine.
3. Read one session: `tracequest messages <hash> --pretty`
   (`<hash>` is the 8-character id that `find` and `search` print; `sessionHash` in `--json`).
4. Totals and the most common failure causes:
   `tracequest insights "project:<folder>" --refresh`
5. Report what keeps failing, with the session hashes as evidence. Propose the
   lesson as a short AGENTS.md rule and show it to the user before writing it.
   If nothing matches, say so instead of guessing.

## Commands

| Need | Command |
| --- | --- |
| Recent sessions, filtered | `tracequest find "<expr>"` (add `--json` for records) |
| Full-text search | `tracequest search "<text>" [--filter "<expr>"]` |
| Matches as Markdown for a prompt | `tracequest handoff "<text>" --limit 5` |
| One session as messages | `tracequest messages <hash> --pretty` |
| One session as an HTML report | `tracequest render <hash> -o report.html` |
| Failure causes, retries, time, cost | `tracequest insights [expr] --refresh` |
| Standup from yesterday's sessions | `tracequest standup --yesterday` (`--print-input` first shows what is sent to the agent) |
| Copy sessions from another machine | `tracequest import ssh <host>` |
| Web app | `tracequest serve`, then open http://localhost:7777 |

Filter keys: `project`, `source` (claude, codex, cursor, factory, opencode, grok,
vktr, fx, dsh), `host`, `tool`, `model`, `grade`, `errors`, `size`, `age`, `live`.
Combine with `AND`, `OR`, `NOT`, parentheses and free text, for example
`source:codex errors:>0 age:<7d`.

Sessions contain conversation text and command output. Quote only what the
user needs, and do not paste secrets from them.

Full reference: https://github.com/viktor-com/tracequest/blob/main/docs/cli-reference.md
