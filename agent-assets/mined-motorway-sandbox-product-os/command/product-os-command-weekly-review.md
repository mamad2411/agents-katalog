<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: End-of-week review combining progress tracking, stale work detection, operating retro, development priorities, AI/automation assessment, and goal-setting -->

# Weekly Review

End-of-week review: assess progress against goals, detect stale work, evaluate how you operated, check in on how you're feeling, review development priorities and AI/automation usage, identify actions, and set goals for the next period.

## Instructions

### Step 0: Parse arguments

- The user provides arguments in the format: `$ARGUMENTS`
- Expected format: `{initials}` (e.g. `CR` or `JK`)
- If no arguments are provided, check the auto-memory (MEMORY.md) for the user's initials before asking
- Use **initials** for all file paths (e.g. `team/{initials}/todo_list.md`, `team/{initials}/weekly-reviews/`)
- From the auto-memory or team context, identify:
  - The PM's **name** and **role/level** (e.g. Product Director, Senior PM, Lead PM)
  - Their **development priorities** if known (from performance reviews, coaching notes, etc.)
  - Their **team/squad** and the **outcome metric** they own (from `context/current-priorities.md`)

### Step 1: Gather data

Pull from all available sources. Run independent queries in parallel.

1. **Previous weekly review** — Check `team/{initials}/weekly-reviews/` for the most recent review file. Read it to get:
   - Last week's goal(s) — this is what you'll assess progress against
   - Themes or issues flagged last week — check if they recurred
   - Any monthly/quarterly goals if previously set
   - Previous development priority ratings and AI/automation observations — check for trends
2. **Todo list** — Read `team/{initials}/todo_list.md` and identify:
   - Items marked as done (`[x]`) — this week's completions
   - Items marked as dropped (`[-]`) — removed because no longer needed
   - Items still open — note overdue or expected-this-week items
3. **Git history** — Run `git log --since="7 days ago" --oneline --stat` to see what was committed this week
4. **Recently modified files** — Run `git diff --stat HEAD@{7.days.ago}..HEAD` to understand scope of changes
5. **Remote sync check** — Run `git fetch` then `git status` to check if the current branch is behind its remote tracking branch. If there are remote changes not reflected locally, flag this to the PM before proceeding
6. **Meetings** — Use `mcp__claude_ai_Granola__list_meetings` with `this_week` and `last_week` to get all meetings from the past 7 days. Then use `mcp__claude_ai_Granola__get_meetings` (batch, up to 10 IDs per call) to pull notes and summaries from each. If a meeting's notes are sparse (just a few words or empty), use `mcp__claude_ai_Granola__get_meeting_transcript` to pull the full transcript and summarise key points instead
7. **Current priorities** — Read `context/current-priorities.md` to understand team goals and Q-level priorities this PM is responsible for
8. **Goals** — Read `team/{initials}/me/goals.md` for monthly, quarterly, and development priorities
9. **Achievements** — Read `team/{initials}/me/achievements.md` for current state
10. **Decision log** — Read `team/{initials}/decision-log.md` (if it exists) for this week's decisions and unresolved follow-ups
11. **Recurring meeting context** — Read files in `team/{initials}/recurring-meeting-context/` for carry-forward item trends
12. **Claude Code usage** — Read the auto-memory files. List the commands in `.claude/commands/`. Review git history for patterns in what Claude was used for (command runs, file types created/edited, research vs execution). Check `.claude/commands/` and `scripts/` for new or modified automations
13. **Quarterly tracking changes** — Check for `team/{initials}/quarterly-tracking-changes-*.md` files from this week. If found, read them and incorporate any RAG changes, new risks, or milestone updates into the Progress Review

### Step 2: Progress Review

Assess progress across three levels:

**A. Against last week's goal**
- Pull the specific goal from the previous weekly review
- Assess: was meaningful progress made? What evidence exists?
- If the goal was missed or partially met, identify what got in the way

**B. Against team/squad goals**
- Check the PM's squad metric from `context/current-priorities.md`
- Look for evidence in meetings, documents, or data work that moved the needle on their owned metric
- Flag if the week's work was mostly aligned with their core metric or mostly pulled elsewhere

**C. Against quarterly priorities**
- Check the PM's initiatives in `context/current-priorities.md`
- Note any RAG changes, milestones hit, or risks emerging

