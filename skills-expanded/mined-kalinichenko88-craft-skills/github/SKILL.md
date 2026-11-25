---
name: github
description: Use when touching a repository's GitHub surface — writing a commit message, running `gh pr create` or merging a pull request, filing or updating an issue, picking an issue up to work on (including a bare `#91` or issue URL as the whole message), checking whether a finding is already filed, or creating or editing a GitHub Actions workflow.
---

# Working with GitHub

Everything here needs `gh` authenticated against a GitHub remote. Where it is
not — `gh auth status` fails, or the remote is elsewhere — skip the step and say
so in the final report rather than inventing a substitute. There are two
exceptions. In *Public repositories*, the target counts as public.
`plugin-defect.md` names the tracker of this plugin, so the remote does not
matter there.

| Moment | What must happen | Read first |
| --- | --- | --- |
| Writing a commit message | `type: one sentence`, at most 5 bullets under it, no `Co-Authored-By:` | *Commits* below |
| `gh pr create` | `--assignee @me`; assign every issue it closes too; `Part of #15`: `keep-open.sh` after it; then read what it closes | *Pull requests* below |
| Merging | Wait for the PR's checks first: a failed or cancelled one, one still running after two watches, or a refusal, stops the merge, and `--admin` or `--auto` only when the person names the flag. `gh pr merge --squash --delete-branch --subject --body`, in English: the PR title with ` (#<PR>)` and one bullet list for the whole branch, run in the checkout that holds the branch, with no `--delete-branch` for an older `gh` in a linked worktree; then *Finishing*, and *Cleanup* when the person asks for it | `merge.md` |
| Finding something out of scope | In the task's module, clear and smaller than the task: fix it in this PR, under **Also fixed**; clear but for a choice, the same after the person chooses. Otherwise add it to an open issue on the same code with `add-finding.sh`, or file a new one. A nit, or a failure that `filing.md` rules out: one line in the final report, no issue | `filing.md` |
| A rule, a skill or a script of this plugin is wrong | Search `kalinichenko88/craft-skills`; show the person the issue, with nothing from their project; file it only after a yes. A step the person had to point out: do it at once, and *Finishing* in `merge.md` drafts it. In a checkout of `craft-skills`: the row above | `plugin-defect.md` |
| Filing next to an existing issue | Name the relation, and correct the other side | `filing.md` |
| Picking an issue up — `#91` or its URL | `take-in-check.sh`; before the next step, give the issue's number, its title and two or three sentences on what it asks; on `continue #91 on <branch>`, `continue.md` says which of the steps below run; close its duplicates; unless told otherwise, `worktree.sh` with `fix/91-what-it-does`; read what it is wired to; re-check its `path:line`; check every open bug and debt issue in the same area first; take along settled issues on the same code, and assign each one and put the label `in progress` on it when it joins; after the work, the check and the review, then the PR and the merge question, in the same turn, on the conditions in *The pull request* of `craft:review-loop` | `take-in.md`; `continue.md` after a `continue` line |
| Writing to a repository — an issue, a comment, a PR, a branch, a commit | `gh repo view <owner/name> --json visibility` on each repository that gets it, and when it fails, take it as `PUBLIC`; `PUBLIC`: no names, numbers, titles, paths or code from a private source. Write "a private tracker with 100 open issues" | *Public repositories* below |
| Editing a workflow | Pin `uses:` to the latest major; runtime ≥ host | *GitHub Actions* below |

A file in the last column sits next to this one, in this skill's base
directory. Read all of it before the first step of that moment: the row above
is its summary, not its rules. `take-in.md`, `filing.md` and `merge.md` send
you on to `tracker.md`, which runs the scripts and reads the tracker.

## Commits

A commit message is a typed subject line, and under it, at most, a short list of
what was done:

```
fix(hooks): make the docs hook read commands, not prose

- Add the newline to the separator class
- Replay two recorded pushes through the hook in tests/hooks_test.sh
```

The subject is `type: sentence` or `type(scope): sentence` — imperative, up to
100 characters, so the whole first sentence fits. The types, and the only ones:

| Type | Use for |
| --- | --- |
| `feat` | a capability the user did not have before |
| `fix` | behaviour that was wrong and is now right |
| `refactor` | a change with no visible behaviour change |
| `docs` | documentation only |
| `test` | tests only |
| `ci` | workflows and pipelines |
| `chore` | anything else: dependencies, tooling, housekeeping |

A change touching several kinds takes the type of the part the reader cares
about; `wip` is not a type and never reaches `main`.

The list, when there is one, comes after a blank line: one to five bullets, one
line each, each naming a thing that was done. The reasoning, the measurements
and the alternatives stay in the PR description. Nothing else goes below the
list.

Commit messages are English, in every repository — see *Code speaks English* in
the global prompt.

Never add a `Co-Authored-By:` trailer: no Claude, no model name, no
`noreply@anthropic.com`.

## Pull requests

Every PR opened with `gh pr create` carries an assignee — always pass
`--assignee @me`, so the authenticated account owns it.

