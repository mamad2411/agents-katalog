---
name: maintain-project-state
description: Resume, save and recover the workspace state. Use at session start, before a handoff or context compaction, after an abrupt stop, or when ws check reports errors.
---

# Maintain project state

Keep `docs/state/` current so the next session can continue without the chat.

## Resume

1. Run `python .agents/tools/ws.py brief`. Handle its Attention section first, then read the T0 files it names.
2. Run the command under "Next" in the brief. When it says "do not claim", another window is working:
   ask the user, and read `.agents/guides/PROTOCOL.md` "Ownership" before you write anything.
3. If `ws start` lists unsaved files, open each one and sort it with the table below.
4. If `recovery_notes` names a running job or a long command, check whether it finished and what it
   changed before you run it again: a second run may repeat a deploy or a write.
5. Record what you found: `ws card --set recovery_notes="..."`.
6. Before the first code change, run the current task's acceptance once. A failure that was there
   before your change is the baseline; write it in `recovery_notes` so it is not blamed on your work.

| An unsaved file is | Do |
| --- | --- |
| Product code or a state file the last task changed, and complete | Run that task's acceptance; record the result with `ws verify` |
| Half-done, matching the card's `current_task` or `stop_point` | Finish it as that task, or set the task back to `todo` with a reason |
| A scratch script, probe output or report from another project | Move it to `.tmp/` or its project; add a generated path to `exclude` |
| Not explained by the card, the tasks or the notes | Do not delete or seal it. Ask the user, and record it in `recovery_notes` |

## Save

| Moment | Command |
| --- | --- |
| Every few turns, or after a finding worth keeping | `ws note "..."` |
| After a verified step | `ws checkpoint --keep --stop "..." --next "..."` |
| Before a long or risky command | `ws card --set recovery_notes="running X; if it dies, check Y"` |
| Context nearly full, or the user switches tools | `ws checkpoint --stop "..." --next "..."` |
| Brief or checkpoint reports unreconciled messages | `ws reconcile`, then answer each listed message |

The stop point names the exact state: file, function, test result.
The next step is an action a new session can start without asking.

## Recover

| `ws` reports | Do |
| --- | --- |
| `NOT READY: REQUIREMENTS.md has a goal but no requirement rows` | Record the confirmed requirements from the conversation, then checkpoint again |
| `checkpoint refused` | Fix each listed error. If you cannot, add `<!-- SYNC-PENDING -->` under "Unfinished work" in HANDOFF.md, describe the gap and checkpoint again with `--keep`: the card is saved without a seal and READY waits for the fix |
| `this session runs with WS_ROLE set` | You are a subagent or helper. Report to the session that started you; do not write state |
| `wrote N min ago; another conversation may still be working` | Do not take over. Ask the user which window continues |
| `revision conflict` or `took over the workspace` | Another session is active. Stop writing and re-read HANDOFF.md |
| a broken table with file and line | Repair that row by hand, then run `ws check` |
| `change rejected; no change can be checked until these are repaired` | Repair what it lists first: a broken row by hand, a changed or missing archive file from version control or a snapshot. Ask the user before you touch the CONTINUITY line |
| `files changed after the last checkpoint` | Inspect them, then checkpoint |
| `owns the workspace from another window that is still running` | Do not write. Ask the user; if that window is finished, `ws start --force --reason "<what the user said>"` |
| `another ws.py command is running` | Wait and retry: another window runs a `ws` command, and the lock ends with that process, so delete nothing. If the message names `WS_LOCK=legacy`, the drive cannot lock; move the project to a local disk |
| `<ID> was removed. IDs are permanent` | Restore the row, or close it and run `ws compact` |
| `ws` cannot run (no shell, no Python) | Edit the tables by hand in the PROTOCOL.md formats; run `ws check` when it can run again |

## Size

Run `ws compact` when `ws check` warns about size or after a milestone.
It moves closed rows to `docs/logs/CLOSED_ITEMS.md` and rolls long logs. IDs stay reserved.
