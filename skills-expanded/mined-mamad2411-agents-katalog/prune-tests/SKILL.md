---
name: prune-tests
description: "Prune a repo's test suite and speed up its test run, cutting only tests that catch no bug another test catches, proved with planted bugs and replayed past fixes. Use when asked to clean up, dedupe or trim tests, cut useless or redundant tests, or make tests or CI faster."
---

# prune-tests

The rule (fewer-tests, Keith 2026-10-16): a test stays only if it catches a plausible bug no other
test catches. This skill makes that rule a measurement. A **mutant** is a planted bug: one small edit
to the code (`<` to `<=`, `+` to `-`, a constant plus one, `return x` to `return None`). A test
**kills** a mutant when it goes red on it. The **kill matrix** records which tests kill which mutants.
A test whose kills are all shared with other tests adds run time and no protection.

"CI" on Keith's boxes means the test runs before each commit; there is no CI server.
Speed and count are two targets: the minutes usually sit in a few **heavy** tests, so measure first.

## Setup

- `PY` = the repo's own venv interpreter (full path). It needs pytest 8.2+ (argument files) and
  coverage. Run every script with it: `$PY $SK/scripts/<script>.py`, with `SK=~/.claude/skills/prune-tests`.
- `RUN` = a run folder in the session scratchpad; every JSON and the report land there.
- The scripts rewrite source files while they work, so they only run in scratch worktrees:
  `git -C <repo> worktree add --detach $WT/base/<repo-folder-name> HEAD`. Keep the repo's folder
  name: a repo root holding `__init__.py` imports its tests through that name.
- Put the ignored files the tests read into the worktree
  (`git ls-files --others --ignored --exclude-standard`): hardlink secrets (`.env`, creds) so no
  second copy lands on disk, and copy the rest, since a planted bug can write through a hardlink.
  Extra workers get the same: a hardlink where the worktree has one, else a copy.

## Stages

Each stage ends on its done-when line. Write findings to `$RUN/notes.md` as you go.

**0. Read.** Find what runs the tests (pytest.ini, pyproject, conftest, hooks, the repo's CLAUDE.md
test rules). Check for a **freeze**: code that hashes files into a ledger (td3c, brent-structure and
wb-forecast do; grep `hashlib` near ledger, freeze or lock). If test files are inside the hash,
stop and tell the user: cutting them voids the track. Name the **exempt** globs: guards born from
incidents (no-typed-numbers, call style, desk-check guards), contract tests against outside data,
and tests that read source files as text. Planted bugs do not model what these protect.
Done when: runner, freeze status and exempt globs are in notes.md.

**1. Profile.** `prune.py profile --repo $BASE --python $PY --out $RUN/profile-before.json --runs 1`.
Done when you can say where the minutes go: collection, a few heavy tests, or the long tail.
Tests that fail before any change are excluded from every later stage; list them in notes.md.

**2. Map and candidates.**
`prune.py map --repo $BASE --python $PY --out $RUN/map.json` runs the suite under coverage with
one context per test (the bundled `prune_plugin.py`), giving each test's line set.
`prune.py subsets --map $RUN/map.json --profile $RUN/profile-before.json --exempt <globs> --out $RUN/candidates.json`
flags each **candidate**: a test whose lines all sit inside another test's lines.
Every other test is a **keeper**. Done when candidates.json exists and you have read its
`no_coverage` list (tests that ran no repo line: guards that read source, constant pins).

**3. Kill matrix.**
`mutate.py kill --repo $BASE --python $PY --map $RUN/map.json --candidates $RUN/candidates.json --profile $RUN/profile-before.json --out $RUN/kills.json --workers N`.
It plants mutants on lines the candidates run. Per mutant it runs the covering candidates in full,
then, if one killed it, the covering keepers fastest-first and stopping at the first red.
It first breaks a target file outright and refuses to go on if the covering tests stay green (a
blind run). Pick N near a third of the cores for a suite with heavy tests, and run it in the
background. Each result is saved as it finishes, so rerunning the same command resumes a crashed
run. Tests that fail before any change are left out of every pass. Then:
`prune.py plan --kills $RUN/kills.json --candidates $RUN/candidates.json --profile $RUN/profile-before.json --map $RUN/map.json --out $RUN/plan.json`.

