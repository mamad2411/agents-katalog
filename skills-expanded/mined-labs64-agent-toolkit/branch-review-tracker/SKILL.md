---
name: branch-review-tracker
description: >
  Use for any review of a branch or a pull/merge request: "review this branch",
  "review this PR", "check the branch against its ticket", a re-review after
  fixes, or when invoked by name. Use it even when the user does not mention
  tracking: tracking the issues until they are fixed is what it adds, not a
  condition for using it. Load any project-specific review checklist together
  with it, not instead of it.
  Asks for the target branch, base branch and ticket, checks the environment,
  reviews the code and its prose against the ticket and its design comments,
  verifies every finding against the code, and publishes a read-only Artifact
  page listing each issue with its status, evidence, fix assessment and
  file:line. Re-reviews the branch on each update, drafts PR comments and
  tickets for the user to post, and keeps a small resume file so that a new
  session can continue at low cost. Not for a quick question about a single
  hunk or about uncommitted local changes.
---

# Branch review tracker

A review of a branch that is fixed over several rounds. Each round re-reviews the
branch and updates one page: a numbered list of issues, each with a status and a
Details popup giving the evidence, the commit responsible and the places to look.

The page is a claude.ai Artifact, and it is the record of the review. It is
read-only for viewers: only Claude changes a status, as the review and the fixes
progress. A new session resumes from the page's small `context.json`, not from
the conversation or local files.

The tracker holds three files:

- `index.html`: the page, a copy of `assets/tracker.html`;
- `issues.json`: every issue, and the session log;
- `context.json`: the resume notes and an index of the issues for the next
  session, the prompt that starts it, and the short list of what waits on the user,
  which is the only part the page shows.

## 1. Ask what to review

Gather candidates first, then ask everything in one `AskUserQuestion` call. Skip a
question whose answer came with the invocation, for example a PR number or URL.

    git for-each-ref --sort=-committerdate --count=6 --format='%(refname:short)' refs/heads
    git symbolic-ref --short refs/remotes/origin/HEAD      # the default base
    git log --format=%s <base>..<target> | grep -oE '[A-Z]+-[0-9]+' | sort -u
    gh pr list --head <target> --json number,url,title     # or: glab mr list --source-branch <target>

| Question | Options |
|---|---|
| Target branch | the PR's head branch if a PR was given; otherwise the three most recently updated local branches other than the base |
| Base branch | the remote's default branch (Recommended), then other long-lived branches, if any |
| Ticket | ids found in the branch name and its commit subjects; `No ticket` |

The user can always type another value. Ask the ticket question after the branch is
known, or derive its options from the most likely target.

## 2. Check the environment

Run the preflight script and show its table to the user:

    <this skill>/scripts/preflight --target <branch> [--base <base>] [--ticket <id>]

It checks the repository, both refs, the user's checkout, whether the local branch
matches the PR head, the PR on the host, checkout filters that can stop
`git worktree`, and the CLIs the review uses. Exit code 2 means a blocker; 1 means
warnings only. It does not check the project's build tools: the project's
build-and-test helper does, as described below.

The script fetches both branches. It takes the base from origin, where it is
current, and the target from the clone, where the author may have pushed it.
Review against the refs it prints. If it warns that the local branch differs from
the PR head, review the PR head: read it with `git show <sha>:<path>` instead of
checking it out.

Then check the tools of this session, which a script cannot see, and add them to
the table:

| Needed for | Tool | Without it |
|---|---|---|
| the review | `code-review` skill, or the `Agent` tool | blocker |
| the page | `Artifact` tool | keep the files in the scratchpad and give the user their paths after each round; say so |
| the ticket's context, and posting tickets | Atlassian tools (`getJiraIssue`, `createJiraIssue`) | review without it; say so |
| the PR's comments and checks | `gh` or `glab`, authenticated | review the branch only; say so |

Then look for the project's helper skills, as described in "Helper skills" below,
and add one row per helper to the table: found, with its name, or missing, with
what the review will lack.

