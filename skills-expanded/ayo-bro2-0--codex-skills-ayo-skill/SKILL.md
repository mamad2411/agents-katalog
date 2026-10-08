---
name: ayo
description: Save, resume, checkpoint, and restore AI-assisted project state. Use when the user says "ayo" to save a Markdown handoff, "oya" to read the latest handoff and continue after confirmation, "ayo bro" to create a Git-backed AYO checkpoint plus .ayo project memory, or "fuck" to restore the latest AYO checkpoint after confirmation. Also use for project handoff, status summary, continuation note, context transfer, progress report, next-task document, project resume, checkpoint, archive, save point, rollback, restore, or safe-state requests. Works for any project type by reading visible conversation, available workspace context, handoff files in ayo-handoffs, and AYO memory files in .ayo.
---

# Ayo

## Purpose

When the user says `ayo`, create a practical Markdown handoff document that lets another AI or human continue the work with minimal context loss, and save it as a file instead of displaying the full document in chat.

When the user says `oya`, resume from the latest saved handoff document in the current project's `ayo-handoffs` folder, then ask for confirmation before continuing work.

When the user says `ayo bro`, create a game-like safe checkpoint: Git stores the code, and AYO stores the memory in `.ayo/memory.md` plus `.ayo/checkpoints.json`. Keep only the latest AYO checkpoint in `.ayo/checkpoints.json`; each new `ayo bro` replaces the previous AYO checkpoint record and memory.

When the user says `fuck`, restore the project to the latest `ayo bro` checkpoint after confirming with the user.

Do not treat `ayo`, `oya`, `ayo bro`, or `fuck` as greetings or casual language. Treat them as explicit project state commands.

## Command Routing

- `ayo`: save a new handoff Markdown file.
- `oya`: read the latest saved handoff, understand the project state, propose the next action, and ask the user to confirm before executing.
- `ayo bro`: create a project checkpoint with Git plus AYO memory files, replacing the previous AYO checkpoint record.
- `fuck`: restore the latest AYO checkpoint after user confirmation.

## Ayo Workflow

1. Reconstruct the project goal from the conversation first.
2. Inspect local context only when it is useful and available:
   - Current working directory and file tree.
   - Important source/config/document files.
   - Git status, recent commits, or diffs if the workspace is a Git repository.
   - Running commands, test output, logs, or app URLs mentioned in the chat.
3. Identify what is complete, partially complete, blocked, and not started.
4. Determine the project directory:
   - Prefer the current workspace/project root.
   - If inside a Git repository, the Git root is a good project directory.
   - If no project root is detectable, use the current working directory.
5. Create an `ayo-handoffs` folder directly inside the project directory.
6. Save the handoff as a new Markdown file named `handoff-YYYYMMDD-HHMMSS.md` inside `ayo-handoffs`.
7. Reply in chat with only a short success note and the saved file path. Do not paste the full handoff document into chat unless the user explicitly asks to view it.

## Oya Workflow

1. Determine the project directory:
   - Prefer the current workspace/project root.
   - If inside a Git repository, the Git root is a good project directory.
   - If no project root is detectable, use the current working directory.
2. Look for handoff files in:

```text
<project-directory>/ayo-handoffs/*.md
```

3. Select the latest handoff file by modified time. If modified time is unavailable or ambiguous, use the newest timestamp in filenames like `handoff-YYYYMMDD-HHMMSS.md`.
4. Read the latest handoff document.
5. Inspect additional project files only when needed to verify current state.
6. Reply with a short resume summary:
   - Which handoff file was read.
   - Current goal.
   - Current progress.
   - Proposed next action.
7. Ask for confirmation before execution. Use a direct question such as:

```text
Should I start the proposed next step?
```

8. Do not modify files, run project-changing commands, start services, install dependencies, commit, push, or otherwise execute the next task until the user clearly confirms.
9. After confirmation, continue the project from the handoff and follow the normal engineering workflow for the requested task.

If no handoff file exists, explain that no `ayo-handoffs` Markdown file was found and ask the user to run `ayo` first or provide the handoff content.

## Ayo Bro Workflow

Use `ayo bro` as a save point. The user should not need to understand Git.

1. Determine the project directory:
   - Prefer the current workspace/project root.
   - If inside a Git repository, use the Git root.
   - If no project root is detectable, use the current working directory.
2. Check whether Git is available. If Git is not installed or cannot run, explain that checkpointing requires Git and stop.
3. If the project is not a Git repository, run `git init`.
4. If Git commit identity is missing, set repository-local defaults instead of stopping:

```text
git config user.name "AYO"
git config user.email "ayo@example.local"
```

5. Create `.ayo/` in the project root.
6. Write `.ayo/memory.md` as a fresh project memory summary. Do not copy README verbatim. Summarize:
   - Project name.
   - Project goal.
   - Current development progress.
   - Recent changes.
   - Core files.
   - Current problems.
   - Next plan.
   - Notes for a future AI.
7. Treat `.ayo/checkpoints.json` as an untracked single-slot save file. Ensure `.ayo/checkpoints.json` is ignored by Git by adding this line to `.git/info/exclude` if it is not already present:

```text
.ayo/checkpoints.json
```

8. If `.ayo/checkpoints.json` is already tracked, remove it from the Git index without deleting the working file:

