---
name: resolve-conflicts
description: Finds every conflicted file after a merge or rebase, resolves each with written reasoning and runs the checks before you continue.
disable-model-invocation: true
---

Resolve the merge or rebase conflicts in this repository. Notes: $ARGUMENTS

1. Run `git status` to see whether a merge, rebase or cherry-pick is in progress, and `git diff --name-only --diff-filter=U` for the conflicted files.
2. For each file, view the three versions (`git show :1:file`, `:2:`, `:3:`) and the commit messages on each side (`git log --merge -p -n 3 -- file`). Decide what each side intended.
3. Resolve by combining intents, not by picking a side. For lockfiles, regenerate with the package manager instead of editing markers. For generated files, rerun the generator.
4. Remove every marker and check with `grep -rn "<<<<<<<\|>>>>>>>" .` that none remain.
5. If a conflict changes behavior and you cannot tell which intent wins, leave the file unresolved and ask.
6. Run lint, type check and tests.

Print a table of file, resolution and reason. Then `git add` only the files you resolved, and ask before `git rebase --continue` or `git commit`. Never run `--abort` or `checkout --theirs` without asking.
