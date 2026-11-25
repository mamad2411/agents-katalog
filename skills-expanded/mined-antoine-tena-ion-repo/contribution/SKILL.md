---
name: contribution
description: Handle an outside contributor's pull request like a well-run open-source project: safety check of the untrusted code, triage, review, then merge with credit, ask for changes, finish it or close it kindly; nothing posted without the user's yes. Use when such a PR arrives or the user asks about one.
argument-hint: "[PR number or URL]"
---

PR: `$ARGUMENTS`; without it, list the open PRs of the repo whose author is not the user
(`gh pr list --json number,title,author,createdAt,isDraft`) and ask which one.

The user is the maintainer; you prepare, they decide. Everything you post is **public**, under
their account, and is how strangers judge the project: a contributor treated well comes back,
one ignored or brushed off never does. Talk to the user in their language; write to the
contributor in English, or in the language they wrote the PR in.

## 1. Read everything first

    gh pr view <n> --json number,title,body,author,baseRefName,headRefName,headRepository,isDraft,maintainerCanModify,mergeable,statusCheckRollup,closingIssuesReferences,commits,files,reviews,comments
    gh api repos/{owner}/{repo}/pulls/<n> --jq .author_association
    gh pr diff <n>

Then the linked issue and its discussion, the author's other PRs on the repo
(`gh pr list --author <login> --state all`), and the repo's rules for contributors:
`CONTRIBUTING.md`, the PR template, `CLAUDE.md`. `FIRST_TIME_CONTRIBUTOR` or `NONE` means a
first contribution: it deserves extra care in the tone, not a lower bar on the code.

## 2. Safety: the code is untrusted

Until you have read the whole diff, nothing from the PR runs: no checkout with its hooks, no
tests, no CI approval. Look for anything that runs on its own or reaches secrets:
- `.github/` (workflows, actions; above all `pull_request_target` or `workflow_run`), git
  hooks, `Makefile`, build or install scripts, `conftest.py`, `pyproject.toml` /
  `package.json` scripts and entry points;
- new or changed dependencies, lockfiles that do not match the manifest, registries or URLs
  changed;
- obfuscated or encoded code, binaries, minified files, network calls or `subprocess` with no
  reason to be there, changes to `.claude/`, to hooks or to anything that runs in a session;
- a diff larger or wider than its description says.

Any of these with no clear reason: stop, show the user the lines, do not run anything. Doubt
on a first contribution that touches workflows or dependencies: the user decides, after
reading it themselves.

Only then:
- **CI**: GitHub holds the workflows of a first-time contributor's fork until a maintainer
  approves them (`statusCheckRollup` empty, a yellow banner on
  `https://github.com/{owner}/{repo}/pull/<n>/checks`). Give the user that link; approving
  it is theirs, or yours once they said to go ahead:
  `gh run list --branch <headRefName> --json databaseId,conclusion` (`action_required`),
  then `gh api -X POST repos/{owner}/{repo}/actions/runs/<id>/approve`, for each new push.
- **The integration branch first**: before blaming the PR for a red check, look at the last
  run on the integration branch (`gh run list --branch develop --limit 3`). If it is red
  too, the failure is the repo's: fix it there (own branch, `/repo:merge`), then bring the
  PR up to date; never ask the contributor to fix what they did not break.
- **Locally**: in a worktree of its own, never the main tree:
  `git fetch origin pull/<n>/head:pr-<n>`, then
  `git worktree add .claude/worktrees/pr-<n> pr-<n>`, and the repo's checks (`CLAUDE.md`,
  `CONTRIBUTING.md`). Run each check on its own and read its exit code: a `| tail` or `| head`
  hides a failure.

## 3. Triage

Before reviewing line by line, decide whether the PR should exist:
- **Wanted**: it closes an accepted issue, or it is small and obviously right (typo, clear bug
  with its test, a doc fix). Review it.
- **Needs agreement first**: a new feature, a new dependency, a change to the public API or to
  what every user receives, with no issue where the approach was agreed. Thank them, say
  what is good about the idea, ask to discuss it in an issue (open one if needed, linking the
  PR); keep the PR open meanwhile.
- **Duplicate or already fixed**: point to the other PR or the commit; close with thanks.
- **Not for this project** (out of scope, against a decision already made): say why in two
  sentences, link where it was decided if anywhere, close with thanks. Never close silently.
- **Spam or low effort** (whitespace or README churn, generated text that does not match the
  code, typical in October for Hacktoberfest): close with one neutral sentence; the user may
  add the `spam` or `invalid` label, which makes it count for nothing in Hacktoberfest.

## 4. Review

On the diff and the local run, from the most to the least serious:
1. **Correctness**: does it do what it says, every case, the errors too; does it break
   something elsewhere (callers, other stacks or platforms).