When heavy candidates (page renders, seconds each) sit on many lines, one pass can run for days:
size it first by summing each mutant's covering-candidate seconds. Then run two passes. `prune.py
split --seconds 2` writes the light and heavy candidate files and a skip list for each.
Pass 1 scores the light candidates with `--skip skip-heavy.txt`. Pass 2 scores the heavy ones
with `--skip plan-light.json` after pass 1, or with `--skip skip-light.txt` alongside it, in its
own base worktree. Either way no cut leans on a test the other pass may cut. A test whose only
twin sits in the other pass stays, the safe direction. `--max-mutants` may sample pass 2; the report then
says those cuts rest on a sample. `prune.py merge --plans plan-light.json plan-heavy.json --out
plan.json` joins them, and verify takes both kills and plans in the same order.
A greedy **set cover** keeps the fewest candidates that still kill every mutant only candidates
kill (fastest test wins a tie); the rest form the cut ledger, each row naming the tests that now
catch its bugs. Done when plan.json exists.

**4. Judge the ledger.** Read the body of every cut test and every no-coverage test.
- Keep a cut test that guards what mutants cannot plant: string keys that feed a join, an
  exception contract, a file format read outside the repo. Note why in notes.md.
- Cut, even with a unique kill: tests that pin a constant, a message or a format, and tests of a
  one-off script whose run is done (the script stays).
- No-coverage tests: a guard joins the exempt list; a pin is cut; anything else stays.
Done when every ledger and no-coverage row has a decision in notes.md.

**5. Cut.** In a second worktree at the base commit (`git worktree add --detach $SLIM <base sha>`),
delete the cut tests, and fold near-duplicates (same body, different values) into one
`parametrize` table. Touch tests only; source must stay byte-identical or verify refuses. Give a
change its own small run, unless the commit hook already picks tests by what the change imports
(code-health's `venv-run --tests` does): mark heavy tests (`@pytest.mark.heavy`, registered in the
pytest config) so a per-change run can pass `-m "not heavy"`, or write a `-k` map in the repo's
test docs. The default run keeps every test: a heavy test that alone
catches its bugs is still protection, and the stopwatch must compare like with like. Remove
fixtures and helpers the cut left unused. Commit on the detached HEAD: stage 6 runs on that
commit. Done when the slim suite passes, minus the stage 1 failures.

**6. Prove it.** Three checks, none of them your own judgement:
- Planted bugs: `mutate.py verify --repo $SLIM --python $PY --kills $RUN/kills.json --plan $RUN/plan.json --out $RUN/verify.json`
  re-plants every bug a cut test killed and runs the tests the plan says now catch it (`--workers`
  as in stage 3). Lost must be 0; each lost bug means restore its cut test.
- Past bugs: `replay.py --base $BASE --slim $SLIM --python $PY --map $RUN/map.json --plan $RUN/plan.json --profile-before $RUN/profile-before.json --profile-after $RUN/profile-after.json --out $RUN/replay.json`
  takes up to 20 recent `fix:` commits, reverse-applies each fix's source diff onto today's code
  in both worktrees, and runs the cut tests and the slim tests that cover the rewritten lines.
  A row reads **lost** when only a cut test went red; restore that test.
- Stopwatch: on a quiet machine, `profile --runs 3` on base then on slim
  (`profile-before.json`, `profile-after.json`), and the same for one typical per-change selection
  (`change-before.json`, `change-after.json`, pytest args after `--`).
Then `prune.py report --dir $RUN --out $RUN/report.html`, open it, and copy it next to the repo's
other reports if it has a docs folder. Now name the branch, on a fresh commit of the slim tree whose
message carries the numbers: tests before and after, full-run and per-change medians, both lost
counts. `git -C $SLIM branch chore/prune-tests $(git -C $SLIM commit-tree HEAD^{tree} -p <base sha> -F msg.txt)`.
Done when lost is 0 on both bug checks, all four timing files exist, and the branch carries the numbers.

## Grading a cut that already landed

When tests were already cut by hand or by another session, grade that cut before cutting more.
Run stages 1 and 2 on the commit before it (`$BASE`), put the cut commit in `$SLIM`, then
`prune.py grade --map $RUN/map.json --profile $RUN/profile-before.json --slim $SLIM --python $PY --out-dir $RUN`.
It lists the removed tests and the **orphaned** lines, source lines that only removed tests ran.
`mutate.py kill` with `--map map-orphan.json --candidates candidates-removed.json` plants bugs on
those lines: no remaining test runs them, so every catch is a catch the cut lost. That count is
a floor: a removed test can also be the only one that checks a line others merely run, which a
kill run over the removed tests' full lines finds. `replay.py
--plan removed.json` replays fix commits across the cut. Restore, on a branch, each removed test
that alone catches a planted bug or a replayed fix. Judge each restore as in stage 4, so a pin stays
cut, and pick the set by run time: a unit test beats a page render that catches the same bug.

## Handover

Chat: tests before and after, full-run minutes before and after, per-change minutes, and the two
lost counts. Everything else is in the report. Remove the scratch worktrees
(`git worktree remove --force`) once the branch is committed.

## Gotchas

- Session-scoped fixture setup is credited to the first test that triggers it, so that test looks
  broader than it is. Coverage only flags candidates; the kill matrix decides.
- Lines run at import (module constants) belong to no test, so no mutant lands there.
- Each parametrized case is its own node id; cutting one case means editing its parameter list.
- The runner sets `PYTHONDONTWRITEBYTECODE` and deletes the mutated file's `.pyc`: a mutant of the
  same size, written in the same second, can otherwise run from stale bytecode.
- A busy box times batches out, not just bugs: after a timeout each unfinished test re-runs alone,
  and only one that fails or hangs alone counts. Keep all workers, across every session, under the
  core count, or those re-runs eat the pass.
- A keeper run that hits `--budget` counts as no keeper kill, so its candidates stay. The report
  counts these; raise the budget if they are many.
- mutmut and cosmic-ray record one killed-or-survived result per mutant, and mutmut needs `os.fork`
  (WSL on Windows). The kill matrix needs every killing test, hence the bundled runner.
