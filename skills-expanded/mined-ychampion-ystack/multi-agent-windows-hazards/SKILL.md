---
name: multi-agent-windows-hazards
description: >-
  Hazards of running many parallel coding agents (codex exec, Claude subagents) on one Windows machine
  with git worktrees, a self-hosted CI runner and a merge train. Use when agents' commands start dying
  with 0xC0000142 / -1073741502, codex exec fails with "code-mode host exited during handshake", a
  `git stash pop` brings in another agent's files, a push to a PR branch starts no CI run, a CI job
  fails with no failing step and no logs, a hash guard fails right after a merge that conflicted
  `.gitattributes`, pytest says "could not create numbered dir ... after 10 tries", a SQLite file hash
  changes when nothing wrote to it, worktree removal fails with "Filename too long" or "Device or
  resource busy", or a "keep both sides" CSS merge silently breaks styles.
---

# Multi-agent hazards on a Windows host

Each entry: the symptom you see, the real cause, and what to do. They were found running a dozen or so
concurrent agents on one Windows box, each in its own git worktree of one repo, with CI on a
self-hosted Linux runner and PRs landed one after another. Several apply on any OS.

## Process and agent failures

### 1. Process-spawn exhaustion: `0xC0000142` / `-1073741502` (STATUS_DLL_INIT_FAILED)

**Trigger:** roughly 10+ concurrent agent process trees (codex exec plus pytest plus node or vitest
workers). Every new process in the affected sessions fails at start-up, including `git --version` and
PowerShell itself.
**Shape:** intermittent and per session. The orchestrator's own shell can keep working while
agent-spawned shells die; later even fresh agent sessions die.
**Why:** desktop-heap / session resource exhaustion. It clears partly as agents drain and fully only on
reboot.
**Do:**
- Cap concurrency (about 3 heavy test gates at once).
- If one harness's agents start dying, move the work to agents that run inside the orchestrator's
  harness process.
- Tell agents: "if commands die with 0xC0000142 twice, stop and report what stands". Their edits on
  disk survive, so the orchestrator can commit and push them.
- Reboot before the next heavy wave.

**Don't:** relaunch the same agent into the wall repeatedly, or blanket-kill `node.exe`: other projects
run there.

### 2. `codex exec`: "code-mode host exited during handshake"

**Trigger:** after an exhaustion event like #1, new `codex exec` sessions fail every tool call with this
message while older surviving sessions keep working.
**Bypass:** `codex exec -c features.code_mode_host=false ...` restored shell execution in the codex
version where this was seen (check `codex features list` for the flag name in yours).
**Cost:** that path had a per-command ceiling of about 300 s, so a full test suite can't run inside one
command. Run it detached (PowerShell `Start-Process -RedirectStandardOutput`, then poll the file), or
let CI be the gate.
**Also:** `codex exec` with a prompt argument can block on "Reading additional input from stdin..." when
stdin is an open pipe. Launch it with `< /dev/null`.

### 3. `pgrep -f` / `pkill -f` over ssh kills your own ssh session

`ssh host 'OLD=$(pgrep -f "codex exec"); ...; kill $OLD'` also matches the remote `bash -c` whose
command line contains the pattern. The kill takes down the ssh shell mid-sequence (exit 255, no
output), and everything after it, such as the relaunch, never runs.
**Do:** match the binary path with a self-excluding pattern, for example
`ps -eo pid,args | awk '/[/]usr[/]bin[/]codex exec/ {print $1}'`, or use `pgrep -x`, and check by PID
before and after. Never `pkill -f` a phrase that appears in your own command.

### 4. Orphaned dev-server grandchildren block worktree removal

**Symptom:** `git worktree remove --force` fails with "Filename too long" and `rm -rf` with "Device or
resource busy". Neither names the cause.
**Why:** killing a backgrounded `pnpm start` (or `bun run start`) wrapper does not kill the `next start`
(or similar) grandchild, which keeps an open handle on the app folder. Orphans also leak memory across
parallel lanes.
**Fix:** kill by path before removing:

```powershell
Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
  Where-Object { $_.CommandLine -like "*<worktree path>*" } |
  ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
```

## Git worktrees

### 5. `refs/stash` is shared across all worktrees of one repo

Stashes live in the repo's common directory, not per worktree.
**Incident shape:** agent A runs `git stash push`, then a 150 s test, then `git stash pop`, and pops
agent B's stash (pushed in the meantime) into A's worktree: foreign files, in conflict.
**Rule:** never `git stash` in worktrees of a shared repo. Commit to the branch, or copy files to a
scratch folder. If you must, note `git rev-parse stash@{0}` and restore by SHA
(`git checkout <sha> -- <paths>`), never by position.

