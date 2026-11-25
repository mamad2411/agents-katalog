---
name: gabito-entrega
description: Delivers work through Git on GitHub, GitLab and Bitbucket with the saved settings: commit, push, PR and merge via gabitotl vcs, no repeated questions. Trigger: committing, pushing, opening or merging a PR/MR, or finishing a task.
license: Apache-2.0
metadata:
  author: gabitotl
  version: "1.0"
---

# Gabito delivery: commit, push, PR, merge from saved settings

Delivery settings are asked once and saved. After that you act without prompting.
Never ask the user again what `vcs.md` already answers. The one exception is publishing to GitHub or GitLab
(see "Save CI minutes").

## 1. Check state

Run `gabitotl vcs status`. Read three things:

- `delivery:` If it says not configured, set it up as a short conversation, ONCE (see "Setup by dialogue").
  Do not pre-answer for the user, and do not ask again once configured. To change one answer later, run
  `gabitotl vcs setup --yes` with the matching flag (`--vcs-automation`, `--vcs-merge-method`,
  `--vcs-delete-branch`, `--vcs-draft`, `--vcs-provider`), only when the user asks.
- `auth:` If it is not ok, run `gabitotl vcs login`. It uses `gh auth` or `glab auth`, or for Bitbucket a token
  from an environment variable. Show the user the exact fix it prints. `gabitotl vcs login --check` only verifies.
  Never loop on login prompts: run it once, report the result, and stop if it still fails.
- The current branch and the base branch.

## Setup by dialogue

You ask the questions, in chat; the user is never sent to a terminal prompt.

1. Run `gabitotl vcs setup --questions`. It prints JSON and changes nothing: the questions that apply now (`id`,
   `title`, `options` with `value` and `label`, `default`), the `flag` that carries each answer, the inferred
   platform, and `scope` (`team` asks everything, `personal` asks only how much to automate for this person).
2. Ask ONE question at a time with the runtime's question tool if it has one, else in plain chat with numbered
   options, using each `title` and `label` as given. Mark the `default`. Then STOP and wait for the answer.
   Skip a question whose `only_if_automation` does not include the automation answer. Never invent questions:
   nothing about PR size, budgets, chaining or exceptions.
3. When every answer is in, save them in ONE call:
   `gabitotl vcs setup --yes --vcs-automation=all --vcs-merge-method=squash --vcs-delete-branch=true --vcs-draft=false`
   (omit `--vcs-provider` when the platform answer is `none`). Say in one line what was saved and where.
4. If the user said "no preguntes" or "usá lo estándar" (or "don't ask" or "use the defaults"), use the defaults for the open
   questions.

Without a terminal, `gabitotl vcs setup` alone changes nothing and exits with an error; that is expected.

## 2. Deliver

Preferred path, one command:

`gabitotl vcs ship --title "feat(scope): summary" [--body "..."] [-m "feat(scope): summary"]`

It commits pending changes, pushes the task branch, opens the PR/MR and merges when the settings allow and the
checks pass. It never asks, so on GitHub or GitLab get the user's OK before running it (see "Save CI minutes").
Use `--dry-run` to preview the plan, `--json` for machine output.

Step by step when you need control:

1. `gabitotl vcs commit -m "<conventional message>" [--paths a,b]`
2. `gabitotl vcs push`
3. `gabitotl vcs pr --title "..." [--body "..."] [--base BRANCH]`
4. `gabitotl vcs merge [--pr URL|NUMBER]`

## Rules

- Commits are Conventional Commits: `type(scope): imperative summary`. One logical work unit per commit,
  with its tests and docs.
- No attribution of any kind: no co-author trailers, no "generated with/by" lines, no AI names or links, in commits,
  PR titles, PR bodies or comments. Authorship belongs to the person who asked.
- Write commit messages and PR text in English, unless the project history clearly uses another language.
  The PR body says what changed, why, how it was verified, and any OJO (Heads-up in English).
- Never commit or push the base branch. If you are on it, `ship` moves the work to a task branch; create or
  switch to one yourself (`feature/<task>`) otherwise.
- Never force-push, amend a published commit, rebase shared history or `git reset --hard`. Undo shared changes
  with a revert commit. The CLI refuses these anyway.
- Never run `git push`, `gh` or `glab` yourself to bypass `gabitotl vcs`; the guard and settings live there.
- Merge only when the checks pass. If checks are failing or pending past the wait, report it. Do not merge by hand.
- Keep secrets out of `.gabitotl/`. Only references (`env:NAME`, `keychain:NAME`, `native`).

## Save CI minutes: push by milestone (GitHub and GitLab)

On GitHub and GitLab every push, PR update and merge can start paid CI runs (Actions minutes, CI/CD minutes).
`gabitotl vcs status` shows the platform. There:

- Work locally. Commit each work unit on the task branch; local commits are already the rollback point.
  Do not push after every commit.
- Publish only when an important milestone is done (a feature or fix ready for review, the end of a stacked series).
  Ask the user first in one short question, even when the saved automation is `all`. This is the one question the
  saved settings never answer. Then publish everything in one go with `gabitotl vcs ship`.
- Never push to "see if CI passes": run the same checks locally first (build, tests, vet, lint).
- After a review comment or a failed check, fix everything, verify locally and push once, not fix by fix.
- On Bitbucket and other hosts the saved settings decide, as usual.
- If the project's CI wastes minutes, propose (never apply unasked) with an everyday example: `concurrency` with
  `cancel-in-progress: true` so a new push cancels the outdated run, `paths-ignore` for docs-only changes, and not
  running heavy jobs on draft PRs.

## Big work: stacked PRs, automatically

When the change exceeds the saved PR budget (`pr_budget_lines` in `vcs status`), `gabitotl vcs ship`
slices it into stacked PRs at commit boundaries: each PR targets the previous one, and the parts merge in order.
So commit per work unit, and let `ship` cut the stack. Preview it with `gabitotl vcs ship --dry-run`.

Never ask the user about PR size, a budget exception or an exemption. The saved settings decide.
Do not split commits artificially or delete tests and docs to fit a budget.

## When a setting blocks you

Settings are `allow`, `ask` or `deny` per operation (branches, commits, push, pull requests, merge).

- `allow`: act, do not mention it.
- `ask` or `deny`: stop. Say which setting blocked the step and the command to change it, for example
  `gabitotl vcs setup --vcs-automation=all`. Do not retry, do not work around it, do not ask again later.
- If the user wants to merge themselves (`until-pr`), deliver up to the PR and give them the link.

## After delivery

- Report the commit hash, PR link and whether it merged, in the short persona blocks.
- Save the closed task to memory (`gabito-memoria`) and update the declared work (`gabito-equipo`).
- If a step failed, give the exact message and the one fix; do not paraphrase an error away.