```text
git rm --cached .ayo/checkpoints.json
```

9. Stage all project files except `.ayo/checkpoints.json`. Include `.ayo/memory.md`.
10. Create a checkpoint commit with message. If there are no staged changes, create an empty checkpoint commit with `git commit --allow-empty` so every `ayo bro` produces a restorable save point:

```text
AYO_CHECKPOINT_YYYYMMDD_HHMM
```

11. Get the checkpoint commit hash with `git rev-parse HEAD`.
12. Move or create the checkpoint tag so it points at this commit:

```text
git tag -f ayo-checkpoint <commit>
```

13. Overwrite `.ayo/checkpoints.json` with a JSON array containing only the latest checkpoint entry:

```json
[
  {
    "id": "checkpoint_latest",
    "commit": "abc123",
    "time": "2026-06-11 21:05",
    "summary": "Completed login module"
  }
]
```

Use `checkpoint_latest` as the id. Create a concise summary from the current project state and recent changes.

14. Do not commit `.ayo/checkpoints.json`. It is local AYO metadata and must survive `git reset --hard`.
15. Reply with the checkpoint id, commit hash, time, and summary.

If there are no file changes to commit, still refresh `.ayo/memory.md` and `.ayo/checkpoints.json` so the checkpoint records current project memory. The previous AYO checkpoint record should still be replaced.

## Fuck Workflow

Use `fuck` as a game-like load command. It restores the latest `ayo bro` checkpoint.

Because rollback changes project files, ask for confirmation before executing any restore. First read `.ayo/checkpoints.json`, find the latest checkpoint, and show:

- checkpoint id
- commit hash
- time
- summary

Ask a direct confirmation question such as:

```text
Restore this checkpoint now?
```

Only continue if the user clearly confirms.

After confirmation:

1. Verify the project is a Git repository.
2. Read `.ayo/checkpoints.json`.
3. Select the only checkpoint entry in the array. If an older multi-entry index is found, use the last entry as a backward-compatible fallback.
4. Prefer the `ayo-checkpoint` tag as the restore target when it exists. Otherwise use the commit recorded in `.ayo/checkpoints.json`.
5. Verify the restore target exists with `git cat-file -e <target>^{commit}`.
6. Before resetting, preserve any current uncommitted work with:

```text
git stash push -u -m AYO_BACKUP_BEFORE_RESTORE_YYYYMMDD_HHMM
```

If there is nothing to stash, continue.

7. Restore the project with:

```text
git reset --hard <target>
```

8. Reply with:
   - Restored checkpoint id.
   - Checkpoint time.
   - Checkpoint summary.
   - The restored commit hash.
   - Whether a pre-restore stash backup was created.

If `.ayo/checkpoints.json` is missing, empty, invalid JSON, or the restore target is missing, explain the problem and do not reset.

## Output Requirements

For `ayo`, write the saved Markdown file in the same language the user is using unless they request another language.

Use this structure:

```markdown
# Ayo Handoff

## Project Overview

## Current Goal

## Progress So Far

## Current State

## Project Structure

## Important Files And Context

## Decisions Made

## Open Issues Or Blockers

## Next Tasks

## Suggested Next Prompt
```

Keep the document specific. Prefer concrete file paths, feature names, commands, URLs, branch names, and dates over generic statements.

## Ayo File Output

Default output location:

```text
<project-directory>/ayo-handoffs/handoff-YYYYMMDD-HHMMSS.md
```

Use local time for the timestamp when available. Use a filesystem-safe filename.

If a handoff file with the same name already exists, append a short numeric suffix such as `-2`.

After saving, respond with:

```text
Created handoff document: <path>
```

If file writing is unavailable in the current AI environment, explain the blocker briefly and do not paste the full handoff unless the user asks.

## Section Guidance

`Project Overview`: Explain what the project is, who it is for, and the intended outcome.

`Current Goal`: State the immediate objective being pursued in this conversation.

`Progress So Far`: List completed work and verified behavior. Mention tests or checks that passed.

`Current State`: Describe what exists right now, including partial work and any known uncertainty.

`Project Structure`: Summarize the relevant directory and file layout. If the project is large, include only the parts needed for handoff.

`Important Files And Context`: Call out files, commands, tools, environment details, credentials assumptions, external services, or conversation details that matter.

`Decisions Made`: Capture architectural, product, design, naming, workflow, and tradeoff decisions.

`Open Issues Or Blockers`: State unresolved problems, missing information, failing tests, or risks.

`Next Tasks`: Give ordered, actionable tasks. Each task should be clear enough for a new AI agent to start immediately.

`Suggested Next Prompt`: Provide a concise prompt the user can paste into a new AI chat to continue from the handoff.

## Quality Bar

- Be honest about uncertainty. Use "Unknown" rather than inventing details.
- Separate facts from assumptions.
- Do not expose secrets, API keys, tokens, cookies, private credentials, or unrelated personal data.
- Do not over-read the filesystem. Inspect enough to make the handoff useful.
- If no files are available, create the saved handoff from the conversation alone.
- If the conversation is short, still produce the document and mark unknown sections clearly.
- For checkpoint and restore commands, prefer clear status messages over long explanations.
- Never run `git reset --hard` for `fuck` until the user confirms the exact checkpoint to restore.