### 6. Shuttling files between worktrees: `git checkout` reverts the wrong copy

A test that finds the repo root from its own location (`Path(__file__).resolve().parents[2]`) only
ever scans the tree it lives in. Copying edits from worktree B into worktree A to run it there, then
running `git checkout <files>` to clean up while the shell is still in B, reverts your own uncommitted
edits in B instead of the copies in A. `cp` takes explicit paths; `git checkout` silently takes the
current directory, and nothing errors.
**Do:** don't shuttle. Run the test inside the worktree that has the edits (for Python, `uv run pytest`
there builds that worktree its own `.venv`; delete it afterwards if disk is tight). To clean another
tree, address it explicitly: `git -C <path> checkout -- <files>`. With two worktrees of one repo open,
use `git -C` for every mutating git call.
**Generalises:** any root-relative tooling (coverage config, ruff or mypy config discovery, fixture
paths) reads the tree it is launched from, not the one you edited.

### 7. Junctioned `node_modules` in a source-only worktree: remove the junction first

**Trick:** a source-only worktree can borrow the main checkout's `node_modules` through a directory
junction (`mklink /J`) instead of a full install (with pnpm on Windows each worktree's `node_modules`
can be a real copy of several hundred MB, not hard links). vitest, tsc and eslint run normally.
**Trap:** some delete paths follow the junction and wipe the main checkout's real `node_modules`, which
every other lane is borrowing. Remove the junction itself first: `rmdir <worktree>\...\node_modules`
in cmd, or `Remove-Item` on the junction without `-Recurse`. Check the target still exists, then remove
the worktree.

## Merges

### 8. A conflicted `.gitattributes` silently de-normalises files during that same merge

**Symptom, pointing the wrong way:** after resolving a merge, a content-hash guard fails as if vendored
data were corrupt (for example "dataset X hashes to 45f3..., but its manifest records aa6f...").
**Real cause:** while `.gitattributes` held conflict markers, git could not parse it, and said so in one
easily missed line during the merge (`... is not a valid attribute name: .gitattributes:17`). With the
file unparseable, its `-text` rule was not in force for that checkout, so `core.autocrlf` converted a
fixture whose bytes are attested, and its sha256 changed.
**Diagnose** by comparing the committed blob with the working tree:

```bash
git show origin/main:path/to/fixture.csv | sha256sum   # authoritative
sha256sum path/to/fixture.csv                          # what you have
```

Different only by line endings means the repo is fine and only your checkout is wrong.
**Fix:** resolve `.gitattributes` first, then re-checkout every path it governs:
`rm -rf <fixture dir> && git checkout -- <fixture dir>`.
**Generalises:** any merge that conflicts `.gitattributes` leaves every attribute-dependent file
mis-materialised until re-checkout. On Linux CI with `autocrlf=false` nothing is wrong, so it
reproduces only on Windows. Don't "fix" the manifest.

### 9. "Keep both sides" on a CSS tail conflict can splice rule bodies

Two lanes appended blocks to one stylesheet whose selectors differed but whose property bodies were
byte-identical. Git's line merge aligned the identical bodies across the blocks, so a mechanical
keep-ours-then-theirs left one selector carrying the other block's properties: no conflict marker, no
lint error, no failing test.
**Rule:** resolve append-only CSS conflicts at **block** level. Take each lane's whole delimited span
(`/* LANE X */ ... /* END LANE X */`) verbatim from its own branch (`git show <branch>:path/to/file.css`),
never line by line from the marker regions. Then run any file-wide checks on the assembled file: each
lane passes alone, and it's the merged file that fails.

### 10. Append-only CSS: an unconditional rule at the end shadows the base media rules

A lane appended `.surface { padding-bottom: 1rem }` for phones at the end of the stylesheet. Being last
and unconditional, it beat the base's `@media (min-width: 768px)` value at every width, so desktop
regressed silently.
**Rule:** in an appended block, every rule on a selector that exists elsewhere in the file is written as
the phone value plus a paired `@media (min-width: ...)` restore for each breakpoint the base uses.
Review sweep: each top-level selector in the block is either unique to the block or restored in the
block's own media queries. This can be made a lint check at integration time.

## CI on a self-hosted runner

### 11. Pushes to a PR branch sometimes start no CI run

**Shape:** some pushes to open-PR branches produce no `pull_request` run at all. Check within about 10
minutes of a push.
**Fallback:** add `workflow_dispatch` to the workflow and start it by hand:
`gh workflow run "<workflow name>" --ref <branch>`.
**Related:** a single self-hosted runner serialises everything, and `concurrency: cancel-in-progress`
per ref means each push cancels that branch's older run. "Cancelled" is usually churn, not failure.

