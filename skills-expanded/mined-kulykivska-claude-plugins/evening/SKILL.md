---
name: evening
description: >-
  Evening wind-down, the pair of /morning. On "evening" (or "/evening",
  "that is enough for today", "how should I end the day", "sum up the day") close the
  work day: summarize what was done TODAY, name what can wait until
  tomorrow, and suggest how to spend the evening well: physical activity,
  mental recovery, and one or two people worth talking to. Use whenever the
  user asks for an end-of-day summary or signals fatigue in the evening.
---

# Evening wind-down

The job: give an honest "you did enough today", park the work cleanly, and
point the evening at recovery, not more screens. Tone: warm, brief, zero
guilt. English.

## Step 1 — What TODAY produced

```bash
TODAY=$(date +%Y-%m-%d)
# commits today across every repo under ~/Documents/Work/Projects
find ~/Documents/Work/Projects -maxdepth 4 -name .git -type d 2>/dev/null
git -C <repo> log --all --since="$TODAY 00:00" --pretty='%h %s' 2>/dev/null
```

Plus today's Claude Code sessions (`~/.claude/projects/*.jsonl` modified
today) and memory notes. Compress into 3-5 lines of real accomplishment;
name finished things as finished. If the day was mostly thinking/debugging
with no commits, say that it still counts.

## Step 2 — Park the work

- **Safe to stop?** Check for dangerous dangling state: uncommitted changes
  (`git status -s` per active repo), a half-applied migration, a prod
  deploy mid-flight. If something shouldn't be left overnight, name ONLY
  that as the one thing to close out.
- **Tomorrow's top 3**: from today's threads, what to pick up first. Write
  them so tomorrow's /morning can quote them back.
- Then say it plainly: work is parked, today was enough.

## Step 3 — The evening itself

Check the calendar for tonight/tomorrow morning (Google Calendar tools if
connected: events between now and tomorrow 10:00) so suggestions fit
reality (don't propose a workout at 22:30 before an 8:00 event).

Suggest ONE physical and ONE mental item, varied across days, e.g.:
- physical: a walk without the phone, gym/stretch/yoga, a swim, early night
  when sleep has been short;
- mental: screens-off hour before bed, journaling three lines about the
  day, music/reading, cooking something proper instead of a snack.

If a wellbeing tracker or notes app exists, align with it
rather than inventing a parallel plan.

## Step 4 — People

Suggest 1-2 people to reach out to tonight, sourced from real signals, in
priority order:
1. calendar: birthdays or events today/tomorrow involving someone;
2. messages the user said they'd reply to (memory/transcripts);
3. family/friends not mentioned in a while: a short "how are you" counts;
4. warm business contacts ONLY if the user is clearly in the mood for it:
   the evening is for recovery first.

## Output shape

```
🌆 Evening check-out — <date>

**Done today:** <3-5 lines>
**Park it:** <the one thing to close, or "nothing dangling: safe to stop">
**Tomorrow:** 1) ... 2) ... 3) ...

**Tonight:** <one physical + one mental suggestion, one line each>
**Reach out:** <1-2 people and why>

That is enough for today.
```

Keep the whole thing under 20 lines. Never add new work items in the
evening; anything new goes into tomorrow's list.
