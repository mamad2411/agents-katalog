---
name: gh-pr-create
description: >
  Use only when the user explicitly says "create PR", "open PR", "make a pull
  request", "push and create PR", "pr-creator", `$gh-pr-create`,
  `/gh-pr-create`, or `/pr-creator`, or when safe main reconciliation has
  concretely failed. Origin workshop is out of scope for this plugin.
---

# PR Creator

GitHub-workshop skill. Origin is out of scope for this plugin; use this
`gh-pr-create` skill on GitHub only.

Use this skill only after an explicit PR request, or after a concrete failed
attempt to reconcile local and remote `main` safely has made direct delivery
impossible. In that fallback case, create or check out a distinct non-`main`
head branch before following the workflow; never let the later branch push
target `main`.

## Assignee

```bash
# Optional override; default is the authenticated GitHub user
GH_ASSIGNEE="${GH_ASSIGNEE:-$(gh api user -q .login)}"
```

Pass `--assignee "${GH_ASSIGNEE}"` on create and enforce with
`gh pr edit --add-assignee "${GH_ASSIGNEE}"` afterward. Do **not** pass
`--reviewer` for the PR author — GitHub rejects self-review requests (exit
128). Never pass `--draft` unless the user explicitly asked for a draft.

## Execution Backend

1. Verify `git` with `git --version` and `gh` with `gh auth status`.
2. Follow the plain `git`/`gh` workflow in this file.
3. If either verification fails, STOP and report the failed check. For a `gh`
   failure, report verbatim: "`gh` is missing or unauthenticated. Install it if
   needed, run `gh auth login`, then retry."

## Auth + identity policy

- For assistant-authored operations, use plain `git` and `gh`:

```bash
git commit -m "..."
git push origin HEAD
gh pr create --base "${BASE_BRANCH}" --title "..." --body-file pr.md
```

- For repos where the authenticated user has collaborator access: direct
  branch + PR.
- For public repos without collaborator access: fork-first workflow, then PR
  from the fork to upstream.
- On permission errors, stop and report the exact error to the user.

## Stale injected skill paths

Automation prompts often pin versioned cache links. If that file is gone and
the first read fails with `No such file or directory`, do not stop and do not
keep retrying the dead versioned path.

Recover immediately:

1. If you are already inside this skills repo, use the current workspace copy
   of `gh-pr-create`.
2. Otherwise locate the live skill by name under the active plugin caches and
   continue with the newest matching copy.
3. Treat the skill name `gh-pr-create` as the source of truth; the versioned
   cache path is only a hint. Older automations may call this flow
   `pr-creator`; treat that alias as the same skill request.

## Workflow

1. **Verify branch state**: Run `git status` to ensure working tree is clean or changes are committed.
2. **Pick base branch**: Default to `main` — set `BASE_BRANCH="main"`. Preserve
   an explicit caller-provided base instead. If the repository has no selected
   base branch, `git rev-parse --verify
   "refs/remotes/origin/${BASE_BRANCH}"` fails; stop and ask rather than guessing.
3. **Local CodeRabbit pass**: For code or behavioural `SKILL.md` runtime
   instruction changes, run the repository-aware
   `code-review` guard on the committed branch with `--switch-org -- --base
   "${BASE_BRANCH}"` when that tool is available. Fix Critical/Warning findings
   before pushing, or note the deferral in the PR body. If the CLI or capacity
   is unavailable, record that and rely on repository tests plus independent
   local inspection; never retry an unchanged diff merely to satisfy the gate.
4. **Push to remote**: Run `git push -u origin HEAD` to push current branch
5. **Analyze changes**: Run `git log "${BASE_BRANCH}"..HEAD --oneline` and `git diff "${BASE_BRANCH}"...HEAD --stat` to understand scope
6. **Learn the repo's title convention**: Run `gh pr list --state merged --limit 15 --json title --jq '.[].title'` and match the style (prefixes, capitalisation, tense). The title must be concise, human-readable, and say why the change matters.
7. **Generate description**: Write the PR body following the standards below — open with the problem in plain language, from the user's original intent.
8. **Create PR**: Use `gh pr create` with title/body and
   `--assignee "${GH_ASSIGNEE}"`. Do NOT pass `--reviewer` for the author.
   **Never pass `--draft` unless the user explicitly asked for a draft**.
