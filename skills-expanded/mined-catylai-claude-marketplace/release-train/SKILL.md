---
name: release-train
description: "Runs a large change as a release: a leader proves work bundles touch disjoint files, gives each worker its own git worktree off release/<slug>, verifies every worker branch, and merges in dependency order. Use when a change spans many files or several repositories and splits into independent workstreams. Not for one focused change (do it directly); not for writing the plan (use writing-plans); not for opening the request that lands it (use github-workflow:pr-lifecycle or gitlab-workflow:mr-lifecycle). Claude Code only."
argument-hint: "[release slug, or a short description of the change]"
disable-model-invocation: true
allowed-tools: Bash(git ls-files *), Bash(git log --oneline *), Bash(git diff --stat *), Bash(git diff --name-only *), Bash(git rev-parse *), Bash(git config --get *), Bash(mktemp -d), Bash(sort *), Bash(comm -12 *), Agent, SendMessage, TaskStop
license: MIT
---

# Release train

The change to run: $ARGUMENTS

An orchestrated release. One leader session supervises a small set of named worker subagents, each
pinned to its own git worktree, all converging on one shared `release/<slug>` branch per repository.

This is the procedural counterpart to `agent-craft:agent-orchestration`, which supplies the doctrine:
when delegation earns its token multiplier, hub-and-spoke routing, decomposition as the owner of
coverage, complete context in the spawn prompt, review by a fresh instance. Read it first. This file
specifies the mechanics that doctrine leaves open when the delegated work **writes to a shared
repository** instead of returning a report. If the work arrives as a plan from `writing-plans`, its
`Files:` blocks are the bundle paths.

**The admission criterion is disjointness, not worker count.** If you cannot demonstrate that the
bundles touch non-overlapping sets of files, you do not have parallel work. You have one serial job
and a merge conflict scheduled for later.

**Shell state.** Shell variables do not persist between Bash calls. In the commands below,
`<slug>`, `<bundle>`, `<branch>` and `<base>` are placeholders: write the real values literally into
every call. A variable assigned inside a block (`WORK`, `BEFORE`, `AFTER`) is used only within that
block, so run each such block as a single Bash call. The one value needed much later, the release's
starting commit, is stored in git config (section 2).

## Forge neutrality

This skill converges branches with `git` and stops there: no pull or merge request, no review state,
no forge CLI. Once the release branch is green and integrated, opening the request that lands it
belongs to `github-workflow:pr-lifecycle` or `gitlab-workflow:mr-lifecycle`. The orchestration
discipline below is identical on every forge, which is why it stays out of a provider API.

## When to run it, and when not

| Situation | Verdict |
| --- | --- |
| A change touching many files across areas you can name separately | Run it |
| A change spanning several repositories that must land together | Run it |
| One focused change, however large it feels | Decline; do it directly |
| Work where every bundle needs the same deep shared context | Decline; the briefing cost exceeds the fan-out saving |
| Bundles you cannot prove disjoint after two attempts at recutting | Decline; collapse to fewer, larger bundles |

Declining is a normal outcome and should be stated plainly, with the reason.

## 1. Decomposition, and proving the bundles disjoint

A **bundle** is the unit a worker owns. It carries a name, a repository root, an explicit list of
owned path globs, the new paths it plans to create, acceptance criteria phrased as observable facts,
and any `depends_on` edges to other bundles.

The leader writes the bundles, then *proves* the disjointness rather than eyeballing it. Comparing
globs as strings is the failure that looks like success: two globs where neither is a textual prefix
of the other can still select the same files.

```text
Bundle A owns:  services/*/config/**
Bundle B owns:  services/billing/**
```

Neither glob is a prefix of the other, so a string comparison calls them disjoint. They share every
file under `services/billing/config/`.

Expand each bundle to a concrete file set and intersect the sets, from the repository root:

```sh
WORK=$(mktemp -d)                                  # one Bash call for the whole block
git ls-files -- ':(glob)services/*/config/**' | sort > "$WORK/bundle-a"
git ls-files -- ':(glob)services/billing/**'  | sort > "$WORK/bundle-b"
comm -12 "$WORK/bundle-a" "$WORK/bundle-b"        # any output at all means not disjoint
```

The `:(glob)` pathspec magic is load-bearing. Without it, git's default matching lets a bare `*`
cross `/`, so the expansion is wider than the glob you wrote. With `:(glob)`, `*` stops at a path
separator and `**` crosses one, which is what the bundle definition means.

Run the intersection for every pair: three bundles are three pairs, five are ten. It is cheap, and
it is the only check that answers the question.

Two cases the intersection alone misses; handle both before dispatch:

