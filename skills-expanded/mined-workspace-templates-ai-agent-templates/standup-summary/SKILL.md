---
name: standup-summary
description: Summarizes what you changed since yesterday from git history and the working tree, in a form you can read out at standup.
disable-model-invocation: true
---

Summarize recent work for standup. Scope: $ARGUMENTS (my commits since the last working day if empty).

1. Get the author from `git config user.name`. Choose the start: yesterday, or Friday if today is Monday, unless the user gave a range.
2. Run `git log --all --author="<name>" --since="<start>" --pretty="%h %ad %s" --date=short` and `git status --short`. Check `git stash list` and the current branch.
3. Group the commits by branch or feature. Read the diff of a commit only when its subject is vague.
4. Write three parts, each two or three bullets at most: **Done** (finished and merged or pushed), **In progress** (uncommitted or unpushed work, with the branch), **Blocked or needs input** (only if the history shows reverts, long-lived drafts or failing work; otherwise write "nothing visible").
5. Do not invent plans for today. End with one line asking what to add that git cannot know.

Keep it under 120 words, in the first person, plain language.
