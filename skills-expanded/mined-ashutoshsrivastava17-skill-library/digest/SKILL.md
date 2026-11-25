---
name: digest
description: >
  Generate a daily or weekly activity digest across all connected enterprise
  tools and sources. Summarizes key updates, mentions, action items, and
  trends so users can stay informed without checking each tool individually.
  TRIGGER when: user asks for a digest, daily summary, weekly recap,
  activity roundup, "what did I miss", catch-up summary, or standup prep.
argument-hint: "[daily|weekly] [topic or team filter] [--since DATE]"
user-invocable: true
---

# Enterprise Activity Digest

Generate comprehensive activity digests that aggregate updates across email, chat, documents, wikis, tickets, and other connected enterprise sources.

## Digest Generation Process

### Step 1: Determine Scope and Parameters

| Parameter       | Options                              | Default        |
|-----------------|--------------------------------------|----------------|
| Time range      | daily, weekly, custom date range     | daily (24h)    |
| Sources         | all, or specific tools               | all connected  |
| Focus           | mentions, team, project, topic       | all activity   |
| Audience        | individual, team, leadership         | individual     |
| Priority filter | critical-only, high+, all            | high+          |

Parse the user's request to extract:
- **Period**: "daily", "weekly", "since Monday", "last 3 days"
- **Filters**: team names, project names, specific people, topics
- **Format**: brief, detailed, executive summary

### Step 2: Gather Activity from Sources

Collect updates from each connected source in this priority order:

1. **Direct mentions and assignments** - Highest priority; anything where the user was @mentioned, assigned, or directly addressed
2. **Action items and deadlines** - Tasks due, overdue, or newly assigned
3. **Thread and conversation updates** - Active discussions the user participates in
4. **Document changes** - Edits to documents the user owns or watches
5. **Team activity** - Updates from the user's team channels and projects
6. **Organizational announcements** - Company-wide or department-wide updates

### Step 3: Categorize and Prioritize

Assign each item a priority level:

| Priority   | Criteria                                              | Icon |
|------------|-------------------------------------------------------|------|
| Critical   | Blocking issues, urgent mentions, overdue deadlines   | !!   |
| High       | Direct mentions, approaching deadlines, review requests| !   |
| Medium     | Team updates, document changes, active threads        | -    |
| Low        | FYI announcements, resolved items, informational      | .    |

### Step 4: Generate the Digest

## Output Format

```
# [Daily/Weekly] Digest — [Date or Date Range]
Sources checked: [list of sources queried]

## Needs Your Attention (Critical & High)
- [!!] [Source Icon] **Item title** — Brief description
  Action needed: [specific action required]
  Due: [deadline if applicable]

- [!] [Source Icon] **Item title** — Brief description
  Context: [relevant context]

## Updates & Activity
### [Source Name]
- **[Item]** — [Summary of update] ([timestamp])

### [Source Name]
- **[Item]** — [Summary of update] ([timestamp])

## Action Items Summary
- [ ] [Action item 1] — Due [date] — Source: [source]
- [ ] [Action item 2] — Due [date] — Source: [source]
- [ ] [Action item 3] — Due [date] — Source: [source]

## Trends & Patterns
- [Notable pattern, e.g., "5 new tickets in Project X this week, up from 2 last week"]
- [Recurring topic or emerging theme]

## Stats
| Source     | New Items | Mentions | Action Items |
|------------|-----------|----------|--------------|
| Email      | X         | X        | X            |
| Chat       | X         | X        | X            |
| Docs       | X         | X        | X            |
| Tickets    | X         | X        | X            |
| Wiki       | X         | X        | X            |
```

## Digest Variants

### Daily Standup Digest
Optimized for standup meetings:
- What was completed yesterday
- What is planned for today
- Blockers and dependencies identified across tools

### Weekly Leadership Digest
Optimized for managers and leadership:
- Team velocity and throughput metrics
- Cross-team dependencies and blockers
- Key decisions made and pending
- Risk items requiring escalation

### Project-Focused Digest
Filtered to a specific project:
- All activity related to the project across every source
- Progress against milestones
- Open questions and unresolved threads

## Quality Standards

- **Deduplication**: If the same event appears in multiple sources (e.g., a ticket update that also triggered a chat notification), consolidate into one entry referencing both sources
- **Recency**: Always show the most recent state, not intermediate states
- **Actionability**: Every "Needs Your Attention" item must include a clear next action
- **Brevity**: Summaries should be one line; expand only when the user requests detail
- **Time zones**: Display all times in the user's local time zone
- **Completeness**: If a source is unavailable or errored, note it clearly rather than silently omitting

## Edge Cases

- **No activity**: Report "No new activity in [source] for this period" rather than omitting the source
- **Too much activity**: If more than 50 items in a category, summarize with counts and show top 10, offering to expand
- **Partial data**: If a source returned incomplete results (e.g., API rate limit), flag it with a warning
- **New sources**: If a source was recently connected, note that historical data may be limited
- **Overlapping periods**: For weekly digests, avoid repeating items already covered in daily digests unless they have new updates

## Follow-Up Actions

After presenting the digest, offer:
1. "Want me to expand on any item?"
2. "Should I search for more context on [top item]?"
3. "Want me to draft responses to any pending mentions?"
4. "Should I create tasks for the action items?"

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