- **Files that do not exist yet.** `git ls-files` sees tracked files only. Append each bundle's
  planned new paths to its file set before intersecting, so two bundles creating the same path
  collide on paper rather than at merge.
- **Files every bundle needs.** A lockfile, a changelog, a central registry or barrel file, a
  generated index, a shared type module. These are the real source of release-train conflicts. Two
  ways out: assign the file to **exactly one** bundle and have the other workers state their required
  change in their report for that owner to apply, or hoist it out of the fan-out — the leader makes
  the shared edit once, before dispatch or after integration, in a single pass.

When a pair overlaps, **merge them into one bundle**. Worktree isolation separates uncommitted state;
it does nothing about two commits changing the same lines.

Keep the count small. Every additional worker adds a brief to write, a branch to verify, a merge to
order, and a share of the leader's finite attention. Start with three to five workers.

## 2. A worktree per worker, created by the leader

Every worker gets its own worktree, with its branch cut from the shared release branch. A shared
checkout has one HEAD and one working tree, so two agents in it contend for the same files; separate
worktrees give each worker its own HEAD, index, and files while sharing one object database and refs
namespace, so the leader can inspect and merge every worker branch from the base checkout without a
fetch.

The leader creates the release branch and every worktree before dispatch, under the repository's
`.claude/worktrees/` directory (add it to `.gitignore`). Cut the release branch from the
repository's base on the remote, not from whatever happens to be checked out, so no stray local
work rides along:

```sh
git fetch origin "<base>"
git switch -c "release/<slug>" "origin/<base>" && git push -u origin "release/<slug>"
git config "branch.release/<slug>.releasetrainstart" "$(git rev-parse "release/<slug>")"   # start point, for section 8
```

Then, once per bundle:

```sh
git worktree add ".claude/worktrees/<bundle>" -b "rt/<slug>/<bundle>" "release/<slug>"
git config "branch.rt/<slug>/<bundle>.releasetrainbase" "release/<slug>"   # config is shared by all worktrees
```

The `releasetrainstart` key survives across Bash calls and compaction, which a shell variable does
not. The `releasetrainbase` key tells `dev-guardrails:session-sync` which base this branch belongs to, so
a later repo-wide sweep rebases it onto `release/<slug>` rather than the default branch.

**Why not the built-in `isolation: worktree` worktree on its own:** Claude Code creates that worktree
from the repository's default branch (or the current `HEAD` with `worktree.baseRef: "head"`), on a
branch it names itself, and the periodic cleanup sweep eventually removes it. It cannot take a branch
name as its base, and its branch name is not one the leader chose, so it cannot carry the
`rt/<slug>/<bundle>` bookkeeping or the `releasetrainbase` key set before dispatch.

**How a worker enters its worktree.** Spawn each worker with the Agent tool, giving it a `name` and
passing `isolation: "worktree"` on the call. Its brief opens with one instruction: call
`EnterWorktree` with `path` set to its worktree under `.claude/worktrees/`. A subagent running
with worktree isolation can use only that `path` form of `EnterWorktree`, and only for a target
under `.claude/worktrees/` of the session's repository, which is why the leader places worktrees
there. The throwaway worktree the
isolation created stays empty, so Claude Code removes it when the worker finishes. Once inside, Claude Code blocks
the worker's edits and git commands that target the main checkout. If `EnterWorktree` refuses the
path — for example a second repository outside the session's own — the worker reports `blocked`
with the refusal text and stops; run that repository's bundles from a session started there.

One worker, one repository, one worktree, for the whole run.

