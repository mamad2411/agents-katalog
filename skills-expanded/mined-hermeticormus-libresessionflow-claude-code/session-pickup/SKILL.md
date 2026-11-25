---
name: session-pickup
description: "Session entry ritual, the reader half of the handoff contract: finds the right HANDOFF.md (through the handoff index, a path, or a project name), re-runs its verify commands to separate still-done from drifted, loads the key files, and presents a short orientation with the next action. Falls back to reconstructing context from git history when no handoff exists, and can resume a chat thread when LibreWhatsApp is installed. Use at the start of a session, after a context clear, a machine switch, or a teammate's handoff."
user-invocable: false
---

# Pickup: restore context at session start

> Consume a HANDOFF.md and orient the session, reconstruct context from git when there is no handoff, or resume a conversation. Three modes, detected in order.

| Mode | Trigger | Detail |
|---|---|---|
| **Handoff** | A HANDOFF.md exists for the target | this file |
| **Cold** | The project exists but has no handoff | [cold-pickup.md](cold-pickup.md) |
| **Conversation** | The argument names a chat, not a project | [conversation-pickup.md](conversation-pickup.md) |

Run the steps without asking for confirmation, except where a step says to ask. Goal: from zero context to working, fast.

## Settings

Read the settings file if it exists: `cat "${SESSIONFLOW_CONFIG:-$HOME/.claude/sessionflow.json}" 2>/dev/null`.

- `home` (env `SESSIONFLOW_HOME`, default `~/.claude/sessionflow`): holds the handoff index at `<home>/handoffs/INDEX.md`.
- `pickup.search_paths` (default: the current project plus `~/projects` when it exists): where to look for a project by name.
- `pickup.remotes` (optional): prefixes that route the search to another machine over ssh.
- `pickup.chats` (optional): chats that `all` also reads.

## Step 0: route the argument

Check the handoff index first if it exists (`<home>/handoffs/INDEX.md`, written by the handoff plugin). It lists every handoff with its absolute path, so a lookup there beats a filesystem search.

Top-down, first match wins:

1. **Ends with `all`**: strip it, route the rest normally, then widen the sweep (see "Scope modifier: all").
2. **No argument**: take the newest index row with status `open`. No index or no open row: check `./HANDOFF.md`, then `<git root>/HANDOFF.md`, then the most recently modified `HANDOFF.md` under the search paths (`find <path> -maxdepth 3 -name HANDOFF.md`). Several candidates: list them with dates and ask which.
3. **A file path** (starts with `/`, `./`, or `~/`): use it.
4. **Matches index rows** (case-insensitive match on the slug or topic column): one row, use its path (strip the backticks, expand `~`); several rows, list When, Slug, and Status and ask one question. If the indexed file no longer exists, mark the row `missing`, say so, and continue down this list.
5. **A URL or hostname** (contains a dot and a known suffix such as `.com`, `.app`, `.io`, `.dev`): strip the scheme, `www.`, port, and path; use the leftmost label as the project hint (`docs.example.com` becomes `docs`) and continue with rule 7.
6. **First word matches a `pickup.remotes` prefix**: the rest is the project name; run every search and read below over `ssh <host> "<command>"` in that remote's roots, and write paths as `<host>:<path>`.
7. **Chat-shaped** (a channel keyword such as `chat`, `dm`, `wa`, `whatsapp`, `thread`, `conversation`; a phone number; an id ending in `@c.us` or `@g.us`): conversation mode, see [conversation-pickup.md](conversation-pickup.md).
8. **A project name**: `find <search paths> -maxdepth 3 -type d -iname "*<name>*"`. For each match, look for `HANDOFF.md`. One match with a handoff: use it. Several: list and ask. Match without a handoff: cold mode, see [cold-pickup.md](cold-pickup.md).
9. **Nothing found**: say `No HANDOFF.md or project found. Pass a path or a project name, for example /pickup ./HANDOFF.md` and stop.

If the argument could be both a project and a chat, ask "project or chat?" once.

## Step 1: read and parse

Read the HANDOFF.md fully. Handoffs written by the handoff plugin use these sections; accept other layouts too and map them as well as you can:

- **What I was doing**: the mission
- **Where I left off**: the exact file, line, phase, or failing test
- **What's done** and **What's NOT done**
- **Key context not obvious from the diff**: decisions, false leads, intentional oddities, references to read first
- **Open questions**
- **Verify what's done is still done**: commands
- **Next step**
- **Resume prompt**, when present

A malformed handoff: note what is missing and load what you can.

## Step 2: load key context

- Read every file the handoff names as a reference or key file, if it exists and is under about 200 lines; for larger files note the path and read only the named section.
- In the project's git repo:

  ```bash
  git -C <project> status --short
  git -C <project> log --oneline -5
  git -C <project> branch --show-current
  ```

- Compare with the handoff: commits made after it was written, or a different branch, mean the state moved. Say so.

## Step 3: verify that done is still done

State drifts between sessions. Take each command from the verify section and run it.

- Read-only checks (tests, `git`, `grep`, `curl` of a health endpoint, `gh ... view`) run without asking.
- A command that changes state (installs, migrations, deploys, pushes, deletes) is shown, not run; ask first.
- Classify each claim:

| Result | Meaning |
|---|---|
| **still done** | The check passes as the handoff expected |
| **drifted** | The check fails or returns something else; show the difference |
| **not checkable** | No command given, or the command needs something unavailable here |

Drifted items come before the next step: the next step may no longer be the right one.

## Step 4: present the orientation

A distillation, not a copy of the handoff:

```markdown
## Resumed: <project>

**Path**: <absolute path>
**Branch**: <branch> | **Last commit**: <hash> <subject>
**Git status**: <clean | N files changed>

### What was happening
<one to two sentences>

### Verified
- still done: <items>
- drifted: <items, with what changed>
- not checkable: <items>

### Key context
<the two to four facts from the handoff that matter most before touching anything>

### Open questions
<carried over, or "none">

### Next action
<the single most immediate action: file, command, or decision; revised if drift changed it>
```

## Step 5: plan before editing

If the next action is an implementation task, enter plan mode (the EnterPlanMode tool) and draft the plan, so the user confirms it before any edit. Skip plan mode for cold and conversation pickups.

## Step 6: mark the handoff consumed

Once the orientation is shown, flip the handoff's index row from `open` to `picked-up` (match on the path column). Leave the HANDOFF.md file where it is: it is part of the project history, and the next `/handoff` replaces or updates it. Rename it to `HANDOFF.archived.md` only if the user asks.

## Scope modifier: all

`/pickup <target> all` widens the sweep beyond the handoff. Gather each source that is available and skip the rest silently:

1. The handoff flow above.
2. GitHub state for the repo, when `gh` is authenticated: `gh pr list --author @me`, `gh issue list --assignee @me`, and `gh pr status`.
3. Chats listed for this project in `pickup.chats`, through LibreWhatsApp `/pull`, showing only what is new since the last pull.

Synthesize one orientation: handoff state, ticket state, conversation state. Flag conflicts between them, for example a PR merged that the handoff lists as open.

## Notes

- Trust the handoff; do not re-read the whole history.
- Ask clarifying questions only when the handoff is ambiguous about what to do next.
- Several handoffs match: ask which before loading anything.
