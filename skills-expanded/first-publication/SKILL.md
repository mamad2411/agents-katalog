---
name: first-publication
description: "Use before a repo's first push. It is irreversible."
version: 1.1.0
author: coder role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, github, publication, history-rewrite, privacy, identity]
    category: software-development
    related_skills: [open-source-release]
---

# First publication

Creating a remote and pushing to it for the first time. Also: rewriting
history that has already been pushed. The window where mistakes are cheap is
**before** the first push and nowhere after it.

Decide first WHICH identity (account, commit email, project folder) publishes
WHICH project, and keep that map in one private place of your own, read before
every publication. This skill covers the publication mechanics.

## The rule that drives everything else

**A force-push does NOT delete orphaned commits on GitHub.** It unlinks them
from the branch: they vanish from the history list, and they stay on the
server, reachable by anyone who knows the sha.

    github.com/<owner>/<repo>/commit/<old-sha>     still loads
    gh api repos/<o>/<r>/contents/README.md?ref=<old-sha>   still returns it

Measured, not assumed: after squashing 28 commits into 1 and force-pushing,
the orphaned commit still served the full old README. The branch listed one
sha; the object was still there.

So: **fix the README wording, the licence, the emails and the leaks BEFORE
the first push.** Afterwards the only true removal is deleting the repo.

## Order of operations

1. scan (below) — failures here cost nothing
2. `gh auth switch --user <identity>` — before touching any remote
3. `gh repo create <owner>/<repo> --private --source=. --remote=origin`
   — never `--push`; create, verify private + owner, then push
4. `git push -u origin main`
5. verify from the HOST side, not from the local clone

## Scan the HISTORY, not the working tree

A clean tree proves nothing — the leak may sit in an old commit.

    git log --format='%ae %ce' | sort -u          # author AND committer
    git grep -lniE '<pattern>' $(git rev-list --all) -- .
    git log --all --pretty=format: --name-only | sort -u | grep -iE '<private>'
    git ls-files | grep -iE '(^|/)\.env$|\.pem$|\.key$|id_rsa|credentials'

`git log --format='%ae'` alone misses the **committer** field, which is a
separate identity and a separate leak. Check both.

Also scan for what must never have existed in ANY commit, not just the tip:
private dirs, agent instruction files, databases, real home paths
(a Windows user folder, `/home/<user>`, `/Users/<user>`).

## Verify from the host, never from the clone

The local repo cannot tell you what the server holds.

    gh repo view <o>/<r> --json name,isPrivate,defaultBranchRef
    gh api 'repos/<o>/<r>/commits?per_page=100' --jq 'length'
    gh api 'repos/<o>/<r>/commits?per_page=100' \
      --jq '[.[] | select(.author.login != "<identity>")] | length'   # must be 0
    gh api repos/<o>/<r>/git/trees/main?recursive=1 --jq '.tree[].path'
    gh api repos/<o>/<r> --jq '{description,homepage,topics,has_pages,has_wiki}'

A commit can carry the right email and still show as an unknown author if the
address is not attached to the account. Check `.author.login`, not only
`.commit.author.email`.

## Multiple accounts on one machine: two separate traps

- `gh auth login` authorises whoever the **browser** is signed in as, not the
  name typed in the command → private window, sign in as the target identity
  only, then paste the device code.
- `gh auth switch --user <identity>` before every remote operation: the
  credential helper hands over the **active** account's token, regardless of
  which folder you are in.

Confirm with `gh api user --jq '{login,id}'` and match the id against the
noreply email in the commits. Same number or stop.

Never run `gh auth login` or `gh auth refresh` on the user's behalf — the
device code goes in their browser. Hand them the exact command and wait.

## Deleting a repo is the only real undo

`gh repo delete` takes the object store with it. Cheap while the repo is
private with no forks, no issues, no stars; impossible once it is public and
cloned.

Delete, recreate, push, then **prove the old shas are gone** — the delete is
the only step whose success is worth verifying, and the check is the same
call that proved they survived the force-push:

    gh api repos/<o>/<r>/commits/<old-sha>      # must fail: 404 / 422

Run it against the sha whose content you fetched BEFORE the delete, so the
before-and-after is the same query. Anything that still resolves means the
object store was not replaced.

The scope is not granted by default and cannot be self-issued:

    gh auth refresh -h github.com -s delete_repo     # the USER runs this

The alternative — asking host support to garbage-collect — is slow and puts the
leak in a support ticket. Worse on every axis.

## Before rewriting history, back up and PROVE the backup

A squash or `filter-repo` that drops a file is invisible until it matters.

    cp -r <repo> "$TMPDIR/<name>-prebackup-$(date +%Y%m%d-%H%M%S)"
    diff -r --exclude=.git <repo> <backup>      # empty output or stop

Squash to one commit, keeping the tree:

    git checkout --orphan squashed && git add -A && git commit -m "..."
    git branch -D main && git branch -m main

Then purge the local leftovers, or the old objects stay in this clone:

    git reflog expire --expire=now --all && git gc --prune=now
    git fsck --unreachable        # empty = gone locally

Local purging does **not** touch the host. See the rule at the top.

## Squash vs keep history — state the cost, then do as asked

Squashing to one commit permanently destroys `git blame`, `git bisect`, and
any version convention that counts commits. Say that once, plainly, with the
alternative (scrub the string from every commit with `git-filter-repo`,
available via `uvx git-filter-repo`), then execute the choice made. It is the
owner's repo.

## Public README language

Generic, never personal. No `your sister`, `your friends`, `people you both
know`; no `her`/`his` attached to example names. A reader may be an archivist
or a photographer sorting a client's files — every kinship word narrows the
tool to one kind of user and reads as amateurish.

`your` aimed at the **operator** is correct and stays: `your machine`, `your
photos`, `your own LLM`. It assumes nothing about who is in the pictures.

Sweep before publishing:

    grep -niE '\b(sister|brother|friend|family|mum|dad|wife|husband|kids)\b' README.md
    grep -niE '\b(her|hers|she|his|him|he)\b' README.md

## Verification

Done means, checked against the host and not from memory: repo private, owner
correct, one branch, commit count matches local, every commit attributed to
the publishing identity, remote file list free of private material, and
description/homepage/topics/Pages/wiki all empty or off.