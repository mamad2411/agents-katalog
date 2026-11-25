---
name: morning
description: >-
  Morning standup / daily kickoff. On "morning" (or "/morning", "good morning",
  "what did we do yesterday", "where do I start") produce a per-project recap of what was
  done YESTERDAY across all projects and what to continue or do next — pulled
  from git commits and yesterday's Claude Code conversations/transcripts and
  project memory. Use whenever the user types `morning` or asks for a daily
  start-of-day summary.
---

# Morning briefing

Give the user a fast, accurate "where we are" at the start of the day. Be
concrete and grounded in real data — never invent activity.

## Step 1 — Time window

```bash
YDAY=$(date -v-1d +%Y-%m-%d)        # yesterday (macOS date)
TODAY=$(date +%Y-%m-%d)
```

"Yesterday" = the calendar day `$YDAY`. If yesterday was a weekend/empty,
broaden to "since the last active day" and say so.

## Step 2 — What was DONE yesterday (per project)

**Git commits** across every repo under `~/Documents/Work/Projects`:

```bash
# discover repos (some projects keep multiple repos in subdirs)
find ~/Documents/Work/Projects -maxdepth 4 -name .git -type d 2>/dev/null
# for each <repo>:
git -C <repo> log --all --since="$YDAY 00:00" --until="$YDAY 23:59:59" \
    --pretty='%h %an %s' 2>/dev/null
```

Group commits by project. Also note uncommitted work in progress if relevant:
`git -C <repo> status -s`.

**Claude Code conversations from yesterday** — sessions touched yesterday hold
what was discussed/worked on even when nothing was committed:

```bash
# yesterday's session transcripts, newest first
find ~/.claude/projects -name '*.jsonl' \
     -newermt "$YDAY 00:00" ! -newermt "$TODAY 00:00" 2>/dev/null
```

Read the relevant transcript(s) and the lightweight prompt log
`~/.claude/history.jsonl` to recover, per project: what was being worked on,
what got finished, and what was explicitly left for later. Map the sanitized
project dir names back to real projects (e.g. the `...Documents-Work-Projects...`
dir is the Projects root).

**Project memory** — check the `memory/` folder inside each touched
`~/.claude/projects/<sanitized-project-dir>/` for ongoing-work notes that
affect today.

## Step 3 — What to CONTINUE / do next

From yesterday's transcripts and commits, surface:
- **In progress** — started but not finished (open branches, WIP commits,
  half-done threads).
- **Mentioned to continue / next** — anything the user said to pick up later,
  do tomorrow, fix, or follow up on. Quote the gist so they recognize it.
- **Blockers / open questions** raised yesterday and still unanswered.

Prefer the user's own words for carryover items so they trust the recall.

## Step 4 — Output

Format (English, concise, scannable):

```
☀️ Good morning — <today, weekday>

## <Project>
**Done yesterday:** <commits / key activity>
**Continue:** <wip + carryover>
**To do:** <todos / follow-ups>

## AI
...

## <other active projects>
...

## Today's priorities
1. <top next action>
2. ...
```

Only list projects with real activity yesterday or open carryover. End with a
short prioritized "today" list (top 3–5). Keep it tight — this is a kickoff,
not a report.

## Step 5 — News briefing

After the project recap, add a short news briefing. Topics (in priority order):

1. **AI / LLM industry** — new models & releases, major research, AI products,
   moves by Anthropic / OpenAI / Google / Meta / Mistral, funding.
2. **Startups / product** — notable launches, funding rounds, product/market
   trends relevant to my own products.
3. **General tech / industry** — big-tech moves, regulation, broadly significant
   events.

How to gather:
- Use `WebSearch` (and `WebFetch` for the few best sources) scoped to the **last
  ~24–48h**. Prefer primary/reputable sources; skip rumor and SEO filler.
- For a deeper dig on a heavy news day or when the user asks, run the
  `deep-research` skill on the specific topic instead of shallow search.

Output: 3–6 bullets total, each one line — headline + one-clause why-it-matters +
source. Newest/most important first. If nothing significant happened, say "quiet
day" rather than padding.

```
## 📰 News (last 24h)
- <AI/LLM headline> — <why it matters> · <source>
- <startup/product headline> — <…> · <source>
- <tech headline> — <…> · <source>
```

Keep the briefing skimmable — it complements the scheduled Cowork briefing, it
doesn't try to replace a full report.

## Notes

- Ground every "done" item in a commit, a transcript, or memory — if you can't
  source it, don't claim it.
- If git/transcripts show nothing for yesterday, say so plainly and fall back to
  open carryover from memory.
