---
name: afk
description: Start a time-boxed standing mandate so the host agents keep working while the user is away from the keyboard, and stop it on return. Run when the user asks for afk, away mode, work while away, or to stop the mandate on returning.
disable-model-invocation: true
argument-hint: "[start [hours]|stop]"
---

# afk: start or stop an away mandate

Dependency: `delegate`. <script> is <delegate folder>/scripts/afk.py; if it is absent, report the missing dependency and stop. It classifies requests, keeps the lease and the log, executes nothing and makes no network call. What `check` allows is [references/rules.md](references/rules.md), the output of `afk.py rules`; read it, never restate it.

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

## Start

1. Run only on the user's invocation; no argument means `start`. Run `python3 -I <script> start`, with `--hours <n>` for `/afk start <duration>` (whole hours, rounded down; under one hour refuse; the script keeps 1 to 24 and the setup's `Lease hours`), and report its summary: the guards first, the lease length, any line saying a retired setting is no longer read, and the `This folder` line. It needs a recorded `## afk` section (`/setup add afk`). One lease covers every session on the machine: when one is live, `start` says when it ends and changes nothing. Then wake the coordinators and run the merge-blocker preflight as [references/start.md](references/start.md) says.
2. afk has one mode (`strict` was removed in 0.3.3): everything runs except the credential floor and the guards that are on, and Lease hours is the only limit (script). Blocking anything more is the host's job (its permission rules, auto mode, deny rules and sandbox); tell the user to write a host deny rule for anything that must stay forbidden. A repository's approved guards win in that repository; read `python3 -I <script> effective` there (script for `check`; following the view is advisory (agent judgment)). Never extend the lease or change setup while away: `check` denies everything after a setup change.
3. Keep the session working (advisory (agent judgment)): the lease bounds actions and starts no turn. Build this repository's queue with `goal` ([references/lease-rules.md](references/lease-rules.md)), set the host goal (`/goal`) to the line it prints, and start a self-paced loop where the host allows it (`/loop` on Claude Code); stop the loop when `check` prints an `end` line.
4. Never ask or wait for the user while the lease is live: settle questions through "Decide". On Claude Code the away question gate, the afk stop hook and the afk permission hook enforce this ([references/stops.md](references/stops.md)); elsewhere it is advisory (agent judgment).

## Work inside the lease

Load [references/lease-rules.md](references/lease-rules.md) when the lease starts and follow it for every action until it ends (advisory (agent judgment); `check` enforces [references/rules.md](references/rules.md)).

## Decide

Load [references/decide.md](references/decide.md) for every decision you would otherwise ask the user: the checks against "Where it must stop", the precedent packet, the ladder (a recorded rule, the evaluation table, the advisor, the host) and one `log --kind decision` record per attempt. The ladder is advisory (agent judgment); the record, the packet caps and the command forms are script-enforced. A decision grants no authority: the chosen action still passes `check`.

## End a turn and permission prompts

Load [references/stops.md](references/stops.md) before ending a turn under the lease and when a host permission prompt is denied with a request digest.

## Merge gate

Before any merge, load [references/merge-gate.md](references/merge-gate.md) and merge only when it holds (advisory (agent judgment), with the enforcers it names).

## Stop and return

On the user's return or `/afk stop`, run `python3 -I <script> stop --all` and report it; plain `stop` is refused, so an agent never ends the lease for every session (script). List first every merge that used the same-family fallback, then parked work, decisions and delegated runs still waiting; record running delegates as orphaned and leave them to the user. List the decisions from your `log --kind decision` records, those with `--precedents 0` first, and ask the user to mark each `kept` or `reversed`; record each with `python3 -I <script> review --decision <id> kept|reversed` (script: the id must exist) and write each reversal back as a decision with the user's reason through `tidy` (advisory (agent judgment)).

No plugin-run loop, scheduler or notice hook ships; following this procedure is advisory (agent judgment), backed by the script, the merge gate and, on Claude Code, the away question gate, the afk stop hook and the afk permission hook.