If the build-and-test helper names an environment check, run it with the refs the
preflight printed and the ticket, and add its lines to the table. Its lines and
exit code have the preflight's format. A FAIL in it blocks builds and tests: the
review goes on by reading the code, and says so. If a line of the helper checks
something the preflight checked too, such as where the ticket appears, the
helper's line settles it: an OK there replaces the preflight's WARN.

Stop on a blocker and say what is missing. On warnings, say what the review will
not cover, and go on.

If the ticket can be read, fetch its summary and status. Write a status in
parentheses after the id: `PROJ-123 (in progress)`.

## 3. First round

1. **Review.** Invoke `code-review` on `<target>` against `<base>`, or on the PR
   number. Tell the reviewer to read other commits with `git show <rev>:<path>`, and
   never to check out anything in the user's directory.
2. **Review the prose**, as described in "The prose review" below. `code-review`
   looks for defects in the code and does not cover it.
3. **Verify every finding**, as described in "Verifying findings" below. An issue
   goes on the page only after this step. A finding that does not survive it is
   either dropped before it is listed, or, once listed, set to `dismissed` with
   its reason.
4. **Classify every issue.**
   - The commit responsible: `git log -S'<symbol>' <base>..<target>`, or
     `git blame -s <target> -- <path>`.
   - Whether the base has it too: `git show <base>:<path>`. An issue the base
     already has gets `"commitRole": "Pre-existing on"` and `"commit": "<base>"`.
     It is not a regression of the branch, but it can still block the merge when
     the branch makes it worse, for example by exposing more data through it.
   - `file:line` for every location, at the reviewed commit.
5. **Write the tracker** in the session scratchpad, in a folder named after the
   branch (`/` replaced by `-`):
   - `index.html`: a copy of `assets/tracker.html`, with `__TITLE__` replaced by
     the page name. The name is the branch's topic in two to four words, followed
     by "Review", such as `API Key Authorization Review`.
   - `issues.json` and `context.json`, as described in "The data files" below.
6. **Validate** both files. The validator checks the schema, that every location
   exists at the reviewed commit, and that the index in `context.json` matches
   the issues:

       python3 -I <this skill>/scripts/validate-issues.py <dir>/issues.json --repo <repo>

7. **Publish** with the Artifact tool's publish action, `file_path` set to `<dir>/index.html`,
   `files` set to `{"issues.json": "<dir>/issues.json", "context.json":
   "<dir>/context.json"}`, `icon: "checklist"` and a one-sentence `description`.
   Write the returned URL into both files (`"artifact"`), republish, and give the
   link to the user.

## 4. Later rounds

Run a round when the user says the branch was updated, or asks for a re-review.

1. **Confirm that the branch moved.** Compare the PR head, or the target ref, with
   `reviewed`, and look at `git reflog -3 --date=iso <target>`. A push can arrive
   late, and the user's local branch can lag behind the PR. If nothing moved, say so
   and stop.
2. **Fetch the base** (`git fetch origin <base>`). If the base moved, note it, and
   compare the branch with
   `git range-diff <old-base>..<old-tip> <new-base>..<new-tip>`.
