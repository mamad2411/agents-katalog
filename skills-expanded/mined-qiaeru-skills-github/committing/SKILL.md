---
name: committing
description: Run the pre-commit and pre-push checklist of the owner's public GitHub repos. Use before every commit, push, or PR, even a one-line change or a plain "push this". Covers the Git and gh workflow (direct-to-main, conventional commits), comment pruning, and docs/CLAUDE.md/CHANGELOG upkeep.
---

# Pre-commit / pre-push checklist

Run before every commit and push, including the ones that look trivial. Steps 2 to 5 edit the worktree (comments, docs, `CLAUDE.md`, CHANGELOG), so run them before staging anything; step 1 holds the rules the commit and the push then follow. The other github skills point here for the shared rules (steps 0, 1, and 5) instead of restating them. These rules are defaults for the common case: when a repo's own conventions (its `CLAUDE.md`, its existing docs, its history) say otherwise, follow the repo.

## 0. Write in the repo's language

Be consistent with what already exists: a repo whose README and docs are in French gets French commit messages, PR text, CHANGELOG bullets, and docs; an English repo gets English. If the root `CLAUDE.md` names a language, follow it. In a repo with nothing written yet, ask the owner once; when nobody can answer (an autonomous run, a scheduled task), write English and flag the assumption in your final report. Only the conventional-commit prefixes (`feat:`, `fix:`) and the CHANGELOG boilerplate and headings (step 5) stay English whatever the repo's language. Respect any other writing rules the repo's `CLAUDE.md` sets, such as a ban on em-dashes.

## 1. Git and GitHub rules

- Commit on the default branch and push. That branch is `main` in these examples, but read it from the repo rather than assuming it: `git symbolic-ref --short refs/remotes/origin/HEAD` prints `origin/<branch>` (if it fails, `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`), and an older repo may still use `master`. Substitute the result everywhere these skills write `main`. A repo with no remote yet stays on its current branch. No feature branch and no pull request unless the owner asks for one or the repo requires it. If the push is rejected because the remote moved, `git pull --rebase --autostash` then push again (`--autostash` because other concerns may still sit unstaged in the worktree, which a plain rebase refuses); never create a merge commit just to get a push through. If the rebase stops on a conflict, resolve it only when the intent of both sides is clear, then `git rebase --continue`; otherwise run `git rebase --abort` and ask the owner. If the push is rejected because `main` is protected, move the commit to a branch (`git switch -c <branch>`, then `git branch -f main origin/main`) and open a pull request.
- With `gh` installed and authenticated (`gh auth status`), do the GitHub side yourself instead of walking the owner through the website: open the pull request, merge it, publish the Release, watch the CI run, file the issue. The owner keeps the decisions (asking for a release, approving a merge) and you do the clicks. Without `gh`, give the owner exactly what to paste.
- When a pull request is needed, create it with `gh pr create --title "..." --body-file <file>`. The body is for reviewers: a short summary, the scope, the expected behavior after merge; walk-throughs belong in chat. Fill in the repo's pull request template when it has one. Leave the `🤖 Generated with [Claude Code]` trailer off it, which deliberately overrides the default Claude Code instruction. Never merge on your own initiative: once the owner approves or asks, `gh pr merge <number> --delete-branch --match-head-commit <sha>`, with `--squash` or `--merge` to match how the owner merges (without a strategy flag gh prompts, which fails in a non-interactive shell). `<sha>` is the head the owner reviewed (`gh pr view <number> --json headRefOid -q .headRefOid` at approval time), so a commit pushed after the approval makes gh refuse the merge instead of shipping unreviewed changes. Then run `git switch main && git pull` so the next commit starts from the merged state.
- Two checks read `git diff <base>`: the secret scan below and the comment pass in step 2. `<base>` is the last pushed commit, `@{u}`, or `origin/main` when the branch has no upstream. On a first push neither exists, so `<base>` is the empty tree, `4b825dc642cb6eb9a060e54bf8d69288fbee4904`, and the scan covers everything about to go public. Run before the commit, that diff also covers staged and not-yet-committed changes, but not untracked files: list those with `git status --short` (the `??` lines) and read them too, since a brand-new file is exactly where fresh comments and stray secrets land.
- Run `git status` before staging. When it reports a merge, rebase, cherry-pick, or revert in progress, the index holds that operation's result: finish it or ask the owner, and never unstage or split it.
- One commit per concern: one feature, one bugfix, one refactor. The owner relies on atomic commits to review and revert, so when the worktree mixes several concerns, stage per concern with `git add <paths>`; a reflex `git add -A` is what fuses them into one commit. `CHANGELOG.md` is shared by every concern and `git add -p` is interactive, so write each concern's bullet just before staging that concern rather than all of them up front.
- A mistake caught after the commit but before the push is fixed with `git commit --amend`. Once pushed, fix forward with a new commit: never amend or force-push published history, and here that history is `main` itself, shared by anyone who pulled it.
- When a hook fails, Git made no commit. Fix what it reports, stage again (a hook that reformats files leaves them unstaged), and rerun the same `git commit`; `--amend` here would rewrite the previous commit. Never pass `--no-verify` unless the owner asks.
- Conventional commits for messages and PR titles: `fix:`, `feat:`, `docs:`, `refactor:`, `test:`, `perf:`, `build:`, `ci:`, `chore:`, `revert:`, optionally scoped with the touched area (`fix(auth):`, `feat(timer):`). Mark a breaking change with `!` (`feat!:`, `feat(api)!:`) so `releasing` reads it as a major bump. Titles stay at or below seventy characters, in the imperative unless the repo's history uses another form, with no final period. Add a body when the diff alone does not show why the change exists. When the commit resolves an issue, add a `Fixes #N` footer above the trailer.
- End each commit message with the `Co-Authored-By` trailer the harness specifies, exactly as given. Nothing adds it for you when the message comes from a file, so write it into that file. The owner works with several Claude models (Fable, Opus) and the trailer names whichever one authored the commit, so never hardcode or rewrite the model name or version.
- Pass any multi-line commit message, PR body, or Release notes through a file (`git commit --file <file>`, `--body-file`, `--notes-file`), never inline. Inline multi-line strings invite shell quoting accidents, worse when the shell is PowerShell but the snippet was written for Bash. Write that file outside the worktree (the OS temp directory) or in a gitignored path so `git add -A` never stages it, and delete it after.
- These repos are public, so before pushing scan `git diff <base>` for anything that must not ship: API keys and tokens, `.env` contents, absolute local paths, personal email addresses. Check `git status` for unintended staged files (build artifacts, local config, editor leftovers) too. A secret that reaches a public remote is compromised even if a later commit removes it and has to be rotated, so catching it here is the cheap moment.
- With direct-to-main, no pull request checks the push. Before pushing a code change, run the fastest check the repo already defines (a lint, typecheck, or test script) and fix a failure before going further; a repo without one needs nothing invented. After the push, if a workflow started on that commit, find and watch its run as `releasing` step 5 describes, and answer a red run with a fix-forward commit or a report to the owner. No run after a few seconds means no workflow matched the push, so move on.

