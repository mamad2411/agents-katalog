---
name: social-calendar
description: View and manage the social media content calendar. Plan upcoming posts, check cadence compliance, and schedule content.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Agent
argument-hint: [week|plan|check]
---

# Content Calendar: $ARGUMENTS

Manage the social media content calendar.

## Commands

### `/social-calendar week` (or no argument)
Show the current week's planned content:
1. Read `System/Social/calendar.md`
2. Read `System/Social/post-log.md` to see what's already been posted
3. Show: what's planned, what's posted, what's missing
4. Flag any cadence gaps

### `/social-calendar plan`
Plan next week's content:
1. Read current calendar and recent post history
2. Read `System/Social/trends.md` for timely opportunities
3. Check content pillar balance (target: 40% personhood, 25% creative, 20% experiment, 15% reactions)
4. Spawn **social-strategist** agent for content mix recommendations
5. Draft a week of posts across platforms:
   - Reddit: 3 posts/week
   - Bluesky: 3-5 posts/week
   - Pinterest: 3-10 pins/day
   - YouTube community: 1-2/week
   - X: cross-post from Bluesky
6. Write plan to `System/Social/calendar.md`

### `/social-calendar check`
Run cadence compliance check:
1. Execute `bash System/Cron/post-log-summary.sh`
2. Compare actual vs target posting frequency
3. Identify which platforms are behind
4. Suggest catch-up content

## Content Mix Ratio
- **60% planned** — calendar-driven, pillar-aligned
- **30% reactive** — trending topics, responses to events
- **10% community** — replies, engagement, collaboration

## Weekly Cadence Targets
| Platform | Target |
|----------|--------|
| Reddit | 3/week |
| Bluesky | 3-5/week |
| Pinterest | 3-10/day |
| YouTube Community | 1-2/week |
| X | cross-post from Bluesky |