3. **See what changed**:
   - `git range-diff <base>..<reviewed> <base>..<target>` shows which commits were
     rewritten, added or dropped;
   - `git diff <reviewed> <target>` shows the net change;
   - the PR's new comments, reviews and checks (`gh pr view <n> --json
     comments,reviews`, `gh api repos/<owner>/<repo>/pulls/<n>/comments`, `gh pr
     checks <n>`).
4. **Assess every fix.** For each issue the change addresses, read the fix and
   record in `fix` what it does and how the code behaves now. Set `fixed` only
   when the reading confirms it, and say in `verified` how far it was verified.
5. **Look for problems the fixes cause.** A fix often moves the problem instead of
   removing it. Check the inputs the old code handled by accident:
   - a missing, empty or null value, for example a property a client does not set,
     that used to produce a harmless literal and now means "no restriction";
   - defaults a value falls back to;
   - code paths that the change reaches without touching them, such as callers,
     other endpoints, older clients and the import side of an export;
   - behaviour the change alters for requests it did not target.
   Add each problem as a new issue, and note the fix that caused it on both issues.
   Run "The prose review" on the net change.
6. **Re-evaluate every issue that is not fixed** against the new code, and look
   again at the fixed ones whose code changed.
7. **Run tests** only as "Reproducing with tests" below allows.
8. **Update the tracker**, as described in "Keeping the tracker current" below:
   - Set `reviewed` to the new tip.
   - Rewrite `commits` to the new hashes. A rewritten commit gets its new hash; a
     dropped one leaves the map; a new one is added.
   - Change `status`, `commit`, `commitRole`, `note`, `fix` and `detail` of the
     issues that changed.
   - Re-find every location's line at the new tip with `git grep -n`. Do not shift
     lines by arithmetic.
   - Append new issues with the next free number. Never renumber.
9. **Validate, then republish** to the same URL.
10. **Report** to the user: what this round fixed, what is still open, and what is
    new, with file:line and what was run. End with the page link.

## Verifying findings

Read the code yourself at the reviewed commit before an issue goes on the page.

1. **Trace the scenario end to end.** Follow the input from where it enters to
   where the damage happens, and name each step with `file:line`. A finding that
   needs a step the code does not take is dismissed, with that step as the reason.
2. **Check the preconditions.** Ask how the triggering state can arise:
   - who can create the input, for example through which API, and whether a
     validator or a default stops it;
   - whether a configured default, such as an unlimited lifetime or a role assigned
     when none is given, makes the scenario unreachable, or makes it the normal
     case;
   - whether existing data can contain it. When only data outside the repository
     can answer, use the project's data-check helper; without one, ask the user how
     to find out. Record the answer in `verified`, and in the log.
3. **Separate "intended" from "acceptable".** A runbook, test or code comment that
   shows a behaviour is deliberate does not make it harmless. Check backward
   compatibility on its own: existing clients and deployed versions, existing data,
   and vendors or users who never used the new feature. A deliberate break of an
   existing workflow is an issue, and a blocker unless the user accepts it.
4. **Say how it was verified.** Write it into `verified`: "Reproduced by a
   controller-level test; the service layer was stubbed", "From reading the code;
   not run", "Data check: no matching records". Report what the evidence proves and name
   what it does not. Do not assert a causal or comparative verdict the data does
   not show.
5. **Dismiss with a record.** A dismissal sets `status: "dismissed"` and a
   `dismissal` with who decided, when, and why. When Claude dismisses, say so,
   and that no person signed it off; the page shows it.
6. **Reopen when challenged.** When the user questions a dismissal or a verdict,
   re-check it from the code instead of defending it. If it was wrong, reopen the
   issue, remove the dismissal, and say plainly in `note` what the earlier verdict
   got wrong.

## Reproducing with tests

Run builds and tests only when the user asks, or when the repository's and the
user's instructions allow it without asking. How to build and test the project,
with which toolchain and settings, comes from the project's build-and-test helper
and its instructions, not from this skill.

1. **Never use the user's checkout.** Put the commit under test in a separate
   directory, the way the project's build-and-test helper or the repository's and
   workspace's instructions say, for example with a tool that reuses the user's
   build. Only if neither says how:
   - `git worktree add --detach <scratchpad>/<name>-wt <sha>`;
   - if anything blocks the worktree, export the commit instead, leaving out the
     paths that block it:
     `git archive <sha> -- . ':(exclude)<blocked-path>' | tar -x -C <dir>`. For
     example, a `git-crypt` smudge filter fails on encrypted paths when the key is
     not available to it. The preflight script names the paths that have checkout
     filters.
   If the project's method refuses a commit, for example because the commit needs
   a build of its own, tell the user what it would take before working around it.
2. **Build and run the way the project says.** A tool failure, such as a toolchain
   the project does not support, is not a test result: fix the environment as the
   project's helper or instructions say, then run again. Without a helper, ask the
   user rather than guess, and note what was learned for the project notes.
3. **Write the test so that it asserts the correct behaviour.** A failure then
   reproduces the issue, and the same test becomes the regression test for the fix.
   Drive the real classes along the path, and stub only what the scenario needs.
   Make each stub mirror what the real code does, and name every stubbed or
   unexercised layer in `verified`, such as HTTP, the security chain or the
   database.
4. **Run the narrowest set:** the new test, plus the tests that cover the changed
   code.
5. **Keep the test source in the tracker.** The scratchpad can be wiped between
   sessions. Publish the test as `tests/<Name>.<ext>` in `files`, with
   `contentType: "text/plain"`, and name it in the issue.
6. **Clean up.** Remove what the run left: the worktree or the export, unless the
   project's tool removes it itself, and any build output in the user's checkout,
   such as compiled test classes, which a later build would pick up. Then check
   that `git status` and `git worktree list` show the user's checkout unchanged.

## Helper skills

The review flow is the same for every project; what the project knows lives in its
own skills. Use them when they exist; this skill never hard-codes project tooling.

Find them in this session's list of available skills, by their descriptions. Do not
guess names. Load one with the `Skill` tool when the step needs it.

| Helper | Used for | Without it |
|---|---|---|
| review checklist | the project's risk areas: security model, compatibility promises, API contracts, migrations | the review relies on general knowledge; say which areas it may miss |
| build and test | checking that the environment can build and test; building and testing one commit in isolation: commands, toolchain, settings, known blockers | the preflight does not check the build environment; tests run only after asking the user how; findings stay "from reading the code" |
| data checks | answering questions from data outside the repository, safely | the user is asked how to find out |
| prose rules | comments, docstrings, changelogs, commit messages and PR text, such as a general writing standard | the prose review uses the instruction files only |
| ticket conventions | the ticket system's projects, types, priorities, fields and links | the project is queried before posting |

For each missing helper, give the user a one-line hint: what the helper would hold,
and which part of the review it would make more reliable.
`references/helper-skills.md` lists what each helper should contain. At the end of a
review, offer to draft the missing helpers from what the review learned about the
project, such as a toolchain mismatch or a checkout blocker.

## Writing for others

Draft first. The user posts PR comments; post a ticket only when the user says so.
Write every draft in a fenced `markdown` block, ready to copy.

**PR comments**

- One issue per comment, anchored to the file and line range it fits best, as a
  permalink at the full reviewed SHA:
  `https://github.com/<owner>/<repo>/blob/<full-sha>/<path>#L<start>-L<end>`.
