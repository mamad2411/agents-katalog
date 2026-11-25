---
# okl-fingerprint: sha256:089ec64053d7ecf12f43a010c4fa8617de594c2af2685732d38a5f0d968af7cb
name: okl-review
description: Check the code you just wrote against this repo's okl lessons, each lesson on its own in a fresh context, and fix what a check finds. Use when the Stop hook asks for the review after writing, before you open or update a pull request, or when asked to review a change against the lessons.
allowed-tools: Bash(okl check:*), Bash(okl show:*), Bash(python3 -m okl check:*), Bash(python3 -m okl show:*)
---

# okl-review: the review after writing

okl keeps the lessons this repo has learned. This skill checks a change against them before it
ships. The steps come from okl itself (`okl check --change` prints them), so they stay the ones
that were measured: follow them as printed, and do not shorten them.

## 1. Run it where the change is

In the checkout or worktree that holds the code, run:

```
okl check --change
```

It compares with the remote's default branch, then `main`, then `master`. If the work started
from another branch, name it: `okl check --change <branch>`. If the work is in another
worktree, run it there (`cd <worktree> && okl check --change`): from any other checkout it does
not see the work. The Stop hook names the worktrees that had work in the last hour.

If `okl` is not a command in this shell, the repo runs okl another way, and every `okl` in these
steps and in okl's output means that command. Use the first of these that starts:

1. the command the Stop hook named, where it said `okl` is not a command in this shell;
2. the `okl_bin` value in `.okl/config.json` (in a worktree, the main checkout's);
3. `python3 -m okl`.

## 2. Read every page

A long review comes in pages, each short enough to arrive whole. Page 1 names the command for
each further page. Run each as a command of its own, and read every page before you pick.

## 3. Follow its steps

In short: say what the change does, pick the ten lessons it is most likely to break, and check
each on its own in a fresh context, with the lesson's full text (`okl show <id>`) and the
question the steps give. Fix what a check finds, and run the tests that cover it. The printed
steps are the authority; this summary is not.

## 4. Report

Say which lessons you checked, which the change broke and what you changed for each, and which
needed nothing. If you checked them in one context instead of fresh ones, say so: that review is
weaker.

## When it cannot run

- Nothing changed since the base: say so. There is nothing to review.
- okl is not set up here, or cannot reach its store (it exits 2 and says why): say so.
- No okl command starts (`command not found`, from each of the three above): say so, and name
  what you tried.

Never report a clean review that did not run.
