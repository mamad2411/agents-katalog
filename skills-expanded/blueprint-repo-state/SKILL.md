---
name: blueprint-repo-state
description: "Confirm the folder is a clean clone of a GitHub repository on its up-to-date default branch, and keep the build's own notes out of git."
---

# The repository, as it stands

The user cloned this repository and trusted the folder in Claude Code. Everything that follows commits,
pushes and opens pull requests here, so it must start from exactly what GitHub has.

1. Confirm the project folder is the repository root and `origin` is on GitHub. `gh auth status` must pass;
   if it does not, ask the user to run `gh auth login` (use the base pack's `guides/gh-login.md`) and stop.
2. Add `.blueprint/` as its own line to `.git/info/exclude`. That file is local to this clone and changes
   nothing in the repository; it keeps the build's notes from ever being committed. Never add it to
   `.gitignore` — that would be a change to their repository.
3. If the working tree has changes, **ask** what to do and stop. Never stash, reset, discard or commit
   someone else's changes.
4. Check out the default branch (`sh <base pack>/checks/default-branch.sh` prints it) and bring it up to
   date with `git pull --ff-only`. If that fails, ask.

Change nothing in the repository in this step — `.git/info/exclude` belongs to this clone, not to the
repository, and checking out or fast-forwarding the default branch changes nothing that is theirs.

Done when the check passes: the folder is the repository root, origin is on GitHub, gh is signed in,
`.blueprint/` is excluded, the tree is clean, and the default branch matches origin.

## Always

- Read `.blueprint/spec.md` if it exists. It is the agreed plan; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Never force-push, rebase, or rewrite history. Never delete a branch you did not create.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
