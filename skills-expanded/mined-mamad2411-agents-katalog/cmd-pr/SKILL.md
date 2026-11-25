---
name: cmd-pr
description: Command — Push the current branch and open a Pull Request with a description focused on what reviewers need
---

# /pr

Drafts a PR description, **waits for your explicit confirmation**, then pushes the branch and opens the PR via `gh`.

Argument `[title]` (optional): explicit PR title. If omitted, derived from the most recent commit message.

## Plan-mode guard (do this first)

If plan mode is active, STOP. This command pushes commits to the remote and creates a public PR — both are write operations. Plan mode prohibits writes. Tell the user: "Plan mode is active. /pr is a write operation (push + PR creation). Exit plan mode to proceed."

## Steps

1. **Draft the description.** Invoke `Skill(pr-description)` to produce: Summary, Why, Test plan, Out of scope, Notes for reviewers.

2. **Show the proposed title + body to the user** for review. Format:

   ```
   Proposed PR:
   Title: <title>
   Body:
   ---
   <body>
   ---
   ```

3. **WAIT for explicit user confirmation.** Type "approved" or paste edits. Do NOT proceed automatically. If running in a non-interactive context (no human in the loop), STOP and report that this command requires human confirmation.

4. **On confirmation, execute.** Assign the approved title and body to shell variables first, then invoke. This prevents flag-injection if the title contains `--label` lookalikes or other shell metacharacters — the variables are never interpolated into the command line as literals.

   ```bash
   # Assign the approved values as shell variables (NOT interpolated into the command string)
   TITLE='<approved title, exactly as confirmed>'
   BRANCH="$(git rev-parse --abbrev-ref HEAD)"

   git push -u origin "$BRANCH"
   gh pr create --title "$TITLE" --body "$(cat <<'PRBODY'
   <approved body, exactly as confirmed — single quotes around PRBODY prevent variable expansion inside>
   PRBODY
   )"
   ```

   Substitute the approved title literally into the `TITLE='...'` assignment (using single quotes prevents shell expansion). The body content goes inside the `<<'PRBODY'` heredoc — also single-quoted, so backticks/`$`/`!` in the body don't expand.

   If the user omitted the `[title]` argument, derive the title from the most recent commit subject BEFORE Step 3 (so it can be shown for confirmation):

   ```bash
   TITLE=$(git log -1 --pretty=%s)
   ```

## Error handling

- **`git push` fails** (no upstream / protected branch / auth failure): report the exact stderr to the user, do NOT retry, do NOT attempt to force-push. Suggest checking `git remote -v`, branch protection rules, or `gh auth status`.
- **`git push` succeeds, `gh pr create` fails** (duplicate PR / invalid base / network error): the branch is already on the remote. Print the drafted title + body and a copy-pasteable `gh pr create --title "$TITLE" --body "..."` command so the user can finish manually. Do NOT delete the pushed branch.
- **`gh` not authenticated**: stop and tell the user to run `gh auth login`. Print the drafted body + the `gh pr create` command they can run manually.
- **`gh` not installed**: print the drafted body + a manual `gh pr create` command to run after installing.

Requires `gh` CLI authenticated.

## Arguments

`[title]`
