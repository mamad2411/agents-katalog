---
name: publish-to-github
description: Publish a workspace's Forgejo repository to GitHub, once, on request: a GitHub repository, then a push mirror from Forgejo. For the publisher; nothing here runs unless a person asks.
---

# Publish to GitHub

Forgejo stays the home of the work. GitHub gets a copy, pushed from Forgejo, so
nothing needs the board to be reachable from the internet. This is a recipe a bot
follows when a person asks for it. It is not a board feature. The board's code
handles no GitHub credential; under Path B below the person's token is a fleet
secret for a short time, which is a cost they must agree to.

## The token never goes through the thread

GitHub must be told who the user is, and that takes a token. Nobody pastes one
into a thread, a message or a file: the board is visible to other readers. Offer
the user one of two ways and wait for their choice (`@mention`, with `meta.needs`):

- **Path A, recommended: the person does the GitHub part themselves.** No bot sees
  the token. You guide and check.
- **Path B: a temporary fleet secret.** The person adds `GITHUB_PUBLISH_TOKEN`
  under Shared secrets on the Configuration page. A fleet secret reaches **every
  bot on every box**, within minutes, until the person removes it; say so, because
  that is what they agree to by choosing B. Creating the repository also needs a
  token that can create repositories, and that has broad reach: a classic `repo`
  token reaches **all** their private repositories, and a fine-grained token with
  Administration write needs access to all repositories to create one. Say that too. (Path A has no such cost: they create the
  repository themselves and the token reaches only that one.) You use it from your environment, and the
  person removes it when you say you are done (the last step).

Also ask, once: the GitHub owner (their login or an organisation), the
repository name, and public or private (suggest private). A public repository
publishes the whole history, every commit and every branch Forgejo has, so say
that before they choose it, and ask them to search the history for secrets
first. List only the commit and the file, never the matching text, so a secret does
not land in the thread (for example
`git rev-list --all | xargs -n 50 git grep -l -i -E 'token|secret|password|key'`, or a
scanner such as gitleaks with its output kept to the commit and the file).
A leaked secret in an old commit stays public. Create nothing before the yes.

## Path A: the person sets the mirror

Give them these steps, in the thread, with their real names filled in:
1. On GitHub, create `<owner>/<name>` empty: no README, no licence, no .gitignore.
2. Create a token that can push to only that repository (a fine-grained token
   with Contents write).
3. In Forgejo, open the repository, Settings, Mirror settings, Push mirror. Set
   the address to `https://github.com/<owner>/<name>.git`, the username to their
   GitHub login and the password to the token. Turn on "sync when commits are
   pushed". Save.

Then check and finish (the last two steps, without the secret).

## Path B: you do it

`$FORGEJO_URL` and `$FORGEJO_TOKEN` are in your environment, and so is
`$GITHUB_PUBLISH_TOKEN`. The workspace's repository, `<fo>/<fn>` below, is
`repository` in `GET $BOARD/api/workspaces/<slug>`. Never print the token or put
it on a command line: it stays in the environment and goes into a request through
standard input.

1. **Check GitHub has nothing there.** A push mirror makes GitHub match Forgejo:
   it deletes any branch Forgejo lacks. Only a missing or empty repository is safe.
   ```bash
   GH_TOKEN="$GITHUB_PUBLISH_TOKEN" gh repo view "$OWNER/$NAME" >/dev/null 2>&1 && echo "exists: stop and ask the user"
   ```
   If it exists, stop and tell the user why. Do not continue.
2. **Create it, empty.** Use `--public` only if the user said public.
   ```bash
   GH_TOKEN="$GITHUB_PUBLISH_TOKEN" gh repo create "$OWNER/$NAME" --private --disable-wiki
   ```
3. **Set the push mirror** on the Forgejo repository. `sync_on_commit` pushes on
   every commit; the interval is a backstop.
   ```bash
   OWNER=$OWNER NAME=$NAME jq -n '{remote_address: ("https://github.com/" + env.OWNER + "/" + env.NAME + ".git"),
       remote_username: env.OWNER, remote_password: env.GITHUB_PUBLISH_TOKEN, interval: "8h0m0s", sync_on_commit: true}' \
     | curl -sS -H "Authorization: token $FORGEJO_TOKEN" -H 'Content-Type: application/json' \
         "$FORGEJO_URL/api/v1/repos/<fo>/<fn>/push_mirrors" -d @-
   ```
   If Forgejo answers 403, the fleet account lacks admin on the repository: say so
   and give the user the Path A steps instead.

## Check it worked

Trigger a push and look at GitHub. None of this needs the token.
```bash
curl -sS -X POST -H "Authorization: token $FORGEJO_TOKEN" "$FORGEJO_URL/api/v1/repos/<fo>/<fn>/push_mirrors-sync"
curl -sS -H "Authorization: token $FORGEJO_TOKEN" "$FORGEJO_URL/api/v1/repos/<fo>/<fn>/push_mirrors"   # last_error should be empty
```
For a public repository, `git ls-remote https://github.com/<owner>/<name>.git` lists
the branches; for a private one, ask the user to look. Say in the thread what is
live: the GitHub address, and the branches there.

## Finish

Path B only: tell the person to delete `GITHUB_PUBLISH_TOKEN` from Shared secrets now,
and unset it in your own environment. Record in the workspace's knowledge base
that the repository is mirrored to `<owner>/<name>` on GitHub, without any
credential.

## Issues from outsiders (optional)

GitHub issues do not reach a Forgejo on a laptop by themselves. If the user wants
outsiders to file issues, offer the issue bridge: `deploy/github-bridge/check`,
a routine that copies GitHub issues to Forgejo and carries comments both ways. It
is off by default and wakes no bot. Offer it; do not turn it on unasked.

## Not in scope

Exposing the board with a tunnel, a GitHub App, or keeping the GitHub token on the
board. Changing the board's code for any of this.
