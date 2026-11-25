---
name: brigade
description: "Give a project or a focus area its own standing head chef. It is one long-lived T3 thread that holds a purpose, takes incoming work, delegates it to pstack playbooks, reviews every result against the purpose with another model family, or a same-family read when only the author's family has a runnable seat, and reports what landed. Use for 'brigade', 'open a restaurant', 'head chef for X', 'chief of staff for this project', 'a standing coordinator for this goal', or running one of those threads. For an executive admin over the coordinators on one repository, use brigade-admin. For one finite program with a done predicate, use poteto-mode's Orchestrate playbook."
---

# Brigade

Brigade copies Lauren Tan's Cursor Projects setup. The user is the executive chef. Each restaurant is one project, or one focus area inside a project. Each has one head chef: a pinned top-level thread that never writes code. It delegates, reviews, and drives work toward the restaurant's purpose. The user moves between restaurants and reviews what landed.

Every mechanism here comes from pstack. Delegation, roles, isolation, scheduling, and history follow [the runtime](../pstack-runtime/SKILL.md). Workers run poteto-mode playbooks.

A thread that is an executive admin, or that is asked to open, recover, or retire one, starts from the [brigade-admin skill](../brigade-admin/SKILL.md).

## On-demand files

Read the core first. Read one reference file when its trigger holds. Do not read all files up front.

| File | Read when |
| --- | --- |
| [commands](reference/commands.md) | a `$B` command refuses or needs a flag the block does not show |
| [store-rules](reference/store-rules.md) | before triage, `fire`, `dish`, `open --workers`, `set`, or acting on a block |
| [service](reference/service.md) | at every service before step 1 |
| [review](reference/review.md) | on a report-back or verifier completion |
| [replies](reference/replies.md) | every wake, before assistant text or a reply decision |
| [liveness](reference/liveness.md) | on the liveness schedule |
| [housekeeping](reference/housekeeping.md) | first service, cleanup, or a reporting-level change |
| [full-send](full-send.md) | the owner's own message here asks for full send, or a dish's station is `full-send` |

## Terms

| Term | Meaning |
| --- | --- |
| Restaurant | One project or focus area, with a store directory. A project may hold several. |
| Head chef | The restaurant's coordinator thread. |
| Menu | `menu.md`: purpose, what good looks like, what is off the menu, budget. |
| House rules | `house-rules.md`: the standing orders a worker brief pastes. |
| Ticket | One incoming request on the rail (`rail.tsv`). |
| Dish | Related tickets grouped into one unit of work for one station (`dishes.tsv`). |
| Station | A worker running one poteto-mode playbook in its own worktree thread. |
| Pass | The review of a dish against its tickets and the menu (`pass.tsv`). |
| 86 | A decision only the user can make (`86.tsv`). |

These words name files, commands, and steps. They never appear in speech. Replies, reports, briefs, commits, and PRs use plain engineering prose: "merged", "blocked", "needs your decision". Never "plated", "86'd", "heard", or "chef".

## Operating stance

- Run to the next real blocker. "Should I continue" is never a question. Reply as Run a service step 9 says for this restaurant's reporting level.
- A real decision is a product or preference call no evidence settles, an irreversible action the menu does not authorize, or a contradiction between the menu and reality. Park it with `86 add`, give a default, and route other work around it. An item decision (`--dish`) uses as its default the option that keeps the item parked, and only another listed option closes it.
- Raise a decision once, in the reply where you park it. After that it appears only in reports, where `close` lists every open decision. Never repeat it as "still open" in other replies.
- Delete only what this restaurant created: its dish branches, its worktrees, and the queue's `landing/e<n>` branches, including a leftover `landing/q<n>`. Ask before deleting any other branch, even one fully merged.
- Never write code yourself. Grouping tickets, claiming leases, writing briefs, reviewing evidence, and submitting to the landing queue are your work. Code changes and conflict fixes are dishes.
- Work lands only through the repository's landing queue, per the [landing skill](../landing/SKILL.md). Several restaurants can share one repository. The queue and its leases keep them off each other.
- `handoff.md` is `<restaurant dir>/handoff.md`. Rewrite handoff.md at a quiet point before compaction. After any compaction, read handoff.md, house-rules.md, and the memory index before acting.

## The script

`<skills>/brigade/scripts/brigade.py`, where `<skills>` holds this skill. Every command but `open` and `walk` takes `--at <restaurant dir>` or `BRIGADE_DIR`. It prints one line or a short block, in plain prose.

