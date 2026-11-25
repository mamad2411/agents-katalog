---
name: scratchpad-working-files
description: Convention for working files that do not belong in the repository history, such as notes, progress tracking, reports, manual test helpers, scratch databases, reproduction scripts and session transcripts. All of them go in a gitignored .scratchpad/ folder, organized by feature slug. Use it at the start of any multi-step task, whenever you are about to create a temporary file, write a report, track progress, or brief a subagent, and whenever the user mentions the scratchpad or asks you to "save this" or "write the report".
---

# Scratchpad working files

If AGENTS.md sets a different convention for this topic, follow AGENTS.md.

## Location

Everything temporary goes in `.scratchpad/` at the repository root. Never use `/tmp`, the system temp folder or a session-specific scratch folder. The user expects to find the files in one place, and files outside the project are lost between sessions.

Before the first write, make sure `.scratchpad/` is in `.gitignore`. If not, add it in its own commit:

```text
# Working notes
.scratchpad/
```

## Layout

Use the feature slug (from the branch, see `git-commit-organizer`) as a subfolder:

```text
.scratchpad/
└── <slug>/
    ├── progress.md                 step, status and commits; used to resume after an interruption
    ├── interview-decisions.md      answers from on-the-spot
    ├── verification-report.md      verify-against-spec
    ├── browser-test-report.md      browser-acceptance-testing
    ├── redteam-report.md           red-team-review
    ├── change-list.md              triage-findings-list
    ├── production-readiness-report.md
    ├── retrospective.md            session-retrospective-rules
    ├── pr-body.md                  write-visual-pr
    ├── manual-env.sh               helpers to start an isolated server
    ├── manual-data/                isolated data for manual checks (scratch database, fixtures)
    ├── scripts/                    reproduction and verification scripts
    └── transcripts/                archived session transcripts
```

## Reports

Every long task ends with a report file, even if the user did not ask for one. Tell the user the path. A report that only exists in the chat is lost when the context is compacted.

## Progress file

Keep `progress.md` current during any loop:

```markdown
| Step | Status | Commits | Notes |
| --- | --- | --- | --- |
| 1 Walking skeleton | done | 0c31ee8, 84ae35f | |
| 2 Cancel an order | in progress | | |
```

If the session stops (usage limit, crash, new day), the next session reads this file and continues.

## Manual test environment

- Keep the data of manual checks (a scratch database, fixtures) inside `.scratchpad/<slug>/`, never the real data.
- Use a dedicated port that other sessions do not use.
- Put start and stop helpers in `manual-env.sh` so each check is one command.
- Stop every server you start by the PID that the start helper saved. Do not use `pkill -f` with a pattern that also appears in the command you run. It can stop your own shell. After the stop, wait until the port is free (`lsof -iTCP:<port> -sTCP:LISTEN`); a `pgrep` right after `kill` can still see the process.
- Mutation checks and backups also go in `.scratchpad/<slug>/`, not in `/tmp`.
- Keep test credentials in the helper script, not in chat messages.

## Briefing subagents

When you delegate work, include these rules in the brief:

- Write any file only under `.scratchpad/<slug>/`. Do not edit repository files unless the task says so.
- Use their own port and data if they start a server, and stop it at the end.
- Say which claims were verified and which were inferred.
