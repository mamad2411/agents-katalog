---
name: landing
description: "Let many agents write to one repository at once without collisions: a per-repository landing contract, path leases claimed before work starts, one queue that is the only writer to trunk, and a machine-wide slot governor for builds and tests. Use for 'landing', 'land this', 'merge queue', 'many agents on one repo', 'where does this work land', or before any coordinator (brigade, Orchestrate, Autopilot, swarm) delegates writing work in parallel."
---

# Landing

Writing scales. Integration does not. Landing makes integration a property of the repository, decided once, so no coordinator asks where work lands and no two writers collide.

The rules:

1. One trunk per repository. Every change lands there through the queue.
2. A writer claims a lease on the paths it will change before it starts. Overlapping claims are refused.
3. Writers never integrate. A worker commits in its own worktree and stops. It never merges, rebases a shared branch, or pushes trunk.
4. The queue is the only writer to trunk. It is a lock, not a process. Whoever runs `land` while the lock is free drains the queue. Everyone else gets "queue busy".
5. A review verdict holds only for the exact change reviewed. The queue lands the pinned SHA, and bounces it when the rebased change differs from the reviewed one.
6. Builds and tests run under a governor slot, so the machine is not overrun.

## The script

`<skills>/landing/scripts/land.py`, where `<skills>` is the directory holding this skill. Run it from any checkout of the repository, or pass `--repo <path>`. State lives in SQLite under `${XDG_STATE_HOME:-~/.local/state}/pstack-t3/landing/`, one store per repository.

```bash
L="python3 <skills>/landing/scripts/land.py --repo <checkout>"
$L init --trunk main --mode human|merge|push|local --check "<cmd>" [--check ...] [--setup "npm ci"] [--batch 4] [--timeout 1800] [--merge-method merge|squash|rebase] [--author-policy any|configured|credited] [--pr-item-line on|off] [--heartbeat-ms 3600000] [--merge-heartbeat-ms 900000] [--base <commit>] [--cap 4] [--generated <paths>] [--rebuild "<cmd>"]
$L mode merge [--merge-method squash]   # change the mode while the queue is empty. --merge-method may change while entries await merge
$L cap 4                     # most changes in flight on the repository at once; 0 clears it
$L lease claim --holder <restaurant>/<dish> --paths src/engine,package.json [--owner <restaurant>/@<generation>]   # prints L<n>, who holds the overlap, or the cap and its holders
$L lease check --holder <restaurant>/<dish> --paths src/engine   # what a claim would answer now, with no lease claimed and no reservation armed: free, the overlapping leases, or the cap
$L lease renew L3 [--if-live] [--owner ...] ; $L lease release L3 [--owner ...] ; $L lease list
$L submit --holder <restaurant>/<dish> --branch <b> --sha <reviewed sha> --lease L3 --reviewer <provider/model> [--owner ...] [--title "..." --body-file pr.md]   # prints E<n>
$L owner --prefix <restaurant>/ --generation 2   # raise a holder prefix's floor; it never lowers
$L lease reserve --for <restaurant>/ --paths a.md,docs --ruling R<n> [--ttl-hours 2] --owner .admin/@<generation>   # prints S<n>; refuses other holders' claims on those paths
$L lease unreserve S<n> --owner .admin/@<generation>   # lift a reservation
$L share --for <restaurant>/ <n> [--clear] --owner .admin/@<generation>   # that prefix's share of the cap; --clear takes 0
$L contest --holders <a>,<b> --owner <restaurant>/@<generation>   # prints C<n>; land holds both holders' entries
$L contest --settle C<n> --first <holder> --owner .admin/@<generation>   # the first holder lands, then the other
$L contest --cancel C<n> --owner .admin/@<generation>   # remove the hold or the order
$L land                      # drain the queue; prints what landed, bounced, or is still queued
$L status [E3] ; $L resume
$L status --holder <restaurant>/<dish>   # that holder's entries with their SHAs; a value ending in / matches every holder under it
$L status --holder <restaurant>/<dish> --sha <sha>   # only its entries at exactly that commit
$L status --holder <restaurant>/<dish> --json   # the same entries as JSON objects, one per entry
$L slot -- npm test          # run a heavy command under a governor slot
$L slot --exclusive -- npm run bench   # hold every slot: nothing else heavy runs while it measures
$L slot --slots 2 -- npm test   # take 2 worker slots in one admission
```

Every command takes `--help`.

A coordinator replaced by another thread must not write again. `owner --prefix docs/ --generation 2` raises the floor for holders under `docs/` and never lowers it, so a rerun changes nothing and a lower generation exits 1. `lease claim`, `lease renew`, `lease release`, and `submit` take `--owner <prefix>@<generation>`, whose prefix the holder must start with. Inside the write's transaction each refuses a generation below the prefix's floor with `land: owner docs/@1 is stale; docs/ is at generation 2`, and refuses a holder under a floored prefix that passes no `--owner`. A prefix with no floor works without `--owner`. brigade's `set --thread --replace` raises its restaurant's floor before it records the new thread.