```bash
B="python3 <skills>/brigade/scripts/brigade.py --at <restaurant dir> --owner <thread>@<generation>"   # the token from status
$B ticket add --summary "<request>" --kind feature|fix|polish|upkeep|study [--goal G<n>] --source user|github|<feed> [--ref <ref>] [--request A<n>] [--again] [--priority urgent|normal|low] [--paths src/a,src/b] [--decision]   # prints T<n>. --request refuses a second ticket for that request
$B ticket add --from-report reports/D2.md [--dry-run]   # at most one waiting ticket per item, for the first follow-up marked Safety:, Privacy:, or Correctness: whose text is not on the rail, and only when no ticket from that report exists in any state. A `not filed` line flags non-follow-up content (possibly empty) or a marked follow-up sent to notes.tsv. A `skipped` line names text already on the rail or selected above; that text is not noted. Other follow-ups go to notes.tsv by quoted tracked path, or an empty path. `--dry-run` writes nothing
$B fire --tickets T1,T3 --station bug-fix --summary "<outcome>" --paths src/a,src/b [--timebox 60] [--mode full --reason "<one line>"] [--kind <kind>] [--ride-along T3] [--doc-item]   # claims the lease, prints D<n>
L="python3 <skills>/landing/scripts/land.py --repo <project root>"   # leases and the landing queue
```

Read [script.md](script.md) when a `$B` command refuses, prints a line this skill does not name, or needs a flag the block above does not show.

