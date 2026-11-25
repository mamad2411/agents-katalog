---
name: lantern-bitbucket
description: List, read, open and comment on Bitbucket Cloud (bitbucket.org) pull requests from the terminal with the account added in Lantern — list open pull requests, show one, push the current branch and open a pull request into a target branch, comment on one. The workspace and repository come from the git remote. Use whenever the user asks to "open a PR", "wystaw PR", "create a pull request", "raise a PR", "what PRs are open", "show PR 12", "comment on the pull request", or finishes work on a branch in a repo whose remote is on bitbucket.org. Needs no setup beyond adding the Bitbucket account in Lantern (command palette, Integrations), which puts BITBUCKET_EMAIL and BITBUCKET_API_TOKEN in the run's environment, or hands them to the script on request when the chat was not started by Lantern; nothing to install or configure by hand. If the user already has their own Bitbucket skill in the project or in ~/.claude/skills, use that one instead; this is the default for projects that have none. A lantern-delegate delegate opens its pull request through this skill too, by way of lantern-delegate's pr-create.mjs, which adds the identity checks. Never merges, approves, deletes or force-pushes.
---

# Bitbucket pull requests, with the Lantern account

One script, `scripts/bitbucket.mjs`, no dependencies (Node 18 or newer). Run it from inside the
repository: the workspace and repo are read from the remote that points at bitbucket.org. It never
prints the token, an Authorization header or a URL carrying one. `scripts/` below is this skill's
folder, so from the repository root the script is `node .claude/skills/lantern-bitbucket/scripts/bitbucket.mjs`
(or `.agents/skills/...` under Codex).

## Commands

```
node scripts/bitbucket.mjs list
node scripts/bitbucket.mjs show 12
node scripts/bitbucket.mjs create --title "Add retry to the sync job" --body-file .ai/tmp/pr-body.md --target main
node scripts/bitbucket.mjs create --title "..." --dry-run
node scripts/bitbucket.mjs comment 12 --body "Rebased on main."
node scripts/bitbucket.mjs check
node scripts/bitbucket.mjs create --title "..." --branch feat/retry --target main
node scripts/bitbucket.mjs description-block 12 --name run:cost --file .ai/tmp/cost.md
```

- `list` takes `--limit` (1 to 50) and `--json`; `show` takes `--json`.
- `create` pushes the current branch (a plain `git push`, never forced) and opens one pull request
  from it into `--target`, by default the remote's default branch. It refuses a detached HEAD, uncommitted
  changes to tracked files (untracked scratch files such as a PR body are fine), a source equal to the target and a target that is not on the remote. When the branch already
  has an open pull request it pushes the new commits and prints that pull request instead of opening a
  second. `--dry-run` checks everything and prints what it would do without pushing or sending.
  `--branch <name>` pushes HEAD to that branch name and opens the pull request from it, for a checkout whose
  local branch has another name.
- `comment` takes the text as `--body "<text>"` or `--body-file <path>`.
- `check` confirms the account resolves (environment, or the running Lantern over its socket) and that the
  token can write pull requests on this repository (`x-oauth-scopes`), and prints where the account came
  from, never a token. `--offline` only resolves the account and calls nothing; `--json` prints it as data.
- `description-block <id> --name <marker> --file <path>` puts the file's text between `<!-- name -->` and
  `<!-- /name -->` in the pull request description, replacing an earlier block of that name, so a second run
  never stacks a second copy. The marker is lowercase letters, digits, `:`, `_` and `-`.
- With several remotes on bitbucket.org, pass `--remote <name>`.
- There is no merge, approve, decline, delete or force-push command, and none is to be improvised.

## Conventions are the user's

This skill says how to connect to Bitbucket and run its commands. It never says what goes in a title, body or comment: people and teams have their own rules, and their own skills for them.

Before the first `create` or `comment` of a session, run `node scripts/bitbucket.mjs conventions` (read-only, offline; `--json` for data). It lists, with a path and one line each, the repository's own pull request templates, the user's skills about pull requests or tickets (project and home `.claude/skills` and `.agents/skills`) and any template saved for this project. It prints names and paths only, never the contents.

- Something found: ask the user once which to follow ("I found X; use it?"), never choose silently. On yes, read that file or skill and follow it yourself.
- Nothing found: ask whether to write a pull request template for this project. On yes, draft it with the user, write it to a file they approve and keep it with `node scripts/bitbucket.mjs template save pr --file <path>` (it refuses to replace a saved one without `--force`); `template show pr` prints it later, and you fill it in. On no, use the user's own wording.
- The skill supplies no default title, body, comment, label or transition text.

## Where the credentials come from

1. `BITBUCKET_EMAIL` and `BITBUCKET_API_TOKEN` in the environment, when set. Nothing else is contacted.
2. Otherwise the running Lantern, asked over a local socket for the account of the project the script
   runs in (the working directory). The answer is used in memory for that one run: it is never
   written to a file, the environment or the output. The socket is `LANTERN_CREDENTIAL_SOCKET` when
   that is set, else `lantern.sock` in Lantern's user-data folder (`Lantern`, or `Lantern-dev` for a
   dev run).

This is what makes the skill work in a chat inside Lantern's embedded editor, which Lantern did not
start and so could not give an environment.

## When it fails

- `Missing BITBUCKET_EMAIL, ...`: the account is not in Lantern for this run. The message ends with the
  reason Lantern gave: no Bitbucket account added yet, or none chosen for this project (the user chooses
  an account for this project in Integrations, any account they added, whatever the remote), its store
  locked or unavailable, a folder that is not an opened project, or Lantern not running. Tell the user
  what it says; do not ask them to paste a token into the chat or a file.
- `refused (401)`: the account was not accepted; it may have expired.
- `refused (403)`: the token lacks the pull request scopes for this repository.
- `git push` failures are the machine's git credentials, not Lantern's account; report the message.

Commit the work first (the `lantern-commit` skill, if present); `create` never commits for you.