**D. Against monthly/quarterly goals**
- Read `team/{initials}/me/goals.md`
- Assess progress against each active monthly and quarterly goal
- Flag any that are at risk or off track
- Note evidence of progress or blockers

Present this section and ask: "Does this capture your week fairly? Anything to add or correct?"

### Step 3: Stale Work Scan

Scan for stale items across the workspace.

**3a. Stale todo items:**
- Read `team/{initials}/todo_list.md`
- Flag open items where: due date passed by 2+ weeks, item open 3+ weeks without update, or high-priority items open 2+ weeks
- Categorise as: OVERDUE (due date passed), AGING (open too long), STUCK (high priority, not moving)

**3b. Dormant projects:**
- Use Glob to find files in `projects/`
- For each, check git log for last modification date
- Flag any not modified in 3+ weeks

**3c. Rolling 1:1 carry-forward items:**
- Read files in `team/{initials}/recurring-meeting-context/`
- Flag items carried forward 3+ weeks (check "added {date}" markers)

**3d. Unresolved decision follow-ups:**
- Read `team/{initials}/decision-log.md` (if it exists)
- Flag decisions with follow-up items 2+ weeks old and likely unresolved

Include stale work counts in the operating review. Only flag genuinely stale items — be conservative.

### Step 4: Operating Review

Analyse how the PM operated this week. Ground EVERY observation in specific evidence from the data — no generic advice.

**4a. What's working well (keep doing):**
- Specific strengths with evidence from this week
- Patterns that are working and should be maintained

**4b. What needs attention (stop/change):**
- Patterns or gaps with evidence
- Benchmark against what a high-performing person in this PM's role would do
- Specific, actionable recommendations

**4c. What's new or different (start doing):**
- New tools, habits, or approaches that emerged
- Opportunities spotted but not yet acted on

Present the top 3-5 observations (mix of strengths and improvements) and ask: "Do these resonate? Anything you'd push back on or add?"

### Step 5: Wellbeing Check

After reviewing the data, share your read on how the week felt — then ask the PM directly. This section captures the subjective side that evidence alone misses.

**5a. Your read (based on the data):**
Before asking, offer a hypothesis based on what you've seen. For example:
- A week with lots of completions but all reactive/tactical might signal "productive but unfulfilling"
- A week dominated by one blocker (e.g. hiring freeze) might signal frustration
- A week with strong strategic progress might signal momentum
- Heavy meeting load with few outputs might signal being stretched

Frame it as: "Based on what I'm seeing, this looks like it was a [X] kind of week — [brief reason]. How does that land?"

**5b. Ask the PM:**
Use `AskUserQuestion` with these prompts:

1. **Energy**: "How's your energy at the end of this week?" — options: High (energised, want to keep going), Medium (fine, normal week), Low (drained, need to recharge)
2. **Satisfaction**: "How satisfied are you with what you achieved?" — options: Very (meaningful progress on what matters), Somewhat (got things done but not the right things), Not really (week got away from me)
3. **One word**: "One word to describe the week?"

**5c. Capture what drained vs energised:**
Ask: "What drained you most this week? And what gave you energy?"

This is lightweight — 2-3 minutes. The value comes from tracking patterns over time (e.g. consistently low energy when meeting-heavy, or high satisfaction correlating with strategic work weeks).

### Step 6: Personal Development Review

Review how the PM is tracking against their development priorities this week. Pull these from `team/{initials}/me/goals.md` (Development Priorities section) or from the auto-memory.

For each priority:
- **Rating**: Strong / Some / Limited / None — based on evidence from this week
- **Trend**: ↑ / → / ↓ compared to previous weekly review (if available)
- **Evidence**: Specific examples from meetings, outputs, decisions this week
- If there's no evidence of progress on a priority this week, say so explicitly

Be honest and specific. This section is most valuable when it's candid.

Present and ask: "Fair assessment?"

### Step 7: AI & Automation Review

Assess how the PM is using AI tools and automation this week. This section tracks progress on building an AI-first workflow.

**Usage this week:**
- Which automations ran and produced useful output? (Check scripts/logs/ if accessible)
- What commands or agents were used? (Check git history for `.claude/` changes)
- What new commands, scripts, or workflows were built or improved?
- How is the PM using AI in their day-to-day work? (Research, analysis, writing, prototyping, coaching)