## Rulings

The executive admin carries out its rulings from [rulings.md](reference/rulings.md).

## Set up a repository once

Run `init` the first time any coordinator writes to a repository. The mode decides whether the user stays a gate on landing, so it is the user's choice. brigade asks it when a restaurant opens. Any other coordinator asks once per repository with the host's question tool, unless the user already said.

The stored-contract rules live in [contract.md](reference/contract.md).

| Mode | Landing does | The user |
| --- | --- | --- |
| `merge` | Opens a PR and merges it, per [Pull request lifecycle](pauses.md#pull-request-lifecycle). | Reviews after the fact. Nothing waits on them. |
| `human` | Opens a PR and keeps it open for the user to merge, per [Pull request lifecycle](pauses.md#pull-request-lifecycle). | Merges every PR. |
| `push` | Rebases, runs the checks, and pushes trunk only if the remote is still at the tested base. No PRs. | Reviews after the fact, in the commit history. |
| `local` | Lands on `refs/landing/<trunk>`, which no checkout uses. Pass `--base`. | Merges the lane into a branch when ready. |

`merge` and `push` let reviewed changes reach trunk with no human gate. When the PR needs an approving review, or when it has changes requested, the queue pauses and names the PR and that requirement. It does not run `gh pr merge --auto`. The user then either relaxes the rule for the queue or switches to `human`.

Checks are the repository's own test, type check, and lint gates. In `push` and `local` mode there is no pull request or CI behind the queue, so the checks are the only gate. `land.py init` and `land.py status` print a warning while those modes have none. The warning is advice only and never changes an exit code. `--setup` installs dependencies, because the queue's worktree is cleaned with `git clean -ffdx` before every attempt. `land.py mode` switches between `merge`, `human`, and `push` once nothing is queued, landing, or awaiting merge. `land.py mode --merge-method` changes the method the next `gh pr merge` uses, and it may run while entries are queued, landing, or awaiting merge. Changing trunk or remote, or moving to or from `local`, needs a new contract.

## Run writers through it

[The runtime's Modes section](../pstack-runtime/SKILL.md#modes) sets the mode lines of every brief this skill writes and how its spawns run in light mode.

For every unit of writing work:

1. **Claim.** `lease claim` the files and directories the unit will change, before delegating. When the claim is refused, fold the unit into the holder's work or hold it until that lease is released. A cap refusal names every holder in flight. Hold the unit until one of them releases. Never claim `.` unless the unit really touches everything. `lease renew` extends a live lease. Renewing an expired lease is a new claim on its paths. It is refused when another holder's lease now overlaps or the cap is full, and the refusal names which. `--if-live` refuses an expired lease instead, so admitting it again is always a separate step taken after the old worker stopped.
2. **Brief.** A writer is a worktree thread from `t3_thread_launch` when it runs long or the user should see it, and a `delegate_task` child otherwise. Isolate a delegated writer per [the runtime's Isolation section](../pstack-runtime/SKILL.md#isolation). Use the required landing base, which can differ from the parent's current commit. Tell the worker to work only in its own worktree branched from `<remote>/<trunk>` (or `refs/landing/<trunk>` in local mode), change only the leased paths, keep history linear with no merge commits, run builds and tests through `land.py slot --` and every benchmark or timing measurement through `land.py slot --exclusive --`, commit, and report the branch and head SHA. Put rule 3 in the brief unchanged.
3. **Review** the exact SHA with a verifier from another model family, or a same-family seat when only the author's family has a runnable seat, per the coordinator's own review step.
4. **Submit** that SHA with the lease and the reviewer. In `merge` and `human` mode, pass `--title` and `--body-file` so the PR says what changed and how it was verified. The queue sends the submitted title unchanged. It sends the body unchanged unless the contract sets prItemLine to on, which adds the item's Kind and Goal line when it has one. The line follows body text after one blank line or is the whole body when the body holds only whitespace. With no `--body-file`, the body is the reviewed commit's body. The reviewer stays in the queue's local store. A submit that changes paths outside the lease is refused. Widen the lease or split the change.
5. **Land.** Run `land`. When it prints `queue busy`, run `land` again, at most 3 more times, waiting 5 seconds before each try.
6. **Settle.** Read `status E<n>`.
   - `landed`: the lease is released. Record it in the coordinator's tables, then remove the worker's worktree with `git worktree remove` and delete its branch.
   - `bounced`: the lease is active again for the fix. Resubmitting prints a new entry id. Call `unwatch_pull_request` on the bounced PR. Fire a fresh worker with the original brief, the bounce reason, and trunk. For a size bounce, read [File size limit](size-limit.md). A conflict or a changed rebase needs a new review after the fix. A reason that reads `commit <sha12> has author <name> <<email>>, not the configured <name> <<email>>; recommit it as the configured author` says the entry has a foreign commit author. The contract's `authorPolicy` decides this check. `any` never bounces on authorship. `configured` and `credited` compare each commit between the entry's base and its reviewed commit with `git config user.name` and `git config user.email`, and they run only when both have a value. `configured` bounces an entry with a reviewed commit whose author is not that identity. `credited` bounces it too unless every such commit carries a `Co-authored-by` trailer equal to its author as `name <email>` and the body has a line that reads `Based on #<n> by @<login>` with an optional trailing period. The body is the `--body-file` text, or the reviewed commit message body when that text is empty or absent.
   - `awaiting-merge` (`merge` and `human` mode): the PR is open. [Pull request lifecycle](pauses.md#pull-request-lifecycle) says what the next `land` does with it.

## Keep the queue moving

While any entry you submitted is `queued` or `awaiting-merge`, keep the queue moving. Drains from other coordinators on the same repository are harmless, because the queue lock runs one at a time. `land` prints every holder's entries. Act only on lines whose holder is this coordinator's own, and call `watch_pull_request` only on those PRs. A sibling's PR is the sibling's to watch. When a sibling's `land` opens your PR, read its URL from your own `status --holder <restaurant>/<dish>`, which brigade's `watch` prints as `awaiting merge <pr url>`.

In `merge` and `human` mode, once `land` has opened a PR, this thread calls `watch_pull_request` on that PR per [Pull request watching](../pstack-runtime/SKILL.md#pull-request-watching). This thread owns the PR. A worker child cannot watch. On each wake, run `land` and act on what it prints. When that wake's `land` prints `queue busy`, retry as step 5 of [Run writers through it](#run-writers-through-it) says before ending the turn. The passed-checks wake is spent, so this thread would otherwise notice the merge only from the hourly heartbeat. In `merge` mode `land` merges PRs in the order of [the line](pauses.md#the-line). An entry whose `status E<n>` shows `waiting for E<m> to merge first` needs nothing from this thread. When `land` prints `rebuilt E<n> (<holder>) <url>` for your entry, keep the watch, because `land` pushed a new candidate to the same PR. Never merge a queue PR by hand in `merge` mode, and never turn on auto-merge for one, because a later PR of the line holds the commits of the entries ahead of it. Keep the watch while the entry is queued or awaiting merge. An interim status reply keeps the watch. Call `unwatch_pull_request` only when this thread stops driving that PR or hands the queue back to the user. Driving stops when that PR closes, when the queue bounces its entry, or when this thread stops owning the queue. A bounce of an unmerged PR tries to close it when it is open and delete remote `landing/e<n>`. Both cleanup steps run even if one fails, and each failure prints a warning. In `merge` mode, a bounce for failed posted checks first tries to turn off auto-merge when the check read's `autoMergeRequest` is not null. If that attempt fails, the queue pauses instead of bouncing. A rebuild bounce does not try to turn off auto-merge.

Keep one `schedule_task` heartbeat for a `queued` entry that has no open PR yet, and beside every watch. Create that heartbeat only if none is running, and reuse it across frontiers. The heartbeat exists because a PR with no posted check never wakes the watch, and because a merge never wakes the watch. In `merge` mode on a repository with required checks, when the PR is not in a merge queue, use `{"type": "interval", "everyMs": <fallback>}` where `<fallback>` is the everyMs number `land.py status` names. When it names none use 3600000. While an entry is `awaiting-merge` in `human` mode, or `gh api graphql` reports that `PullRequest.isInMergeQueue` is true for that PR, the heartbeat is required and uses `{"type": "interval", "everyMs": <merge wait>}` where `<merge wait>` is the merge wait number `land.py status` names. When it names none use 900000. That interval is the exception in [Pull request watching](../pstack-runtime/SKILL.md#pull-request-watching). The prompt is "Run `python3 <skills>/landing/scripts/land.py --repo <checkout> land` and act on what it prints per the landing skill." If the running heartbeat has the other interval, delete it with `delete_scheduled_task` and create it again. Do not drop the heartbeat in `merge` mode. Delete it with `delete_scheduled_task` when `status` shows nothing queued or awaiting merge. A crashed run is recovered by the next one. It asks git whether the last attempt was published before it retries. The contract refuses a fallback below 3600000 and a merge wait below 900000.

Before you drive an entry's PR in `merge` or `human` mode, read [Pull request lifecycle](pauses.md#pull-request-lifecycle). When the queue pauses or a command refuses the repository's `core.worktree` setting, read [When the queue pauses](pauses.md#when-the-queue-pauses).

## Capacity

The slot counts live in [capacity.md](reference/capacity.md).
