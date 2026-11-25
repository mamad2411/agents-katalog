---
name: rexmod
description: Work with the rexmod Changes panel and editor pane in Rex. Use when the user's message carries review comments from their editor, when you want to show the user a file or line in their editor pane, or when you need the change sets the panel shows (last turn, uncommitted, branch).
---

# rexmod

The user runs you in a Rex pane with rexmod: a Changes panel on the right of
the window, a Neovim editor pane beside you, and review comments they leave in
that editor. The `rexmod` command (`~/.local/bin/rexmod`) talks to all of it.
It finds this tab from `REX_SESSION`, which your shell already has.

## Review comments

Comments the user left for you arrive with their next message, as a list of
`file:line`, the code, and the comment. Treat each one as a request about that
exact spot: address every comment, then say briefly what you did for each.

To see what is still waiting (comments not yet delivered):

```sh
rexmod comments list --pending
```

## Show the user code

Open a file at a line in the editor pane next to you (it is created if
missing, and reused after that):

```sh
rexmod open path/to/file.go:42
```

Do this when you point the user at something specific: the bug you found,
the function you changed, the place they should review.

## Change sets

The panel's tabs as JSON (files with added/deleted line counts):

```sh
rexmod changes --mode last-turn     # what your last turn changed
rexmod changes --mode uncommitted   # working tree vs HEAD
rexmod changes --mode branch        # this branch vs its base
```

Don't edit the panel's state under `.git/rexmod/`; rexmod manages it.