**System health:**
- Are existing automations producing value or just noise?
- Are there broken or stale automations that need fixing?
- What's the current command/script count? Any new additions?
- Are MCP integrations (Granola, Slack, Notion, BigQuery) working reliably?

**Opportunities:**
- Are there patterns in this week's work that could be automated but aren't?
- What manual, repetitive tasks appeared this week that a command or script could handle?
- Are there AI tools or workflows the PM's team is using that could be adopted more widely?
- Specific recommendations for improving the AI-first workflow

**AI capability building:**
- Is the PM advancing AI adoption across their team (not just personal use)?
- Evidence of coaching others on AI tools, sharing workflows, or building team capability

Present findings and include specific recommendations.

### Step 8: Suggested Actions

Based on Steps 2-7, propose 5-8 concrete actions split into three categories:

**Progress actions** — things that would move their goals and metrics forward:
- Unblock stalled priorities
- Follow up on commitments from meetings
- Advance strategic work that keeps slipping

**Operating actions** — things that would help them work more effectively:
- New automations or commands to build
- Habits to adopt or change
- Tools or integrations to start using
- Meeting or communication improvements

**Development actions** — things that move their development priorities forward:
- Cross-functional relationship investments
- Team coaching moments to create
- AI-first practices to adopt or share

Each action should have: description, priority (H/M/L), and a one-line rationale.

Present the actions and ask: "Which of these would you like to add to your todo list? Any you'd change or drop?"

### Step 9: Goal Setting

**Weekly goal:**
Based on the open todo items, upcoming meetings, quarterly priorities, and this week's themes, suggest 1-2 candidate goals for next week. The goal should be:
- A single, specific outcome (not a list of tasks)
- Directly tied to their most important priority or a recurring theme that needs breaking

Ask: "What's your main goal for next week?"

**Monthly/quarterly goal (if applicable):**
Check today's date:
- If it's the **last week of the month**: prompt the PM to reflect on the month and set a goal for next month. What should next month's theme be? What needs to shift?
- If it's the **last week of the quarter**: prompt the PM to reflect on the quarter against their OKRs/initiatives. What was delivered vs planned? What should the focus be for next quarter? What needs to change in how they operate?
- If it's the **first week of a month/quarter**: check if goals were set in the previous review and reference them

Use `AskUserQuestion` for goal-setting to keep it interactive.

### Step 10: Archive completed todos

After confirming the completed items:
1. Move all `[x]` (completed) and `[-]` (dropped) items out of the main table in `team/{initials}/todo_list.md`
2. Add them to an "## Archive" section at the bottom of the file, grouped under a week heading (e.g., "### Week of Feb 10"). Mark each with its status: **Done** or **Dropped**
3. Renumber remaining open items sequentially
4. Update summary counts
5. Only keep the last 4 weeks of archive history — older entries should be removed

### Step 11: Update todo list with accepted actions

For any actions the PM accepted in Step 8:
1. Add them to `team/{initials}/todo_list.md` following the existing format
2. Priority as discussed
3. Due date: "This week" for high priority, "TBD" for medium/low
4. Source: "Weekly Review ([date])"
5. Re-sort and renumber after adding

### Step 12: Update achievements log

Scan this week's completions, decisions, and outcomes for achievements worth recording:

1. Read `team/{initials}/me/achievements.md`
2. Look for items from this week that qualify as achievements:
   - **Experiments that shipped or produced results** (with quantified impact if available)
   - **Metrics that moved** — any owned metric that improved with evidence of the PM's contribution
   - **Strategy work that landed** — documents approved, presentations delivered, direction set
   - **Team milestones** — hires made, processes established, capability built
   - **Cross-functional wins** — alignment achieved, stakeholder buy-in secured, blockers removed
3. For each potential achievement:
   - Check it's not already in the achievements file (compare by meaning)
   - Determine the tier: Tier 1 (highest-impact strategic), Tier 2 (leadership/operating model), Tier 3 (supporting)
   - Write a concise bullet with quantified impact where possible
4. Suggest new achievements to the PM: "I found X potential achievements from this week. Want me to add them to your achievements log?"
5. If the PM confirms, add them to the appropriate tier section in `team/{initials}/me/achievements.md`
6. Update the "Last updated" date at the top of the file

### Step 13: Save the weekly review

1. Create `team/{initials}/weekly-reviews/` directory if it doesn't exist
2. Write the final review to `team/{initials}/weekly-reviews/review-YYYY-MM-DD.md` using today's date
3. Display the saved file path

