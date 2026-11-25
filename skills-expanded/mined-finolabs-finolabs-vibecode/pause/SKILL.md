---
name: pause
description: Before you restart or shut the machine down, stop starting new work, let running work finish, write handovers and report what recorded work remains; resume after the restart.
disable-model-invocation: true
argument-hint: "[restart|shutdown] [--in <minutes>] | status | resume"
---

# Pause: drain before a restart or shutdown

Dependency: `delegate`. Resolve <pause> to `<delegate folder>/scripts/pause.py` and <handover> to `<delegate folder>/scripts/handover_state.py`; if either is absent, report the missing dependency and stop (advisory (agent judgment)). Pause only drains and records. It never stops a process, sends a signal, shuts the machine down or declares it safe: restarting is the user's call.

**Advisory (agent judgment):** Talk to the user in the language they are using, including questions and option labels; keep command names, flags, file paths, skill names and other technical names unchanged.

## Start

1. Run only on the user's invocation (host setting `disable-model-invocation`). With no argument, treat it as `start` (advisory (agent judgment)).
2. Run `python3 -I <pause> start [restart|shutdown] [--in <minutes>]`. `--in` is the time left before the machine goes down, as the user said it (script: integer 1 to 1440). The script writes the marker, ends an active afk lease and starts nothing.
3. From then on start no delegated run and no heavy job (advisory (agent judgment)). `heavy_run.py` refuses a new command with exit 77 while the marker is active (script); a missing, damaged or older-than-24-hours marker never blocks it.

## Drain and checkpoint

4. Write a handover for this session with `python3 -I <handover> write --session <id>` (goal, decisions, work in progress, next action on stdin; the id has 8 to 64 letters, digits or hyphens). Write one for each other session you know. The write is silent when storage is unsafe, so a handover counts only after the next step reads it back (script).
5. Run `python3 -I <pause> status` once, with one `--checkpoint <id>` for every handover you wrote, because a verdict covers only the ids given in that run and the line `checkpoints checked in this run` must equal the number of sessions you wrote for (advisory (agent judgment); the script reads each id given). Report the verdict and the whole "agent processes seen, not identified" section as printed (advisory (agent judgment)). The verdict covers recorded work only: `blocked`, `unknown` or `no recorded work remains` (script). It excludes the coordinator's own ledger record by the agent's judgment, and it never sees jobs started outside `heavy_run.py` or agent sessions it has no record of: say so, and tell the user to check those themselves.
6. A run past its budget is reported as stalled and left running (script). Wait for running work and report again on request (advisory (agent judgment)).
7. With `--in`, stay silent about stopping runs until the output says `deadline passed`. Then ask the user about each remaining run, one at a time, with the native question tool, and stop none yourself; record `cancelled` or `stalled` with `ledger.py finish` only after that run's yes (advisory (agent judgment)).
8. For `shutdown` the status output says handovers expire after 24 hours. Offer a longer-lived note and write it only with the user's yes (advisory (agent judgment)).

## Resume

9. After the restart, on the user's `resume`, run `python3 -I <pause> resume`. It removes the marker, counts handovers still within their lifetime and lists open dispatches that may have ended without a finish line. It starts nothing and does not restart afk (script). Read the handovers before continuing (advisory (agent judgment)).

`status` alone, at any time, only reports; it changes nothing.