9. **Post-create enforcement**: Run
   `gh pr edit --add-assignee "${GH_ASSIGNEE}"` to guarantee the assignee is
   set even if omitted during creation.
10. **Apply requested labels**: If the prompt specifies labels, add them after
    PR creation with `gh pr edit --add-label <label>`. Add every requested label
    individually so a missing label surfaces clearly.
11. **Automation follow-up**: If the prompt says "if you create a PR" and asks
    for an issue, PR comment, Slack message, or other GitHub follow-up, do that
    work before finishing. If no PR is created, skip the follow-up and say why.
12. **Return repo to `main`**: After the PR is opened, check the local repo
    back out to `main`. This skill does not merge; if the user also asked to
    babysit/watch the PR ("file and babysit"), continue with `gh-babysit-pr`
    after opening — it must `gh pr checkout <n>` before any write operation.
    Do not auto-trigger Bugbot after open (`bugbot run` / `@cursor review`);
    see `gh-babysit-pr` → **Bugbot — Manual Only**.
13. **Return URL**: Output the PR URL and mention any post-PR actions you
    completed

## Assignee Policy

- Resolve assignee as `GH_ASSIGNEE="${GH_ASSIGNEE:-$(gh api user -q .login)}"`.
- Unless the user explicitly asks otherwise, every new PR must include
  `--assignee "${GH_ASSIGNEE}"`.
- **Do NOT request the PR author as a reviewer.** GitHub rejects self-review
  requests with exit 128. Visibility is achieved via the assignee field alone.
- After PR creation, enforce the assignee with:

```bash
gh pr edit --add-assignee "${GH_ASSIGNEE}"
```

- If assignee assignment fails (permissions/team constraints), report the exact GH error and PR URL.

## Label Policy

- If the user or automation prompt specifies labels, apply them after PR creation with `gh pr edit`.
- For multiple labels, call `gh pr edit` once per label so failures identify the missing label precisely.
- Treat labels such as `codex` / `codex-automation` as ordinary requested labels, not implied defaults. Add them when asked; do not invent them when not asked.
- If GitHub rejects a label because it does not exist or permissions prevent applying it, report the exact error and continue with the rest of the workflow.

## Quick Start (Most Common Path)

```bash
git status
BASE_BRANCH="main"  # override only if user explicitly named another base
GH_ASSIGNEE="${GH_ASSIGNEE:-$(gh api user -q .login)}"
python3 <skills-dir>/code-review/scripts/coderabbit_repo_review.py \
  --switch-org -- --base "${BASE_BRANCH}" || exit $?
git push -u origin HEAD
git log "${BASE_BRANCH}"..HEAD --oneline
git diff "${BASE_BRANCH}"...HEAD --stat
gh pr list --state merged --limit 15 --json title --jq '.[].title'
gh pr create --base "${BASE_BRANCH}" \
  --title "Title matching repo convention; says why it matters" \
  --assignee "${GH_ASSIGNEE}" \
  --body "$(cat <<'EOF'
## Summary
Plain-language problem statement from the original intent, then the fix briefly.

## Changes
- Main technical changes

## Testing
- What you ran (or "Not run")

EOF
)"
gh pr edit --add-assignee "${GH_ASSIGNEE}"
git checkout main
```

## Post-PR branch cleanup

After the PR is created, always leave the local repo on `main`:

```bash
git checkout main
```

This is mandatory even when the PR remains open for review. Do not leave the
local repo parked on the feature branch after the workflow.

## Expected Inputs (Clarify Early)

- Target repo; base branch defaults to `main` — only clarify if user explicitly wants a different base
- Treat terse automation prompts such as `$gh-pr-create against main` as a direct PR-create request with `main` as the base branch
- Treat alias prompts such as `use pr-creator`, `/pr-creator`, or `open PR ... using pr-creator` as the same direct PR-create request
- Optional `GH_ASSIGNEE` override
- PR title intent in imperative mood
- Testing status (run tests or explicitly say not run)

## PR Description Standards

