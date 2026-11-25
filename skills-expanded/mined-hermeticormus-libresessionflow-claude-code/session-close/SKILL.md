---
name: session-close
description: "End-of-session ritual: audits the session, writes a handoff when work is unfinished, saves durable learnings to memory, writes a session summary, optionally notifies you through a channel you configure, then ends cleanly. Use when the user is wrapping up, says they are done for now, or asks to close out the session."
user-invocable: false
---

# Close: the end-of-session ritual

> Preserve the work. Carry the thread forward.

When invoked, run every step in order. Keep each step short: the output is for the next session, not a report for its own sake.

## Settings

Read the settings file if it exists: `cat "${SESSIONFLOW_CONFIG:-$HOME/.claude/sessionflow.json}" 2>/dev/null`. Every key is optional.

| Setting | Env override | Default |
|---|---|---|
| `home` | `SESSIONFLOW_HOME` | `~/.claude/sessionflow` |
| `memory_dir` | `SESSIONFLOW_MEMORY_DIR` | the project's auto memory folder, else `<project root>/.claude/memory/` |
| `notify.command` | `SESSIONFLOW_NOTIFY_CMD` | none: nothing is sent |
| `notify.push_target` | none | none |

With no settings at all, close still works: it writes the summary and memory locally and sends nothing.

## Step 1: session audit

Review the whole conversation and list:

- **Worked on**: projects, files, features
- **Decisions**: choices made and their reasons, preferences the user stated
- **State**: what works, what is broken, what is half-done
- **Open threads**: unfinished work and the next concrete step for each
- **Learnings**: gotchas hit, fixes found, patterns confirmed

If the session was a quick question with nothing to preserve, skip to Step 6 and keep the rest to one line.

## Step 2: handoff, when work is unfinished

If there is incomplete work that a later session must resume, write a handoff:

- With the handoff plugin installed (its `/handoff` command is available), follow `/handoff`.
- Without it, write `<project root>/HANDOFF.md` with: what we were doing, where it stopped (file and line if mid-edit), what is done, what is not done, context the diff does not show, commands that verify the done items, and one specific next step.

Skip this step when the work is finished and shipped.

## Step 3: update memory

Save only stable knowledge that a future session needs and cannot read from the code.

- With the absorb plugin installed (its `absorb-learnings` skill is available), run that method.
- Without it: resolve the memory folder (settings, then the project's auto memory folder, then `<project root>/.claude/memory/`), append or update entries in `MEMORY.md` or a topic file, and keep `MEMORY.md` a one-line-per-entry index.

Save: confirmed gotchas, changed project structure, new user preferences, solved recurring problems, changed service configuration.
Do not save: in-progress task state, conclusions from one observation, anything already in a CLAUDE.md, secrets.

## Step 4: session summary

Write `<home>/sessions/<project-slug>/<YYYY-MM-DD>-<slug>.md`, where `<project-slug>` is the project folder name and `<slug>` is a two-to-four word kebab-case description. Create the folders if needed.

```markdown
# Session: <YYYY-MM-DD>, <two-to-four word description>

## Work done
- <completed items>

## Current state
- <what works, what runs, what is deployed>

## Open threads
- <unfinished work with enough context to resume>

## Key files
- `<path>`: <what changed>

## Decisions and context
- <choices made, with reasons>

## Next steps
- <prioritized list>
```

The summary lives outside the repo on purpose: it is your record, not project history. The handoff (Step 2) is the file meant for the repo.

## Step 5: offer to ship, when the session produced a clear outcome

If the working tree has uncommitted changes that belong to finished work, list them and ask whether to commit (and push). Never commit or push without a yes.

## Step 6: notify (optional)

Compose the message:

```
Session closed

<two-to-three sentence summary of the work>

State: <brief current state>
Next: <top one or two priorities>
Repo: <https url> (<branch> @ <short hash>)
```

For the `Repo:` line, inside a git repo: `git remote get-url origin`, rewrite `git@github.com:owner/repo.git` to `https://github.com/owner/repo`, then `git branch --show-current` and `git rev-parse --short HEAD`. Omit the line outside a repo or without a remote.

Deliver it:

1. **`notify.command` or `SESSIONFLOW_NOTIFY_CMD` is set**: show the message, then run the command with the message on stdin (write the message to a temp file and pipe it, so quotes and backticks survive). Report the exit status in one line. On failure, print the message instead and say the notification did not go out.
2. **`notify.push_target` is set and the LibreWhatsApp `/push` command is available**: hand the message to `/push <push_target>`. Push shows its preview and waits for the user's confirmation; do not bypass that gate.
3. **Nothing configured**: print the message and say it was not sent anywhere. That is the default and it is fine.

Never put secrets or tokens in the message.

## Step 7: offer distillation

If the session contained a repeatable workflow or a new pattern, ask once:

> "This session had <pattern>. Want to turn it into a reusable skill before closing?"

Only offer when there is something worth keeping.

## Step 8: end

Print what was written, each on its own line with its absolute path (handoff, memory files, summary), then:

```
Session closed. State preserved. Exit with /exit or Ctrl+C.
```

Then stop. Do not continue the conversation.

## Notes

- Be concise. Everything written here is for the next session.
- Focus on resumability: what does the next session need to know first?
- Close orchestrates; the handoff and absorb plugins do the deep work when installed, and close falls back to short built-in versions when they are not.
