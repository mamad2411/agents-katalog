---
name: usage-audit
description: Use when the person asks how their agent setup is actually being used, or whether a change to it helped ("are the skills being used?", "usage audit", "did the hook help?", "how often do I ask if it is done?"). Counts skill calls, typed turns, close-out questions and stop-check blocks from the session transcripts, for the last N days against the N days before. A script, no model, so the same question gets the same numbers.
---

# Usage audit

Count, then compare. The numbers come from the session transcripts on this machine and
from nowhere else.

## Run it

```bash
python3 ~/.claude/skills/usage-audit/scripts/usage_counts.py            # last 7 days against the 7 before
python3 ~/.claude/skills/usage-audit/scripts/usage_counts.py --days 14
python3 ~/.claude/skills/usage-audit/scripts/usage_counts.py --json     # for a file or another script
```

It reads `~/.claude/projects` (`--root` for another folder) and takes about fifteen seconds
on a few thousand sessions. It writes nothing.

## What it counts

| Count | What it is |
|---|---|
| skill calls | every time an agent loaded a skill, by skill |
| typed turns | messages a person typed, those sent while the agent worked included |
| close out questions | typed turns such as "can I close", "anything left", "are we done" |
| stop check blocks | times the stop check sent an agent back for a dropped request |
| sessions with a person | sessions with at least one typed turn; loop and script runs are left out |

## How to report it

1. Show the two tables as printed. Do not round, rank or rename.
2. Say what changed in the setup between the two periods, if you know it from the
   repository history: a profile, a hook, a skill added or removed. A count means little
   without that.
3. Name what the counts cannot show:
   - a skill's description can steer a session without the skill being loaded;
   - a skill added inside the period has no "before";
   - close-out questions are matched by wording, so an unusual phrasing is missed;
   - stop-check blocks are recognised by how the client records a Stop hook; check the
     first real block against the count;
   - nothing here says whether the work was right.
4. Stop there. A recommendation needs a question from the person.

## To judge one change

Count before the change and keep the output (`--json` into the repository's `.agent/`
folder), then count again after the same number of days. Compare the same rows.
