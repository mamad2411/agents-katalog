---
name: upgrade-execute
description: "Carries out an approved .upgrade/plan.md one step at a time: apply one change, make the code edits it forces, compare every gate against the recorded baseline, and make one local commit per step, reverting and reporting any step that fails. Use when the user runs /dependency-upgrades:upgrade-execute after upgrade-plan. Not for deciding what or in what order to upgrade (use upgrade-plan). Claude Code only: it edits code, runs the suite and commits; it never pushes."
argument-hint: "[plan path, default .upgrade/plan.md] [step numbers, default all]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit(.upgrade/**), Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git rev-parse *), Bash(git add *), Bash(git commit *), Bash(git switch -c *), Bash(git revert --no-edit *), Bash(git revert --abort), Bash(mkdir -p .upgrade/*)
license: MIT
---

# upgrade-execute

Stage 4 of the upgrade pipeline. Arguments: `$ARGUMENTS`. A token ending in `.md` is the plan path
(default `.upgrade/plan.md`); numbers select steps to run (default: every step, in plan order). The
plan, baseline and step formats are defined in
[plan-format.md](${CLAUDE_SKILL_DIR}/../upgrade-plan/references/plan-format.md), owned by
`upgrade-plan`. Run from the repository root.

The discipline in one line: one change, verified against the baseline, committed alone, before the
next change starts. A failure then names its own cause, and `git bisect` can find any later one.

## Invariants

- Work only in local commits on a non-default branch. Pushing, force-pushing, amending, rebasing and
  resetting commits stay with the user; to undo a committed step, use `git revert`, which adds a
  commit instead of rewriting one.
- One plan step per commit. Two steps that both passed still get two commits.
- Let commit hooks run. A hook failure is fixed at its input, or the step fails.
- Shell variables do not survive between Bash calls, so write SHAs and results into `.upgrade/`
  files and read them back, rather than carrying them in variables.

## Preflight

Copy and tick:

```
- [ ] Plan parses: Plan-Format 1, every field present, Decision is proceed or proceed-unverified
- [ ] Tree clean
- [ ] On a non-default branch
- [ ] Baseline valid for HEAD
- [ ] Step log in .upgrade/report.md started or read back
```

1. **Plan.** Read the plan. If a field is missing, a value is outside its enum, or `Decision` is not
   `proceed` or `proceed-unverified`, stop and name the defect; the fix is to re-run `upgrade-plan`,
   not to guess. With no plan at all, stop and suggest `upgrade-plan`.
2. **Tree.** `git status --porcelain` must print nothing (`.upgrade/` ignores itself). If it prints
   anything, show the list and ask the user to commit or stash it. Their uncommitted work is theirs
   to move, and an unrelated change makes every later revert ambiguous.
3. **Branch.** Run `git rev-parse --abbrev-ref HEAD` (prints `main`) and
   `git rev-parse --abbrev-ref origin/HEAD` (prints `origin/main`). Remove the leading `origin/`
   from the second before comparing, because the two never match as printed. If the second command
   fails, ask which branch is the default. On the default branch, create a working branch with
   `git switch -c deps/upgrades`, or ask for a name if that one exists.
4. **Baseline.** When the plan says `Baseline: none (no gates)`, there is nothing to compare: every
   step runs as `unverifiable` and ends at best `committed-unverified`, and step 3 of the loop is
   skipped. Otherwise read `.upgrade/baseline/summary.md`. If its `HEAD` equals `git rev-parse HEAD`,
   it is valid. If not, re-run each gate's `Command` from that file, write the results over the
   baseline with the new `HEAD`, and compare with the old one; if any gate got worse, stop and
   report it. When the plan names a baseline file that does not exist, stop and suggest
   `upgrade-plan`.
5. **Step log.** If `.upgrade/report.md` does not exist, create it with `Start: <git rev-parse HEAD>`
   as its first line and a `## Step log` heading. If it exists, keep it: it holds the outcome of
   steps from earlier runs, which the dependency check in step 0 reads.

## The step loop

For each selected step, in plan order.