**Agent teams.** When `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set, a named Agent call normally
launches a teammate. A call that passes `isolation` launches an ordinary subagent even then, so this
procedure behaves the same with teams on or off. It does not use the team task list; the leader
tracks bundles itself.

## 3. What the leader keeps, and what it delegates

The leader supervises. Its context window is the integration budget, so it stays out of bundle code.

| Leader keeps | Delegated to workers |
| --- | --- |
| Decomposition and the disjointness proof | Implementation inside one bundle |
| Creating the release branch and every worktree | Committing, and pushing its branch once as a backup |
| Writing each brief | Choosing how to satisfy the acceptance criteria |
| Verifying each branch against its declared scope | Reporting a short structured status |
| Merge order and conflict adjudication | Rebasing and resolving conflicts in code it wrote |
| Cross-bundle integration and the final verification | Nothing cross-bundle |
| The decision to stop, recut, or decline | Nothing about scope |

The one exception is the shared-file edit hoisted out of the fan-out in section 1: a single small
change the leader makes deliberately.

The brief is the entire budget. A worker's spawn prompt is its only channel in, so it carries the
worker's name, its worktree path and the `EnterWorktree` instruction, its owned paths and planned new
paths, its acceptance criteria, the base it branched from, and the report shape — nothing else. A
full plan, a prior handoff, or this file in the brief inflates every worker's window with context it
will not use.

## 4. Bounded supervision

Everything the leader spends on watching is unavailable for merging, and a leader that runs out
mid-integration cannot be rescued: it is the only session holding the shape of the whole change.

- **Wait on completion notifications.** Where you must check, do so on a bounded cadence with an
  explicit cap on the number of checks, and report a timeout when the cap is reached.
- **Read the branch, not the transcript.** Workers report a few lines of structured status; the
  ground truth is on disk, and `git log --oneline` and `git diff --stat` cost a fraction of a
  transcript.
- **Start long commands in the background** and check them later; a Bash call has a timeout.
- **Treat a long window before integration as a bad cut.** Too many bundles, or bundles too small
  to be worth a session. Stop, collapse them, and say so.

## 5. Verifying a worker, because its own report is not evidence

A worker reporting success is a claim about its intent. Check the branch from the base checkout;
branch refs are shared across worktrees, so no `-C` is needed.

```sh
git log --oneline "release/<slug>..<branch>"      # commits actually exist
git diff --stat "release/<slug>...<branch>"       # and are not empty
git diff --name-only "release/<slug>...<branch>"  # and stay inside owned paths
```

The three-dot form diffs against the merge base, so commits other bundles already landed on the
release branch do not show up as this worker's changes.

| What you find | Verdict |
| --- | --- |
| No commits, or a diff that is entirely empty files | Reported done, produced nothing. Re-dispatch. |
| Changed files outside the bundle's owned paths | Scope violation. It may already conflict with another worker's branch, so adjudicate before any merge. |
| Work present, acceptance criteria not observably met | Send it back once with the specific unmet criterion. |

A scope violation found *after* the work is the defect the disjointness proof prevents *before* it:
the proof ran on the wrong globs, or the bundle grew during the run.

## 6. Integration

Merge into the release branch in dependency order first: a bundle another bundle `depends_on` lands
before its dependent. Among bundles with no edges between them, land the widest one first, so the
remaining workers rebase onto the larger change.

For each bundle, in that order:

1. **Bring the base checkout current**, so the rebase target is the real release tip:

   ```sh
   git pull --ff-only origin "release/<slug>"
   ```

2. **Have the worker rebase.** Resume it with `SendMessage` (to its name) and ask it to confirm it is
   in its worktree (`git rev-parse --show-toplevel`; re-enter with `EnterWorktree` if not), run
   `git rebase "release/<slug>"`, resolve any conflict in its own code, rerun its bundle's tests, and
   report. The local `release/<slug>` ref is shared, so the worker needs no fetch. A worker stopped
   with `TaskStop` resumes the same way once its stopped run has exited. If `SendMessage` is refused
   because the agent was cancelled (a user stop), dispatch a fresh one with the section 7 brief.
3. **Re-verify** with the section 5 commands. A rebase can pull a branch out of scope.
4. **Merge and confirm the ref moved:**

   ```sh
   BEFORE=$(git rev-parse "release/<slug>")        # one Bash call for the whole block
   git merge --no-ff "<branch>"                    # bookkeeping only after the rebase
   AFTER=$(git rev-parse "release/<slug>")
   if [ "$BEFORE" = "$AFTER" ]; then echo "ref did not move: merge stopped, or branch already merged or empty"; exit 1; fi
   git push origin "release/<slug>"
   ```

   The worker rebased onto this same local ref, so the merge should not conflict; if it stops
   anyway, run `git merge --abort` and re-verify the branch with section 5. What can
   fail is the push: a non-fast-forward rejection means someone else pushed to `release/<slug>`.
   Stop there and report it. The release branch has one writer, the leader; reconciling a second
   writer is a decision for the user, and a force push here would discard their commits.

**Why the rebased worker branch is not pushed again.** The worker pushed its branch once as a backup,
so after the rebase its remote copy has diverged and a second push would need a force push. The
merge reads the local, rebased branch through the shared refs, and only `release/<slug>` needs to
reach the remote — so the whole run stays free of force pushes. The stale remote worker branch is
harmless; delete it at cleanup.

If disjointness held, conflicts are structural rather than semantic: a lockfile, a generated index, a
changelog, an import barrel. Those resolve mechanically. **A semantic conflict is a decomposition
bug**: stop merging, record which files collided, and recut. The leader decides *who* resolves a
conflict and leaves the resolution to the author of the code.

## 7. When a worker fails or stalls

Define a stall before the run: no new commit and no status between two consecutive supervision
checks. Then the ladder is fixed, and it ends in an explicit decision:

1. Ask the worker directly, once, naming what you expected to see.
2. No useful answer — stop it with `TaskStop`. Keep its worktree and branch; the branch is the record.
3. Inspect the branch with the section 5 commands and decide: usable partial work, or nothing.
4. Dispatch a fresh worker into the same worktree with a brief that names exactly what already
   landed on that branch and what remains. Start fresh because the stalled window is what failed.
5. If the same bundle fails twice, it is too large or under-specified. Split it or fold it into the
   leader's own serial work, and say which.

A failed bundle that no other bundle depends on does not stop the release. One that others depend on
does: land its dependents only after it is genuinely complete.

## 8. Verify the release

Before handing the release branch on:

1. Run the repository's own build and test commands (from its README, CI config, or package
   manifest) in the base checkout on `release/<slug>`. A failure here is an integration defect:
   identify the bundles whose files are involved and send the fix to their owner.
2. Confirm the release touched only what was planned. Read the starting commit stored in
   section 2, and stop if it prints nothing, because an empty start turns the diff into
   `HEAD..release/<slug>`, which is empty and would pass every check:

   ```sh
   git config --get "branch.release/<slug>.releasetrainstart"
   git diff --name-only "<start-sha>..release/<slug>"    # the SHA printed above, written literally
   ```

   Every path should fall inside the union of the bundles' owned paths, planned new paths, and the
   hoisted shared edits. Anything else is unexplained and gets named in the report.
3. Run the integration review with a fresh instance, per `agent-craft:agent-orchestration`.
4. Clean up: `git worktree remove .claude/worktrees/<bundle>` for each worker, then delete the
   local and remote worker branches. Deleting a local branch also removes its `releasetrainbase`
   key.

Report: bundles landed (in order), bundles declined or folded, the build and test result, and any
unexplained paths.

## Worked examples

<example>
Request: "Run the auth refactor as a release across the API service and the web client."

Correct: cut bundles per repository with declared owned paths; expand and intersect every pair,
including the new files each bundle plans to create; create `release/auth-refactor` in both
repositories and one worktree per bundle under `.claude/worktrees/`; dispatch one named worker per
bundle with worktree isolation and an `EnterWorktree` first step; supervise on a bounded cadence;
verify each branch against its owned paths; for each bundle in dependency order, fast-forward the
base, have the worker rebase, re-verify, merge, and confirm the ref moved; build and test the release
branch; hand it to `github-workflow:pr-lifecycle` to open the request that lands it.
</example>

<example>
Request: "Fix the typo in the retry-policy docs."

Correct: decline the fan-out and do it directly. One focused change has no independent subtasks to
name, so the multi-agent multiplier buys nothing (`agent-craft:agent-orchestration` rule 1).
</example>

<example>
Two bundles are proposed as `services/*/config/**` and `services/billing/**`.

The pairwise intersection returns 40-odd files under `services/billing/config/`. Neither glob is a
prefix of the other, so a string comparison would have called them disjoint.

Correct: merge them into one bundle. Wrong: give them separate worktrees and expect the merge to
sort it out — separate worktrees isolate working state, not commits.
</example>

<example>
A worker reports "done, all criteria met." `git diff --name-only release/x...branch` lists two files
outside its owned paths, one of which another worker also owns.

Correct: treat the bundle as unverified. Adjudicate the shared file to a single owner before any
merge, have the violating worker revert its half, and re-verify. Merging first and reconciling
afterwards is how a release train produces a branch nobody can explain.
</example>

## Failure modes

**Disjointness assumed from the glob strings.** The most common one, and it fails silently until the
second merge. The intersection is three commands.

**A leader that started coding.** It writes one "quick" bundle itself, then has neither the window
nor the neutrality to integrate the rest.

**Tight-loop polling.** The leader spends its budget confirming that workers are still working, then
compacts mid-integration and loses the merge order it was holding.

**Worker reports treated as verification.** Nothing produced, out of scope, criteria unmet — all
present as the same cheerful message.

**A worker left in the throwaway isolation worktree.** It skipped the `EnterWorktree` step, so its
commits land on a branch cut from the default branch. Section 5 catches it: the log against
`release/<slug>` shows commits the release never had.

**Hand-resolving a semantic conflict.** It merges, it builds, and the behaviour is a blend neither
worker designed. A semantic conflict means recut.

## Surface

Claude Code only. This skill spawns subagents, creates worktrees, and runs `git`; Cowork has no
checkout and no shell. There is no degraded mode: a release train without workers is a serial
session, and you should run that deliberately.