### 12. Never restart the runner while a job is in progress: check jobs, not runs

`gh run list` can show a run as `queued` while one of its jobs is already `in_progress` (run status
lags; jobs queue independently). Restarting the runner (`systemctl restart actions.runner...`) on the
strength of "no run in progress" kills the job, which then shows as a job-level failure with **no
failing step** and "log not found". It looks like a mysterious infrastructure fault.
**Before any restart:**

```bash
gh api repos/<owner>/<repo>/actions/runs/<id>/jobs --jq '.jobs[] | {name, status}'   # every non-completed run
gh api repos/<owner>/<repo>/actions/runners --jq '.runners[] | {name, busy}'          # want busy:false
```

**Recovery** for a job you killed: wait for the run to finish, then `gh run rerun <id> --failed`. A
runner service left `failed` after an OOM kill still needs the restart; wait for idle first.

### 13. Memory-bounded test runs on a shared host

Coverage-instrumented pytest over a large suite (about 1,900 tests) in one process was OOM-killed (exit
137) on a host whose other workloads held most of the RAM, even after swap filled.
**Fix:** split the test files into sequential pytest processes with `--cov-append` (start with
`coverage erase`). Each slice exits and frees its memory; the combined coverage is the same.

### 14. `ENOSPC` on the CI host masquerades as a pytest fixture bug

**Symptom:** `OSError: could not create numbered dir with prefix <name> in /tmp/pytest-of-<user>/... after
10 tries`, with a cascade of errors at fixture setup.
**Why it misleads:** pytest's `make_numbered_dir` retries `mkdir` ten times inside a bare
`except Exception: pass`, so the real errno is swallowed. It reads like a tmpdir defect; it is a full
disk.
**Check:** `df -h /; df -i /` on the host (rule out inodes too).
**Before pruning:** `docker system df`. If build cache is already 0 B, the usual `docker builder prune`
won't help, and on a shared box the rest usually belongs to other tenants. Reclaim only regenerable
artifacts you own (`.venv`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, runner `_diag` logs, stale
`/tmp/pytest-of-*`). Never delete another tenant's data for headroom; report the disk as the blocker.
**Related:** heavy local verification on that same host (a big `pnpm install`) while CI runs can cause
this in someone else's job. On Windows, ENOSPC can also surface as a generic build failure with no
mention of disk: check free space before debugging a sudden build break, and re-check at the moment of
any decision, because agent transcripts and caches grow fast.

### 15. A CI job that runs within a minute of its timeout

If a job's durations across lanes cluster just under `timeout-minutes` (for example 39 to 44 minutes
against 45) and the slowest run carried no extra slow test, the spread is host contention. Any lane can
then go red on a spurious timeout that looks like its own fault. Before blaming a diff, compare the
job's duration with its siblings:

```bash
gh api repos/<owner>/<repo>/actions/runs/<id>/jobs \
  --jq '.jobs[] | select(.name=="<job>") | "\(.started_at) -> \(.completed_at)"'
```

The fix is to raise `timeout-minutes`, not to delete tests, but don't edit shared CI config in the
middle of a merge train: it invalidates every queued run.

## Flaky tests

### 16. Hashing a SQLite file across a WAL checkpoint is a timing test, not a mutation test

**Symptom:** a test asserting `sha256(db_file)` is unchanged across an operation that writes nothing
fails intermittently (CI only, or 1 run in N) with two different digests.
**Why:** in `PRAGMA journal_mode = WAL`, SQLite rewrites the main file whenever it checkpoints:
automatically past `wal_autocheckpoint` (1000 pages by default) and when the last connection closes.
Read-only connections that aren't closed explicitly close at garbage collection (for example on
`asyncio.to_thread` workers), so a *read* can rewrite the file inside the test's before/after window.
**Diagnose:** insert `PRAGMA wal_checkpoint(PASSIVE)` between the two digests. If the verdict flips while
the operation still wrote nothing, the assertion measures checkpoint timing.
**Fix:** hash at a canonical boundary (open a connection, `PRAGMA wal_checkpoint(TRUNCATE)`, close, then
hash), or compare rows instead of bytes.

## A working loop

What held up through all of the above:

1. Agents edit. If their shells are dead, the orchestrator commits and pushes their edits verbatim.
2. CI verifies on Linux.
3. An independent reviewer agent posts a verdict.
4. PRs merge in landing order, each only on a green main.

Keep one authoritative board file (per-PR state, landing order, follow-ups) and update it on every
event. Prefer report files to completion notifications: wrapper shells get reaped while the processes
they started survive.