### 0. Check it can run

- Look up each step in `Depends on` in the step log (this run or an earlier one). If any did not
  end `committed`, `committed-unverified` or `no-op`, mark this one `skipped` and move on. A `no-op`
  counts as satisfied, because its target version is already in the tree.
- If `Deployment-pinned: yes`, ask the user with AskUserQuestion before touching anything: it changes
  what deploys, and the ceiling is theirs to move. Without approval, mark it `awaiting-approval`.
- Re-read the step against the current tree. An earlier step's lockfile regeneration can already
  have moved it (mark `no-op`) or changed what it needs.

### 1. Apply exactly one change

Make the hand edits the step's `Changes` lists (a `.nvmrc`, a Dockerfile tag, a constraint), then
run its `Apply` commands. [references/apply-commands.md](references/apply-commands.md) has the
per-ecosystem commands and the files that always ask for approval.

Then read `git diff --stat` and the lockfile diff. If a package that is not in this step moved a
major version, or a provider the step does not name moved, the plan has not analysed that change:
discard the step (see **When a step fails**) and mark it `needs-replanning`.

### 2. Make the code changes the upgrade forces

These belong to the step, because a commit that leaves the build broken for the next one destroys
the bisect property:

- the call sites in the step's `Breaking changes`, and any new type errors;
- configuration keys the new version renamed or removed;
- tests that depended on behaviour the migration notes say legitimately changed. The commit body says
  which test changed and quotes the note that justifies it, so a reviewer can tell an adaptation from
  a silenced regression;
- deprecation warnings the bump introduced: resolve them, or list each one with a reason in the
  commit body.

Everything the upgrade did not force (refactors, clean-ups, style) waits for its own commit.

### 3. Verify against the baseline

Run `mkdir -p .upgrade/steps/<n>` first, because a redirect into a missing directory fails with
exit 1 and reads as a failing gate. Then run each gate in the step's `Gates`, using the exact
`Command` from the baseline summary, with output to `.upgrade/steps/<n>/<gate>.log` (write the step
number literally). Pass a longer `timeout` to the
Bash tool for slow suites. Write `.upgrade/steps/<n>/summary.md` in the gate-run format, then
compare it gate by gate with the baseline:

| Result | Reading |
| --- | --- |
| Exit code no worse, failing set a subset of the baseline's, tests run not fewer | Clean. Baseline failures stay out of scope for this step |
| A new failing test, a gate that passed now failing, or fewer tests run | The step regressed. A drop in tests run counts, because a test that stopped running also stopped verifying |
| A baseline failure now passes | Clean; note it in the report |
| `tf-plan` exits 2 (changes present) | A provider upgrade wants to change live infrastructure. Keep the output, discard the step, mark it `needs-review` |

**A new failure that might be flaky.** Re-run only the newly failing tests twice. If they fail both
times, the step regressed. If they pass on either run, re-run the full gate once: clean means the
step may be committed, and the test is listed as flaky under **Unverified** in the report; a
failure means the step regressed. Test flakiness is reported, never resolved by retrying until green.

**Steps marked `unverifiable`.** Run the gates that exist (build, typecheck, lint) and compare them
the same way. A clean result makes the step `committed-unverified`, and the commit body carries the
line `Unverified: <the plan's reason>`.

### 4. Commit alone

1. Stage the step's files by name: `git add -- <manifests> <lockfiles> <changed source files>`.
2. Check `git diff --cached --stat` lists only this step's files.
3. Write the message with `dev-standards:commit-standards`, loaded with the Skill tool. If that skill
   is not installed, match the style of `git log --oneline -20`. The body carries the version
   transition, the rank reason from the plan, the code changes the upgrade forced, and any test
   change with its justification.
4. `git commit`, then append `Step <n>: <status> <git rev-parse HEAD>` to the step log in
   `.upgrade/report.md`. Every other outcome is appended the same way, with `-` for the SHA.

## When a step fails

A failed step is a result, not a reason to abandon the plan: four of five upgrades landing, with the
fifth documented, beats none.

