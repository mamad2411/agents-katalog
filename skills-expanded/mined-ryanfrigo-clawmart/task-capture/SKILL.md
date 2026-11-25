---
name: task-capture
description: Turn any message ("remind me…", "can you…") into a tracked task with a due date, in your real task tool.
metadata: { "openclaw": { "emoji": "📌" } }
---

# Task Capture

The best chief of staff never lets a commitment fall through the cracks. This skill listens for action language in your mail and messages, extracts the real task, resolves the due date, de-dupes it, and files it in your actual task manager — so "can you send that over by Friday?" becomes a dated to-do without you touching it.

## When to use (trigger phrases)

Use this skill when the user says:

- "add that to my tasks" / "capture that"
- "remind me to …" / "don't let me forget …"
- "pull the action items out of this thread"
- Or run it automatically over inbound mail/messages to catch commitments as they arrive.

## How it works

1. **Detect action language** directed at the user: "can you…", "could you…", "please…", "remind me…", "don't forget…", "we need to…", "action item:", "todo:", "by <date>", "follow up on…". Ignore rhetorical questions and asks aimed at other people.
2. **Extract the task fields:**
   - **Action** — rewrite as a crisp imperative ("Send Dana the Q3 deck"), not a quote of the sentence.
   - **Owner** — default the user; only capture others' tasks if explicitly asked.
   - **Due date** — parse relative language ("Friday", "EOW", "tomorrow", "next week", "in 2 days") into an absolute date **in the user's timezone**. "EOD" → today; "EOW" → this Friday; bare weekday → the next occurrence.
   - **Context** — a one-line note plus a link/reference back to the source message so the task is actionable later.
   - **List / project / tags** — route by keyword or sender to the right list if `routingRules` are configured.
3. **De-dupe.** Fuzzy-match the action against open tasks before writing, so re-reading a thread doesn't create three copies of the same to-do. If a near-match exists, update its due date instead of adding a new one.
4. **Handle ambiguity honestly.** If a due date is genuinely unclear ("soon", "later this month"), either ask one quick clarifying question or file it undated and note the assumption — never invent a hard deadline that wasn't stated.
5. **Write to the task tool** — `things add "…" --when <date> --notes "<source>"`, `remindctl add --title "…" --due <date> --list <list>`, Todoist, Notion, or Trello. Use each tool's `--dry-run` / preview first when available.
6. **Confirm** with a one-line receipt so the user knows it landed and where.

**Batch mode:** given a thread, standup note, or meeting recap, scan the whole thing and extract every action item owned by the user as a checklist, then file them together.

## Output

Single capture:

```
Captured ✅
  "Send Dana the Q3 deck"
  Due: Fri Mar 6  ·  List: Work  ·  from Slack DM w/ Dana (linked)
```

Batch, from a standup thread:

```
Found 3 action items for you in "Launch standup":
  1. Finalize the pricing page copy        — due Wed Mar 4   → Work
  2. Get legal sign-off on the ToS          — due Fri Mar 6   → Work
  3. Book the launch retro                  — no date given   → filed undated
Filed all 3 to Things. Want #3 dated?
```

## Notes

- **Requires a task tool** connected to OpenClaw — `things` (Things 3, macOS), `remindctl` (Apple Reminders), Todoist, Notion, or Trello. This skill decides *what* the task is; the tool stores it.
- **Date parsing depends on timezone.** Set the user's TZ; relative dates are meaningless without it, and a wrong zone puts "tomorrow" on the wrong day.
- **Captures the user's commitments by default.** It won't assign work to teammates unless the user explicitly says so.
- **Never fabricates deadlines.** No stated date → undated or a quick clarify. Don't guess "Friday" to look tidy.
- **Idempotent by design.** Safe to run repeatedly over the same inbox; de-dup keeps it from spamming your list.
- **Source links** are only as good as what the message tool exposes — some channels give a deep link, some just quoted text. Fall back to quoting the trigger line.
