---
name: bmad-merge-wave
description: >
  Post-merge cleanup for a single wave. Verifies the wave's pull request is
  merged on the remote, pulls main fast-forward-only, removes the wave's
  worktree via an absolute git -C path, deletes the local branch, archives
  the wave checkpoint, marks the wave done in its lifecycle record, and
  verifies the cleanup. Idempotent across re-invocation.
when_to_use: |
  After a wave's PR is merged on the remote (any merge style), including when
  /bmad-status-wave shows a merged-with-worktree row. Not for abandoning an
  unmerged wave -- delete that branch and worktree manually.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
metadata:
  version: 1.3.0
  inputs:
    - wave-id (positional, required)
    - --verbose (optional; full git output instead of one line per step)
---

# bmad-merge-wave
Five steps, each with a precondition, an action, and a checkpoint marker under
.bmad/wave-<id>/cleanup/. If step N fails, steps N+1..5 do not run; re-invoke
after fixing and the skill picks up at the right step.

Variables, computed once at entry (the skill never uses cd; every git command
takes its repo via `git -C <abs-path>`):
- WAVE_ID: positional arg 1.
- MAIN_REPO: the main working tree, read from the first `worktree` record of
  `git worktree list --porcelain`, never from the invocation directory. The
  skill may be invoked from inside a worktree, and `git -C MAIN_REPO worktree
  remove` must address the main tree.
- BRANCH_SUFFIX: the wave's branch suffix from its waves.md row.
- WORKTREE_PATH and BRANCH_NAME: **resolved by discovery, never by path
  convention** (see below).
- CHECKPOINT_DIR: <MAIN_REPO>/.bmad/wave-<WAVE_ID>; CLEANUP_DIR:
  <CHECKPOINT_DIR>/cleanup. A session rooted in the wave's worktree writes
  the checkpoint and the lifecycle record in
  <WORKTREE_PATH>/.bmad/wave-<WAVE_ID>/ instead, which is ignored and goes
  with the worktree; step 3 adopts it into CHECKPOINT_DIR before removal.

## Resolving the worktree and branch

Parse `git -C MAIN_REPO worktree list --porcelain` into (path, branch) pairs,
stripping the `refs/heads/` prefix. BRANCH_NAME is the branch whose name is
BRANCH_SUFFIX or ends in `/BRANCH_SUFFIX`; WORKTREE_PATH is that record's path
if one exists. If no worktree carries the branch, search local branches the
same way with `git -C MAIN_REPO branch --format='%(refname:short)'`.

Discovery rather than convention, because two layouts are both in use and
neither is wrong. A worktree created by hand sits at
`<parent-of-MAIN_REPO>/<project>-wave-<WAVE_ID>` on branch `wave-<WAVE_ID>*`;
one created by the Claude Code harness sits at
`<MAIN_REPO>/.claude/worktrees/<slug>-<hash>` on branch `claude/<slug>-<hash>`.
Earlier versions of this skill reconstructed both by the first convention
alone, so against a harness worktree the preflight matched nothing, read that
as already-cleaned, and exited 0 having done nothing while the worktree and
branch stayed in place. Cleanup then had to be done by hand on every wave and
no checkpoint was ever archived, which is what the Epic 1 closure hit. A third
layout is a matter of a suffix match, not a third convention.

Ambiguity is refused, not guessed: if more than one branch matches
BRANCH_SUFFIX, refuse and name them. Matching on the suffix rather than on the
directory name also closes the mismatch the 2026-08-24 cleanup sweep found,
where a worktree directory named for one wave was checked out on an unrelated
branch.

## Step 1: Preflight (six checks, refuse-and-exit-1 on failure)
1. Wave exists in waves.md.
2. Worktree state: if present, it is a git worktree on BRANCH_NAME with a
   clean tree (`git -C <worktree> status --porcelain` empty). Dirty or
   wrong-branch: refuse. Absent: pass (idempotent).
3. Branch state: capture tip SHA. If worktree AND local branch are both gone,
   say the wave is clean on evidence rather than on a failed lookup, because
   an exit code of 0 has to mean the work is done and not that nothing was
   found to do. Check `git ls-remote --heads origin` for BRANCH_SUFFIX:
   - Absent there too: already cleaned up. Skip to step 5, exit 0.
   - Present and its pull request reads merged: a merged remote branch that
     was not auto-deleted. Normal, not an error. Report it in the summary as
     a remaining remote branch and continue; do not refuse.
   - Present with no merged pull request: refuse and name BRANCH_SUFFIX. Local
     resolution found nothing while unmerged remote work exists, which is
     either a resolution failure or a branch never fetched, and reporting a
     clean sweep would bury it.
4. PR merged: `gh pr view <BRANCH_NAME> --json number,state,mergedAt,mergeCommit,headRefName`.
   There is no `merged` field: `gh` rejects the whole call with "Unknown JSON
   field", so a spec naming it fails before it can judge anything. Merged is
   `state == "MERGED"`, equivalently a non-null `mergedAt`. No PR, or not
   merged: refuse with the PR URL. Capture the merge commit SHA.
5. Branch ahead of merge: commits past the merged head mean orphan work;
   refuse and name the SHAs to cherry-pick first.
6. Checkpoint: warn (not block) if checkpoint.json is missing or the last
   marker is not step-12.done, reading CHECKPOINT_DIR and, while the
   worktree exists, <WORKTREE_PATH>/.bmad/wave-<WAVE_ID>/.

## Step 2: Pull main
`git -C MAIN_REPO pull --ff-only origin main`. Verify local main is the merge
SHA or a descendant; abort on divergence (force-push suspected).

