---
name: standup
description: >-
  Mission Control daily standup. Looks at all outstanding projects/tasks for the
  day and the live Claude sessions, then plans the day for maximum parallelism and
  writes today's single todo surface into the vault daily note. Use when asked to
  "standup", "plan my day", "daily plan", "what should I do today", or "let's plan".
---

# standup — Mission Control daily standup

Turns the day's outstanding work + live agent sessions into ONE plan, written into
the day's note as the single todo surface. The deterministic draft runs unattended
(e.g. 7am); when you're in the loop, refine it with judgment.

## Run it

```bash
python3 ~/mission-control/bin/standup.py          # human summary (sessions + buckets + blocked)
python3 ~/mission-control/bin/standup.py --json    # structured data to reason over
python3 ~/mission-control/bin/standup.py --draft    # write Today's Focus + Parallel Plan into Daily/<date>.md
```

`--draft` is non-destructive: it replaces only the `## Today's Focus` and `## Parallel
Plan` sections in `Daily/<date>.md` (creating the note from template if absent), leaving
everything else intact.

## The collaborative pass (what Claude adds over the deterministic draft)

After running `--draft`, read `--json` and improve the plan with judgment the script can't:

1. **Split the ready work into two lanes:**
   - **🔴 You, personally / sequential** — calls, decisions, anything that needs you (e.g. p0
     phone calls, family/finance choices). These define the day's critical path.
   - **🟢 Fan out to agents (parallel)** — self-contained work that a Claude session can drive
     (code tasks, research, drafting). Match these to the **idle sessions** (spare capacity)
     and propose `mc bind <id> --project "<P>" --task <slug>` for each.
2. **Respect dependencies** — anything in `blocked` stays off today's list; mention what unblocks it.
3. **Unblock waiting agents first** — any session with status `waiting` is costing you parallelism;
   surface it at the top.
4. **WIP limit** — your bottleneck is your own review bandwidth, not agent count. Don't fan out
   more parallel agent work than you can review; cap concurrent "waiting on you" sessions.
5. Rewrite the `## Parallel Plan` section with the two-lane plan, then present it to the user for
   sign-off. Treat the written plan as `needs_review` (it's auto-drafted until the user confirms).

## Notes

- Tasks declare dependencies via an optional `depends_on: [<slug>, …]` frontmatter field.
  When present, `standup.py` classifies dependent tasks as **blocked**; without it, all open
  tasks are **ready** and you reason about ordering yourself.
- Pairs with `harvest` (live session status) and the `today` glance layer.
- Engine: `~/mission-control/bin/standup.py` · design: `~/mission-control/README.md`.
