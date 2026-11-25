---
name: review
description: "Daily and weekly review rituals for Obsidian vaults. Morning planning, evening wrap-up, and weekly reflection using your vault data. Use when the user wants structured review habits or asks about their day/week."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: cognitive-toolkit
---

# Review Pack — "I never close the loop"

Structured review rituals that use your vault as the ground truth.

## Commands

### /today — Morning planning ritual

When the user invokes `/today`:

1. Gather context:
   - `obs daily open --json` — today's daily note (create if needed: `obs daily create`)
   - `obs daily open --date <yesterday> --json` — yesterday's note
   - `obs tasks pending --json` — all open tasks
   - `obs files list --since 1d --sort modified --json` — what changed yesterday
2. Analyze:
   - Unfinished tasks from yesterday
   - Open items carried forward
   - What was actively worked on (recently modified files)
   - Any scheduled items (check frontmatter for `due` dates matching today)
3. Generate a morning briefing:
   ```
   ## Today — YYYY-MM-DD

   ### Carried forward
   - [ ] [Unfinished task from yesterday]
   - [ ] [Open item]

   ### Active projects
   - [[project]] — last touched yesterday, [status]

   ### Suggested focus
   1. [Most important thing based on momentum + deadlines]
   2. [Second priority]
   3. [Third priority]

   ### Quick wins (< 15 min)
   - [ ] [Small tasks that can be knocked out]
   ```
4. Offer to write this plan into today's daily note
5. If the daily note already has content, append the plan rather than overwrite

### /closeday — Evening wrap-up ritual

When the user invokes `/closeday`:

1. Gather the day's data:
   - `obs daily open --json` — today's daily note
   - `obs files list --since 1d --sort modified --json` — everything touched today
   - `obs tasks pending --json` and `obs tasks done --json` — task progress
2. Analyze the day:
   - What files were created or significantly modified?
   - Which tasks were completed vs. still open?
   - What new notes or ideas appeared?
3. Generate an evening summary:
   ```
   ## End of day — YYYY-MM-DD

   ### Completed
   - [x] [Tasks finished]
   - [Files created/updated]

   ### Still open
   - [ ] [Remaining tasks — carry forward?]

   ### New ideas captured
   - [[new note]] — [one-line summary]

   ### Tomorrow
   - [ ] [Suggested priority based on what's open]
   ```
4. Offer to append this to today's daily note
5. Flag anything that's been open for more than a week as potentially stale

### /weekly — Weekly review and reflection

When the user invokes `/weekly`:

1. Gather the week's data:
   - `obs files list --since 1w --sort modified --json` — all files touched this week
   - `obs tasks pending --json` and `obs tasks done --json` — task overview
   - `obs tags all --json` — tag activity
   - `obs vault wordcount --json` — writing volume
2. Read a sample of the week's modified files to understand themes
3. Generate a weekly review:
   ```
   ## Weekly Review — Week of YYYY-MM-DD

   ### By the numbers
   - Files created: N
   - Files modified: N
   - Tasks completed: N
   - Tasks still open: N
   - Words written: ~N

   ### What you worked on
   - **[Area 1]**: [Summary of activity]
   - **[Area 2]**: [Summary of activity]

   ### Patterns this week
   - [Recurring themes or topics]
   - [Tags that saw the most activity]

   ### Stale projects
   - [[project]] — not touched in N days, M open tasks

   ### Emerging themes
   - [New topics or connections that appeared]

   ### Reflection prompts
   - What got the most energy this week?
   - What did you avoid?
   - What surprised you?
   ```
4. Offer to save as a weekly review note: `Reviews/YYYY-WNN.md`
5. Compare with previous weekly reviews if they exist for trend spotting

## Tips

- /today should be quick and actionable. Don't overwhelm — 3 priorities max.
- /closeday should create a sense of closure. Acknowledge what was done before listing what's left.
- /weekly is the most analytical. Take time to read files and find genuine patterns.
- Respect the user's daily note format. Read existing content before appending.
- Use yesterday's date for /closeday if invoked after midnight.
