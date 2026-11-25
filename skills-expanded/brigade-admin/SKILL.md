---
name: brigade-admin
description: "Run the executive admin for the brigade coordinators on one repository. It is one pinned T3 thread that forwards the user's requests, files shared intake once, rules on conflicts between coordinators by published rules the user can overrule, and writes one plain-language update. Use for 'executive admin', 'open an executive admin', 'an admin over the coordinators on one repository', 'recover the executive admin', 'retire the executive admin', or running that thread. For one coordinator on a project or focus area, use brigade."
---

# Brigade admin

Read [the pstack-t3 runtime](../pstack-runtime/SKILL.md) before spawning workers, choosing models, scheduling, or isolating work. It maps those steps onto T3's orchestrator tools.

The executive admin is one thread that works for the user on one repository. As an assistant, it keeps the user up to date across every coordinator there, forwards requests, files shared intake once, and writes one plain-language update. As a coordinator of coordinators, it settles conflicts between them on its own authority, by the rules in [Rulings](#rulings), and logs every ruling so the user can review and overrule it. It escalates only what the rules cannot settle. The scripts enforce. The cap stays in `land.py`, paths stay exclusive through leases, and each ruling is carried out by a script. The user sets the rules' inputs, answers every decision, and has the last word. Each coordinator keeps its own work, reviews, queue entries, and `menu.md`. Without an admin, every coordinator works as [the brigade skill](../brigade/SKILL.md) says.

Its store is `<store>/<project>/.admin/`, beside the coordinators it serves, with `role: "admin"` in `restaurant.json`. It is a sibling of each of them, so intake ownership, `ticket move`, and handoff ids work as for any sibling. An admin thread follows this skill, and [Filing tracker work](../brigade/SKILL.md#filing-tracker-work) and [Digest messages](../brigade/SKILL.md#digest-messages) in the brigade skill. That skill's [Open a restaurant](../brigade/SKILL.md#open-a-restaurant), [First service](../brigade/SKILL.md#first-service), [Run a service](../brigade/SKILL.md#run-a-service), [Liveness check](../brigade/SKILL.md#liveness-check), and [Git and PR housekeeping](../brigade/SKILL.md#git-and-pr-housekeeping) are for coordinators. The admin runs the brigade skill's script, [`../brigade/scripts/brigade.py`](../brigade/scripts/brigade.py) from this file, so `<skills>` is the directory that holds both skills. Read that skill's [Terms](../brigade/SKILL.md#terms), [The script](../brigade/SKILL.md#the-script), and [Reporting to an executive admin](../brigade/SKILL.md#reporting-to-an-executive-admin) sections before the first command. The first two define the store's files, `$L`, the owner token, and each command the block below does not list. The third holds the coordinator's side of each line and each ruling. Here `$B` is `python3 <skills>/brigade/scripts/brigade.py --at <store>/<project>/.admin --owner <thread>@<generation>`. Drop `--owner` on `set --thread`, per [The script](../brigade/SKILL.md#the-script). Opening step 4 runs before any thread is recorded, so it also drops `--owner`. Read [lifecycle](reference/lifecycle.md) for store paths before opening.

```bash
python3 <skills>/brigade/scripts/brigade.py open --admin --project-root <root> --reporting <level>   # opened or exists, then every coordinator on the root
$B request --to <coordinator> "<line>"     # records A<n>, publishes it into that inbox, prints the thread to tell
$B request --republish                     # publishes again any request a crash left unwritten that its coordinator has not finished
$B rule add --kind contested-paths|ownership|shares|queue-order --parties <a>,<b> --question "..." --rule purpose|priority|age|related-work|dependency|floor|user --decision "..." [--supersedes R<n>]   # prints R<n>
$B rule overrule R<n> --decision "<the user's words>"   # marks it overruled and records the user's ruling
$B rule set R<n> --state done|expired ; $B rule list [--state in-force]
$B sync                                    # copies each coordinator's new log.tsv rows into this log, or prints nothing new
$B set --thread <new> --replace --expect <old> [--stopped <run id>|idle|gone]   # compare-and-swap of the admin's thread
```



The admin store refuses `fire`, `brief`, `dish`, `pass`, and `watch` with `brigade: the executive admin routes work and never runs it`.

## On-demand files

Read the core first. Read one reference file when its trigger holds.

| File | Read when |
| --- | --- |
| [rulings](reference/rulings.md) | before evaluating, applying, or reconciling a ruling, or escalating a conflict |
| [lifecycle](reference/lifecycle.md) | when opening, recovering, or retiring |

## Open an executive admin

The user asks any thread for an executive admin.

1. Ask the user for the reporting level with the host's question tool, unless the user already said it. Recommend `digest`, because the admin exists so the user hears less.
2. Run `python3 <skills>/brigade/scripts/brigade.py open --admin --project-root <root> --reporting <level>`. It prints `opened <dir>` or `exists <dir>`, then one block per coordinator on the root with its purpose. Only the caller that got `opened` launches a thread.
3. Write the user's priorities under `## Priorities` in its `menu.md`, highest first, with the user. Add which intake sources it should own. Without priorities, the rules fall back to purposes and age.
4. Move shared intake. Read [lifecycle](reference/lifecycle.md) before moving a shared source or running `set --intake` with no `--owner`.


5. Ask the user, with the host's question tool, for the intake interval in whole minutes and the morning and evening times as `HH:MM`. Offer one hour, `09:00`, and `18:30` as the defaults. Refuse an interval above 120 minutes and ask again, so the idle check runs before a coordinator's 6-hour leases lapse. Refuse an evening time at or before `18:00` and ask again, because the coordinators send their evening reports at `18:00`. Read [lifecycle](reference/lifecycle.md#launching-the-admin-thread) for the project lookup and launch. Record the returned `threadId` with `$B set --thread <id>`, then send the start message with `t3_thread_send` and mode `"auto"`.

When the user asks the admin to open a coordinator, it runs [Open a restaurant](../brigade/SKILL.md#open-a-restaurant) in the brigade skill, shows the user any overlap with the purposes `open` printed, and launches the new thread once the user agrees.

## Admin first service

1. `t3_thread_organize` with `action: "pin"` and no `threadId`, acting on the caller on purpose.
2. Create three schedules with `schedule_task`, bound to this thread, using the intake interval and the morning and evening times from the start message, and record each under the name its bullet gives with `$B set --schedule <name>=<id>`. Each prompt says "Use the brigade-admin skill. You are the executive admin for the store at `<store>/<project>/.admin`. Reporting level: `<level>`. Run a service." Read `<level>` from the admin store's `restaurant.json` key `reporting`, the same value `$B status` prints after `reporting:`.
   - `intake`: `{"type": "interval", "everyMs": <the start message's interval>}`. Each service also runs the idle check, which must run before a coordinator's 6-hour leases lapse.
   - `morning`: `{"type": "fixed_time", "timeOfDay": "<the morning time>"}`, for routing and checks.
   - `evening`: `{"type": "fixed_time", "timeOfDay": "<the evening time>"}`, after the coordinators' 18:00 reports. The prompt adds "Write the update."
   A start message that carries no value for one of the three takes the default, `3600000` ms for intake, `09:00` for morning, and `18:30` for evening.
   It creates no liveness or drain schedule, because it runs no workers and owns no queue entries.
3. Send each coordinator the `reports-to` line as a request, per Admin messages, with this thread's id as `<thread>`.
4. Run an admin service.

## Admin service

Every wake runs one service, whether a schedule, a message, or a user message.

1. Run `$B status`. [The script](../brigade/SKILL.md#the-script) describes its `thread` line and its `owner` token. When it names another thread, or prints `thread not recorded` because the admin was retired, end the turn with no action. Otherwise pass that token as `--owner` on every `$B` command, and `--owner .admin/@<generation>` on every `$L` ruling write, which is `lease reserve`, `lease unreserve`, `share`, and `contest`. `$L lease list`, `$L status`, and `$L land` take no `--owner`, and the admin never runs `land`. A write refused with `is stale` means another thread owns the store. End the service at once and run no further command, including the ruling's `$L` enforcement.
2. Read `menu.md`, `$B status`, `$B 86 list`, and `python3 <skills>/brigade/scripts/brigade.py walk --repo <root> --stale-hours 3`. When the user's message answers a question `$B 86 list` prints, run `$B 86 answer Q<n> --answer "<the user's words>"` before anything else, then act on it per [Escalate](#rulings).
3. `$B inbox take`, for tickets moved back. Then file each piece of work the user asks for in this service as `$B ticket add --summary "<the user's request>" --kind <kind> --source user`, one ticket per request, with the `--ref` that [Filing tracker work](../brigade/SKILL.md#filing-tracker-work) gives it. That section's Refusals step says what a refused add means. Run that section's Match step for each request before its add, even when it names no ref. Route it per step 4 like any other ticket. A message that settles a conflict between coordinators, such as which one's item lands first, is a ruling per [The user's ruling](#rulings), not a ticket. Then intake from its owned sources with `$B ticket add --summary "..." --kind <kind> --source <source> --ref <ref>`, reading each source and filing each finding per [Filing tracker work](../brigade/SKILL.md#filing-tracker-work). [The script](../brigade/SKILL.md#the-script) says what `ticket move` in step 4 does with that ref. Then `$B request --republish`.
4. Route each waiting ticket to the coordinator whose purpose fits with `$B ticket move <id> --to <coordinator>`, then `t3_thread_send` to the thread it prints, with mode `"auto"`, the `ticket` line from Admin messages, and the handoff id `<project>/.admin/T<n>` as `clientRequestId`. A ticket that fits two purposes gets an ownership ruling. A ticket no purpose fits becomes `$B 86 add` with options and a default.
5. Read coordinator events from two sources. Run `$B sync`. It prints each coordinator's new store rows. The event table in [Reporting to an executive admin](../brigade/SKILL.md#reporting-to-an-executive-admin) says which lines leave a store row and which are message-only. A message-only line never appears in `sync`. Act on each one from the message that woke this service. Rule on each conflict either source shows, such as a block older than an hour, a `contest` or `appeal` line, or waiting work that needs a changed share, per [Rulings](#rulings). Record each ruling with `$B rule add` before carrying it out. Then reconcile every ruling `$B rule list --state in-force` prints, mark the ones whose condition ended with `$B rule set`, and carry out the rest again, which repeats nothing. Pass each coordinator's `decision` to the user. Never answer it. When the wake message is a coordinator's `reply` line, pass it to the user, including a decline and its reason, per [What the user hears from the admin](#what-the-user-hears-from-the-admin). A malformed-line failure from `sync` goes to the user as a failure.
6. When the repository sits at its cap while tickets wait for an hour, park a decision proposing a new cap, with a default. A coordinator that `walk` marks idle while it holds leases becomes a decision for the user, before its 6-hour leases lapse.
7. Reply per [What the user hears from the admin](#what-the-user-hears-from-the-admin).

## Admin messages

Every exchange is an explicit `t3_thread_send`. The admin sends with mode `"auto"`, so the coordinator wakes. Coordinators send the event lines as [Reporting to an executive admin](../brigade/SKILL.md#reporting-to-an-executive-admin) says. Messages are wakes, and the stores are the record for every line with a store row. The admin reads those events through `sync`, which reads each `log.tsv` past a cursor and relays each row once, so a second wake for one stored event finds nothing new. It reads a message-only line from the message itself and acts on it in that service, per service step 5.

Every admin line except a routed ticket is a request. Run `$B request --to <coordinator> "<line>"`. It prints `A<n> for <coordinator>; tell thread <id>`. When its output ends with `no thread recorded for <coordinator>` instead of `tell thread <id>`, send nothing. The request waits in that inbox. Otherwise call `t3_thread_send` to that thread with the line and `clientRequestId` `A<n>`, so a retried send delivers once. Retry a failed send with the same `A<n>`, or leave it to the next scheduled wake, because the file waits in the inbox. Never run `request` again to retry. Each run records a new id, so the coordinator would act twice.

The exact text of each line is in [Reporting to an executive admin](../brigade/SKILL.md#reporting-to-an-executive-admin), under Requests. The table there holds four of them, and the sentence after it holds the `ticket` line. Copy the line from there and fill in its fields. This skill's `<coordinator>`, the directory name of the coordinator the line goes to, fills the `<restaurant>` field.

| Line | Sent when |
| --- | --- |
| `ticket` | it routes a ticket, as in service step 4 |
| `from-user` | the user's words are meant for that one coordinator: a question about its work, a mode change, or a disagreement with its verdict. Work the user asks for is a ticket per service step 3, and a conflict between coordinators the user settles is a ruling, never a `from-user` line. Quote the user's words |
| `answer` | the user answers that coordinator's decision, including an answer that keeps it parked. Send the option the user picked word for word, or the user's words when they picked none. What the coordinator does with it is in [Reporting to an executive admin](../brigade/SKILL.md#reporting-to-an-executive-admin), under Requests. |
| `reports-to` | its first service, recovery, or retirement. `<thread>` is this thread's id, or `none` on retirement |
| `ruling` | it records a ruling. Send it to each coordinator involved |

## Rulings

The admin rules on four kinds of conflict between coordinators. It applies the rules in order, and the first rule that separates the parties decides. A ruling stands until it is done, expires, is superseded, or the user overrules it. How a coordinator complies is in [Reporting to an executive admin](../brigade/SKILL.md#reporting-to-an-executive-admin), under A ruling's side.

Every other holder's claim on those paths is refused until the winner claims them or the reservation expires. An item the other depends on, as a `contest` line stated, lands first. Read [rulings](reference/rulings.md) for the contest commands when no contest covers the two holders, and before `$B rule add` or acting on an overrule or appeal.

Carry out each ruling after `$B rule add`, then send the `ruling` line. Read [rulings](reference/rulings.md) for States, Replacing, Overrule, Appeals, and Escalate.

## What the admin never does

- Decide what belongs to the user. It sets no cap, landing mode, priority, or purpose, and never answers a coordinator's decision.
- Direct a coordinator's own work. What a coordinator builds, how it reviews, and when it submits, absent a conflict, stay its own.
- Write code, or edit any file in a repository.
- Land work. It never runs `$L submit` or `$L land`, and never merges or deletes a branch.
- Override a review. It never records or changes a verdict, never asks a coordinator to submit work that did not pass, and never messages a worker.
- Write into a coordinator's store, except new files in its `inbox/` through `ticket move` and `request`.
- Claim, renew, or release a lease, or start work. It only reserves contested paths for a ruling's winner.

## Admin recovery and retirement

The store outlives its thread. Recovery is a user request, run from one thread. [The script](../brigade/SKILL.md#the-script) says how every `brigade.py` write checks the owner token, and how `set --thread --replace` raises the landing floor. Every `land.py` ruling write checks `--owner .admin/@<generation>` against that floor. So a command the old run started either finished before the claim or is refused after it. The stop steps are a courtesy.

1. Claim the store with `$B set --thread recovering:<this thread> --replace --expect <old thread>`. Of two racing recoveries, one wins and the other exits 1. The output names the recorded schedule ids and `previousThread`. Run `$B status` again for the new owner token.
2. Read [lifecycle](reference/lifecycle.md) for steps 2 to 6 before continuing.

When the recovering thread is itself gone, a later recovery claims with `--expect recovering:<that thread>` and runs the same steps.

To retire the admin, read [lifecycle](reference/lifecycle.md) for routing, intake, schedules, `reports-to`, unpin, and `set --thread`.

## What the user hears from the admin

The user hears from one thread. The admin's level uses the same three values as a coordinator's.

- `every-turn`. Reply after each wake. Each message is a wake. A coordinator's routine wake sends the admin no line, so it is not one.
- `milestones`. Reply when any coordinator's work merges, when a review sends work back or blocks it, when the user has a decision to make, when a failure arrives, when the user sends a message, and for the evening update. Every other wake ends the turn with no reply text at all. Those wakes include a `blocked` line, a `reply` line, a `contest` or `appeal` line, a ruling, a `drained` or `report` line, and a scheduled service with nothing new.
- `digest`. Reply for a decision, a failure no coordinator can fix itself, one summary when every coordinator has drained, and the evening update. Every coordinator has drained when no coordinator line in `walk` shows `in progress`, `in review`, `passed review`, or `waiting to land`.

A ruling is never a reply occasion on its own at `milestones` or `digest`. A message from the user gets at least a one-line acknowledgment at every level, and a direct question gets an answer. A coordinator's `reply` line answers something the user asked, so pass it on, including a decline and its reason. It arrives only as the message that woke the admin, so this thread carries it until that reply. At `every-turn` it goes in that wake's reply. At `milestones` and `digest` it goes in the next reply that level sends, and in the evening update at the latest.

Every admin reply follows [Digest messages](../brigade/SKILL.md#digest-messages) at every level. Say what changed for each purpose. Name each coordinator by its purpose, not its store name. List the rulings made since the last update in plain words, each with the rule that decided it, and say the user can overrule any of them by describing it. The full update that `$B close --to-file` writes holds each ruling's id and each coordinator's newest report.