1. **Discard the step alone.** `git restore --staged --worktree -- .` returns tracked files to the
   last commit (the tree was clean when the step started). If `git status --porcelain` still lists
   untracked files, they were created by this step; delete those. Then run the ecosystem's restore
   command from [references/apply-commands.md](references/apply-commands.md) so installed packages
   match the lockfile again.
2. **Confirm the restore.** Re-run the step's gates and compare with the baseline. If they are not
   clean, stop the whole run: the tree is in a state nobody planned.
3. **Record the cause concretely:** the failing tests or the resolver error, verbatim, and the likely
   reason. "Step 4 failed" gives nobody anything to act on; "Step 4 (`acme-client` 4→5): 11 tests in
   `test/cache.spec.ts` fail with `TypeError: invalid options`; the 5.0 migration guide moves
   connection options out of the constructor" does.
4. **Continue.** Steps that do not depend on the failed one run as planned; steps that do are
   `skipped`.

A step passes honestly or fails. Force flags, `--legacy-peer-deps`, deleted or skipped tests, and
disabled gates are all ways of failing that look like passing; `dev-standards:zero-tolerance-testing`,
when installed, lists the rest.

A problem traced to an already-committed step `k` is undone by reverting, newest first, every
committed step that depends on `k` directly or through another step, and then `k` itself: a
dependent left in place would sit on top of a change it needs. Run `git revert --no-edit <sha>` for
each, followed by the restore command, and record each as `reverted` in the step log. If a revert
stops on a conflict (two steps regenerated neighbouring lockfile lines, for example), run
`git revert --abort`, confirm `git status --porcelain` is empty, and stop the run: resolving a
lockfile conflict by hand is the hand-edited lockfile the plan rules out.

## Stop the run

Stop, report what has landed so far, and return to the user when:

- the plan is malformed or its `Decision` does not allow execution;
- the tree is dirty at start, or the baseline cannot be established;
- a re-run baseline is worse than the recorded one;
- a discarded step did not restore the baseline;
- a revert stopped on a conflict.

Everything else is a per-step outcome and the run continues.

## Verify and report

After the last step, run `mkdir -p .upgrade/steps/final`, re-run every baseline gate on the final
`HEAD` into it (`Run: final`), and compare with the baseline. Then check that
`git log --oneline <start>..HEAD` shows one commit per step marked `committed` or
`committed-unverified` in the step log, plus one `Revert "…"` commit per `reverted` step, and that
`git status --porcelain` is empty.
A final regression when every step was clean on its own means two steps interact; report it with
the failing tests, and leave the commits in place for the user to bisect rather than reverting them.

Write the report to `.upgrade/report.md` below the step log, replacing any report an earlier run
left there, and show it to the user:

```markdown
# Upgrade report
Branch: <name> · Commits: <n> · Final gates vs baseline: clean | regressed (<gates>)

## Moved
| Step | Change | Commit | Code changes forced | Verification |
| --- | --- | --- | --- | --- |

## Did not move
| Step | Status | Reason | Cause | What would unblock it |
| --- | --- | --- | --- | --- |

## Unverified
<Every committed-unverified step and its reason; flaky tests seen; anything checked only by a build.>

## Needs a human
<Deployment pins awaiting approval, terraform plan output awaiting a read, deferred deprecations,
and the push: nothing has been pushed.>
```

Step statuses form a closed set: `committed`, `committed-unverified`, `failed`, `skipped`, `no-op`,
`awaiting-approval`, `needs-replanning`, `needs-review`, `reverted`, `not-planned`. `Reason` is `—`
for plan steps. Also list the plan's `Not in this plan` rows under **Did not move**, with their
research ID in the Step column, `not-planned` as the status and the plan's reason in `Reason`, so the
report accounts for every row.

`.upgrade/` stays on disk for the reviewer; tell the user it is safe to delete once the branch is
merged.

## Without a checkout

This skill needs Claude Code with the repository checked out, because it edits files, runs the
suite and commits. On a surface without a shell, say so, and offer the plan's steps as a checklist
the user can carry out by hand.