- Keep it concise: the defect, how the triggering state arises, what it exposes or
  breaks, the suggested fix, and how it was verified.
- Use the tracker's issue numbers, and keep one numbering everywhere. If an earlier
  comment used other numbers, give the user the mapping.
- Say plainly whether a sentence describes the current behaviour or the proposed
  one, and where a step leaves a gap.
- Cross-reference other comments by topic, not by a number the reader cannot see.
- After the user posts, record it in the issue's `posted`, and in the log.

**Tickets**

- Follow the project's ticket-conventions helper if there is one. Without it,
  check the project's issue types, priorities and required fields before posting.
  Use a value that exists; if the requested one does not, use the closest and tell
  the user.
- Leave out line numbers and commit SHAs; they go stale. Name classes and methods.
- Reference the related ticket and the PR, and link the tickets.
- Record the ticket in the issue's `followUp`, and in the log.

## Keeping the tracker current

Update the tracker with every change in the state of the review, not only at the
end of a round: a verdict, a dismissal, a reopening, a posted comment, a created
ticket, a reported data-check result. In one step:

1. Change the issue in `issues.json`.
2. Update `context.json`: its index entry, `waiting`, and any section the change
   affects.
3. Append a line to `log` in `issues.json`, with the UTC time and what happened.
4. Validate, then republish all files to the same URL.

## Resuming in a new session

The page has a "Resume in a new session" button. Hovering over it, or focusing it,
shows the prompt from `context.json`; clicking it copies the prompt to the
clipboard. Where the clipboard is refused, a popup shows the prompt selected. The prompt names the page URL and tells the new
session to do the following, which is also the procedure when the user gives only
the link:

