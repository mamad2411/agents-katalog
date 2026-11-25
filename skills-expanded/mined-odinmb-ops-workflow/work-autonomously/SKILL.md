---
name: work-autonomously
description: Shared rules for unattended execution — only load when explicitly referenced by another command or skill. Never auto-trigger based on user prompts.
---

# Autonomous Conventions

Rules for commands and skills that run without user input (e.g., `/ops:get-to-work`, `/ops:batch-execute`). The goal is to keep moving and defer human judgment to a structured follow-up review.

## Core Rules

1. **Never stop for user input.** Record questions and move on.
2. **Delete only what the list below allows.** Record every other intended deletion under **Files to Delete** in the follow-up file.
3. **Never push to remote,** except a commit touching only `to-decide/` on the repository's default branch, as `ops:decide` says ("Landing to-decide items"), unless the user's own rules forbid that push. Otherwise only local branches and commits.
4. **Commit with explicit pathspecs.** Name the paths you changed on the commit itself: `git add -- <path> <path> …` (needed for new files, which a commit pathspec alone does not pick up), then `git commit -m "<message>" -- <path> <path> …`. Never `git add -A`, `git add .` or `git commit -a`, and never a bare `git commit` after staging: a plain commit takes the whole index, so it can sweep a parallel agent's or the user's half-finished work into your commit. Work out the paths from the agent's summary and `git status`.
5. **When uncertain, make a sensible choice and move on.** Record your reasoning and alternatives in the follow-up file so the user can review. Only skip when the wrong choice could have truly bad consequences (data loss, security, breaking external contracts). Getting work done with transparent doubts beats a slightly lower chance of mistakes.
6. **No real-world actions** (the list below).
7. **Goals and autopilot's files are the user's.** Never change `charter.md`: a goal, audience or non-goal that looks wrong goes under **User Input Needed**. Where `ops:decide` is loaded and your own instructions let you write question items, make it a question item in the project's to-decide queue instead, listed there only as `decide <id>`. Where the repo's CLAUDE.md has an `## Autopilot` section, never edit, move or delete `state/autopilot.md` or `references/autopilot-policy.md` either: they are autopilot's alone. Every other file is shared, and a run works in it by the usual rules.

### Real-world actions an unattended run never takes

This is the one full list; agents and commands point here. Never:

- Send emails, messages, or notifications
- Submit forms, applications, or registrations
- Post to social media or external platforms
- Make API calls that modify external state
- Make purchases or financial transactions
- Contact anyone on behalf of the user

You can: research (web search, read public pages), write files, create plans, analyze data, produce drafts and artifacts the user can later use for world-affecting actions, maintain the repo's knowledge system, and put outgoing steps and questions only the user can answer in the project's to-decide queue (`ops:decide`).

**The one exception** is the user's Approve on an outbox card in `ops:decide`'s walk, in a session they are chatting in, stated in full in `ops:decide` ("Each kind keeps its own authorisation"). Unattended runs and subagents act on nothing.

### Deletions an unattended run may make

These are part of the commands' own process, so they happen without asking:

- **Processed `.update/` inbox files** — a source file whose useful content has been fully extracted into the knowledge base, per the `update` skill's disposition rules. When unsure, keep it (move it to `references/`) rather than delete it.
- **`plans/<batch>-direct-tasks.md`** — once `/ops:batch-execute` has processed its last entry.
- **Worktrees this run created, and their branches** — after their branch is merged into the run's branch: `git worktree remove <path>` and `git branch -d <branch>`. Never `-D`, never `--force`, never a worktree or branch the run did not create.
- **A parallel task's notes file** (`plans/<run>-<task>-agent-notes.md`) — once `/ops:get-to-work` has folded it into the follow-up file.

Removing an entry from a file — a done backlog item, a stale `INDEX.md` line, a processed direct-task entry — is an edit, not a deletion. Moving a finished plan to `plans/completed/` is a move. Both are fine.

Everything else stays forbidden: no deleting any other file or folder (temp files included — see below), no discarding uncommitted changes (`git checkout -- …`, `git restore`, `git reset --hard`, `git clean`), no deleting other branches or tags, no rewriting history.

## Follow-Up File

Create a follow-up `.md` file in the project's plans directory (`.plans/` or `plans/`, whichever the project uses) at the start of the process. It captures everything that needs human review afterward.

### Required sections

```markdown
## Controversial Decisions
Items where the agent made a judgment call the user should review.

## Skipped Items
Opportunities identified but not acted on, with reasons.

## User Input Needed
Questions that blocked progress on specific items. An agent that writes its questions to the to-decide queue (`ops:decide`) lists only `decide <id>` lines here.

## Files to Delete
Files that should be removed but are not on the list of deletions an unattended run may make.

## Implementation Issues
Problems encountered during execution.

## Borderline Insights
Findings that might warrant persisting to the project's knowledge system (e.g., MEMORY.md, CLAUDE.md, or equivalent) but the agent wasn't confident enough to add directly. User should review and decide whether to keep or discard.

## Suggested Follow-Up Work
Potential new work items that emerged during execution but the agent wasn't confident enough to add directly (e.g., to a backlog, TODO list, or issue tracker). User should review and decide whether to act on or discard.
```

Not every section will be used by every command — include the ones that are relevant.

## Showing the run

The handoff of a long run shows its effect as well as saying it, wherever the session talking to the user can: a rendered excerpt of a deliverable, a small diagram of a plan or structure the run reshaped, a few before → after numbers about the project (open questions, stale items, backlog items with an owner) — whichever the run already has, often just one. Numbers describe the project, never the run's activity: no commit, file or task counts.

Where `SendUserFile` is in your tool list (cloud sessions, and sessions with Remote Control connected), send it as one or two files, each with a one-line caption: a deliverable's excerpt or a diagram with `display: "render"`, the numbers as one short Markdown file. Otherwise write one throwaway HTML page holding all of it to the session's scratchpad and give its full absolute path. Never the Artifact tool. It is a by-product, never a step: nothing is produced only for it (no extra research, no generated images), it is skipped if it would take more than a few minutes, and it carries no personal data, since a sent file leaves the machine. Only the session talking to the user sends it, at the handoff, never a task agent mid-run, and it never replaces the plain-terms handoff or the follow-up review. A headless run with nobody to hand it to skips it.

## Resolving Follow-Up Items

After all work is complete, go through follow-up items with the user:

1. Use the **AskUserQuestion** tool with concrete options derived from the context (e.g., "Keep as-is", "Revert this commit", "Modify to X") plus an "Other (I'll specify)" option.
2. Don't ask open-ended questions when you can present sensible choices.
3. Document each resolved item in the related plan file.
4. Once all items are resolved and integrated into their plan files, delete the follow-up file.

## Bash Command Rules

Respect the bash command allowlist rules from CLAUDE.md so the process doesn't get interrupted for user confirmations.

### Temporary files

If your project CLAUDE.md says to create temp files instead of running inline Python/Node in Bash, then delete them afterward: during autonomous execution, do NOT delete temp files — `rm` may require user confirmation and will interrupt the unattended run. Instead, add the file path to the **Files to Delete** section in the follow-up file. The user will clean them up during follow-up review.
