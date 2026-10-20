---
description: Score your recent writing against rules/writing-style.md. Tool invocation (run /founder-os:writing-score). Counts the tells, names the three to fix first, reports the change since the last run. Read-only on your files.
allowed-tools: ["Read", "Glob", "Bash"]
---

# Founder OS writing-score

Measure the writing, do not rewrite it.

## Procedure

1. Read the skill at `skills/writing-score/SKILL.md` and execute it end to end.

2. The skill owns the run, the reading-back, and the output. This command is a thin trigger.

3. If the skill file is missing, reply: `Writing-score skill not found at skills/writing-score/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

4. If the founder named a file rather than asking for the whole scorecard, run the single-file form instead and read that back:
   `python scripts/register_census.py <path> --lines`

## Rules

- Read-only on the founder's writing. The only writes are `state/writing-scorecard.md` and `state/writing-scores.jsonl`, which the script makes.
- Never rewrite a sentence unless asked. The point is the count.
- Quote a real sentence for each class named. A class name on its own teaches nothing.
- If the install is empty (no `core/identity.md`), reply: `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
- No em dashes or en dashes. Hyphens only.
