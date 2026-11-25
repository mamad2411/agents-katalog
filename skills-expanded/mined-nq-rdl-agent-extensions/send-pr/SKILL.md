---
name: send-pr
license: CC-BY-4.0
description: >-
  Commit the pending changes, push a feature branch and open a GitHub pull
  request with a conventional-commit title, a structured body and requested
  reviewers. Use when the user asks to "ship", or to commit, push and raise a
  PR.
disable-model-invocation: true
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Commit, Push and Raise PR

Invoking this skill authorizes: creating a feature branch when needed,
committing the pending changes, pushing that branch, opening one pull request,
and requesting the reviewers the user names. It does not authorize pushing to
the default branch, force-pushing, merging, or choosing reviewers yourself.

## Steps

1. **Inspect.** `git status`, `git diff`, `git diff --staged`, the current
   branch and `git remote -v`. Derive the commit message and PR text from the
   changes; do not ask the user to describe them. With nothing to commit and
   nothing unpushed, stop and say so. A missing remote or an unauthenticated
   `gh` does not stop the local steps: still create the branch and commit,
   then report the step that could not run.
2. **Branch.** Never commit to or push the default branch
   (`git symbolic-ref --short refs/remotes/origin/HEAD` prints `origin/<name>`;
   without it, treat `main` or `master` as the default).
   If you are on it, create `<type>/<short-slug>` first, for example
   `fix/negative-totals`, and carry the uncommitted changes onto it.
3. **Stage by name.** `git add path/to/file …`. Leave out `.env*`, keys,
   credentials, large binaries and build output, even when untracked, and say
   what you left out. Use `git add -A` only after confirming none are present.
4. **Commit.** Conventional Commits subject (types and breaking-change rules:
   `gh:conventional-commits`), imperative and lowercase, 50 characters or fewer
   where possible and never more than 72; wrap the body at 72. Follow the
   repository's commit conventions and hooks. If the changes span several
   concerns, say so, but make one commit unless told otherwise.
5. **Push.** `git push -u origin HEAD`. On failure (no remote, authentication,
   rejected push), stop and report the error; do not force-push.
6. **Create the PR.** Write the body (template below) to a file from `mktemp`,
   then:

   ```bash
   gh pr create --title "<commit subject>" --body-file "$body_file" \
     [--base <branch>] [--reviewer <login>[,<login>…]]
   ```

   Omit `--base` unless the user named one or the repository documents a
   different target; `gh pr create` then uses the repository's default branch.
   Remove the body file afterwards. If `gh` fails, report its error together
   with the pushed branch name. Do not retry with guessed bases or remotes:
   when `gh` cannot resolve the repository or authenticate, every `gh` command
   fails the same way.
7. **Reviewers.** Use the logins named in the request (`--reviewer` above). If
   none were named, ask once after creation and add them with
   `gh pr edit --add-reviewer <login>`; skip if the user declines.
8. **Verify.** `gh pr view --json url,baseRefName,headRefName,reviewRequests`.
   Report the PR URL and the reviewers GitHub lists, not the ones you asked
   for.

## PR body

The PR title is the commit subject.

```markdown
## Summary
[2-3 sentences: what this PR does and why]

## Changes
[Key modifications, grouped logically]

## Test Plan
- [ ] [Specific scenario derived from the change]
- [ ] [Edge case to check]

## Notes for Reviewers
[Uncertainties, alternatives considered, files to scrutinise]
```

Test-plan items must be specific to the change, not generic placeholders.
