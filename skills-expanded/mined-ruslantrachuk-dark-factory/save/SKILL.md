---
name: save
description: Save the state of the work where the next session finds it — before /clear, before a long pause, at the quota ceiling, when the session ends. Updates the PR description (Done / Decisions / Open questions), adds notes to the claimed bd task, writes to memory what is not in git. Use for "save", "/save", "wrap up", "before clear", "we stop here".
---

# Skill `save` — the state of work, where the next session reads it

> Canonical template (templates/base). Needs no configuration.

> **Seam:** code host = GitHub (`gh pr edit`); execution queue = beads (`bd`). To use another tool, rewrite steps 2 and 3.

Nothing survives `/clear`, compaction or the end of a session except what is in git, in the PR, in the execution
queue and in memory. The SessionStart hook (`scripts/agent/session-context.sh`) reads the first three
back at the start of the next session; memory is loaded by the agent itself (Claude Code's project memory, Codex's memories). This skill writes all
four, in this order, and says what it wrote.

## Steps

1. **Commit what is worth keeping.** Finished, green work — a normal commit. Unfinished work that must
   not be lost — a `wip:` commit on the feature branch (never on the main branch). Push the branch only
   if the human allows pushes in this session; an unpushed commit is still in git.
2. **The PR description — the record of this work.** The branch has a PR (a draft opened at the start
   of work; none yet — `gh pr create --draft --title "<plain title>" --body-file -`). Rewrite its
   description as the current state, not a diary:
   ```markdown
   ## Done
   What the change does now, for a reader of `git log --merges`: behaviour, not file names.

   ## Decisions
   The choices made and why, including assumptions the human has not confirmed yet.
   A decision that shapes the architecture also gets an ADR in the branch.

   ## Open questions
   What is left or needs the human. Each follow-up is a bd task (its id here); "none" if none.
   ```
   Keep the board-card line (`Part of <PREFIX>-N`) if there is one. Pass it on stdin, so no file is
   written (this also works at the quota ceiling): `gh pr edit <branch> --body-file - <<'EOF'` … `EOF`. An old `gh` fails here with
   "Projects (classic) is being deprecated": update `gh`; until then `gh api -X PATCH
   repos/<owner>/<repo>/pulls/<number> -F body=@- <<'EOF'` … `EOF` does the same (not at the quota ceiling). `scripts/merge-feature.sh` refuses to merge without
   these three sections and puts this text into the merge commit.
3. **The claimed task's notes.** `bd update <id> --append-notes "<where I stopped: the next step, the
   command to run, what is half done>"` — short, for the session that picks the task up. A follow-up
   found along the way: `bd create … --deps discovered-from:<id>`, not a line in the PR only.
4. **Memory — what is not in git.** A preference or rule the human stated, a fact about the
   environment, a decision about how to work that is not a project decision: write it to memory (Claude Code: the
   project memory directory it loads at session start; Codex: its memories, `/memories`). Do not copy into memory what git, the
   PR or the queue already holds.
5. **Report** in two or three lines: the commit, the PR link, the task id with its note, what went to
   memory. If the session is ending on a quota ceiling, also name when the work resumes.

## Rules

- No secrets in any of the four places (dev stand passwords, tokens, account details).
- The PR description is rewritten, not appended to: the next reader needs the state, not the history.
- Anything that is neither in git, nor in the PR, nor in bd, nor in memory is lost at `/clear`.
