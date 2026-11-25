---
name: token
description: Set up a service's credentials (PyPI, Stripe, an API, a host…) in a `.<service>/` folder at the repo root (`token`, chmod 600, and `config` on its scope), with one command that pastes the token unseen. Use when a task needs an API key or a token, or when the user wants to give one.
argument-hint: "<service> [what the token is for]"
---

Service: the first word of `$ARGUMENTS` (lowercase, e.g. `pypi`); the rest says what the token
is for. The user always pastes the secret themselves: never ask them to type it in the
conversation, never read it back, never print it, never commit it.

1. At the repo root (`git rev-parse --show-toplevel` of the main tree, not of a worktree), create
   `.<service>/` and add `.<service>/` to `.git/info/exclude` if it is not there; check with
   `git check-ignore -q .<service>/config`.
2. Write `.<service>/config`: `key=value` lines, with comments that say what the token is for,
   the scope to choose when creating it (as narrow as possible) and where it is used (a GitHub
   secret, an env variable…). Keep an existing `config`: complete it, don't overwrite it.
3. Give the direct link of the page that creates the token (e.g.
   https://pypi.org/manage/account/token/), the scope to pick, then this command, to run in
   their own terminal (not with Claude Code's `!`: it waits for keyboard input):

       read -rs -p "<Service> token: " t && printf '%s' "$t" > <root>/.<service>/token && chmod 600 <root>/.<service>/token && unset t && echo " ok"

   Nothing shows while pasting: the token stays hidden and out of the shell history.
4. When they say it is done: check that the file exists, is not empty and is `600`
   (`stat -c %a`), without displaying it. Then use it by path only: `$(cat <root>/.<service>/token)`
   inside the command that needs it, or `gh secret set <NAME> < <root>/.<service>/token` for a
   GitHub secret.