## Step 3: Remove worktree
First adopt the worktree's checkpoint into the main checkout, so removal
cannot take the wave's record with it:

    python3 {skill-root}/../bmad-dev-wave/scripts/wave_status.py adopt \
        --project-root MAIN_REPO --wave WAVE_ID --from WORKTREE_PATH

It copies every file under <WORKTREE_PATH>/.bmad/wave-<WAVE_ID>/ that
CHECKPOINT_DIR lacks and overwrites nothing. Exit 0: adopted, or nothing to
adopt. Exit 1: a file differs between the two copies; it names them and
copies nothing. Stop there: which copy is right is the founder's call, and
the wave gate denies this session a hand edit of `wave.md` in either place.
Do not copy the checkpoint by hand: `wave.md` is written by `wave_status.py`
and nothing else.

Then `git -C MAIN_REPO worktree remove WORKTREE_PATH` -- always from the main
repository path, never from inside the worktree being removed (the documented
git foot-gun this skill exists to prevent). If removal leaves a stale
registry entry: `git -C MAIN_REPO worktree prune` and re-verify. Absent
worktree: skip (idempotent).

## Step 4: Delete local branch
`git -C MAIN_REPO branch -d BRANCH_NAME`. If -d refuses AND step 1 verified
the PR merged, it was squash- or rebase-merged; escalate to -D. The -D
path is reachable only behind the verified-merged check -- never otherwise.

## Step 5: Verify cleanup
Worktree directory absent; worktree registry clean; branch absent; archive
checkpoint.json and the step-N.done markers under CHECKPOINT_DIR/archive/,
and the cleanup markers under CHECKPOINT_DIR/archive/cleanup/. The cleanup
markers are named step-1.done to step-5.done too, so archived beside the
wave's own markers they would overwrite five of them. Then mark the wave done:

    python3 {skill-root}/../bmad-dev-wave/scripts/wave_status.py set \
        --project-root MAIN_REPO --wave WAVE_ID --status done

This is the wave's terminal status and this skill is the only writer of it: a
wave is done when its pull request is merged and its worktree and branch are
swept, which is the state this step has just verified. Leave the lifecycle
record itself in place -- archive the checkpoint, not the record, because a
later dispatch reading no record would treat a swept wave as unmigrated and
infer its stage all over again.

The set exits 1 if the wave is blocked, and that refusal stands: a blocked
wave is not made done by cleaning up after it. Report it and stop; clearing
the block is the founder's act, not this skill's.

The archive is a step record, not a gate: epic closure reads it when present
and proves cleanup from live pull-request and worktree state, so a missing
archive blocks nothing. Print the five-line summary and exit 0.

## Merge-Type Acceptance
Merge-commit, squash, and rebase merges are all accepted; the only rejected
state is one that is not `MERGED`.

## Refusals
| Refusal | Trigger | Resolution |
|---|---|---|
| Unknown wave | wave-id not in waves.md | check spelling; /bmad-create-wave first |
| PR not merged | state is not `MERGED` | merge on GitHub (URL in diagnostic), re-invoke |
| Worktree dirty | porcelain non-empty | commit, stash, or discard; diagnostic prints the dirty paths |
| Branch ahead of merge | commits past the merge SHA | cherry-pick the named SHAs to a new branch |
| Wrong branch | worktree not on the resolved BRANCH_NAME | check out the wave branch or remove the worktree manually |
| Ambiguous branch | more than one branch matches BRANCH_SUFFIX | refuse and name them; disambiguate before re-invoking |
| Resolution failed | local branch absent while origin carries an unmerged one | refuse and name BRANCH_SUFFIX; fetch, or correct the waves.md suffix |
| Wave blocked | the status record reads blocked | refuse to mark it done; a human clears the block by editing or deleting `.bmad/wave-<id>/wave.md` |
Idempotent no-op: worktree gone, branch gone locally and on origin -> "already
cleaned up; nothing to do", exit 0. A merged remote branch left undeleted is
reported, not refused.

## Version history
- 1.3.0 (2026-10-17, ffbapp wave 6B): step 3 adopts the worktree's
  checkpoint into CHECKPOINT_DIR before removing the worktree, through
  `wave_status.py adopt`. A session rooted in the worktree writes
  `.bmad/wave-<id>/` there, ignored, so removal destroyed the record step 5
  then tried to mark done; 6B's was copied out by hand. Preflight check 6
  reads both places. Step 5 archives the cleanup markers under
  `archive/cleanup/`, where they no longer overwrite the wave's own
  `step-1.done` to `step-5.done`.
- 1.2.1 (2026-10-01, R4 of docs/reviews/harness-engineering-review-v1.md):
  frontmatter only. `when-to-use` is `when_to_use`, the field Claude
  Code reads, so it now reaches the skill listing; `version` and `inputs` sit under
  `metadata:`, which Claude Code leaves to the fork's own tooling. Nothing in
  the body changed.
- 1.2.0 (2026-09-11, Phase 2 of docs/harness-conversion-plan.md): step 5 marks
  the wave `done` in its lifecycle record once cleanup verifies, making this
  skill the only writer of that terminal status. The record survives the
  archive sweep on purpose: archiving it would make the next dispatch read a
  swept wave as unmigrated and infer its stage again. A blocked wave refuses
  the transition rather than being tidied into done.
- 1.1.0 (2026-08-24, founder ruling at the Epic 1 closure): worktree and branch
  resolved by discovery rather than by path convention, so a harness-created
  worktree is found instead of silently missed; the `gh --json merged` field
  corrected to `state`/`mergedAt`, which rejected the whole call; the
  already-cleaned no-op now checks the remote before claiming a clean sweep.
