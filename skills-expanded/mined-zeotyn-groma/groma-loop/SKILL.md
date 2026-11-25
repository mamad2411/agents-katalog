---
name: groma-loop
description: Runs a change through propose, apply, verify and archive with an independent reviewer model. Use for "groma-loop", "build this with review", "implement with a second model", or to review a proposal or implementation with another model.
---

# groma-loop

You are the **author** and the orchestrator. A different model is the **reviewer**. Every round: the reviewer finds, you answer each finding, the loop decides. The user is interrupted only on escalation (and, in `gated` mode, at the two gates).

**User language.** Talk to the user in the language of their latest message: questions, summaries, hints, warnings, escalations and the reasons for commands you print. Commands, paths, config keys and ids stay literal. Files you write, the findings report too, keep the language of their templates.

Paths are relative to this skill folder unless they start with `<project>`. Settings come from `review` in `<project>/.groma/config.yaml`; missing keys use these defaults: `mode: autonomous`, `stop_when: no-high`, propose `reviewer: auto, max_rounds: 2`, apply `reviewer: auto, per: task-group, max_rounds: 1, test_retries: 2`. The docs gate reads `docs.gate` (default `review`). The git steps read `git` (defaults `enabled: true`, `integrate: rebase`, `branch_per_change: true`, `commits: conventional`, `push: ask`) and run only inside a git repository. `git.enabled: false`: the project does not use git; skip every git step without asking and say "git steps skipped (git.enabled: false)" once in the summary; run no git command at all: review rounds read the files the unit changed instead of a `git diff`, and the archive's list of the change's docs is the docs the change edited.

## Start

1. **Change.** The user names an existing change or describes an idea. Existing change: start at the first phase whose work is missing (no tasks ticked → apply; all ticked → verify). New idea: start at propose.
2. **Methodology.** Read the matching section of [references/methodology-adapters.md](references/methodology-adapters.md).
3. **Reviewer.** For each phase you will run, resolve the reviewer once:
   ```sh
   sh scripts/resolve-reviewer.sh <your agent> --phase <propose|apply> --config <project>/.groma/config.yaml --author-model <your model>
   ```
   Say the result in one line, e.g. "Reviewer: gemini (other vendor)". `reviewer=self` means self-review: run each review as a fresh subagent or session that gets only the prompt file, and mark it `self-review` everywhere.
