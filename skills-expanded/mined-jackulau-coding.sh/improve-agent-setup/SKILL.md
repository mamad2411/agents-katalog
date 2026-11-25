---
name: improve-agent-setup
description: "Finds what goes wrong most in this repo's recorded agent sessions and the AGENTS.md or CLAUDE.md line that fixes it, then checks whether a committed change helped. Use when the user asks to improve their agent setup, asks why the agent keeps repeating a mistake, or asks whether an AGENTS.md, CLAUDE.md, rule or skill change worked."
license: MIT
---

# Improve the agent setup

Uses three tools of the coding.sh MCP server: `improve`, `harness_changes` and `session_get`. They
read sessions recorded on this machine and change nothing.

## Find what to fix

1. Call `improve`. Pass `repo` only when the user means a repo other than the one you are in.
2. Take the first entry of `issues`. Open its `example.sessionId` with `session_get` and check that
   the session shows the problem. Say what you found in one or two sentences. If the session does
   not show it, say so and take the next issue.
3. When the issue has `line` and `file`, show the user both. Add the line only after they say yes.
   When it has no `line`, tell the user what to do from `fix`: no instruction line fixes it. When
   it has `quietSince`, it has not come back since that change: say the change may have fixed it,
   and do not propose a new line.
4. After the edit, tell the user to commit the file. The verdict on a change comes from sessions
   recorded after its commit.
5. When `changes` is not empty, give each earlier change's `verdict` and `reason` in one sentence.

When `issues` is empty, say so and give `scope.sessions`, the number of sessions it read. With few
sessions, call `status` to check that sessions are being captured.

## Check whether a change helped

1. Call `harness_changes`. Pass `commit` when the user names one.
2. For each change, give `verdict` and `reason` with the counts behind them: sessions and flagged
   sessions in `before` and `after`, and `rules`, which says how often the agent followed each new
   line before and after.
3. Use the table for what to say next.
4. List `after.flaggedSessions` with their flags. For `regressed`, open the newest one with
   `session_get` and say what went wrong.

| Verdict | What to tell the user |
|---|---|
| `helped` | Fewer sessions went wrong after the change. Give the counts. |
| `regressed` | More sessions went wrong after it. Show the flagged sessions and offer to revert the line. |
| `followed-no-effect` | The agent follows the new line, but the failures did not fall. Give the command in `next`. |
| `costlier` | Sessions after it do more work and the failures did not fall. Give the command in `next`. |
| `no-clear-change` | The difference could be chance. More sessions will narrow it. |
| `too-early` | Fewer than 5 sessions ran with the change. Ask again after more sessions. |
| `no-sessions-after` | No session ran with the change yet. With `headlessLeftOut`, only that many headless runs did: call again with `headless: true` to count them. |
| `no-baseline` | No session ran before the change, so there is nothing to compare with. |

## Rules

- Never edit AGENTS.md, CLAUDE.md, a rule or a skill before the user says yes.
- Do not claim more than the numbers show. A verdict from a handful of sessions is a hint.
- A command in `next` can run for minutes and can call a model. Give it to the user to run.