1. Read the page with the Artifact tool (`action: "read"`, `url` set to the page
   address), then read its `context.json` the same way, with `path:
   "context.json"`. It is small, and its notes and index are enough to orient. Do
   not load all issues up front.
2. When work on an issue starts, read `issues.json` with the Artifact tool
   (`action: "read"`, `path: "issues.json"`), which saves the file to the
   scratchpad. Extract the one issue:
   `jq '.issues[] | select(.n == 11)' <file>`. Read `tests/` files only when needed.
3. Check the PR for commits and comments newer than `context.json` records, and tell
   the user briefly what changed.
4. Continue, and publish with `url` set to the page's address.

To find a lost page, list the user's artifacts with the Artifact tool
(`action: "list"`) and look for the title, or ask the user for the link.

Write the resume prompt for a reader who does not know these conventions: name the
tool and the action, as in "Read the tracker with the Artifact tool's read action".
Do not write "Artifact read the URL", which reads as if the page itself read
something.

The prompt names only the review, the tracker's URL and this skill. The steps above
are the skill's, so the prompt does not repeat them: a copied procedure goes stale
when the skill changes. It holds no review state either, such as issue numbers,
commits, statuses or which test belongs to which issue, because a pasted copy goes
stale too. That state lives in `context.json` and `issues.json`; for example, an
issue's `verified` names its stored test. Use this shape:

    Resume the review of <owner>/<repo> PR #<n> (<ticket>) with the
    branch-review-tracker skill. The tracker is the claude.ai artifact <url>.

If a session receives this prompt but the skill is not available, it says so and
asks the user how to continue, instead of improvising the procedure.

## The prose review

Check the prose of the branch against the code at the target and against every
rule that the instructions of the repository and the workspace give for prose.

1. **Collect the rules.** Read every instruction file that applies to a changed
   file: `CLAUDE.md` or `AGENTS.md` in each directory above the repository root,
   and the ones `git ls-files '*CLAUDE.md' '*AGENTS.md'` lists on the path of a
   changed file. Load the prose-rules helpers those files or the session name,
   such as a general writing standard for comments, docstrings, changelogs and
   PR descriptions.
2. **Collect the prose to check**, from the whole range
   `git diff <base>...<target>`, not commit by commit:
   - every comment, docstring or doc comment, changelog entry, doc page, runbook and
     test name the branch adds or changes;
   - the docstrings of every class and method whose behaviour the branch changes,
     even if their text is unchanged. Follow the change along every layer that
     forwards to it, such as a controller, a service and a repository, with
     `git grep` from the repository root;
   - the commit subjects of `<base>..<target>`, and the PR title and description.
3. **Check each item against the code at the target.** For a docstring, trace
   every branch of the code it describes: the errors raised, the items dropped,
   the defaults, the input normalisation. A docstring or runbook that the code
   contradicts, or that leaves out an outcome a caller can observe, is an issue,
   and so is one that breaks a collected rule.
4. **Verify, classify and list** the prose issues like any other. Give the text
   that breaks the rule in `detail`, name the rule and the file that sets it, and
   suggest wording that follows it. Issues that share one cause, such as the same
   docstring copied to several layers, are one issue with several `locations`.

## The data files

`assets/issues.example.json` and `assets/context.example.json` show every field.

`issues.json`:

| Field | Meaning |
|---|---|
| `title` | the page name, as in the `<title>` |
| `branch`, `base`, `ticket` | what is reviewed; `ticket` may be null |
| `pr` | `{number, url}` of the pull or merge request, or null |
| `reviewed` | the short hash of the target commit the page describes |
| `artifact` | the page URL, once published |
| `commits` | short hash → subject, for every commit the issues name |
| `issues[]` | see below |
| `log[]` | `{at, text}`: what happened, oldest first, UTC |
| `closed` | set when the review is closed: `date`, `at`, `base`, `summary` |

Every issue has:

- `n`: its number, which never changes;
- `status`: see "Statuses" below;
- `title`: one line naming the defect;
- `where`: a short pointer, such as `TokenService getExportTokens`;
- `commit` and `commitRole`: for example `Introduced in`, `Introduced and fixed in`,
  `Fixed in`, `Pre-existing on`;