4. **Tests and style checks.** Find the project's test command (AGENTS.md, `package.json`, `Makefile`, CI workflow). No test command: say so once; the apply gate then only checks that the build or lint step passes, if any. Then read the "Enforced by tools" table of the code-style doc (`<project>/docs/code-style.md`, or the file the docs index lists for code style); its check commands run in every tests gate.
5. **Git.** Inside a git repository (`git rev-parse --is-inside-work-tree`) with `git.enabled` not `false`: `git status --porcelain` must print nothing. Otherwise escalate before anything else, with the options "commit or stash the files yourself, then rerun" and "continue without git steps" (then skip every git step below and say so in the summary). Then name the main branch `<main>` by the "Main branch" rule of [references/git-strategies.md](references/git-strategies.md) (the remote's default branch, else `main`, else `master`); when only a remote-only `origin/main` or the current branch is left, escalate and ask which branch is the main branch. When `branch_per_change` is true: on `<change-id>` already → go on; on `<main>` → `git switch -c <change-id> <main>` (`git switch <change-id>` when the branch exists); on any other branch or a detached HEAD → escalate ("switch to `<main>` or `<change-id>` yourself"). For a new idea this happens right after propose named the change. `branch_per_change: false`: stay on `<main>`; the integration step is then skipped. The change base `<change-base>` is `git merge-base <main> HEAD` on the change branch, else the parent of the commit that added `<change-dir>/proposal.md` (`HEAD` when that commit does not exist).

## Phases

Announce each step as `<Phase> · <unit> · round N of M`.

**Propose.** Write the change artifacts with the methodology's propose workflow. Then review rounds (below) on the artifacts. `gated`: after the loop, show a five-line summary (goal, scope, open rejected findings) and wait for approval. Git steps on: create the change branch (Start, step 5) and commit the change folder: `docs(<scope>): propose <change-id>` (`<scope>` from [references/methodology-adapters.md](references/methodology-adapters.md)).

**Apply.** Split the tasks into review units by `per` (task, task-group, change). For each unit:
1. Record the base: `git rev-parse HEAD` (or note "working tree" when uncommitted work exists).
2. Implement the unit's tasks, tick them.
3. **Tests gate.** Run the tests, then every check command from the code-style doc. A failing check counts as red tests. Red: fix and rerun, at most `test_retries` times; still red → escalate with the failing output (test or check). No review on red tests.
4. Review rounds on the unit's diff (`git diff <base>`), its tasks and the requirements they implement.
5. **Commit** (git steps on, review stopped clean): stage the files `git status --porcelain` lists (all of them belong to the unit, because the tree was clean at start) and commit with the user's configured git identity; never set one, never `--amend`, never `--no-verify`. Write every commit message to a file and use `git commit -F <file>` (never `-m`, so quotes, backticks and `$` in titles are safe); delete the file afterwards. Subject by `commits`: `conventional` → `<type>(<change-id>): <unit title>` with `<type>` from the change name by "Commit type" in [references/git-strategies.md](references/git-strategies.md) (`c` and `m<N>-` feat, `f` and `m<N>-fix-` fix, `r` and `m<N>-refactor-` refactor, `s` and `m<N>-spike-` chore; a unit that only adds tests: `test`); `free` → the unit title. The unit title is the task-group heading without its number, the task text for `per: task`, the proposal title (`<proposal title>` in [references/methodology-adapters.md](references/methodology-adapters.md)) for `per: change`. No git identity (`git config user.name` prints nothing) → escalate.

**Verify.** Run the methodology's verify step, then one review round on its report and the full diff (`git diff <change-base>`). Critical verify issues count as high findings. Git steps on: when `git status --porcelain` lists files after the round (fixes for findings, docs-gate answers), commit them as in Apply, step 5, with the subject `fix(<change-id>): address verify findings` (`commits: free` → "address verify findings"), so that nothing is left for the archive commit. **Docs gate** (`docs.gate` is `review` or `strict`): run `sh scripts/docs-impact.sh --root <project> <change-dir>` and add every `impact` and `adr` line as a high finding of that round. Answer an `impact` finding by updating the doc or by adding a task line `Docs: <path> unchanged, because <reason>`; answer an `adr` finding by writing the proposed ADR as "ADR candidates from a change" in `../groma-lay-out/SKILL.md` describes. groma-lay-out missing: tell the user to add it (`npx skills add Zeotyn/groma --skill groma-lay-out`) and leave `adr` lines out of the findings; `impact` lines still count.

**Archive.** `gated`: wait for approval. `strict`: run `scripts/docs-impact.sh --gate` first; exit 4 → escalate with the report instead of archiving. groma-lay-out missing: exit 4 also fires on `adr` lines, so ignore the exit code, read the `summary` line and escalate only when its `impact=<n>` is not 0. Before archiving, list the change's docs: `git diff --name-only <change-base> -- docs/` plus `git ls-files --others --exclude-standard -- docs/` (`<change-base>` from Start, step 5). Then archive with spec sync, followed by the **docs sync** (skip it when `docs.gate` is `off`). These edits are authored work inside the user's change, like its code, not setup writes; they touch only the docs on that list:
1. Every ADR in `<project>/docs/adr/` with `origin: <change>#…` and `status: proposed` → `status: accepted`.
2. `last_reviewed` → today in every listed doc that has the key.
3. In `docs/adr/README.md`, set the status cell of each ADR accepted in step 1 to `accepted`, and add a row for every listed ADR still missing.
4. Run `sh ../groma-methodology/scripts/roadmap.sh --root <project>` (groma-methodology's roadmap). groma-methodology missing: skip it and tell the user to add it (`npx skills add Zeotyn/groma --skill groma-methodology`) to keep `docs/roadmap.md` current.

Then the **git steps** (git steps on). These git operations are authored work inside the user's change too:
1. **Archive commit.** Stage the archive move, the spec sync and the docs sync and commit: `docs(<scope>): archive <change-id>`.
2. **Integrate** (on the change branch). Follow the "Procedure" of [references/git-strategies.md](references/git-strategies.md) with the row of `git.integrate`:
   - before the row: `git status --porcelain` prints nothing (the archive commit left it clean); when `<main>` is checked out in another worktree (`git worktree list --porcelain`), that worktree must be clean too, and every main-side command runs there as `git -C <main worktree> …` without the `git switch` commands ("Linked worktrees"); record `git rev-parse <main> <branch>`; when a remote exists, `git fetch`, and fast-forward `<main>` to its upstream when it is behind (`git merge --ff-only <main>@{u}`), escalate when it diverged ("run `git pull --ff-only` on `<main>` yourself, then rerun");
   - the row's commands in order, with `<main>` and `<branch>` resolved and the squash message (`<type>(<change-id>): <proposal title>`, `<change-id>: <proposal title>` with `commits: free`) in a file for `git commit -F`;
   - the first failing command stops the sequence: conflicting paths (`git diff --name-only --diff-filter=U` where the command ran) → note them, run the row's abort commands, check the recorded refs, escalate with the paths; no conflicting paths (already integrated, refused fast-forward, failing hook) → no abort, escalate with git's output and the current branch.
   The branch stays after a successful integration. Never delete it, never `--force` or `--force-with-lease`, never `git branch -f`, `git update-ref` or `git reset --hard` on `<main>`, never a merge commit when the strategy is `rebase`.
3. **Push** `<main>` by `git.push`: `auto` → `git push`; `ask` → ask "Push `<main>` to its remote?" and push only on yes; `never` → do not push, the summary says "not pushed (git.push: never)". No remote: say so. A rejected push → escalate; never retry with `--force`. Only `<main>` is pushed: a change branch that was pushed earlier and diverged through the rebase stays as it is, and the summary mentions it.

## Review round

1. **Prompt.** Build `<change>/reviews/.prompt-<phase>-<n>.md` from [references/review-prompt.md](references/review-prompt.md): the phase's artifacts or diff, the project rules (AGENTS.md, accepted ADRs and the code-style doc), and all earlier findings with your responses.
2. **Run.** `sh scripts/review.sh <reviewer> <prompt-file> <change>/reviews/.raw-<phase>-<n>.md` (or the fresh-context self-review). Exit 5: the reviewer failed; resolve again without it and record why.
3. **Answer every finding.** For each row: either fix it and write `fixed: <what changed>`, or write `rejected: <reason>`. A rejected finding is not argued again unless the reviewer brings new evidence.
4. **Record.** Write `<change>/reviews/<phase>-round-<n>.md` from [templates/review-record.md](templates/review-record.md) with all findings and responses. Delete the `.prompt-*` and `.raw-*` files.
5. **Decide.**
   - stop criterion holds (`no-high`: no open high finding; `no-findings`: no open finding; rejected counts as closed) → `stop-clean`, next phase.
   - round limit reached with open high findings → `escalate`.
   - you rejected a **high** finding → `escalate` (a human decides disagreements on high findings).
   - otherwise → next round with the fixes.

Done when the record exists and its `decision` is set.

## Escalation

Stop the loop, keep all work and records, and send one message:

```
groma-loop stopped: <cause, one line>
<the open findings or the failing test output, at most 10 lines>

Options:
1. <apply the reviewer's suggestion>
2. <accept the risk and continue>
3. <change the design / split the change>
```

Escalate also before any destructive step outside the change: deleting files that existed before the change, rewriting git history, force-pushing. Git causes, each with its own options:
- dirty working tree at start → "commit or stash the files yourself, then rerun" or "continue without git steps";
- no main branch, another branch or a detached HEAD at start, or `<main>` checked out in a dirty worktree → "name the main branch", "switch to `<main>` or `<change-id>` yourself", "clean that worktree";
- `<main>` diverged from its upstream → "run `git pull --ff-only` on `<main>` yourself, then rerun";
- integration conflict (after the abort, naming the conflicting paths) → "resolve the conflict yourself and run the integration commands" or "leave the branch for a later integration";
- integration failure without conflicts (git's output, the current branch) → "fix the cause and rerun the integration commands" or "leave the branch as it is";
- rejected push → "run `git pull --ff-only` on `<main>`, rerun the integration and push" or "push yourself"; groma never pushes with `--force`.

## Summary

At the end print: phases run, rounds per phase, reviewer per phase (with `self-review` marked), findings fixed and rejected (list every rejected one with its reason), test result, archive location, git result (branch, commits made, how it was integrated into `<main>`, pushed or "not pushed (git.push: never)", or "git steps skipped"), and the next action.