**Format**:
```
## Summary
Plain-language statement of the problem, framed from the user's original intent
(what was wrong or missing, and for whom), then the solution in one or two
sentences. Never open with an implementation inventory.

## Changes
- The few modifications that matter, and any decision a reviewer should weigh
- Note any breaking changes

## Testing
- Describe validation performed (or say "Not run")

```

**Required**:
- Title matches the repo's convention (read recent merged PR titles first); concise, human-readable, says why it matters
- Body opens with the problem, then the solution — never a file-by-file inventory
- Professional tone for human reviewers

**Prohibited**:
- Co-authored-by tags (including `Co-authored-by: Cursor <cursoragent@cursor.com>`), AI signatures, "Written by <model>" attribution lines, AI advertisements or generated-by badges — anywhere: commits AND PR bodies
- `git commit --trailer` and `gh pr create` bodies that mention Cursor/AI authorship
- Generic descriptions like "Update files" or "Various changes"
- Emojis in the description

## Examples

**Bad title**: `Update postprocess.py and Makefile`
**Good title**: `Fix energy-budget undercount when interface cells straddle MPI boundaries`

**Bad description opening** (implementation inventory):
```
## Summary
- Modified getFacets() in postprocess.py
- Updated Makefile flags
- Added two tests
```

**Good description opening** (problem first, from original intent):
```
## Summary
Post-processed energy budgets from multi-rank runs disagreed with serial runs
by up to 3% because interface cells straddling MPI subdomain boundaries were
counted on both ranks. This deduplicates facet ownership by rank before the
reduction, so serial and parallel budgets now match to round-off.
```

## Commands Reference

```bash
GH_ASSIGNEE="${GH_ASSIGNEE:-$(gh api user -q .login)}"
BASE_BRANCH="main"

git push -u origin HEAD
git log "${BASE_BRANCH}"..HEAD --oneline
git diff "${BASE_BRANCH}"...HEAD --stat

gh pr create --base "${BASE_BRANCH}" \
  --title "Title matching repo convention" \
  --assignee "${GH_ASSIGNEE}" \
  --body "$(cat <<'EOF'
## Summary
Problem statement first, then the fix.

## Changes
- Change 1
- Change 2

## Testing
- Test 1

EOF
)"

gh pr edit --add-assignee "${GH_ASSIGNEE}"
gh pr view --json url -q .url
```

## Gotchas

1. **Dirty working tree at PR time** — always run `git status` before pushing. A PR created from a branch with uncommitted changes means those changes are invisible to reviewers and will not be part of the review diff.
2. **Do not add the PR author as a reviewer** — GitHub rejects self-review requests with exit 128. Use `--assignee "${GH_ASSIGNEE}"` only. If a real second reviewer is needed, ask the user for a specific username before passing `--reviewer`.
3. **No AI markers anywhere** — no attribution lines, generated-by badges, co-authored-by trailers, or tool advertisements in PR bodies or commit messages. Scan before posting.
4. **Base branch is `main` unless user overrides** — do not "detect" or "infer" a base. Assume `main`. If the repo genuinely has no `main` branch (legacy `master`, upstream fork), STOP and ask — do not silently guess.
5. **Requested labels are not automatic** — if the prompt calls for labels, add them explicitly with `gh pr edit --add-label ...` after PR creation.
6. **Leaving the local repo on the feature branch after PR creation breaks later automation** — always `checkout main` after the PR is opened so future runs start from a clean default branch.

## Error Handling

- If branch already has open PR: Inform user and provide existing PR URL
- If push fails: Check for uncommitted changes or remote conflicts
- If gh CLI not authenticated: Run `gh auth status` first
- If no commits ahead of base branch: Inform user there's nothing to PR
- Base branch is `main` by default; if the repo has no `main` and the user hasn't named another base, STOP and ask
- If requested label application fails: report the exact GH error, list which labels landed, and continue unless the user made label success a hard requirement
- For automation runs: if ambiguity remains after judgement calls, include an evidence-backed note under `Skill/Script Upgrade Candidates` in the PR description; do not block PR creation unless push/create fails technically

## Additional Resources

- [pr-template.md](references/pr-template.md) - Template variations by PR type
- [commands-reference.md](references/commands-reference.md) - Complete git/gh commands