- `locations[]`: `{path, line, what}`, repository-relative, at `reviewed`;
- `detail[]`: paragraphs, written as the "Wording" section below asks;
- `verified`: how the issue, or its fix, was verified, and what was not.

It may also have:

- `blocker: true`: the page shows "before merge" while the issue is not done;
- `minor: true`;
- `note`: one line shown under the title;
- `fix`: `{what, behavior}`, required when `fixed`: what the fix does, and how the
  code behaves now;
- `dismissal`: `{by, at, reason}`, required when `dismissed` or `wontfix`;
- `posted[]`: `{at, where, url}` for each PR comment or other place the issue was
  raised;
- `followUp[]`: `{ticket, url, summary}` for tickets created from the issue.

`context.json`:

| Field | Meaning |
|---|---|
| `updatedAt` | UTC time of the last change |
| `reviewed`, `artifact` | as in `issues.json` |
| `resumePrompt` | the prompt the page's resume popup shows |
| `index[]` | `{n, status, title, blocker}` for every issue, matching `issues.json` |
| `waiting[]` | `{kind, text, issues}`: what waits on the user, shown on the page; `kind` is `decision`, `to post` or `to run` |
| `sections[]` | `{title, text}`: the resume notes, for the agent only; the page does not show them |

The page shows only `waiting` from this file, under "Waiting on you", and hides
the block when it is empty. Write each item as one sentence the user can act on,
with the issue numbers it concerns. Remove an item once the user has acted on it.

Keep the sections short. Use these titles:

- **Where things stand**: the PR and branch, the reviewed and first reviewed
  commits, what blocks the merge.
- **Posted and pending**: what was posted where, with numbering differences, and
  which drafts are not posted.
- **Open decisions**: what waits for the user, with the recommendation.
- **Project notes**: which helper skills this review uses, and what the review
  learned about the project that no helper covers yet, such as a checkout blocker
  and its workaround. Never include the content of a credentials file.
- **Conventions**: the user's preferences stated during the review.

## Statuses

- `open`: verified and not fixed.
- `in progress`: the user said someone is working on it.
- `partial`: a fix landed but part of the problem remains. `detail` says which part.
- `fixed`: confirmed by reading the code at `reviewed`, and by tests where tests can
  show it. `fix` says what changed; `verified` says how far it was checked.
- `dismissed`: the finding did not hold, for example the scenario is unreachable.
  `dismissal` says who, when and why.
- `wontfix`: a valid issue the user decided not to fix. `dismissal` records the
  decision.

## Wording

`detail`, `fix`, `verified` and drafts are technical text: the wording rules of the
workspace and repository instructions apply. Say what the code does and what goes
wrong. Give a timeline for a race or a timeout. Write each paragraph so that it
stands alone.

## Closing

When the user closes the review, set `closed`: the date, the final hash, the base
hash, and one sentence saying what is fixed and what was not verified. Update
`context.json` to say the review is closed. Republish; the page shows a banner.
If helpers were missing, offer once more to draft them from the project notes.
Delete the page only if the user asks for it to be deleted. Deleting cannot be
undone.

## Pitfalls

- **The user's checkout stays put.** A subagent gets the same instruction in its
  prompt, with the project's way of isolating a commit if the run needs one.
- **The local branch may lag the PR.** Compare with the host's head before
  reviewing, and say which commit the review describes.
- **The Artifact tool's `edits` cannot be combined with `files`.** To change the page and the
  data in the same round, edit `index.html` with the Edit tool, then publish all.
- **A prompt or draft written for the user names the commit it was based on.**
  Check the ref again before handing it over; the branch may have moved.
- **"Page not found" for the user** usually means their browser is signed in to
  another claude.ai account. Reading the page with the Artifact tool's read action
  confirms that it still exists.
- **zsh modifiers in paths.** In `git show "$rev:$path"`, zsh reads `:a`, `:h` and
  similar after a variable as modifiers. Write `"${rev}:$path"`.