## Review Template

```markdown
# Weekly Review — Week of [Monday date] to [Friday date]

## Progress Review

### Last Week's Goal
> **[Goal from previous review]**
>
> Assessment: [Met / Partially met / Not met] — [Evidence]

### Team Goal Progress
- Squad metric: [metric name] — [what moved this week, if anything]
- Key initiative status: [RAG and brief update]

### Monthly/Quarterly Goal Progress

| Goal | Status | Evidence |
|------|:------:|----------|
| Monthly goal 1 | On track / At risk / Off track | Brief evidence |

### Completed This Week

| # | Item | Source |
|:-:|------|--------|
| 1 | Description | Where it came from |

### Dropped This Week

| # | Item | Reason |
|:-:|------|--------|
| 1 | Item dropped | Why |

### Key Decisions & Outcomes
- Decision or outcome, with context

---

## Stale Work

### Stale Todo Items ({count})
### Dormant Projects ({count})
### Rolling 1:1 Items ({count})
### Unresolved Decision Follow-ups ({count})
[If nothing stale in a category, note "None — all current"]

---

## Operating Review

### What's Working Well (Keep Doing)
- Specific strength with evidence

### Areas to Sharpen (Stop/Change)
For each:
- **What I noticed**: Pattern or gap
- **Best practice benchmark**: What great [role] PMs do here
- **Recommendation**: Specific action

### New Opportunities (Start Doing)
- New approach or opportunity with rationale

---

## Wellbeing Check

- **Energy**: High / Medium / Low
- **Satisfaction**: Very / Somewhat / Not really
- **One word**: [word]
- **Drained by**: [what drained energy this week]
- **Energised by**: [what gave energy this week]

---

## Personal Development

| Priority | Rating | Trend | Evidence |
|----------|:------:|:-----:|----------|
| [Priority 1] | Strong/Some/Limited/None | ↑/→/↓ | Brief evidence |
| [Priority 2] | Strong/Some/Limited/None | ↑/→/↓ | Brief evidence |
| [Priority 3] | Strong/Some/Limited/None | ↑/→/↓ | Brief evidence |

---

## AI & Automation

### Usage This Week
- Commands/scripts used, new ones built, automations that ran
- How AI was used in day-to-day work (research, analysis, writing, prototyping)
- Team AI adoption: coaching, sharing workflows, capability building

### System Health
- [count] commands, [count] scripts. MCP integrations: [status]
- Broken or stale automations: [list or "none"]
- Uncommitted work: [count] files

### Recommendations
- Specific opportunities to automate or improve AI workflow
- Tools or integrations to explore

---

## Actions

| # | Action | Type | Priority | Rationale |
|:-:|--------|------|:--------:|-----------|
| 1 | Description | Progress / Operating / Development | H/M/L | Why |

---

## Goals

### Next Week
> **[Goal]**
>
> Why: [Rationale]

### [Next Month / Quarter — if applicable]
> **[Goal]**
>
> Why: [Rationale]

---

## Achievements Added
[Any new items added to achievements.md]

---

## Data Sources
[List all sources used]
```

## Important Notes

- Keep it concise — this is a personal development checkpoint, not a report for others
- Be honest and direct in the operating review; this is most valuable when it's candid
- Ground all observations in evidence from the actual data — no generic productivity advice
- When benchmarking, be specific about what "great" looks like for this person's role and level
- If there's limited activity data (few commits, sparse meetings), note this and adjust expectations
- The goal for next week should be a single outcome, not a list of tasks
- For monthly/quarterly goals, connect them to the PM's owned metrics and initiatives
- Don't skip the interactive questions — this works best as a conversation, not a dump
- For stale work: be conservative — only flag genuinely stale items
- For development priorities: be honest about whether there's evidence of progress or not
- For AI/automation: be practical — suggest specific improvements, not vague encouragement. Track system health week-over-week
- Don't skip the wellbeing check — it's lightweight (2-3 min) and the value comes from tracking patterns over time
- Don't skip achievement detection — these compound over time for performance reviews
- **Context management**: This is a long command (13 steps). If context is running low, prioritise Steps 1-9 (the review and goal-setting) over Steps 10-12 (file updates). File updates can be done in a follow-up `/todo` run. If you notice you're losing track of earlier data, summarise what you have and proceed with the interactive steps rather than re-reading files
