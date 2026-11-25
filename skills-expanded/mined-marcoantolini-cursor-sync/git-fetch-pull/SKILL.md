---
name: git-fetch-pull
description: Fetches all remotes then pulls the current branch’s upstream.
disable-model-invocation: true
---

# Git fetch and pull

## Steps

1. From the repo root: `git fetch --all`.
2. `git pull` on the **current** branch (keep the repo’s configured merge/rebase behavior unless this message asks for one explicitly).
3. **Done when:** fetch finished and the current branch is up to date with its upstream, or you have reported a hard stop (see below) and taken no further git mutation.

## Hard stops

- No upstream → explain; suggest `git branch -vv` and setting upstream. Do not invent remotes.
- Uncommitted changes block the pull → report and stop. Stash/discard only if the user says so in this message.

## Guardrails

- No destructive fetch refspecs, force-pull, or `reset --hard` unless explicitly requested.
- Do not create commits or merge other branches as part of this run.
