---
name: commit-iteration
description: Commit a git checkpoint after an iteration round, with a useful, audit-trail-quality commit message that summarizes what changed. Optional companion to the iteration loop. Use whenever the user says "commit this iteration," "save a checkpoint," "git commit," or after a meaningful iteration boundary (rubric score crossed a threshold, gap closed, structural change made). Skip if git is not initialized on this project.
---

# commit-iteration

## When to invoke
- After a meaningful iteration round (rubric score lift, gap closed, structural revision)
- When the user asks to "commit this," "save a checkpoint," "checkpoint this version"
- At the end of a working session (final commit captures all session changes)
- After a destructive operation completes successfully (so it can be reverted if needed)

## When NOT to invoke
- After every chat message — that's noise, not useful checkpoints
- If `git` is not initialized on this folder (check for `.git/`)
- For trivial edits the user is still drafting (commit when an iteration round finishes)
- Mid-iteration, when the work is in a partial state

## What this skill does

Writes a useful commit message describing what changed, runs `git add -A` and `git commit`, and confirms the checkpoint to the user in plain language.

## Steps

1. **Check git is initialized.** If `.git/` is not present, prompt the user to run `init-git-repo` first.
2. **Read `LOG.md`** to identify what just happened (the most recent session/block) — this is the source for the commit message.
3. **Read `RUBRIC_SCORES.md`** if it exists — to capture the score progression in the message.
4. **Compose a commit message** in this format:
   ```
   <short title — one line, ≤72 characters>
   
   <blank line>
   
   <2-5 lines describing what changed: what was the gap, what was the fix,
    what was the score lift if rubric was scored>
   
   <blank line>
   
   <optional: file count summary, e.g., "Files updated: 4. Lines: +120 -45.">
   ```
5. **Run `git add -A`** to stage all changes including new files.
6. **Run `git commit -m "..."`** with the composed message.
7. **Print a friendly confirmation** showing: the checkpoint title, the file count, and how to revert if needed.

## Commit message conventions

- **Title** (first line) starts with `Iteration N:` or `Session N:` or a domain-specific prefix
- Title is in present tense imperative ("Add chat-vs-agent explainer," not "Added chat-vs-agent explainer")
- Title is descriptive enough to be useful in `git log` output 6 months later
- Body explains the *why* (what gap was closed, what insight emerged), not the *what* (which files changed — git already shows that)

### Examples of good titles

```
Iteration 2: Add chat-vs-agent explainer + 11 inline hyperlinks
Iteration 3: Closing question added + external-link handling
Iteration 4: Voice calibration to author's prose patterns
Iteration 5: Final precision fixes — italic, forward-ref, self-ref
Session 2: Conceptual additions per user feedback (mutual discovery framing)
Session 7: Rubric scoring shows ship-ready (3.89/4.0)
```

### Examples of bad titles

```
Update                            ← useless 6 months later
Fix typos                         ← fine for tiny fixes; wrong for iteration boundaries
Changed some stuff                ← never commit with this message
WIP                               ← work-in-progress shouldn't be a checkpoint
.                                 ← genuinely seen in real repos; don't
```

## Output format

```
==> Iteration checkpoint saved.

  Title: "<the title>"
  Files updated: <N>  (changes: +<lines added> / -<lines removed>)
  
==> What this means in plain English:
    This version of your project is now permanently saved. If you change
    your mind about anything we did in this iteration, you can ask me
    to "revert to the previous checkpoint." To see the full history,
    ask "show me the project history."
```

## What NOT to do

- Do not commit if there are no actual changes (`git status` clean) — print a no-op message instead
- Do not commit secrets or large binary files. Verify the staged files don't include `*.env`, `*.key`, `secrets.json`, or files larger than ~10MB. Refuse the commit and explain if any are present.
- Do not push to a remote unless the user explicitly asks. This skill is local-only.
- Do not write commit messages that are just timestamps or empty descriptions. Always include the *why*.
- Do not chain commits — one commit per skill invocation, even if there are multiple logical changes (let the user decide whether to split).

## Operating principles

- **Iteration-boundary granularity.** Commit when a rubric round crossed a threshold or a gap closed — not after every chat message.
- **Useful messages over fast messages.** Spend the 30 seconds to write a message that will be readable months later. The audit trail is part of the asset.
- **Plain language in output.** "Checkpoint" not "commit." "Earlier version" not "previous SHA." The user isn't a developer.
- **Refuse destructive operations.** This skill commits forward. It does NOT push, force-push, rebase, or modify history. Those are separate explicit operations.