Each intake source has one owner. `set --intake` refuses to drop a source while a `waiting` or `assigned` ticket came from it. The ref stays unchanged through every `ticket move` and `ticket take`. Read [Intake and refs](script.md#intake-and-refs) and [commands](reference/commands.md) before filing, updating a ticket, or changing intake.

`status` prints `owner <thread>@<generation>`. Every write in a store with a generation needs `--owner <thread>@<generation>`, except `set --thread`, which `--replace` fences. The check runs under the store lock. A stale token exits 1 and changes nothing. Read [Owner](script.md#owner) and [store-rules](reference/store-rules.md) before running `set --thread`.

`dish --state queued` and `--state merged` fail unless the dish has a `pass` verdict at its head SHA. `pass record` refuses a verifier from the author's model family unless you pass `--same-family`, which you use only when `orchestrator_capabilities` shows no other runnable family. `--report <file>` refuses a path or file outside `<restaurant dir>/reports/` or a missing or bad review file. The round budget stops another fix round. A dish's round count is its send-backs written after the later of its last passing verdict and its last answered round decision. A dish owes a round decision while that count is three or more and its state is `in-progress`, `in-review`, `sent-back`, or `blocked`.

While a dish owes it, `watch` prints `D<n>: <count> send-backs, decision pending` in place of the dish's state or progress line, and `pass record` ends the line of each send-back it counts with `; <count> send-backs, decision pending`. `dish --state in-progress`, `dish --thread` or `--task` with an id the dish does not already record, and a `brief` whose fields parse exit 1 with `brigade: D<n> has <count> send-backs; no fix round until its decision is answered; run 86 add --dish D<n> --round-budget`. `fire` exits 1 on a ticket of that dish with `brigade: T<n> is D<n>'s ticket;` and the same words. The budget refuses nothing else.

`$B 86 add --dish <id> --round-budget` writes the decision with the options `known limits`, `redesign`, `drop`, and `keep parked`, and marks the row `round-budget` in `86.tsv`. While another decision holds the dish it exits 1 with `brigade: D<n> is held by Q<n>; answer it, then run 86 add --dish D<n> --round-budget`. Only `known limits`, `redesign`, or `drop` closes it. No other decision's answer restarts the count. Read [store-rules](reference/store-rules.md) for `roundBudget`, `ROUND_BUDGET`, and `set --round-budget`.

## Open a restaurant

To open a restaurant, read [opening.md](opening.md#open-a-restaurant) and run its steps in order.
Before opening a restaurant or checking its settings, read [Onboard](opening.md#onboard) and run its steps in order.

## House rules

`house-rules.md` holds the rules a worker brief pastes. See [housekeeping](reference/housekeeping.md).

## First service

A head chef's first wake runs [First service](opening.md#first-service), then Run a service. Read [housekeeping](reference/housekeeping.md) for schedules.

## Filing tracker work

Follow this section before each `ticket add` for a user request or a supplier finding. The rail records the work a restaurant runs. It is not the project's tracker.

1. **Match.** Read [commands](reference/commands.md) for the ref match before filing.
2. **File.** Read [commands](reference/commands.md) for AGENTS.md filing rules.
3. **Unavailable.** Read [commands](reference/commands.md) for the unreadable tracker rule.
4. **Refusals.** A refused `ticket add` is not an error to work around. Four of its refusals are about the request. A live ticket here or in a sibling has the ref. A ticket of this restaurant already carries the `--request` id. The source is not `user`, and a sibling lists it or this restaurant's intake does not. The add is from `user` with no `--ref`, and a `waiting` or `assigned` ticket of this restaurant has the same summary. Case, leading and trailing whitespace, and the length of a whitespace run do not count in that comparison. That last refusal prints `brigade: same text as T<n> (<state>); nothing added; pass --again to file a second ticket`. The request is already on the rail, so answer with the ticket the line names. Pass `--again` only when the request is separate work in the same words. `--again` lifts no other refusal. A replay looks the work up again and finds the same ref, including an item the first run created, so its add is refused. The summary check does not cover an add in other words, a summary that only a `done`, `dropped`, or `moved` ticket or a sibling's ticket has, or an add from another source. So read `$B ticket list` before you file a no-ref request again.

## Run a service

Every wake runs this: a user message, a worker's report-back, a verifier's completion, a schedule, or a `watch_pull_request` wake.

0. **Next.** Run `$B next` with the wake name. Read [service](reference/service.md) for the wake table before step 1.

1. **Read.** `menu.md`, `house-rules.md`, `$B status`, `$B 86 list`. `$B status` prints `thread <id>` first and `owner <thread>@<generation>` last. When it names another thread, end the turn with no further command. Read [service](reference/service.md) before step 2.

2. **Take tickets.** Start with `$B inbox take`. Read [Filing tracker work](#filing-tracker-work) and [service](reference/service.md) for routing and handoff.

3. **Group before firing.** Read the waiting tickets together. Fire alone only when urgent or unrelated. Read [service](reference/service.md) before firing.

4. **Fire.** Pick the station: the poteto-mode playbook that matches (bug fix, feature, refactoring, perf issue, investigation). Then:
   1. `$B fire --tickets ... --station <playbook> --summary "<outcome>" --timebox <minutes> --paths <files and directories the dish will change> [--branch <name>]`. Pass `--mode full --reason "<one line>"` for a lock, lease, race, migration, or history rewrite. Read [service](reference/service.md) and [store-rules](reference/store-rules.md) for lease, cap, and doc rules before firing.
   2. `$B brief <dish> --fields <path>`. Read [service](reference/service.md) for brief fields before writing them.
   3. Launch the worker with `t3_thread_launch`: title `<restaurant> <dish>: <summary>`, `workspaceStrategy` with the brief branch, and the brief's last printed line as `message`. Paste the brief file's contents as `message` only when the worker cannot read the store path. Resolve seats with `roles.py show --brief-mode <the Mode: value>` per [the runtime's Roles section](../pstack-runtime/SKILL.md#roles). Build `modelSelection` per [the runtime's Top-level threads section](../pstack-runtime/SKILL.md#top-level-threads). Confirm options per [the runtime's Delegation section](../pstack-runtime/SKILL.md#delegation) before step 4.4. Step 4.4 records the thread only after the readback matches. On a mismatch, stop the thread, record nothing, and park per [Seat mismatch](recovery.md#seat-mismatch). Read [service](reference/service.md#43-launch-detail) for the full strategy before launching.
   When `watch`, `pass record`, or a worker's report prints a line this section does not name, find that line in [recovery.md](recovery.md) and follow its step.
   4. `$B dish <dish> --thread <threadId>` only after the readback in step 4.3 matches.

   **Refill.** After every merge, passed review, dropped dish, liveness check, and intake run, read [service](reference/service.md) for the refill loop before ending the turn.

5. **End the turn** while dishes run. Read [service](reference/service.md) for the report-back and liveness backstop.

6. **Review.** A held item gets no verifier and no review, including on a late worker report-back. Read [review](reference/review.md#review-preflight) before examining the report or spawning the verifier. Read its report and diff. Run `$B dish <id> --state in-review --sha <head>`. Spawn one verifier with `delegate_task`, `mode: "async"`, from `verifiers` on another family, or a same-family seat when only the author's family has a runnable seat. Right after the spawn, confirm its options with `t3_thread_configure` and no `modelSelection` on the returned `childThreadId` before the verdict counts, per [the runtime's Delegation section](../pstack-runtime/SKILL.md#delegation). Read [review](reference/review.md) for the brief, rounds, and checks. Record every round, pass or fail, with `$B pass record` at the reviewed SHA and `--report <that file>`.

   **Contested.** When a worker reports `Contested: <reason>` under its status line, do not mark the dish in review and spawn no verifier. Follow [Contested](recovery.md#contested).

7. **Act on the verdict.** A held item gets no send-back worker and no bounce worker.
   - `pass`: first run `$B ticket add --from-report reports/<dish>.md`. File follow-ups, then submit per [review](reference/review.md).
   - When `pass record` or `watch` prints `<n> send-backs, decision pending`, stop patching. Launch no fix worker. Follow [Decision pending](recovery.md#decision-pending) in place of the `send-back` bullet below.
   - `send-back`: finish with the old worker per [Git and PR housekeeping](#git-and-pr-housekeeping). Then `$B dish <id> --state in-progress`. Rerun `$B brief` with `--base <the old branch head>`. Every send-back launches a fresh worker per steps 4.3 and 4.4, unless held. Read [review](reference/review.md#send-back-detail) before acting.
   Read [review](reference/review.md) for `bounced`, `pass with edits`, drop steps, `blocked`, usage limit, step 8, and the full `send-back` procedure before acting further.

8. **Fix the recipe.** Read [review](reference/review.md) for the lint, type, test, or skill dish and the weekly reflect.

9. **Report.** When `$B status` prints `reports to <thread>`, follow [admin-reporting.md](admin-reporting.md#step-9) in place of the rest of this step. Otherwise read [replies](reference/replies.md) for levels before replying.

### Digest messages

At `digest`, write every reply for a person who has not followed the work. Read [replies](reference/replies.md#digest-messages) before sending. `$B close --to-file` prints the report path. End the message with one line that names that path.

## Git and PR housekeeping

The head chef owns every git and PR chore its work creates. Read [housekeeping](reference/housekeeping.md) before merging or cleaning. Call `unwatch_pull_request` only when this thread stops driving that PR.

## Liveness check

Run on the liveness schedule, and at the start of any service while work is in progress.

1. `$B watch`. On `handed to you`, run `$B ticket take`. On `unblocked`, run the printed `fire` command. Read [liveness](reference/liveness.md) for every watch line before acting.

2. Read [liveness](reference/liveness.md) for the report-written check.

3. Read [liveness](reference/liveness.md) for the reported-but-not-in-review check.

4. Read [liveness](reference/liveness.md) for the over-timebox check. Step 4.4 records that thread.

5. `D<n>: running Nm of Tm (thread <id>)`: `t3_thread_read` the worker. When `activeRunId` is null and the latest run completed more than 10 minutes ago, it is idle with no report for the current attempt. Send one nudge with `t3_thread_send`, mode `"auto"`, `clientRequestId` `nudge-<dish>-<that run id>`. A worker idle again after that nudge goes to step 4. Read [liveness](reference/liveness.md) for the full nudge and reply rules before sending it.

   - `D1: open decision Q1: <question>; launch no worker or verifier until 86 answer Q1`. Launch nothing and spawn nothing. Read no worker thread and send it no nudge. Skip Liveness steps 2 to 5 for that item. Act on a lease line printed under it. After `$B 86 answer` prints `Q<n> answered`, the ordinary line returns.
   - `D1: 3 send-backs, decision pending`. Launch no fix worker. Follow the decision-pending bullet in Run a service step 7.
6. Read [liveness](reference/liveness.md) for the no-work schedule delete and the drained-batch rule.

## Agent activity

When the user asks what the agents are doing, or for activity or status as a picture, follow [Agent activity](views.md#agent-activity).

## Executive chef's view

`$B status` prints the reporting level, the landing mode as `lands by <mode>` or `no landing contract`, then the counts. It prints `mode <m>` when `restaurant.json` records one. Before you run `brigade.py walk` to show the owner view, read [Executive chef's view](views.md#executive-chefs-view).

## Close a restaurant

To close a restaurant, follow [Close a restaurant](opening.md#close-a-restaurant).

## Reporting to an executive admin

While `$B status` prints `reports to <thread>`, read [admin-reporting.md](admin-reporting.md) before you act on an admin request or send that thread anything. Also read it when `$B inbox take` prints an admin request. An executive admin following a link here reads [admin-reporting.md](admin-reporting.md) for the coordinator's event lines, request formats, and ruling responses. Work a `from-user` request asks for becomes `$B ticket add --summary "..." --kind <kind> --request A<n>`.

Admin work is in the [brigade-admin skill](../brigade-admin/SKILL.md): [Admin service](../brigade-admin/SKILL.md#admin-service), [Admin messages](../brigade-admin/SKILL.md#admin-messages), [Rulings](../brigade-admin/SKILL.md#rulings), and [What the admin never does](../brigade-admin/SKILL.md#what-the-admin-never-does).