---
name: flow-map
description: Use when someone wants to audit their whole automation system and see it as a visual map - which agents, crons, routines, and scheduled jobs actually run, where data flows in and out, what writes to what, and what's stale or dead. Trigger on "/flow-map", "map my data flows", "audit my system and map it", "make a flow map", "where does my data actually move", "map my automations".
---

# flow-map

Audit an automation system end to end and render it as one dark, interactive, single-file HTML data-flow map: four columns (Sources → Agents/routines → Stores → Outbox), hover any node to isolate its flows, plus a Schedule tab and a Changed tab.

**Core principle: the map only shows what you can prove is running.** Live state is the source of truth. Docs, memory files, and the user's own description are leads, not evidence. Anything you can't verify gets flagged as unverified, never silently drawn as fact.

## Step 0 — Scope

One quick question before touching anything: what system are we mapping? (work vs personal vs everything, one machine vs several, include on-demand tools or scheduled-only). Default: scheduled + event-driven things that move data, on this machine plus connected cloud services. On-demand tools only if they're part of a running flow.

## Step 1 — Discover from live state

Enumerate every scheduler surface that exists on this platform. Check each; skip what doesn't apply. Record WHERE you verified each item (this becomes your evidence list).

| Surface | How to enumerate |
|---|---|
| Cloud scheduled agents / routines | The platform's trigger/cron API (list ALL, note enabled vs disabled). Read the LIVE prompt or config, not a local copy. |
| macOS LaunchAgents | `ls ~/Library/LaunchAgents/`, then read each plist for schedule + what script it runs. Read the script's header to learn what it actually does. |
| Unix cron / systemd | `crontab -l`, `systemctl list-timers` |
| Windows | `schtasks /query` |
| CI crons | `.github/workflows/*.yml` schedule blocks, GitLab schedules |
| No-code automations | Zapier/Make/n8n dashboards, Notion/Airtable native automations, Slack workflows. Often not enumerable from the CLI: this is an interview question. |
| Webhooks / event-driven | App code (route handlers), Supabase/Firebase functions, form triggers. Also an interview question if code isn't local. |

For each item found, extract: **name, schedule, runtime/model, what it reads, what it writes, guardrails (what it must never touch), status** (live / needs work / off-dead / on-demand), and any recent change worth flagging.

Disabled or retired things are findings too. They go in the Changed tab, not on the map.

## Step 2 — Model it

Four columns, fixed:

- **col 0 — Sources**: external + local inputs (email, chat, calendar, APIs, DBs read by agents, local files)
- **col 1 — Agents / routines**: everything that runs (cloud + local + native + on-demand)
- **col 2 — Stores**: the system of record (databases, canonical pages, logs)
- **col 3 — Outbox**: where results land for the human (DMs, draft folders, sends)

Node fields: `{id, col, label, status, sched, model, does, flag}`. Status colors: `green` scheduled + live, `amber` needs work, `red` off/dead, `blue` external or on-demand, `purple` store. `flag` is for warnings and recent changes only, not general description.

Classification rules that trip people up:
- **Unverified is a flag, not a color.** Status reflects the node's nature; amber is only for a concrete needs-work reason (broken step, stale data, half-built). A perfectly healthy Zap you just couldn't inspect stays blue with an unverified flag.
- **`model` on non-LLM automations**: put the runtime instead ("Shell script", "Webhook", "Notion rules", "Python"). Every col-1 node gets one.
- **Dead-end local artifacts** (backup folders, exports nothing reads): they're Stores. Outbox is only for surfaces the human actually checks (DMs, draft folders, sent messages).

Edges: `[from, to, kind]` where kind is `read` (data in, blue), `write` (data out, green), or `stale` (broken flow, red dashed). Every edge must trace to evidence from Step 1. An agent with no edges is fine (on-demand products); an edge with no evidence is not.

## Step 3 — Interview

Discovery always misses things that don't live on disk. Ask AFTER discovering, so questions are informed, and batch them into ONE multiple-choice round (AskUserQuestion or equivalent), not a drip. Pull from this bank, keep only what discovery couldn't answer:

1. **Coverage**: "I found N scheduled things: [list]. What am I missing?" (options: no-code automations like Zapier/Notion, webhooks, manual rituals that should count, nothing)
2. **Ambiguous status**: for each item you couldn't classify: "X looks [dead/stale/half-built]. What's its real status?"
3. **Recently retired**: "Anything killed recently that I should list in the Changed tab so the map explains its own history?"
4. **Sensitive exclusions**: "Anything to leave off (personal-side jobs, secrets-adjacent flows, client names)?"
5. **Destination**: "Where should the file live?" (Desktop, project folder, published artifact)

Fold answers back into nodes/edges. User-reported items you couldn't verify get `flag: "Reported by [user], not verified against live state."`

## Step 4 — Generate

Copy `template.html` from this skill's folder. It is a complete working example with sample data. Replace:

1. `<title>` + the `<h1>` + the header `.sub` line (put the verification date in the sub: "Verified against live state YYYY-MM-DD")
2. Everything between `// ==== DATA START ====` and `// ==== DATA END ====` (COLS, NODES, E)
3. The `changedView` innerHTML: what changed recently, what's carried over, what was retired (with dates)

Do NOT touch the CSS or the render/hover/panel/schedule JS. The template is self-contained, no external requests, works from a double-click.

Hard rules for the data:
- Never invent a schedule, model name, or read/write edge. No evidence = no edge.
- Unverified user-reported items keep their flag.
- Convert cron expressions to human time in the user's timezone ("Wed 9:07am ET"), keep UTC math out of labels.
- `does` text is 1-3 sentences, plain language, written for a teammate who has never seen the system.

## Step 5 — Verify and deliver

- Open the file in a browser. Confirm it renders, hover isolation works, all three tabs populate.
- Sanity-count: nodes on map == items in your evidence list + interview additions. Say the number out loud in your summary.
- Tell the user explicitly what you EXCLUDED and why (scope, personal-side, unverifiable).

## Common mistakes

| Mistake | Fix |
|---|---|
| Building the map from a README, memory file, or old map | Those decay. Enumerate live schedulers first; use docs only as leads. |
| Interviewing before discovering | You'll ask lazy questions the filesystem could answer. Discover first. |
| Drawing disabled routines as live nodes | Disabled/retired = Changed tab, not a green dot. |
| Inventing edges because they "must" exist | An agent that probably reads the calendar gets no calendar edge until you've read its prompt/config. |
| Editing the template's render JS | All customization is in the DATA block and header. The JS is layout, leave it. |
| One giant open-ended "tell me about your system" question | Batch informed multiple-choice questions from the bank instead. |