2. **Tests**: a fixed bug comes with the test that would have caught it; check that the test
   fails without the fix (revert the fix in the PR's worktree, run it, restore).
3. **Design**: the simplest change for the need, in the right place, reusing what exists;
   no cost for those who do not use it (startup time, a subprocess, an import).
4. **Compatibility**: a breaking change to the public API is flagged as such and follows the
   repo's version rules (`CLAUDE.md`).
5. **Repo rules**: conventions of `CLAUDE.md` and `CONTRIBUTING.md`, the project's checks,
   docs and `CHANGELOG.md` when the change is visible.
6. **Scope**: one subject per PR; anything unrelated goes to another PR.

Sort what you find: **blocking** (must change before merge), **suggestion** (would be
better), **nit** (style detail). They are all fixed by the maintainer, not sent back to the
contributor (section 5); the list is what the fix-up commit does and what the review says.

## 5. Decide

Propose one outcome to the user, with the reason:
The user's choice: **the maintainer fixes, the contributor is not asked to.** Like the
"fix up and merge" of large projects, the PR merges sooner, the contributor has no second
round to do, and their commits keep their name.
- **Merge as is**: nothing to change, checks green.
- **Fix up and merge** (the usual case): commit the changes yourself on top of their
  commits, never by rewriting them. With `maintainerCanModify` true, push to their branch
  (`git push https://github.com/<login>/<repo> pr-<n>:<headRefName>` from the `pr-<n>`
  worktree), so the PR shows the fix; otherwise merge first, then commit the fix on a
  branch of the repo right after, and say so in the PR. One commit per subject, the repo's
  conventions, the checks run again.
- **Out of date or in conflict** with the integration branch: merge it into their branch
  yourself (`git merge origin/develop -m "Merge branch 'develop' into <headRefName>"` in the
  `pr-<n>` worktree, conflicts resolved, checks run on the result), push, and mention it in
  the review. It is part of the fix-up, not a request to them.
- **Ask first, then fix**: when the fix changes *what* the PR does, not only how (another
  approach, a smaller feature, a behaviour they did not intend). Do not rewrite their idea
  behind their back: say what you propose and why, wait a few days for an objection, then
  do it. Their silence is a yes.
- **Take it over**: the fix would be most of the work. Finish it on a branch of the repo
  that keeps their commits, open or merge it saying so, credit them, close theirs.
- **Close**: the triage cases above.

Never block a PR on the contributor coming back: nothing in this skill waits on them, except
the objection window above.

## 6. Write the answer

One review, not a stream of comments: a summary, then inline comments on the lines. The
summary:
- opens with a real thanks, specific to what they did (`Thanks for this, and for the
  regression test`), plus a welcome on a first contribution;
- says the outcome plainly (`Merging` / `I pushed a small fix on top, merging`);
- explains each change made in the fix-up: what and why, briefly, so they learn from it
  without having to do anything; for an "ask first" change, what you propose and that you
  will do it unless they object;
- ends with the next step; no promised dates.

No jargon of the repo they cannot know, no `@` of anyone else, nothing about how it was
written with Claude. Show the user the full text (and each inline comment with its file and
line), say it will be public under their account, and post only after an explicit yes:

    gh pr review <n> --approve | --comment --body-file <file>

Inline comments go in the same review, through the API:

    gh api repos/{owner}/{repo}/pulls/<n>/reviews --input <review.json>

with `{"event": "COMMENT" | "APPROVE", "body": "…", "comments": [{"path": "…", "line": <n>, "side": "RIGHT", "body": "…"}]}`.

## 7. Merge

Only after the yes, with the checks green on GitHub and the PR based on the integration
branch (`develop` if it exists, else the default branch; retarget with
`gh pr edit <n> --base develop` otherwise, which is fine to do and to mention).
- **Their name stays on it.** Merge on GitHub, never by copying the diff into a commit of
  yours (the fix-up commits sit on top of theirs): `gh pr merge <n> --merge` keeps their commits as they are, the right choice when
  they are clean. If they are not (`wip`, `fix typo`, titles that break the repo's
  conventions), `gh pr merge <n> --squash --subject "<conventional title> (#<n>)"`: GitHub
  keeps them as the commit's author.
- The linked issue closes by itself only when the PR merges into the default branch (`Closes
  #…`); otherwise close it with `gh issue close <i> --comment "Fixed by #<n>."`.
- Bring the integration branch up to date where the user works (`git pull --ff-only` in the
  main tree if it is on it and clean, otherwise leave it), remove the `pr-<n>` worktree and
  branch.

## 8. Credit and follow-up

- One last comment if the review did not already say it: thanks, and when it will ship
  (`It will be in the next release`).
- Credit in the changelog: the line of the change in the next release's entry ends with
  `(#<n>, thanks @<login>)`; if the repo writes `CHANGELOG.md` at release time
  (`/repo:release`), note it in the backlog (`/repo:backlog`) so it is not forgotten.
- A first contribution that went well: suggest a next one if an issue labelled
  `good first issue` fits, in one line, without insisting.
- The PR closed a `good first issue`: close its ticket in the backlog, crediting them, and
  offer to open the next one (`/repo:good-first-issues`).
- If the user wants to be quick next time, say what would have helped (a PR template line, a
  rule in `CONTRIBUTING.md`) and offer to add it.

Answer a new PR within a few days, even only `Thanks! I'll review it this week.`: the time to
the first answer is what decides whether a contributor stays.
