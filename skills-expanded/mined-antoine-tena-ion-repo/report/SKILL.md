---
name: report
description: Report a defect of ion-repo (generated file, charter rule, plugin skill or hook, reusable workflow, command) to antoine-tena/ion-repo: a PR when the fix is clear, an issue otherwise, only with the user's consent. Use when a problem comes from ion-repo ([REPORT-TO-ION-REPO]) or the user asks.
argument-hint: "[what went wrong]"
---

What went wrong: `$ARGUMENTS`; without it, the defect met in this session.

Everything this skill posts is **public**, under the user's GitHub account, and ion-repo is judged
by its tracker: one clear, reproducible report is worth more than ten vague ones. Talk to the
user in their language; write the issue, the PR and its commits in **English**.

## 1. Make sure it is ion-repo's

It is when the faulty thing comes from ion-repo: a file of the template (`.copier-answers.yml` at
the root, `_src_path` pointing to `antoine-tena/ion-repo`), a rule of the shared part of
`CLAUDE.md`, a skill, hook or the status line of an ion-repo plugin, a workflow or action called from `antoine-tena/ion-repo`, the `ion-repo` or `charter`
command. It is not when it is this repo's own code or rules (they are amended here), Claude
Code itself (the user types `/bug`), or a third-party tool (uv, Copier, ruff, GitHub…), unless
ion-repo uses it wrongly.

Then rule out an old version: `ion repo doctor` says whether the ion-repo tool (`ion-repo` line) and the
repo's template (`modèle` line) are behind the latest release. If they are, offer
`/repo:update` first, then check whether the defect is still there.

## 2. Search before writing

    gh search issues --repo antoine-tena/ion-repo --include-prs "<two or three key words>"

Open and closed, issues and PRs; try two or three wordings, in French too (older issues are).
- An open issue or PR covers it: open nothing. Offer a 👍 on it
  (`gh api -X POST repos/antoine-tena/ion-repo/issues/<n>/reactions -f content=+1`), and a comment
  only if it adds something (another stack, a smaller repro, a log).
- A merged PR fixed it: the fix comes with the next release (`/repo:update`). A closed issue
  turned it down: tell the user why. Post nothing in either case.

## 3. Issue or pull request

- **Pull request** when the fix is clear and local (a few lines in one place) and comes with
  the test that would have caught it.
- **Issue** when several approaches are possible, when the change would alter what every
  generated repo receives (a new rule, file or dependency), or when the fix is unknown. In
  doubt, the issue first: a PR built on a choice not made yet gets redone.

## 4. Nothing private

This repo may be private: leave out its code, its name, its file names and paths, its data and
URLs, and anything that looks like a secret, a token, an e-mail address or a real person's
data; write `~` for the home folder. The best evidence is a repro on a fresh repo, which also
proves the defect is ion-repo's: `ion repo new "$(mktemp -d)/repro" --no-github` with the same stack
(answers in `.copier-answers.yml`, flags in `ion repo new --help`), then the steps.

## 5. Write it

Issue. Title: what is wrong, specifically (`ion repo update drops the pnpm overrides of a nuxt
repo`, not `Bug in ion-repo`). Body: the sections of the bug form
(`.github/ISSUE_TEMPLATE/bug.yml`), so that it reads like the others:

    ### What happened?

    What was run, what was expected, what happened instead; steps from `ion repo new` if possible.

    ### Output

    ```shell
    the relevant lines only
    ```

    ### ion repo version

    The `ion-repo` and `modèle` lines of `ion repo doctor`.

    ### Stack

    e.g. `django + nuxt, podman` (from `.copier-answers.yml`), or `n/a`.

    ### OS

    Linux, WSL, macOS or Other.

    ### Claude Code version

    `claude --version`, for a skill, hook or status line.

An improvement rather than a defect takes the sections of the idea form (`idea.yml`):
`### What problem would this solve?`, then `### What do you have in mind?`. Last line of the
body: `<sub>Drafted with Claude Code (/repo:report).</sub>`.

Pull request: the sections of `.github/pull_request_template.md` (What, Why, How to test,
Checklist), `Closes #<n>` when an issue exists, the output of the checks, and the same last
line.

## 6. Ask, then post

Show the user the title and the whole body (for a PR, the diff too), say that it will be
public under their GitHub account, and post only after an explicit yes. A no ends it: nothing
is posted, and it is not brought up again.

**Issue**, with `gh` logged in (`gh auth status`):

    gh issue create --repo antoine-tena/ion-repo --title "<title>" --body-file <file>

No `--label`: the maintainer labels at triage. Without `gh`, give the user the prefilled form
instead, each value URL-encoded:
`https://github.com/antoine-tena/ion-repo/issues/new?template=bug.yml&title=…&what=…&output=…&version=…&stack=…&claude-code=…`.

**Pull request.** If `gh api user --jq .login` prints `antoine-tena`, the user is ion-repo's
maintainer: no fork, no PR, the fix goes into their ion-repo checkout following its `CLAUDE.md`.
Anyone else:
1. Outside this repo, in a temporary folder: `git clone https://github.com/antoine-tena/ion-repo`,
   then `git switch -c fix/<short-name>` (the clone starts on `develop`).
2. Read the clone's `CLAUDE.md` and `CONTRIBUTING.md`: for this work they replace the rules of
   the user's repo (branches, commits, checks).
3. The smallest change that fixes it, and the test that would have caught it. `uv sync`, then
   the checks of `CONTRIBUTING.md`: all must pass. If they fail for a reason you cannot see,
   open an issue instead, with what you found.
4. Commits: `fix: …` title of 50 characters at most, no `Co-Authored-By: Claude` or
   `Claude-Session:` trailer, no `--author`.
5. After the yes: `gh repo fork --remote` (the fork becomes `origin`, ion-repo `upstream`),
   `git push -u origin fix/<short-name>`, then
   `gh pr create --repo antoine-tena/ion-repo --base develop --head <login>:fix/<short-name> --title "<title>" --body-file <file>`.

## 7. After

Give the link. The fix reaches this repo with the next ion-repo release (`/repo:update`, or the
prompt at the start of a session). Meanwhile ion-repo's files in this repo stay as they are
([REPORT-TO-ION-REPO]); if the defect blocks the user, a workaround that does not touch them (a
setting, a command run by hand) is fine, and worth a line in the issue.

One defect per issue, one issue per defect; no `@` mention of the maintainer (they watch the
repo); never more than one comment or reaction on the same issue.