If the PR closes an issue — `Closes #12`, `Fixes #12` — assign that issue the
same way *before* the PR merges and closes it: `gh issue edit 12 --add-assignee
@me`. Once GitHub closes an issue automatically, nothing goes back to record who
did the work. An issue already assigned to someone else stays theirs: say so,
do not reassign.

Every issue the PR closes beside the task — a ride-along, or a bug or debt the
change removes (`take-in.md`) — gets its own line under **Also closes** in the
description, with its own keyword — `Closes #15` — because GitHub closes only
the numbers a keyword precedes, and the issues linked to the PR. An issue with
`## Also:` sections closes only when every problem in it is fixed; when the
change fixes some of them, the description says `Part of #15` instead of
`Closes #15`.

A `Part of #15` PR still closes #15 on merge when its branch is linked to #15,
and `worktree.sh` links every branch it makes: when the PR opens, GitHub turns
the branch's link into a link of the PR. So right after `gh pr create`, remove
that link: `bash <dir>/scripts/keep-open.sh <PR> 15`, where `<dir>` is this
skill's base directory.

Then read what the merge will close, and read it again after each edit of
the description. GitHub can add the link of a new keyword a second later,
so the command waits first:

```bash
sleep 3; gh pr view <PR> --json closingIssuesReferences --jq '.closingIssuesReferences[].url'
```

It must print only the issues that the description closes on purpose. A
closing word in the description before a number — `closed #11`, `does not
close #5` — is a keyword too: write that sentence without it. Any other issue
in the list is a link: the branch's, or one made by hand in the issue's
*Development* panel. When the description does not close that issue, run
`keep-open.sh` for it.

The title and description follow the language the project already uses — read
the recent merged PRs and issues before writing, and match them. English is the
default only where there is nothing to match.

## Public repositories

Before the first write to each repository, read the visibility of the
repository that gets the text. Give `gh repo view` that repository as
`owner/name` or as a remote URL: the `--repo` of the `gh` call, the
`owner/name` in the issue or PR URL that the call takes, or the URL of the
remote you push to. `gh repo view` does not take an issue or PR URL. A `gh`
call with none of these writes to the checkout's default repository, the one
that `gh repo view` prints with no argument. That default can differ from the
remote that `git push` uses: with no default set, `gh` takes `upstream` before
`origin`.

```bash
gh repo view <owner/name or remote URL> --json visibility --jq .visibility
```

When the command fails for that repository, or `gh` cannot run, write as if it
printed `PUBLIC`.

A write is an issue, a comment, a PR title or description, a branch name, a
tag, a release, or a commit. A commit is its message and each file it changes:
code, tests, fixtures and docs.

`PUBLIC` means that everybody can read the text, and search engines index it.
In a public repository, a case from a private source goes in only as its shape
and its counts. A source is public only when anybody can open it without a
login: a public repository, docs, a package page, a CVE record. Every other
source is private:

- A repository for which the command prints `PRIVATE` or `INTERNAL`, or
  fails. A local checkout of one.
- A work tracker, a wiki or a chat.
- A log or a file that the person gives you.
- The data of a person or a customer.

The content of the repository that gets the text is not a private source for
that text: its own paths, numbers and code stay as they are.

From a private source, leave out each detail that names the source or its
content:

| Leave out | Write instead |
| --- | --- |
| The repository, the organization, a URL, a local path | "a private tracker with 100 open issues" |
| Issue and PR numbers, titles, quotes | The count and the shape: "two issues that cite the same `path:line`" |
| File paths, branch names, identifiers, code | The same case with neutral names: `src/a.ts:42`, `parseOrderCsv` → `parseRows` |
| People and customers | The role: "a customer", "a teammate" |

Record a fixture from a public source when one has the shape, for example the
issues of the repository you write to. When only a private source has the
shape, keep its structure and every character the case depends on —
whitespace, markup, order, a keyword — and replace the rest of its text as the
table says. Write in the PR description that the fixture is a rewritten
private payload, without a name of the source.

An edit does not remove the old text. GitHub keeps the old body of an issue, a
PR or a comment in its edit history, and an old title in the timeline. After a
force push, the PR timeline still shows the old commit's SHA, and the commit
stays readable by it. So check before the write. When private text went out,
tell the person what went out and where. The person decides what to do.

## GitHub Actions

When creating or editing CI workflows, in any project:

1. **Pin every `uses:` to the latest available major.** Don't trust memory —
   verify against the GitHub API:
   `gh api repos/<owner>/<repo>/releases/latest --jq .tag_name`, and confirm the
   floating major tag exists:
   `gh api repos/<owner>/<repo>/git/matching-refs/tags/v --jq '[.[].ref|sub("refs/tags/";"")]|map(select(test("^v[0-9]+$")))'`.
   Pin to the floating major (e.g. `actions/checkout@v7`), not an exact patch.

2. **Never pin a CI language runtime below the host dev machine.** The CI
   version must be **>= the version installed on the current machine** (e.g.
   `node --version`, `bun --version`). Match the host major by default; never go
   lower. Re-check whenever touching workflow runtime versions.

Apply both whenever adding or reviewing CI, even if not explicitly asked.