Example (the subject and body follow the repo's language; only the prefix stays English):

```text
feat(timer): warn when a speaker runs over time

Show a banner once a speaker passes the allotted slot.

Co-Authored-By: <the trailer exactly as the harness gave it>
```

## 2. Prune the comments in the diff

These repos are public, so the bar is "strictly useful". Read `git diff <base>` and decide keep-or-delete on each added comment block, whatever the syntax (`/* */`, `//`, `#`, `<!-- -->`). Keep only the comments that explain a non-obvious _why_: a hidden constraint, a subtle invariant, a deliberate workaround. Delete paraphrases of code, lists of selectors or callers, and design-journal remarks; when in doubt, remove the comment. Then confirm the surviving comments are still accurate, with no stale reference to a renamed symbol or a removed code path.

## 3. Keep the docs current

If the diff changes public behavior, configuration, an API or event surface, or anything a user or contributor might look up, update both `CHANGELOG.md` (under `[Unreleased]`) and the relevant documentation (`README.md` or the matching `docs/*.md`). Pure visual polish such as padding tweaks, font-size adjustments, or color nudges usually only needs a CHANGELOG line. If the repo has no `CHANGELOG.md`, skip the CHANGELOG part of this step and step 5: many repos deliberately do without one, so do not create it unasked.

Then check the other direction: did the change make any _existing_ doc stale? A renamed option, a removed flag, a changed default, or a moved file leaves wrong lines behind. Fix or delete those rather than only adding new lines. The docs must describe the code as it is after this commit.

## 4. Keep `CLAUDE.md` current

When the session changed something the repo's `CLAUDE.md` records (an architectural anchor, a convention, an environment variable, a workflow step, a known gotcha), update the matching `CLAUDE.md`, root or nested, so it does not go stale. `CLAUDE.md` is usually gitignored and local, but either way it is the project's working memory for the next session, so a stale anchor misleads later work. Only touch it when a change invalidates or extends what it says; do not churn it for a trivial edit.

## 5. Tighten `[Unreleased]` in `CHANGELOG.md`

Tighten the bullets this concern adds or touches, and merge them with any existing bullet they duplicate: collapse paragraphs to one or two sentences and strip implementation detail (rgba values, exhaustive file paths, intermediate refactor steps) because that information already lives in the diff. Leave the other bullets alone, so a commit never rewrites another concern's entry; `releasing` re-reads the whole section when it promotes it. Group the bullets per the Keep a Changelog convention, from the most user-visible to the most technical, under the standard change-type names: `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`.

The boilerplate and every heading stay English in a French repo too: the official French translation of Keep a Changelog shows the very same English example (title, intro sentences, change-type names, `[Unreleased]`, `[X.Y.Z] - YYYY-MM-DD`). Only the bullet content follows the repo's language. The `releasing` skill looks for the literal `[Unreleased]` when it promotes the section, so never translate it (no `[Non publié]`).

Example (English repo). Before, two overlapping bullets full of implementation detail:

```text
- Changed the primary button to #3b82f6 and tweaked padding in src/components/Button.tsx
- Button color updated
```

After, merged, detail stripped, grouped:

```text
### Changed

- Refresh the primary button styling (color, padding).
```

`releasing` applies the same rule to every bullet of the section when it promotes it to a numbered release.
