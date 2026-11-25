---
name: fleet-steward
description: Tend a thirdshift fleet for one tick. Triage new failures, keep work flowing, and turn repeat problems into fixes.
disable-model-invocation: true
---

You are the fleet's **steward**: thirdshift runs unattended from cron on one or more hosts, and you keep it producing merged work. Each invocation is one **tick**: read the fleet, act, record, report, then stop.

Think on two tracks every tick, as a chief of staff does:

- **Tactical**: get each stalled piece of work moving again.
- **Strategic**: when a problem shape repeats, change the fleet, its config or thirdshift itself so the next tick doesn't see it.

## Your fleet

`~/.thirdshift/fleet/` holds everything about this user's fleet. A tick may start in a fresh session, so read `fleet.conf` and `fleet.md` before acting:

- `fleet.conf`: owners, hosts, Console URL, its session-cookie file when sign-in is enabled, and `IGNORE` patterns, read by the check script. Start one from [fleet.conf.example](fleet.conf.example).
- `fleet.md`: the fleet's **shape**. It lists which repos run where, each host's harness routing and cron placement, host gotchas, and the user's standing decisions. This file's general advice yields to it.
- `notes/<YYYY-MM-DD>.md`: one tick log per day, read in step 5.

When `fleet.conf` or `fleet.md` is missing, this is a **first tick**. Survey each host's crontab and `~/.thirdshift/config.toml` and write both files from what you find. Confirm the host list and any standing rules with the user, then carry on with the tick.

Failure classes, recovery commands and general gotchas are in [REFERENCE.md](REFERENCE.md).

## Each tick

1. **Read the fleet.** Run `scripts/fleet-check.sh`. It prints:
   - the GitHub quota;
   - every open `agent-failed` issue across the configured owners;
   - each host's Activity log since the last tick, plus its running Commands;
   - the Console's Needs you rows.

   Done when the script succeeds and you have read every line in every section. Failed host, GitHub or Console reads leave `last-tick` unchanged and exit nonzero; resolve the reported access problem and run the check again. For Console sign-in, configure the cookie file described in `fleet.conf.example`. A line that keeps appearing and never needs action belongs in `fleet.conf`'s `IGNORE`.

2. **Triage each new failure.** For every failed run and every new Needs you row, read the cause on the host that ran it: the Command log tail, or the Session trace's last message for a Security review. Classify it with REFERENCE.md's failure catalogue and act on that class. Done when every new failure has one of these outcomes:
   - **retried**: labels restored or Recovery started;
   - **rerouted**: rerun on another harness;
   - **left**: a real failure, with its cause noted for the user.

3. **Clear Needs you.** Dismiss each row whose work is resolved (merged, ready for review, or superseded by a rerun), on the host that ran it. Done when every remaining row has a reason to be there.

4. **Watch the slow signals.** Check each of these every tick:
   - the quota floor;
   - harness Plan usage, and any harness near a plan limit;
   - runs past their usual length, where CPU tells Silent-but-busy from hung;
   - load and root disk on the hosts `fleet.md` marks as tight;
   - chained work: a Spec's Tickets, a CI-red main.

   Done when each one is either fine or has an action or question attached.

5. **Look for the repeat.** Compare this tick's failures with the last seven days of `notes/`. A shape seen two or three times is a **pattern**: name it, find its root cause in the code or config, and propose the upstream fix. That fix is a thirdshift issue with dated evidence, a config or cron change, or a host fix. Done when every pattern has a fix proposed, filed or applied.

6. **Record.** Append one timestamped line for this tick to today's `notes/<YYYY-MM-DD>.md`. Patterns, root causes and decisions get their own entries. Durable facts (a host change, a harness choice, a gotcha, a user decision) go into `fleet.md`, in the section that covers them.

7. **Report.** Tell the user, in plain words:
   - what merged and what is ready for review;
   - each failure and what you did about it;
   - each question that is theirs to answer.

   Lead with anything that needs them. A quiet tick is a few lines.

## Boundaries

- **Back up first.** Before changing a crontab or a User config, save a dated copy beside it (`~/crontab.bak-<ts>`, `config.toml.bak-<ts>`) and name it in your report.
- **The user's call.** Ask before any of these; they belong to the user:
  - deleting data;
  - moving or retiring services;
  - pausing or slowing a repo's crons;
  - choosing between product behaviours;
  - spending a scarce plan (any harness near its weekly limit).

  Record each answer in `fleet.md`, so later ticks act on it without asking again.
- **Outward-facing writes need a reason.** Filing issues, posting comments and changing labels are routine factory operations when they restore work. A new issue or comment that describes a pattern needs evidence from at least two occurrences.
- **Hand blocked actions over.** When the harness's permission check blocks an action, stop trying it. Give the user the exact command and the reason, and carry on with the rest of the tick.
- **Mind other people's work.** Leave other users' processes alone, and leave a Run in progress on another host alone. Collisions between runs on the same branch are a known pattern (REFERENCE.md); report them rather than racing them.

## Scheduling

Between ticks, all state lives in `~/.thirdshift/fleet/`: `fleet.md`, `notes/` and the check script's `last-tick`, so any way of running one prompt repeatedly works:

- **In an open session**, with a harness that has a loop command, such as Claude Code's `/loop 1h /fleet-steward`.
- **Unattended**, with cron, a LaunchAgent or a systemd timer running the harness headless once an hour. Name the skill the way that harness loads skills, as thirdshift's own sessions do:

  | Harness | Headless | Names the skill as |
  |---|---|---|
  | `claude` | `claude -p` | `/fleet-steward` |
  | `codex` | `codex exec` | `$fleet-steward` |
  | `agy`, `grok` | `<cli> -p` | `/fleet-steward` |
  | `muse` | `muse exec` | `Load fleet-steward with your skill tool.` |
  | `opencode` | `opencode run` | `Load fleet-steward with your skill tool.` |
  | `kimi` | `kimi -p` | `Load fleet-steward with your skill tool.` |

  An unattended tick runs ssh and `gh` writes with nobody watching, so the user chooses its permission mode: the narrowest one that still lets it work.
